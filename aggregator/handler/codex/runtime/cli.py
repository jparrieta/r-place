"""Terminal interface to the same live actors used by the HTML panel."""
import argparse, json, os, shlex, shutil, subprocess, sys, time, urllib.request, urllib.error
from pathlib import Path
from .common import *

def request(data):
    endpoint=read(DATA/'controller.json')
    if not endpoint:
        command=shlex.join([sys.executable,str(Path(__file__).resolve().parents[1]/'run.py'),'serve'])
        raise Error('Start the controller: '+command)
    req=urllib.request.Request(endpoint['url']+'/api',data=json.dumps(data).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+endpoint['token']})
    try:
        with urllib.request.urlopen(req,timeout=100) as r: answer=json.load(r)
    except urllib.error.HTTPError as e: raise Error(json.load(e).get('error',str(e)))
    except OSError as e: raise Error('Controller unavailable: '+str(e))
    if 'error' in answer: raise Error(answer['error'])
    return answer['result']

def chat_request(actor,line):
    if line.startswith('/answer '):
        state=next((s for s in request({'action':'status'})['actors'] if s['id']==actor),{})
        q=next(iter(state.get('questions',[])),None)
        if not q:raise Error('No live question is pending. Refresh the conversation.')
        text=line[len('/answer '):]
        if q.get('source')=='file':
            return request({'action':'answer-ask','actor':actor,'run':q['run'],'request':q['requestKey'],'text':text})
        try:answers=json.loads(text) if text.lstrip().startswith('{') else {q['questions'][0]['id']:text}
        except ValueError:raise Error('Use /answer text for one question, or /answer {"question_id":"answer"} for several')
        if len(q['questions'])>1 and not text.lstrip().startswith('{'):raise Error('Answer all questions using a JSON object keyed by question ID')
        return request({'action':'answer','actor':actor,'request':q['requestKey'],'answers':answers})
    action=line[1:] if line in ('/pause','/stop','/save') else 'message'
    return request({'action':action,'actor':actor,'text':line})

def chat(actor):
    request({'action':'open','actor':actor})
    print('Connected. /pause, /stop, /save, /answer text, /quit. Type while it works to steer. /quit detaches.')
    import threading
    done=threading.Event()
    def events():
        offset=0
        while not done.wait(.7):
            try:
                r=request({'action':'events','actor':actor,'offset':offset}); offset=r['offset']
                for ev in r['events']:
                    m=ev['native']; p=m.get('params',{})
                    if m.get('method')=='item/agentMessage/delta': print(p.get('delta',''),end='',flush=True)
                    if m.get('method')=='turn/completed': print('\n['+p['turn']['status']+']',flush=True)
                    if m.get('method')=='item/tool/requestUserInput':
                        print('\n[Question for you. Use /answer. No answer is sent automatically.]',flush=True)
                        for q in p.get('questions',[]):print(q['id']+': '+q['question']+'\n'+'\n'.join(o['label']+': '+o.get('description','') for o in q.get('options') or []),flush=True)
                    if m.get('method') in ('item/started','item/completed') and p.get('item',{}).get('type')=='commandExecution':
                        item=p['item'];print('\n['+item.get('status','tool')+'] '+item.get('command','')+'\n'+(item.get('aggregatedOutput') or ''),flush=True)
            except Exception as e: print('\n'+str(e)); return
    threading.Thread(target=events,daemon=True).start()
    try:
        while True:
            line=input('\n> ')
            if line=='/quit': break
            try: print(json.dumps(chat_request(actor,line),ensure_ascii=False))
            except Error as e: print(e)
    except (EOFError,KeyboardInterrupt): pass
    finally: done.set()

def scientific_dependencies():
    """Use the same isolated interpreter import policy as trusted D4 replay."""
    code="import json,numpy,scipy;print(json.dumps({'numpy':numpy.__version__,'scipy':scipy.__version__}))"
    try:
        result=subprocess.run([sys.executable,'-I','-B','-c',code],capture_output=True,text=True,timeout=20)
        if result.returncode:return {'available':False,'error':result.stderr.strip()[-2000:]}
        return {'available':True,'versions':json.loads(result.stdout),'interpreter':sys.executable}
    except (OSError,subprocess.TimeoutExpired,ValueError) as error:return {'available':False,'error':str(error)}

def main(argv=None):
    p=argparse.ArgumentParser(description='Resumable r/place agents, files and interviews inside the workspace (the folder that holds r-place)')
    sub=p.add_subparsers(dest='command',required=True)
    x=sub.add_parser('serve'); x.add_argument('--port',type=int,default=8767)
    x=sub.add_parser('remote-serve',help='Private remote gateway; does not start or stop actors')
    x.add_argument('--origin',required=True); x.add_argument('--port',type=int,default=8768)
    sub.add_parser('remote-link',help='Print the private remote browser link')
    sub.add_parser('remote-revoke',help='Invalidate remote links without stopping actors')
    x=sub.add_parser('phone',help='Set up private phone access; never starts research');x.add_argument('--check',action='store_true')
    sub.add_parser('status'); sub.add_parser('login'); sub.add_parser('handler')
    x=sub.add_parser('build'); x.add_argument('run'); x.add_argument('--source'); x.add_argument('--fleet-arm',choices=['codex','openrouter'],default='codex')
    x=sub.add_parser('branch'); x.add_argument('source_run'); x.add_argument('checkpoint'); x.add_argument('run'); x.add_argument('--leg',required=True)
    for command in ('branch-status','prepare-branch','publish-branch'):
        x=sub.add_parser(command); x.add_argument('run')
    x=sub.add_parser('branch-cancel-upload'); x.add_argument('run'); x.add_argument('path'); x.add_argument('--stage')
    x=sub.add_parser('branch-put'); x.add_argument('run'); x.add_argument('path'); x.add_argument('--file',required=True); x.add_argument('--stage')
    sub.add_parser('arms')
    sub.add_parser('lead-status')
    x=sub.add_parser('import-lead'); x.add_argument('sub'); x.add_argument('--home',required=True); x.add_argument('--workspace',required=True); x.add_argument('--executable',required=True); x.add_argument('--thread',required=True); x.add_argument('--model',required=True); x.add_argument('--effort',required=True)
    x=sub.add_parser('register-lead'); x.add_argument('sub'); x.add_argument('checkpoint')
    x=sub.add_parser('step'); x.add_argument('run'); x.add_argument('leg'); x.add_argument('--start',action='store_true')
    x=sub.add_parser('run-block',help='Authorize and run a finite range of repeated legs');x.add_argument('run');x.add_argument('--first',required=True);x.add_argument('--last',required=True)
    for command in ('block-status','stop-block','resume-block'):
        x=sub.add_parser(command);x.add_argument('run')
    for cmd in ('chat','pause','stop','save','open'):
        x=sub.add_parser(cmd); x.add_argument('actor')
    x=sub.add_parser('send'); x.add_argument('actor'); x.add_argument('text')
    x=sub.add_parser('close'); x.add_argument('run'); x.add_argument('actor')
    for cmd in ('resume','resume-handler'):
        x=sub.add_parser(cmd);x.add_argument('checkpoint');x.add_argument('--actor')
    for cmd in ('stop-run','continue-run','recover-plan'):
        x=sub.add_parser(cmd);x.add_argument('run')
    sub.add_parser('prune')
    x=sub.add_parser('verify'); x.add_argument('checkpoint')
    x=sub.add_parser('job'); x.add_argument('job')
    x=sub.add_parser('dispatch'); x.add_argument('run'); x.add_argument('stage'); x.add_argument('--round'); x.add_argument('--only'); x.add_argument('--dry-run',action='store_true')
    x=sub.add_parser('labelers'); x.add_argument('run'); x.add_argument('--recheck',action='store_true')
    sub.add_parser('test'); sub.add_parser('manual'); sub.add_parser('doctor'); sub.add_parser('verify-all')
    x=sub.add_parser('acceptance'); x.add_argument('--live',action='store_true',required=True); x.add_argument('--fleet-arm',choices=['codex','openrouter'],default='codex')
    x=sub.add_parser('recover'); x.add_argument('dispatch')
    x=sub.add_parser('start'); x.add_argument('actor')
    x=sub.add_parser('card'); x.add_argument('actor'); x.add_argument('text')
    a=p.parse_args(argv); d=vars(a); cmd=d.pop('command')
    if cmd=='phone':
        from .phone import setup
        print(json.dumps(setup(**d),indent=2));return 0
    if cmd in ('remote-serve','remote-link','remote-revoke'):
        from . import remote
        if cmd=='remote-serve': return remote.serve(**d)
        print(remote.link() if cmd=='remote-link' else remote.revoke()); return 0
    if cmd=='branch-put':
        from .branches import CHUNK
        import base64
        source=Path(d.pop('file')).expanduser(); total=source.stat().st_size; digest=sha(source); offset=0
        with source.open('rb') as stream:
            while True:
                chunk=stream.read(CHUNK)
                result=request({'action':'branch-upload',**d,'content':base64.b64encode(chunk).decode(),'offset':offset,'total':total,'digest':digest})
                offset=result['received']
                if result['complete']:break
        print(json.dumps(result,indent=2));return 0
    if cmd=='import-lead':
        from .imports import capture_cli
        from . import leads
        if leads.hashes(d['workspace'])!=leads.hashes(leads.CORPUS/d['sub']): raise Error('Workspace triplet does not match current room')
        receipt=capture_cli(d['home'],d['workspace'],d['executable'],d['model'],d['effort'],d['thread'])
        print(json.dumps(leads.bind(d['sub'],receipt['checkpoint']),indent=2)); return 0
    if cmd in ('lead-status','register-lead'):
        from . import leads
        result=leads.preflight() if cmd=='lead-status' else leads.bind(d['sub'],d['checkpoint'])
        print(json.dumps(result,indent=2)); return 0
    if cmd=='arms':
        from .arms import catalog
        print(json.dumps(catalog(),indent=2)); return 0
    if cmd=='serve':
        from .server import serve
        return serve(**d)
    if cmd=='verify-all':
        from .verification import verify
        return verify()
    if cmd=='manual':
        from .manual import publish
        print(json.dumps(publish(),indent=2)); return 0
    if cmd=='doctor':
        from .native import resolve_executable
        print(json.dumps({'root':str(ROOT),'python':sys.version,'codex':resolve_executable(required=False),'free_GiB':round(shutil.disk_usage(ROOT).free/1024**3,2),'scientific_dependencies':scientific_dependencies(),'private_login_present':(DATA/'login/auth.json').is_file(),'controller_present':(DATA/'controller.json').is_file()},indent=2)); return 0
    if cmd=='acceptance':
        from .acceptance import live, live_openrouter
        if d['fleet_arm']=='openrouter': live=live_openrouter
        result=live(); print(json.dumps(result,indent=2)); return 0 if result['passed'] else 1
    if cmd=='login':
        from .native import configure, resolve_executable
        executable=resolve_executable()
        home=DATA/'login'; configure(home,'gpt-6-sol','medium',DATA/'login-workspace')
        return subprocess.call([executable,'login'],env=env(home),cwd=ROOT)
    if cmd=='test':
        return subprocess.call([sys.executable,'-B','-m','unittest','discover','-s',str(CODEX/'runtime/tests'),'-v'],cwd=ROOT,env={**env(),'PYTHONPATH':str(CODEX)})
    if cmd=='chat': return chat(d['actor'])
    if cmd=='dispatch' and d.get('only'): d['only']=d['only'].split(',')
    if cmd=='step':
        start=d.pop('start'); r=request({'action':'prepare',**d})
        if start: request({'action':'message','actor':r['actor'],'text':r['prompt']})
    else: r=request({'action':{'send':'message','resume':'restore'}.get(cmd,cmd),**d})
    print(json.dumps(r,indent=2,ensure_ascii=False)); return 0
