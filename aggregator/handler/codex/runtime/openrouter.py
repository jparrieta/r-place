"""Text-only OpenRouter actors with private histories and cancellable local transport.

These are conversation replays, not native Codex or Claude sessions. No tool loop.
"""
import copy, getpass, json, os, subprocess, sys, threading, time, uuid
from urllib.parse import quote
from .common import *

INSTRUCTIONS='You are an independent research packet reader. Read only the supplied packet and shared material. Follow its return specification exactly. Do not consult other agents. Do not use tools or the network.'

def key():
    secret=os.environ.get('OPENROUTER_API_KEY') or os.environ.get('OPENROUTER_KEY')
    if not secret:
        try:
            r=subprocess.run(['security','find-generic-password','-s','openrouter','-a',getpass.getuser(),'-w'],capture_output=True,text=True,timeout=15)
            if r.returncode==0: secret=r.stdout.strip()
        except (OSError,subprocess.TimeoutExpired): pass
    if not secret: raise Error('OpenRouter credential missing. Set OPENROUTER_API_KEY for the controller or use Keychain service openrouter, account '+getpass.getuser())
    return secret

class Transport:
    def __init__(self,record=None):
        self.guard=threading.Lock(); self.proc=None; self.cancelled=threading.Event(); self.record=record
    def cancel(self):
        self.cancelled.set()
        with self.guard:
            if self.proc and self.proc.poll() is None: self.proc.terminate()
    def call(self,path,body=None,timeout=900):
        secret=key()
        with self.guard:
            if self.cancelled.is_set(): raise Error('OpenRouter request interrupted')
            self.proc=subprocess.Popen([sys.executable,'-I','-S','-B',str(CODEX/'runtime/openrouter_http.py')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,cwd=ROOT,env=env())
            proc=self.proc
            if self.record:
                from .native import process_identity
                write(self.record,{'pid':proc.pid,'identity':process_identity(proc.pid),'utc':now()})
        try:
            out,_=proc.communicate(json.dumps({'key':secret,'path':path,'body':body,'timeout':timeout}),timeout=timeout+10)
            if self.cancelled.is_set(): raise Error('OpenRouter request interrupted; remote billing may have occurred')
            if proc.returncode: raise Error('OpenRouter transport process exited; request outcome may be unknown')
            try: result=json.loads(out)
            except ValueError: raise Error('OpenRouter transport returned invalid JSON')
            if result.get('error'): raise Error(result['error'])
            return result['data']
        except subprocess.TimeoutExpired:
            proc.kill(); proc.communicate(); raise Error('OpenRouter timeout; no automatic inference retry')
        finally:
            if proc.poll() is None:
                proc.kill(); proc.communicate()
            with self.guard: self.proc=None
            if self.record: Path(self.record).unlink(missing_ok=True)

def evidence(reply,transport):
    if not isinstance(reply,dict) or reply.get('error'): raise Error('OpenRouter returned an error or non-object response')
    gid=reply.get('id')
    if not isinstance(gid,str) or not gid: raise Error('Missing OpenRouter generation ID')
    generation={}
    for attempt in range(3):
        try:
            result=transport.call('generation?id='+quote(gid,safe=''),timeout=30)
            data=result.get('data',result) if isinstance(result,dict) else {}
            if isinstance(data,dict): generation=data
            if generation.get('model') and generation.get('provider_name'): break
        except Error: pass
        if attempt<2:
            if transport.cancelled.wait(1): raise Error('OpenRouter metadata lookup interrupted')
    model=generation.get('model') or reply.get('model')
    provider=generation.get('provider_name') or reply.get('provider')
    if not isinstance(model,str) or '/' not in model or model.startswith('@preset/') or not isinstance(provider,str) or not provider:
        raise Error('Served model/provider could not be verified; response retained, no inference retry')
    return {'model':model,'provider':provider,'generation_id':gid,'generation':generation,'response_model':reply.get('model')}

def payload(config,messages,binding=None):
    body={'model':binding['model'] if binding else config['model'],'messages':copy.deepcopy(messages),'stream':False,
          'max_tokens':config.get('max_tokens',16000),'tools':[],'tool_choice':'none','plugins':[],'transforms':[],
          'provider':{'allow_fallbacks':False,'require_parameters':True},'reasoning':{'effort':config['effort']}}
    if binding: body['provider']['only']=[binding['provider']]
    if 'temperature' in config: body['temperature']=config['temperature']
    return body

def bind(root,config):
    """One trivial probe per study, never a research packet. Persist before dispatch."""
    path=root/'openrouter-binding.json'; prior=read(path)
    if prior:
        if prior['alias']!=config['model']: raise Error('OpenRouter alias changed within study')
        return prior
    probe=root/'openrouter-preflight'; probe.mkdir(exist_ok=True)
    check_process(probe/'http-process.json')
    transport=Transport(probe/'http-process.json')
    body=payload({**config,'max_tokens':1024},[{'role':'user','content':'Reply READY. No tools.'}])
    write(probe/'request.json',body)
    # Reuse an existing paid response if metadata retrieval was interrupted.
    reply=read(probe/'response.json')
    if reply is None:
        reply=transport.call('chat/completions',body,config.get('timeout',900)); write(probe/'response.json',reply)
    info=evidence(reply,transport)
    binding={**info,'alias':config['model'],'utc':now(),'preset_scope':'model/provider selection only; request parameters come from frozen arm'}
    write(path,binding); return binding

def check_process(path):
    previous=read(path)
    if previous:
        from .native import process_identity
        if previous.get('identity') and process_identity(previous['pid'])==previous['identity']:
            raise Error('Recorded OpenRouter HTTP process is still alive; no second owner allowed')

def create(actor,workspace,config,binding):
    base=actor_dir(actor)
    with lock(DATA/'locks'/('create-'+identity(actor)+'.lock')):
        if base.exists(): raise Error('Actor already exists')
        ensure_space(); base.mkdir(parents=True)
        copy_tree(workspace,base/'workspace'); (base/'workspace/out').mkdir(exist_ok=True)
        state={'id':actor,'backend':'openrouter','role':'reader','model':binding['model'],'alias':config['model'],'effort':config['effort'],
               'config':copy.deepcopy(config),'binding':copy.deepcopy(binding),'status':'prepared','thread_id':uuid.uuid4().hex,
               'active_turn_id':None,'last_turn_id':None,'boundary':None,'created_utc':now(),'run':None,'read_only':True,
               'instructions':INSTRUCTIONS,'runtime':{'format':'rplace-openrouter-v1','adapter_sha256':sha(Path(__file__))}}
        write(base/'state.json',state); write(base/'thread.json',{'messages':[{'role':'system','content':INSTRUCTIONS}],'turns':[]})
    return state

class Actor:
    def __init__(self,actor):
        self.base=actor_dir(actor); self.state=actor_state(actor); self.guard=threading.RLock()
        self.condition=threading.Condition(self.guard); self.lease=None; self.worker=None; self.transport=None
    def save(self): write(self.base/'state.json',self.state)
    def emit(self,method,**params): event(self.base/'events.jsonl',native={'method':method,'params':params})
    def open(self):
        with self.guard:
            if actor_state(self.state['id']).get('evicted'):raise Error('Actor store is archived. Restore checkpoint '+str(self.state.get('checkpoint'))+' as a new actor.')
            if not self.lease:
                lease=lock(self.base/'owner.lock'); lease.__enter__(); self.lease=lease
                try: check_process(self.base/'http-process.json')
                except Exception:
                    self.release(); raise
                self.state=actor_state(self.state['id'])
                if self.state.get('active_turn_id'):
                    self.state.update(active_turn_id=None,status='interrupted',boundary='interrupted',error='Previous process ended during an HTTP turn. Evidence retained; inspect before retry.')
                    self.save()
            return self.state
    def release(self):
        with self.guard:
            if self.worker and self.worker.is_alive(): return
            if self.lease: self.lease.__exit__(None,None,None); self.lease=None
    def message(self,text):
        if not isinstance(text,str) or not text.strip(): raise Error('Message is empty')
        ensure_space(); self.open()
        with self.guard:
            if self.state.get('active_turn_id') or (self.worker and self.worker.is_alive()):
                raise Error('OpenRouter turn is in flight. Wait or stop and save; mid-turn steering is unavailable.')
            turn=uuid.uuid4().hex
            self.state.update(active_turn_id=turn,status='working',error=None); self.save()
            self.emit('item/completed',item={'type':'userMessage','content':[{'text':text}]})
            event(self.base/'messages.jsonl',role='user',text=text)
            self.transport=Transport(self.base/'http-process.json'); self.worker=threading.Thread(target=self._turn,args=(turn,text),daemon=True); self.worker.start()
            return {'turn':{'id':turn,'status':'working'}}
    def _turn(self,turn,text):
        target=self.base/'turns'/turn; target.mkdir(parents=True)
        try:
            thread=read(self.base/'thread.json'); messages=thread['messages']+[{'role':'user','content':text}]
            body=payload(self.state['config'],messages,self.state['binding']); write(target/'request.json',body)
            response=self.transport.call('chat/completions',body,self.state['config'].get('timeout',900)); write(target/'response.json',response)
            info=evidence(response,self.transport); write(target/'routing.json',info)
            if (info['model'],info['provider'])!=(self.state['binding']['model'],self.state['binding']['provider']):
                raise Error('Served model/provider differs from pinned arm; response quarantined')
            choices=response.get('choices')
            if not isinstance(choices,list) or len(choices)!=1 or not isinstance(choices[0],dict): raise Error('Expected one completion')
            choice=choices[0]; message=choice.get('message',{})
            if message.get('tool_calls') or message.get('function_call'): raise Error('Text reader returned tools; not executed')
            if choice.get('finish_reason')!='stop': raise Error('OpenRouter stopped with '+str(choice.get('finish_reason'))+'; inspect token ceiling or refusal before retry')
            if not isinstance(message.get('content'),str): raise Error('Expected text reader return')
            # Carry reasoning details unchanged when provided by the API.
            assistant={k:v for k,v in message.items() if k in ('role','content','reasoning','reasoning_details','refusal')}; assistant['role']='assistant'
            thread['messages']=messages+[assistant]
            thread['turns'].append({'id':turn,'status':'completed','response':response,'routing':info})
            write(self.base/'thread.json',thread)
            with self.condition:
                self.state.update(active_turn_id=None,last_turn_id=turn,status='idle',boundary='completed',effective=info,usage=response.get('usage'),error=None)
                self.save(); self.emit('item/agentMessage/delta',delta=message['content']); self.emit('turn/completed',turn={'id':turn,'status':'completed'}); self.condition.notify_all()
        except Exception as e:
            with self.condition:
                write(target/'ERROR.json',{'error':str(e),'coding_failure':False,'utc':now()})
                self.state.update(active_turn_id=None,last_turn_id=turn,status='interrupted',boundary='interrupted',error=str(e)); self.save()
                self.emit('turn/completed',turn={'id':turn,'status':'interrupted'}); self.condition.notify_all()
    def wait(self,timeout=3600):
        if self.worker:
            self.worker.join(timeout)
            if self.worker.is_alive(): raise Error('OpenRouter request still running')
        return self.state
    def interrupt(self):
        if self.transport: self.transport.cancel()
        self.wait(60)
    def pause(self):
        atomic(self.base/'workspace/out/PAUSE','Save after the current HTTP turn.\n')
        return {'pause':'Current request will settle, then be saved. No new turn starts.'}
    def final(self):
        if self.state.get('boundary')!='completed': raise Error(self.state.get('error') or 'No completed OpenRouter turn')
        return read(self.base/'thread.json')['turns'][-1]['response']['choices'][0]['message']['content']
    def checkpoint(self,interrupt=False):
        if interrupt:
            atomic(self.base/'workspace/out/PAUSE','Stopped by investigator. Explicit recovery required.\n')
            self.interrupt()
        self.open()
        with self.guard:
            if self.state.get('active_turn_id') or (self.worker and self.worker.is_alive()): raise Error('HTTP turn active; wait or stop before capture')
            if not self.state.get('last_turn_id'): raise Error('No OpenRouter turn to archive')
            from .portable import commit
            try:
                receipt=commit(self.base,self.state); self.state.update(checkpoint=receipt['checkpoint'],status='saved'); self.save(); return receipt
            finally: self.release()
