"""Evict redundant completed stores only after verifying their committed checkpoint.

Checkpoint folders and registered lead histories are never removed. Small actor
records remain visible; opening one instructs the operator to restore its archive.
"""
import shutil
from .common import *
from . import archive, backends


def ready(actor):
    state=actor_state(actor)
    if backends.name(state)=='claude':return {'retained':True,'reason':'Claude shared run and native store are not eligible for controller eviction'}
    state['retention_ready']=True;write(actor_dir(actor)/'state.json',state)


def protected(base,state):
    if backends.name(state)=='claude':return 'Claude shared run and native store retained'
    if state.get('active_turn_id') or state.get('boundary')!='completed':return 'unfinished native boundary'
    if state.get('role') not in ('aggregator','probe','reader','labeler'):return 'role retained'
    if state.get('status')!='saved' or not state.get('retention_ready'):return 'not released for retention'
    for path in (DATA/'runs').glob('*/state.json'):
        run=read(path,{})
        if run.get('active_actor')==state['id']:return 'current study actor'
        ws=run.get('latest_workspace')
        if ws and Path(ws).resolve().is_relative_to(base.resolve()):return 'latest study workspace'
        for key in ('dispatch_active','dispatch_blocked'):
            did=run.get(key)
            if did and (state.get('dispatch_id')==did or state['id'].startswith(did+'-')):return 'unresolved dispatch'
    return None


def verified(state):
    backends.require(state,'retention')
    ck=identity(state['checkpoint']);src=DATA/'checkpoints'/ck
    receipt=read(src/'receipt.json',{})
    if not (src/'COMMITTED').is_file():raise Error('Checkpoint has no commit marker')
    digest=(src/'COMMITTED').read_text().strip()
    if sha(src/'agent.tar.gz')!=digest or receipt.get('sha256')!=digest:raise Error('Checkpoint receipt/hash mismatch')
    manifest=archive.verify(src/'agent.tar.gz')
    if receipt.get('boundary')!='completed':raise Error('Only completed checkpoints may replace stores')
    if manifest.get('format')=='rplace-native-v1':
        if sha(src/'runtime.tar.gz')!=receipt.get('runtime_archive_sha256'):raise Error('Runtime archive hash mismatch')
        archive.verify(src/'runtime.tar.gz')
        if (manifest.get('thread_id'),manifest.get('last_turn_id'))!=(state.get('thread_id'),state.get('last_turn_id')):raise Error('Checkpoint boundary differs from actor')
    else:
        import tarfile,json
        with tarfile.open(src/'agent.tar.gz') as tar: saved=json.load(tar.extractfile('state.json'))
        if (saved.get('thread_id'),saved.get('last_turn_id'))!=(state.get('thread_id'),state.get('last_turn_id')):raise Error('API checkpoint boundary differs from actor')
    return receipt,manifest


def evict(actor):
    base=actor_dir(actor)
    if backends.name(actor_state(actor))=='claude':
        return {'actor':actor,'evicted':False,'reason':'Claude shared run and native store retained'}
    with lock(base/'owner.lock'):
        state=actor_state(actor)
        if state.get('evicted'):return {'actor':actor,'evicted':False,'reason':'already archived'}
        reason=protected(base,state)
        if reason:return {'actor':actor,'evicted':False,'reason':reason}
        from .native import process_identity
        for name in ('native-process.json','http-process.json'):
            proc=read(base/name,{})
            if proc.get('identity') and process_identity(proc['pid'])==proc['identity']:raise Error('Actor process remains alive')
        receipt,manifest=verified(state);expected=manifest['files']
        actual={'workspace/'+n:v for n,v in inventory(base/'workspace').items()}
        if (base/'native').exists():
            actual.update({str(p.relative_to(base)):{'sha256':sha(p),'bytes':p.stat().st_size,'mode':p.stat().st_mode & 0o7777} for p in archive.native_files(base/'native')})
        prefixes=('workspace/','native/')
        if actual!={n:v for n,v in expected.items() if n.startswith(prefixes)}:raise Error('Live files differ from committed checkpoint; store retained')
        for name in ('thread.json','events.jsonl','messages.jsonl'):
            if (base/name).exists() and sha(base/name)!=expected.get(name,{}).get('sha256'):raise Error('Unarchived conversation evidence; store retained')
        state.update(evicted=True,status='archived',evicted_utc=now(),retained_checkpoint=receipt['checkpoint'])
        write(base/'state.json',state)
        reclaimed=0
        for name in ('workspace','native','support','scratch'):
            path=base/name
            if path.exists():
                reclaimed+=sum(p.stat().st_size for p in files(path));shutil.rmtree(path)
        return {'actor':actor,'evicted':True,'checkpoint':receipt['checkpoint'],'logical_bytes_released':reclaimed}


def sweep():
    results=[]
    with lock(DATA/'locks/retention.lock'):
        for path in (DATA/'actors').glob('*/state.json'):
            state=read(path,{})
            if not state.get('retention_ready') or state.get('evicted'):continue
            try:results.append(evict(state['id']))
            except (Error,OSError,ValueError) as e:results.append({'actor':state.get('id'),'evicted':False,'reason':str(e)})
    return {'actors':results,'logical_bytes_released':sum(r.get('logical_bytes_released',0) for r in results)}
