"""Self-contained archives. Verify every regular member before commit or restore."""
import gzip, json, os, shutil, stat, tarfile, tempfile, uuid, sys, platform
from pathlib import Path, PurePosixPath
from .common import Error, DATA, REPO, CODEX, TMP, now, inside, identity, read, write, atomic, sha, files, inventory, copy_tree, ensure_space, lock

SECRET_NAMES={'auth.json','credentials.json','.env','server.stderr.log'}

def relocate_native_index(home, destination, thread_id, original_workspace, workspace):
    """Rebase copied index metadata only; paginated transcript byte offsets stay intact."""
    import sqlite3
    from contextlib import closing
    home=Path(home); destination=Path(destination); rollouts={}; changes=[]; indexed=False
    for folder in ('sessions','archived_sessions'):
        for p in (home/folder).rglob('*.jsonl'):
            with p.open() as stream: first=stream.readline()
            try: meta=json.loads(first).get('payload',{})
            except ValueError: continue
            tid=meta.get('id')
            if not tid: continue
            if tid in rollouts: raise Error('Duplicate native thread in archive: '+tid)
            rollouts[tid]=str(destination/p.relative_to(home))
    if thread_id not in rollouts: raise Error('Native thread file missing from archive')
    for db in home.glob('state_*.sqlite'):
        with closing(sqlite3.connect(db)) as conn, conn:
            tables={r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if 'threads' not in tables: continue
            columns={r[1] for r in conn.execute('PRAGMA table_info(threads)')}
            if not {'id','rollout_path','cwd'}<=columns: raise Error('Unsupported native thread index schema')
            for tid,old_path,cwd in conn.execute('SELECT id,rollout_path,cwd FROM threads').fetchall():
                if tid not in rollouts: raise Error('Native index references a thread absent from the archive: '+tid)
                new_cwd=cwd
                try: new_cwd=str(Path(workspace)/Path(cwd).relative_to(original_workspace))
                except ValueError: pass
                conn.execute('UPDATE threads SET rollout_path=?,cwd=? WHERE id=?',(rollouts[tid],new_cwd,tid))
                changes.append({'database':db.name,'thread_id':tid,'from':old_path,'to':rollouts[tid]})
                if tid==thread_id: indexed=True
        # Closing the copied database safely flushes its own WAL, never the parent.
    return {'indexed':indexed,'resume_path':rollouts[thread_id],'changes':changes}

def native_files(home):
    home=inside(home)
    for d,dirs,names in os.walk(home,followlinks=False):
        dirs[:]=sorted(n for n in dirs if n not in ('tmp','shell_snapshots','logs','cache','__pycache__'))
        for n in dirs:
            if (Path(d)/n).is_symlink(): raise Error('Native store contains unexpected directory link')
        for name in sorted(names):
            p=Path(d)/name
            if name in SECRET_NAMES or p.suffix in ('.sock','.lock','.pyc'): continue
            if p.is_symlink() or not p.is_file(): raise Error('Native store contains unexpected special file')
            yield p


def verify(path, extract=None):
    path=inside(path); expected={}; seen=set()
    with tarfile.open(path,'r:gz') as tf:
        members=tf.getmembers()
        for m in members:
            n=PurePosixPath(m.name)
            if n.is_absolute() or '..' in n.parts or m.name in seen or not m.isfile(): raise Error('Unsafe or duplicate archive member: '+m.name)
            seen.add(m.name)
        if 'MANIFEST.json' not in seen: raise Error('Archive has no manifest')
        manifest=json.load(tf.extractfile('MANIFEST.json'))
        expected=manifest.get('files',{})
        if set(expected)!=seen-{'MANIFEST.json'}: raise Error('Archive inventory does not match manifest')
        import hashlib
        for m in members:
            if m.name=='MANIFEST.json': continue
            h=hashlib.sha256(); size=0
            stream=tf.extractfile(m)
            for b in iter(lambda:stream.read(1024*1024),b''): h.update(b); size+=len(b)
            meta=expected[m.name]
            if h.hexdigest()!=meta['sha256'] or size!=meta['bytes'] or stat.S_IMODE(m.mode)!=meta['mode']: raise Error('Archive hash/size/mode mismatch: '+m.name)
        for directory in manifest.get('directories',[]):
            d=PurePosixPath(directory)
            if d.is_absolute() or '..' in d.parts: raise Error('Unsafe directory in manifest')
        if extract:
            dest=inside(extract)
            if dest.exists() and any(dest.iterdir()): raise Error('Restore destination must be empty')
            dest.mkdir(parents=True,exist_ok=True)
            for directory in manifest.get('directories',[]): inside(dest/directory,dest).mkdir(parents=True,exist_ok=True)
            # Write only verified files, never tarfile.extract and never links/devices.
            for m in members:
                q=inside(dest/m.name,dest); q.parent.mkdir(parents=True,exist_ok=True)
                with q.open('xb') as f: shutil.copyfileobj(tf.extractfile(m),f)
                q.chmod(stat.S_IMODE(m.mode))
    return manifest

def commit(actor, state):
    ensure_space(); base=inside(actor); TMP.mkdir(parents=True,exist_ok=True)
    ck=identity(state['id']+'-'+uuid.uuid4().hex[:12]); target=DATA/'checkpoints'/ck
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='capture-',dir=TMP) as tmp:
        tmp=Path(tmp); payload=tmp/'payload'; payload.mkdir()
        before=inventory(base/'workspace')
        ensure_space(sum(x['bytes'] for x in before.values())*3)
        copy_tree(base/'workspace',payload/'workspace')
        if inventory(base/'workspace')!=before or inventory(payload/'workspace')!=before: raise Error('Workspace changed during capture')
        for p in native_files(base/'native'):
            q=payload/'native'/p.relative_to(base/'native'); q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,q)
        if (base/'mailbox').exists():copy_tree(base/'mailbox',payload/'mailbox')
        for name in ('state.json','thread.json','events.jsonl','messages.jsonl','continuation.json','native-relocation.json'):
            if (base/name).exists(): shutil.copy2(base/name,payload/name)
        write(payload/'state.json',{**state,'checkpoint':ck})
        # Future branch cards have not yet been delivered to this actor, but must
        # travel with its private checkpoint rather than depend on coordinator memory.
        if state.get('role')=='aggregator' and state.get('run'):
            study_base=DATA/'runs'/identity(state['run'])
            study_state=read(study_base/'state.json',{})
            if study_state.get('branch'):
                from .branches import verify_inputs
                verify_inputs(study_base,study_state)
                for folder in ('drops','trusted'):copy_tree(study_base/folder,payload/'study'/folder)
                for name in ('BRANCH.json','trusted-hashes.json','arm.json','fleet-arm.json','publication.json'):
                    if (study_base/name).is_file():shutil.copy2(study_base/name,payload/'study'/name)
                write(payload/'study/state.json',study_state)
        # Runtime code and executable travel with the bundle. Authentication never does.
        copy_tree(CODEX/'runtime',payload/'support/runtime')
        write(payload/'support/environment.json',{'python':sys.version,'python_executable':sys.executable,'platform':platform.platform(),'runtime_dependencies':'Python standard library; Codex binary included; platform libraries and authentication external','instrument_dependencies':'Copied workspace tools retain their own source and dependency manifests'})
        exe=Path(state['runtime']['executable'])
        if sha(exe)!=state['runtime']['sha256']: raise Error('Pinned Codex executable changed')
        runtime_hash=state['runtime']['sha256']
        import hashlib
        package=state['runtime'].get('package_root'); bundle=state['runtime'].get('app_bundle')
        object_key=hashlib.sha256(json.dumps(state['runtime'].get('package_files',state['runtime'].get('bundle_files',{'codex':runtime_hash})),sort_keys=True).encode()).hexdigest()
        runtime_object=DATA/'objects'/(object_key+'.tar.gz')
        runtime_entrypoint=('codex-package/'+state['runtime']['package_executable'] if package else
                            'CodexCLI.app/'+state['runtime']['bundle_executable'] if bundle else 'bin/codex')
        runtime_object.parent.mkdir(parents=True,exist_ok=True)
        with lock(DATA/'locks'/('runtime-'+object_key+'.lock'),wait=True):
            if not runtime_object.exists():
                rt=tmp/'runtime'; rt.mkdir()
                ensure_space((sum(p.stat().st_size for p in Path(package).rglob('*') if p.is_file()) if package else exe.stat().st_size)*2)
                if package:
                    current={str(p.relative_to(package)):sha(p) for p in Path(package).rglob('*') if p.is_file()}
                    if current!=state['runtime']['package_files']: raise Error('Pinned runtime package changed')
                    shutil.copytree(package,rt/'codex-package')
                    copied={str(p.relative_to(rt/'codex-package')):sha(p) for p in (rt/'codex-package').rglob('*') if p.is_file()}
                    if copied!=current: raise Error('Pinned runtime package changed during capture')
                elif bundle:
                    current={str(p.relative_to(bundle)):sha(p) for p in Path(bundle).rglob('*') if p.is_file()}
                    if current!=state['runtime']['bundle_files']: raise Error('Pinned app bundle changed')
                    shutil.copytree(bundle,rt/'CodexCLI.app')
                else:
                    (rt/'bin').mkdir(); shutil.copy2(exe,rt/'bin/codex')
                write(rt/'MANIFEST.json',{'format':'rplace-runtime-v1','files':inventory(rt)})
                part=runtime_object.with_suffix('.tmp-'+uuid.uuid4().hex)
                with tarfile.open(part,'w:gz',compresslevel=6) as tar:
                    for p in files(rt): tar.add(p,arcname=str(p.relative_to(rt)),recursive=False)
                verify(part); os.replace(part,runtime_object)
            verify(runtime_object)
        manifest={'format':'rplace-native-v1','checkpoint':ck,'subject':state['role'],'handler_conversation_included':state.get('origin_role',state['role'])=='handler','utc':now(),'parent':state.get('parent_checkpoint'),'thread_id':state.get('thread_id'),'last_turn_id':state.get('last_turn_id'),'boundary':state.get('boundary'),'runtime':state['runtime'],'original_workspace':str(base/'workspace'),'original_native':str(base/'native'),'files':inventory(payload),'directories':[str(Path(d).relative_to(payload)) for d,_,_ in os.walk(payload) if Path(d)!=payload]}
        write(payload/'MANIFEST.json',manifest)
        archive=tmp/'agent.tar.gz'
        with tarfile.open(archive,'w:gz',compresslevel=6) as tf:
            for p in files(payload): tf.add(p,arcname=str(p.relative_to(payload)),recursive=False)
        verify(archive)
        target.mkdir()
        os.replace(archive,target/'agent.tar.gz')
        os.link(runtime_object,target/'runtime.tar.gz')
        receipt={'checkpoint':ck,'sha256':sha(target/'agent.tar.gz'),'bytes':(target/'agent.tar.gz').stat().st_size,'runtime_archive_sha256':sha(target/'runtime.tar.gz'),'runtime_sha256':runtime_hash,'runtime_entrypoint':runtime_entrypoint,'actor':state['id'],'role':state['role'],'parent':state.get('parent_checkpoint'),'boundary':state.get('boundary'),'utc':now()}
        write(target/'receipt.json',receipt)
        atomic(target/'COMMITTED',receipt['sha256']+'\n')
    return receipt

def detach_interview(state):
    """Keep provenance without inheriting membership of a live study or fleet."""
    for field in ('run','study_run','dispatch_id'):
        value=state.pop(field,None)
        if value:state.setdefault('origin_'+field,value)

def checkpoint_backend(checkpoint):
    """Inspect the envelope before choosing an archive parser."""
    from . import backends
    src=DATA/'checkpoints'/identity(checkpoint)
    receipt=read(src/'receipt.json',{})
    backend=backends.name(receipt)
    if receipt.get('format')=='rplace-claude-v1' and backend!='claude':raise Error('Claude receipt is missing its backend tag')
    if (src/'backend.json').exists() and backend!='claude':raise Error('Checkpoint backend envelope disagrees with receipt')
    return backend

def verify_checkpoint(checkpoint):
    src=DATA/'checkpoints'/identity(checkpoint)
    if checkpoint_backend(checkpoint)=='claude':
        from .claude_backend import verify as verify_claude
        return verify_claude(checkpoint)
    receipt=read(src/'receipt.json',{})
    if not (src/'COMMITTED').is_file() or sha(src/'agent.tar.gz')!=(src/'COMMITTED').read_text().strip():
        raise Error('Checkpoint is not committed or has changed')
    if receipt.get('sha256')!=sha(src/'agent.tar.gz'):raise Error('Checkpoint receipt/hash mismatch')
    return verify(src/'agent.tar.gz')

def restore(checkpoint,actor,mode='interview'):
    checkpoint=identity(checkpoint); actor=identity(actor); src=DATA/'checkpoints'/checkpoint; dst=DATA/'actors'/actor
    if checkpoint_backend(checkpoint)=='claude':
        from .claude_backend import restore as restore_claude
        return restore_claude(checkpoint,actor,mode)
    if mode not in ('interview','continuation'):raise Error('Unknown restore mode')
    if (src/'agent.tar.gz').is_file() and verify(src/'agent.tar.gz').get('format')=='rplace-openrouter-v1':
        from .portable import restore as restore_api
        return restore_api(checkpoint,actor)
    with lock(DATA/'locks'/('restore-'+actor+'.lock')):
        if dst.exists(): raise Error('Actor destination already exists')
        if not (src/'COMMITTED').is_file(): raise Error('Checkpoint is not committed')
        if sha(src/'agent.tar.gz')!=(src/'COMMITTED').read_text().strip(): raise Error('Archive SHA-256 mismatch')
        TMP.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='restore-',dir=TMP) as tmp:
            tmp=Path(tmp); m=verify(src/'agent.tar.gz')
            ensure_space(sum(x['bytes'] for x in m['files'].values())*2)
            verify(src/'agent.tar.gz',tmp)
            receipt=read(src/'receipt.json')
            if sha(src/'runtime.tar.gz')!=receipt.get('runtime_archive_sha256'): raise Error('Runtime archive hash mismatch')
            runtime_root=tmp/'support/pinned-runtime'
            verify(src/'runtime.tar.gz',runtime_root)
            entry=receipt.get('runtime_entrypoint','bin/codex')
            exe=inside(runtime_root/entry,runtime_root)
            if sha(exe)!=receipt.get('runtime_sha256'): raise Error('Runtime executable hash mismatch')
            exe.chmod(0o755)
            state=read(tmp/'state.json')
            if state['runtime']['platform']!=os.uname().sysname or state['runtime']['machine']!=os.uname().machine: raise Error('Archive requires the recorded operating system and architecture')
            state.pop('evicted',None);state.pop('retention_ready',None);detach_interview(state)
            state.update(id=actor,origin_role=state.get('origin_role',state['role']),role='interview',parent_checkpoint=checkpoint,status='restored',active_turn_id=None,run=None,checkpoint=None,restored_utc=now(),original_workspace=m['original_workspace'],fork_pending=True)
            state['runtime']['executable']=str(dst/'support/pinned-runtime'/entry)
            if state['runtime'].get('package_root'): state['runtime']['package_root']=str(dst/'support/pinned-runtime/codex-package')
            if state['runtime'].get('app_bundle'): state['runtime']['app_bundle']=str(dst/'support/pinned-runtime/CodexCLI.app')
            relocation=relocate_native_index(tmp/'native',dst/'native',state['thread_id'],m['original_workspace'],dst/'workspace')
            state['resume_path']=None if relocation['indexed'] else relocation['resume_path']
            write(tmp/'native-relocation.json',{'utc':now(),**relocation})
            write(tmp/'state.json',state)
            dst.parent.mkdir(parents=True,exist_ok=True)
            os.replace(tmp,dst)
            # TemporaryDirectory tolerates an already moved root.
    return state
