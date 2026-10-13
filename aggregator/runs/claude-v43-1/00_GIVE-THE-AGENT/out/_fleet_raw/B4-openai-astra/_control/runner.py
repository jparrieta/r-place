from pathlib import Path
from datetime import datetime,timezone
import os,sys,json,hashlib,subprocess,threading,time,concurrent.futures,fcntl,traceback
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'returns'; CTRL=OUT/'_control'
MODEL='gpt-6-astra';EFFORT='medium';EXPECTED='9cef838aa631759e409996be1f57960559f036665794701756f96ead60cd0f97'
MANIFEST=json.loads((ROOT/'MANIFEST.json').read_text())
ARGS=json.loads((CTRL/'reader-config-args.json').read_text())
PROFILE='(version 1) (allow default) (deny file-read-data (literal "/Users/arrieta/.codex/AGENTS.md") (literal "/Users/arrieta/.codex/AGENTS.override.md") (subpath "/Users/arrieta/.codex/memories"))'
LOCK=threading.Lock()
def utc(): return datetime.now(timezone.utc).isoformat()
def write_json(path,data):
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(data,indent=2)+'\n');os.replace(temp,path)
def verify_inputs():
    assert hashlib.sha256((ROOT/'SHA256SUMS').read_bytes()).hexdigest()==EXPECTED
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,rel=line.split(maxsplit=1);p=ROOT/rel.lstrip('*')
        assert p.resolve().is_relative_to(ROOT.resolve()) and not p.is_symlink()
        assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,str(p)
    assert json.loads((CTRL/'isolation-PASS.json').read_text())['passed']
def validate(raw,packet):
    try: text=raw.decode('utf-8')
    except UnicodeDecodeError:return False,'reply is not UTF-8',None
    lines=text.splitlines()
    while lines and not lines[-1].strip():lines.pop()
    if not lines or lines[-1]!='END-OF-RETURN':return False,'missing final END-OF-RETURN line',None
    rows=[]
    for num,line in enumerate(lines[:-1],1):
        if not line.strip():continue
        try: obj=json.loads(line,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
        except (json.JSONDecodeError,ValueError):return False,f'line {num} is not JSON',None
        if not isinstance(obj,dict):return False,f'line {num} is not an object',None
        rows.append(obj)
    spec=MANIFEST[packet]
    count=sum(spec['count_key'] in row and not any(k in row for k in spec['count_exclude']) and ('pass' not in row or (row['pass']==1 and not isinstance(row['pass'],bool))) for row in rows)
    if count!=spec['items']:return False,f'item count {count}, expected {spec["items"]}',count
    return True,None,count

def logrow(row):
    with LOCK:
        with (OUT/'log.jsonl').open('a') as f:f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
def existing():
    with LOCK:
        p=OUT/'log.jsonl';return [json.loads(x) for x in p.read_text().splitlines() if x] if p.exists() else []
def allocate_retry():
    with LOCK:
        p=CTRL/'next-reader-id.json';n=json.loads(p.read_text()) if p.exists() else 3
        write_json(p,n+1);return f'oa{n}'
def attempt(packet,replicate,reissue,rid):
    source=ROOT/'messages'/packet/f'oa{replicate}.txt';prompt=source.read_bytes()
    if reissue:
        old=f'Your reader id is oa{replicate}; write it as `agent` on every line.'.encode()
        new=f'Your reader id is {rid}; write it as `agent` on every line.'.encode()
        assert prompt.count(old)==1
        prompt=prompt.replace(old,new,1)
    dest=OUT/packet;dest.mkdir(exist_ok=True)
    work=CTRL/'workspaces'/f'{packet}-{rid}';work.mkdir(parents=True,exist_ok=False)
    raw_path=dest/f'{rid}.raw.txt';events_path=dest/f'{rid}.events.jsonl';err_path=dest/f'{rid}.stderr.txt'
    assert not any(p.exists() for p in [raw_path,events_path,err_path])
    (dest/f'{rid}.stdin.sha256').write_text(hashlib.sha256(prompt).hexdigest()+'\n')
    if reissue:(dest/f'{rid}.prompt.txt').write_bytes(prompt)
    command=['/usr/bin/sandbox-exec','-p',PROFILE,'codex','exec','--ephemeral','--ignore-user-config','--ignore-rules','--skip-git-repo-check','--json','--color','never','-o',str(raw_path),*ARGS,'-']
    env={k:v for k,v in os.environ.items() if not k.startswith(('CODEX_','OPENAI_','ANTHROPIC_','MCP_'))}
    start=utc();t0=time.monotonic();sid=None;usage=None;turn_failed=False;tool_event=False;errors=[]
    meta={'packet':packet,'reader_id':rid,'replicate':replicate,'reissue':reissue,'model':MODEL,'effort':EFFORT,'start_utc':start,'prompt_sha256':hashlib.sha256(prompt).hexdigest(),'state':'starting'}
    write_json(dest/f'{rid}.state.json',meta)
    with events_path.open('xb') as ev,err_path.open('xb') as er:
        p=subprocess.Popen(command,cwd=work,env=env,stdin=subprocess.PIPE,stdout=ev,stderr=er,start_new_session=True)
        meta.update(pid=p.pid,state='running');write_json(dest/f'{rid}.state.json',meta)
        print(json.dumps({'event':'started',**meta}),flush=True)
        p.communicate(prompt);code=p.returncode
    for line in events_path.read_text().splitlines():
        try: event=json.loads(line)
        except json.JSONDecodeError:continue
        if event.get('type')=='thread.started':sid=event.get('thread_id')
        if event.get('type')=='turn.completed':usage=event.get('usage')
        if event.get('type')=='turn.failed':turn_failed=True;errors.append(event.get('error'))
        if event.get('type')=='error':errors.append(event.get('message',event))
        item=event.get('item',{})
        if item.get('type') in ['command_execution','file_change','mcp_tool_call','web_search','tool_call']:tool_event=True
    raw=raw_path.read_bytes() if raw_path.exists() else b''
    if not raw_path.exists():raw_path.write_bytes(b'')
    valid,reason,count=validate(raw,packet)
    if code!=0 or turn_failed:valid=False;reason=f'native exec exit={code}, turn_failed={turn_failed}; '+str(reason or errors)[0:1500]
    if tool_event:valid=False;reason='isolation failure: unexpected tool event'
    if not valid:
        with (dest/f'{rid}.failed.txt').open('xb') as f:f.write((str(reason).replace('\n',' ')+'\n').encode()+raw)
    result={**meta,'state':'valid' if valid else 'failed','end_utc':utc(),'seconds':round(time.monotonic()-t0,3),'native_session_id':sid,'input_tokens':usage.get('input_tokens') if usage else None,'cached_input_tokens':usage.get('cached_input_tokens') if usage else None,'output_tokens':usage.get('output_tokens') if usage else None,'reasoning_output_tokens':usage.get('reasoning_output_tokens') if usage else None,'valid':valid,'item_lines':count,'reason':reason,'exit_code':code,'raw_sha256':hashlib.sha256(raw).hexdigest(),'tool_events':tool_event,'errors':errors}
    logrow(result);write_json(dest/f'{rid}.state.json',result)
    print(json.dumps({'event':'ended',**result}),flush=True)
    if tool_event: raise RuntimeError(reason)
    return result

def reading(packet,replicate):
    rows=[x for x in existing() if x['packet']==packet and x['replicate']==replicate]
    if any(x['valid'] for x in rows):return next(x for x in rows if x['valid'])
    for reissue in range(len(rows),3):
        rid=f'oa{replicate}' if reissue==0 else allocate_retry()
        result=attempt(packet,replicate,reissue,rid)
        if result['valid']:return result
    return result if 'result' in locals() else rows[-1]

def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'first-pair'
    concurrency=int(sys.argv[2]) if len(sys.argv)>2 else 2
    lease=(CTRL/'runner.lock').open('a');fcntl.flock(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
    verify_inputs()
    jobs=[(p,r) for p in sorted(MANIFEST) for r in [1,2]]
    if mode=='first-pair':jobs=jobs[:2]
    write_json(CTRL/'controller-state.json',{'pid':os.getpid(),'start_utc':utc(),'mode':mode,'concurrency':concurrency,'state':'running'})
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures=[pool.submit(reading,*job) for job in jobs]
        for f in concurrent.futures.as_completed(futures):f.result()
    verify_inputs()
    rows=existing();valid={(r['packet'],r['replicate']) for r in rows if r['valid']}
    summary={'state':'complete' if len(valid)==96 else 'first_pair_complete' if mode=='first-pair' else 'complete_with_exhausted','end_utc':utc(),'valid_returns':len(valid),'total_expected':96,'attempts':len(rows),'exhausted_replicates':[{'packet':p,'replicate':r} for p,r in jobs if (p,r) not in valid],'total_input_tokens':sum(x['input_tokens'] or 0 for x in rows),'total_cached_input_tokens':sum(x['cached_input_tokens'] or 0 for x in rows),'total_output_tokens':sum(x['output_tokens'] or 0 for x in rows),'unknown_usage_attempts':sum(x['input_tokens'] is None or x['output_tokens'] is None for x in rows),'sha256sums_sha256':EXPECTED}
    summary['total_tokens']=summary['total_input_tokens']+summary['total_output_tokens']
    summary['exhausted_packets']=sorted(set(x['packet'] for x in summary['exhausted_replicates']))
    write_json(CTRL/'controller-state.json',summary)
    if mode=='all':
        with (OUT/'DONE').open('x') as f:f.write(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)
main()
