"""Concurrent JSON-RPC client. One owner per native home; responsive interrupt/steer."""
import json, os, queue, shutil, signal, subprocess, threading, time, sys, uuid
from pathlib import Path
from .common import Error, DATA, TMP, inside, write, sha, env, now

def bundled_executables():
    """Known macOS app locations, checked only when PATH has no Codex CLI."""
    return [base/relative for base in (Path('/Applications'), Path.home()/'Applications')
            for relative in ('ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex',
                             'Codex.app/Contents/Resources/codex')]

def resolve_executable(executable=None, required=True):
    """Find a new runtime. An explicit archived runtime never falls back."""
    if executable is not None:
        path=Path(executable).expanduser()
        if path.is_file() and os.access(path,os.X_OK): return str(path.resolve())
        raise Error('Recorded Codex executable is unavailable: '+str(path)+'. Restore its recorded runtime; no fallback was selected.')
    candidate=shutil.which('codex')
    for path in ([Path(candidate)] if candidate else [])+bundled_executables():
        if path.is_file() and os.access(path,os.X_OK): return str(path.resolve())
    if required: raise Error('Codex CLI not found on PATH or in the installed ChatGPT/Codex app. Install the app or make the CLI available on PATH, then retry.')
    return None

class Native:
    def __init__(self, home, cwd, executable=None, on_event=None):
        self.home=inside(home); self.home.mkdir(parents=True,exist_ok=True)
        self.cwd=inside(cwd); self.callback=on_event or (lambda m:None)
        self.exe=resolve_executable(executable)
        self.pending={}; self.questions={}; self.sequence=0; self.guard=threading.RLock(); self.closed=False
        self.stderr=(self.home/'server.stderr.log').open('ab')
        self.p=subprocess.Popen([self.exe,'app-server','--stdio'],cwd=self.cwd,env=env(self.home,self.home.parent/'scratch'),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.stderr,start_new_session=True,text=True,bufsize=1)
        self.events=queue.Queue()
        self.event_reader=threading.Thread(target=self._events,daemon=True); self.event_reader.start()
        self.reader=threading.Thread(target=self._read,daemon=True); self.reader.start()
        try:
            self.call('initialize',{'clientInfo':{'name':'rplace','version':'1.0.0'},'capabilities':{'experimentalApi':True}},timeout=30)
            self.send({'method':'initialized'})
        except BaseException: self.close(); raise
    def send(self,m):
        with self.guard:
            if self.p.poll() is not None: raise Error('Codex app-server exited')
            self.p.stdin.write(json.dumps(m)+'\n'); self.p.stdin.flush()
    def _read(self):
        try:
            for line in self.p.stdout:
                try: m=json.loads(line)
                except ValueError: continue
                if 'id' in m and 'method' not in m:
                    q=self.pending.get(m['id'])
                    if q: q.put(m)
                elif 'id' in m:
                    if not self.question_request(m):
                        # Research questions are separate from permission and credential grants.
                        self.send({'id':m['id'],'error':{'code':-32601,'message':'This managed actor does not accept approval or credential requests'}})
                else:
                    if m.get('method')=='serverRequest/resolved':
                        with self.guard:
                            self.questions={k:v for k,v in self.questions.items() if v['id']!=m.get('params',{}).get('requestId')}
                    elif m.get('method')=='turn/completed':
                        turn=m.get('params',{}).get('turn',{}).get('id')
                        with self.guard:self.questions={k:v for k,v in self.questions.items() if v['params'].get('turnId')!=turn}
                    self.events.put(m)
        finally:
            for q in list(self.pending.values()): q.put({'error':{'message':'Codex connection closed'}})
            if not self.closed:self.events.put({'method':'rplace/nativeDisconnected','params':{}})
    def question_request(self,m):
        if m.get('method')!='item/tool/requestUserInput':return False
        p=m.get('params',{});questions=p.get('questions',[])
        if not questions or len(questions)>3 or any(q.get('isSecret') or not q.get('id') for q in questions):return False
        key=uuid.uuid4().hex
        with self.guard:self.questions[key]=m
        self.events.put({'method':m['method'],'params':{**p,'requestId':m['id'],'requestKey':key}})
        return True
    def answer(self,key,answers,thread,turn):
        with self.guard:
            m=self.questions.get(key)
            if not m or m['params'].get('threadId')!=thread or m['params'].get('turnId')!=turn:
                raise Error('Question is no longer pending on this live turn. Refresh before replying.')
            ids={q['id'] for q in m['params']['questions']}
            if not isinstance(answers,dict) or set(answers)!=ids or any(not isinstance(v,str) or not v.strip() or len(v)>20000 for v in answers.values()):
                raise Error('Supply one nonempty answer for every question')
            self.send({'id':m['id'],'result':{'answers':{k:{'answers':[v]} for k,v in answers.items()}}})
            self.questions.pop(key,None)
        return {'answered':key,'new_turn_started':False}
    def _events(self):
        while True:
            m=self.events.get()
            if m is None: return
            try: self.callback(m)
            except Exception as e:
                self.callback_error=str(e)
                try:write(self.home.parent/'callback-error.json',{'error':str(e),'utc':now(),'method':m.get('method')})
                except Exception:pass
    def call(self,method,params=None,timeout=90):
        with self.guard:
            self.sequence+=1; i=self.sequence; q=queue.Queue(); self.pending[i]=q
        try:
            self.send({'id':i,'method':method,'params':params or {}})
            try: r=q.get(timeout=timeout)
            except queue.Empty: raise Error('Timed out waiting for '+method)
            if 'error' in r: raise Error(method+': '+json.dumps(r['error']))
            return r.get('result',{})
        finally: self.pending.pop(i,None)
    def close(self):
        if self.closed: return
        self.closed=True
        if self.p.poll() is None:
            self.p.stdin.close()
            try: self.p.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(self.p.pid,signal.SIGTERM)
                try: self.p.wait(timeout=5)
                except subprocess.TimeoutExpired: os.killpg(self.p.pid,signal.SIGKILL); self.p.wait()
        try: os.killpg(self.p.pid,0)
        except ProcessLookupError: pass
        else: os.killpg(self.p.pid,signal.SIGKILL)
        self.reader.join(timeout=5)
        self.events.put(None)
        if self.p.stdout: self.p.stdout.close()
        if self.p.stdin and not self.p.stdin.closed: self.p.stdin.close()
        self.stderr.close()


def configure(home,model,effort,workspace=None,readonly=False,stage=None,probe=False,interactive=True):
    home=inside(home); home.mkdir(parents=True,exist_ok=True)
    ws=inside(workspace or home.parent/'workspace')
    entries={':minimal':'read',str(ws):'read',str(ws/'out'):'read' if readonly else 'write',str(ws/'RUN.json'):'read' if readonly else 'write',str(ws/'out/_transcripts'):'deny',str(ws/'out/_probe'):'deny',str(ws/'out/_answers'):'read'}
    scratch=inside(home.parent/'scratch')
    for name in ('tmp','cache','pycache'):(scratch/name).mkdir(parents=True,exist_ok=True)
    entries[str(scratch)]='write'
    # A venv keeps packages locally but loads its stdlib from the base install.
    python_roots={str(Path(p).resolve()):'read' for p in (sys.prefix,sys.base_prefix,sys.base_exec_prefix)}
    entries.update(python_roots)
    if probe: entries={':minimal':'read',**python_roots,str(ws):'deny',str(scratch):'write'}
    entries.update({'/tmp':'deny','/private/tmp':'deny','/var/tmp':'deny','/private/var/tmp':'deny','/private/var/folders':'deny'})
    if stage in ('E1','E2'):
        entries.pop(str(ws/'out/_transcripts'),None); entries.pop(str(ws/'out/_probe'),None)
    shell_env={'PATH':str(Path(sys.executable).parent)+':/usr/bin:/bin:/usr/sbin:/sbin',
               'TMPDIR':str(scratch/'tmp'),'TMP':str(scratch/'tmp'),'TEMP':str(scratch/'tmp'),
               'TMPPREFIX':str(scratch/'tmp/zsh'),
               'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1',
               'PYTHONPYCACHEPREFIX':str(scratch/'pycache'),'XDG_CACHE_HOME':str(scratch/'cache')}
    text='\n'.join(['model = '+json.dumps(model),'model_reasoning_effort = '+json.dumps(effort),'approval_policy = "never"','default_permissions = "rplace"','cli_auth_credentials_store = "file"','web_search = "disabled"','allow_login_shell = false','[shell_environment_policy]','inherit = "core"','ignore_default_excludes = false','exclude = ["PYTHONHOME", "PYTHONPATH", "BASH_ENV", "ENV"]','[shell_environment_policy.set]']+[json.dumps(k)+' = '+json.dumps(v) for k,v in shell_env.items()]+['[features]','default_mode_request_user_input = '+('true' if interactive and not probe else 'false'),'multi_agent = false','multi_agent_v2 = false','[analytics]','enabled = false','[permissions.rplace.filesystem]']+[json.dumps(k)+' = '+json.dumps(v) for k,v in entries.items()]+['[permissions.rplace.network]','enabled = false',''])
    (home/'config.toml').write_text(text)

def auth_to(home):
    src=DATA/'login/auth.json'; dest=inside(home)/'auth.json'
    if not src.exists(): return False
    shutil.copyfile(src,dest); dest.chmod(0o600); return True

def fingerprint(exe):
    path=Path(exe).resolve()
    result={'executable':str(path),'sha256':sha(path),'platform':os.uname().sysname,'machine':os.uname().machine}
    # The desktop package also owns code-mode-host, shell resources and rg.
    # Capturing only CodexCLI.app produces a CLI that chats but cannot run tools.
    for package in path.parents:
        if (package/'codex-package.json').is_file():
            members=list(package.rglob('*'))
            if any(p.is_symlink() for p in members): raise Error('Pinned runtime package contains a symbolic link')
            result.update(package_root=str(package),package_executable=str(path.relative_to(package)),
                          package_files={str(p.relative_to(package)):sha(p) for p in members if p.is_file()})
            return result
    if os.uname().sysname=='Darwin' and len(path.parents)>2 and path.parents[2].suffix=='.app':
        result['app_bundle']=str(path.parents[2]); result['bundle_executable']=str(path.relative_to(path.parents[2]))
        result['bundle_files']={str(p.relative_to(path.parents[2])):sha(p) for p in path.parents[2].rglob('*') if p.is_file()}
    return result


def process_identity(pid):
    result=subprocess.run(['/bin/ps','-p',str(int(pid)),'-o','lstart=','-o','comm='],capture_output=True,text=True)
    return result.stdout.strip() if result.returncode==0 else None
