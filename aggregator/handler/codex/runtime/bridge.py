"""File mailbox for the handler, and automatic capture of completed leg exits."""
import threading
from .common import *
from . import blocks, backends

HANDLER = '''You are the operational handler for this r/place study. Talk with the investigator while the aggregator works. Keep out/_head.md and append-only out/diary.jsonl. Do not infer findings or expose your private conversation to the aggregator.
The controller publishes out/status.json. To act, write a new JSON file out/requests/<unique-id>.json, using one action below. Read the matching out/responses/<unique-id>.json. A returned job ID is asynchronous: ask action job with that ID until completed or failed. Never repeat a request with a new ID just because it is slow. Never write outside this workspace or call another provider.
Actions: build (run, optional fleet_arm: codex or openrouter); prepare (run, leg); start (actor); message (actor, text); card (actor, text); pause (actor); stop (actor); close (run, actor); dispatch (run, stage, optional round); labelers (run, optional recheck); recover (dispatch, resumes the whole saved phase plan); recover-plan (run); stop-run (run); continue-run (run, clears a stop without starting a turn); restore (checkpoint, optional actor, interview only); resume-handler (checkpoint, optional actor, operational continuation); job (job).
Choose the investigator-authorized fleet arm when building. Codex is the default; OpenRouter uses the configured preset only for packet readers. Never change a study arm after build. Prepare returns actor and exact first prompt. Start sends that prompt. Analysis branching uses branch (source_run, checkpoint, run, leg), then branch-status (run). This creates an idle draft. The investigator supplies file changes through the panel or CLI. Use prepare-branch (run) to seal and publish the setup, then prepare its first leg without a turn. publish-branch (run) retries a failed Git push without repeating analysis. Start is separate. Never change a parent or invent authorization to start the branch. Prepare and start only the investigator's authorized leg. Respect study barriers. Aggregator leg closure automatically validates, archives, probes, and dispatches required fleets. Do not duplicate it. Cards are explicit investigator messages, never your entire context. Failures belong in your head and must be reported to the investigator. Mechanical failures preserve stores; do not silently change models or start fresh.
'''

HANDLER+='\nFor an investigator-approved finite range of repeated legs, use run-block (run, first, last). Example identifiers: A1b-01 through A1b-03. Get the last leg from the declared reading plan or investigator, never invent it. The controller prepares, starts and checks each leg, then stops at that bound. It stops at an actual interview cut or stage completion and never crosses to another step or stage. Read block-status (run); stop-block (run) stops after the current leg; resume-block (run) requires renewed investigator authorization after resolving the reported issue. No browser or handler turn needs to remain open. Do not issue separate starts for a running block. Tell the investigator about blocked judgment or execution, without inventing an answer.\n'
ALLOWED={'build','prepare','start','message','card','pause','stop','close','dispatch','labelers','recover','restore','resume-handler','recover-plan','stop-run','continue-run','job','branch','branch-status','prepare-branch','publish-branch','run-block','block-status','stop-block','resume-block'}

def tick(controller):
    # Snapshot the registry under its lock, then perform work without holding it.
    with controller.guard: actors=list(controller.actors.values())
    if any(a.state.get('active_turn_id') for a in actors) and __import__('shutil').disk_usage(DATA).free < 8*1024**3:
        for actor in actors:
            if actor.state.get('active_turn_id'):
                actor.interrupt(); actor.state['error']='Storage reserve reached; native store preserved. Free space before capture or continuation.'; actor.save()
        event(DATA/'controller-errors.jsonl',error='Storage reserve reached, active actors interrupted')
    states=controller.list()
    public={'runs':states['runs'],'actors':[{k:s.get(k) for k in ('id','role','run','leg','status','model','effort','checkpoint','error')} for s in states['actors']],'jobs':states['jobs'],'errors':states.get('errors',[])}
    for actor in actors:
        st=actor.state
        if not backends.allowed(st,'bridge'):continue
        ws=backends.workspace(actor); out=ws/'out'
        if st.get('handler_retired'):continue
        if st['role']=='handler':
            backends.require(st,'handler')
            with actor.guard:
                write(out/'status.json',public)
                for req in sorted((out/'requests').glob('*.json')):
                    key=identity(req.stem); response=out/'responses'/req.name
                    record=actor.base/'mailbox'/(key+'.json')
                    if record.exists(): continue
                    # Claim before execution. A crash is visible, never replayed blindly.
                    write(record,{'status':'claimed','utc':now()})
                    try:
                        if req.is_symlink() or req.stat().st_size>1024**2: raise Error('Invalid mailbox request')
                        data=read(req)
                        if data.get('action') not in ALLOWED: raise Error('Handler action not supported')
                        result={'status':'accepted','result':controller.action(data)}
                    except Exception as e: result={'status':'failed','error':str(e)}
                    write(record,result); write(response,result)
        if st.get('active_turn_id') or st.get('boundary')!='completed' or st.get('undelivered'): continue
        if st['role']=='aggregator' and st.get('run'):
            run=read(DATA/'runs'/st['run']/'state.json',{})
            marker=out/'_closes'/f"{st['leg'][:2]}-{st['leg']}.closed"
            if not blocks.manages_close(st['run'],st['id']) and run.get('active_actor')==st['id'] and marker.is_file() and st.get('auto_close_turn')!=st['last_turn_id']:
                st['auto_close_turn']=st['last_turn_id']; actor.save()
                controller.job(controller.close_leg,st['run'],st['id'],job_meta={'action':'close','run':st['run'],'actor':st['id']})
        elif backends.pause_marker(actor).exists() and st.get('pause_saved_turn')!=st['last_turn_id']:
            st['pause_saved_turn']=st['last_turn_id']; actor.save()
            controller.job(actor.checkpoint,job_meta={'action':'save','actor':st['id']})
    blocks.tick(controller)

def watch(controller):
    while not controller.stopping.wait(1):
        try: tick(controller)
        except Exception as e: event(DATA/'controller-errors.jsonl',error=str(e))
