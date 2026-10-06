#!/usr/bin/env python3
"""The adapter's lifecycle acceptance, live, on the Mac: the ClaudeActor itself, with the installed claude
CLI, in a synthetic run of its own. No research run, no research data.

It covers what codex/ADAPTERS.md asks before the controller admits Claude: event shapes, the adapter's hook
combined with the run's own hooks, steering receipts, a durable answer while idle, a controller restart that
attaches to a running turn, a quiescent save, an interview restored from that save, a refused continuation,
a failed start and its retry, the run's close once, and the model in live metadata. It costs about six short
turns.

    python3 aggregator/handler/claude-adapter/probe_lifecycle.py [--model claude-sonnet-5-5] [--effort low]
        [--login-from RUN_FOLDER]

The synthetic run lives in the controller's data folder, always at the same place: claude-lifecycle/current/
run. A previous synthetic run moves to claude-lifecycle/<time>/, and its Claude folder (CONTROL/.cc) moves into
the new run at the same path, so a login made once into that folder serves every later probe, whether the CLI
keeps it in the folder or in the Keychain. The probe checks first that the folder can answer, and stops with the
one command to log in if it cannot. --login-from instead copies the two login files (.credentials.json,
.claude.json) of another run's CONTROL/.cc into it, mode 600, and deletes them when the probe ends. Each check
prints PASS or FAIL; the report stays beside the run.
"""
import argparse
import importlib.util
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent / 'claude'
_spec = importlib.util.spec_from_file_location('claude_adapter_actor', HERE / 'actor.py')
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)

# the synthetic run's step.sh and close.sh: tests/harness_stub.py, which builds a complete snapshot with the
# run's own protocol_guard.py (capture, preclose, verify_checkpoint); it leaves out the snap, the recall probe
# and publish.sh
STEP = '#!/usr/bin/env bash\nexec python3 "$(dirname "$0")/harness_stub.py" step "$@"\n'
CLOSE = '#!/usr/bin/env bash\nexec python3 "$(dirname "$0")/harness_stub.py" close "$@"\n'
START_ONLY = '''
import importlib.util, sys, time
spec = importlib.util.spec_from_file_location('a', sys.argv[1]); A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
a = A.ClaudeActor(sys.argv[2]); a.message(sys.argv[3]); time.sleep(2)
'''


def build(root, model, effort):
    run = root / 'run'
    c = run / 'CONTROL'
    (c / 'harness/validation_tools').mkdir(parents=True)
    (c / '.cc').mkdir()
    (run / '00_GIVE-THE-AGENT/out').mkdir(parents=True)
    for name in ('protocol_guard.py', 'pretool_guard.py', 'after_compact.sh', 'lib.sh'):
        shutil.copy(HARNESS / name, c / 'harness' / name)
    shutil.copy(HARNESS / 'settings.template.json', c / 'settings.template.json')
    shutil.copy(HERE / 'tests/harness_stub.py', c / 'harness/harness_stub.py')
    (c / 'harness/step.sh').write_text(STEP)
    (c / 'harness/close.sh').write_text(CLOSE)
    (c / 'harness/validation_tools/validate.py').write_text('import sys\nsys.exit(0)\n')
    (c / 'arm.json').write_text(json.dumps({'A1': {'analyst': model, 'effort': effort}}))
    (c / 'RUN.json').write_text('{}\n')
    return run


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    # a full model id: the close's model audit, as close.sh's, accepts a served model only when it starts with
    # the arm's name, and an alias such as 'sonnet' never does
    ap.add_argument('--model', default='claude-sonnet-5-5')
    ap.add_argument('--effort', default='low')
    ap.add_argument('--claude', default=shutil.which('claude'))
    ap.add_argument('--login-from')
    a = ap.parse_args()
    if not a.claude:
        sys.exit('claude is not on PATH')
    stamp = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    base = A.data_dir() / 'claude-lifecycle'
    root = base / 'current'
    carried = None
    if root.exists():
        # the last synthetic run steps aside under its time; its Claude folder, with any login, comes along
        old = base / ('%s-before-%s' % (time.strftime('%Y%m%dT%H%M%SZ', time.gmtime(root.stat().st_mtime)), stamp))
        if (root / 'run/CONTROL/.cc').is_dir():
            carried = base / ('.cc-carried-' + stamp)
            os.rename(root / 'run/CONTROL/.cc', carried)
        os.rename(root, old)
    run = build(root, a.model, a.effort)
    cc = run / 'CONTROL/.cc'
    if carried:
        os.rmdir(cc)
        os.rename(carried, cc)
    copied = []
    if a.login_from:
        for name in ('.credentials.json', '.claude.json'):
            src = Path(a.login_from) / 'CONTROL/.cc' / name
            if src.exists():
                shutil.copy(src, cc / name)
                os.chmod(cc / name, 0o600)
                copied.append(cc / name)
        if not (Path(a.login_from) / 'CONTROL/.cc/.credentials.json').exists():
            print('%s holds no .credentials.json: on macOS the login is kept outside the folder (the Keychain, as '
                  'far as we know), so it cannot be copied. Log in once into the synthetic run (below); the '
                  'probe keeps that folder for every later run.' % a.login_from)
    results = []

    def check(name, ok, detail=''):
        results.append({'check': name, 'pass': bool(ok), 'detail': str(detail)[:300]})
        print('%s  %s%s' % ('PASS' if ok else 'FAIL', name, ('  (' + str(detail)[:200] + ')') if detail else ''))

    print('synthetic run: ' + str(run))
    try:
        env = dict(os.environ, CLAUDE_CONFIG_DIR=str(cc))
        r = subprocess.run([a.claude, '-p', '--model', a.model, '--', 'Say OK and nothing else.'], cwd=str(run),
                           env=env, capture_output=True, text=True, timeout=180)
        if r.returncode or 'OK' not in r.stdout:
            print('The synthetic run\'s Claude folder cannot answer: %s' % (r.stderr or r.stdout)[-400:])
            print('Log in once into it, or pass --login-from with a run whose CONTROL/.cc is logged in:')
            print('  CLAUDE_CONFIG_DIR="%s" claude' % cc)
            sys.exit(2)
        word = secrets.token_hex(3).upper()
        name = 'lifecycle-' + stamp.lower()

        # 1. preparation starts no inference
        st = A.create(name, run, 'A1a', executable=a.claude)
        ac = A.ClaudeActor(name)
        check('create prepares an idle leg without a turn', st['status'] == 'prepared' and not (ac.base / 'turns').exists())

        # 2. a turn, a message mid-turn with its receipt, the hooks combined, the model in live metadata
        ac.message('This is a synthetic test, not research. Use Bash to run `sleep 6`, then `echo one`, then `echo two`. '
                   'Then say whether a message from the principal investigator reached you during this turn and, if '
                   'one did, quote its code word. Then stop.')
        time.sleep(3)
        q = ac.message('The code word is %s. Quote it in your last message.' % word)
        ac.wait(600)
        check('the turn completes and the session is confirmed', ac.state['boundary'] == 'completed' and ac.state['confirmed'],
              ac.state.get('error'))
        check('the message mid-turn has a hook receipt', (ac.receipt(q.get('queued', '')) or {}).get('via') == 'hook',
              ac.receipt(q.get('queued', '')))
        check('the analyst quoted the code word', word in ac.final(), ac.final()[-200:])
        eff = ac.state.get('effective', {})
        used = list((ac.state.get('usage') or {}).get('modelUsage', {}) or {})
        check('the live metadata names the session and a model', eff.get('session_id') == ac.state['session_id'] and
              (eff.get('model') or used), json.dumps({'init': eff, 'modelUsage': used}))
        print('note: the effort level is passed as --effort; the stream does not report it back.')
        rows = [json.loads(x)['native'] for x in (ac.base / 'events.jsonl').read_text().splitlines()]
        check('the panel events have their shapes', all(m in [e['method'] for e in rows] for m in (
            'turn/started', 'item/started', 'item/completed', 'turn/completed', 'rplace/messageDelivered')))

        # 3. a durable answer while idle, without a turn
        with (run / '00_GIVE-THE-AGENT/out/asks.jsonl').open('a') as f:
            f.write(json.dumps({'id': 'QA1-001', 'question': 'Probe question?', 'assumption': 'none', 'leg': 'A1a'}) + '\n')
        ac.surface(None)
        turns = len(list((ac.base / 'turns').iterdir()))
        r = ac.answer('QA1-001', {'answer': 'Probe answer.'})
        time.sleep(2)
        check('an idle answer is written read-only and starts no turn',
              not r['new_turn_started'] and len(list((ac.base / 'turns').iterdir())) == turns and
              (os.stat(run / '00_GIVE-THE-AGENT/out/_answers/QA1-001.md').st_mode & 0o222) == 0)

        # 4. a controller restart: another process starts a turn and exits; this one attaches and follows it
        ac.release()
        subprocess.run([sys.executable, '-c', START_ONLY, str(HERE / 'actor.py'), name,
                        'Use Bash to run `sleep 15`, then say ATTACHED.'], check=True, timeout=120)
        b = A.ClaudeActor(name)
        b.open()
        attached = any('Controller restarted' in (json.loads(x)['native']['params'].get('item') or {}).get('command', '')
                       for x in (b.base / 'events.jsonl').read_text().splitlines())
        b.wait(600)
        check('a restarted controller attaches to the running turn and sees it end', attached and
              b.state['boundary'] == 'completed' and 'ATTACHED' in b.final(), b.final()[-100:])

        # 5. a quiescent save, then an interview restored from it; a continuation is refused
        saved = b.checkpoint()
        check('a save is verified and is not a close', saved['verified'] and not b.state.get('closed') and
              not (run / 'CONTROL/close-calls.log').exists())
        try:
            A.restore(saved, name + '-cont', mode='continuation', executable=a.claude)
            refused = False
        except A.Error:
            refused = not (A.data_dir() / 'actors' / (name + '-cont')).exists()
        check('a continuation from a copy is refused before any change', refused)
        iv = A.restore(saved, name + '-iv', executable=a.claude)
        c = A.ClaudeActor(name + '-iv')
        c.message('What was the code word the principal investigator sent you? Answer with the word only.')
        c.wait(600)
        check('the interview runs in its own copy, forked, and remembers', c.state['boundary'] == 'completed' and
              word in c.final() and str(c.workspace) != str(b.workspace), c.final()[-100:])
        check('the saved folder is unchanged', bool(A.verify_saved(A.harness(run), saved['archive'])))
        c.release()

        # 6. a failed start keeps the message; an explicit retry sends it
        good = b.state['runtime']['executable']
        b.state['runtime']['executable'] = str(root / 'missing-claude')
        b.save()
        try:
            b.message('Say RETRIED.')
        except Exception:
            pass
        kept = len(b.state.get('undelivered', [])) == 1
        b.state['runtime']['executable'] = good
        b.save()
        b.continue_queued()
        b.wait(600)
        check('a failed start keeps the message and the retry sends it', kept and 'RETRIED' in b.final(), b.final()[-100:])

        # 7. the run's close, once; the probe stands in for done.sh, which the synthetic run does not have
        mark = run / '00_GIVE-THE-AGENT/out/_closes/A1-A1a.closed'
        mark.parent.mkdir(parents=True, exist_ok=True)
        mark.write_text(time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + ' close\n')
        try:
            receipt = b.close()
            again = b.close()
            check('the close runs once, verifies the whole snapshot and returns the same receipt',
                  receipt['verified'] and receipt['scientific'] and again.get('repeated') and
                  len((run / 'CONTROL/close-calls.log').read_text().splitlines()) == 1, receipt['publication'])
        except A.Error as e:
            check('the close runs once, verifies the whole snapshot and returns the same receipt', False, e)
        b.release()
        print('interview actor: %s' % iv['id'])
    finally:
        for p in copied:
            p.unlink(missing_ok=True)
        A.write(root / 'report.json', {'model': a.model, 'effort': a.effort, 'results': results})
        print('report: ' + str(root / 'report.json'))
    sys.exit(0 if results and all(r['pass'] for r in results) else 1)


if __name__ == '__main__':
    main()
