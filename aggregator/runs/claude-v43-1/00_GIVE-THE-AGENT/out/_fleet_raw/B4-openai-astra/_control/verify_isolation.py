from pathlib import Path
import json,hashlib,datetime,subprocess,shutil
out=Path(__file__).resolve().parent
d=json.loads((out/'isolation-request.json').read_text())
assert d['model']=='gpt-6-astra' and d['reasoning']['effort']=='medium'
assert not d.get('tools')
assert all(not item.get('tools') for item in d['input'] if item.get('type')=='additional_tools')
messages=[x for x in d['input'] if x.get('type')=='message'];users=[x for x in messages if x['role']=='user']
assert len(users)==1 and users[0]['content']==[{'type':'input_text','text':'ISOLATION_PREFLIGHT_ONLY'}]
assert len(messages)==2 and messages[0]['role']=='developer'
base=''.join(c.get('text','') for c in messages[0]['content'])
original=json.loads((out/'model-catalog.original.json').read_text())['models'][0]
edited=json.loads((out/'model-catalog.no-tools.json').read_text())['models'][0]
changed={k:{'before':original.get(k),'after':edited.get(k)} for k in original if original[k]!=edited[k]}
assert set(changed)=={'apply_patch_tool_type','experimental_supported_tools','tool_mode','supports_search_tool'}
report={'passed':True,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'test':'native exec outgoing request captured by localhost mock, no inference','model':d['model'],'effort':d['reasoning']['effort'],'offered_tools':0,'input_messages':len(messages),'user_prompt_exact':True,'memory_or_environment_context':False,'builtin_developer_prompt_sha256':hashlib.sha256(base.encode()).hexdigest(),'model_catalog_changes':changed,'cli_version':subprocess.check_output(['codex','--version'],text=True).strip(),'cli_sha256':hashlib.sha256(Path(shutil.which('codex')).read_bytes()).hexdigest(),'limits':'The CLI host reads its runtime and existing authentication. Readers have no file/web/execution/retrieval tools. The unchanged built-in Codex developer instruction is retained. macOS Seatbelt blocks global AGENTS and memory reads.'}
(out/'isolation-PASS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
