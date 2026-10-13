from pathlib import Path
import json,hashlib,re,fcntl,os,shutil,subprocess
runner=Path(__file__).with_name('runner.py')
ns={'__file__':str(runner),'__name__':'reissue_import'}
source=runner.read_text(); assert source.endswith('main()\n')
exec(compile(source[:-len('main()\n')],str(runner),'exec'),ns)
root=ns['ROOT']; out=ns['OUT']; ctrl=ns['CTRL']; dest=out/'S05-27'
lease=(ctrl/'runner.lock').open('a'); fcntl.flock(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
ns['verify_inputs']()
proof=json.loads((ctrl/'isolation-PASS.json').read_text())
assert hashlib.sha256(Path(shutil.which('codex')).read_bytes()).hexdigest()==proof['cli_sha256']
assert ns['MODEL']=='gpt-6-astra' and ns['EFFORT']=='medium'
args=ns['ARGS']; assert 'model="gpt-6-astra"' in args and 'model_reasoning_effort="medium"' in args
original=json.loads((ctrl/'model-catalog.original.json').read_text())['models'][0]
edited=json.loads((ctrl/'model-catalog.no-tools.json').read_text())['models'][0]
changes={k:{'before':original.get(k),'after':edited.get(k)} for k in original if original[k]!=edited[k]}
assert changes==proof['model_catalog_changes']
old_hash=hashlib.sha256((dest/'oa1.raw.txt').read_bytes()).hexdigest()
prior_log=ns['existing']()
assert len(prior_log)==96 and not any(r['reader_id'] in ('oa3','oa4') for r in prior_log)
assert next(r['raw_sha256'] for r in prior_log if r['packet']=='S05-27' and r['replicate']==1)==old_hash
base_validate=ns['validate']
def inspect_codes(raw,packet):
    rows=[]
    for number,line in enumerate(raw.decode().splitlines(),1):
        if line.strip() and line!='END-OF-RETURN':rows.append((number,json.loads(line),line))
    by_position={r['position']:r.get('theme_id') for _,r,_ in rows if 'position' in r and not any(k in r for k in ['primary','revises','predicted_confusion'])}
    issues=[]; floor=[]; cited=0
    for number,row,line in rows:
        codes=set(re.findall(r'\bC[0-9]{7}\b',line)); cited+=len(codes)
        key=row.get('theme_id') or by_position.get(row.get('revises',row.get('position')))
        foreign=sorted(codes-set(ns['MANIFEST'][packet]['codes_by_item'].get(key,[])))
        if foreign:issues.append({'line':number,'theme_id':key,'foreign_codes':foreign})
        for theme,concepts in row.get('also_present',{}).items():
            if not isinstance(concepts,list) or len(set(concepts))<3:floor.append({'line':number,'theme':theme})
    return {'foreign_concept_lines':issues,'also_present_floor_failures':floor,'concept_citations_checked':cited}
def validate(raw,packet):
    valid,reason,count=base_validate(raw,packet)
    if not valid:return valid,reason,count
    report=inspect_codes(raw,packet)
    if report['foreign_concept_lines']:return False,'foreign concept codes: '+json.dumps(report['foreign_concept_lines']),count
    if report['also_present_floor_failures']:return False,'also_present minimum three concepts: '+json.dumps(report['also_present_floor_failures']),count
    return True,None,count
ns['validate']=validate
old_check=inspect_codes((dest/'oa1.raw.txt').read_bytes(),'S05-27')
assert any(x['line']==5 and 'C0436497' in x['foreign_codes'] for x in old_check['foreign_concept_lines'])
state=json.loads((dest/'oa3.state.json').read_text()); assert state['state']=='running'
try:os.kill(state['pid'],0)
except ProcessLookupError:pass
else:raise RuntimeError('oa3 PID remains live: refuse retry')
events=[json.loads(x) for x in (dest/'oa3.events.jsonl').read_text().splitlines() if x]
assert not any(e['type'] in ('turn.completed','turn.failed') or (e.get('item',{}).get('type')=='agent_message') for e in events)
assert not (dest/'oa3.raw.txt').exists()
preserve=dest/'interrupted-oa3-20261013T1650Z';preserve.mkdir()
for p in sorted(dest.glob('oa3.*')):p.rename(preserve/p.name)
(ctrl/'workspaces/S05-27-oa3').rename(preserve/'empty-workspace')
for name in ['DONE','SHA256SUMS']:
    (preserve/(name+'.before-reissue')).write_bytes((out/name).read_bytes())
interrupted={**state,'state':'interrupted','valid':False,'end_utc':None,'observed_dead_utc':ns['utc'](),'native_session_id':next(e['thread_id'] for e in events if e['type']=='thread.started'),'input_tokens':None,'cached_input_tokens':None,'output_tokens':None,'reasoning_output_tokens':None,'exit_code':None,'reason':'Process disappeared before any reply or completion event; cause unknown. Evidence preserved; one bounded fresh-process retry of the same oa3 reissue.','transport_attempt':1,'evidence_directory':str(preserve.relative_to(out)),'raw_sha256':None,'tool_events':False}
ns['logrow'](interrupted);ns['write_json'](preserve/'INTERRUPTION.json',interrupted)
ns['write_json'](ctrl/'reissue-isolation-check.json',{'checked_utc':ns['utc'](),'passed':True,'prior_native_request_proof':'isolation-PASS.json','cli_sha256':proof['cli_sha256'],'config_sha256':hashlib.sha256((ctrl/'reader-config-args.json').read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256((ctrl/'model-catalog.no-tools.json').read_bytes()).hexdigest(),'same_model_effort_tools_context_and_seatbelt_profile':True,'original_raw_sha256':old_hash})
ns['write_json'](ctrl/'reissue-controller-state.json',{'pid':os.getpid(),'state':'running','start_utc':ns['utc'](),'scope':'S05-27 replicate 1 only'})
print(json.dumps({'event':'preflight_passed','old_validation':old_check,'interrupted_attempt_preserved':str(preserve)}),flush=True)
results=[]
for rid,reissue in [('oa3',1),('oa4',2)]:
    result=ns['attempt']('S05-27',1,reissue,rid);results.append(result)
    assert hashlib.sha256((dest/'oa1.raw.txt').read_bytes()).hexdigest()==old_hash
    if result['valid'] or 'foreign concept codes' not in str(result['reason']):break
ns['verify_inputs']()
passed=next((r for r in results if r['valid']),None)
rows=ns['existing']();summary=json.loads((preserve/'DONE.before-reissue').read_text())
summary.update(end_utc=ns['utc'](),attempts=len(rows),completed_reading_attempts=sum(r.get('exit_code')==0 for r in rows))
for key in ['input_tokens','cached_input_tokens','output_tokens']:summary['total_'+key]=sum(r.get(key) or 0 for r in rows)
summary['total_tokens']=summary['total_input_tokens']+summary['total_output_tokens']
summary['unknown_usage_attempts']=sum(r.get('input_tokens') is None or r.get('output_tokens') is None for r in rows)
summary['token_totals_scope']='Known visible usage only; incomplete oa3 transport attempt has unknown usage.'
summary['reissues']={'S05-27/replicate1':{'original_reader':'oa1','original_raw_sha256':old_hash,'original_validation':old_check,'attempts':[r['reader_id'] for r in results],'incomplete_transport_attempts':1,'accepted_reader':passed['reader_id'] if passed else None,'validation':'format/count, every cited concept in its item MANIFEST codes_by_item, also_present minimum three concepts'}}
if not passed:summary.update(state='complete_with_exhausted',valid_returns=95,exhausted_replicates=[{'packet':'S05-27','replicate':1}],exhausted_packets=['S05-27'])
ns['write_json'](out/'DONE',summary)
ns['write_json'](dest/'REISSUE-VALIDATION.json',{'checked_utc':ns['utc'](),'original_unchanged':True,'original_raw_sha256':old_hash,'original_validation':old_check,'results':results,'membership_checks':{r['reader_id']:inspect_codes((dest/(r['reader_id']+'.raw.txt')).read_bytes(),'S05-27') for r in results if base_validate((dest/(r['reader_id']+'.raw.txt')).read_bytes(),'S05-27')[0]},'accepted_reader':passed['reader_id'] if passed else None})
ns['write_json'](ctrl/'reissue-controller-state.json',{'state':summary['state'],'end_utc':ns['utc'](),'results':[r['reader_id'] for r in results],'accepted_reader':passed['reader_id'] if passed else None})
print(json.dumps(summary),flush=True)
