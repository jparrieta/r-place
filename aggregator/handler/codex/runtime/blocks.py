"""Finite, investigator-authorized sequences of repeated legs. No inferred scope."""
import copy
import uuid
from .common import *
from . import study, plans, cancellation, backends


def path(run): return study.run_dir(run)/'block.json'
def state(run): return read(path(run), {})
def stop_path(run): return study.run_dir(run)/'block-stop.json'


def stopped(run, block):
    return read(stop_path(run), {}).get('block') == block.get('id')


def owns(run, block_id=None):
    b=state(run)
    return bool(b.get('status')=='running' and not stopped(run,b) and b.get('id')!=block_id)


def guard(run, block_id=None):
    if owns(run,block_id): raise Error('An approved leg block owns this study; stop the block before manual preparation')


def manages_close(run, aid):
    b=state(run)
    return b.get('actor')==aid and b.get('status') in ('running','paused','blocked')


def sequence(first, last):
    a,b=study.descriptor(first),study.descriptor(last)
    if (a['stage'],a['step'])!=(b['stage'],b['step']):
        raise Error('A block stays within one repeated step; it cannot cross stages or steps')
    row=next(r for r in study.load_module(study.INSTRUMENT/'tools/steps.py','block_steps').table()
             if (r['stage'],r['step'])==(a['stage'],a['step']))
    if row['repeat']!='yes' or a['cont'] or b['cont']:
        raise Error('Choose numbered repeated legs without a pause continuation')
    start,end=int(a['count']),int(b['count'])
    if not 1<=start<=end<=99: raise Error('Choose an ordered finite range within the instrument two-digit leg IDs')
    return [a['stage']+a['step']+'-'+str(n).zfill(2) for n in range(start,end+1)]


def ready(run, s):
    cancellation.run_stopped(run)
    if s.get('dispatch_active') or s.get('dispatch_blocked') or plans.pending(s):
        raise Error('Resolve the pending fleet or phase plan before continuing the block')
    if s.get('publication',{}).get('status')=='blocked':
        raise Error('Retry Git publication before continuing the block')


def scientific_gate(run, leg, workspace):
    """B1's mandatory PI check-in is stronger than range authorization."""
    desc=study.descriptor(leg)
    if (desc['stage'],desc['step'])!=('B1','b'):return
    result=study.trusted(run,'saturation.py',['status','--stage','B1','--root',workspace,'--json'],workspace)
    if result.returncode:raise Error('Cannot verify the B1 stopping rule; inspect saturation.py status')
    report=json.loads(result.stdout)
    if report['state'] in ('check-in','report','stopped'):
        raise Error('B1 stopping rule: '+report['state']+'. A block does not authorize a PI decision')
    if report.get('left',{}).get('rooms')==0:
        raise Error('B1 first-pass reading is exhausted; do not create more reading legs')


def start(run, first, last):
    backends.require_run(run,'blocks')
    run=identity(run);legs=sequence(first,last)
    with lock(DATA/'locks'/('block-'+run+'.lock')),lock(DATA/'locks'/('run-'+run+'.lock')):
        s=study.run_state(run);ready(run,s)
        if state(run).get('status') in ('running','paused','blocked'):
            raise Error('A saved block exists; resume it or finish stopping it before replacing it')
        if s.get('branch',{}).get('status')=='draft': raise Error('Publish and prepare the analysis branch first')
        # Adoption is allowed only for a genuinely unstarted first leg, never a
        # failed or uncertain prior turn merely labelled prepared in the study.
        simulated=copy.deepcopy(s);aid=s.get('active_actor')
        if aid:
            actor=actor_state(aid)
            if actor.get('leg')!=legs[0] or actor.get('active_turn_id') or actor.get('leg_started') or (
                    actor.get('last_turn_id') and actor.get('leg_started') is not False):
                raise Error('The current leg has already started or differs from the block; resolve it first')
            simulated['legs'].pop(legs[0],None)
        for leg in legs:
            study.check_order(simulated,leg)
            simulated['legs'][leg]={'leg':leg,'stage':study.descriptor(leg)['stage'],'status':'verified'}
        b={'id':uuid.uuid4().hex,'run':run,'legs':legs,'cursor':0,'status':'running',
           'phase':'prepared' if aid else 'queued','actor':aid,'created_utc':now(),
           'reason':'Approved finite leg block','completed':[]}
        write(path(run),b);event(study.run_dir(run)/'block-events.jsonl',kind='approved',block=b)
        return b


def stop(run, reason='Stop after the current leg'):
    run=identity(run);b=state(run)
    if not b or b.get('status') in ('completed','stopped'):return b
    # Independent durable latch: even a slow archive or start cannot erase it.
    write(stop_path(run),{'block':b['id'],'reason':reason,'utc':now()})
    return {**b,'stop_requested':True,'reason':reason}


def pause_restart():
    for p in (DATA/'runs').glob('*/block.json'):
        b=read(p,{})
        if b.get('status')=='running':
            b.update(status='paused',reason='Controller restarted. Inspect the current leg, then explicitly resume the block.')
            write(p,b)


def resume(run):
    run=identity(run)
    backends.require_run(run,'blocks')
    with lock(DATA/'locks'/('block-'+run+'.lock')):
        b=state(run)
        if b.get('status') not in ('paused','blocked','stopped'):raise Error('No suspended block to resume')
        s=study.run_state(run);ready(run,s)
        if b['phase'] in ('preparing','starting'):
            row=s['legs'].get(b['legs'][b['cursor']],{})
            if row.get('status')!='verified' or not row.get('checkpoint'):
                raise Error('Uncertain preparation or start. Inspect and resolve it manually; no automatic replay')
            b.update(phase='closing',actor=row.get('actor'))
        if b.get('actor') and (actor_dir(b['actor'])/'workspace/out/NEEDS-JUDGMENT.md').exists():
            raise Error('Resolve NEEDS-JUDGMENT.md with the analyst before resuming')
        if b.get('actor') and actor_state(b['actor']).get('active_turn_id') and b.get('status')=='paused':
            raise Error('Inspect and settle the recorded active turn after restart before resuming the block')
        # Keep the old stop receipt; a new generation makes renewed consent explicit.
        b.update(id=uuid.uuid4().hex,status='running',reason='Explicitly resumed',resumed_utc=now())
        write(path(run),b);return b


def halt(run,b,reason,status='blocked'):
    b.update(status=status,reason=str(reason),updated_utc=now());write(path(run),b)
    event(study.run_dir(run)/'block-events.jsonl',kind=status,block=b['id'],reason=str(reason))


def advance(controller,run):
    """One admission/settlement at a time. Claims precede side effects."""
    backends.require_run(run,'blocks')
    with lock(DATA/'locks'/('block-'+identity(run)+'.lock')):
        b=state(run)
        if stopped(run,b) and b.get('status') in ('running','paused','blocked'):
            return halt(run,b,read(stop_path(run))['reason'],'stopped')
        if b.get('status')!='running':return
        try:
            if stopped(run,b):return halt(run,b,read(stop_path(run))['reason'],'stopped')
            if controller.stopping.is_set():return halt(run,b,'Controller is stopping','paused')
            s=study.run_state(run);ready(run,s)
            if b['cursor']>=len(b['legs']):return halt(run,b,'Approved range completed','completed')
            leg=b['legs'][b['cursor']];row=s['legs'].get(leg)
            if row and row.get('status')=='verified':
                if not row.get('checkpoint') or not row.get('probe'):raise Error('Verified leg lacks its native checkpoint or recall probe')
                cp=DATA/'checkpoints'/identity(row['checkpoint'])
                if not (cp/'COMMITTED').is_file():raise Error('Checkpoint has no committed archive')
                b['completed'].append({'leg':leg,'checkpoint':row['checkpoint']});b['cursor']+=1
                b.update(phase='queued',actor=None);write(path(run),b)
                if b['cursor']==len(b['legs']):return halt(run,b,'Approved range completed','completed')
                if row.get('cut')=='interview' or study.descriptor(leg)['stage'] in s.get('finished_stages',[]):
                    return halt(run,b,'Stage or interview boundary reached before the range limit','completed')
                return
            if row and row.get('status')=='paused':raise Error('Analyst paused. Resolve the continuation explicitly')
            aid=s.get('active_actor')
            if b['phase']=='queued':
                if aid:raise Error('Another leg owns this run')
                scientific_gate(run,leg,Path(s['latest_workspace']))
                ensure_space();b['phase']='preparing';write(path(run),b)
                result=study.prepare(run,leg,block_id=b['id'])
                aid=result['actor'];b.update(phase='prepared',actor=aid);write(path(run),b)
            if aid!=b.get('actor'):raise Error('Current actor differs from the approved block')
            actor=controller.actor(aid);st=actor.state
            if b['phase']=='prepared':
                if stopped(run,b):return halt(run,b,'Stopped before the next turn','stopped')
                if st.get('active_turn_id') or st.get('leg_started'):raise Error('Leg was started outside the block')
                scientific_gate(run,leg,actor.base/'workspace')
                ensure_space();b['phase']='starting';write(path(run),b)
                with controller.control(aid):
                    controller.mutable(actor,'message')
                    if stopped(run,b):
                        b['phase']='prepared'
                        return halt(run,b,'Stopped before the next turn','stopped')
                    prompt=(actor.base/'first-message.txt').read_text()
                    prompt+='\nController-approved block: '+b['legs'][0]+' through '+b['legs'][-1]+'. Perform only your current leg. The controller handles the next one. If investigator judgment is required or the declared blocks are exhausted, write out/NEEDS-JUDGMENT.md with the question, save head and diary, and stop without advancing. Do not invent additional work to fill this range.'
                    actor.message(prompt);actor.state['leg_started']=True;actor.save()
                b['phase']='running';write(path(run),b);return
            if b['phase'] in ('preparing','starting'):raise Error('Uncertain operation; inspect before any retry')
            if st.get('active_turn_id') or st.get('status')=='starting':
                if actor.server and (getattr(actor.server,'callback_error',None) or actor.server.p.poll() is not None):
                    raise Error('Native process or event callback failed; store preserved')
                return
            if st.get('boundary')!='completed' or st.get('error'):raise Error('Turn failed or was interrupted; inspect the saved actor')
            out=actor.base/'workspace/out'
            if (out/'NEEDS-JUDGMENT.md').exists():raise Error('Investigator judgment requested in out/NEEDS-JUDGMENT.md')
            marker=out/'_closes'/f'{study.descriptor(leg)["stage"]}-{leg}.closed'
            if not marker.is_file():raise Error('Turn ended without a leg close. Inspect its question or error; no automatic retry')
            b['phase']='closing';write(path(run),b)
            # Share the watcher receipt so an error is never retried by two paths.
            st['auto_close_turn']=st['last_turn_id'];actor.save()
            controller.close_leg(run,aid)
        except Exception as error:
            halt(run,b,error)


def tick(controller):
    if not hasattr(controller,'block_busy'):return
    for p in (DATA/'runs').glob('*/block.json'):
        b=read(p,{})
        if b.get('status')!='running' and not (b.get('status') in ('paused','blocked') and stopped(b['run'],b)):continue
        run=b['run']
        try:backends.require_run(run,'blocks')
        except Error:continue
        with controller.guard:
            if run in controller.block_busy or controller.stopping.is_set():continue
            controller.block_busy.add(run)
        def work(run=run):
            try:advance(controller,run)
            except Exception as error:event(DATA/'controller-errors.jsonl',run=run,error=str(error))
            finally:
                with controller.guard:controller.block_busy.discard(run)
        try:controller.pool.submit(work)
        except Exception:
            with controller.guard:controller.block_busy.discard(run)
            raise
