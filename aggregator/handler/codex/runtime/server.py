"""Authenticated loopback control plane. Browser and terminal share the same actor."""
import contextlib, concurrent.futures, hmac, http.server, json, secrets, threading, time, urllib.parse, uuid
from pathlib import Path
from .common import *
from . import actors, archive, study, fleet, labelers, bridge, plans, cancellation, retention, branches, publication, blocks, questions, backends

def owned_run(actor):
    if actor.state.get('role')=='interview':return None
    return actor.state.get('run') or actor.state.get('study_run')


class Controller:
    def __init__(self):
        self.actors={};self.guard=threading.RLock();self.controls={};self.jobs={}
        self.pool=concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self.control_pool=concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self.stopping=threading.Event();self.closing=set();self.block_busy=set()
        blocks.pause_restart()
        for p in (DATA/'jobs').glob('*.json'):
            old=read(p)
            if old.get('status')=='working':write(p,{**old,'status':'interrupted','error':'Controller restarted. Inspect actors and recover the pending plan.'})
        from .native import process_identity
        for path in (DATA/'actors').glob('*/state.json'):
            state=read(path,{})
            if state.get('backend')=='claude':continue # durable file questions survive controller restarts
            if not state.get('questions'):continue
            proc=read(path.parent/'native-process.json',{})
            if not (proc.get('identity') and process_identity(proc['pid'])==proc['identity']):
                event(path.parent/'events.jsonl',native={'method':'rplace/questionsInterrupted','params':{'questions':state['questions']}})
                state.update(questions=[],active_turn_id=None,status='interrupted',boundary='interrupted',error='Controller restarted while awaiting an answer. The question is preserved in Conversation. Send a message to continue explicitly.')
                write(path,state)
        for p in (DATA/'runs').glob('*/state.json'):
            state=read(p);did=state.get('dispatch_active')
            if did:
                paths=list((DATA/'actors').glob(did+'*/native-process.json'))+list((DATA/'actors').glob(did+'*/http-process.json'))
                alive=any((v:=read(q)) and v.get('identity') and process_identity(v['pid'])==v['identity'] for q in paths)
                if not alive:state.update(dispatch_active=None,dispatch_blocked=did);write(p,state)
        self.watcher=threading.Thread(target=bridge.watch,args=(self,),daemon=True);self.watcher.start()
    def actor(self,aid):
        with self.guard:
            if self.stopping.is_set():raise Error('Controller is stopping; no new actor work is admitted')
            if aid not in self.actors:self.actors[aid]=actors.load(aid)
            return self.actors[aid]
    @contextlib.contextmanager
    def control(self,aid,closing=False):
        with self.guard:
            guard=self.controls.setdefault(aid,threading.RLock())
            if aid in self.closing:raise Error('Actor closure is in progress')
        if not guard.acquire(blocking=False):raise Error('Actor control operation is in progress')
        try:
            if self.stopping.is_set():raise Error('Controller is stopping')
            if closing:
                with self.guard:self.closing.add(aid)
            yield
        finally:
            if closing:
                with self.guard:self.closing.discard(aid)
            guard.release()
    def mutable(self,actor,op):
        backends.require(actor.state,op)
        current=actor_state(actor.state['id'])
        if current.get('handler_retired'):raise Error('Handler continued elsewhere; use '+str(current.get('continuation_actor')))
        if current.get('evicted'):raise Error('Actor is archived; restore checkpoint '+str(current.get('checkpoint')))
        if actor.state.get('role')=='reader' and op in ('message','card'):raise Error('Packet readers are controlled by the fleet; restore an interview to ask questions')
        run=owned_run(actor) if actor.state.get('role')=='interview' else actor.state.get('run')
        if run and study.run_state(run).get('active_actor')!=actor.state['id']:raise Error('This leg is saved. Open an interview fork to talk to it.')
        if op in ('message','card') and run:cancellation.run_stopped(run)
    def job(self,fn,*args,urgent=False,job_meta=None,**kwargs):
        if self.stopping.is_set():raise Error('Controller is stopping')
        with self.guard:
            if job_meta:
                for jid,j in self.jobs.items():
                    if j.get('status')=='working' and j.get('request')==job_meta:return {'job':jid}
            jid=uuid.uuid4().hex;record={'status':'working','started_utc':now(),'request':job_meta or {'action':getattr(fn,'__name__',type(fn).__name__)}}
            self.jobs[jid]=record
            write(DATA/'jobs'/(jid+'.json'),record)
        def work():
            try:
                if self.stopping.is_set():raise Error('Controller stopped before job admission')
                self.jobs[jid]={**record,'status':'completed','finished_utc':now(),'result':fn(*args,**kwargs)}
            except Exception as e:self.jobs[jid]={**record,'status':'failed','finished_utc':now(),'error':str(e)}
            write(DATA/'jobs'/(jid+'.json'),self.jobs[jid])
        (self.control_pool if urgent else self.pool).submit(work);return {'job':jid}
    def list(self):
        errors=[]
        p=DATA/'controller-errors.jsonl'
        if p.exists():
            from collections import deque
            with p.open() as f:
                for line in deque(f,maxlen=20):
                    try:errors.append(json.loads(line))
                    except ValueError:pass
        errors.extend({'actor':p.parent.name,**read(p,{})} for p in (DATA/'actors').glob('*/callback-error.json'))
        persisted={p.stem:read(p) for p in (DATA/'jobs').glob('*.json')}
        actor_rows=[]
        for path in sorted((DATA/'actors').glob('*/state.json')):
            a=read(path);owner=self.actors.get(a['id'])
            try:a['backend_capabilities']=backends.capabilities(a)
            except Error as e:errors.append({'actor':a['id'],'error':str(e)})
            a['questions_live']=bool(owner and getattr(owner,'server',None) and owner.server.p.poll() is None)
            # Status need not transfer the full native transcript on every poll.
            if isinstance(a.get('effective'),dict):
                a['effective']={k:v for k,v in a['effective'].items() if k!='thread'}
            run=a.get('run');s=read(study.run_dir(run)/'state.json',{}) if run else {}
            if a.get('backend')=='claude':
                answerable=backends.allowed(a,'answer') and (a.get('role')=='interview' or s.get('active_actor')==a['id'])
                a['questions']=[{**q,'source':'file','run':run,'answerable':answerable,'isBlocking':False}
                                for q in a.get('questions',[])]
            latest=s.get('active_actor') or next(iter(reversed(s.get('legs',{}).values())),{}).get('actor')
            if run and a['id']==latest:
                try:
                    records=questions.listing(Path(s['latest_workspace']),run)
                    native_ids={qid for q in a.get('questions',[]) for qid in q.get('persistedAsks',{}).values()}
                    if a.get('backend')=='claude':native_ids|={q.get('requestKey') for q in a.get('questions',[])}
                    a['study_asks']=records
                    a['questions']=[*a.get('questions',[]),*[
                        {'source':'file','requestKey':r['id'],'isBlocking':False,'run':run,
                         'questions':[{'id':r['id'],'question':r['question']}],'assumption':r.get('assumption',''),
                         'origin_leg':r.get('leg'),'answerable':True}
                        for r in records if not r['answered'] and r['id'] not in native_ids]]
                except (Error,OSError,ValueError) as e:errors.append({'actor':a['id'],'error':str(e)})
            actor_rows.append(a)
        return {'actors':actor_rows,'checkpoints':[read(p) for p in sorted((DATA/'checkpoints').glob('*/receipt.json'))], 'runs':[{**(s:=read(p)),**({'branch':branches.summary(s['branch'])} if s.get('branch') else {}),'block':blocks.state(s['id']),'stop':read(p.parent/'STOP.json',None)} for p in sorted((DATA/'runs').glob('*/state.json'))], 'jobs':{**persisted,**self.jobs},'errors':errors,'features':['analysis-branches-v1','leg-blocks-v1','control-guards-v1','live-questions-v1','persistent-asks-v1','external-handler-v1']}
    def close_leg(self,run,aid):
        with self.control(aid,closing=True):result=self._close_leg(run,aid)
        retention.sweep();return result
    def _close_leg(self,run,aid):
        result=study.close(run,self.actor(aid))
        if result.get('backend')=='claude':return result
        published=publication.after_close(run)
        if published:result['publication']=published['publication']
        if plans.pending(study.run_state(run)):result['dispatch_plan']=plans.resume(run,self.actor)
        return result
    def cancel_run(self,run,reason='Operator stop'):
        run=identity(run);state=study.run_state(run)
        blocks.stop(run,reason)
        write(study.run_dir(run)/'STOP.json',{'reason':reason,'utc':now()})
        did=state.get('dispatch_active') or state.get('dispatch_blocked')
        if did:cancellation.gate(DATA/'dispatches'/did).cancel(reason)
        return {'run':run,'dispatch':did,'stop_requested':True}
    def stop_run(self,run,reason='Operator stop'):
        result=self.cancel_run(run,reason)
        with self.guard:owned=[a for a in self.actors.values() if owned_run(a)==run]
        def settle(a):
            try:
                # Checkpoint verifies durability; failure retains the native/API store.
                return {'actor':a.state['id'],'receipt':a.checkpoint(interrupt=True)}
            except Exception as e:return {'actor':a.state['id'],'error':str(e),'store_preserved':True}
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:result['actors']=list(pool.map(settle,owned))
        return result
    def lifecycle(self,aid,op):
        with self.control(aid):
            actor=self.actor(aid);self.mutable(actor,op)
            if actor.state.get('role')!='interview' and actor.state.get('run') and op in ('pause','stop'):
                blocks.stop(actor.state['run'],'Investigator requested '+op)
            if op=='pause':
                if actor.state.get('role')!='interview' and actor.state.get('dispatch_id'):
                    run=actor.state.get('study_run')
                    if run:self.cancel_run(run,'Pause at dispatch boundary')
                return actor.pause()
            if op=='stop':
                run=owned_run(actor)
                if run:return self.stop_run(run)
                return actor.checkpoint(interrupt=True)
            return actor.checkpoint()
    def continue_handler(self,checkpoint,aid=None):
        checkpoint=identity(checkpoint);aid=identity(aid or 'handler-'+uuid.uuid4().hex[:10])
        backends.require({'backend':archive.checkpoint_backend(checkpoint)},'handler')
        with lock(DATA/'locks/handler-continuation.lock'),contextlib.ExitStack() as controls:
            src=DATA/'checkpoints'/checkpoint
            manifest=archive.verify(src/'agent.tar.gz')
            if not manifest.get('handler_conversation_included'):raise Error('Checkpoint is not a native handler history')
            receipt=read(src/'receipt.json',{});parent=receipt.get('actor')
            if parent:
                controls.enter_context(self.control(parent))
                with self.guard:owner=self.actors.get(parent)
                if owner:controls.enter_context(owner.guard)
            from .native import process_identity
            for p in (DATA/'actors').glob('*/state.json'):
                st=read(p,{})
                if st.get('role')=='handler' and (st.get('id')==parent or st.get('parent_checkpoint')==checkpoint):
                    proc=read(p.parent/'native-process.json',{})
                    if st.get('active_turn_id') or (proc.get('identity') and process_identity(proc['pid'])==proc['identity']):raise Error('Handler owner is still open. Save and detach it before continuation.')
                    if st.get('parent_checkpoint')==checkpoint:raise Error('This handler checkpoint already has an operational continuation')
            st=archive.restore(checkpoint,aid)
            if st.get('origin_role')!='handler':raise Error('Only handler histories can continue operationally')
            base=actor_dir(aid);out=base/'workspace/out'
            # Old archives did not carry the mailbox journal. Never replay inherited
            # requests, including a request claimed just before a crash.
            for req in (out/'requests').glob('*.json'):
                key=identity(req.stem);record=base/'mailbox'/(key+'.json');response=out/'responses'/req.name
                if not record.exists():write(record,{'status':'inherited','error':'Historical request is not replayed; inspect its original result.'})
                if not response.exists():write(response,read(record))
            st.update(role='handler',run=None,read_only=False,continuation_instructions=bridge.HANDLER)
            write(base/'state.json',st)
            if parent and (actor_dir(parent)/'state.json').exists():
                retired=actor_state(parent);retired.update(handler_retired=True,continuation_actor=aid)
                write(actor_dir(parent)/'state.json',retired)
                if owner:owner.state=retired
            return st
    def action(self,a):
        op=a['action']
        meta={k:a[k] for k in ('action','run','source_run','actor','checkpoint','dispatch','leg') if k in a}
        if op=='status':return self.list()
        if op=='job':return self.jobs.get(a['job']) or read(DATA/'jobs'/(identity(a['job'])+'.json'),{})
        if op=='events':
            p=actor_dir(a['actor'])/'events.jsonl';offset=max(0,int(a.get('offset',0)))
            if not p.exists():return {'offset':0,'events':[]}
            with p.open() as f:
                f.seek(offset);lines=[]
                for _ in range(250):
                    line=f.readline()
                    if not line:break
                    lines.append(json.loads(line))
                return {'offset':f.tell(),'events':lines}
        if self.stopping.is_set():raise Error('Controller is stopping')
        # Refuse unsupported platform work before job records, block stops or writes.
        run_operations={'run-block':'blocks','resume-block':'blocks','prepare':'prepare','branch':'branch',
                        'prepare-branch':'publication','publish-branch':'publication',
                        'branch-cancel-upload':'branch','branch-upload':'branch',
                        'recover-plan':'fleet','labelers':'fleet','dispatch':'fleet'}
        if op in run_operations:backends.require_run(a.get('source_run') or a['run'],run_operations[op])
        if op=='recover':
            recovered=read(DATA/'dispatches'/identity(a['dispatch'])/'input.json',{})
            if recovered.get('run'):backends.require_run(recovered['run'],'fleet')
        if op in ('close','save','open','stop','pause','message','card','answer','answer-ask','start'):
            backends.require(actor_state(a['actor']),op)
        if op in ('restore','resume-handler'):
            backends.require({'backend':archive.checkpoint_backend(a['checkpoint'])},'restore' if op=='restore' else 'handler')
        if op=='build':return self.job(study.build,identity(a['run']),a.get('source'),a.get('fleet_arm','codex'),job_meta=meta)
        if op=='run-block':return blocks.start(a['run'],a['first'],a['last'])
        if op=='block-status':return blocks.state(identity(a['run']))
        if op=='stop-block':return blocks.stop(a['run'])
        if op=='resume-block':return blocks.resume(a['run'])
        if op=='branch':return self.job(branches.create,a['source_run'],a['checkpoint'],a['run'],a['leg'],job_meta=meta)
        if op=='prepare-branch':return self.job(publication.prepare,identity(a['run']),job_meta=meta)
        if op=='publish-branch':return self.job(publication.publish,identity(a['run']),job_meta=meta)
        if op=='branch-status':return branches.inspect(a['run'])
        if op=='branch-cancel-upload':return branches.cancel_upload(a['run'],a['path'],a.get('stage'))
        if op=='branch-upload':return branches.upload(a['run'],a['path'],a['content'],a['offset'],a['total'],a['digest'],a.get('stage'))
        if op=='prepare':
            if study.run_state(a['run']).get('branch',{}).get('status')=='draft':raise Error('Use prepare-branch to publish the setup and prepare its first leg')
            result=study.prepare(identity(a['run']),a['leg']);retention.sweep();return result
        if op=='open':
            with self.control(a['actor']):return self.actor(a['actor']).open()
        if op=='answer':
            with self.control(a['actor']):
                actor=self.actor(a['actor']);self.mutable(actor,'message')
                result=actor.answer(a['request'],a['answers'])
                if owned_run(actor):blocks.stop(owned_run(actor),'Investigator answered a question; review before further automatic legs')
                return result
        if op=='answer-ask':
            with self.control(a['actor']):
                actor=self.actor(a['actor'])
                if backends.name(actor.state)=='claude':
                    self.mutable(actor,'answer')
                    if owned_run(actor)!=a['run']:raise Error('Question belongs to another study')
                    result=actor.answer(a['request'],{'answer':a['text']})
                    if a['run']:blocks.stop(a['run'],'Investigator answered a question; review before further automatic legs')
                    return result
                return questions.answer_study(a['run'],a['request'],a['text'],a['actor'])
        if op=='start':
            with self.control(a['actor']):
                actor=self.actor(a['actor']);self.mutable(actor,'message');st=actor.state
                if st.get('role')!='aggregator' or not st.get('run'):raise Error('Start requires a prepared research leg')
                if st.get('active_turn_id') or st.get('leg_started') or (st.get('last_turn_id') and st.get('leg_started') is not False):
                    raise Error('This leg already started or its start is uncertain. Inspect Activity; use a message for deliberate continuation.')
                if study.run_state(st['run']).get('legs',{}).get(st['leg'],{}).get('status')!='prepared':raise Error('Leg is not prepared')
                return self.action({'action':'message','actor':a['actor'],'text':(actor.base/'first-message.txt').read_text()})
        if op in ('card','message'):
            with self.control(a['actor']):
                actor=self.actor(a['actor']);self.mutable(actor,op);text=a['text']
                if not isinstance(text,str) or not text.strip():raise Error('Empty message')
                if actor.state.get('role')!='interview' and actor.state.get('run'):blocks.stop(actor.state['run'],'Manual message or start; review the block before resuming')
                if op=='card':
                    run=actor.state.get('run')
                    if not run:raise Error('Cards require the current study actor')
                    if backends.name(actor.state)=='claude':
                        # Its durable inbox and hook own delivery. Do not create a
                        # second pseudo-workspace or claim the hook has delivered it.
                        card=None
                    else:
                        card=backends.workspace(actor)/'out/inbox'/('card-'+uuid.uuid4().hex+'.md');atomic(card,text+'\n')
                    event(study.run_dir(run)/'interventions.jsonl',actor=a['actor'],card=str(card),text=text)
                    text='Investigator card: '+text
                backends.pause_marker(actor).unlink(missing_ok=True)
                if actor.state.get('role')=='aggregator':
                    # Claim before transport. An uncertain response must not
                    # make the opening prompt eligible for automatic replay.
                    actor.state['leg_started']=True;actor.save()
                delivery=actor.message(text)
                return {'card':str(card) if card else None,'delivery':delivery} if op=='card' else delivery
        if op=='pause':return self.lifecycle(a['actor'],op)
        if op=='stop':
            # Latch before queueing the potentially slow checkpoint operation.
            with self.control(a['actor']):
                actor=self.actor(a['actor']);self.mutable(actor,op)
                run=owned_run(actor)
                if run:self.cancel_run(run)
            return self.job(self.lifecycle,a['actor'],op,urgent=True,job_meta={**meta,'run':run})
        if op=='save':return self.job(self.lifecycle,a['actor'],op,job_meta={**meta,'run':owned_run(self.actor(a['actor']))})
        if op=='stop-run':
            self.cancel_run(a['run']);return self.job(self.stop_run,a['run'],urgent=True,job_meta={'action':op,'run':a['run']})
        if op=='continue-run':
            if any(j.get('status')=='working' and j.get('request',{}).get('run')==a['run'] and j.get('request',{}).get('action') in ('stop','stop-run') for j in self.jobs.values()):
                raise Error('Stop and save is still working. Wait for its result before clearing the study stop.')
            with lock(DATA/'locks'/('run-'+identity(a['run'])+'.lock')):
                state=study.run_state(a['run'])
                if state.get('dispatch_active') or state.get('dispatch_blocked') or plans.pending(state):raise Error('Use recover or recover-plan for an unresolved dispatch')
                (study.run_dir(a['run'])/'STOP.json').unlink(missing_ok=True)
            return {'run':a['run'],'continued':True,'new_turn_started':False}
        if op=='close':return self.job(self.close_leg,a['run'],a['actor'],job_meta={'action':op,'run':a['run'],'actor':a['actor']})
        if op=='restore':return self.job(archive.restore,identity(a['checkpoint']),identity(a.get('actor') or 'interview-'+uuid.uuid4().hex[:10]),job_meta={'action':op,'checkpoint':a['checkpoint'],**({'actor':a['actor']} if a.get('actor') else {})})
        if op=='resume-handler':return self.job(self.continue_handler,a['checkpoint'],a.get('actor'),job_meta={'action':op,'checkpoint':a['checkpoint']})
        if op=='recover':return self.job(plans.recover,identity(a['dispatch']),self.actor,job_meta={**meta,'run':read(DATA/'dispatches'/identity(a['dispatch'])/'input.json',{}).get('run')})
        if op=='recover-plan':return self.job(plans.resume,identity(a['run']),self.actor,explicit=True,job_meta=meta)
        if op=='labelers':return self.job(labelers.dispatch,a['run'],self.actor,recheck=a.get('recheck',False),job_meta=meta)
        if op=='dispatch':return self.job(fleet.dispatch,a['run'],a['stage'],self.actor,round=a.get('round'),only=a.get('only'),dry_run=a.get('dry_run',False),job_meta={**meta,'stage':a['stage'],'round':a.get('round'),'only':a.get('only'),'dry_run':a.get('dry_run',False)})
        if op=='prune':return self.job(retention.sweep)
        if op=='verify':return self.job(archive.verify_checkpoint,identity(a['checkpoint']))
        if op=='handler':
            raise Error('Use a separate Codex chat as the handler. Read codex/HANDLER-CHAT.md. No website handler was created.')
        raise Error('Unknown action')
    def shutdown(self):
        self.stopping.set();self.watcher.join(timeout=3)
        for p in (DATA/'runs').glob('*/state.json'):
            s=read(p,{})
            if s.get('active_actor') or s.get('dispatch_active') or plans.pending(s):self.cancel_run(s['id'],'Controller shutdown')
        with self.guard:owned=list(self.actors.values())
        def stop(a):
            try:a.interrupt()
            except Exception as e:
                try:event(DATA/'controller-errors.jsonl',actor=a.state['id'],error=str(e))
                except Exception:pass
            finally:a.release()
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(stop,owned))
        self.pool.shutdown(wait=False,cancel_futures=True)
        self.control_pool.shutdown(wait=False,cancel_futures=True)


def serve(port=8767):
    DATA.mkdir(parents=True,exist_ok=True)
    with lock(DATA/'controller.lock'):
        controller=Controller(); token=secrets.token_urlsafe(32)
        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self,*a): pass
            def reply(self,code,body,kind='application/json'):
                b=json.dumps(body,ensure_ascii=False).encode() if kind=='application/json' else body
                self.send_response(code); self.send_header('Content-Type',kind+'; charset=utf-8'); self.send_header('Content-Length',str(len(b))); self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff'); self.send_header('Referrer-Policy','no-referrer'); self.end_headers(); self.wfile.write(b)
            def valid_host(self): return self.headers.get('Host') in ('127.0.0.1:'+str(httpd.server_port),'localhost:'+str(httpd.server_port))
            def do_GET(self):
                if not self.valid_host(): return self.reply(403,{'error':'Host rejected'})
                if self.path.split('?')[0]=='/': return self.reply(200,(CODEX/'runtime/panel.html').read_bytes(),'text/html')
                self.reply(404,{'error':'Not found'})
            def do_POST(self):
                if self.path!='/api' or not self.valid_host(): return self.reply(403,{'error':'Endpoint rejected'})
                origin=self.headers.get('Origin')
                if origin and origin!='http://'+self.headers['Host']: return self.reply(403,{'error':'Origin rejected'})
                if not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+token): return self.reply(403,{'error':'Authentication required'})
                try:
                    size=int(self.headers.get('Content-Length','0'))
                    if size<1 or size>2*1024**2: raise Error('Invalid request length')
                    data=json.loads(self.rfile.read(size)); result=controller.action(data); self.reply(200,{'result':result})
                except Exception as e: self.reply(400,{'error':str(e)})
        httpd=http.server.ThreadingHTTPServer(('127.0.0.1',port),Handler)
        endpoint={'url':'http://127.0.0.1:'+str(httpd.server_port),'token':token,'pid':os.getpid(),'started_utc':now()}
        write(DATA/'controller.json',endpoint); (DATA/'controller.json').chmod(0o600)
        url=endpoint['url']+'/#token='+token
        launcher=DATA/'OPENAI-LIVE.html'
        atomic(launcher,'<!doctype html><meta charset="utf-8"><title>v43 control panel</title><a href="'+url+'">Open the live panel on this Mac</a><p>Private launcher. On a phone use the private HTTPS link with Tailscale connected.</p>')
        launcher.chmod(0o600)
        print('Control panel: '+url,flush=True)
        import signal
        def stop(signum,frame): raise KeyboardInterrupt
        signal.signal(signal.SIGTERM,stop)
        try: httpd.serve_forever(poll_interval=.25)
        except KeyboardInterrupt: pass
        finally: httpd.server_close(); controller.shutdown(); (DATA/'controller.json').unlink(missing_ok=True)
