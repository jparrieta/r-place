#!/usr/bin/env python3
"""A stand-in for `claude -p --output-format stream-json`, for the adapter's tests only.

It plays the turns of a scenario (FAKE_SCENARIO, a JSON file {"turns": [[step, ...], ...]}; one turn
per call, counted in <scenario>.n), writes the stream the adapter reads, runs the PostToolUse hooks of
its --settings file as the CLI would, and writes a transcript the harness's confirm() and preclose()
read. A step is one of:
  {"say": text}                          the analyst's words, streamed and then whole
  {"tool": name, "input": {...}, "output": text, "error": bool, "sleep": s, "ask": {question, assumption}}
  {"say_context": true}                  says what the hooks gave it ("heard: ...")
  {"say_prompt": true}                   says the turn's prompt ("prompt: ...")
  {"wait_context": s}                    calls short tools until a hook gives it something, then says it
  {"helper": {...Agent input...}, "reply": text}
  {"pause": s}                           waits without a tool call
  {"thinking": text}, {"compact": true}, {"exit": code}
  {"foreign_session": true}             (anywhere in a turn) writes the transcript under another id
  {"write": {"path": p, "text": t}}      writes a file in the analyst's folder (its cwd)
  {"done": {"stage": NN, "cut": c}}      what done.sh leaves: out/_closes/NN-<.leg>.closed, "<stamp> <cut|close>"
SIGINT ends the turn with an error result, as the CLI ends a headless turn.
"""
import json
import os
import re
import signal
import subprocess
import sys
import time
import uuid

a = sys.argv[1:]
FLAGS = os.environ.get('FAKE_CLAUDE_FLAGS', '--include-partial-messages --forward-subagent-text --permission-prompts')
if a and a[0] == '--version':
    print('9.9.9 (fake stream claude)')
    sys.exit(0)
if a and a[0] == '--help':
    print('Usage: claude [options] [prompt]\n  -p, --print\n  --output-format <format>\n  ' + '\n  '.join(FLAGS.split()))
    sys.exit(0)


def opt(k):
    return a[a.index(k) + 1] if k in a else None


prompt = a[a.index('--') + 1] if '--' in a else ''
sid = (opt('--session-id') if '--fork-session' in a else (opt('--resume') or opt('--session-id'))) or str(uuid.UUID(int=0))
model = opt('--model') or 'unknown'
cfg = os.environ['CLAUDE_CONFIG_DIR']
proj = os.path.join(cfg, 'projects', os.environ.get('CLAUDE_CODE_PROJECT_DIR_NAME', 'other'))
os.makedirs(proj, exist_ok=True)
tpath = os.path.join(proj, sid + '.jsonl')
if '--fork-session' in a:
    parent = os.path.join(proj, opt('--resume') + '.jsonl')
    if os.path.exists(parent) and not os.path.exists(tpath):
        # as claude 2.1.289 forks (J's Mac, 5 October): the parent's messages keep their ids and take the new
        # session's id; lines without an id stay behind
        with open(parent) as src, open(tpath, 'w') as dst:
            for line in src:
                row = json.loads(line) if line.strip() else None
                if row and row.get('uuid'):
                    row['sessionId'] = sid
                    dst.write(json.dumps(row) + '\n')
calls = os.path.join(cfg, 'stream_calls.jsonl')
with open(calls, 'a') as f:
    f.write(json.dumps({'argv': a, 'cwd': os.getcwd(), 'env': {k: os.environ.get(k) for k in (
        'CLAUDE_CODE_PROJECT_DIR_NAME', 'CLAUDE_CODE_DISABLE_AUTO_MEMORY', 'STAGE', 'CLAUDE_CODE_SUBAGENT_MODEL')}}) + '\n')

scenario = os.environ['FAKE_SCENARIO']
counter = scenario + '.n'
n = int(open(counter).read()) if os.path.exists(counter) else 0
open(counter, 'w').write(str(n + 1))
steps = json.load(open(scenario))['turns'][n]
foreign = any('foreign_session' in s for s in steps)

interrupted = []
signal.signal(signal.SIGINT, lambda *_: interrupted.append(1))
settings = json.load(open(opt('--settings'))) if opt('--settings') else {}
contexts, last_text, started = [], '', time.time()


def out(m):
    sys.stdout.write(json.dumps(m) + '\n')
    sys.stdout.flush()


def row(kind, content, stop=None):
    m = {'role': kind, 'content': content}
    if kind == 'assistant':
        m.update(model=model, stop_reason=stop or 'end_turn')
    with open(tpath, 'a') as f:
        f.write(json.dumps({'type': kind, 'sessionId': str(uuid.uuid4()) if foreign else sid, 'uuid': str(uuid.uuid4()), 'message': m}) + '\n')


def check():
    if interrupted:
        out({'type': 'result', 'subtype': 'error_during_execution', 'is_error': True, 'result': 'interrupted',
             'session_id': sid})
        sys.exit(130)


def nap(s):
    end = time.time() + s
    while time.time() < end:
        check()
        time.sleep(0.02)
    check()


def hooks(name, args, tid, output, agent=None):
    for group in (settings.get('hooks') or {}).get('PostToolUse', []):
        m = group.get('matcher') or '*'
        if m != '*' and not re.fullmatch(m, name):
            continue
        for h in group.get('hooks', []):
            payload = {'session_id': sid, 'transcript_path': tpath, 'cwd': os.getcwd(), 'hook_event_name': 'PostToolUse',
                       'tool_name': name, 'tool_input': args, 'tool_use_id': tid, 'tool_response': output}
            if agent:
                payload.update(agent_id=agent, agent_type='general-purpose')
            r = subprocess.run(h['command'], shell=True, input=json.dumps(payload), capture_output=True, text=True,
                               timeout=30)
            if r.stdout.strip():
                ctx = json.loads(r.stdout).get('hookSpecificOutput', {}).get('additionalContext')
                if ctx and not agent:
                    contexts.append(ctx)


def say(text, parent=None):
    global last_text
    mid = 'msg_' + uuid.uuid4().hex[:10]
    if not parent:
        row('assistant', [{'type': 'text', 'text': text}], stop='tool_use')   # the CLI writes each message as it goes
        out({'type': 'stream_event', 'event': {'type': 'message_start', 'message': {'id': mid}}, 'parent_tool_use_id': None})
        out({'type': 'stream_event', 'event': {'type': 'content_block_start', 'index': 0, 'content_block': {'type': 'text'}},
             'parent_tool_use_id': None})
        half = len(text) // 2
        for piece in (text[:half], text[half:]):
            out({'type': 'stream_event', 'event': {'type': 'content_block_delta', 'index': 0,
                                                   'delta': {'type': 'text_delta', 'text': piece}}, 'parent_tool_use_id': None})
        out({'type': 'stream_event', 'event': {'type': 'message_stop'}, 'parent_tool_use_id': None})
        last_text = text
    out({'type': 'assistant', 'message': {'id': mid, 'content': [{'type': 'text', 'text': text}]},
         'parent_tool_use_id': parent, 'session_id': sid})


def tool(name, args, output, error=False, sleep=0.0, parent=None, ask=None):
    tid = 'toolu_' + uuid.uuid4().hex[:12]
    if not parent:
        row('assistant', [{'type': 'tool_use', 'id': tid, 'name': name, 'input': args}], stop='tool_use')
    out({'type': 'assistant', 'message': {'id': 'msg_' + uuid.uuid4().hex[:10],
                                          'content': [{'type': 'tool_use', 'id': tid, 'name': name, 'input': args}]},
         'parent_tool_use_id': parent, 'session_id': sid})
    nap(sleep)
    if ask:
        os.makedirs('out', exist_ok=True)
        with open('out/asks.jsonl', 'a') as f:
            f.write(json.dumps(dict(ask, t='2026-10-04T12:00:00', stage='A1', leg='A1a', ids=[])) + '\n')
    hooks(name, args, tid, output, agent=parent and 'agent-' + parent[-6:])
    out({'type': 'user', 'message': {'role': 'user', 'content': [{'type': 'tool_result', 'tool_use_id': tid,
                                                                    'content': output, 'is_error': error}]},
         'parent_tool_use_id': parent, 'session_id': sid})
    return tid


out({'type': 'system', 'subtype': 'init', 'session_id': sid, 'model': model, 'permissionMode': opt('--permission-mode'),
     'claude_code_version': '9.9.9', 'cwd': os.getcwd(), 'tools': ['Bash', 'Read', 'Agent']})
with open(tpath, 'a') as f:   # the CLI's own lines, without ids, at each start (claude 2.1.289)
    for kind in ('custom-title', 'agent-name', 'mode', 'atis-latch'):
        f.write(json.dumps({'type': kind, 'sessionId': sid}) + '\n')
row('user', prompt)
for s in steps:
    check()
    if 'say' in s:
        say(s['say'])
    elif 'tool' in s:
        tool(s['tool'], s.get('input', {}), s.get('output', ''), s.get('error', False), s.get('sleep', 0), ask=s.get('ask'))
    elif 'say_context' in s:
        say('heard: ' + ' | '.join(contexts))
        contexts.clear()
    elif 'say_prompt' in s:
        say('prompt: ' + prompt)
    elif 'wait_context' in s:
        end = time.time() + s['wait_context']
        while not contexts and time.time() < end:
            tool('Bash', {'command': 'sleep 0.2'}, '')
            nap(0.2)
        say('heard: ' + ' | '.join(contexts))
        contexts.clear()
    elif 'helper' in s:
        tid = 'toolu_' + uuid.uuid4().hex[:12]
        out({'type': 'assistant', 'message': {'id': 'msg_' + uuid.uuid4().hex[:10], 'content': [
            {'type': 'tool_use', 'id': tid, 'name': 'Agent', 'input': s['helper']}]}, 'parent_tool_use_id': None})
        out({'type': 'user', 'message': {'role': 'user', 'content': [{'type': 'text', 'text': s['helper']['prompt']}]},
             'parent_tool_use_id': tid})
        tool('Read', {'file_path': 'out/notes-A1.md'}, 'notes', parent=tid)
        say('helper working note', parent=tid)
        hooks('Agent', s['helper'], tid, s.get('reply', ''))
        out({'type': 'user', 'message': {'role': 'user', 'content': [
            {'type': 'tool_result', 'tool_use_id': tid, 'content': [{'type': 'text', 'text': s.get('reply', '')}]}]},
             'parent_tool_use_id': None})
    elif 'pause' in s:
        nap(s['pause'])
    elif 'thinking' in s:
        out({'type': 'assistant', 'message': {'id': 'msg_t', 'content': [{'type': 'thinking', 'thinking': s['thinking']}]},
             'parent_tool_use_id': None})
    elif 'compact' in s:
        out({'type': 'system', 'subtype': 'compact_boundary', 'compact_metadata': {'trigger': 'auto'}})
    elif 'exit' in s:
        sys.exit(s['exit'])
    elif 'write' in s:
        w = s['write']
        os.makedirs(os.path.dirname(w['path']) or '.', exist_ok=True)
        with open(w['path'], 'w') as f:
            f.write(w.get('text', ''))
        tool('Write', {'file_path': w['path']}, 'written')
    elif 'done' in s:
        st = s['done'].get('stage', 'A1')
        leg = open('.leg').read().strip() if os.path.exists('.leg') else st + '-leg'
        os.makedirs('out/_closes', exist_ok=True)
        with open('out/_closes/%s-%s.closed' % (st, leg), 'a') as f:
            f.write('%s %s\n' % (time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()), s['done'].get('cut') or 'close'))
        tool('Bash', {'command': 'bash tools/done.sh %s' % st}, 'leg %s closed. Stop now.' % leg)
row('assistant', [{'type': 'text', 'text': last_text}])
with open(tpath, 'a') as f:   # a line without an id, as the CLI writes its own (a fork leaves these behind)
    f.write(json.dumps({'type': 'last-prompt', 'sessionId': sid}) + '\n')
out({'type': 'result', 'subtype': 'success', 'is_error': False, 'result': last_text, 'session_id': sid,
     'total_cost_usd': 0.01, 'num_turns': len(steps), 'duration_ms': int((time.time() - started) * 1000),
     'usage': {'input_tokens': 10, 'output_tokens': 5}})
