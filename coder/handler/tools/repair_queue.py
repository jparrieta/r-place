#!/usr/bin/env python3
"""Run the fixed blocked-room repair set, smallest first, six at a time."""
import argparse
import datetime
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time

YARD = Path(__file__).resolve().parents[1]
ROOT = YARD / '_repair_queue'
STOP_AFTER_ACTIVE = ROOT / 'STOP_AFTER_ACTIVE.json'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def read_json(path):
    return json.loads(Path(path).read_text())


def atomic_json(path, value):
    temp = path.with_suffix('.tmp')
    with temp.open('w') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    temp.replace(path)


def blocked_rooms():
    rows = []
    for source in (YARD / 'rooms').iterdir():
        state_path = source / 'STATE.json'
        if not state_path.exists():
            continue
        state = read_json(state_path)
        if (str(state.get('coding_status', '')).startswith('blocked:') or
                state.get('coding_status') == 'repair fresh lead starting'):
            rows.append({'subreddit': source.name, 'items': state.get('items_in_window', 10**12),
                         'initial_status': state.get('coding_status')})
    return sorted(rows, key=lambda row: (row['items'], row['subreddit']))


def live_repair(pid, sub):
    result = subprocess.run(['/bin/ps', '-p', str(pid), '-o', 'command='],
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return result.returncode == 0 and ('repair_blocked_room.py ' + sub) in result.stdout


def live_pid(pid):
    result = subprocess.run(['/bin/ps', '-p', str(pid), '-o', 'pid='],
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parallel', type=int, default=6, choices=range(1, 7))
    parser.add_argument('--retry-failed', action='store_true',
                        help='Retry only unresolved members of the saved repair pool; retain history.')
    args = parser.parse_args()
    ROOT.mkdir(exist_ok=True)
    (ROOT / 'logs').mkdir(exist_ok=True)
    lock = (ROOT / 'LOCK').open('a+')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit('A repair queue is already running.')
    previous_path = ROOT / 'STATE.json'
    previous = read_json(previous_path) if previous_path.exists() else None
    adopting = previous and previous.get('status') in ('running', 'draining')
    if args.retry_failed:
        if not previous or adopting:
            raise SystemExit('--retry-failed requires a stopped saved repair pool.')
        queue = []
        seen = set()
        candidates = list(previous.get('failed', {}))
        candidates.extend(row.get('subreddit') for row in previous.get('queued', []))
        for sub in candidates:
            if not sub or sub in seen:
                continue
            seen.add(sub)
            current = read_json(YARD / 'rooms' / sub / 'STATE.json')
            if current.get('coding_status') == 'verified':
                continue
            queue.append({'subreddit': sub, 'items': current.get('items_in_window', 10**12),
                          'initial_status': current.get('coding_status')})
        queue.sort(key=lambda row: (row['items'], row['subreddit']))
        atomic_json(ROOT / ('STATE-before-retry-%d.json' % time.time_ns()), previous)
        state = previous
        state.setdefault('attempt_failures', []).extend(
            dict(failure, subreddit=sub) for sub, failure in state.get('failed', {}).items())
        state.update({'pid': os.getpid(), 'status': 'running', 'parallel': args.parallel,
                      'active': {}, 'queued': queue, 'failed': {}, 'resumed_utc': now()})
        state.pop('finished_utc', None)
    elif adopting:
        queue = previous.get('queued', [])
        # Keep ended attempts too: the reconciliation loop must record their
        # result instead of silently dropping workers that exited during restart.
        active = dict(previous.get('active', {}))
        for active_row in active.values():
            active_row.setdefault('model', 'gpt-5.6-sol')
            active_row.setdefault('effort', 'medium')
        done = set(previous.get('completed', {})) | set(previous.get('failed', {})) | set(active)
        queue = [row for row in queue if row.get('subreddit') not in done]
        state = previous
        state.update({'pid': os.getpid(), 'status': 'running', 'parallel': args.parallel,
                      'active': active, 'queued': queue, 'resumed_utc': now()})
    else:
        queue = blocked_rooms()
        state = {'pid': os.getpid(), 'status': 'running', 'parallel': args.parallel,
                 'started_utc': now(), 'queued': queue, 'active': {},
                 'completed': {}, 'failed': {}}
    if STOP_AFTER_ACTIVE.exists():
        state['status'] = 'draining'
        state['stop_after_active'] = read_json(STOP_AFTER_ACTIVE)
    atomic_json(ROOT / 'STATE.json', state)
    children = {sub: row['pid'] for sub, row in state['active'].items()}
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}

    def event(kind, sub=None, **fields):
        row = {'at': now(), 'event': kind, 'subreddit': sub, **fields}
        with (ROOT / 'EVENTS.jsonl').open('a') as stream:
            stream.write(json.dumps(row) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        print(json.dumps(row), flush=True)

    event('repair-queue-resumed' if adopting else 'repair-queue-started',
          count=len(queue), parallel=args.parallel, adopted=sorted(children))
    while queue or children:
        draining = STOP_AFTER_ACTIVE.exists()
        if draining:
            state['status'] = 'draining'
            state['stop_after_active'] = read_json(STOP_AFTER_ACTIVE)
        for sub, child in list(children.items()):
            try:
                if isinstance(child, subprocess.Popen):
                    code = child.poll()
                    alive = code is None
                else:
                    alive = live_repair(child, sub)
                    code = None if alive else None
                    if alive and not live_pid(child):
                        alive = False
                if alive:
                    continue
                children.pop(sub, None)
                active = state['active'].pop(sub, {})
                source_state = read_json(YARD / 'rooms' / sub / 'STATE.json')
                receipt = YARD / 'rooms' / sub / 'validation' / 'RUN-RECEIPT.json'
                if source_state.get('coding_status') == 'verified' and receipt.exists():
                    tokens = read_json(receipt).get('reported_total_tokens')
                    state['completed'][sub] = {'at': now(), 'tokens': tokens,
                                               'archive_sha256': source_state.get('lead_archive_sha256')}
                    event('finished', sub, tokens=tokens,
                          next_model=None if draining else 'gpt-5.6-sol/medium',
                          next_subreddit=queue[0]['subreddit'] if queue and not draining else None)
                else:
                    state['failed'][sub] = {'at': now(), 'returncode': code,
                                            'status': source_state.get('coding_status'),
                                            'log': active.get('log'),
                                            'archive_sha256': source_state.get('lead_archive_sha256')}
                    event('needs-attention', sub, returncode=code,
                          status=source_state.get('coding_status'))
                subprocess.run([sys.executable, '-B', str(YARD / '_tools/status.py'),
                                '--yard', str(YARD), '--no-refresh'], env=env,
                               stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                subprocess.run([sys.executable, '-B', str(YARD / '_tools/update_coding_progress.py')],
                               env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            except Exception as exc:
                children.pop(sub, None)
                active = state['active'].pop(sub, {})
                state['failed'][sub] = {'at': now(), 'returncode': None,
                                        'status': 'coordinator reconciliation failed: ' + str(exc),
                                        'log': active.get('log')}
                event('needs-attention', sub, returncode=None,
                      status='coordinator reconciliation failed: ' + str(exc))

        while queue and len(children) < args.parallel and not STOP_AFTER_ACTIVE.exists():
            # Exercise prompt generation before dispatch. A shared scheduler error must
            # stop the pool instead of consuming every remaining room as a failed retry.
            probe = subprocess.run([sys.executable, '-B', str(YARD / '_tools/room.py'),
                                    'message', 'lead', '--room',
                                    str(YARD / 'rooms' / queue[0]['subreddit'])],
                                   env=env, capture_output=True, text=True)
            if probe.returncode:
                state.update(status='blocked: scheduler prompt preflight', queued=queue,
                             updated_utc=now())
                atomic_json(ROOT / 'STATE.json', state)
                event('scheduler-blocked', error=probe.stderr[-3000:])
                return
            if STOP_AFTER_ACTIVE.exists():
                break
            row = queue.pop(0)
            sub = row['subreddit']
            attempt = 'repair-' + str(time.time_ns())
            log = ROOT / 'logs' / (sub + '-' + attempt + '.log')
            command = [sys.executable, '-B', str(YARD / '_tools/repair_blocked_room.py'),
                       sub, '--attempt', attempt]
            with log.open('w') as stream:
                child = subprocess.Popen(command, env=env, stdout=stream,
                                         stderr=subprocess.STDOUT, start_new_session=True,
                                         close_fds=True)
            children[sub] = child
            state['active'][sub] = {'items': row['items'], 'pid': child.pid,
                                    'attempt': attempt, 'log': str(log), 'started_utc': now(),
                                    'model': 'gpt-5.6-sol', 'effort': 'medium'}
            event('started', sub, items=row['items'], pid=child.pid,
                  model='gpt-5.6-sol', effort='medium')
        state['queued'] = queue
        state['updated_utc'] = now()
        atomic_json(ROOT / 'STATE.json', state)
        if STOP_AFTER_ACTIVE.exists() and not children:
            break
        if queue or children:
            time.sleep(20)
    if STOP_AFTER_ACTIVE.exists():
        state.update({'status': 'stopped after active', 'stopped_utc': now(),
                      'updated_utc': now(), 'queued': queue})
        atomic_json(ROOT / 'STATE.json', state)
        event('repair-queue-drained', completed=len(state['completed']),
              failed=len(state['failed']), queued=len(queue))
        return
    state.update({'status': 'finished', 'finished_utc': now(), 'updated_utc': now()})
    atomic_json(ROOT / 'STATE.json', state)
    event('repair-queue-finished', completed=len(state['completed']), failed=len(state['failed']))


if __name__ == '__main__':
    main()
