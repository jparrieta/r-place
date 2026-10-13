from pathlib import Path
from datetime import datetime,timezone
import json,os,statistics
out=Path(__file__).resolve().parents[1]
p=out/'log.jsonl';rows=[]
for line in p.read_text().splitlines() if p.exists() else []:
 try:rows.append(json.loads(line))
 except json.JSONDecodeError:pass
live=[]
for p in out.glob('S05-*/*.state.json'):
 try:d=json.loads(p.read_text())
 except (FileNotFoundError,json.JSONDecodeError):continue
 if d['state']=='running':
  try:os.kill(d['pid'],0);alive=True
  except ProcessLookupError:alive=False
  live.append({'packet':d['packet'],'reader_id':d['reader_id'],'alive':alive,'elapsed_s':round((datetime.now(timezone.utc)-datetime.fromisoformat(d['start_utc'])).total_seconds())})
valid={(d['packet'],d['replicate']) for d in rows if d['valid']}
result={'checked_utc':datetime.now(timezone.utc).isoformat(),'valid':len(valid),'expected':96,'attempts':len(rows),'failed':sum(not d['valid'] for d in rows),'reissues':sum(d['reissue']>0 for d in rows),'live':len(live),'oldest_live_s':max((x['elapsed_s'] for x in live),default=0),'dead_marked_running':[x for x in live if not x['alive']],'median_seconds':round(statistics.median(d['seconds'] for d in rows),1) if rows else None,'input_tokens':sum(d['input_tokens'] or 0 for d in rows),'output_tokens':sum(d['output_tokens'] or 0 for d in rows),'unknown_usage':sum(d['input_tokens'] is None or d['output_tokens'] is None for d in rows),'done_exists':(out/'DONE').exists()}
print(json.dumps(result))
