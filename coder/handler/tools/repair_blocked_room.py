#!/usr/bin/env python3
"""Repair one blocked room from a clean, forked case-lead boundary."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

YARD = Path(__file__).resolve().parents[1]
TOOLS = YARD / '_tools'
sys.path.insert(0, str(TOOLS))
import room
from lead_archive import archive_one, restore_one


def run(args, **kwargs):
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
    return subprocess.run([sys.executable, '-B', *map(str, args)], env=env,
                          check=True, **kwargs)


def classify(status, detail=''):
    batch = re.search(r'batch-(\d+)-check\.txt', status)
    if not batch:
        batch = re.search(r"--batch', '(\d+)'", status)
    if batch:
        number = int(batch.group(1))
        return 'coder', ('lead-first' if number == 1 else 'collected-%02d' % (number - 1))
    if 'run-check.txt' in status:
        contaminated = [int(n) for n in re.findall(r'close_run fleet (\d+): FAIL', detail)]
        if contaminated:
            number = min(contaminated)
            return 'coder', ('lead-first' if number == 1 else 'collected-%02d' % (number - 1))
        return 'lead', 'after-fleet'
    return 'fresh-lead', None


def state_note(source, status, note=None, **fields):
    state = room.load_state(str(source))
    state['coding_status'] = status
    state.update(fields)
    if note:
        state.setdefault('notes', []).append({'at': room.now(), 'note': note})
    room.save_state(str(source), state)


def failure_detail(status):
    if not status.startswith('blocked: '):
        return status
    match = re.search(r'retained at (/.+?\.txt)$', status)
    if not match:
        return status[len('blocked: '):]
    path = Path(match.group(1))
    if not path.is_file():
        return status[len('blocked: '):]
    text = path.read_text(errors='replace')
    failed = text.find('FAILED')
    return text[failed if failed >= 0 else 0:][-6000:]


def resolve_checkpoint(store, requested):
    direct = store / 'refs' / (requested + '.json')
    if direct.is_file():
        return requested
    matches = sorted((store / 'refs').glob(requested + '-*.json'),
                     key=lambda path: path.stat().st_mtime)
    if not matches:
        raise RuntimeError('No clean checkpoint matching ' + requested)
    return matches[-1].stem


def latest_repair_log(sub, exclude_attempt=None):
    logs = sorted((path for path in (YARD / '_repair_queue' / 'logs').glob(sub + '-repair-*.log')
                   if path.name != sub + '-' + str(exclude_attempt) + '.log'),
                  key=lambda path: path.stat().st_mtime_ns, reverse=True)
    for path in logs:
        text = path.read_text(errors='replace')
        if text.strip():
            return text[-12000:]
    return ''


def preserve_unverified_run(source, state, attempt):
    current = source / 'run'
    if not current.exists():
        return None
    receipt = source / 'validation' / 'RUN-RECEIPT.json'
    if state.get('coding_status') == 'verified' or state.get('verified_utc') or receipt.is_file():
        raise RuntimeError('Canonical source run is verified; refusing to replace or move it.')
    target = source / ('_failed_run_' + attempt + '-' + str(time.time_ns()))
    if target.exists():
        raise RuntimeError('Unique failed-run preservation path already exists: ' + str(target))
    current.rename(target)
    updated = room.load_state(str(source))
    updated.setdefault('failed_run_history', []).append({
        'path': str(target), 'preserved_utc': room.now(), 'attempt': attempt,
    })
    room.save_state(str(source), updated)
    return target


def preserve_old_archive(sub, archive, source):
    stamp = str(time.time_ns())
    old = archive.with_name(archive.name[:-len('.tar.zst')] + '-superseded-' + stamp + '.tar.zst')
    state = room.load_state(str(source))
    state.setdefault('lead_archive_history', []).append({
        'path': str(old), 'sha256': state.get('lead_archive_sha256'),
        'bytes': state.get('lead_archive_bytes'), 'superseded_utc': room.now(),
    })
    archive.rename(old)
    state.pop('lead_archive', None)
    state.pop('lead_archive_sha256', None)
    state.pop('lead_archive_bytes', None)
    room.save_state(str(source), state)
    return old


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('subreddit')
    parser.add_argument('--attempt', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_]+', args.subreddit):
        raise SystemExit('Invalid subreddit.')
    if not re.fullmatch(r'[A-Za-z0-9-]+', args.attempt):
        raise SystemExit('Invalid attempt.')
    sub = args.subreddit
    source = YARD / 'rooms' / sub
    state = room.load_state(str(source))
    old_status = str(state.get('coding_status', ''))
    restart_statuses = {
        'repair fresh lead starting', 'repair case lead forking',
        'repair coder restarting', 'repair lead correction running',
        'repair interrupted work resuming',
    }
    if not old_status.startswith('blocked:') and old_status not in restart_statuses:
        raise SystemExit('Room is not blocked: ' + old_status)
    store = YARD / '_lead_sessions' / (sub + '-gpt56-calibration-v1')
    archive = store.with_name(store.name + '.tar.zst')
    had_archive_at_start = archive.exists()
    strategy = checkpoint = None
    note = old_status[len('blocked: '):] if old_status.startswith('blocked:') else old_status
    primary_error = None
    try:
        if archive.exists():
            restore_one(sub)
        note = failure_detail(old_status)
        strategy, checkpoint = classify(old_status, note)
        repair_log = latest_repair_log(sub, args.attempt)
        queue_state = json.loads((YARD / '_coding_queue' / 'STATE.json').read_text())
        failed_log = Path(queue_state.get('failed', {}).get(sub, {}).get('log', ''))
        failed_text = failed_log.read_text(errors='replace') if failed_log.is_file() else ''
        if ('serverOverloaded' in failed_text or
                'Selected model is at capacity' in failed_text):
            # The failed native turn may have changed thread history. Resume
            # from the last completed checkpoint, not the rejected turn.
            interrupted = old_status + '\n' + failed_text
            match = re.search(r"--batch', '(\d+)'", interrupted)
            if "--message', 'collect'" in interrupted and match:
                batch_number = int(match.group(1))
                strategy = 'coder'
                checkpoint = ('lead-first' if batch_number == 1 else
                              'collected-%02d' % (batch_number - 1))
            elif "--message', 'finish'" in interrupted:
                strategy, checkpoint = 'lead', 'after-fleet'
        if ("FAILED: Command " in repair_log and
                "room.py', 'message'" in repair_log):
            strategy, checkpoint = 'resume', None
        if 'Batch manifest model differs from --model' in repair_log:
            strategy, checkpoint = 'redispatch', 'lead-first'
        hints_path = YARD / '_repair_queue' / 'HINTS.json'
        hints = json.loads(hints_path.read_text()) if hints_path.exists() else {}
        user_stopped_path = YARD / '_coding_queue' / 'USER-STOPPED.json'
        user_stopped = (json.loads(user_stopped_path.read_text())
                        if user_stopped_path.exists() else {})
        user_pause = sub in user_stopped and old_status.startswith('blocked: user requested stop')
        hint = hints.get(sub, {}) if sub not in user_stopped or user_pause else {}
        strategy = hint.get('strategy', strategy)
        checkpoint = hint.get('checkpoint', checkpoint)
        if hint.get('note'):
            note = note.rstrip() + '\n\nScheduler diagnosis: ' + hint['note'].strip()
        if ('invalid paginated history lineage' in repair_log or
                'missing source rollout' in repair_log or
                'invalid paginated history lineage' in note or
                'missing source rollout' in note):
            strategy, checkpoint = 'fresh-lead', None
            note = note.rstrip() + (
                '\n\nScheduler diagnosis: the moved case-lead store cannot fork because '
                'its native history references a missing source rollout. Start a fresh '
                'case lead from the contract and preserve the broken store archive.')
        archive_marker_path = store / 'ARCHIVE.json'
        archive_marker = (json.loads(archive_marker_path.read_text())
                          if archive_marker_path.is_file() else {})
        moved_archive = (had_archive_at_start and
                         archive_marker.get('restore_tool') != str(TOOLS / 'lead_archive.py'))
        if (moved_archive and strategy in ('coder', 'lead', 'redispatch')
                and not user_pause):
            strategy, checkpoint = 'fresh-lead', None
            note = note.rstrip() + (
                '\n\nScheduler diagnosis: this repair began from an archive moved from the '
                'old yard. Native fork lineage has not been reliable after the move, so start '
                'a fresh case lead from the contract and preserve the old archive.')
        if strategy == 'fresh-lead':
            preserved = preserve_unverified_run(source, state, args.attempt)
            if store.is_dir():
                archive_one(sub)
                preserve_old_archive(sub, archive, source)
            state_note(source, 'repair fresh lead starting',
                       'No narrow safe checkpoint repair was identified; starting a new case lead from the contract.' +
                       ((' Preserved the unverified source run at ' + str(preserved) + '.') if preserved else ''))
            run([TOOLS / 'start_yard_lead.py', sub, '--complete'])
            return

        if strategy == 'resume':
            if (store / 'RUNNING.json').exists():
                run([TOOLS / 'codex_lead.py', '--store', store, 'recover-run'])
            state_note(source, 'repair interrupted work resuming',
                       'The prior attempt stopped before a lead checkpoint; resuming its intact saved lead and checked coder files.')
            run([TOOLS / 'continue_yard_room.py', sub, '--attempt', args.attempt,
                 '--retry-note', note])
            return

        state_note(source, 'repair case lead forking',
                   'Forking clean checkpoint %s for %s repair: %s' % (checkpoint, strategy, note))
        try:
            checkpoint = resolve_checkpoint(store, checkpoint)
        except RuntimeError as exc:
            if not str(exc).startswith('No clean checkpoint matching '):
                raise
            preserved = preserve_unverified_run(source, state, args.attempt)
            if store.is_dir():
                archive_one(sub)
                preserve_old_archive(sub, archive, source)
            state_note(source, 'repair fresh lead starting',
                       'The requested clean checkpoint does not exist. Preserved the failed store and restarted the whole room from the contract.' +
                       ((' Preserved the unverified source run at ' + str(preserved) + '.') if preserved else ''))
            run([TOOLS / 'start_yard_lead.py', sub, '--complete'])
            return
        run([TOOLS / 'codex_lead.py', '--store', store, 'verify', '--checkpoint', checkpoint])
        run([TOOLS / 'codex_lead.py', '--store', store, 'fork',
             '--checkpoint', checkpoint, '--name', args.attempt])
        if strategy == 'redispatch':
            state_note(source, 'repair coder restarting',
                       'Forked immutable lead-first and cleanly redispatching its mismatched batch manifest.')
            managed_run = store / 'workspace/room/run'
            run([managed_run / 'tools/fleet.py', 'redispatch', '--batch', '01',
                 '--model', 'gpt-5.6-sol'], cwd=managed_run)
            run([TOOLS / 'continue_yard_room.py', sub, '--attempt', args.attempt,
                 '--retry-note', note])
            return
        if strategy == 'coder':
            state_note(source, 'repair coder restarting',
                       'Fresh case lead fork created; rerunning the failed coder slice from its clean dispatch boundary.')
            run([TOOLS / 'continue_yard_room.py', sub, '--attempt', args.attempt,
                 '--retry-note', note])
            return

        managed = store / 'workspace/room'
        gate = json.loads((managed / 'run/out/_gate.json').read_text())
        batch = len(gate.get('slices', []))
        base = subprocess.check_output(
            [sys.executable, '-B', str(TOOLS / 'room.py'), 'message', 'finish',
             '--room', str(managed), '--batch', str(batch)], text=True,
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        prompt = store / 'state' / ('repair-' + args.attempt + '.txt')
        prompt.write_text(base.rstrip() + '\n\nREPAIR TURN\nOpen and follow CONTRACT-case-lead.md and CONTRACT.md. '
                          'The prior consolidation failed this exact mechanical check:\n' + note + '\n'
                          'Work from this clean after-fleet fork. Inspect the relevant evidence and use the room tools. '
                          'Correct the cited defect without weakening the contract, then complete the case lead output.\n')
        state_note(source, 'repair lead correction running',
                   'Fresh case lead fork is correcting the preserved run-check defect.')
        run([TOOLS / 'codex_lead.py', '--store', store, 'turn', '--prompt-file', prompt,
             '--label', 'lead-closed-' + args.attempt])
        run([TOOLS / 'continue_yard_room.py', sub, '--attempt', args.attempt,
             '--retry-note', note])
    except BaseException as exc:
        primary_error = exc
        state_note(source, 'blocked: ' + str(exc), repair_attempt=args.attempt)
        raise
    finally:
        if store.is_dir() and not (store / 'RUNNING.json').exists():
            try:
                archive_one(sub)
            except Exception as exc:
                print('WARNING: repair store remained unpacked: ' + str(exc), file=sys.stderr)
                state_note(source, 'blocked: archive failed after ended repair: ' + str(exc),
                           repair_attempt=args.attempt)
                if primary_error is None:
                    raise


if __name__ == '__main__':
    main()
