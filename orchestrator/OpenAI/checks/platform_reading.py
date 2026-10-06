"""Opt-in v43 platform-reading test. No research run, fleet, or external data."""
from pathlib import Path
import json, re, sys, uuid, argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--live', action='store_true', help='Explicitly allow a small paid synthetic model check')
args = parser.parse_args()
if not args.live:
    parser.error('Use --live only when a live acceptance check is authorized.')
REPO = Path(__file__).resolve().parents[3]
CODEX = REPO/'aggregator/handler/codex'
sys.path.insert(0, str(CODEX))
from runtime import study, actors
from runtime.common import DATA, atomic, write, read, sha, now

if not (DATA/'login/auth.json').is_file():
    raise SystemExit('BLOCKED: complete python3 run.py login in the isolated v43 runtime first.')
tag = 'v43-platform-' + uuid.uuid4().hex[:8]
private = DATA/'acceptance'/tag
source = private/'source'
ws = source/'00_GIVE-THE-AGENT'
(ws/'out').mkdir(parents=True)
(source/'DROPS').mkdir()
atomic(ws/'out/_head.md', '# Synthetic platform-reading acceptance\nNo corpus or research is present.\n')
for name in ('CLAUDE.md', 'PLATFORM-claude.md'):
    atomic(ws/name, 'STALE-CLAUDE-REFERENCE: must not reach a Codex analyst.\n')
result = {'id':tag, 'started_utc':now(), 'synthetic':True, 'passed':False}
a = None
try:
    study.build(tag, source)
    s = study.run_state(tag)
    s.update(auto_dispatch=False, synthetic_acceptance=True)
    write(study.run_dir(tag)/'state.json', s)
    p = study.prepare(tag, 'A1a')
    a = actors.Actor(p['actor'])
    delivered = a.base/'workspace'
    names = sorted(f.name for f in delivered.glob('*.md'))
    assert 'PLATFORM-codex.md' in names
    assert 'CLAUDE.md' not in names and 'PLATFORM-claude.md' not in names
    assert sha(delivered/'PLATFORM-codex.md') == sha(study.INSTRUMENT/'PLATFORM-codex.md')
    result.update(delivered_root_markdown=names, model=a.state['model'], effort=a.state['effort'], platform_sha256=sha(delivered/'PLATFORM-codex.md'))
    prompt = '''This is a synthetic v43 acceptance test, not a research leg. Do not analyse rooms, run fleets, close the leg or produce scientific findings. There is no corpus. Read the delivered AGENT.md, AGENTS.md, OPENAI-RUNTIME.md, PLATFORM-codex.md and the stage card named by .stagefile. The shell starts in out. Read the required documents from the workspace root (one parent, cd ..). Do not seek files outside this workspace.
Return only a JSON object with these fields, based on those documents:
platform_document (filename); current_stage; current_leg; analyst_model; current_effort; A1c_effort;
B2_readers {model, effort, copies, route}; C2_reviewers {model, effort};
D2_case_leads {resume_original (boolean), platform};
continuation_uses_native_history (boolean); controller_dispatches_fleets (boolean);
pause_command (the literal command for this stage);
A1_task (one sentence stating what the delivered A1 stage does and its scope).
Do not write files. Do not infer or substitute model names from memory.'''
    a.message(prompt)
    a.wait(360)
    assert a.state.get('boundary') == 'completed', a.state.get('error')
    answer = a.final().strip()
    if answer.startswith('```'):
        answer = re.sub(r'^```(?:json)?\s*|\s*```$', '', answer)
    response = json.loads(answer)
    expected = {'platform_document':'PLATFORM-codex.md', 'current_stage':'A1', 'current_leg':'A1a', 'analyst_model':'gpt-6-astra', 'current_effort':'medium', 'A1c_effort':'high', 'continuation_uses_native_history':True, 'controller_dispatches_fleets':True}
    for key,value in expected.items():
        assert response.get(key) == value, (key, response.get(key), value)
    assert response['B2_readers'] == {'model':'gpt-6-sol','effort':'medium','copies':3,'route':'codex'}, response['B2_readers']
    assert response['C2_reviewers'] == {'model':'gpt-6-astra','effort':'high'}, response['C2_reviewers']
    assert response['D2_case_leads']['resume_original'] is True
    assert response['D2_case_leads']['platform'].lower() == 'codex'
    assert response['pause_command'] == 'bash tools/done.sh A1 --pause'
    result['analyst_response'] = response
    result['checkpoint'] = a.checkpoint()
    result['passed'] = True
except Exception as exc:
    result['error'] = str(exc)
finally:
    if a:
        a.release()
    if (study.run_dir(tag)/'state.json').exists():
        s=study.run_state(tag)
        s.update(stopped=True, stop_reason='Synthetic acceptance only. No research is authorized.')
        write(study.run_dir(tag)/'state.json',s)
        write(study.run_dir(tag)/'STOP.json',{'utc':now(),'reason':s['stop_reason']})
    result['finished_utc']=now()
    write(private/'result.json',result)
    # Deliberately exclude raw native logs, config, auth and account data from Orchestrator.
    print(json.dumps({'passed': result['passed'], 'receipt': str(private/'result.json'), 'error': result.get('error')}, indent=2))
if not result['passed']:
    raise SystemExit(1)
