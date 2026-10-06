"""Bind native case histories to exact corpus revisions, never replace a missing lead."""
import csv, json, tarfile
from .common import *
from . import archive

REGISTRY=DATA/'case-leads.json'
CORPUS=REPO/'aggregator/input/coders/rooms'
TRIPLET=('case.md','codes.jsonl','themes.jsonl')

def hashes(room):
    room=inside(room)
    if any(not (room/n).is_file() for n in TRIPLET): raise Error('Incomplete case triplet: '+str(room))
    return {n:sha(room/n) for n in TRIPLET}

def inspect_checkpoint(checkpoint, expected=None):
    src=DATA/'checkpoints'/identity(checkpoint)
    if not (src/'COMMITTED').is_file() or sha(src/'agent.tar.gz')!=(src/'COMMITTED').read_text().strip():
        raise Error('Lead checkpoint is not committed or its hash differs')
    m=archive.verify(src/'agent.tar.gz'); receipt=read(src/'receipt.json',{})
    if receipt.get('sha256')!=(src/'COMMITTED').read_text().strip():
        raise Error('Lead receipt and committed archive hash differ')
    if m.get('format')!='rplace-native-v1' or m.get('boundary')!='completed':
        raise Error('Case lead requires a completed native checkpoint')
    if sha(src/'runtime.tar.gz')!=receipt.get('runtime_archive_sha256'): raise Error('Lead runtime archive hash differs')
    with tarfile.open(src/'agent.tar.gz') as tf: st=json.load(tf.extractfile('state.json'))
    if st.get('origin_role',st.get('role')) not in ('case-reader','case-lead','labeler'):
        raise Error('Checkpoint is not a case lead or its return continuation')
    if not st.get('thread_id') or not st.get('last_turn_id'): raise Error('Lead native boundary identity missing')
    if expected:
        candidates=[Path(n).parent for n in m['files'] if n.startswith('workspace/') and Path(n).name=='case.md']
        if not any(all(m['files'].get(str(folder/n),{}).get('sha256')==digest for n,digest in expected.items()) for folder in candidates):
            raise Error('Native lead files do not match this corpus revision')
    return {'checkpoint':checkpoint,'sha256':receipt['sha256'],'thread_id':st['thread_id'],
            'last_turn_id':st['last_turn_id'],'model':st['model'],'effort':st['effort']}

def bind(sub,checkpoint):
    identity(sub); expected=hashes(CORPUS/sub); rec=inspect_checkpoint(checkpoint,expected)
    with lock(DATA/'locks/case-leads.lock'):
        registry=read(REGISTRY,{'rooms':{}}); registry['rooms'][sub]={**rec,'corpus':expected,'utc':now()}
        write(REGISTRY,registry)
    return registry['rooms'][sub]

def require(sub, expected=None):
    rec=read(REGISTRY,{}).get('rooms',{}).get(sub)
    if not rec: raise Error('No native lead registered for '+sub+'; fresh readers are forbidden at D2')
    expected=expected or hashes(CORPUS/sub)
    if rec.get('corpus')!=expected: raise Error('Registered lead is for an older corpus revision: '+sub)
    checked=inspect_checkpoint(rec['checkpoint'],expected)
    if any(checked[k]!=rec.get(k) for k in checked): raise Error('Lead registry identity mismatch: '+sub)
    return rec

def preflight():
    rooms=sorted(p.name for p in CORPUS.iterdir() if p.is_dir())
    ready=[]; blocked=[]
    for sub in rooms:
        try: require(sub);ready.append(sub)
        except (Error,OSError,ValueError) as e: blocked.append({'sub':sub,'reason':str(e)})
    return {'rooms':len(rooms),'ready':len(ready),'blocked':len(blocked),'ready_rooms':ready,'problems':blocked,
            'research_ready':not blocked,'live_native_acceptance':'separate from archive identity checks'}
