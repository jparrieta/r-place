import os,json,subprocess,threading,time,hashlib
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'returns'/'_control'
PROBE=OUT/'preflight'
features=['memories','shell_tool','unified_exec','multi_agent','multi_agent_v2','apps','plugins','hooks','browser_use','browser_use_external','computer_use','in_app_browser','image_generation','view_image','goals','sleep_tool','skill_search','shell_snapshot','workspace_dependencies','code_mode','code_mode_host','tool_suggest']
settings={'model':'gpt-6-astra','model_reasoning_effort':'medium','project_doc_max_bytes':0,'web_search':'disabled','agents.enabled':False,'skills.bundled.enabled':False,'skills.include_instructions':False,'memories.use_memories':False,'memories.generate_memories':False,'include_environment_context':False,'include_apps_instructions':False,'include_permissions_instructions':False,'include_collaboration_mode_instructions':False,'tools.update_plan.enabled':False,'tools.experimental_request_user_input.enabled':False,'orchestrator.mcp.enabled':False,'history.persistence':'none','approval_policy':'never','check_for_update_on_startup':False}
for flag in features: settings['features.'+flag]=False
settings['features.skip_host_skill_discovery']=True
settings['model_catalog_json']=str(OUT/'model-catalog.no-tools.json')
args=[]
for k,v in settings.items():args += ['-c',k+'='+json.dumps(v)]
(OUT/'reader-config-args.json').write_text(json.dumps(args,indent=2)+'\n')
e={k:v for k,v in os.environ.items() if not (k.startswith(('CODEX_','OPENAI_','ANTHROPIC_','MCP_')) or k in ['LD_PRELOAD','DYLD_INSERT_LIBRARIES'])}
# Production uses the existing CLI authentication, without copying account files.
# exec below ignores user config; all context/tool settings are explicit.
p=subprocess.run(['codex','debug','prompt-input',*args,'ISOLATION_PREFLIGHT_ONLY'],env=dict(e,CODEX_HOME=str(PROBE/'codex-home')),cwd=PROBE,capture_output=True,timeout=30)
(OUT/'prompt-input-isolated.json').write_bytes(p.stdout);(OUT/'prompt-input-isolated.stderr.txt').write_bytes(p.stderr)
print('prompt_exit',p.returncode,'stderr',p.stderr.decode()[:1000],flush=True)
data=json.loads(p.stdout)
print('input_roles',[x.get('role') for x in data], 'input_texts',[c.get('text','')[:180] for x in data for c in x.get('content',[])],flush=True)
received=[]
class Capture(BaseHTTPRequestHandler):
    def log_message(self,*a):pass
    def do_POST(self):
        raw=self.rfile.read(int(self.headers.get('content-length','0')))
        if self.headers.get('content-encoding'):raise RuntimeError(self.headers.get('content-encoding'))
        d=json.loads(raw);received.append(d)
        (OUT/'isolation-request.json').write_bytes(raw)
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        item={'id':'msg_isolation','type':'message','role':'assistant','status':'completed','content':[{'type':'output_text','text':'ISOLATION_OK','annotations':[]}]}
        response={'id':'resp_isolation','object':'response','created_at':int(time.time()),'status':'completed','model':'gpt-6-astra','output':[item],'usage':{'input_tokens':0,'output_tokens':0,'total_tokens':0}}
        events=[{'type':'response.created','response':{**response,'status':'in_progress','output':[]}}, {'type':'response.output_item.added','output_index':0,'item':{**item,'status':'in_progress','content':[]}}, {'type':'response.output_text.delta','item_id':'msg_isolation','output_index':0,'content_index':0,'delta':'ISOLATION_OK'}, {'type':'response.output_item.done','output_index':0,'item':item},{'type':'response.completed','response':response}]
        for event in events:self.wfile.write(('event: '+event['type']+'\ndata: '+json.dumps(event)+'\n\n').encode())
server=ThreadingHTTPServer(('127.0.0.1',0),Capture)
threading.Thread(target=server.serve_forever,daemon=True).start()
provider={'name':'local isolation capture, no inference','base_url':f'http://127.0.0.1:{server.server_port}','wire_api':'responses','requires_openai_auth':False,'supports_websockets':False}
pa=['-c','model_provider="isolation"','-c','model_providers.isolation='+json.dumps(provider).replace(': ', ' = ')]
# TOML inline table, not JSON.
pa=['-c','model_provider="isolation"','-c','model_providers.isolation={name="local isolation capture",base_url="http://127.0.0.1:'+str(server.server_port)+'",wire_api="responses",requires_openai_auth=false,supports_websockets=false}']
p=subprocess.run(['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny file-read-data (literal \"/Users/arrieta/.codex/AGENTS.md\") (literal \"/Users/arrieta/.codex/AGENTS.override.md\") (subpath \"/Users/arrieta/.codex/memories\"))','codex','exec','--ephemeral','--ignore-user-config','--ignore-rules','--skip-git-repo-check','--json',*args,*pa,'-'],input=b'ISOLATION_PREFLIGHT_ONLY',env=e,cwd=PROBE,capture_output=True,timeout=40)
(OUT/'isolation-exec.events.jsonl').write_bytes(p.stdout);(OUT/'isolation-exec.stderr.txt').write_bytes(p.stderr)
server.shutdown()
print('capture_exit',p.returncode,'requests',len(received),'stderr',p.stderr.decode()[:1500],flush=True)
if received:
 d=received[0];print('request_keys',list(d));print('tools',json.dumps(d.get('tools')));print('model',d.get('model'),'reasoning',d.get('reasoning'));print('input',json.dumps(d.get('input'))[:1200])
