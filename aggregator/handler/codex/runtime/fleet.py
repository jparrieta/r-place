"""Bounded independent readers, shared packets and validation across two backends."""
import concurrent.futures, fnmatch, json, os, shutil, tempfile, uuid
from pathlib import Path
from .common import *
from . import actors, study, archive, arms, cancellation, plans, retention


def jobs_for(workspace,stage,arm,round=None,only=None):
    pk,ret,raw=study.dispatch_paths(stage,round); ws=inside(workspace)
    directory=ws/pk; spec=(ws/ret).read_text(); manifest=read(directory/'MANIFEST.json',{})
    shared=[]
    for glob in filter(None,arm.get('shared','').split(',')): shared.extend(sorted(directory.glob(glob)))
    shared=set(shared); packets=[p for p in sorted(directory.glob('*.md')) if p not in shared and not p.name.startswith('RETURN-')]
    groups={}
    for p in packets:
        info=manifest.get(p.stem,{})
        key=identity(info.get('group') or p.stem)
        if only and key not in only and p.stem not in only: continue
        groups.setdefault(key,[]).append((p,info))
    if not groups: raise Error('No packets to dispatch')
    jobs=[]
    shared_text='\n\n'.join('<<< '+p.name+' >>>\n'+p.read_text() for p in sorted(shared))
    for group,parts in groups.items():
        parts.sort(key=lambda v:v[1].get('part',0))
        if any(x[1].get('parts',len(parts))!=len(parts) for x in parts): raise Error('Incomplete multipart group: '+group)
        jobs.append({'group':group,'parts':[{'name':p.stem,'text':p.read_text(),'sha256':sha(p),'rule':info} for p,info in parts],'shared':shared_text,'spec':spec,'schema':read((ws/ret).with_suffix('.schema.json'),{}),'raw':raw})
    return jobs


def one(job,replica,root,config,validator,register):
    token=cancellation.gate(root);token.check()
    group=job['group']; marker=validator.end_marker_of(job['spec'],None)
    if not marker: raise Error('Return specification has no end marker')
    # IDs remain unique across rebuilds and reissues, never overwriting older returns.
    for attempt in range(3):
        token.check()
        rid='r'+str(config.get('offset',0)+replica+attempt*config['n'])
        aid=identity(root.name+'-'+group+'-'+rid)
        d=root/'returns'/group; d.mkdir(parents=True,exist_ok=True)
        session_record=root/'jobs'/(group+'-'+rid+'.json')
        prior=read(session_record)
        if prior and prior.get('status')=='valid': return prior
        if prior and prior.get('status')=='invalid': continue
        accepted=read(root/'jobs'/(group+'-'+rid+'-parts.json'),[])
        if prior and prior.get('status')=='interrupted':
            aid=identity(aid+'-rec'+uuid.uuid4().hex[:6])
            if accepted:
                restored=archive.restore(accepted[-1]['meta']['checkpoint'],aid)
                restored.update(role='reader',read_only=True); write(actor_dir(aid)/'state.json',restored)
                (actor_dir(aid)/'workspace/out/PAUSE').unlink(missing_ok=True)
        if not actor_dir(aid).exists():
            with tempfile.TemporaryDirectory(prefix='reader-',dir=TMP) as tmp:
                empty=Path(tmp); (empty/'out').mkdir()
                write(empty/'packet.json',job)
                if config.get('route')=='openrouter':
                    from . import openrouter
                    openrouter.create(aid,empty,config,config['binding'])
                else:
                    actors.create(aid,empty,config['model'],config['effort'],role='reader',instructions='You are an independent research packet reader. Read only the supplied packet and shared material. Follow its return specification exactly. Do not consult other agents. Do not use tools or the network.',read_only=True)
        actor=register(aid); actor.state.update(dispatch_id=root.name,study_run=read(root/'input.json',{}).get('run'));actor.save()
        rows=[]; rawparts=[]; metas=[]
        try:
            for i,part in enumerate(job['parts']):
                if i<len(accepted):
                    rows.extend(accepted[i]['rows']); rawparts.append(accepted[i]['raw']); metas.append(accepted[i]['meta']); continue
                if (actor_dir(aid)/'workspace/out/PAUSE').exists(): raise Error('Reader paused; explicit dispatch recovery required')
                prefix=job['shared']+'\n<<< RETURN >>>\n'+job['spec']+'\n' if i==0 else ''
                prompt=prefix+'<<< '+part['name']+' >>>\n'+part['text']+'\nReturn only the required JSON lines followed by the end marker.'
                token.call(actor.message,prompt); actor.wait()
                if actor.state.get('boundary')!='completed': raise Error(actor.state.get('error') or 'Service/interruption stop, store retained')
                raw=actor.final(); parsed,why=validator.validate(raw,marker,job['schema'],part['rule'].get('items'),part['rule'])
                meta={'packet':part['name'],'group':group,'reader':rid,'reissue':attempt,'served':actor.state['effective'].get('model'),'effort':actor.state['effort'],'usage':actor.state.get('usage'),'thread_id':actor.state['thread_id'],'packet_sha256':part['sha256'],'valid':parsed is not None,'why':why}
                meta.update(route=config.get('route','codex'),requested=config['model'],provider=actor.state['effective'].get('provider'),generation_id=actor.state['effective'].get('generation_id'))
                receipt=actor.checkpoint(); meta['checkpoint']=receipt['checkpoint']
                metas.append(meta); rawparts.append(raw)
                if parsed is None:
                    atomic(d/(rid+'.failed.txt'),str(why)+'\n'+raw)
                    write(session_record,{'status':'invalid','actor':aid,'why':why,'attempt':attempt});retention.ready(aid)
                    break
                rows.extend(parsed); accepted.append({'rows':parsed,'raw':raw,'meta':meta}); write(root/'jobs'/(group+'-'+rid+'-parts.json'),accepted)
            else:
                atomic(d/(rid+'.jsonl'),''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
                atomic(d/(rid+'.raw.txt'),'\n\n'.join(rawparts)); write(d/(rid+'.meta.json'),metas if len(metas)>1 else metas[0])
                result={'status':'valid','actor':aid,'group':group,'reader':rid,'lines':len(rows),'checkpoints':[x['checkpoint'] for x in metas]}; write(session_record,result); retention.ready(aid); return result
            atomic(d/(rid+'.raw.txt'),'\n\n'.join(rawparts)); write(d/(rid+'.meta.json'),metas)
        except Exception as e:
            actor.release()
            result={'status':'interrupted','actor':aid,'group':group,'reader':rid,'error':str(e),'coding_failure':False}; write(session_record,result); return result
    return {'status':'exhausted','group':group,'reader':replica,'coding_failure':True}


def dispatch(run,stage,register,round=None,only=None,dry_run=False,phase=None):
    base=study.run_dir(run); identity(stage)
    with lock(DATA/'locks'/('run-'+run+'.lock')):
        s=study.run_state(run)
        cancellation.run_stopped(run)
        if plans.pending(s) and phase is None:raise Error('A dispatch plan owns this study; use recover-plan')
        arms.frozen(base)
        if s['active_actor'] or s.get('dispatch_active') or s.get('dispatch_blocked'): raise Error('Run has an active leg or dispatcher')
        arm=read(base/'arm.json').get('D2' if stage=='D3' else stage,{}).get('readers')
        if not arm: raise Error('No readers declared for stage '+stage)
        arms.validate(arm)
        ws=Path(s['latest_workspace'])
        relevant=[v for v in s['legs'].values() if v['status']=='verified' and v['cut']=='packets-out' and v['stage'] in (stage, 'D1' if stage=='D2' else stage)]
        if not relevant: raise Error('No verified packets-out checkpoint for this dispatch')
        jobs=jobs_for(ws,stage,arm,round,only)
        if dry_run: return {'groups':len(jobs),'readers':arm['n'],'jobs':len(jobs)*arm['n'],'route':arm.get('route','codex'),'fleet_arm':s.get('fleet_arm','codex'),'model':arm['model'],'effort':arm['effort'],'parallel':s['fleet_parallel']}
        existing_raw=ws/jobs[0]['raw']
        if existing_raw.exists() and not only: raise Error('Returns exist. Request a named subset with --only for reissue')
        if existing_raw.exists():
            import re
            ids=[int(p.stem[1:]) for p in existing_raw.glob('*/r*.jsonl') if re.fullmatch(r'r[0-9]+',p.stem)]
            arm={**arm,'offset':max(ids,default=0)}
        did=identity(run+'-'+stage+'-'+uuid.uuid4().hex[:8]); root=DATA/'dispatches'/did; root.mkdir(parents=True)
        write(root/'input.json',{'run':run,'stage':stage,'round':round,'jobs':jobs,'arm':arm,'source':str(ws),'only':only})
        plans.claim(s,'fleet',stage,did,phase,round)
        s['dispatch_active']=did; write(base/'state.json',s)
    return execute(root,register)


def recover(dispatch_id,register,reset_stop=False):
    root=DATA/'dispatches'/identity(dispatch_id); inp=read(root/'input.json')
    if not inp: raise Error('Unknown dispatch')
    if 'room_names' in inp:
        from . import labelers
        return labelers.recover(dispatch_id,register,reset_stop=reset_stop)
    run=inp['run']; base=study.run_dir(run)
    with lock(DATA/'locks'/('run-'+run+'.lock')):
        s=study.run_state(run)
        if s.get('active_actor') or s.get('dispatch_active'): raise Error('Run is busy')
        if s.get('dispatch_blocked')!=dispatch_id: raise Error('This is not the blocked dispatch')
        if reset_stop:(base/'STOP.json').unlink(missing_ok=True)
        cancellation.run_stopped(run);cancellation.reset(root)
        s['dispatch_active']=dispatch_id; write(base/'state.json',s)
    return execute(root,register)


def execute(root,register):
    inp=read(root/'input.json'); run=inp['run']; base=study.run_dir(run); s=study.run_state(run)
    jobs=inp['jobs']; arm=inp['arm']; ws=Path(inp['source']); did=root.name; only=inp.get('only')
    results=[]
    try:
        arms.frozen(base)
        token=cancellation.gate(root);token.check()
        if arm.get('route')=='openrouter':
            from . import openrouter
            binding=token.call(openrouter.bind,base,arm)
            write(root/'routing.json',binding)
            arm={**arm,'binding':binding}
        validator=study.load_module(base/'trusted/fleet.py','rplace_fleet_validate')
        items=[(job,r) for job in jobs for r in range(1,arm['n']+1)]
        results=cancellation.bounded(items,lambda item:one(item[0],item[1],root,arm,validator,register),s['fleet_parallel'],token)
        complete=all(x['status']=='valid' for x in results)
        write(root/'RESULT.json',{'complete':complete,'results':results})
        if not complete: raise Error('Fleet has unresolved returns; stores retained at '+str(root))
        # New materialized workspace, no mutation of a saved actor's files.
        dest=base/'deliveries'/did; copy_tree(ws,dest)
        raw=dest/jobs[0]['raw']
        if raw.exists():
            if not only: raise Error('Dispatch destination already exists; use a declared rebuild')
            # Reader IDs are offset beyond previous IDs; prior evidence is preserved.
            pass
        copy_tree(root/'returns',raw)
        write(raw/'arm.json',{'route':arm.get('route','codex'),'fleet_arm':s.get('fleet_arm','codex'),'alias':arm['model'],'served':arm.get('binding',{}).get('model',arm['model']),'provider':arm.get('binding',{}).get('provider'),'effort':arm['effort'],'readers':arm['n'],'dispatch':did,'binding':arm.get('binding')})
        write(raw/'DONE',{'complete':True,'packets':len(jobs),'returns':len(results),'dispatch':did})
        with lock(DATA/'locks'/('run-'+run+'.lock')):
            s=study.run_state(run)
            if s.get('dispatch_active')!=did: raise Error('Dispatch ownership changed')
            s['latest_workspace']=str(dest); s['dispatch_active']=None; s.pop('dispatch_blocked',None); plans.complete(s,did);write(base/'state.json',s)
        return {'dispatch':did,'complete':True,'results':results}
    except BaseException as e:
        with lock(DATA/'locks'/('run-'+run+'.lock')):
            s=study.run_state(run); s['dispatch_active']=None; s['dispatch_blocked']=did; write(base/'state.json',s)
        write(root/'ERROR.json',{'error':str(e),'utc':now()}); raise
