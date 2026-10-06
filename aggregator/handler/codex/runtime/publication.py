"""Publish analysis lineage with Git plumbing, never the shared checkout/index.

Checkpoint tags identify immutable common ancestors. Each analysis has its own
remote branch. Compressed/native histories and interviews remain private.
"""
import subprocess
import tempfile
from .common import *
from . import archive, branches, study


REGISTRY=DATA/'publication/checkpoints.json'

def git(*args, input=None, index=None, check=True):
    e={**os.environ,'GIT_TERMINAL_PROMPT':'0'}
    if index:e['GIT_INDEX_FILE']=str(index)
    result=subprocess.run(['git',*map(str,args)],cwd=REPO,env=e,input=input,capture_output=True,timeout=120)
    if check and result.returncode:raise Error('Git publication failed: '+result.stderr.decode(errors='replace').strip()[-1500:])
    return result.stdout


def remote_ref(ref):
    result=git('ls-remote','origin',ref).decode().strip()
    return result.split()[0] if result else None


def safe_files(root):
    blocked={'native','interviews','interview-workspaces','.git','.cc','.claude','auth.json','credentials.json','.env','OPENAI-LIVE.html'}
    for p in files(root):
        rel=p.relative_to(root)
        if any(x in blocked or x.startswith('.env.') for x in rel.parts):continue
        if rel.parts[0].startswith('.') or p.name.endswith(('.tar.gz','.zip','.sqlite','.sqlite-wal','.sqlite-shm')):continue
        if p.stat().st_size>95*1024**2:raise Error('File exceeds the Git publication limit: '+str(rel))
        yield rel,p


def commit_snapshot(parent, prefix, workspace, drops, metadata, title):
    with tempfile.TemporaryDirectory(prefix='git-analysis-',dir=TMP) as temp:
        index=Path(temp)/'index'
        git('read-tree',parent,index=index)
        old=git('ls-files','-z','--',prefix,index=index)
        if old:git('update-index','--force-remove','-z','--stdin',input=old,index=index)
        entries=[]
        for root,kind in ((workspace,'workspace'),(drops,'stage-deliveries')):
            if root is None:continue
            for rel,p in safe_files(root):
                blob=git('hash-object','-w','--',p).decode().strip()
                mode='100755' if p.stat().st_mode&0o111 else '100644'
                entries.append((mode,blob,prefix+'/'+kind+'/'+str(rel)))
        data=json.dumps(metadata,indent=2,ensure_ascii=False).encode()+b'\n'
        blob=git('hash-object','-w','--stdin',input=data).decode().strip()
        entries.append(('100644',blob,prefix+'/LINEAGE.json'))
        payload=b''.join((mode+' '+blob+'\t'+path).encode()+b'\0' for mode,blob,path in entries)
        git('update-index','-z','--index-info',input=payload,index=index)
        tree=git('write-tree',index=index).decode().strip()
        return git('commit-tree',tree,'-p',parent,input=(title+'\n').encode()).decode().strip()


def checkpoint_ref(checkpoint):return 'refs/tags/analysis-checkpoints/'+identity(checkpoint)


def save_ref(ref,commit):
    current=git('rev-parse','--verify',ref,check=False).decode().strip()
    if current and current!=commit:raise Error('Ref already points elsewhere: '+ref)
    if not current:git('update-ref',ref,commit,'0'*40)


def ensure_ancestor(run,checkpoint,registry):
    """Build missing verified checkpoint ancestry; reuse it for sibling forks."""
    if checkpoint in registry['checkpoints']:
        row=registry['checkpoints'][checkpoint]
        if sha(DATA/'checkpoints'/checkpoint/'agent.tar.gz')!=row['sha256']:raise Error('Published checkpoint changed')
        return row
    s=study.run_state(run);parent_branch=s.get('branch')
    rows=list(s['legs'].values());matches=[i for i,r in enumerate(rows) if r.get('checkpoint')==checkpoint]
    if len(matches)!=1:raise Error('Cannot identify publication ancestor')
    upto=matches[0]
    if parent_branch and checkpoint in {r.get('checkpoint') for r in study.run_state(parent_branch['source_run'])['legs'].values()}:
        return ensure_ancestor(parent_branch['source_run'],checkpoint,registry)
    if parent_branch:
        pub=read(study.run_dir(run)/'publication.json',{})
        if not pub.get('setup_commit'):raise Error('Publish the parent analysis branch before forking its results')
        parent=pub['setup_commit'];prefix=pub['prefix'];start=next(i for i,r in enumerate(rows) if r.get('checkpoint')==parent_branch['checkpoint'])+1
    else:
        parent=registry.get('anchor')
        if not parent:
            parent=remote_ref('refs/heads/main')
            if not parent:raise Error('Remote main is missing')
            git('fetch','--no-tags','origin',parent)
            registry['anchor']=parent
        prefix='aggregator/runs/'+run;start=0
    for row in rows[start:upto+1]:
        cp=identity(row['checkpoint'])
        if row['status'] not in ('verified','paused'):raise Error('Publication ancestor is unresolved')
        if cp in registry['checkpoints']:
            known=registry['checkpoints'][cp]
            if known['parent_commit']!=parent:raise Error('Checkpoint has conflicting Git ancestry')
            parent=known['commit'];continue
        source=DATA/'checkpoints'/cp;receipt=read(source/'receipt.json',{})
        if not (source/'COMMITTED').is_file() or sha(source/'agent.tar.gz')!=(source/'COMMITTED').read_text().strip():raise Error('Uncommitted publication checkpoint')
        manifest=archive.verify(source/'agent.tar.gz')
        ensure_space(sum(v['bytes'] for v in manifest['files'].values())*2)
        if receipt.get('sha256')!=sha(source/'agent.tar.gz'):raise Error('Publication receipt hash mismatch')
        with tempfile.TemporaryDirectory(prefix='publish-checkpoint-',dir=TMP) as temp:
            manifest=archive.verify(source/'agent.tar.gz',Path(temp)/'saved')
            if manifest.get('subject')!='aggregator' or manifest.get('boundary')!='completed':raise Error('Only completed aggregator analyses are published')
            info={'kind':row['status']+'-leg','run':run,'leg':row['leg'],'checkpoint':cp,
                  'sha256':receipt['sha256'],'runtime_archive_sha256':receipt['runtime_archive_sha256'],'parent_commit':parent,
                  'native_history':'Private checkpoint, not stored in Git'}
            commit=commit_snapshot(parent,prefix,Path(temp)/'saved/workspace',study.run_dir(run)/'drops' if parent_branch else None,info,'Analysis '+run+': '+row['status']+' '+row['leg'])
        save_ref(checkpoint_ref(cp),commit)
        registry['checkpoints'][cp]={**info,'commit':commit,'prefix':prefix}
        write(REGISTRY,registry)
        parent=commit
    return registry['checkpoints'][checkpoint]


def publish(run):
    """Explicit initial publication, then idempotent publication of verified legs."""
    run=identity(run);base=study.run_dir(run)
    with lock(DATA/'locks/publication.lock'), lock(DATA/'locks'/('run-'+run+'.lock')):
        s=study.run_state(run);b=s.get('branch')
        if not b:raise Error('Automatic Git publication is limited to analysis branches')
        if s.get('active_actor') or s.get('dispatch_active'):raise Error('Publish at an idle branch boundary')
        branches.seal(base,s,b['target_leg'])
        registry=read(REGISTRY,{'checkpoints':{}})
        pub=read(base/'publication.json',{})
        branch_ref='refs/heads/analysis/'+run
        remote=remote_ref(branch_ref)
        if remote and remote not in (pub.get('pushed_commit'),pub.get('pending_commit')):
            raise Error('Remote analysis branch changed independently; inspect before publishing')
        if not pub:
            ancestor=ensure_ancestor(b['source_run'],b['checkpoint'],registry)
            metadata={'kind':'analysis-setup','run':run,'source_run':b['source_run'],'after_leg':b['after_leg'],
                      'target_leg':b['target_leg'],'checkpoint':b['checkpoint'],'parent_commit':ancestor['commit'],
                      'checkpoint_sha256':b['checkpoint_sha256'],'changes':b['changes'],
                      'validation':'Inherited trusted validators; prior results certify original inputs only'}
            commit=commit_snapshot(ancestor['commit'],ancestor['prefix'],base/'baseline',base/'drops',metadata,'Analysis '+run+': setup before '+b['target_leg'])
            pub={'ref':branch_ref,'base_commit':ancestor['commit'],'setup_commit':commit,'prefix':ancestor['prefix'],
                 'pending_commit':commit,'pushed_commit':None,'checkpoint':b['checkpoint']}
            write(base/'publication.json',pub)
        rows=list(s['legs'].values());last=rows[-1]
        if last.get('checkpoint')!=b['checkpoint']:
            if last.get('status')!='verified':raise Error('Latest branch leg is not verified')
            row=ensure_ancestor(run,last['checkpoint'],registry)
            pub.update(pending_commit=row['commit'],checkpoint=last['checkpoint']);write(base/'publication.json',pub)
        commit=pub['pending_commit']
        local=git('rev-parse','--verify',branch_ref,check=False).decode().strip()
        if local and local not in (pub.get('pushed_commit'),commit):raise Error('Local analysis ref changed independently')
        git('update-ref',branch_ref,commit,local or '0'*40)
        # Push only the new analysis and its checkpoint ancestors, never main or
        # another analyst's branch. Atomic push prevents a partial remote lineage.
        refs=[]
        for cp,row in registry['checkpoints'].items():
            result=subprocess.run(['git','merge-base','--is-ancestor',row['commit'],commit],cwd=REPO,capture_output=True)
            if result.returncode==0:refs.append(checkpoint_ref(cp)+':'+checkpoint_ref(cp))
        git('push','--atomic','origin',commit+':'+branch_ref,*refs)
        if remote_ref(branch_ref)!=commit:raise Error('Remote publication receipt not confirmed; retry publish after inspection')
        pub.update(pushed_commit=commit,pushed_utc=now());write(base/'publication.json',pub)
        s=study.run_state(run);s['publication']={'ref':branch_ref,'commit':commit,'base_commit':pub['base_commit'],'checkpoint':pub['checkpoint'],'status':'pushed'}
        write(base/'state.json',s)
        return {'run':run,'publication':s['publication'],'new_turn_started':False}


def prepare(run):
    """Publish supplied changes, prepare the first leg, and leave it idle."""
    result=publish(run)
    s=study.run_state(run)
    opened=study.prepare(run,s['branch']['target_leg'])
    return {**result,**opened}


def after_close(run):
    s=study.run_state(run)
    if not s.get('branch') or not (study.run_dir(run)/'publication.json').exists():return None
    if list(s['legs'].values())[-1].get('status')!='verified':return None
    try:return publish(run)
    except Exception as error:
        with lock(DATA/'locks'/('run-'+run+'.lock')):
            s=study.run_state(run);s['publication']={**s.get('publication',{}),'status':'blocked','error':str(error)};write(study.run_dir(run)/'state.json',s)
        raise Error('Leg is verified and locally archived, but Git publication failed. Use publish-branch to retry; do not rerun analysis. '+str(error))
