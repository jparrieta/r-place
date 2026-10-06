"""Smallest-ready-first launcher. Owns scheduling, never research decisions."""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

YARD = Path(__file__).resolve().parents[1]
LEGACY_TOOLS = Path('/Users/arrieta/Documents/ChatGPT/place Yard/work')
SUFFIX = '-gpt56-calibration-v1'
PRIOR_RUN_RECODE_ALLOWLIST = {'liverpoolfc'}
sys.path.insert(0, str(YARD / '_tools'))
import room


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def read_json(path, default=None):
    if not path.exists():
        return default
    # Room STATE.json is updated by workers while the scheduler scans rooms.
    # A read can briefly catch the file between truncate and write.
    for attempt in range(10):
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            if attempt == 9:
                raise
            time.sleep(0.1)


def atomic_json(path, value):
    temp = path.with_suffix('.tmp')
    with temp.open('w') as f:
        json.dump(value, f, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    temp.replace(path)


def ready_rooms(excluded=(), yard=YARD, validate=room._brief_validation):
    ready = []
    stored_sources = {read_json(p, {}).get('source_room')
                      for p in (yard / '_lead_sessions').glob('*/STORE.json')}
    for source in (yard / 'rooms').iterdir():
        if not source.is_dir() or not re.fullmatch(r'[A-Za-z0-9_]+', source.name):
            continue
        if source.name in excluded:
            continue
        st = read_json(source / 'STATE.json', {})
        count = st.get('items_in_window')
        if not isinstance(count, int) or not 500 <= count <= 50000:
            continue
        if st.get('failed') or str(st.get('coding_status', '')).startswith('blocked:'):
            continue
        lead_path = yard / '_lead_sessions' / (source.name + SUFFIX)
        if ((source / 'run').exists() or st.get('lead_store') or st.get('lead_archive')
                or str(source) in stored_sources or lead_path.exists()
                or lead_path.with_name(lead_path.name + '.tar.zst').exists()):
            continue
        if (source.name not in PRIOR_RUN_RECODE_ALLOWLIST
                and any(r.get('kind') == 'coder' for r in st.get('prior_runs', []))):
            continue
        if not (source / 'brief/out/brief.md').is_file():
            continue
        validation = validate(str(source))
        if validation['passed'] or not validation['required']:
            ready.append((count, source.name))
    return sorted(ready)


def process_table():
    # Capture locally; never publish other processes' command lines.
    result = subprocess.check_output(['/bin/ps', '-ww', '-axo', 'pid=,ppid=,stat=,lstart=,command='], text=True)
    table = {}
    for line in result.splitlines():
        match = re.match(r'\s*(\d+)\s+(\d+)\s+(\S+)\s+(\w{3}\s+\w{3}\s+\d+\s+[\d:]+\s+\d{4})\s+(.*)', line)
        if not match:
            raise RuntimeError('Cannot parse process inventory; no new rooms will launch.')
        pid, ppid, status, started, command = match.groups()
        if 'Z' not in status:
            table[int(pid)] = {'ppid': int(ppid), 'started': started, 'command': command}
    if not table:
        raise RuntimeError('Empty process inventory; no new rooms will launch.')
    return table


def controllers(table, yard=YARD, legacy=LEGACY_TOOLS):
    found = {}
    for pid, identity in table.items():
        command = identity['command']
        for base in [yard / '_tools', legacy]:
            prefix = r'^\S*python\S*\s+(?:(?:-B|-u)\s+)*'
            pattern = prefix + re.escape(str(base)) + r'/(start_yard_lead|continue_yard_room)\.py\s+([A-Za-z0-9_]+)(?:\s|$)'
            match = re.search(pattern, command, re.I)
            sub = match.group(2) if match else None
            if re.search(prefix + re.escape(str(base / 'retry_ukraine.py')) + r'(?:\s|$)', command, re.I):
                sub = 'ukraine'
            if sub and (yard / 'rooms' / sub / 'STATE.json').exists():
                found.setdefault(sub, []).append(pid)
                break
    return {sub: sorted(set(pids)) for sub, pids in found.items()}


def top_controllers(pids, table):
    tops = []
    for pid in pids:
        ancestor = table[pid]['ppid']
        seen = {pid}
        nested = False
        while ancestor in table and ancestor not in seen:
            if ancestor in pids:
                nested = True
                break
            seen.add(ancestor)
            ancestor = table[ancestor]['ppid']
        if not nested:
            tops.append(pid)
    return tops


def unattended_workers(table, running):
    found = {}
    ambiguous = []
    for store in (YARD / '_lead_sessions').glob('*' + SUFFIX):
        sub = store.name[:-len(SUFFIX)]
        if sub in running:
            continue
        lead = read_json(store / 'RUNNING.json', {})
        live = []
        runner = lead.get('runner_pid')
        if runner in table and 'codex_lead.py' in table[runner]['command'] and str(store) in table[runner]['command']:
            live.append(runner)
            server = lead.get('server_pid')
            if server in table and table[server]['ppid'] == runner:
                live.append(server)
        for receipt in (store / 'audit').glob('coder-*/receipt.json'):
            coder = read_json(receipt, {})
            pid = coder.get('pid')
            if coder.get('status') not in ('completed-and-attached', 'failed') and pid in table:
                command = table[pid]['command']
                if 'codex' in command and str(store / 'workspace/room/run/fleet') in command:
                    live.append(pid)
        if live:
            found[sub] = sorted(set(live))
        else:
            status = read_json(YARD / 'rooms' / sub / 'STATE.json', {}).get('coding_status', '')
            if lead or (status and status != 'verified' and not status.startswith('blocked:')):
                ambiguous.append(sub)
    return found, ambiguous


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parallel', type=int, default=20, choices=range(1, 21))
    parser.add_argument('--inspect', action='store_true', help='Read-only process and ready-queue inventory')
    parser.add_argument('--clear-pause', action='store_true', help='Clear a previously diagnosed launch pause; unresolved conditions pause again')
    parser.add_argument('--requeue-failed', action='store_true',
                        help='Queue currently blocked, unverified historical failures before new rooms')
    args = parser.parse_args()
    root = YARD / '_coding_queue'
    drain_path = root / 'DRAIN'
    table = process_table()
    running = controllers(table)
    orphaned, ambiguous = unattended_workers(table, running)
    if args.inspect:
        print(json.dumps({'active': running, 'unattended': orphaned, 'ambiguous': ambiguous, 'ready': ready_rooms()}, indent=2))
        return
    root.mkdir(exist_ok=True)
    (root / 'logs').mkdir(exist_ok=True)
    lock = (root / 'LOCK').open('a+')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit('A coding queue is already running.')
    state_path = root / 'STATE.json'
    state = read_json(state_path, {'active': {}, 'completed': {}, 'failed': {}, 'events': 0})
    state.setdefault('failure_streaks', {})
    if args.clear_pause:
        state.pop('launch_pause', None)
    state.update({'pid': os.getpid(), 'started_utc': now(), 'status': 'running',
                  'parallel': args.parallel, 'model': 'gpt-5.6-sol', 'effort': 'medium'})
    children = {}
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}

    def event(kind, sub=None, **data):
        row = {'at': now(), 'event': kind, 'subreddit': sub, **data}
        with (root / 'EVENTS.jsonl').open('a') as log:
            log.write(json.dumps(row) + '\n')
            log.flush()
            os.fsync(log.fileno())
        state['events'] += 1
        print(json.dumps(row), flush=True)

    def save():
        state['updated_utc'] = now()
        atomic_json(state_path, state)

    def has_repair(sub):
        return any(r.get('sub') == sub and r.get('status', 'queued') in ('queued', 'running')
                   for r in state.get('repairs', []))

    def mechanical_failure(status, log_path):
        detail = str(status or '')
        path = Path(log_path or '')
        if path.is_file():
            detail += '\n' + path.read_text(errors='replace')[-12000:]
        markers = (
            'No clean checkpoint matching ',
            'Runtime changed. Use the original Codex binary and Python runtime',
            'Previously coded room: outside this wave.',
            'No space left on device',
            'Bad file descriptor',
            'Restore failed:',
            'JSONDecodeError:',
            'Checkpoint differs from current files.',
            "can't initialize sys standard streams",
            'serverOverloaded',
            'Selected model is at capacity',
        )
        return any(marker in detail for marker in markers)

    def token_limit_reached(log_path):
        path = Path(log_path or '')
        if not path.is_file():
            return False
        detail = path.read_text(errors='replace')[-12000:].lower()
        markers = (
            'usagelimitexceeded',
            'ratelimitexceeded',
            'rate_limit_exceeded',
            'insufficient_quota',
            'usage limit reached',
            'usage limit has been reached',
            'reached your usage limit',
            'hit your usage limit',
            'out of credits',
            'not enough credits',
        )
        return any(marker in detail for marker in markers)

    def queue_repair(sub, items, status):
        if has_repair(sub):
            return
        note = str(status or 'Initial scheduler check failed; retry from the clean checkpoint chosen by repair_blocked_room.py.')
        if int(state['failure_streaks'].get(sub, 0)) >= 2:
            return
        attempt = 'auto-' + str(time.time_ns())
        state.setdefault('repairs', []).append({
            'sub': sub, 'items': items, 'attempt': attempt,
            'retry_note': note[-6000:], 'status': 'queued',
            'queued_utc': now(), 'kind': 'auto-after-first-check-failure',
        })
        event('repair-queued', sub, items=items, attempt=attempt)

    def seed_failed_repairs():
        if not args.requeue_failed:
            return
        unresolved = []
        for sub in state.get('failed', {}):
            if sub in state.get('active', {}):
                continue
            source = YARD / 'rooms' / sub
            st = read_json(source / 'STATE.json', {})
            receipt = source / 'validation/RUN-RECEIPT.json'
            if (str(st.get('coding_status', '')).startswith('blocked:')
                    and not receipt.is_file() and not st.get('verified_utc')):
                failure = state.get('failed', {}).get(sub, {})
                if mechanical_failure(st.get('coding_status'), failure.get('log')):
                    detail = str(st.get('coding_status', ''))
                    log_path = Path(failure.get('log', ''))
                    if log_path.is_file():
                        detail += '\n' + log_path.read_text(errors='replace')[-12000:]
                    if 'Runtime changed. Use the original Codex binary and Python runtime' not in detail:
                        continue
                unresolved.append((st.get('items_in_window', 10**9), sub,
                                   st.get('coding_status')))
        for items, sub, status in sorted(unresolved):
            queue_repair(sub, items, status)

    try:
        # A full disk can interrupt codex_lead init before STORE.json or a
        # checkpoint exists. Such a directory is only a partial copy of the
        # intact source room, not a forkable lead store. Recover it narrowly so
        # the same room can be admitted again after capacity is restored.
        live_at_start = set(running) | set(orphaned)
        for sub, old in list(state.get('active', {}).items()):
            if sub in live_at_start or old.get('repair'):
                continue
            store = YARD / '_lead_sessions' / (sub + SUFFIX)
            log_path = Path(old.get('log', ''))
            source = YARD / 'rooms' / sub
            no_space = (log_path.is_file() and
                        'No space left on device' in log_path.read_text(errors='replace'))
            uninitialized = (store.is_dir() and not (store / 'HEAD.json').exists()
                             and not (store / 'state/lead.json').exists()
                             and not (store / 'RUNNING.json').exists())
            if no_space and uninitialized and not (source / 'run').exists():
                shutil.rmtree(store)
                state['active'].pop(sub, None)
                state.get('failed', {}).pop(sub, None)
                event('partial-launch-recovered', sub, reason='no-space init copy removed; source room intact')
        for sub, failure in list(state.get('failed', {}).items()):
            store = YARD / '_lead_sessions' / (sub + SUFFIX)
            log_path = Path(failure.get('log', ''))
            source = YARD / 'rooms' / sub
            no_space = (log_path.is_file() and
                        'No space left on device' in log_path.read_text(errors='replace'))
            empty_exit = (failure.get('status') == 'controller exited before a verified run'
                          and log_path.is_file() and log_path.stat().st_size == 0)
            uninitialized = (store.is_dir() and not (store / 'HEAD.json').exists()
                             and not (store / 'state/lead.json').exists()
                             and not (store / 'RUNNING.json').exists())
            if ((no_space or empty_exit) and uninitialized and not (source / 'run').exists()
                    and int(state['failure_streaks'].get(sub, 0)) < 2):
                shutil.rmtree(store)
                count = read_json(source / 'STATE.json', {}).get('items_in_window')
                attempt = 'clean-restart-' + str(time.time_ns())
                if not has_repair(sub):
                    state.setdefault('repairs', []).append({
                        'sub': sub, 'items': count, 'attempt': attempt,
                        'retry_note': 'Clean restart after a no-space partial initialization.',
                        'status': 'queued', 'queued_utc': now(),
                        'kind': 'fresh-restart-after-partial',
                    })
                event('partial-launch-recovered', sub,
                      reason='no-space partial store removed; clean restart queued')
        seed_failed_repairs()
        event('scheduler-started', parallel=args.parallel)
        while True:
            for sub, child in list(children.items()):
                if child.poll() is not None:
                    del children[sub]
            table = process_table()
            running = controllers(table)
            # A just-launched Python child may not yet appear in ps after exec.
            for sub, child in children.items():
                running.setdefault(sub, [child.pid])
            orphaned, ambiguous = unattended_workers(table, running)
            if ambiguous:
                reason = 'Unattended state needs review: ' + ', '.join(sorted(ambiguous))
                if state.get('launch_pause') != reason:
                    event('launch-paused', reason=reason)
                state['launch_pause'] = reason
            live = {**running, **orphaned}
            changed = False
            for sub in list(state['active']):
                if sub in live:
                    continue
                old = state['active'].pop(sub)
                source = YARD / 'rooms' / sub
                st = read_json(source / 'STATE.json', {})
                receipt = read_json(source / 'validation/RUN-RECEIPT.json', {})
                if st.get('coding_status') == 'verified' and receipt and (source / 'run').is_dir():
                    tokens = receipt.get('reported_total_tokens')
                    state['completed'][sub] = {'tokens': tokens, 'at': now()}
                    state['failed'].pop(sub, None)
                    state['failure_streaks'].pop(sub, None)
                    event('finished', sub, tokens=tokens)
                    for repair in state.get('repairs', []):
                        if repair.get('sub') == sub:
                            repair.update({'status': 'completed', 'finished_utc': now()})
                else:
                    failure = {'at': now(), 'status': st.get('coding_status', 'controller exited before a verified run'), 'log': old.get('log')}
                    state['failed'][sub] = failure
                    limit_reached = token_limit_reached(failure['log'])
                    mechanical = limit_reached or mechanical_failure(failure['status'], failure['log'])
                    streak = int(state['failure_streaks'].get(sub, 0))
                    if not mechanical:
                        streak += 1
                        state['failure_streaks'][sub] = streak
                    event('needs-attention', sub, failure_streak=streak,
                          mechanical=mechanical, **failure)
                    for repair in state.get('repairs', []):
                        if old.get('repair') and repair.get('sub') == sub:
                            repair.update({'status': 'needs-attention', 'finished_utc': now(),
                                           'failure': failure['status']})
                    if limit_reached:
                        state['launch_pause'] = 'GPT-5.6 Sol usage limit reached; user requested no model switch.'
                        event('token-limit-paused', sub, status=failure['status'])
                    elif mechanical:
                        event('mechanical-repair-needed', sub, status=failure['status'])
                        failure_text = Path(failure['log']).read_text(errors='replace')
                        if ('serverOverloaded' in failure_text
                                or 'Selected model is at capacity' in failure_text):
                            queue_repair(sub, old.get('items') or st.get('items_in_window'),
                                         'Temporary GPT-5.6 Sol capacity failure; resume the same saved lead.')
                        elif 'Runtime changed. Use the original Codex binary and Python runtime' in failure_text:
                            queue_repair(sub, old.get('items') or st.get('items_in_window'),
                                         'Saved checkpoint runtime changed; preserve the archive and restart a fresh lead.')
                    elif streak < 2 and str(failure['status']).startswith('blocked:'):
                        queue_repair(sub, old.get('items') or st.get('items_in_window'), failure['status'])
                    elif streak >= 2:
                        event('repair-stopped-after-two-failures', sub,
                              failure_streak=streak, status=failure['status'])
                    if not str(st.get('coding_status', '')).startswith('blocked:'):
                        state['launch_pause'] = 'Unexplained controller exit: ' + sub
                changed = True
            # Reconciliation can turn a stale running repair into needs-attention.
            # Seed it here, before ready-room selection, so no upward room jumps
            # ahead of an authorized unresolved repair.
            seed_failed_repairs()
            for sub, pids in live.items():
                if sub not in state['active']:
                    state['active'][sub] = {'adopted_utc': now()}
                    event('adopted', sub, pids=pids)
                    changed = True
                active = state['active'][sub]
                if sub in orphaned and not active.get('unattended'):
                    event('unattended-worker', sub, pids=pids)
                active.update({'pids': pids, 'unattended': sub in orphaned})
                identities = {str(pid): {'started': table[pid]['started'], 'ppid': table[pid]['ppid'],
                                         'command_sha256': hashlib.sha256(table[pid]['command'].encode()).hexdigest()}
                              for pid in pids if pid in table}
                for pid, previous in active.get('identities', {}).items():
                    current = identities.get(pid)
                    if current and (current['started'], current['command_sha256']) != (previous['started'], previous['command_sha256']):
                        state['launch_pause'] = 'Controller identity changed: ' + sub
                        event('controller-identity-changed', sub, pid=int(pid))
                active['identities'] = identities
                if sub in running:
                    tops = top_controllers([pid for pid in pids if pid in table], table)
                    if len(tops) > 1:
                        reason = 'Duplicate independent controllers: ' + sub
                        if state.get('launch_pause') != reason:
                            event('controller-collision', sub, pids=tops)
                        state['launch_pause'] = reason
            ready = ready_rooms(set(state['active']) | set(state['failed']))
            repairs = sorted(
                [r for r in state.get('repairs', []) if r.get('status', 'queued') == 'queued'],
                key=lambda r: (r.get('items', 10**9), r.get('sub', ''), r.get('queued_utc', '')),
            )
            if drain_path.exists():
                reason = drain_path.read_text().strip() or 'User-requested drain'
                if state.get('launch_pause') != reason:
                    event('launch-paused', reason=reason)
                state['launch_pause'] = reason
            launch_reserve = 0
            while (not state.get('launch_pause') and not drain_path.exists()
                   and len(state['active']) < args.parallel
                   and (repairs or ready)):
                free_bytes = shutil.disk_usage(YARD).free
                floor = 8 * 1024**3
                per_launch = 1024**3
                if free_bytes - launch_reserve < floor + per_launch:
                    wait = {'free_bytes': free_bytes, 'floor_bytes': floor,
                            'reserved_this_cycle': launch_reserve}
                    if state.get('disk_capacity_wait') != wait:
                        event('disk-capacity-wait', **wait)
                    state['disk_capacity_wait'] = wait
                    break
                state.pop('disk_capacity_wait', None)
                repair = repairs.pop(0) if repairs else None
                if repair:
                    sub = repair['sub']
                    count = int(repair['items'])
                    if repair.get('kind') == 'fresh-restart-after-partial':
                        command = [sys.executable, '-B', str(YARD / '_tools/start_yard_lead.py'),
                                   sub, '--complete']
                    elif repair.get('kind') == 'auto-after-first-check-failure':
                        command = [sys.executable, '-B', str(YARD / '_tools/repair_blocked_room.py'), sub,
                                   '--attempt', repair['attempt']]
                    else:
                        command = [sys.executable, '-B', str(YARD / '_tools/continue_yard_room.py'), sub,
                                   '--attempt', repair['attempt'], '--retry-note', repair['retry_note']]
                    repair.update({'status': 'running', 'started_utc': now()})
                    event('repair-started', sub, items=count, attempt=repair['attempt'])
                else:
                    count, sub = ready.pop(0)
                    command = [sys.executable, '-B', str(YARD / '_tools/start_yard_lead.py'), sub, '--complete']
                log_path = root / 'logs' / (sub + '-' + str(time.time_ns()) + '.log')
                # Persist intent before process creation; existing room/store guards also prevent duplicate starts.
                state['active'][sub] = {'items': count, 'log': str(log_path), 'launch_intent_utc': now(),
                                        'repair': bool(repair),
                                        'attempt': repair.get('attempt') if repair else '',
                                        'model': state['model'], 'effort': state['effort']}
                save()
                with log_path.open('w') as log:
                    child = subprocess.Popen(command,
                                             env=env, stdin=subprocess.DEVNULL,
                                             stdout=log, stderr=subprocess.STDOUT,
                                             start_new_session=True, close_fds=True)
                children[sub] = child
                state['active'][sub].update({'pids': [child.pid], 'started_utc': now(),
                                             'model': state['model'], 'effort': state['effort']})
                event('started', sub, items=count, pid=child.pid, log=str(log_path),
                      model=state['model'], effort=state['effort'])
                save()
                changed = True
                launch_reserve += per_launch
            state['ready_count'] = len(ready)
            save()
            if changed:
                with (root / 'progress-update.log').open('a') as log:
                    result = subprocess.run([sys.executable, '-B', str(YARD / '_tools/update_coding_progress.py')], env=env,
                                            stdin=subprocess.DEVNULL,
                                            stdout=log, stderr=subprocess.STDOUT)
                if result.returncode:
                    event('progress-document-error', returncode=result.returncode)
                # Workers archive after the run check. Rebuild the ledger here,
                # after reconciliation, so archive paths and hashes are current.
                with (root / 'status-update.log').open('a') as log:
                    result = subprocess.run([sys.executable, '-B', str(YARD / '_tools/status.py'),
                                             '--yard', str(YARD), '--no-refresh'], env=env,
                                            stdin=subprocess.DEVNULL,
                                            stdout=log, stderr=subprocess.STDOUT)
                if result.returncode:
                    event('status-document-error', returncode=result.returncode)
            if not state['active']:
                state['status'] = 'drained' if drain_path.exists() else ('paused' if state.get('launch_pause') else 'idle-no-ready-rooms')
                event('queue-idle', failed=list(state['failed']))
                save()
                return
            time.sleep(20)
    except BaseException as exc:
        state.update({'status': 'scheduler-stopped', 'stop_reason': str(exc)})
        save()
        raise


if __name__ == '__main__':
    main()
