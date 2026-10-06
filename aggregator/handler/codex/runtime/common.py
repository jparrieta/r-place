"""Filesystem boundaries, atomic state and process-safe locks. No model calls."""
from pathlib import Path
import contextlib, datetime, fcntl, hashlib, json, os, re, shutil, stat, tempfile, uuid

CODEX = Path(__file__).resolve().parents[1]   # aggregator/handler/codex (restructure 2026-10-02)
REPO = CODEX.parents[2]                        # the repository root, rplace/
ROOT = REPO.parent
# v43 is a separate instrument. Never adopt v42 actors, jobs or login state.
DATA = ROOT / '.rplace-runtime-v43'
TMP = DATA / 'tmp'
class Error(RuntimeError): pass

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def identity(value):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,119}', value) or '..' in value:
        raise Error('Invalid identifier: ' + repr(value))
    return value

def inside(path, base=ROOT):
    p = Path(path).expanduser().resolve()
    if not p.is_relative_to(Path(base).resolve()): raise Error('Path leaves the workspace: ' + str(p))
    return p

def read(path, default=None):
    p=Path(path)
    return json.loads(p.read_text()) if p.exists() else default

def atomic(path, data):
    p=inside(path); p.parent.mkdir(parents=True, exist_ok=True)
    b=data.encode() if isinstance(data,str) else data
    q=p.with_name('.'+p.name+'.'+uuid.uuid4().hex)
    try:
        with q.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
        os.replace(q,p)
        fd=os.open(p.parent,os.O_RDONLY)
        try: os.fsync(fd)
        finally: os.close(fd)
    finally: q.unlink(missing_ok=True)

def write(path, data): atomic(path,json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

@contextlib.contextmanager
def lock(path, wait=False):
    p=inside(path); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a') as f:
        try: fcntl.flock(f,fcntl.LOCK_EX | (0 if wait else fcntl.LOCK_NB))
        except BlockingIOError: raise Error('Resource is busy: '+str(p))
        try: yield
        finally: fcntl.flock(f,fcntl.LOCK_UN)

def event(path, **data):
    with lock(str(path)+'.lock',wait=True):
        p=inside(path); p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('a') as f: f.write(json.dumps({'utc':now(),**data},ensure_ascii=False)+'\n'); f.flush(); os.fsync(f.fileno())

def ensure_space(need=0):
    DATA.mkdir(parents=True,exist_ok=True)
    if shutil.disk_usage(DATA).free - need < 8*1024**3:
        raise Error('Insufficient free space: preserve the 8 GiB reserve')

def files(root):
    root=inside(root)
    for d,dirs,names in os.walk(root,followlinks=False):
        for n in dirs+names:
            p=Path(d)/n
            if p.is_symlink(): raise Error('Symlink not allowed in managed workspace: '+str(p))
        dirs[:]=sorted(x for x in dirs if x not in ('__pycache__','.git','.cc','.claude'))
        for n in sorted(names):
            p=Path(d)/n
            if n.endswith('.pyc'): continue
            if not stat.S_ISREG(p.stat().st_mode): raise Error('Not a regular file: '+str(p))
            yield p

def inventory(root):
    return {str(p.relative_to(root)):{'sha256':sha(p),'bytes':p.stat().st_size,'mode':stat.S_IMODE(p.stat().st_mode)} for p in files(root)}

def copy_tree(src,dst):
    src=inside(src); dst=inside(dst); dst.mkdir(parents=True,exist_ok=True)
    for p in files(src):
        q=dst/p.relative_to(src); q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,q)
    for d,dirs,names in os.walk(src):
        dirs[:]=[n for n in dirs if n not in ('__pycache__','.git','.cc','.claude')]
        (dst/Path(d).relative_to(src)).mkdir(parents=True,exist_ok=True)

def env(home=None, scratch=None):
    TMP.mkdir(parents=True,exist_ok=True)
    e={k:v for k,v in os.environ.items() if k not in ('BASH_ENV','ENV') and not k.startswith(('ANTHROPIC_','OPENROUTER_','OPENAI_','CODEX_','CLAUDE_'))}
    e.update(TMPDIR=str(TMP),TMP=str(TMP),TEMP=str(TMP),PYTHONDONTWRITEBYTECODE='1',PYTHONPYCACHEPREFIX=str(DATA/'pycache'),XDG_CACHE_HOME=str(DATA/'cache'))
    if scratch:
        scratch=inside(scratch)
        for name in ('tmp','cache','pycache'):(scratch/name).mkdir(parents=True,exist_ok=True)
        e.update(TMPDIR=str(scratch/'tmp'),TMP=str(scratch/'tmp'),TEMP=str(scratch/'tmp'),XDG_CACHE_HOME=str(scratch/'cache'),PYTHONPYCACHEPREFIX=str(scratch/'pycache'))
    if home: e['CODEX_HOME']=str(inside(home))
    return e

def actor_dir(actor): return DATA/'actors'/identity(actor)
def actor_state(actor): return read(actor_dir(actor)/'state.json') or (_ for _ in ()).throw(Error('Unknown actor '+actor))
