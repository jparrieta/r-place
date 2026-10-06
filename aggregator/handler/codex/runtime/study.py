"""Stage barriers and trusted validation. The supplied run is never mutated."""
import csv, importlib.util, json, os, re, shutil, subprocess, sys, tempfile, uuid
from pathlib import Path
from .common import *
from . import actors, arms, archive, plans, cancellation, retention, backends

INSTRUMENT=REPO/'aggregator/instrument'
HARNESS=REPO/'aggregator/handler/claude'

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_dir(run): return DATA/'runs'/identity(run)
def run_state(run):
    s=read(run_dir(run)/'state.json')
    if not s: raise Error('Unknown study run: '+run)
    return s

def build(run, source=None, fleet_arm='codex'):
    arm,selection=arms.resolve(fleet_arm)
    source=inside(source or DATA/'prepared/openai-v43-1'); dest=run_dir(run)
    with lock(DATA/'locks'/('run-'+run+'.lock')):
        if dest.exists(): raise Error('Run already exists; use a new name')
        if read(source/'CONTROL/sessions.json',{}): raise Error('Source has native sessions; restore a checkpoint instead')
        ensure_space(sum(p.stat().st_size for p in files(source/'00_GIVE-THE-AGENT'))+100*1024**2); dest.mkdir(parents=True)
        try:
            copy_tree(source/'00_GIVE-THE-AGENT',dest/'baseline')
            # Current instrument, not stale prepared-run Claude launch instructions.
            initial=('AGENT.md','AGENTS.md','CONTRACT-aggregator.md','METHOD.md','STANDING-INSTRUCTIONS.md','WRITING.md','OPENAI-RUNTIME.md','PLATFORM-codex.md','PRIOR-template.md')
            for p in (dest/'baseline').glob('*.md'):
                if p.name not in initial: p.unlink()
            for name in initial: shutil.copy2(INSTRUMENT/name,dest/'baseline'/name)
            copy_tree(INSTRUMENT/'tools',dest/'baseline/tools')

            (dest/'baseline/tools/fleet.py').unlink(missing_ok=True)
            (dest/'baseline/CLAUDE.md').unlink(missing_ok=True)
            # Prepared input supplies data, but cards and stage-gated literature
            # must match the current instrument, including retired shelf entries.
            (dest/'drops').mkdir(parents=True,exist_ok=True)
            for p in files(source/'DROPS'):
                rel=p.relative_to(source/'DROPS')
                if len(rel.parts)>1 and rel.parts[1] in ('stages','shelves'): continue
                target=dest/'drops'/rel; target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(p,target)
            copy_tree(HARNESS/'handling',dest/'drops/E2/handling')
            copy_tree(INSTRUMENT/'handoff',dest/'drops/D1/handoff')
            shutil.copy2(INSTRUMENT/'SCHEMA-adaptations.md',dest/'drops/D1/SCHEMA-adaptations.md')
            for stage in ('B2','B3','B4','C2','C5','D1','D2','D3','E1'):
                (dest/'drops'/stage).mkdir(parents=True,exist_ok=True)
                shutil.copy2(INSTRUMENT/'FLEET.md',dest/'drops'/stage/'FLEET.md')
            for p in INSTRUMENT.glob('stages/STAGE-*.md'):
                st=p.name.split('-')[1]; d=dest/'drops'/st/'stages'; d.mkdir(parents=True,exist_ok=True)
                shutil.copy2(p,d/p.name)
                shelf=INSTRUMENT/'shelves'/st
                if shelf.is_dir(): copy_tree(shelf,dest/'drops'/st/'shelves')
            copy_tree(INSTRUMENT/'tools',dest/'trusted')
            write(dest/'arm.json',arm)
            write(dest/'fleet-arm.json',{**selection,'arm_sha256':sha(dest/'arm.json')})
            state={'id':run,'created_utc':now(),'source':str(source),'latest_workspace':str(dest/'baseline'),'active_actor':None,'legs':{},'finished_stages':[],'auto_dispatch':True,'fleet_parallel':3,'fleet_arm':fleet_arm,'version':'v43-openai-1','continuity':'native-checkpoint'}
            write(dest/'trusted-hashes.json',inventory(dest/'trusted')); write(dest/'state.json',state)
            (dest/'sealed').mkdir()
        except BaseException:
            write(dest/'BUILD-FAILED.json',{'utc':now(),'status':'preserved for inspection'}); raise
    return state

def trusted(run, tool, args, cwd):
    d=run_dir(run); trust=d/'trusted'
    if inventory(trust)!=read(d/'trusted-hashes.json'): raise Error('Trusted instrument changed after build')
    list(files(cwd)) # reject all links before privileged validators read scientific files
    runner="import runpy,sys; sys.path.insert(0,sys.argv[1]); p=sys.argv.pop(1)+'/'+sys.argv.pop(1); sys.argv[0]=p; runpy.run_path(p,run_name='__main__')"
    return subprocess.run([sys.executable,'-I','-S','-B','-c',runner,str(trust),tool,*map(str,args)],cwd=cwd,env=env(),capture_output=True,text=True,timeout=600)

def descriptor(leg):
    return load_module(INSTRUMENT/'tools/steps.py','rplace_steps').parse(leg)

def dispatch_paths(stage,round=None):
    if stage=='B2':
        if not round or not re.fullmatch(r'(\d+|gold|stab-[12])',str(round)): raise Error('B2 needs round number, gold, stab-1 or stab-2')
        return ('out/_packets-B2/round-'+str(round),'out/RETURN-B2.md','out/_fleet_raw/B2/round-'+str(round))
    if stage in ('D2','D3'):
        pk='out/verdict-D'+('/recheck' if stage=='D3' else '')
        return pk,pk+'/RETURN-D2v.md','out/_fleet_raw/'+stage+'v'
    return 'out/_packets-'+stage,'out/RETURN-'+stage+'.md','out/_fleet_raw/'+stage

def check_ready(run, desc, ws):
    if desc['kind']=='check':
        stage=desc['stage']; rounds=[desc['round']] if stage!='B2' or desc['round'] else ['gold','stab-1','stab-2']
        for r in rounds:
            raw=ws/dispatch_paths(stage,r)[2]
            rec=read(raw/'DONE')
            if not rec or not rec.get('complete'): raise Error('Validated dispatch is not complete: '+str(raw))
        if stage=='D2' and not (ws/'DROPS/D/DONE').exists(): raise Error('D2 labeler returns are not complete')
    if desc['kind']=='recheck':
        if not (ws/'DROPS/D/recheck/DONE').exists() or not read(ws/'out/_fleet_raw/D3v/DONE',{}).get('complete'): raise Error('D3 recheck returns are not complete')

def check_order(s, leg):
    desc=descriptor(leg); stage=desc['stage']
    if leg in s['legs']: raise Error('Leg already prepared; resume its actor')
    rows=load_module(INSTRUMENT/'tools/steps.py','rplace_steps').table()
    stages=list(dict.fromkeys(r['stage'] for r in rows))
    prev=stages[stages.index(stage)-1] if stages.index(stage)>0 else None
    if prev and prev not in s['finished_stages']: raise Error('Preceding stage is not verified: '+prev)
    if stage in s['finished_stages']: raise Error('Stage is already finished; use an interview fork')
    existing=[r for r in s['legs'].values() if r['stage']==stage]
    number=int(desc['round'] or desc['count']) if desc['count'] else None
    if not existing:
        if desc['step']!='a': raise Error('Start a stage at its first step')
        if desc['cont']: raise Error('Only a paused leg can have a -p continuation')
        if number not in (None,1): raise Error('Start a stage at its first repeat, count 1')
        return
    last=descriptor(existing[-1]['leg']); last_status=existing[-1]['status']
    if last_status not in ('verified','paused'): raise Error('Previous leg is not resolved')
    if last_status=='paused':
        if desc['step']!=last['step'] or desc['count']!=last['count'] or int(desc['cont'] or 1)!=int(last['cont'] or 1)+1: raise Error('Continue the paused leg with its next -p count')
        return
    if desc['cont']: raise Error('Only a paused leg can have a -p continuation')
    last_number=int(last['round'] or last['count']) if last['count'] else None
    if stage=='B2' and last['step']=='b' and desc['step']=='a':
        if number!=(last_number or 0)+1: raise Error('Pilot round must advance by one')
    elif desc['step']==last['step']:
        row=next(r for r in rows if r['stage']==stage and r['step']==desc['step'])
        if row['repeat']!='yes' or number!=(last_number or 0)+1: raise Error('Repeated step must advance by one')
    elif desc['step']!=chr(ord(last['step'])+1): raise Error('Cannot skip or reverse a stage step')
    elif stage=='B2' and desc['step']=='b':
        if number!=last_number: raise Error('Check the round just built')
    elif number not in (None,1): raise Error('Start a repeated step at its first count, 1')

def prepare(run, leg, block_id=None):
    backends.require_run(run,'prepare')
    desc=descriptor(leg); stage=desc['stage']; base=run_dir(run)
    with lock(DATA/'locks'/('run-'+run+'.lock')):
        from . import blocks
        blocks.guard(run,block_id)
        arms.frozen(base)
        s=run_state(run)
        cancellation.run_stopped(run)
        if plans.pending(s):raise Error('A dispatch plan is incomplete; use recover-plan')
        if s.get('active_actor') or s.get('dispatch_active') or s.get('dispatch_blocked'): raise Error('A leg or dispatch still owns this run')
        if s.get('publication',{}).get('status')=='blocked':raise Error('Git publication is blocked; use publish-branch before advancing')
        check_order(s,leg)
        from . import branches
        branches.seal(base,s,leg)
        src=Path(s['latest_workspace']); check_ready(run,desc,src)
        if stage=='E2':
            for f in ('proposal.md','design-note.md'):
                if not (base/'drops/E2/handling'/f).is_file(): raise Error('Supply '+str(base/'drops/E2/handling'/f))
        arm=read(base/'arm.json')[stage]; ent={**arm,**arm.get('legs',{}).get(desc['step'],{})}
        aid=run+'-'+leg+'-'+uuid.uuid4().hex[:6]
        ins=('You are the research aggregator. Keep this live conversation available to the principal investigator. Record interventions in out/diary and save out/_head.md as you work. Scientific outputs belong in out/. Shell starts in out/: use cd .. before the instrument commands. Instrument files are read-only. Follow AGENT.md and the current stage, with OPENAI-RUNTIME.md taking precedence for runtime operations. Request fleets only by closing at packets-out; the controller dispatches after trusted validation. Do not spawn your own readers. Stop after this leg. If out/PAUSE exists, save a safe pause through tools/done.sh. Never access other actors or handler state.')
        if s['legs']:
            previous=list(s['legs'].values())[-1]
            checkpoint=previous.get('checkpoint')
            if not checkpoint: raise Error('Previous leg has no native checkpoint; notes cannot substitute for its history')
            restored=archive.restore(checkpoint,aid,mode='continuation')
            if restored.get('backend')=='openrouter' or restored.get('boundary')!='completed':
                raise Error('Study progression requires a completed native aggregator checkpoint')
            if restored.get('origin_role')!='aggregator': raise Error('Previous checkpoint is not the aggregator')
            # Preserve the archived parent. The next leg receives its native history plus
            # the controller-validated delivery filesystem, with both inventories recorded.
            ws=actor_dir(aid)/'workspace'
            before=inventory(ws); delivered=inventory(src)
            shutil.rmtree(ws); copy_tree(src,ws)
            restored.update(role='aggregator',run=run,leg=leg,model=ent['analyst'],effort=ent['effort'],instructions=ins,continuation_instructions=ins,leg_started=False)
            write(actor_dir(aid)/'state.json',restored)
            write(actor_dir(aid)/'continuation.json',{'parent_checkpoint':checkpoint,'previous_leg':previous['leg'],
                  'parent_workspace':before,'delivered_workspace':delivered,'source':str(src),
                  'model':ent['analyst'],'effort':ent['effort'],'utc':now()})
        else:
            actors.create(aid,src,ent['analyst'],ent['effort'],run=run,leg=leg,instructions=ins)
        ws=actor_dir(aid)/'workspace'
        from . import questions
        questions.deliver(run,ws)
        (ws/'out/PAUSE').unlink(missing_ok=True)
        # Stage drops are delivered only when the stage opens.
        copy_tree(base/'drops'/stage,ws)
        if stage in ('E1','E2'):
            if (base/'sealed').exists(): copy_tree(base/'sealed',ws/'out')
        for name,value in (('.stage',stage),('.leg',leg)):
            atomic(ws/name,value+'\n')
        stagefiles=sorted((ws/'stages').glob('STAGE-'+stage+'-*.md'))
        if len(stagefiles)!=1: raise Error('Expected exactly one current stage card')
        stagefile=str(stagefiles[0].relative_to(ws)); atomic(ws/'.stagefile',stagefile+'\n')
        if stage in ('D2','D3'):
            args=['D','--root',str(ws),'--out',str(ws/'out')]+(['--recheck'] if stage=='D3' else [])
            result=trusted(run,'ingest.py',args,ws)
            atomic(base/('ingest-'+leg+'.txt'),result.stdout+result.stderr)
            if result.returncode: raise Error('Ingest failed; inspect '+str(base/('ingest-'+leg+'.txt')))
        prompt=f'Stage {stage}, leg {leg}. From the workspace root, read AGENT.md, OPENAI-RUNTIME.md, out/_head.md, {stagefile}, the output of python3 tools/mem.py diary --last 5, then python3 tools/validate.py --open {stage}. Perform only this leg. Save head and diary continuously. Close with bash tools/done.sh {stage} and the required cut, then stop.'
        prompt=branches.notice(s)+prompt+' Read python3 tools/mem.py asks for investigator answers and unresolved assumptions before dependent work. Answers in out/_answers are written only by the controller.'
        atomic(actor_dir(aid)/'first-message.txt',prompt)
        s['latest_workspace']=str(ws);s['active_actor']=aid; s['legs'][leg]={'actor':aid,'stage':stage,'leg':leg,'status':'prepared'}; write(base/'state.json',s)
        return {'actor':aid,'prompt':prompt}

def frozen_inputs(run,state,workspace):
    """Compare against controller-committed history, never a rehashed analyst receipt."""
    trust=run_dir(run)/'trusted'
    if inventory(trust)!=read(run_dir(run)/'trusted-hashes.json'):raise Error('Trusted instrument changed after build')
    vlib=load_module(trust/'vlib.py','rplace_frozen_vlib')
    for stage,names in (('D3',vlib.MODEL_FILES),('D4',('branches.jsonl','subforms.jsonl','crosslinks.jsonl'))):
        legs=[row for row in state['legs'].values() if row['stage']==stage and row.get('status')=='verified']
        if not legs or not legs[-1].get('checkpoint'):raise Error('Missing verified '+stage+' freeze checkpoint')
        manifest=archive.verify_checkpoint(legs[-1]['checkpoint'])
        if manifest.get('format') not in ('rplace-native-v1','rplace-claude-v1') or manifest.get('boundary')!='completed':raise Error('Freeze requires a completed native checkpoint')
        if manifest.get('backend')=='claude' and not manifest['record']['scientific']:raise Error('Freeze requires a scientifically verified Claude close')
        if manifest.get('backend')=='claude' and manifest['record']['state'].get('label')!=stage+'.'+legs[-1]['leg']:
            raise Error('Claude freeze checkpoint belongs to another leg')
        expected={n.removeprefix('workspace/out/'):v['sha256'] for n,v in manifest['files'].items() if n.startswith('workspace/out/') and (n.removeprefix('workspace/out/') in names or (stage=='D3' and n.startswith('workspace/out/model/')))}
        paths=set(names)|set(expected)
        if stage=='D3':paths|={str(p.relative_to(workspace/'out')) for p in files(workspace/'out/model')}
        changed=[name for name in sorted(paths) if (sha(workspace/'out'/name) if (workspace/'out'/name).is_file() else None)!=expected.get(name)]
        if changed:raise Error('Frozen '+stage+' inputs changed: '+', '.join(changed))


def close(run, actor):
    backends.require(actor.state,'close')
    base=run_dir(run)
    with lock(DATA/'locks'/('run-'+run+'.lock')):
        s=run_state(run); st=actor.state; leg=st['leg']; stage=descriptor(leg)['stage']; ws=backends.workspace(actor)
        if s['active_actor']!=st['id']: raise Error('Actor does not own the current leg')
        if st.get('active_turn_id') or st.get('boundary')!='completed': raise Error('A completed native turn is required for study advancement')
        marker=ws/'out/_closes'/f'{stage}-{leg}.closed'
        if not marker.is_file(): raise Error('Analyst has not closed the leg with done.sh')
        cut=marker.read_text().splitlines()[-1].split()[-1]
        records=read(ws/'RUN.json',{}).get('legs',[])
        recorded=next((r for r in reversed(records) if r.get('leg')==leg and r.get('stage')==stage),None)
        if not recorded or recorded.get('session')!=st['thread_id'] or (recorded.get('cut') or 'close')!=cut:
            raise Error('Leg record is missing or does not match this native session; repair done.sh before advancement')
        if backends.name(st)=='claude':
            return close_claude(run,actor,s,ws,stage,leg,cut)
        report=trusted(run,'validate.py',[stage,str(ws),str(ws/'out')],ws)
        atomic(base/('validation-'+leg+'.txt'),report.stdout+report.stderr)
        valid=report.returncode==0
        if not valid and cut!='pause': raise Error('Trusted validation failed; resume the same actor to repair')
        if cut!='pause' and stage in ('D6','E1','E2'):frozen_inputs(run,s,ws)
        table=load_module(INSTRUMENT/'tools/steps.py','rplace_steps').table()
        laststep=[x['step'] for x in table if x['stage']==stage][-1]
        final=valid and cut!='pause' and descriptor(leg)['step']==laststep and (ws/'out'/f'handback-{stage}.md').is_file()
        if final and stage in ('D3','D4'):
            vlib=load_module(base/'trusted/vlib.py','rplace_freeze_receipt')
            digest=vlib.tree_hash(ws/'out') if stage=='D4' else vlib.model_hash(ws/'out')
            if not digest:raise Error('Cannot freeze missing '+stage+' inputs')
            atomic(ws/'out/_closes'/('tree-D4.sha256' if stage=='D4' else 'model-D3.sha256'),digest+'\n')
        # Probes and transcript storage are sealed from subsequent analyst legs until E1.
        close_record=read(base/('close-'+leg+'.json'),{})
        if close_record.get('turn_id')==st['last_turn_id'] and close_record.get('workspace')==inventory(ws):
            receipt=close_record['receipt']
        else:
            snap=ws/'out/_snap'/f'{stage}-leg-{leg}.sha256'
            if not snap.exists():
                snapped=trusted(run,'snap.py',[stage,'leg-'+leg,'--out',str(ws/'out')],ws)
                if snapped.returncode: raise Error('Leg snapshot failed: '+snapped.stderr)
            atomic(ws/'.tokens.json',json.dumps(st.get('usage',{})))
            receipt=actor.checkpoint()
            write(base/('close-'+leg+'.json'),{'turn_id':st['last_turn_id'],'workspace':inventory(ws),'receipt':receipt})
        probe_receipt=None
        if cut!='pause':
            from .probes import run_probe
            probe_receipt=run_probe(run,actor,receipt['checkpoint'])
        transcript=base/'sealed/_transcripts'; transcript.mkdir(parents=True,exist_ok=True)
        shutil.copy2(actor.base/'thread.json',transcript/(leg+'.json'))
        import json as native_json
        for rollout in (actor.base/'native/sessions').rglob('*.jsonl'):
            with rollout.open() as stream: meta=native_json.loads(stream.readline()).get('payload',{})
            if meta.get('id')==st['thread_id']:
                shutil.copy2(rollout,transcript/(leg+'.native.jsonl')); break
        atomic(transcript/'INDEX.md','# Native Codex transcripts\n\n'+''.join('- ['+p.name+']('+p.name+')\n' for p in sorted(p for p in transcript.iterdir() if p.suffix in ('.json','.jsonl'))))
        s['legs'][leg].update(probe=probe_receipt,status='paused' if cut=='pause' else 'verified',checkpoint=receipt['checkpoint'],cut=cut,validation_sha256=sha(base/('validation-'+leg+'.txt')))
        s['latest_workspace']=str(ws); s['active_actor']=None
        table=load_module(INSTRUMENT/'tools/steps.py','rplace_steps').table()
        laststep=[x['step'] for x in table if x['stage']==stage][-1]
        if final:s['finished_stages'].append(stage)
        if cut=='packets-out' and s.get('auto_dispatch'):
            s['dispatch_plan']=plans.new(stage,leg,descriptor(leg)['round'])
        write(base/'state.json',s)
        retention.ready(st['id'])
        event(base/'diary.jsonl',kind='close',leg=leg,checkpoint=receipt['checkpoint'],cut=cut)
        return {'receipt':receipt,'cut':cut,'stage':stage,'run':run}


def close_claude(run,actor,state,workspace,stage,leg,cut):
    """The platform owns validation, recall and publication. Never repeat them here."""
    if cut=='pause':raise Error('Claude paused-leg advancement is not admitted. Save the actor and retain the current leg.')
    if actor.state.get('undelivered'):raise Error('Claude has undelivered messages. Resolve them before closing this leg.')
    if Path(actor.state['claude_run']).resolve()/ '00_GIVE-THE-AGENT' != workspace.resolve():
        raise Error('Claude research workspace does not match its owning run')
    if stage in ('D6','E1','E2'):frozen_inputs(run,state,workspace)
    receipt=actor.close()
    verified=archive.verify_checkpoint(receipt['checkpoint'])
    if verified.get('backend')!='claude' or not verified.get('record',{}).get('scientific'):
        raise Error('Claude close did not produce verified scientific evidence')
    # Saved RUN.json and marker must agree too, not just the live workspace.
    expected=verified['files']
    for name in ('RUN.json',f'out/_closes/{stage}-{leg}.closed'):
        if expected.get('workspace/'+name,{}).get('sha256')!=sha(workspace/name):
            raise Error('Claude closed snapshot differs from the leg record')
    state['legs'][leg].update(backend='claude',status='verified',checkpoint=receipt['checkpoint'],cut=cut,
                             validation_sha256=verified['record']['files']['validation-report.txt']['sha256'])
    state.update(backend='claude',latest_workspace=str(workspace),active_actor=None)
    table=load_module(INSTRUMENT/'tools/steps.py','rplace_steps').table()
    laststep=[r['step'] for r in table if r['stage']==stage][-1]
    if descriptor(leg)['step']==laststep and 'workspace/out/handback-'+stage+'.md' in expected:
        if stage not in state['finished_stages']:state['finished_stages'].append(stage)
    raw=verified['record']['receipt']
    state['platform_publication']=raw.get('publication')
    # Claude preparation and fleets stay with the harness until their separate admission.
    state['platform_next_action']='Use the Claude harness for the next leg or fleet; controller automation is not admitted.'
    write(run_dir(run)/'state.json',state)
    event(run_dir(run)/'diary.jsonl',kind='close',backend='claude',leg=leg,checkpoint=receipt['checkpoint'],cut=cut)
    return {'backend':'claude','receipt':receipt,'cut':cut,'stage':stage,'run':run,
            'publication':raw.get('publication'),'next_action':state['platform_next_action']}
