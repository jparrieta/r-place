from pathlib import Path
from datetime import datetime,timezone
import ast,json,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'returns';CTRL=OUT/'_control'
p=CTRL/'runner.py';tree=ast.parse(p.read_text());tree.body=tree.body[:-1];ns={'__file__':str(p)};exec(compile(tree,str(p),'exec'),ns)
ns['verify_inputs']()
assert (OUT/'DONE').exists(),'controller is not done'
rows=[json.loads(x) for x in (OUT/'log.jsonl').read_text().splitlines() if x]
manifest=json.loads((ROOT/'MANIFEST.json').read_text());ids=[x['native_session_id'] for x in rows if x['native_session_id']]
assert len(ids)==len(set(ids)),'session reused'
accepted={};failed=[];retry_ids=[];item_lines=0
for row in rows:
 packet=row['packet'];rid=row['reader_id'];rep=row['replicate'];dest=OUT/packet
 assert row['model']=='gpt-6-astra' and row['effort']=='medium'
 assert 0<=row['reissue']<=2
 if row['reissue']:retry_ids.append(rid)
 raw=(dest/f'{rid}.raw.txt').read_bytes();assert hashlib.sha256(raw).hexdigest()==row['raw_sha256']
 source=(ROOT/'messages'/packet/f'oa{rep}.txt').read_bytes()
 if row['reissue']:
  old=f'Your reader id is oa{rep}; write it as `agent` on every line.'.encode();new=f'Your reader id is {rid}; write it as `agent` on every line.'.encode()
  assert source.count(old)==1;source=source.replace(old,new,1)
  assert (dest/f'{rid}.prompt.txt').read_bytes()==source
 assert hashlib.sha256(source).hexdigest()==row['prompt_sha256']
 events=[json.loads(x) for x in (dest/f'{rid}.events.jsonl').read_text().splitlines()]
 texts=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
 valid,reason,count=ns['validate'](raw,packet)
 if row['valid']:
  assert valid and texts and raw==texts[-1].encode()
  assert not row['tool_events'] and row['exit_code']==0
  assert (packet,rep) not in accepted
  accepted[(packet,rep)]=rid;item_lines+=count
 else:
  failure=(dest/f'{rid}.failed.txt').read_bytes();assert failure.split(b'\n',1)[1]==raw;failed.append({'packet':packet,'reader_id':rid,'reason':row['reason']})
assert len(retry_ids)==len(set(retry_ids)),'reissue id reused'
expected={(packet,rep) for packet in manifest for rep in [1,2]};missing=sorted(expected-set(accepted))
done=json.loads((OUT/'DONE').read_text());assert done['valid_returns']==len(accepted)
for field,target in [('input_tokens','total_input_tokens'),('cached_input_tokens','total_cached_input_tokens'),('output_tokens','total_output_tokens')]:assert done[target]==sum(row[field] or 0 for row in rows)
report={'checked_utc':datetime.now(timezone.utc).isoformat(),'audit_passed':True,'complete':not missing,'expected_readings':len(expected),'valid_readings':len(accepted),'attempts':len(rows),'fresh_native_sessions':len(ids),'failed_attempts':failed,'exhausted_replicates':[{'packet':p,'replicate':r} for p,r in missing],'counted_item_lines':item_lines,'expected_item_lines':2*sum(m['items'] for m in manifest.values()),'raw_replies_match_native_messages':True,'original_inputs_unchanged':True,'model':'gpt-6-astra','effort':'medium','token_totals':{k:v for k,v in done.items() if 'token' in k or k=='unknown_usage_attempts'}}
(CTRL/'final-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
