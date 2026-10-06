"""Independent native actors with explicit models and durable lifecycle state."""
from pathlib import Path
import json, os, shutil, threading, time, uuid
from .common import *
from .native import Native, configure, auth_to, fingerprint, process_identity, resolve_executable
from . import archive, questions, backends

DIALOGUE='''The investigator is an available collaborator in this same live conversation. Share concise progress and make uncertainty visible. Ask the investigator with request_user_input when an assumption, ambiguity, conflict or consequential choice needs their judgment. Wait for the answer before dependent work; silence is not permission. Use a blocking question when the answer is required. If that tool is unavailable, state the question plainly and end the turn without closing the leg. Never invent their answer. Routine choices within the agreed method remain yours. Do not request passwords or credentials. Your visible messages and tool activity are shown live; private reasoning is not a transcript. For a research aggregator, use tools/mem.py ask with --assume for nonblocking questions and continue independent work. Read mem.py asks at each boundary and before dependent work. Never write investigator answers in out/_answers. Native questions and answers are also kept there. These instructions do not relax scientific checks or workspace permissions.'''

def load(actor):
    backend=backends.name(actor_state(actor))
    if backend=='claude':
        from .claude_backend import Actor as ClaudeActor
        return ClaudeActor(actor)
    if backend=='openrouter':
        from .openrouter import Actor as APIActor
        return APIActor(actor)
    return Actor(actor)

class Actor:
    def __init__(self, actor):
        self.base=actor_dir(actor); self.guard=threading.RLock(); self.condition=threading.Condition(self.guard)
        self.state=actor_state(actor); self.server=None; self.lease=None
    @property
    def workspace(self): return self.base/'workspace'
    @property
    def capabilities(self): return backends.capabilities(self.state)
    def save(self): write(self.base/'state.json',self.state)
    def update(self,m):
        # Native event log stays outside the analyst workspace.
        event(self.base/'events.jsonl',native=m)
        p=m.get('params',{}); method=m.get('method')
        with self.condition:
            if method=='turn/started' and p.get('threadId')==self.state.get('thread_id'):
                self.state.update(active_turn_id=p['turn']['id'],status='working')
            elif method=='turn/completed' and p.get('threadId')==self.state.get('thread_id'):
                turn=p['turn']; self.state.update(active_turn_id=None,last_turn_id=turn['id'],boundary=turn['status'],status='idle' if turn['status']=='completed' else turn['status'],error=turn.get('error'))
                self.state['questions']=[]
                self.condition.notify_all()
            elif method=='item/tool/requestUserInput' and p.get('threadId')==self.state.get('thread_id'):
                if self.state.get('role')=='aggregator': questions.mirror_native(self,p)
                self.state.setdefault('questions',[]).append(p)
                self.save()
            elif method=='serverRequest/resolved' and p.get('threadId')==self.state.get('thread_id'):
                self.state['questions']=[q for q in self.state.get('questions',[]) if q['requestId']!=p.get('requestId')]
                self.save()
            elif method=='rplace/nativeDisconnected':
                self.state.update(questions=[],status='disconnected',error='Native connection ended. Conversation and files are preserved. Inspect before explicit continuation.')
                self.save();self.condition.notify_all()
            elif method=='thread/tokenUsage/updated': self.state['usage']=p.get('tokenUsage',{})
            if method in ('turn/started','turn/completed','thread/tokenUsage/updated'): self.save()
    def open(self):
        with self.guard:
            if actor_state(self.state['id']).get('handler_retired'):raise Error('Handler continued elsewhere; open its operational continuation')
            if actor_state(self.state['id']).get('evicted'):raise Error('Actor store is archived. Restore checkpoint '+str(self.state.get('checkpoint'))+' as a new actor.')
            if self.server: return self.state
            self.lease=lock(self.base/'owner.lock'); self.lease.__enter__()
            try:
                previous=read(self.base/'native-process.json')
                if previous and process_identity(previous['pid'])==previous['identity']: raise Error('Recorded native process is still alive; do not start a second owner')
                if self.state.get('questions'):
                    event(self.base/'events.jsonl',native={'method':'rplace/questionsInterrupted','params':{'questions':self.state['questions']}})
                    self.state['questions']=[]
                runtime=self.state['runtime']; exe=runtime['executable']
                if sha(exe)!=runtime['sha256']: raise Error('Pinned runtime changed; restore its recorded executable')
                configure(self.base/'native',self.state['model'],self.state['effort'],self.base/'workspace',self.state.get('read_only',False),(self.state.get('leg') or '')[:2],self.state.get('role')=='probe',interactive=self.state.get('role') not in ('reader','labeler','probe')); auth_to(self.base/'native')
                self.server=Native(self.base/'native',self.base/'workspace/out',exe,self.update)
                write(self.base/'native-process.json',{'pid':self.server.p.pid,'identity':process_identity(self.server.p.pid),'utc':now()})
                params={'cwd':str(self.base/'workspace/out'),'model':self.state['model'],'approvalPolicy':'never','permissions':'rplace'}
                interactive=self.state.get('role') in ('aggregator','handler','interview')
                instructions=self.state.get('continuation_instructions') or self.state.get('instructions','')
                if interactive:instructions+='\n'+DIALOGUE
                if self.state.get('thread_id'):
                    params['threadId']=self.state['thread_id']
                    if instructions:params['developerInstructions']=instructions
                    if self.state.get('resume_path'): params['path']=self.state['resume_path']
                    if self.state.get('fork_pending'):
                        params['lastTurnId']=self.state['last_turn_id']
                        result=self.server.call('thread/fork',params)
                        self.state['fork_pending']=False; self.state['resume_path']=None
                    else: result=self.server.call('thread/resume',params)
                else:
                    params['developerInstructions']=instructions
                    result=self.server.call('thread/start',params)
                if result.get('model')!=self.state['model']: raise Error('Requested model not confirmed by app-server')
                if result.get('reasoningEffort')!=self.state['effort']:raise Error('Requested effort not confirmed by app-server')
                self.state.update(thread_id=result['thread']['id'],effective=result,status='idle',active_turn_id=None)
                if self.state.get('thread_id') and self.state.get('last_turn_id'):
                    durable=self.server.call('thread/read',{'threadId':self.state['thread_id'],'includeTurns':True})['thread'].get('turns',[])
                    if durable and durable[-1]['status'] in ('completed','interrupted','failed'):
                        self.state.update(last_turn_id=durable[-1]['id'],boundary=durable[-1]['status'])
                atomic(self.base/'workspace/.session',self.state['thread_id']+'\n')
                self.save(); return self.state
            except BaseException:
                self.release(); raise
    def release(self):
        if self.server:
            self.server.close(); self.server=None
            (self.base/'native-process.json').unlink(missing_ok=True)
        (self.base/'native/auth.json').unlink(missing_ok=True)
        if self.lease: self.lease.__exit__(None,None,None); self.lease=None
    def message(self,text):
        if not isinstance(text,str) or not text.strip(): raise Error('Message is empty')
        ensure_space()
        self.open()
        with self.guard:
            if self.state.get('questions'):raise Error('Answer the pending question in the live panel, or Stop and save before changing direction.')
            event(self.base/'messages.jsonl',role='user',text=text)
            if self.state.get('active_turn_id'):
                return self.server.call('turn/steer',{'threadId':self.state['thread_id'],'expectedTurnId':self.state['active_turn_id'],'input':[{'type':'text','text':text}]})
            self.state.update(status='starting',error=None); self.save()
            params={'threadId':self.state['thread_id'],'input':[{'type':'text','text':text}],'cwd':str(self.base/'workspace/out'),'model':self.state['model'],'effort':self.state['effort'],'approvalPolicy':'never','permissions':'rplace'}
            if self.state.get('original_workspace'):
                params['input'][0]['text']='[Restore notice: the saved workspace '+self.state['original_workspace']+' is now '+str(self.base/'workspace')+'. Use the restored files; the parent is immutable.]\n'+text
            result=self.server.call('turn/start',params)
            self.state.update(active_turn_id=result['turn']['id'],status='working'); self.save(); return result
    def wait(self,timeout=3600):
        end=time.monotonic()+timeout
        with self.condition:
            while self.state.get('active_turn_id') or self.state['status']=='starting':
                left=end-time.monotonic()
                if left<=0: raise Error('Turn still running; it remains resumable')
                self.condition.wait(min(left,2))
                if self.server and getattr(self.server,'callback_error',None):raise Error('Native event callback failed: '+self.server.callback_error)
                if self.server and self.server.p.poll() is not None: raise Error('Native server exited; interrupted store preserved')
        if self.server and getattr(self.server,'callback_error',None):raise Error('Native event callback failed: '+self.server.callback_error)
        return self.state
    def answer(self,key,answers):
        with self.guard:
            if not self.server or not self.state.get('active_turn_id'):
                raise Error('This question is not attached to a live turn. Inspect the saved conversation.')
            question=next((q for q in self.state.get('questions',[]) if q.get('requestKey')==key),None)
            if not question:raise Error('Question is no longer pending. Refresh before replying.')
            result=self.server.answer(key,answers,self.state['thread_id'],self.state['active_turn_id'])
            questions.record_native_answer(self,question,answers)
            self.state['questions']=[q for q in self.state.get('questions',[]) if q.get('requestKey')!=key]
            event(self.base/'events.jsonl',native={'method':'rplace/questionAnswered','params':{'requestKey':key,'questions':question['questions'],'answers':answers}})
            self.save()
            return result
    def interrupt(self):
        with self.guard:
            if self.server and self.state.get('active_turn_id'):
                self.server.call('turn/interrupt',{'threadId':self.state['thread_id'],'turnId':self.state['active_turn_id']})
        self.wait(60)
    def pause(self):
        with self.guard:
            atomic(self.base/'workspace/out/PAUSE','Requested '+now()+'\n')
            if self.state.get('role') in ('reader','labeler'):return {'pause':'Worker will settle at its next boundary; no prompt changed.'}
            if not self.state.get('active_turn_id'):return {'pause':'Already idle. No turn started.','new_turn_started':False}
            if not self.server:raise Error('Active turn is not attached. Inspect its process before recovery.')
            # Hold the same lock used by completion callbacks: pause may steer,
            # but must never fall through to starting a turn after completion.
            return self.message('Pause at the next safe boundary. Save head and diary with the next action, then stop. Acknowledge the pause.')
    def checkpoint(self,interrupt=False):
        if interrupt: self.interrupt()
        with self.guard:
            if self.state.get('active_turn_id'): raise Error('Turn active; pause or stop it before capture')
            if not self.state.get('thread_id') or not self.state.get('last_turn_id'): raise Error('No native turn to archive')
            self.open()
            bg=self.server.call('thread/backgroundTerminals/list',{'threadId':self.state['thread_id']})
            if bg.get('data') or bg.get('nextCursor'): raise Error('Background tool processes remain; settle them before capture')
            thread=self.server.call('thread/read',{'threadId':self.state['thread_id'],'includeTurns':True})['thread']
            turns=thread.get('turns',[])
            if not turns or turns[-1]['id']!=self.state['last_turn_id'] or turns[-1]['status'] not in ('completed','interrupted','failed'): raise Error('Native boundary is not durable')
            write(self.base/'thread.json',thread)
            # Keep lease through shutdown, archive verification and state publication.
            self.server.close(); self.server=None
            (self.base/'native-process.json').unlink(missing_ok=True)
            (self.base/'native/auth.json').unlink(missing_ok=True)
            try:
                if self.state.get('boundary')=='completed':
                    found=False
                    for path in (self.base/'native/sessions').rglob('*.jsonl'):
                        with path.open() as log:
                            for line in log:
                                row=json.loads(line); payload=row.get('payload',{})
                                if row.get('type')=='event_msg' and payload.get('type')=='task_complete' and payload.get('turn_id')==self.state['last_turn_id']: found=True
                    if not found: raise Error('Completed turn not flushed in native rollout')
                receipt=archive.commit(self.base,self.state)
                self.state.update(checkpoint=receipt['checkpoint'],status='saved'); self.save()
                return receipt
            finally:
                if self.lease: self.lease.__exit__(None,None,None); self.lease=None
    def final(self):
        if not self.server: self.open()
        t=self.server.call('thread/read',{'threadId':self.state['thread_id'],'includeTurns':True})['thread']
        matches=[x for x in t.get('turns',[]) if x['id']==self.state.get('last_turn_id')]
        if not matches: raise Error('Recorded turn missing')
        items=[x for x in matches[-1].get('items',[]) if x.get('type')=='agentMessage']
        finals=[x for x in items if x.get('phase')=='final_answer'] or items[-1:]
        return '\n'.join(x.get('text','') for x in finals)

def create(actor, workspace, model, effort, role='aggregator',run=None,leg=None,instructions='',read_only=False,executable=None):
    base=actor_dir(actor)
    with lock(DATA/'locks'/('create-'+identity(actor)+'.lock')):
        if base.exists(): raise Error('Actor already exists')
        ensure_space(sum(p.stat().st_size for p in files(workspace))+64*1024**2); base.mkdir(parents=True)
        try:
            copy_tree(workspace,base/'workspace'); (base/'workspace/out').mkdir(exist_ok=True)
            (base/'workspace/RUN.json').touch(exist_ok=True)
            if not (base/'workspace/RUN.json').stat().st_size: write(base/'workspace/RUN.json',{})
            exe=resolve_executable(executable)
            state={'id':actor,'role':role,'model':model,'effort':effort,'run':run,'leg':leg,'status':'prepared','thread_id':None,'active_turn_id':None,'last_turn_id':None,'boundary':None,'created_utc':now(),'runtime':fingerprint(exe),'instructions':instructions,'read_only':read_only}
            (base/'native').mkdir(); write(base/'state.json',state)
        except BaseException:
            # New disposable actor only, never an existing store.
            shutil.rmtree(base); raise
    return state
