from pathlib import Path
import json,hashlib,re,fcntl
runner=Path('/Users/arrieta/Jail/Orchestrator/B4b-arm/returns/_control/runner.py')
ns={'__file__':str(runner),'__name__':'reissue_import'}
source=runner.read_text(); assert source.endswith('main()\n')
exec(compile(source[:-len('main()\n')],str(runner),'exec'),ns)
root=ns['ROOT']; out=ns['OUT']; dest=out/'S05-27'
lease=(ns['CTRL']/'runner.lock').open('a'); fcntl.flock(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
ns['verify_inputs']()
old_hash=hashlib.sha256((dest/'oa1.raw.txt').read_bytes()).hexdigest()
base_validate=ns['validate']
def validate(raw,packet):
 valid,reason,count=base_validate(raw,packet)
 if not valid:return valid,reason,count
 spec=ns['MANIFEST'][packet]
 for number,line in enumerate(raw.decode().splitlines(),1):
  if not line.strip() or line=='END-OF-RETURN':continue
  row=json.loads(line); codes=set(re.findall(r'\bC\d{7}\b',line))
  if codes:
   key=row.get('theme_id'); allowed=set(spec['codes_by_item'].get(key,[]))
   foreign=sorted(codes-allowed)
   if foreign:return False,f'line {number}: foreign concept codes for {key}: {foreign}',count
  for theme,concepts in row.get('also_present',{}).items():
   if not isinstance(concepts,list) or len(set(concepts))<3:return False,f'line {number}: also_present {theme} has fewer than three concepts',count
 return True,None,count
ns['validate']=validate
results=[]
for rid,reissue in [('oa3',1),('oa4',2)]:
 result=ns['attempt']('S05-27',1,reissue,rid); results.append(result)
 assert hashlib.sha256((dest/'oa1.raw.txt').read_bytes()).hexdigest()==old_hash
 if result['valid'] or 'foreign concept codes' not in str(result['reason']):break
summary=json.loads((out/'DONE').read_text())
prior=out/'_control/DONE-before-S05-27-reissue.json'; assert not prior.exists(); prior.write_bytes((out/'DONE').read_bytes())
rows=ns['existing'](); summary.update(end_utc=ns['utc'](),attempts=len(rows))
for key in ['input_tokens','cached_input_tokens','output_tokens']:
 summary['total_'+key]=sum(r.get(key) or 0 for r in rows)
summary['total_tokens']=summary['total_input_tokens']+summary['total_output_tokens']
summary['unknown_usage_attempts']=sum(r.get('input_tokens') is None or r.get('output_tokens') is None for r in rows)
passed=next((r for r in results if r['valid']),None)
summary['reissues']={'S05-27/replicate1':{'original_reader':'oa1','original_raw_sha256':old_hash,'original_invalid_reason':'foreign C0436497 cited for T2-85354','attempts':[r['reader_id'] for r in results],'accepted_reader':passed['reader_id'] if passed else None,'validation':'format/count, per-item concept membership, also_present minimum three concepts'}}
if not passed:
 summary.update(state='complete_with_exhausted',valid_returns=95,exhausted_replicates=[{'packet':'S05-27','replicate':1}],exhausted_packets=['S05-27'])
ns['write_json'](out/'DONE',summary)
ns['write_json'](dest/'REISSUE-VALIDATION.json',{'original_unchanged':True,'original_raw_sha256':old_hash,'results':results,'accepted_reader':passed['reader_id'] if passed else None})
print(json.dumps(summary),flush=True)
