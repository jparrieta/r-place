#!/usr/bin/env python3
"""Single-coordinator queue and durable logs for the 395 authorized pre-week briefs."""
import argparse
import collections
import csv
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

YARD=Path(__file__).resolve().parents[1]
QUEUE=YARD/'BRIEF-QUEUE.json'
LOG=YARD/'BRIEF-RUN-LOG.jsonl'
PATCH_FILES=('newbrief.py','read_brief.py','CONTRACT-brief-writer.v30.md')

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read():return json.loads(QUEUE.read_text())
def atomic(path,data):
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(data);temp.replace(path)
def log(event,**fields):
    with LOG.open('a') as fh:fh.write(json.dumps(dict(at=now(),event=event,**fields),ensure_ascii=False)+'\n')
def save(q):
    q['updated_utc']=now();atomic(QUEUE,json.dumps(q,indent=2,ensure_ascii=False)+'\n')
    rows=q['rooms'];counts=collections.Counter(r['status'] for r in rows)
    lines=['# Brief progress','',f'Updated: {q["updated_utc"]}', '', 'Scope: 395 never-coded communities. Dispatch order: ascending 97-hour item count.',
           'Model: gpt-5.6-sol. Deliverable: pre-week priors briefs.', '', '| Status | Rooms |','|---|---:|']
    lines += ['| %s | %d |'%(k,v) for k,v in sorted(counts.items())]
    lines += ['', '| Rank | Community | 97-hour items | Pre-week items | Status |','|---:|---|---:|---:|---|']
    lines += ['| %(rank)d | %(sub)s | %(items_in_window)d | %(preweek_items)d | %(status)s |'%r for r in rows]
    atomic(YARD/'BRIEF-PROGRESS.md','\n'.join(lines)+'\n')
    with (YARD/'BRIEF-QUEUE.tsv').open('w',newline='') as fh:
        keys=['rank','sub','items_in_window','preweek_items','work','status','agent_id','started_utc','finished_utc','attempts']
        w=csv.DictWriter(fh,fieldnames=keys,delimiter='\t',extrasaction='ignore');w.writeheader();w.writerows(rows)

def command(args,cwd):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPYCACHEPREFIX='/tmp/atlas-yard-pycache')
    r=subprocess.run([sys.executable]+list(map(str,args)),cwd=str(cwd),env=env,text=True,capture_output=True)
    return r

def getrow(q,rank):return next(r for r in q['rooms'] if r['rank']==rank)

def prepare(q,row):
    room=YARD/'rooms'/row['sub']
    if row['status'] not in ('queued','retry'):raise SystemExit('room already prepared: '+row['status'])
    # A retry preserves the complete failed attempt, without replacing successful work.
    if (room/'brief').exists():
        if row['status']!='retry':raise SystemExit('unexpected existing brief directory')
        target=room/('brief_failed_%02d'%row.get('attempts',1))
        if target.exists():raise SystemExit('failed attempt archive exists')
        (room/'brief').rename(target)
    for name in PATCH_FILES:
        target=room/'instrument'/name
        if target.exists():target.chmod(0o644)
        shutil.copy2(YARD/'_instrument/v30'/name,target)
        target.chmod(0o444)
    r=command([YARD/'_tools/room.py','brief','--model',q['model']],room)
    log('prepare',rank=row['rank'],sub=row['sub'],returncode=r.returncode,output=r.stdout+r.stderr)
    if r.returncode:
        row.update(status='build failed',error=(r.stdout+r.stderr)[-3000:]);save(q);raise SystemExit(r.stdout+r.stderr)
    row['attempts']=row.get('attempts',0)+1
    row['status']='prepared';row['prepared_utc']=now();save(q)
    return row

def start(q,row,agent):
    if row['status']!='prepared':raise SystemExit('not prepared')
    row.update(status='running',agent_id=agent,started_utc=now())
    log('agent started',rank=row['rank'],sub=row['sub'],agent_id=agent,model=q['model'],attempt=row['attempts'])
    save(q)

def recover(q,row,error):
    if row['status']!='running':raise SystemExit('writer is not running')
    row.update(status='retry',finished_utc=now(),error=error)
    log('agent interrupted',rank=row['rank'],sub=row['sub'],agent_id=row.get('agent_id'),output=error)
    save(q)
    return row

def finish(q,row,message,transcript=None):
    room=YARD/'rooms'/row['sub'];out=room/'brief/out'
    if row['work']=='writer':
        if row['status']!='running':raise SystemExit('writer not running')
        (out/'final_message.md').write_text(message.rstrip()+'\n')
        if not transcript:
            sessions=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'sessions'
            matches=list(sessions.glob('**/*'+row['agent_id']+'.jsonl'))
            if len(matches)==1:transcript=str(matches[0])
        if transcript:
            models=set()
            for line in Path(transcript).open():
                rec=json.loads(line)
                if rec.get('type')=='turn_context':models.add(rec.get('payload',{}).get('model'))
            if models and models!={q['model']}:raise SystemExit('Unexpected writer model in platform transcript: '+str(models))
            shutil.copy2(transcript,out/'_transcript.jsonl');provenance='full platform transcript'
        else:
            (out/'_transcript.jsonl').write_text(json.dumps({'type':'assistant','message':{'model':q['model'],'content':message},'agent_id':row['agent_id'],'transcript_scope':'final message only'},ensure_ascii=False)+'\n')
            provenance='final message only; full platform transcript not exposed to coordinator'
        row['transcript_scope']=provenance
    else:provenance='harness; no agent ran'
    r=command([YARD/'_tools/room.py','check','--brief'],room)
    (out/'validation.txt').write_text(r.stdout+r.stderr)
    row.update(status='verified' if r.returncode==0 else ('retry' if row.get('attempts',0)<2 else 'failed twice'),finished_utc=now())
    if r.returncode:row['error']=(r.stdout+r.stderr)[-5000:]
    else:row.pop('error',None)
    st=json.loads((room/'STATE.json').read_text())
    st.setdefault('agents',[]).append({'role':'brief writer' if row['work']=='writer' else 'brief harness','model':q['model'] if row['work']=='writer' else 'harness','agent_id':row.get('agent_id'),'started':row.get('started_utc',row['prepared_utc']),'ended':row['finished_utc'],'attempt':row['attempts'],'transcript':provenance})
    st.setdefault('notes',[]).append({'at':now(),'note':'Brief queue rank %d; %s; %s'%(row['rank'],row['status'],provenance)})
    atomic(room/'STATE.json',json.dumps(st,indent=1,ensure_ascii=False)+'\n')
    log('validation',rank=row['rank'],sub=row['sub'],status=row['status'],agent_id=row.get('agent_id'),output=r.stdout+r.stderr)
    save(q)
    status=command([YARD/'_tools/status.py','--yard',YARD,'--no-refresh'],YARD)
    if status.returncode:raise SystemExit(status.stdout+status.stderr)
    return {'rank':row['rank'],'sub':row['sub'],'status':row['status'],'validation':r.stdout+r.stderr}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('action',choices=['list','prepare','start','finish','recover','refresh']);ap.add_argument('--rank',type=int);ap.add_argument('--limit',type=int,default=4);ap.add_argument('--agent');ap.add_argument('--message-file');ap.add_argument('--message',default='');ap.add_argument('--error',default='writer interrupted');ap.add_argument('--transcript');a=ap.parse_args();q=read()
    if a.action=='list':
        print(json.dumps({'counts':dict(collections.Counter(r['status'] for r in q['rooms'])),'next':[r for r in q['rooms'] if r['status'] in ('queued','retry','prepared')][:a.limit]},indent=2));return
    if a.action=='refresh':save(q);return
    row=getrow(q,a.rank)
    if a.action=='prepare':result=prepare(q,row)
    elif a.action=='start':start(q,row,a.agent);result=row
    elif a.action=='recover':result=recover(q,row,a.error)
    else:result=finish(q,row,Path(a.message_file).read_text() if a.message_file else a.message,a.transcript)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
