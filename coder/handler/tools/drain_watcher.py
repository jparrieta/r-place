"""Observe one draining controller, then refresh reports without launching work."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

YARD = Path(__file__).resolve().parents[1]


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def process_matches(pid, expected):
    result = subprocess.run(
        ['/bin/ps', '-p', str(pid), '-o', 'command='],
        text=True, capture_output=True,
    )
    return result.returncode == 0 and expected in result.stdout


def atomic_json(path, value):
    temp = path.with_suffix('.tmp')
    with temp.open('w') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    temp.replace(path)


def main():
    pid = int(sys.argv[1])
    subreddit = sys.argv[2]
    expected = f'continue_yard_room.py {subreddit}'
    while process_matches(pid, expected):
        time.sleep(20)

    subprocess.run(
        [sys.executable, '-B', str(YARD / '_tools/update_coding_progress.py')],
        cwd=YARD,
    )
    root = YARD / '_coding_queue'
    state_path = root / 'STATE.json'
    state = json.loads(state_path.read_text())
    room_state = json.loads((YARD / 'rooms' / subreddit / 'STATE.json').read_text())
    receipt_path = YARD / 'rooms' / subreddit / 'validation' / 'RUN-RECEIPT.json'
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
    verified = room_state.get('coding_status') == 'verified' and receipt_path.exists()
    active = state.setdefault('active', {})
    active.pop(subreddit, None)
    if verified:
        tokens = receipt.get('reported_total_tokens')
        state.setdefault('completed', {})[subreddit] = {'tokens': tokens, 'at': now()}
        event = {'at': now(), 'event': 'finished', 'subreddit': subreddit,
                 'tokens': tokens, 'next_model': None}
    else:
        failure = {'at': now(), 'status': room_state.get('coding_status', 'controller exited')}
        state.setdefault('failed', {})[subreddit] = failure
        event = {'at': now(), 'event': 'needs-attention', 'subreddit': subreddit,
                 **failure, 'next_model': None}
    state.update({'status': 'drained', 'updated_utc': now()})
    atomic_json(state_path, state)
    with (root / 'EVENTS.jsonl').open('a') as stream:
        stream.write(json.dumps(event) + '\n')
        stream.flush()
        os.fsync(stream.fileno())


if __name__ == '__main__':
    main()
