"""Verified API conversation bundles. No provider credentials or invented native state."""
import os, shutil, sys, tarfile, tempfile, uuid
from .common import *
from . import archive

def commit(base,state):
    ensure_space(); TMP.mkdir(parents=True,exist_ok=True)
    ck=identity(state['id']+'-'+uuid.uuid4().hex[:12]); dest=DATA/'checkpoints'/ck
    with tempfile.TemporaryDirectory(prefix='api-capture-',dir=TMP) as directory:
        tmp=Path(directory); payload=tmp/'payload'; payload.mkdir()
        before=inventory(base/'workspace'); ensure_space(sum(x['bytes'] for x in inventory(base).values())*3)
        copy_tree(base/'workspace',payload/'workspace')
        for name in ('thread.json','events.jsonl','messages.jsonl'):
            if (base/name).is_file(): shutil.copy2(base/name,payload/name)
        if (base/'turns').exists(): copy_tree(base/'turns',payload/'turns')
        write(payload/'state.json',{**state,'checkpoint':ck})
        copy_tree(CODEX/'runtime',payload/'support/runtime')
        write(payload/'support/environment.json',{'python':sys.version,'format':'rplace-openrouter-v1','dependencies':'Python standard library, OpenRouter access and fresh credentials. HTTP history replay; no hidden server state or process image.'})
        if inventory(base/'workspace')!=before or inventory(payload/'workspace')!=before: raise Error('Workspace changed during API capture')
        manifest={'format':'rplace-openrouter-v1','checkpoint':ck,'utc':now(),'files':inventory(payload),
                  'directories':[str(Path(d).relative_to(payload)) for d,_,_ in os.walk(payload) if Path(d)!=payload]}
        write(payload/'MANIFEST.json',manifest)
        packed=tmp/'agent.tar.gz'
        with tarfile.open(packed,'w:gz') as tar:
            for path in files(payload): tar.add(path,arcname=str(path.relative_to(payload)),recursive=False)
        archive.verify(packed,tmp/'extracted')
        receipt={'checkpoint':ck,'format':'rplace-openrouter-v1','backend':'openrouter','sha256':sha(packed),'bytes':packed.stat().st_size,
                 'actor':state['id'],'role':state['role'],'model':state['model'],'provider':state['binding']['provider'],
                 'parent':state.get('parent_checkpoint'),'boundary':state.get('boundary'),'utc':now()}
        dest.mkdir(parents=True); os.replace(packed,dest/'agent.tar.gz'); write(dest/'receipt.json',receipt); atomic(dest/'COMMITTED',receipt['sha256']+'\n')
    return receipt

def restore(checkpoint,actor):
    src=DATA/'checkpoints'/identity(checkpoint); dst=actor_dir(actor)
    with lock(DATA/'locks'/('restore-'+identity(actor)+'.lock')):
        if dst.exists(): raise Error('Actor destination already exists')
        if not (src/'COMMITTED').exists() or sha(src/'agent.tar.gz')!=(src/'COMMITTED').read_text().strip(): raise Error('API checkpoint is not committed or hash differs')
        m=archive.verify(src/'agent.tar.gz')
        if m.get('format')!='rplace-openrouter-v1': raise Error('Not an OpenRouter conversation bundle')
        ensure_space(sum(x['bytes'] for x in m['files'].values())*2); TMP.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='api-restore-',dir=TMP) as tmp:
            tmp=Path(tmp); archive.verify(src/'agent.tar.gz',tmp); state=read(tmp/'state.json')
            if state.get('backend')!='openrouter': raise Error('API archive backend mismatch')
            state.pop('evicted',None);state.pop('retention_ready',None);archive.detach_interview(state)
            state.update(id=actor,origin_role=state.get('origin_role',state['role']),role='interview',status='restored',active_turn_id=None,
                         thread_id=uuid.uuid4().hex,parent_checkpoint=checkpoint,checkpoint=None,run=None,restored_utc=now())
            write(tmp/'state.json',state); dst.parent.mkdir(parents=True,exist_ok=True); os.replace(tmp,dst)
    return state
