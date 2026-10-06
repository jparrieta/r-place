"""Offline release checks, with all temporary files kept inside the workspace (the folder that holds rplace)."""
import csv,subprocess,sys,tempfile
from .common import *

def verify():
    checks=[]; reports=DATA/'test-reports'; reports.mkdir(parents=True,exist_ok=True)
    for label,args in [
        ('runtime',[sys.executable,'-B','-m','unittest','discover','-s',str(CODEX/'runtime/tests'),'-v']),
        ('scientific',['bash',str(REPO/'aggregator/instrument/tools/tests/run.sh')])]:
        r=subprocess.run(args,cwd=ROOT,env={**env(),'PYTHONPATH':str(CODEX)},capture_output=True,text=True)
        atomic(reports/(label+'.log'),r.stdout+r.stderr); checks.append({'check':label,'passed':r.returncode==0,'log':str(reports/(label+'.log'))})
    bad=[]
    for base in ('aggregator/handler/codex/runtime','data','aggregator','coder/handler/tools'):
        for p in (REPO/base).rglob('*.py'):
            if any(n in p.parts for n in ('run','runs','input','archive','__pycache__','_work','rooms','_versions')): continue
            try: compile(p.read_text(),str(p),'exec')
            except Exception as e: bad.append(str(p)+': '+str(e))
    checks.append({'check':'script syntax','passed':not bad,'errors':bad})
    run=REPO/'aggregator/runs/claude-v43-1'; coders=REPO/'aggregator/input/coders'
    with (coders/'ROOMS.tsv').open() as f: rooms={r['sub'] for r in csv.DictReader(f,delimiter='\t')}
    needed=['brief.md','case.md','codes.jsonl','themes.jsonl','threads.jsonl','pointers.jsonl','window.json','forest/forest.jsonl','forest/tree_index.json']
    missing=[sub+'/'+name for sub in rooms for name in needed if not (coders/'rooms'/sub/name).is_file()]
    with (run/'00_GIVE-THE-AGENT/package/store/rooms.jsonl').open() as f: store={__import__('json').loads(line)['sub'] for line in f if line.strip()}
    checks.append({'check':'prepared corpus','passed':not missing and rooms==store,'rooms':len(rooms),'missing':missing,'frame_difference':sorted(rooms^store)})
    result={'utc':now(),'passed':all(c['passed'] for c in checks),'checks':checks,'live_model_acceptance':'separate: run.py acceptance --live'}
    write(reports/'offline.json',result); print(__import__('json').dumps(result,indent=2)); return 0 if result['passed'] else 1
