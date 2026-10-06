"""Independent D2/D3 room labelers with controller-owned collection and validation."""
import concurrent.futures, shutil, uuid
from pathlib import Path
from .common import *
from . import study, actors, archive, leads, cancellation, plans, retention

def dispatch(run,register,recheck=False,phase=None):
    base=study.run_dir(run); stage='D3' if recheck else 'D2'
    with lock(DATA/'locks'/('run-'+run+'.lock')):
        s=study.run_state(run)
        cancellation.run_stopped(run)
        if plans.pending(s) and phase is None:raise Error('A dispatch plan owns this study; use recover-plan')
        if s.get('active_actor') or s.get('dispatch_active') or s.get('dispatch_blocked'): raise Error('Run is busy')
        expected='D3' if recheck else 'D1'
        if not any(v.get('status')=='verified' and v['stage']==expected and v.get('cut')=='packets-out' for v in s['legs'].values()): raise Error('Labelers require a verified packets-out leg')
        ws=Path(s['latest_workspace']); tasks=ws/'out/handoff-D'
        if recheck: tasks=tasks/'recheck'
        tasks=tasks/'tasks'
        if not tasks.is_dir(): raise Error('Labeler task folder missing')
        rooms=[p for p in sorted(tasks.iterdir()) if p.is_dir()]
        if not rooms: raise Error('No labeler tasks')
        # Resolve the entire return cohort before any model turn, with exact input identity.
        lead_records={}
        for room in rooms:
            expected=leads.hashes(ws/'package'/room.name)
            if recheck:
                checkpoint=s.get('case_returns',{}).get(room.name)
                if not checkpoint: raise Error('No D2 return checkpoint for '+room.name)
                lead_records[room.name]=leads.inspect_checkpoint(checkpoint,expected)
            else: lead_records[room.name]=leads.require(room.name,expected)
        did=identity(run+'-'+stage+'labels-'+uuid.uuid4().hex[:8]); root=DATA/'dispatches'/did; root.mkdir(parents=True)
        write(root/'input.json',{'run':run,'stage':stage,'source':str(ws),'tasks':str(tasks),'room_names':[p.name for p in rooms],'recheck':recheck,'leads':lead_records})
        plans.claim(s,'labelers',stage,did,phase)
        s['dispatch_active']=did; write(base/'state.json',s)
    return execute(root,register)

def recover(dispatch_id,register,reset_stop=False):
    root=DATA/'dispatches'/identity(dispatch_id); inp=read(root/'input.json'); run=inp['run']; base=study.run_dir(run)
    with lock(DATA/'locks'/('run-'+run+'.lock')):
        s=study.run_state(run)
        if s.get('active_actor') or s.get('dispatch_active'): raise Error('Run is busy')
        if s.get('dispatch_blocked')!=dispatch_id: raise Error('This is not the blocked dispatch')
        if reset_stop:(base/'STOP.json').unlink(missing_ok=True)
        cancellation.run_stopped(run);cancellation.reset(root)
        s['dispatch_active']=dispatch_id; write(base/'state.json',s)
    return execute(root,register)

def execute(root,register):
    inp=read(root/'input.json'); run=inp['run']; stage=inp['stage']; base=study.run_dir(run); s=study.run_state(run)
    ws=Path(inp['source']); tasks=Path(inp['tasks']); rooms=[tasks/n for n in inp['room_names']]; did=root.name; recheck=inp['recheck']
    token=cancellation.gate(root)
    def one(room):
        token.check()
        dest=root/'returns'/room.name
        prior=read(dest/'run.json',{})
        if prior.get('validated'):
            return {'room':room.name,'status':'returned','actor':prior['actor'],'checkpoint':prior['checkpoint']}
        jobfile=root/'jobs'/(room.name+'.json'); job=read(jobfile,{})
        aid=job.get('actor') or identity(did+'-'+room.name)
        try:
            if not job:
                rec=inp['leads'][room.name]
                st=archive.restore(rec['checkpoint'],aid)
                # Original files are preserved. The new task and return get distinct folders.
                delivery=actor_dir(aid)/'workspace'/('return-'+stage)
                copy_tree(room,delivery)
                instruction=('You are the original case lead, resumed for a return to this room. '
                    'The prior coding task is closed. Preserve its files and history. Follow the new '
                    'return task in return-'+stage+'/TASK.md, using its current model VERSION. '
                    'Write only the requested return into out/return-'+stage+'. '
                    'Resolve all supported local exceptions with evidence. Do not access other rooms.')
                st.update(role='labeler',case_sub=room.name,continuation_instructions=instruction,dispatch_id=did,study_run=run)
                write(actor_dir(aid)/'state.json',st)
                job={'actor':aid,'parent_checkpoint':rec['checkpoint'],'coding_failures':0,'attempts':0}
                write(jobfile,job)
            a=register(aid)
            if job['coding_failures']>=2: raise Error('Two invalid completed returns; inspect the same lead before further repair')
            for _ in range(2-job['coding_failures']):
                prompt=('From the workspace root read return-'+stage+'/TASK.md and RETURN-D.md in that folder. '
                        'Use that folder for the supplied task files. Write model-D.md and adaptations.jsonl '
                        'in out/return-'+stage+'. Preserve earlier work. Complete this return and stop.')
                if job.get('defects'): prompt+=' Repair these checker defects in the same return: '+job['defects']
                job['attempts']+=1; write(jobfile,job)
                token.call(a.message,prompt); a.wait()
                if a.state.get('boundary')!='completed': raise Error('Mechanical interruption; lead store retained for recovery')
                receipt=a.checkpoint(); job['checkpoint']=receipt['checkpoint'];write(jobfile,job)
                out=a.base/'workspace/out'/('return-'+stage); dest.mkdir(parents=True,exist_ok=True)
                attempt=root/'attempts'/room.name/str(job['attempts'])
                copy_tree(out,attempt)
                for name in ('model-D.md','adaptations.jsonl'):
                    if (out/name).is_file(): shutil.copy2(out/name,dest/name)
                    else: (dest/name).unlink(missing_ok=True)
                metadata={'actor':aid,'model':a.state['model'],'effort':a.state['effort'],
                    'session_id':a.state['thread_id'],'checkpoint':receipt['checkpoint'],
                    'parent_checkpoint':job['parent_checkpoint'],'attempts':job['attempts'],
                    'version':(room/'VERSION').read_text().strip(),'validated':False}
                write(dest/'run.json',metadata)
                args=['D','--root',str(ws),'--out',str(ws/'out'),'--drops',str(root/'returns'),'--check',room.name]
                if recheck: args.append('--recheck')
                result=study.trusted(run,'ingest.py',args,ws)
                atomic(attempt/'check.txt',result.stdout+result.stderr)
                if result.returncode==0:
                    metadata['validated']=True;write(dest/'run.json',metadata);retention.ready(aid)
                    return {'room':room.name,'status':'returned','actor':aid,'checkpoint':receipt['checkpoint']}
                job['coding_failures']+=1;job['defects']=(result.stdout+result.stderr)[-12000:];write(jobfile,job)
            raise Error('Two invalid completed returns; same lead and all attempts preserved')
        except Exception as e:
            if 'a' in locals(): a.release()
            return {'room':room.name,'status':'unreturned','actor':aid,'error':str(e)}
    try:
        results=cancellation.bounded(rooms,one,s['fleet_parallel'],token)
        write(root/'RESULT.json',results)
        if any(x['status']!='returned' for x in results): raise Error('Labeler returns incomplete; stores retained at '+str(root))
        dest=base/'deliveries'/did; copy_tree(ws,dest)
        drops=dest/'DROPS/D'
        if recheck: drops=drops/'recheck'
        copy_tree(root/'returns',drops)
        atomic(drops/'DONE',f'returned {len(results)} unreturned 0\n'); atomic(drops/'UNRETURNED.tsv','sub\treason\n')
        # Ingest checks scientific return structure before the next check leg can open.
        args=['D','--root',str(dest),'--out',str(dest/'out')]+(['--recheck'] if recheck else [])
        result=study.trusted(run,'ingest.py',args,dest); atomic(root/'ingest.txt',result.stdout+result.stderr)
        if result.returncode or len((drops/'UNRETURNED.tsv').read_text().splitlines())>1: raise Error('Labeler ingest rejected returns; inspect '+str(root/'ingest.txt'))
        with lock(DATA/'locks'/('run-'+run+'.lock')):
            s=study.run_state(run); s.setdefault('case_returns',{}).update({x['room']:x['checkpoint'] for x in results}); s.update(latest_workspace=str(dest),dispatch_active=None); s.pop('dispatch_blocked',None);plans.complete(s,did); write(base/'state.json',s)
        return {'dispatch':did,'complete':True,'results':results}
    except BaseException as e:
        with lock(DATA/'locks'/('run-'+run+'.lock')):
            s=study.run_state(run); s.update(dispatch_active=None,dispatch_blocked=did); write(base/'state.json',s)
        write(root/'ERROR.json',{'error':str(e),'utc':now()}); raise
