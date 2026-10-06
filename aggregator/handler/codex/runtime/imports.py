"""Capture a completed CLI coder as a native interview checkpoint."""
import shutil,uuid
from pathlib import Path
from .common import *
from . import archive
from .native import fingerprint

def capture_cli(home,workspace,executable,model,effort,thread_id):
    home=inside(home); workspace=inside(workspace)
    if not thread_id: raise Error('CLI supplied no native thread ID')
    matched=None; last_started=None; last_completed=None; recorded_model=None; recorded_effort=None
    for path in (home/'sessions').rglob('*.jsonl'):
        with path.open() as stream:
            import json
            first=json.loads(stream.readline())
            if first.get('payload',{}).get('id')!=thread_id: continue
            for line in stream:
                row=json.loads(line); p=row.get('payload',{})
                if row.get('type')=='turn_context':
                    recorded_model=p.get('model') or recorded_model
                    recorded_effort=p.get('effort') or p.get('reasoning_effort') or recorded_effort
                if row.get('type')=='event_msg' and p.get('type')=='task_started': last_started=p.get('turn_id')
                if row.get('type')=='event_msg' and p.get('type')=='task_complete': last_completed=p.get('turn_id')
            matched=path;break
    if not matched or not last_completed or (last_started and last_started!=last_completed): raise Error('CLI has no completed persisted boundary; retain native store for recovery')
    if recorded_model and recorded_model!=model: raise Error('Requested model differs from the original CLI lead')
    if recorded_effort and recorded_effort!=effort: raise Error('Requested effort differs from the original CLI lead')
    aid='case-reader-'+uuid.uuid4().hex[:16]; base=actor_dir(aid);base.mkdir(parents=True)
    copy_tree(workspace,base/'workspace')
    for p in archive.native_files(home):
        q=base/'native'/p.relative_to(home);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
    st={'id':aid,'role':'case-reader','model':model,'effort':effort,'run':None,'leg':None,'status':'idle','thread_id':thread_id,'active_turn_id':None,'last_turn_id':last_completed,'boundary':'completed','created_utc':now(),'runtime':fingerprint(executable),'instructions':'Native CLI case reader, restored for interview. Work only in this workspace. Preserve the parent checkpoint.','read_only':False,'resume_path':str(base/'native'/matched.relative_to(home)),'capture_source':'native CLI completed rollout plus matching batch files'}
    write(base/'state.json',st)
    receipt=archive.commit(base,st);st.update(checkpoint=receipt['checkpoint'],status='saved');write(base/'state.json',st)
    return receipt
