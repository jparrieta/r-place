"""Persistent investigator questions. Answering never starts an agent turn."""
import re
from .common import *

QID = re.compile(r'Q[A-Z0-9]{1,4}-[0-9]{3,}')


def safe_file(workspace, relative):
    workspace = inside(workspace)
    path = workspace / relative
    if not path.resolve().is_relative_to(workspace):
        raise Error('Question file leaves its workspace')
    for part in (path, *path.parents):
        if part == workspace.parent: break
        if part.is_symlink(): raise Error('Question files cannot use symlinks')
    return path


def rows(workspace):
    path = safe_file(workspace, 'out/asks.jsonl')
    if not path.exists(): return []
    result = []; seen = set()
    with path.open() as stream:
        for line in stream:
            # The analyst may be in the middle of its final append.
            if not line.endswith('\n'): break
            if not line.strip(): continue
            try: row = json.loads(line)
            except ValueError: raise Error('Malformed completed line in asks.jsonl') from None
            qid = row.get('id', '')
            if not isinstance(qid,str) or not QID.fullmatch(qid) or qid in seen:
                raise Error('Invalid or duplicate question identifier')
            if not isinstance(row.get('question'),str) or not row['question'].strip():
                raise Error('Question text is missing')
            seen.add(qid); result.append(row)
    return result


def answer_path(workspace, qid):
    if not isinstance(qid,str) or not QID.fullmatch(qid): raise Error('Invalid question identifier')
    return safe_file(workspace, 'out/_answers/' + qid + '.md')


def listing(workspace, run=None):
    result = []
    for row in rows(workspace):
        path = answer_path(workspace, row['id'])
        saved = read(DATA/'runs'/identity(run)/'answers'/(row['id']+'.json'),{}) if run else {}
        if saved and saved.get('question')!=row:
            raise Error('An answered question changed. Keep the original and ask a new question.')
        answer = saved.get('answer') or (path.read_text().strip() if path.exists() else None)
        result.append({**row, 'answer':answer, 'answered':bool(answer)})
    return result


def deliver(run, workspace):
    """Overlay later answers on a new leg, never on an archived parent."""
    for row in rows(workspace):
        saved = read(DATA/'runs'/identity(run)/'answers'/(row['id']+'.json'),{})
        if saved and saved.get('question')!=row: raise Error('Question changed before answer delivery')
        if saved: atomic(answer_path(workspace,row['id']),saved['answer']+'\n')
    safe_file(workspace,'out/_answers').mkdir(parents=True,exist_ok=True)


def answer_study(run, qid, text, expected_actor):
    from . import study, blocks
    run=identity(run)
    if actor_state(expected_actor).get('backend')=='claude':
        raise Error('Use the Claude actor answer route; direct controller answer-file writes are not supported')
    if not isinstance(text,str) or not text.strip() or len(text)>20000: raise Error('Provide a nonempty answer of at most 20000 characters')
    with lock(DATA/'locks'/('run-'+run+'.lock')):
        state=study.run_state(run)
        latest=state.get('active_actor') or next(iter(reversed(state.get('legs',{}).values())),{}).get('actor')
        if expected_actor!=latest: raise Error('The study advanced. Refresh before answering its current question.')
        workspace=Path(state['latest_workspace'])
        row=next((r for r in rows(workspace) if r['id']==qid),None)
        if not row: raise Error('Question no longer belongs to this study workspace')
        # Live native questions must be answered on their exact request, not by file.
        actor=actor_state(latest)
        if any(qid in q.get('persistedAsks',{}).values() for q in actor.get('questions',[])):
            raise Error('Answer this question through its live request')
        path=study.run_dir(run)/'answers'/(qid+'.json'); previous=read(path,{})
        existing=next(r for r in listing(workspace,run) if r['id']==qid).get('answer')
        if existing and existing!=text.strip(): raise Error('An answer is already recorded. Send a new correction card.')
        # Validate the destination before recording a durable intervention.
        if state.get('active_actor'): answer_path(workspace,qid)
        if not previous:
            write(path,{'id':qid,'utc':now(),'answer':text.strip(),'question':row,'actor':latest})
            event(study.run_dir(run)/'interventions.jsonl',kind='question-answer',actor=latest,question=qid,text=text.strip())
        if state.get('active_actor'):
            atomic(answer_path(workspace,qid),text.strip()+'\n')
        blocks.stop(run,'Investigator answered a question; review before further automatic legs')
        return {'answered':qid,'new_turn_started':False,'delivery':'available to the current leg' if state.get('active_actor') else 'saved for the next leg'}


def mirror_native(actor, request):
    """Keep native questions readable through mem.py asks after interruption."""
    workspace=actor.base/'workspace'; stage=(actor.state.get('leg') or 'N')[:2]
    mapping={}
    for question in request.get('questions',[]):
        qid='QN-'+str(uuid.uuid4().int)
        row={'id':qid,'t':now(),'stage':stage,'leg':actor.state.get('leg'),
             'question':question['question'],'assumption':'Wait for the answer before dependent work.',
             'ids':[],'origin':'native','request_key':request['requestKey'],'question_id':question['id']}
        event(safe_file(workspace,'out/asks.jsonl'),**row)
        event(safe_file(workspace,'out/diary/'+stage+'-1.jsonl'),t=row['t'],kind='ask',stage=stage,leg=row['leg'],ids=[qid],text=row['question'])
        mapping[question['id']]=qid
    request['persistedAsks']=mapping


def record_native_answer(actor, request, answers):
    workspace=actor.base/'workspace'
    for key,qid in request.get('persistedAsks',{}).items():
        atomic(answer_path(workspace,qid),answers[key].strip()+'\n')
