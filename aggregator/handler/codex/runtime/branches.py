"""Analysis branches: verified ancestry, idle setup and pinned stage deliveries.

No model calls. Parent artifacts are read-only. Interviews use archive.restore instead.
"""
import base64
import copy
import hashlib
import re
import shutil
import tempfile
from pathlib import PurePosixPath
from .common import *
from . import archive, study, arms, backends

CHUNK = 512 * 1024


def create(source_run, checkpoint, run, leg):
    source_run, checkpoint, run = map(identity, (source_run, checkpoint, run))
    backends.require_run(source_run,'branch')
    backends.require({'backend':archive.checkpoint_backend(checkpoint)},'branch')
    if source_run == run: raise Error('A branch needs a new study name')
    src, dest = study.run_dir(source_run), study.run_dir(run)
    # The destination does not yet exist. One global creation lock avoids opposite
    # source/destination lock ordering; uploads and preparation use the run lock.
    with lock(DATA/'locks/branch-create.lock'), lock(DATA/'locks'/('run-'+source_run+'.lock')), lock(DATA/'locks'/('run-'+run+'.lock')):
        if dest.exists(): raise Error('Study already exists; choose a new branch name')
        parent = study.run_state(source_run)
        arms.frozen(src)
        if parent.get('branch'):
            verify_inputs(src, parent)
            if parent['branch']['status'] == 'draft': raise Error('Cannot branch an unfinished setup')
        ordered = list(parent['legs'].items())
        found = [i for i, (_, row) in enumerate(ordered) if row.get('checkpoint') == checkpoint]
        if len(found) != 1: raise Error('Choose a checkpoint recorded by this study')
        index = found[0]; previous_leg, previous = ordered[index]
        if previous.get('status') != 'verified': raise Error('Only verified completed legs can seed analysis branches')
        cp = DATA/'checkpoints'/checkpoint
        if not (cp/'COMMITTED').is_file() or sha(cp/'agent.tar.gz') != (cp/'COMMITTED').read_text().strip():
            raise Error('Parent checkpoint is not committed or has changed')
        manifest = archive.verify(cp/'agent.tar.gz')
        receipt = read(cp/'receipt.json', {})
        if manifest.get('format') != 'rplace-native-v1' or manifest.get('subject') != 'aggregator' or manifest.get('boundary') != 'completed':
            raise Error('Analysis branches require a completed native aggregator checkpoint')
        if receipt.get('sha256') != sha(cp/'agent.tar.gz') or sha(cp/'runtime.tar.gz') != receipt.get('runtime_archive_sha256'):
            raise Error('Parent archive receipt mismatch')
        archive.verify(cp/'runtime.tar.gz')
        inherited = dict(copy.deepcopy(ordered[:index+1]))
        later = {row['stage'] for _, row in ordered[index+1:]}
        stages = {row['stage'] for row in inherited.values()}
        finished = [s for s in parent.get('finished_stages', []) if s in stages and s not in later]
        state = {k:copy.deepcopy(parent[k]) for k in ('auto_dispatch','fleet_parallel','fleet_arm','version') if k in parent}
        state.update(id=run, created_utc=now(), source=source_run, active_actor=None,
                     legs=inherited, finished_stages=finished, continuity='native-checkpoint',
                     latest_workspace=str(dest/'baseline'))
        study.check_order(state, leg)
        if inventory(src/'trusted') != read(src/'trusted-hashes.json'):
            raise Error('Parent trusted validators changed')
        ensure_space(sum(v['bytes'] for v in manifest['files'].values())*2)
        with tempfile.TemporaryDirectory(prefix='analysis-branch-', dir=TMP) as tmp:
            payload = Path(tmp)/'saved'; archive.verify(cp/'agent.tar.gz', payload)
            saved = read(payload/'state.json', {})
            if saved.get('leg') != previous_leg or saved.get('id') != previous.get('actor'):
                raise Error('Checkpoint does not match the recorded leg')
            # A packets-out snapshot precedes its returns. Never borrow a later live
            # workspace, which could contain findings beyond the selected boundary.
            study.check_ready(run, study.descriptor(leg), payload/'workspace')
            dest.mkdir()
            try:
                copy_tree(payload/'workspace', dest/'baseline')
                for name in ('trusted','drops'): copy_tree(src/name, dest/name)
                for name in ('trusted-hashes.json','arm.json','fleet-arm.json'):
                    if (src/name).is_file(): shutil.copy2(src/name, dest/name)
                # Retain only sealed evidence up to this fork, never later-stage text.
                for old_leg, row in inherited.items():
                    for folder, pattern in (('_transcripts', old_leg+'.*'), ('_probe', row['stage']+'-'+old_leg+'.*')):
                        for p in (src/'sealed'/folder).glob(pattern):
                            q=dest/'sealed'/folder/p.name; q.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p,q)
                for name in ('notes.jsonl','receipts.jsonl'):
                    p=src/'sealed/_probe'/name
                    if p.is_file():
                        rows=[json.loads(line) for line in p.read_text().splitlines() if line.strip()]
                        atomic(dest/'sealed/_probe'/name, ''.join(json.dumps(r)+'\n' for r in rows if r.get('leg') in inherited))
                trans=dest/'sealed/_transcripts'
                atomic(trans/'INDEX.md', '# Inherited native transcripts\n\n'+''.join('- '+p.name+'\n' for p in sorted(trans.glob('*')) if p.name!='INDEX.md'))
                state['branch']={'status':'draft','source_run':source_run,'checkpoint':checkpoint,
                    'checkpoint_sha256':receipt['sha256'],'after_leg':previous_leg,'target_leg':leg,
                    'created_utc':now(),'changes':{},'baseline':inventory(dest/'baseline'),
                    'deliveries':inventory(dest/'drops'),'trusted':inventory(dest/'trusted')}
                write(dest/'state.json',state)
                write(dest/'BRANCH.json',state['branch'])
            except BaseException:
                write(dest/'BUILD-FAILED.json',{'utc':now(),'reason':'Branch setup interrupted; preserved for inspection'})
                raise
        return {'run':run,'branch':summary(state['branch']),'new_turn_started':False}


def verify_inputs(base, state):
    branch=state.get('branch')
    if not branch: return
    if (base/'BUILD-FAILED.json').exists(): raise Error('Branch creation failed; inspect preserved files')
    for name,key in (('drops','deliveries'),('trusted','trusted')):
        if inventory(base/name)!=branch[key]: raise Error('Branch '+name+' changed outside recorded setup')
    if branch['status']=='draft' and inventory(base/'baseline')!=branch['baseline']:
        raise Error('Branch data changed outside recorded setup')


def destination(base, state, path, stage=None):
    if not isinstance(path,str) or '\\' in path: raise Error('Use a relative POSIX path')
    p=PurePosixPath(path)
    if not path or p.is_absolute() or str(p)!=path or any(x in ('..','.') or x.startswith('.') for x in p.parts):
        raise Error('Unsafe branch file path')
    if stage:
        table=study.load_module(study.INSTRUMENT/'tools/steps.py','rplace_branch_steps').table()
        stages=list(dict.fromkeys(r['stage'] for r in table))
        if stage not in stages or stages.index(stage)<stages.index(study.descriptor(state['branch']['target_leg'])['stage']):
            raise Error('Stage delivery precedes the branch start')
        if p.parts[0]=='stages':
            names=[q.name for q in (base/'drops'/stage/'stages').glob('STAGE-'+stage+'-*.md')]
            if len(p.parts)!=2 or p.name not in names: raise Error('Replace the existing card filename for this stage')
        elif p.parts[0] not in ('package','trees','shelves','handling','attachments'):
            raise Error('Stage uploads accept its card or data folders, not tools or control files')
        root=base/'drops'/stage
    else:
        if p.parts[0] not in ('package','trees','shelves','handling','attachments','out') or len(p.parts)<2:
            raise Error('Workspace uploads must name a file in a data folder')
        if p.parts[0]=='out' and (p.parts[1].startswith('_') or p.parts[1] in ('PAUSE','diary','inbox','requests','responses')):
            raise Error('Cannot replace control files or the audit record')
        root=base/'baseline'
    if p.suffix.lower() in ('.py','.sh','.exe','.so','.dylib','.sqlite','.db') or p.name in archive.SECRET_NAMES:
        raise Error('Upload data or Markdown cards, not executables, native state or credentials')
    q=inside(root/path, root)
    for ancestor in (q,*q.parents):
        if ancestor==base: break
        if ancestor.is_symlink(): raise Error('Branch paths cannot contain links')
    return q, ('stage/'+stage+'/' if stage else 'workspace/')+path


def upload(run, path, content, offset, total, digest, stage=None):
    """Bounded chunks permit phone uploads without large HTTP requests or retries."""
    run=identity(run); base=study.run_dir(run)
    if type(offset)!=int or type(total)!=int or not 0<=offset<=total: raise Error('Invalid upload offsets')
    if not isinstance(digest,str) or not re.fullmatch('[0-9a-f]{64}',digest): raise Error('SHA-256 is required')
    try: chunk=base64.b64decode(content,validate=True)
    except (ValueError,TypeError): raise Error('Invalid base64 file content')
    if len(chunk)>CHUNK or offset+len(chunk)>total or (not chunk and total): raise Error('Invalid upload chunk')
    with lock(DATA/'locks'/('run-'+run+'.lock')):
        s=study.run_state(run)
        if s.get('branch',{}).get('status')!='draft': raise Error('Branch setup is sealed; create another branch to change inputs')
        verify_inputs(base,s)
        q,key=destination(base,s,path,stage)
        upload_id=hashlib.sha256(key.encode()).hexdigest()
        temp=base/'uploads'/upload_id
        meta=temp.with_suffix('.json')
        expected={'path':path,'stage':stage,'total':total,'sha256':digest}
        if offset==0:
            if temp.exists() or meta.exists(): raise Error('Upload already pending; inspect branch status, do not repeat it blindly')
            ensure_space(total*2); write(meta,expected); temp.touch()
        if read(meta)!=expected or not temp.exists() or temp.stat().st_size!=offset:
            raise Error('Upload offset or metadata differs; inspect pending upload')
        with temp.open('ab') as f: f.write(chunk);f.flush();os.fsync(f.fileno())
        next_offset=offset+len(chunk)
        if next_offset==total:
            if sha(temp)!=digest: raise Error('Uploaded file hash mismatch; pending file preserved')
            before=sha(q) if q.is_file() else None
            q.parent.mkdir(parents=True,exist_ok=True);os.replace(temp,q);q.chmod(0o644);meta.unlink()
            old=s['branch']['changes'].get(key,{})
            s['branch']['changes'][key]={'before_sha256':old.get('before_sha256',before),'sha256':digest,'bytes':total,'utc':now()}
            s['branch']['baseline']=inventory(base/'baseline');s['branch']['deliveries']=inventory(base/'drops')
            write(base/'state.json',s);write(base/'BRANCH.json',s['branch'])
            event(base/'branch-events.jsonl',kind='file',file=key,sha256=digest,bytes=total)
        return {'run':run,'path':key,'received':next_offset,'complete':next_offset==total,'new_turn_started':False}


def inspect(run):
    base=study.run_dir(identity(run));s=study.run_state(run)
    if not s.get('branch'): raise Error('Study is not an analysis branch')
    return {'run':run,'branch':summary(s['branch']),'pending_uploads':[
        {**read(p),'received':p.with_suffix('').stat().st_size if p.with_suffix('').exists() else 0}
        for p in sorted((base/'uploads').glob('*.json'))]}


def cancel_upload(run, path, stage=None):
    base=study.run_dir(identity(run))
    with lock(DATA/'locks'/('run-'+run+'.lock')):
        s=study.run_state(run)
        if s.get('branch',{}).get('status')!='draft':raise Error('Branch setup is sealed')
        _,key=destination(base,s,path,stage)
        upload_id=hashlib.sha256(key.encode()).hexdigest()
        temp=base/'uploads'/upload_id;meta=temp.with_suffix('.json')
        if not temp.exists() and not meta.exists():raise Error('No pending upload at this destination')
        preserved=base/'abandoned-uploads'/uuid.uuid4().hex;preserved.mkdir(parents=True)
        for p in (temp,meta):
            if p.exists():shutil.move(str(p),preserved/p.name)
        event(base/'branch-events.jsonl',kind='upload-cancelled',file=key,preserved=str(preserved))
        return {'run':run,'cancelled':key,'preserved':str(preserved),'new_turn_started':False}


def seal(base,s,leg):
    """Called under the study lock, before any actor is prepared. No turn starts."""
    verify_inputs(base,s)
    b=s.get('branch')
    if not b or b['status']!='draft': return
    if leg!=b['target_leg']: raise Error('First branch leg must be '+b['target_leg'])
    if any((base/'uploads').glob('*')): raise Error('Branch has a pending upload; complete it before preparation')
    b.update(status='sealed',sealed_utc=now())
    write(base/'BRANCH.json',b);write(base/'state.json',s)


def notice(state):
    b=state.get('branch')
    if not b:return ''
    changes=', '.join(sorted(b['changes'])) or 'No file overrides'
    return ('This is analysis branch '+state['id']+' from '+b['source_run']+' after '+b['after_leg']+
            '. The supplied files supersede remembered versions. Read the current stage card and data. '+
            'Recorded changes: '+changes+'. Earlier validation belongs to the original inputs; '+
            'do not claim those checks certify changed data. Keep the inherited trusted checks. ')


def summary(branch):
    return {k:v for k,v in branch.items() if k not in ('baseline','deliveries','trusted')}
