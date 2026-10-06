#!/usr/bin/env python3
"""Protocol fixture only. Never used by a research run."""
import json, os, sys, uuid, re, tomllib
from pathlib import Path
home=Path(os.environ['CODEX_HOME']); sessions=home/'sessions'; sessions.mkdir(exist_ok=True)
threads={}; active=None;waiting={}
effort=tomllib.loads((home/'config.toml').read_text()).get('model_reasoning_effort','medium')

def send(data): print(json.dumps(data),flush=True)
def emit(method,params): send({'method':method,'params':params})
def load(path):
 rows=[json.loads(x) for x in Path(path).read_text().splitlines()]; meta=rows[0]['payload']; turns=[x['payload']['turn'] for x in rows if x['type']=='fake_turn']; return {'id':meta['id'],'path':str(path),'turns':turns}
def persist(t):
 p=Path(t['path']); rows=[{'type':'session_meta','payload':{'id':t['id']}}]
 for turn in t['turns']:
  rows.extend([{'type':'fake_turn','payload':{'turn':turn}},{'type':'event_msg','payload':{'type':'task_complete','turn_id':turn['id']}}])
 p.write_text(''.join(json.dumps(r)+'\n' for r in rows))
for line in sys.stdin:
 try:
  r=json.loads(line); m=r.get('method'); p=r.get('params',{}); rid=r.get('id')
  if rid is None:continue
  if m is None and rid in waiting:
   t,turn=waiting.pop(rid);answer=json.dumps(r.get('result',r.get('error')))
   emit('serverRequest/resolved',{'threadId':t['id'],'requestId':rid})
   turn.update(status='completed',items=[{'type':'agentMessage','phase':'final_answer','text':answer}]);t['turns'].append(turn);persist(t);emit('turn/completed',{'threadId':t['id'],'turn':turn});continue
  if m=='initialize': result={'userAgent':'fixture'}
  elif m=='thread/start':
   tid=str(uuid.uuid4()); t={'id':tid,'path':str(sessions/('rollout-'+tid+'.jsonl')),'turns':[]};threads[tid]=t;persist(t);result={'thread':t,'model':p['model'],'reasoningEffort':effort}
  elif m in ('thread/resume','thread/fork'):
   path=p.get('path') or sessions/('rollout-'+p['threadId']+'.jsonl');t=load(path)
   if m=='thread/fork':tid=str(uuid.uuid4());t=dict(t,id=tid,path=str(sessions/('rollout-'+tid+'.jsonl')));persist(t)
   threads[t['id']]=t;result={'thread':t,'model':p['model'],'reasoningEffort':effort}
  elif m=='thread/read':result={'thread':threads[p['threadId']]}
  elif m=='thread/backgroundTerminals/list':result={'data':[]}
  elif m=='turn/start':
   t=threads[p['threadId']];turn={'id':str(uuid.uuid4()),'status':'inProgress','items':[]};send({'id':rid,'result':{'turn':turn}});emit('turn/started',{'threadId':t['id'],'turn':turn})
   text=p['input'][0]['text']; prior=' '.join(x.get('text','') for tr in t['turns'] for x in tr['items']);answer='fixture: '+text+' | previous: '+prior
   if text=='ASK_PI':
    request='question-'+uuid.uuid4().hex;waiting[request]=(t,turn)
    send({'id':request,'method':'item/tool/requestUserInput','params':{'threadId':t['id'],'turnId':turn['id'],'itemId':'ask-pi','isBlocking':True,'questions':[{'id':'choice','header':'Choice','question':'Which interpretation?', 'options':[{'label':'A','description':'First'},{'label':'B','description':'Second'}]}]}});continue
   fixture=re.findall(r'FIXTURE_RETURN ([^\n]+)',text)
   if fixture: answer=fixture[-1]+'\nEND'
   turn.update(status='completed',items=[{'type':'userMessage','content':p['input']},{'type':'agentMessage','phase':'final_answer','text':answer}]);t['turns'].append(turn);persist(t);emit('item/agentMessage/delta',{'delta':answer,'threadId':t['id']});emit('turn/completed',{'threadId':t['id'],'turn':turn});continue
  elif m=='turn/interrupt':
   for request,(t,turn) in list(waiting.items()):
    if turn['id']==p['turnId']:
     waiting.pop(request);emit('serverRequest/resolved',{'threadId':t['id'],'requestId':request});turn.update(status='interrupted');t['turns'].append(turn);persist(t);emit('turn/completed',{'threadId':t['id'],'turn':turn})
   result={}
  else:raise ValueError('unknown fixture method '+str(m))
  send({'id':rid,'result':result})
 except Exception as e:send({'id':r.get('id'),'error':{'message':str(e)}})
