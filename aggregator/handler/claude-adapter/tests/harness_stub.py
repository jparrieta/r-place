#!/usr/bin/env python3
"""A stand-in for the run's step.sh and close.sh, for the adapter's and the driver's offline tests only.

It keeps what the adapter and the driver rely on, and builds what a real close builds, with the run's own
protocol_guard.py (beside this file in the synthetic run's CONTROL/harness/):
- both run under the run's lock (protocol_guard.py locked), so neither runs while a leg's turn holds it;
- step:  refuses a leg the analyst closed (out/_closes/NN-LEG.closed) unless --reopen, and anything when
         CONTROL/refuse-step holds a reason; a leg of another pending launch is refused; the first leg of a
         stage is "handed"; .stage, .leg and .session are written and .pause removed; the leg continues the
         last committed close (RUN.json lineage.resume_session, as step.sh v40); prepare() runs; the first
         message names answers newer than the last close.
- step:  delivers DROPS/NN into the analyst's folder at a stage's first leg;
- close: calls the run's publish.sh, when it has one, with close.sh's kind (close, interview-point, pause, finished);
- close: refuses a committed label and an unclosed leg without --force; a pause cut forces; confirm and
         preclose are the harness's own; the snapshot is complete: fs.tar.gz, fs.sha256, agent.tar.gz,
         agent-files.sha256, transcript.jsonl (capture), validation.json, validation-report.txt,
         instrument.tar.gz (close.sh's list), cost.json, checkpoint.json with close.sh's fields, MANIFEST.sha256 over all of
         them, verify_checkpoint, COMMITTED last; INDEX.tsv; the stage FINISHED when handback-NN.md exists and
         the validation is complete; and close.sh's lines (interview point, paused and the leg to resume with,
         open questions, the dispatch, the stage finished, the git line).
- close: after the capture, writes the leg's tokens into the analyst's RUN.json, when it lists the leg (close.sh 4b).
What it leaves out: the snap, the recall probe and the Manual.
    python3 harness_stub.py step LEG [--prepare] [--reopen]
    python3 harness_stub.py close [NN] LEG [--force]
"""
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE.parents[1]
C, AG = RUN / 'CONTROL', RUN / '00_GIVE-THE-AGENT'
_spec = importlib.util.spec_from_file_location('stub_guard', HERE / 'protocol_guard.py')
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def refuse(text):
    sys.stderr.write('REFUSING: ' + text + '\n')
    sys.exit(1)


def events():
    p = C / 'handover-events.log'
    return p.read_text() if p.exists() else ''


def event(*fields):
    with (C / 'handover-events.log').open('a') as f:
        f.write('\t'.join((utc(),) + fields) + '\n')


def parse(argv):
    flags = [a for a in argv if a.startswith('--')]
    pos = [a for a in argv if not a.startswith('--')]
    leg = pos[1] if len(pos) > 1 else pos[0]
    return leg[:2], leg, '%s.%s' % (leg[:2], leg), flags


def last_close():
    p = C / 'snapshots/INDEX.tsv'
    rows = [r.split('\t') for r in p.read_text().splitlines()[1:] if r.strip()] if p.exists() else []
    rows = [r for r in rows if len(r) > 9 and r[9] == 'agent-and-files']
    return rows[-1] if rows else None


def step(argv):
    nn, leg, label, flags = parse(argv)
    if (C / 'refuse-step').exists():
        refuse((C / 'refuse-step').read_text().strip())
    if (AG / 'out/_closes' / ('%s-%s.closed' % (nn, leg))).exists() and '--reopen' not in flags:
        refuse('leg %s is already closed (out/_closes/%s-%s.closed).' % (leg, nn, leg))
    if not G.confirm(RUN):
        p = G.read(C / 'pending_launch.json', {})
        if p.get('label') != label:
            refuse("Another leg's launch is still pending.")
    if '\thanded\t%s\t' % nn not in events():
        if (RUN / 'DROPS' / nn).is_dir():   # the stage's drop, delivered at its first leg, as step.sh does
            shutil.copytree(RUN / 'DROPS' / nn, AG, dirs_exist_ok=True)
        event('handed', nn, 'STAGE-%s.md' % nn)
    (AG / '.pause').unlink(missing_ok=True)
    (AG / '.stage').write_text(nn + '\n')
    (AG / '.leg').write_text(leg + '\n')
    sessions = G.read(C / 'sessions.json', {})
    if label not in sessions and not (C / 'pending_launch.json').exists():
        last = last_close()
        if last and (C / 'snapshots' / last[0] / 'COMMITTED').exists() and (sessions.get(last[0]) or {}).get('session_id'):
            r = G.read(C / 'RUN.json', {})
            r.setdefault('lineage', {})['resume_session'] = sessions[last[0]]['session_id']
            G.write(C / 'RUN.json', r)
            print('Continuing from the last close, %s (its conversation and this folder).' % last[0])
    answers = ''
    closes = sorted((AG / 'out/_closes').glob('*.closed'), key=lambda p: p.stat().st_mtime) if (AG / 'out/_closes').exists() else []
    for f in sorted((AG / 'out/_answers').glob('*.md')) if (AG / 'out/_answers').exists() else []:
        if not closes or f.stat().st_mtime > closes[-1].stat().st_mtime:
            answers += ' ' + f.stem
    msg = ('Stage %s, leg %s. Orient before you write, do this leg\'s work, and close the leg with '
           '`bash tools/done.sh %s`. Then stop.' % (nn, leg, nn))
    if answers:
        msg += ' The principal investigator answered your questions%s.' % answers
    (C / 'next_prompt.txt').write_text(msg + '\n')
    G.prepare(RUN, label, 'fake-cli')
    (AG / '.session').write_text(G.read(C / 'pending_launch.json')['requested_session_id'] + '\n')
    print('Stage %s, leg %s, model %s.' % (nn, leg, G.arm_for(RUN, label)[0]))
    print('Prepared')


def close(argv):
    nn, leg, label, flags = parse(argv)
    force = '--force' in flags
    d = C / 'snapshots' / label
    if (d / 'COMMITTED').exists():
        refuse('%s is committed. A leg is checkpointed once.' % d)
    with (C / 'close-calls.log').open('a') as f:
        f.write('close %s\n' % ' '.join(argv))
    missing = []
    if '\thanded\t%s\t' % nn not in events():
        missing.append('not-handed')
    marker = AG / 'out/_closes' / ('%s-%s.closed' % (nn, leg))
    cut = ''
    if marker.exists():
        rows = [x.split() for x in marker.read_text().splitlines() if x.strip()]
        cut = rows[-1][1] if rows and len(rows[-1]) > 1 else ''
    else:
        missing.append('analyst-did-not-close')
    paused = cut == 'pause'
    force = force or paused
    if missing and not force:
        refuse('%s is not closable: %s.' % (label, ' '.join(missing)))
    if not G.confirm(RUN):
        refuse('the launch for this run is unconfirmed (above).')
    try:
        G.preclose(RUN, label, force, False)
    except ValueError as e:
        refuse(str(e))
    sid = (G.read(C / 'sessions.json', {}).get(label) or {}).get('session_id')
    if not sid:
        refuse('no confirmed session for %s in CONTROL/sessions.json.' % label)
    t = G.transcript(RUN, sid)
    data = t.read_bytes()
    tsha = hashlib.sha256(data).hexdigest()
    rows = [json.loads(x) for x in data.decode().splitlines() if x.strip()]
    if not any(r.get('type') == 'assistant' for r in rows):
        refuse('transcript %s carries no assistant turn.' % sid)
    tmp = C / 'snapshots' / ('.tmp-%s-%d' % (label, os.getpid()))
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    G.capture(RUN, tmp, sid, tsha)
    shutil.copy(C / ('validation-%s.txt' % label), tmp / 'validation-report.txt')
    shutil.copy(C / ('close-status-%s.json' % label), tmp / 'validation.json')
    with tarfile.open(tmp / 'instrument.tar.gz', 'w:gz') as tar:   # what close.sh archives, as it stood
        for n in ('DROPS', 'CONTROL/harness', 'CONTROL/RUN.json', 'CONTROL/arm.json', 'CONTROL/settings.template.json',
                  'CONTROL/sessions.json', 'CONTROL/active_blocks.json', 'CONTROL/handover-events.log'):
            if (RUN / n).exists():
                tar.add(RUN / n, arcname=n)
    models = {}
    for r in rows:
        m = r.get('message') or {}
        if r.get('type') == 'assistant' and m.get('model'):
            models[m['model']] = models.get(m['model'], 0) + 1
    G.write(tmp / 'cost.json', {'main': {'input_tokens': 0, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0,
                                         'output_tokens': 0, 'models': models}, 'subagents': {}})
    r = G.read(AG / 'RUN.json', {})   # the leg's tokens into the analyst's RUN.json, after the capture, as close.sh does
    for e in reversed(r.get('legs', [])):
        if e.get('stage') == nn and e.get('leg') == leg:
            e['tokens'] = {'input_tokens': 7, 'output_tokens': 3}
            (AG / 'RUN.json').write_text(json.dumps(r, indent=1))
            break
    want = G.arm_for(RUN, label)[0]
    bad = [m for m in models if not m.startswith(want) and m != '<synthetic>']
    print('  model audit: arm %s, served %s' % (want, ', '.join(sorted(models)) or 'none'))
    if bad and not force:
        shutil.rmtree(tmp)
        refuse("the leg's transcript names a model the arm does not (%s). Nothing published." % want)
    fsfp = G.digest(tmp / 'fs.sha256')
    ckid = hashlib.sha256('|'.join((json.dumps(G.read(C / 'arm.json', {}).get(nn)), label, fsfp, tsha)).encode()).hexdigest()[:16]
    status = G.read(C / ('close-status-%s.json' % label))
    last = last_close()
    G.write(tmp / 'checkpoint.json', {
        'checkpoint_id': ckid, 'label': label, 'stage': nn, 'stage_file': 'STAGE-%s.md' % nn, 'kind': 'agent-and-files',
        'parent_label': last[0] if last else None,
        'session': {'session_id': sid, 'transcript_sha256': tsha, 'boundary_line': len(data.splitlines()),
                    'boundary_verified': bool(status.get('completed_turn'))},
        'subject': 'aggregator', 'filesystem_root': '00_GIVE-THE-AGENT', 'handler_conversation_included': False,
        'validation': dict(status, handed='not-handed' not in missing,
                           handback_present=(AG / 'out' / ('handback-%s.md' % nn)).exists()),
        'forced': (' '.join(missing) or 'no reason recorded') if force else None, 'published_utc': utc()})
    lines = []
    for p in sorted(x for x in tmp.rglob('*') if x.is_file() and x.name != 'MANIFEST.sha256'):
        lines.append('%s  %s' % (G.digest(p), p.relative_to(tmp).as_posix()))
    (tmp / 'MANIFEST.sha256').write_text('\n'.join(lines) + '\n')
    G.verify_checkpoint(tmp)
    os.replace(tmp, d)
    (d / 'COMMITTED').write_text(ckid + '\n')
    index = C / 'snapshots/INDEX.tsv'
    if not index.exists():
        index.write_text('label\tstage_file\tclosed_utc\tsession_id\tout_files\tfs_manifest_sha256\ttokens_in\t'
                         'transcript_lines\ttokens_out\tkind\tcheckpoint_id\n')
    with index.open('a') as f:
        f.write('\t'.join((label, 'STAGE-%s.md' % nn, utc(), sid, '0', fsfp, '0', str(len(data.splitlines())), '0',
                           'agent-and-files', ckid)) + '\n')
    event('closed', label, 'STAGE-%s.md' % nn)
    print('checkpoint %s  (%s)' % (label, ckid))
    if missing and force:
        print('  FORCED with: ' + ' '.join(missing))
    if cut == 'interview':
        print('  INTERVIEW POINT (%s). Talk with the analyst in a read-only fork: bash CONTROL/harness/interview.sh %s' % (leg, leg))
    if paused:
        nxt = leg.rsplit('-p', 1)[0] + '-p%d' % (int(leg.rsplit('-p', 1)[1]) + 1) if '-p' in leg else leg + '-p2'
        (C / 'stage-state' / nn).mkdir(parents=True, exist_ok=True)
        print('  paused at a safe stop. Resume when you are ready: bash CONTROL/harness/step.sh ' + nxt)
    print('  at           ' + str(d.relative_to(RUN)))
    asks = AG / 'out/asks.jsonl'
    if asks.exists():
        open_q = [json.loads(x) for x in asks.read_text().splitlines() if x.strip()]
        open_q = [q for q in open_q if not (AG / 'out/_answers' / ('%s.md' % q.get('id'))).exists()]
        if open_q:
            print('  QUESTIONS    the analyst asked, not yet answered (answer in out/_answers/<id>.md):')
            for q in open_q:
                print('               %s (%s): %s' % (q.get('id'), q.get('leg'), q.get('question')))
    if cut == 'packets-out':
        print('  next         the dispatch, outside the analyst:  bash "CONTROL/harness/dispatch.sh" ' + nn)
    if (AG / 'out' / ('handback-%s.md' % nn)).exists() and status.get('complete') is True and not force:
        (C / 'stage-state' / nn).mkdir(parents=True, exist_ok=True)
        (C / 'stage-state' / nn / 'FINISHED').write_text('%s\t%s\n' % (utc(), label))
        print('  stage %s    finished (handback-%s.md written, validation clean)' % (nn, nn))
    kind = 'close'
    if cut == 'interview':
        kind = 'interview-point'
    if paused:
        kind = 'pause'
    fin = C / 'stage-state' / nn / 'FINISHED'
    if fin.is_file() and fin.read_text().strip().endswith('\t' + label):
        kind = 'finished'
    if (C / 'harness/publish.sh').is_file():   # the run's publish.sh, as close.sh calls it
        import subprocess
        r = subprocess.run(['bash', str(C / 'harness/publish.sh'), label, kind], capture_output=True, text=True, check=False)
        sys.stdout.write(r.stdout + r.stderr)
    else:
        print('  git: the run is not in a repository; nothing committed')


if __name__ == '__main__':
    # under the run's lock, as step.sh and close.sh run (protocol_guard.py locked): a turn holds it, so a step or a
    # close while any leg's turn runs is refused, as in the real harness
    if os.environ.get('AGGREGATOR_LOCK_RUN') != str(RUN.resolve()):
        try:
            sys.exit(G.locked(RUN, [sys.executable, str(Path(__file__).resolve())] + sys.argv[1:]))
        except ValueError as e:
            refuse(str(e))
    {'step': step, 'close': close}[sys.argv[1]](sys.argv[2:])
