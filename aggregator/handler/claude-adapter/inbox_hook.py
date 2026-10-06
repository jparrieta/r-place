#!/usr/bin/env python3
"""PostToolUse hook for a leg the adapter runs: gives the analyst the principal investigator's
messages beside its next tool result.

The adapter passes this hook to `claude -p` through --settings, so the run's own settings never
change. Claude Code places a hook's hookSpecificOutput.additionalContext next to the tool result,
and the model reads it on its next request within the same turn (Claude Code hooks documentation).

Argument: the actor's inbox folder (outside the run, where the analyst cannot write). Each message is
inbox/<id>.json; a delivered one gets a receipt inbox/delivered/<id>.json. A helper's tool call
(agent_id in the input) delivers nothing: the messages are for the analyst J talks to. The hook never
fails a tool call: on any error it prints nothing and exits 0.
"""
import datetime
import fcntl
import json
import os
import sys
import uuid
from pathlib import Path

LIMIT = 8000   # characters of one message in the context; the panel keeps the whole text


def atomic(path, text):
    tmp = path.with_name('.' + path.name + '.' + uuid.uuid4().hex)
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def render(m):
    text = m.get('text') or ''
    if len(text) > LIMIT:
        text = text[:LIMIT] + '\n[shortened here; the whole message is in the investigator\'s panel]'
    if m.get('kind') == 'message':
        return ('Message from the principal investigator (%s). He follows your work live; answer him in '
                'your next message, then go on with the leg:\n%s' % (m.get('utc', ''), text))
    return text


def main():
    inbox = Path(sys.argv[1])
    try:
        data = json.load(sys.stdin)
    except ValueError:
        data = {}
    if not isinstance(data, dict) or data.get('agent_id'):
        return
    done = inbox / 'delivered'
    done.mkdir(parents=True, exist_ok=True)
    with open(inbox / '.lock', 'a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        items = []
        for p in sorted(inbox.glob('*.json')):
            if (done / p.name).exists():
                continue
            try:
                m = json.loads(p.read_text(encoding='utf-8'))
            except ValueError:
                continue
            if isinstance(m, dict):
                items.append((p, m))
        if not items:
            return
        # the context goes out before the receipts: a failed receipt repeats a message, never loses it
        context = '\n\n'.join(render(m) for _, m in items)
        sys.stdout.write(json.dumps({'hookSpecificOutput': {'hookEventName': 'PostToolUse',
                                                            'additionalContext': context}}) + '\n')
        sys.stdout.flush()
        stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        for p, m in items:
            atomic(done / p.name, json.dumps({'id': m.get('id'), 'via': 'hook', 'utc': stamp,
                                              'tool': data.get('tool_name'), 'tool_use_id': data.get('tool_use_id'),
                                              'session_id': data.get('session_id')}) + '\n')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
