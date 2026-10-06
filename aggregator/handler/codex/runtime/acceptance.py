"""Small authenticated restore test, opt-in and independent of research runs."""
import tempfile,uuid
from pathlib import Path
from .common import *
from . import actors,archive

def live():
    if not (DATA/'login/auth.json').is_file():raise Error('Sign in first with run.py login. No live test started.')
    tag='acceptance-'+uuid.uuid4().hex[:10]
    conversation_secret=uuid.uuid4().hex;file_secret=uuid.uuid4().hex
    result={'id':tag,'model':'gpt-6-sol','effort':'medium','checkpoints':[],'lineage':[],'passed':False}
    TMP.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='acceptance-',dir=TMP) as tmp:
        tmp=Path(tmp);(tmp/'out').mkdir();atomic(tmp/'out/payload.txt','filesystem-'+file_secret)
        actors.create(tag,tmp,'gpt-6-sol','medium',role='acceptance',instructions='This is a runtime test. Follow the user request literally. Never write the conversation secret to a file.')
    current=actors.Actor(tag)
    try:
        current.message('Remember the conversation-only secret '+conversation_secret+'. Do not use tools or write it to any file. Reply exactly READY.');current.wait(180)
        if current.state.get('boundary')!='completed':raise Error('Initial turn failed')
        initial=current.server.call('thread/read',{'threadId':current.state['thread_id'],'includeTurns':True})['thread']
        initial_turn=next(t for t in initial['turns'] if t['id']==current.state['last_turn_id'])
        if any(i.get('type') not in ('userMessage','agentMessage','reasoning','contextCompaction') for i in initial_turn.get('items',[])):raise Error('Initial secret turn used a tool; acceptance rejected')
        for index in (1,2):
            parent={k:current.state[k] for k in ('thread_id','last_turn_id')}
            receipt=current.checkpoint();result['checkpoints'].append(receipt)
            checkpoint=DATA/'checkpoints'/receipt['checkpoint'];before=inventory(checkpoint)
            restored=archive.restore(receipt['checkpoint'],tag+'-interview'+str(index));current.release();current=actors.Actor(restored['id'])
            if (current.base/'workspace/out/payload.txt').read_text()!='filesystem-'+file_secret:raise Error('Restored filesystem differs')
            current.open()
            thread=current.server.call('thread/read',{'threadId':current.state['thread_id'],'includeTurns':True})['thread']
            if current.state['thread_id']==parent['thread_id'] or parent['last_turn_id'] not in {t['id'] for t in thread.get('turns',[])}:raise Error('Native fork lineage does not include the recorded parent boundary')
            current.message('Without using any tools or reading files, reply with only the conversation-only secret from our earlier conversation.');current.wait(180)
            thread=current.server.call('thread/read',{'threadId':current.state['thread_id'],'includeTurns':True})['thread']
            turn=next(t for t in thread['turns'] if t['id']==current.state['last_turn_id'])
            if any(i.get('type') not in ('userMessage','agentMessage','reasoning','contextCompaction') for i in turn.get('items',[])):raise Error('Recall turn used a tool; acceptance rejected')
            if current.state.get('boundary')!='completed' or current.final().strip()!=conversation_secret:raise Error('Conversation-only recall failed')
            current.message('Read payload.txt in your current working directory and reply with only its exact contents.');current.wait(180)
            if current.state.get('boundary')!='completed' or current.final().strip()!='filesystem-'+file_secret:raise Error('Filesystem read failed')
            if inventory(checkpoint)!=before:raise Error('Parent checkpoint changed')
            result['lineage'].append({'checkpoint':receipt['checkpoint'],'parent_thread':parent['thread_id'],'parent_turn':parent['last_turn_id'],'child_thread':current.state['thread_id'],'child_turn':current.state['last_turn_id']})
        result['checkpoints'].append(current.checkpoint());result['passed']=True
    except Exception as e:result['error']=str(e)
    finally:current.release();write(DATA/'acceptance'/(tag+'.json'),result)
    return result


def live_openrouter():
    """Explicit opt-in: routing probe plus three tiny history turns, no research."""
    from . import arms,openrouter
    openrouter.key()  # fail before creating a test if credentials are absent
    tag='acceptance-router-'+uuid.uuid4().hex[:8]; conversation_secret=uuid.uuid4().hex;file_secret=uuid.uuid4().hex
    root=DATA/'acceptance'/tag; root.mkdir(parents=True)
    config=arms.resolve('openrouter')[0]['B3']['readers']; config={**config,'max_tokens':2048}
    result={'id':tag,'backend':'openrouter','checkpoints':[],'lineage':[],'continuity':'Explicit HTTP message history replay, not a native provider session','passed':False}; current=None
    try:
        binding=openrouter.bind(root,config); result['routing']=binding
        workspace=root/'workspace'; (workspace/'out').mkdir(parents=True); atomic(workspace/'out/payload.txt','filesystem-'+file_secret)
        openrouter.create(tag,workspace,config,binding); current=actors.load(tag)
        current.message('Remember the conversation-only secret '+conversation_secret+'. Reply READY.'); current.wait()
        if current.state.get('boundary')!='completed': raise Error(current.state.get('error') or 'First API turn failed')
        for index in (1,2):
            parent={k:current.state[k] for k in ('thread_id','last_turn_id')};history=read(current.base/'thread.json')
            receipt=current.checkpoint(); result['checkpoints'].append(receipt)
            checkpoint=DATA/'checkpoints'/receipt['checkpoint'];before=inventory(checkpoint)
            restored=archive.restore(receipt['checkpoint'],tag+'-interview'+str(index)); current.release(); current=actors.load(restored['id'])
            if (current.base/'workspace/out/payload.txt').read_text()!='filesystem-'+file_secret: raise Error('Restored filesystem differs')
            if current.state['thread_id']==parent['thread_id'] or current.state['last_turn_id']!=parent['last_turn_id'] or read(current.base/'thread.json')!=history:raise Error('API replay lineage differs from the recorded parent boundary')
            current.message('Recall the conversation-only secret. Reply with only that secret.'); current.wait()
            if current.state.get('boundary')!='completed' or current.final().strip()!=conversation_secret: raise Error('API history replay failed the secret check')
            if inventory(checkpoint)!=before: raise Error('Parent checkpoint changed')
            result['lineage'].append({'checkpoint':receipt['checkpoint'],'parent_thread':parent['thread_id'],'parent_turn':parent['last_turn_id'],'child_thread':current.state['thread_id'],'child_turn':current.state['last_turn_id']})
        result['checkpoints'].append(current.checkpoint()); result['passed']=True
    except Exception as e: result['error']=str(e)
    finally:
        if current: current.release()
        write(root/'RESULT.json',result)
    return result
