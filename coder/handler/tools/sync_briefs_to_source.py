#!/usr/bin/env python3
"""Copy reviewed brief corrections and verified queue outputs to the original Atlas Yard.
Fixed source/destination; preserves originals and refuses conflicting existing briefs.
"""
import datetime
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

STAGE=Path('/Users/arrieta/Documents/ChatGPT/place Yard/atlas_yard')
SOURCE=Path('/Users/arrieta/Documents/Codex/rplace/atlas_yard')
BACKUP=SOURCE/'_brief_revision_backups'/'v30-brief-r1'
STAMP=STAGE/'_changes/source-sync.json'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def writable_copy(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists():dst.chmod(0o644)
    shutil.copy2(src,dst)
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--preserve-source-file',action='append',default=[])
    args=parser.parse_args()
    preserved=set(args.preserve_source_file)
    if not STAGE.is_dir() or not SOURCE.is_dir():raise SystemExit('expected yards missing')
    queue=json.loads((STAGE/'BRIEF-QUEUE.json').read_text())
    assert len(queue['rooms'])==395 and all(r['items_in_window']<=queue['rooms'][min(i+1,394)]['items_in_window'] for i,r in enumerate(queue['rooms']))
    changes=json.loads((STAGE/'_changes/manifest.json').read_text())
    previous=json.loads(STAMP.read_text()) if STAMP.exists() else {'files':{},'rooms':{}}
    # Check every overwrite before any write, including edits since an earlier synchronization.
    for row in changes['files']:
        name=row['file'];dest=SOURCE/name
        if name in preserved:continue
        allowed={row['before_sha256'],row['after_sha256'],previous['files'].get(name)}
        if dest.exists() and digest(dest) not in allowed:
            raise SystemExit('source file changed outside this batch; not overwriting '+str(dest))
    new_tools=['_tools/brief_queue.py','_tools/check_brief_milestone.py','_tools/test_brief_reader.py','_tools/test_brief_validation.py','_tools/sync_briefs_to_source.py']
    for name in new_tools:
        dest=SOURCE/name
        if dest.exists() and digest(dest) not in {previous['files'].get(name),digest(STAGE/name)}:
            raise SystemExit('source helper changed outside this batch: '+name)
    eligible=[]
    for row in queue['rooms']:
        if row['status']!='verified':continue
        sub=row['sub'];stage_room=STAGE/'rooms'/sub;src_room=SOURCE/'rooms'/sub
        state=json.loads((src_room/'STATE.json').read_text())
        if state.get('prior_runs'):raise SystemExit('earlier runs appeared for '+sub)
        md=stage_room/'brief/out/brief.md';sha=digest(md)
        if previous['rooms'].get(sub)==sha:
            if not (src_room/'brief/out/brief.md').exists():raise SystemExit('previously copied brief disappeared: '+sub)
            if digest(src_room/'brief/out/brief.md')!=sha:raise SystemExit('source brief changed since copy: '+sub)
            continue
        if (src_room/'brief').exists():
            if sub not in previous['rooms'] or digest(src_room/'brief/out/brief.md')!=previous['rooms'][sub]:
                raise SystemExit('source brief conflict; not overwriting '+sub)
        eligible.append((row,sha))
    BACKUP.mkdir(parents=True,exist_ok=True)
    for row in changes['files']:
        name=row['file'];dest=SOURCE/name;backup=BACKUP/name
        if name in preserved:continue
        if dest.exists() and not backup.exists():writable_copy(dest,backup)
        writable_copy(STAGE/name,dest);previous['files'][name]=digest(dest)
    for name in new_tools:
        dest=SOURCE/name
        writable_copy(STAGE/name,dest);previous['files'][name]=digest(dest)
    for row,sha in eligible:
        sub=row['sub'];stage_room=STAGE/'rooms'/sub;src_room=SOURCE/'rooms'/sub
        before=json.loads((src_room/'STATE.json').read_text())
        backup=BACKUP/'rooms'/sub
        backup.mkdir(parents=True,exist_ok=True)
        writable_copy(src_room/'STATE.json',backup/'STATE.json')
        for name in ('newbrief.py','read_brief.py','CONTRACT-brief-writer.v30.md'):
            old=src_room/'instrument'/name
            if not (backup/'instrument'/name).exists():writable_copy(old,backup/'instrument'/name)
            writable_copy(stage_room/'instrument'/name,old);old.chmod(0o444)
        if (src_room/'brief').exists():
            archive=backup/('prior_brief_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
            (src_room/'brief').rename(archive)
        shutil.copytree(stage_room/'brief',src_room/'brief')
        bdir=src_room/'brief'
        # Relocate only harness paths. Keep the original platform transcript unchanged.
        c=bdir/'CONTRACT.md'
        if c.exists():
            c.chmod(0o644);c.write_text(c.read_text().replace(str(stage_room/'brief'),str(bdir)))
        evidence=bdir/'out/evidence.json'
        if evidence.exists():
            data=json.loads(evidence.read_text());data['coverage']['corpus']=str(bdir/'brief_corpus.txt');evidence.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
        mp=bdir/'_manifest.json';man=json.loads(mp.read_text())
        man['execution_directory']=str(stage_room/'brief')
        man['relocated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        for name in man.get('sha256',{}):man['sha256'][name]=digest(bdir/name)
        mp.write_text(json.dumps(man,indent=1,ensure_ascii=False)+'\n')
        stage_state=json.loads((stage_room/'STATE.json').read_text())
        before['agents']=stage_state.get('agents',[])
        before.setdefault('notes',[]).append({'at':man['relocated_utc'],'note':'Brief written in '+str(stage_room/'brief')+'; full transcript retained; paths relocated and source-side validation rerun. Queue rank '+str(row['rank'])})
        (src_room/'STATE.json').write_text(json.dumps(before,indent=1,ensure_ascii=False)+'\n')
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPYCACHEPREFIX='/tmp/atlas-yard-pycache')
        result=subprocess.run([sys.executable,str(SOURCE/'_tools/room.py'),'check','--brief'],cwd=str(src_room),env=env,text=True,capture_output=True)
        (bdir/'out/validation-after-relocation.txt').write_text(result.stdout+result.stderr)
        if result.returncode:raise SystemExit('relocated brief validation failed: '+sub+'\n'+result.stdout+result.stderr)
        previous['rooms'][sub]=sha
        STAMP.write_text(json.dumps(previous,indent=2)+'\n')
    for name in ('FIRST-10-BRIEFS.md','CHANGE-LOG.md','POSSIBILITIES-LOG.md','BRIEF-PROGRESS.md','BRIEF-RUN-LOG.jsonl','BRIEF-QUEUE.tsv','BRIEF-QUEUE.json','BRIEF-WRITER-PROMPT.md','ONLINE-HANDOVER.md'):
        if (STAGE/name).exists():writable_copy(STAGE/name,SOURCE/name)
    shutil.copytree(STAGE/'_changes',SOURCE/'_brief_revision_log',dirs_exist_ok=True)
    previous['at']=datetime.datetime.now(datetime.timezone.utc).isoformat();STAMP.write_text(json.dumps(previous,indent=2)+'\n')
    result=subprocess.run([sys.executable,str(SOURCE/'_tools/status.py'),'--yard',str(SOURCE),'--no-refresh'],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),text=True,capture_output=True)
    if result.returncode:raise SystemExit(result.stdout+result.stderr)
    print(json.dumps({'tools_installed':len(previous['files']),'briefs_added_this_sync':len(eligible),'briefs_copied_total':len(previous['rooms']),'source':str(SOURCE)},indent=2))
if __name__=='__main__':main()
