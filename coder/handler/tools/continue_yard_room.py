"""Run the serial fleet cycle, verify, and publish one authorised yard reading."""
import argparse
import collections
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
WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(YARD / '_tools'))
import room
from lead_archive import restore_one
from checkpoints import locked

p = argparse.ArgumentParser()
p.add_argument('sub')
p.add_argument('--attempt', default='', help='Unique retry suffix for immutable checkpoints')
p.add_argument('--retry-note')
a = p.parse_args()
if not re.fullmatch(r'[A-Za-z0-9_]+', a.sub):
    raise SystemExit('Invalid room name.')
if a.attempt and not re.fullmatch(r'[A-Za-z0-9-]+', a.attempt):
    raise SystemExit('Invalid attempt label.')
suffix = ('-' + a.attempt) if a.attempt else ''
after_fleet_label = 'after-fleet' + suffix
closed_label = 'lead-closed' + suffix
store = YARD / '_lead_sessions' / (a.sub + '-gpt56-calibration-v1')
if not store.exists() and store.with_name(store.name + '.tar.zst').exists():
    restore_one(a.sub)
managed = store / 'workspace/room'
run_dir = managed / 'run'
source = YARD / 'rooms' / a.sub
descriptor = json.loads((store / 'STORE.json').read_text())
if descriptor['source_room'] != str(source) or descriptor['model'] != 'gpt-5.6-sol':
    raise SystemExit('Room or model differs from the authorised store.')
effort = descriptor.get('effort')
if effort not in ('medium', 'xhigh'):
    raise SystemExit('Store effort differs from an authorised worker setting.')
audit = store / 'audit' / ('scheduler-' + str(time.time_ns()))
audit.mkdir(parents=True)
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}

def read_json(path):
    return json.loads(Path(path).read_text())

def rows(path):
    path = Path(path)
    if not path.exists():
        return []
    parsed = []
    rejected = []
    for number, line in enumerate(path.read_text(errors='replace').splitlines(), 1):
        if not line.strip():
            continue
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError as exc:
            rejected.append(f'{path}:{number}: {exc}')
    if rejected:
        with (audit / 'jsonl-parse-warnings.txt').open('a') as warning:
            warning.write('\n'.join(rejected) + '\n')
    return parsed

def invoke(args, log=None):
    cmd = [sys.executable, '-B', *map(str, args)]
    if log:
        r = subprocess.run(cmd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (audit / log).write_text(r.stdout)
        print(r.stdout[-6000:], flush=True)
        if r.returncode:
            raise RuntimeError('Check failed; retained at ' + str(audit / log))
        return r.stdout
    subprocess.run(cmd, env=env, check=True)

def captured(args, log):
    """Run a check without ending the lead workflow on a correctable failure."""
    cmd = [sys.executable, '-B', *map(str, args)]
    result = subprocess.run(cmd, env=env, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    path = audit / log
    path.write_text(result.stdout)
    print(result.stdout[-6000:], flush=True)
    return result, path

def state_note(status, **fields):
    st = room.load_state(str(source))
    st['coding_status'] = status
    st.update(fields)
    room.save_state(str(source), st)

def usage_from(path):
    native = None
    cli = []
    for row in rows(path):
        if row.get('type') == 'event_msg' and row.get('payload', {}).get('type') == 'token_count':
            info = row['payload'].get('info') or {}
            if info.get('total_token_usage'):
                native = info['total_token_usage']
        if row.get('type') == 'turn.completed' and row.get('usage'):
            cli.append(row['usage'])
    if native:
        return native
    if cli:
        values = {k: sum(x.get(k, 0) for x in cli) for k in ['input_tokens', 'cached_input_tokens', 'output_tokens']}
        values['total_tokens'] = values['input_tokens'] + values['output_tokens']
        return values
    return None

try:
    if (store / 'RUNNING.json').exists():
        raise RuntimeError('Lead is not idle; wait for its first command to exit.')
    if not (store / 'state/lead.json').exists():
        raise RuntimeError('No completed lead turn.')
    gate = read_json(run_dir / 'out/_gate.json')
    stats = read_json(source / 'record/cut_stats.json')
    if gate.get('threshold') != 500:
        raise RuntimeError('Gate departed from 500; report before running a coder.')
    if abs(gate['items_in_window'] - stats['items_in_window']) > stats['items_in_window'] * .1:
        raise RuntimeError('Gate and room counts disagree by more than a tenth.')
    if gate['branch'] == 'B':
        while not gate.get('consolidated_utc'):
            coders = gate.get('coders', [])
            pending = [c for c in coders if not c.get('collected_utc')]
            if not pending:
                if len(coders) != len(gate['slices']):
                    raise RuntimeError('Expected next dispatched batch is missing.')
                break
            if len(pending) != 1:
                raise RuntimeError('Exactly one uncollected coder is required.')
            nn = '%02d' % int(pending[0]['batch'])
            batch = run_dir / 'fleet' / ('batch_' + nn)
            state_note('coder ' + nn + ' running')
            coder_args = [WORK / 'codex_coder.py', '--room', managed, '--batch', nn,
                          '--model', 'gpt-5.6-sol', '--effort', effort]
            if a.retry_note:
                coder_args += ['--retry-note', a.retry_note]
            # A scheduler failure after the coder exited must not run that coder twice.
            transcript = batch / 'out/_transcript.jsonl'
            final_message = batch / 'out/final_message.md'
            if not (transcript.is_file() and transcript.stat().st_size and final_message.is_file()):
                invoke(coder_args)
            summary = invoke([YARD / '_tools/room.py', 'check', '--room', managed, '--batch', nn], 'batch-' + nn + '-check.txt').strip()
            final_batch = int(nn) == len(gate['slices'])
            label = after_fleet_label if final_batch else 'collected-' + nn + suffix
            state_note('lead collecting ' + nn)
            invoke([YARD / '_tools/codex_lead.py', '--store', store, 'turn', '--message', 'collect',
                    '--batch', nn, '--summary', summary, '--label', label])
            gate = read_json(run_dir / 'out/_gate.json')
            if final_batch and gate.get('consolidated_utc'):
                raise RuntimeError('Last collection consolidated before the saved fork point.')
        if not gate.get('consolidated_utc'):
            if not (store / ('refs/' + after_fleet_label + '.json')).is_file():
                # A new attempt label does not invalidate an existing clean completed
                # after-fleet turn. Verify HEAD before continuing from that exact state.
                candidates = list((store / 'refs').glob('after-fleet*.json'))
                if not candidates:
                    raise RuntimeError('Missing after-fleet checkpoint.')
                verified = json.loads(invoke([YARD / '_tools/codex_lead.py', '--store', store,
                                              'verify'], 'resumed-head-check.txt'))
                if verified.get('live_files_match') is not True:
                    raise RuntimeError('Resumed after-fleet files differ from HEAD.')
            state_note('lead consolidation running')
            invoke([YARD / '_tools/codex_lead.py', '--store', store, 'turn', '--message', 'finish',
                    '--batch', len(gate['slices']), '--label', closed_label])

    # Keep the original case lead available after its finish turn. Most final
    # contract failures are small output defects that the same lead can repair
    # more reliably and cheaply than a new repair lead. Only archive after this
    # loop passes or exhausts its bounded correction attempts.
    max_close_corrections = 2
    close_corrections = 0
    while True:
        attempt_number = close_corrections + 1
        checkpoint_name = 'checkpoint-check-attempt-%02d.txt' % attempt_number
        verification_text = invoke(
            [YARD / '_tools/codex_lead.py', '--store', store, 'verify'],
            checkpoint_name)
        checkpoint_verification = json.loads(verification_text)
        if checkpoint_verification.get('live_files_match') is False:
            raise RuntimeError('Checkpoint differs from current files.')

        check_name = 'run-check-attempt-%02d.txt' % attempt_number
        checked, check_path = captured(
            [YARD / '_tools/verify_room.py', '--room', managed], check_name)
        zero_citations = re.search(r'\b0 ids cited\b', checked.stdout)
        if checked.returncode == 0 and not zero_citations:
            shutil.copy2(audit / checkpoint_name, audit / 'checkpoint-check.txt')
            shutil.copy2(check_path, audit / 'run-check.txt')
            check = checked.stdout
            break

        failure_text = checked.stdout
        if zero_citations and checked.returncode == 0:
            failure_text += '\nFAILED: checker found zero case citations.\n'
        if close_corrections >= max_close_corrections:
            raise RuntimeError('Final check still failed after %d same-lead correction turns; retained at %s'
                               % (max_close_corrections, check_path))

        close_corrections += 1
        base = subprocess.check_output(
            [sys.executable, '-B', str(YARD / '_tools/room.py'), 'message',
             'finish', '--room', str(managed), '--batch',
             str(len(gate.get('slices', [])))],
            text=True, env=env)
        prompt_path = store / 'state' / ('close-correction-%02d%s.txt'
                                         % (close_corrections, suffix))
        prompt_path.write_text(
            base.rstrip() + '\n\nCLOSE CORRECTION TURN\n'
            'The final validation failed. Keep the contract unchanged. Inspect '
            'the cited files and evidence, correct every reported defect with the '
            'room tools, rerun the required close checks, and finish the run. Here '
            'is the exact checker output:\n\n' + failure_text + '\n')
        state_note('lead correcting final check %d/%d'
                   % (close_corrections, max_close_corrections),
                   close_correction_attempt=close_corrections,
                   close_correction_check=str(check_path))
        correction_label = 'lead-corrected-%02d%s' % (close_corrections, suffix)
        invoke([YARD / '_tools/codex_lead.py', '--store', store, 'turn',
                '--prompt-file', prompt_path, '--label', correction_label])

    with locked(store):
        if (store / 'RUNNING.json').exists():
            raise RuntimeError('Lead started while publishing.')
        target = source / 'run'
        if target.exists():
            raise RuntimeError('Canonical run already exists; will not overwrite it.')
        staging = source / ('_run_copy_' + str(time.time_ns()))
        shutil.copytree(run_dir, staging, copy_function=shutil.copy2)
        def inventory(path):
            return {str(f.relative_to(path)): hashlib.sha256(f.read_bytes()).hexdigest()
                    for f in path.rglob('*') if f.is_file()}
        original = inventory(run_dir)
        if inventory(staging) != original:
            raise RuntimeError('Run mirror failed byte verification.')
        staging.rename(target)
        validation = source / 'validation'
        validation.mkdir(exist_ok=True)
        for name in ['run-check.txt', 'checkpoint-check.txt']:
            shutil.copy2(audit / name, validation / name)
        shutil.copy2(store / 'state/prompting.json', validation / 'prompting.json')
        shutil.copy2(store / 'state/lead-opening.txt', validation / 'lead-opening.txt')
        shutil.copy2(YARD / 'CASE-LEAD-PROMPT.md', validation / 'CASE-LEAD-PROMPT.md')
        lead = read_json(store / 'state/lead.json')
        usages = {'case-lead': usage_from(run_dir / 'out/_transcript.jsonl')}
        for batch in sorted((run_dir / 'fleet').glob('batch_*')) if (run_dir / 'fleet').exists() else []:
            usages[batch.name] = usage_from(batch / 'out/_transcript.jsonl')
        total = sum(u['total_tokens'] for u in usages.values() if u and 'total_tokens' in u)
        receipt = {'sub': a.sub, 'model': 'gpt-5.6-sol', 'effort': effort,
                   'prompt_version': 'lead-calibration-v1', 'store': str(store),
                   'checkpoint_head': read_json(store / 'HEAD.json'), 'thread_id': lead['thread_id'],
                   'turn_id': lead['turn_id'], 'verified_utc': room.now(),
                   'source_run': str(run_dir), 'copy_kind': 'byte-identical archival run; native continuation uses original store',
                   'files_sha256': original, 'reported_usage_by_agent': usages,
                   'reported_total_tokens': total, 'usage_complete': all(usages.values())}
        (validation / 'RUN-RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
        st = room.refresh(str(source), persist=False)
        st.update({'verified_utc': receipt['verified_utc'], 'finished': lead['ended_utc'],
                   'coding_status': 'verified', 'carried': 'run', 'lead_store': str(store),
                   'lead_model': 'gpt-5.6-sol', 'lead_prompt_version': 'lead-calibration-v1',
                   'reported_total_tokens': total})
        st.setdefault('notes', []).append({'at': room.now(), 'note': 'Verified coding and exact run mirror; native lead checkpoint remains at '+str(store)})
        room.save_state(str(source), st)
    invoke([YARD / '_tools/status.py', '--yard', YARD], 'yard-status.txt')
    print(json.dumps({'subreddit': a.sub, 'status': 'verified', 'reported_tokens': total,
                      'usage_complete': receipt['usage_complete'], 'run': str(source / 'run')}, indent=2), flush=True)
except BaseException as exc:
    state_note('blocked: ' + str(exc), coding_audit=str(audit))
    (audit / 'STOPPED.txt').write_text(str(exc) + '\n')
    raise
finally:
    # A failed coder/check is still an ended attempt. Keep only its compressed,
    # forkable store unless a native lead operation is genuinely still running.
    primary_failure = sys.exc_info()[0] is not None
    if store.is_dir() and not (store / 'RUNNING.json').exists():
        archived = subprocess.run(
            [sys.executable, '-B', str(YARD / '_tools/lead_archive.py'),
             'archive', a.sub], env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(archived.stdout, end='', flush=True)
        if archived.returncode:
            print('WARNING: idle case-lead store could not be archived.', file=sys.stderr)
            state_note('archive failed after ended attempt', archive_error=archived.stdout[-4000:])
            if not primary_failure:
                raise RuntimeError('Verified work finished but its case-lead store could not be archived.')
