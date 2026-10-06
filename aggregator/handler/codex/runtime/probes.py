"""Recall in a native fork. Tool access denied and any attempted tool use rejected."""
import shutil, tempfile, uuid
from pathlib import Path
from .common import *
from . import archive, actors, study, retention

def read_note(row):
    import json
    data=json.loads(row); data.pop('utc',None); return data

def run_probe(run,actor,checkpoint):
    leg=actor.state['leg']; stage=leg[:2]; base=study.run_dir(run); sealed=base/'sealed/_probe'; sealed.mkdir(parents=True,exist_ok=True)
    aid='probe-'+uuid.uuid4().hex[:16]; state=archive.restore(checkpoint,aid); state.update(role='probe',read_only=True,run=None); write(actor_dir(aid)/'state.json',state)
    probe=actors.Actor(aid)
    with tempfile.TemporaryDirectory(prefix='probe-score-',dir=TMP) as tmp:
        tmp=Path(tmp); copy_tree(actor.base/'workspace/out',tmp/'out')
        r=study.trusted(run,'probe.py',[stage,'--leg',leg,'--root',str(tmp),'--out',str(tmp/'out'),'--ask'],tmp)
        if r.returncode: raise Error('Probe question generation failed')
        q=tmp/'out/_probe'/f'{stage}-{leg}.questions.md'
        try:
            probe.message(q.read_text()); probe.wait()
            if probe.state.get('boundary')!='completed': raise Error('Probe did not complete')
            thread=probe.server.call('thread/read',{'threadId':probe.state['thread_id'],'includeTurns':True})['thread']
            turn=next(x for x in thread['turns'] if x['id']==probe.state['last_turn_id'])
            if any(x.get('type') not in ('userMessage','agentMessage','reasoning','contextCompaction') for x in turn.get('items',[])): raise Error('Probe attempted a tool call; no recall score accepted')
            atomic(q.with_name(q.name.replace('.questions.md','.answers.md')),probe.final())
            r=study.trusted(run,'probe.py',[stage,'--leg',leg,'--root',str(tmp),'--out',str(tmp/'out'),'--score'],tmp)
            if r.returncode: raise Error('Probe scoring failed')
            receipt=probe.checkpoint()
            for p in (tmp/'out/_probe').glob(f'{stage}-{leg}*'): shutil.copy2(p,sealed/p.name)
            notes=tmp/'out/_probe/notes.jsonl'
            if notes.exists():
                for row in notes.read_text().splitlines():
                    if row.strip(): event(sealed/'notes.jsonl',**read_note(row))
            event(sealed/'receipts.jsonl',leg=leg,checkpoint=receipt['checkpoint'],result=r.stdout)
            retention.ready(aid)
            return receipt
        finally: probe.release()
