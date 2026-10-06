#!/usr/bin/env python3
"""The adapter's live check, on the Mac, with the installed claude CLI and your own login.

It answers what the offline tests cannot: does this CLI write the stream the translator expects, does
the inbox hook reach the model in the middle of a turn, is a helper's prompt visible, and does SIGINT end
a turn that --resume can continue. It runs in a scratch folder in the controller's data folder, never in
a run, and costs three short turns.
    python3 aggregator/handler/claude-adapter/probe.py [--model sonnet]
Each check prints PASS or FAIL; the stream and a report stay in the scratch folder it names.
"""
import argparse
import importlib.util
import json
import secrets
import shlex
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('claude_adapter_actor', HERE / 'actor.py')
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)
S = A.stream


def turn(exe, flags, cwd, hooks, args, prompt, model, inbox_after=None, inbox=None, word=None, interrupt_after=None):
    cmd = [exe, '-p', '--output-format', 'stream-json', '--verbose']
    cmd += [f for f in ('--include-partial-messages', '--forward-subagent-text') if f in flags]
    cmd += args + ['--settings', str(hooks), '--strict-mcp-config', '--permission-mode', 'dontAsk',
                   '--allowedTools', 'Bash(sleep:*)', 'Bash(echo:*)', 'Agent', '--model', model, '--', prompt]
    n = len(list(cwd.glob('stream-*.jsonl')))
    out = cwd / ('stream-%d.jsonl' % n)
    start = time.monotonic()
    with out.open('wb') as f:
        p = subprocess.Popen(cmd, cwd=str(cwd), stdout=f, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)
        sent = interrupted = False
        while p.poll() is None:
            t = time.monotonic() - start
            if inbox_after is not None and not sent and t > inbox_after:
                A.write(inbox / 'probe-message.json', {'id': 'probe', 'kind': 'message', 'utc': A.stamp(),
                                                       'text': 'The code word is %s. Quote it in your last message.' % word})
                sent = True
            if interrupt_after is not None and not interrupted and t > interrupt_after:
                p.send_signal(signal.SIGINT)
                interrupted = True
            time.sleep(0.2)
        err = p.stderr.read().decode(errors='replace')
    lines = [json.loads(x) for x in out.read_text().splitlines() if x.strip().startswith('{')]
    return {'rc': p.returncode, 'lines': lines, 'stderr': err[-2000:], 'seconds': round(time.monotonic() - start, 1),
            'stream': str(out)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--model', default='sonnet')
    ap.add_argument('--claude', default=shutil.which('claude'))
    a = ap.parse_args()
    if not a.claude:
        sys.exit('claude is not on PATH')
    found = A.features(a.claude)
    root = A.data_dir() / 'claude-probe' / time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    inbox = root / 'inbox'
    (inbox / 'delivered').mkdir(parents=True)
    hooks = root / 'adapter-settings.json'
    A.write(hooks, {'hooks': {'PostToolUse': [{'matcher': '*', 'hooks': [{'type': 'command', 'command': ' '.join(
        shlex.quote(x) for x in (sys.executable, str(HERE / 'inbox_hook.py'), str(inbox)))}]}]}})
    word = secrets.token_hex(3).upper()
    results = []

    def check(name, ok, detail=''):
        results.append({'check': name, 'pass': bool(ok), 'detail': detail})
        print('%s  %s%s' % ('PASS' if ok else 'FAIL', name, ('  (' + detail + ')') if detail else ''))

    print('claude %s; optional flags offered: %s' % (found['version'], ' '.join(found['flags']) or 'none'))
    print('scratch folder: ' + str(root))
    one = turn(a.claude, found['flags'], root, hooks, [], (
        'This is a test of a message channel, not research. Use Bash to run `sleep 6`, then `echo one`, then '
        '`echo two`. Then start one helper with the Agent tool, description "probe helper", whose prompt is '
        'exactly: Reply with the word READY. When it returns, say whether a message from the principal '
        'investigator reached you during this turn, and if one did, quote its code word. Then stop.'),
        a.model, inbox_after=3, inbox=inbox, word=word)
    t = S.Translator('probe', 'one')
    events = [e for line in one['lines'] for e in t.feed(line)]
    sid = (t.init or {}).get('session_id')
    rows = [p['item'] for m, p in events if m in ('item/started', 'item/completed')]
    finals = [i['text'] for i in rows if i['type'] == 'agentMessage']
    check('the stream opens with system/init and a session id', sid, sid or '')
    check('the stream ends with a successful result', (t.result or {}).get('subtype') == 'success', str(one['rc']))
    if '--include-partial-messages' in found['flags']:
        check('the words stream as deltas', any(m == 'item/agentMessage/delta' for m, _ in events))
    check('each Bash call is a row with its command', any(i.get('command', '').startswith('Bash: sleep') for i in rows))
    helper = [i for i in rows if i.get('command', '').startswith('Helper (')]
    check('the helper\'s row shows the prompt the analyst wrote',
          any('Reply with the word READY' in i.get('aggregatedOutput', '') for i in helper))
    receipts = [json.loads(p.read_text()) for p in (inbox / 'delivered').glob('*.json')]
    check('the inbox hook delivered the message beside a tool result', any(r.get('via') == 'hook' for r in receipts),
          json.dumps(receipts)[:200])
    check('the analyst quoted the code word in the same turn', any(word in x for x in finals), word)
    two = turn(a.claude, found['flags'], root, hooks, ['--resume', sid] if sid else [],
               'Use Bash to run `sleep 60`, then say DONE.', a.model, interrupt_after=8)
    check('SIGINT ends the turn within a minute', two['seconds'] < 60, '%ss, exit %s' % (two['seconds'], two['rc']))
    three = turn(a.claude, found['flags'], root, hooks, ['--resume', sid] if sid else [],
                 'Say RESUMED and nothing else.', a.model)
    t3 = S.Translator('probe', 'three')
    for line in three['lines']:
        t3.feed(line)
    check('the session resumes after the interrupt', 'RESUMED' in str((t3.result or {}).get('result', '')))
    A.write(root / 'report.json', {'claude': found, 'model': a.model, 'word': word, 'results': results,
                                   'turns': [{k: v for k, v in x.items() if k != 'lines'} for x in (one, two, three)]})
    print('report: ' + str(root / 'report.json'))
    sys.exit(0 if all(r['pass'] for r in results) else 1)


if __name__ == '__main__':
    main()
