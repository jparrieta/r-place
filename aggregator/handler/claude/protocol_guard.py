#!/usr/bin/env python3
"""protocol_guard.py, v38: handler-side guards. Only the analyst's private runtime is a fork subject.

Ported from v37 (_v37-source/harness/protocol_guard.py). What changed for v38:
- A launch is a leg, labelled "NN.leg" (for example "B3.build", "C2.pass-2", "D3.group-1"). Every
  leg opens a fresh session; no stages share a session. A leg reopened from a cut is a fork of the
  cut's checkpoint (RUN.json lineage.resume_session), as in v37.
- The model comes from CONTROL/arm.json for the stage and leg, never from a single RUN.json field.
- The settings are rendered per stage: before stage E1 the analyst is denied out/_probe
  and out/_transcripts by the permission rules and by the sandbox, not only by the stage file.
- The launch passes the leg's startup message as the session's first prompt.
- `probe` runs the recall probe as a fresh headless turn of the leg's session.
"""
import datetime
import fcntl
import hashlib
import json
import os
import re
from pathlib import Path
import stat
import subprocess
import sys
import tarfile
import uuid


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def read(p, default=None):
    return json.loads(Path(p).read_text()) if Path(p).exists() else default


def write(p, value):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + '.tmp-' + str(uuid.uuid4()))
    with tmp.open('w') as f:
        json.dump(value, f, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, p)


def digest(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def head(label):
    return label  # v38: every leg is its own session


def stage_of(label):
    return label.split('.', 1)[0]


def arm_for(run, label):
    """(model, entry) for a leg: arm.json {"NN": {"analyst": ..., "legs": {"leg": {"analyst": ...}}}}."""
    arm = read(Path(run) / 'CONTROL/arm.json', {})
    nn, leg = (label.split('.', 1) + [''])[:2]
    st = arm.get(nn) or {}
    ent = dict(st)
    ent.update((st.get('legs') or {}).get(leg) or {})
    model = ent.get('analyst')
    if not model or model == 'SET-ME':
        raise ValueError('CONTROL/arm.json names no analyst model for stage %s leg %s' % (nn, leg))
    return model, ent


def transcript(run, sid):
    if str(uuid.UUID(sid)) != sid:
        raise ValueError('invalid aggregator session ID')
    return Path(run) / 'CONTROL/.cc/projects/run' / (sid + '.jsonl')


def messages(path):
    if not path.exists():
        return []
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    return [r for r in rows if r.get('type') in ('user', 'assistant')
            and not r.get('isSidechain')]


def message_id(row):
    return row.get('uuid') or hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()


def settings(run, stage=None, ag=None, hooks=True):
    """Render the analyst's settings for its folder: the run's own (ag None), or an interview's copy of a
    checkpoint (ag given), whose settings shut the live folder and every other copy, and carry no hooks,
    since the hooks watch the live run."""
    run = Path(run).resolve()
    ag_dir = Path(ag).resolve() if ag else run / '00_GIVE-THE-AGENT'
    template = read(run / 'CONTROL/settings.template.json')
    replacements = {'__RUN__': str(run), '__AG__': str(ag_dir)}
    def render(v):
        if isinstance(v, str):
            for a, b in replacements.items():
                v = v.replace(a, b)
            return v
        if isinstance(v, list):
            return [render(x) for x in v]
        if isinstance(v, dict):
            return {k: render(x) for k, x in v.items()}
        return v
    s = render(template)
    # Lineage stays with the handler: the run's input, everything beside the run and beside its
    # parent (design notes, sources, older kits), and the places on this machine that hold the
    # project or the coders' records. Siblings are denied one by one; the home folder itself is
    # not, or python and its libraries would go with it.
    shut, cur = [], ag_dir
    while cur != run:                    # every sibling on the way up to the run: the live folder and the
        parent = cur.parent              # other interviews' copies included, when this is a copy
        shut += [p for p in sorted(parent.iterdir()) if p != cur
                 and not (parent == run and p.name in ('CONTROL', 'DROPS', 'STAGE CARDS', 'READ-ME-FIRST.md'))]
        cur = parent
    if (run / 'INPUT') not in shut:
        shut.append(run / 'INPUT')
    # three levels up (restructure 2026-10-02): a run sits in aggregator/runs/<run>, so the levels are
    # runs/ (the other runs), aggregator/ (instrument, handler, the shared input) and the repository
    # root (coder/, data/, orchestrator/, Manual/)
    for base, keep in ((run.parent, run), (run.parent.parent, run.parent), (run.parent.parent.parent, run.parent.parent)):
        if base.exists():
            shut += [p for p in sorted(base.iterdir()) if p != keep and not p.name.startswith('.')]
    # a git repository around the run holds every file's history, _probe/ and _transcripts/ included:
    # its .git is shut wherever it sits
    for anc in (run, run.parent, run.parent.parent, run.parent.parent.parent):
        if (anc / '.git').exists() and (anc / '.git') not in shut:
            shut.append(anc / '.git')
    home = Path.home()
    shut += [home / d for d in ('Obsidian', 'Documents', 'Desktop', 'Downloads', 'Library/Mobile Documents',
                                'Library/CloudStorage', 'Dropbox', 'Google Drive') if (home / d).exists()]
    for p in shut:   # a folder takes /**; a file is named as itself (a /** rule on a file matches nothing)
        s['permissions']['deny'].append(('Read(//%s)' if p.is_file() else 'Read(//%s/**)') % str(p).lstrip('/'))
        s['sandbox']['filesystem']['denyRead'].append(str(p))
    if stage not in ('E1', 'E2'):
        ag = str(ag_dir)
        for d in ('_probe', '_transcripts'):   # snaps hold hashes only; nothing in them to learn
            s['permissions']['deny'].append('Read(//%s/out/%s/**)' % (ag.lstrip('/'), d))
            s['sandbox']['filesystem']['denyRead'].append('%s/out/%s' % (ag, d))
        # allowRead stays empty: the analyst's folder is readable by default, and a deny holds inside it
        s['sandbox']['filesystem']['allowRead'] = [x for x in s['sandbox']['filesystem'].get('allowRead', [])
                                                   if x != ag]
    # the CLI's own per-folder scratchpad (tmp/claude-<uid>/<folder slug> under the system temp root) sits outside the folder; the
    # analyst works there by default, and every touch asked J for permission (J, 2026-10-03). Allow that
    # one folder, this folder's only, and nothing else under /tmp.
    slug = re.sub(r'[^A-Za-z0-9]', '-', str(ag_dir))
    for tmp in ('private/tmp', 'tmp'):
        d = '/%s/claude-%d/%s' % (tmp, os.getuid(), slug)
        if d not in s['permissions'].setdefault('additionalDirectories', []):
            s['permissions']['additionalDirectories'].append(d)
        # v43: the leg runs in dontAsk, so writes there need a rule (the analyst's notes and scripts)
        for tool in ('Edit', 'Write'):
            rule = '%s(/%s/**)' % (tool, d)
            if rule not in s['permissions'].setdefault('allow', []):
                s['permissions']['allow'].append(rule)
    if not hooks:
        s.pop('hooks', None)
    write(ag_dir / '.claude/settings.json', s)
    # transcripts are the run's memory: never let the retention sweep delete them (default 30 days)
    cc = run / 'CONTROL' / '.cc'
    cc.mkdir(parents=True, exist_ok=True)
    up = cc / 'settings.json'
    try:
        u = json.load(open(up)) if up.exists() else {}
    except ValueError:
        u = {}
    if u.get('cleanupPeriodDays') != 36500:
        u['cleanupPeriodDays'] = 36500
        write(up, u)


def seed_trust(run, *extra):
    """Mark the repository, the run and the analyst's folder trusted in the run's own login, so no trust
    dialog stops a leg (v43, J 2026-10-04: a git init above the run made the repository the project
    root, untrusted, and every leg asked). Only a login that exists is touched; the file is rewritten
    whole, through a temporary file, and keeps every other key."""
    run = Path(run).resolve()
    p = run / 'CONTROL' / '.cc' / '.claude.json'
    if not p.exists():
        return
    try:
        cfg = json.load(open(p))
    except ValueError:
        return
    roots = [run, run / '00_GIVE-THE-AGENT'] + [Path(x).resolve() for x in extra]
    for anc in (run.parent, run.parent.parent, run.parent.parent.parent):
        if (anc / '.git').exists():
            roots.append(anc)
    projects = cfg.setdefault('projects', {})
    changed = False
    for r in roots:
        e = projects.setdefault(str(r), {})
        if e.get('hasTrustDialogAccepted') is not True:
            e['hasTrustDialogAccepted'] = True
            changed = True
    if changed:
        tmp = p.with_name('.claude.json.trust-tmp')
        with open(tmp, 'w') as f:
            json.dump(cfg, f, indent=2)
        os.replace(tmp, p)


def prepare(run, label, cli):
    c = Path(run) / 'CONTROL'
    pending = read(c / 'pending_launch.json')
    if pending:
        if pending['label'] != label:
            raise ValueError('another stage launch is pending')
        return  # The UUID, parent, baseline and launch token survive every retry.
    sessions = read(c / 'sessions.json', {})
    blocks = read(c / 'active_blocks.json', {})
    lineage = read(c / 'RUN.json', {}).get('lineage') or {}
    parent = lineage.get('resume_session')
    block = head(label)
    if parent:
        mode, sid = 'fork', str(uuid.uuid4())
    elif label in sessions:
        mode, sid = 'resumed', sessions[label]['session_id']
    elif block != label and (blocks.get(block) or sessions.get(block)):
        mode = 'shared'
        sid = blocks.get(block) or sessions[block]['session_id']
    else:
        mode, sid = 'fresh', str(uuid.uuid4())
    baseline = messages(transcript(run, parent or sid))
    write(c / 'pending_launch.json', {
        'subject': 'aggregator', 'label': label, 'mode': mode,
        'requested_session_id': sid, 'parent_session': parent,
        'launch_id': str(uuid.uuid4()), 'cli_version': cli, 'launched_utc': now(),
        'baseline_message_ids': [message_id(r) for r in baseline],
    })


def confirm(run):
    c = Path(run) / 'CONTROL'
    p = read(c / 'pending_launch.json')
    if not p:
        return True
    sid = p.get('requested_session_id')
    if not sid:
        raise ValueError('legacy pending launch has no exact ID; do not guess a transcript')
    baseline = set(p.get('baseline_message_ids', []))
    fresh = [r for r in messages(transcript(run, sid))
             if message_id(r) not in baseline and r.get('sessionId') == sid]
    if not fresh:
        print('Launch remains pending: no new aggregator message under the exact requested ID.', file=sys.stderr)
        return False
    sessions = read(c / 'sessions.json', {})
    sessions[p['label']] = dict(p, session_id=sid, confirmed_utc=now())
    write(c / 'sessions.json', sessions)
    blocks = read(c / 'active_blocks.json', {})
    blocks[head(p['label'])] = sid
    write(c / 'active_blocks.json', blocks)
    if p['mode'] == 'fork':
        r = read(c / 'RUN.json')
        lin = r.setdefault('lineage', {})
        pt = transcript(run, p['parent_session'])
        inherited = sum(1 for _ in open(pt)) if pt.exists() else 0   # the fork's lines it did not write
        lin.update(resumed_session=p['parent_session'], resume_session=None, child_session=sid,
                   inherited_lines=inherited)
        write(c / 'RUN.json', r)
    (c / 'pending_launch.json').unlink()
    print('Confirmed aggregator session ' + sid)
    return True


def launch(run, label, token, api_ok=False):
    run = Path(run).resolve()
    c = run / 'CONTROL'
    p = read(c / 'pending_launch.json')
    if not p or p['label'] != label or p['launch_id'] != token:
        raise ValueError('prepared launch token is stale or belongs to another stage')
    if os.environ.get('ANTHROPIC_API_KEY') and not api_ok:
        raise ValueError('API key is set; subscription launch refused without --api-ok')
    sid = p['requested_session_id']
    path = transcript(run, sid)
    cmd = ['claude']
    if path.exists():
        # A failed/aborted launch can have persisted the chosen ID already.
        rows = messages(path)
        if not rows or not any(r.get('sessionId') == sid for r in rows):
            raise ValueError('requested ID has an unverifiable partial transcript; preserve it for recovery')
        cmd += ['--resume', sid]
    elif p['mode'] == 'fork':
        cmd += ['--resume', p['parent_session'], '--fork-session', '--session-id', sid]
    elif p['mode'] in ('shared', 'resumed'):
        raise ValueError('recorded aggregator transcript is missing; refusing a fresh replacement')
    else:
        cmd += ['--session-id', sid]
    settings(run, stage_of(label))
    model, ent = arm_for(run, label)
    # v43 (J 2026-10-04): nothing asks. dontAsk refuses what no rule, read or sandbox allows, and never prompts
    cmd += ['--strict-mcp-config', '--permission-mode', 'dontAsk', '-n', 'leg-' + label, '--model', model]
    if ent.get('effort'):
        cmd += ['--effort', ent['effort']]
    prompt = (c / 'next_prompt.txt').read_text() if (c / 'next_prompt.txt').exists() else ''
    if prompt:
        cmd += [prompt]
    env = os.environ.copy()
    env.update(CLAUDE_CONFIG_DIR=str(c / '.cc'), CLAUDE_CODE_PROJECT_DIR_NAME='run',
               STAGE=stage_of(label), CLAUDE_CODE_SUBAGENT_MODEL=model,  # helpers run on the leg's model
               CLAUDE_CODE_DISABLE_AUTO_MEMORY='1')  # no Claude auto-memory: what carries between legs is the forked conversation and the folder
    seed_trust(run)
    write(c / 'active_launch.json', dict(p, handler_pid=os.getpid(), started_utc=now()))
    rc = 1
    try:
        rc = subprocess.call(cmd, cwd=run / '00_GIVE-THE-AGENT', env=env)
    finally:
        write(c / 'last_launch_exit.json', {'launch_id': token, 'label': label,
              'session_id': sid, 'exit_code': rc, 'exited_utc': now()})
        (c / 'active_launch.json').unlink(missing_ok=True)
    confirmed = confirm(run)
    return rc if rc else (0 if confirmed else 1)


def preclose(run, label, force, files_only):
    run = Path(run)
    c, ag = run / 'CONTROL', run / '00_GIVE-THE-AGENT'
    nn = stage_of(label)
    rec = read(c / 'sessions.json', {}).get(label, {})
    sid = rec.get('session_id')
    rows = messages(transcript(run, sid)) if sid and not files_only else []
    last = rows[-1] if rows else {}
    completed = (last.get('type') == 'assistant' and last.get('sessionId') == sid
                 and last.get('message', {}).get('stop_reason') == 'end_turn'
                 and message_id(last) not in rec.get('baseline_message_ids', []))
    exited = read(c / 'last_launch_exit.json', {})
    launcher_closed = (not (c / 'active_launch.json').exists()
                       and exited.get('launch_id') == rec.get('launch_id')
                       and bool(rec.get('launch_id')) and exited.get('exit_code') == 0)
    if not files_only and not force and (not completed or not launcher_closed):
        raise ValueError('aggregator must finish a new turn and exit its handler launch before normal close')
    # Validate paths before the privileged validator follows analyst-provided inputs.
    inventory(ag)
    # Never execute analyst-writable code with the handler's broader access.
    trusted = c / 'harness/validation_tools'
    validator = trusted / 'validate.py'
    report = c / ('validation-' + label + '.txt')
    rc = 1
    if validator.exists():
        with report.open('w') as output:
            runner = ("import runpy,sys; sys.path.insert(0,sys.argv[1]); "
                      "target=sys.argv.pop(1)+'/validate.py'; sys.argv[0]=target; "
                      "runpy.run_path(target,run_name='__main__')")
            rc = subprocess.call([sys.executable, '-I', '-S', '-B', '-c', runner, str(trusted),
                                  nn, str(ag), str(ag / 'out')],
                                 cwd=ag, stdout=output, stderr=subprocess.STDOUT)
    else:
        report.write_text('Validator missing. No validation was performed.\n')
    complete = bool(completed and launcher_closed and rc == 0 and not force and not files_only)
    write(c / ('close-status-' + label + '.json'), {
        'subject': 'aggregator', 'complete': complete, 'completed_turn': bool(completed),
        'launcher_exited': bool(launcher_closed), 'validator_exit_code': rc,
        'validator_sha256': digest(validator) if validator.exists() else None,
        'report_sha256': digest(report), 'checked_utc': now(),
    })
    if not complete and not force and not files_only:
        raise ValueError('stage validation failed; see ' + str(report))


def probe(run, label, questions_path, answers_path):
    """The recall probe: one headless turn in a fork of the leg's session (the leg's transcript is
    never touched), tools refused, the questions as the prompt; the reply saved verbatim for
    probe.py --score, the fork's id beside it."""
    run = Path(run).resolve()
    c = run / 'CONTROL'
    rec = read(c / 'sessions.json', {}).get(label) or {}
    sid = rec.get('session_id')
    if not sid:
        raise ValueError('no confirmed session for %s; the probe runs in the leg\'s own session' % label)
    model, ent = arm_for(run, label)
    q = Path(questions_path).read_text()
    env = os.environ.copy()
    env.update(CLAUDE_CONFIG_DIR=str(c / '.cc'), CLAUDE_CODE_PROJECT_DIR_NAME='run', STAGE=stage_of(label),
               CLAUDE_CODE_DISABLE_AUTO_MEMORY='1')
    fork = str(uuid.uuid4())
    cmd = ['claude', '--resume', sid, '--fork-session', '--session-id', fork, '-p', q, '--model', model,
           '--strict-mcp-config',
           '--disallowedTools', 'Bash', 'Read', 'Edit', 'Write', 'Glob', 'Grep', 'NotebookEdit', 'Agent', 'Task']
    if ent.get('effort'):
        cmd += ['--effort', ent['effort']]
    r = subprocess.run(cmd, cwd=run / '00_GIVE-THE-AGENT', env=env, capture_output=True, text=True, timeout=600)
    Path(answers_path).write_text(r.stdout)
    Path(str(answers_path) + '.session').write_text(fork + '\n')
    return r.returncode


def advance(run, label):
    d = Path(run) / 'CONTROL/snapshots' / label
    ck = read(d / 'checkpoint.json', {})
    return ((d / 'COMMITTED').exists()
            and (d / 'COMMITTED').read_text().strip() == ck.get('checkpoint_id')
            and ck.get('kind') == 'agent-and-files' and not ck.get('forced')
            and ck.get('validation', {}).get('complete') is True)


def inventory(root, agent=False):
    root = Path(root)
    result = {}
    def visit(p):
        rel = p.relative_to(root).as_posix()
        if any(c in rel for c in '\t\n\r'):
            raise ValueError('manifest cannot encode path: ' + repr(rel))
        if p.name == '__pycache__' or (not agent and rel == '.cc'):
            return
        if agent and 'credentials' in p.name.lower():
            return
        st = p.lstat()
        mode = oct(stat.S_IMODE(st.st_mode))
        if p.is_symlink():
            target = os.readlink(p)
            if any(c in target for c in '\t\n\r'):
                raise ValueError('manifest cannot encode symlink target')
            # Checkpoints are self-contained; external links are not restorable evidence.
            resolved = (p.parent / target).resolve()
            if resolved != root.resolve() and root.resolve() not in resolved.parents:
                raise ValueError('symlink escapes checkpoint root: ' + rel)
            result[rel] = ('symlink', mode, '-', target)
        elif p.is_dir():
            result[rel] = ('directory', mode, '-', '-')
            for child in sorted(p.iterdir()):
                visit(child)
        elif p.is_file():
            result[rel] = ('file', mode, digest(p), str(st.st_size))
        else:
            raise ValueError('unsupported checkpoint file type: ' + rel)
    for p in sorted(root.iterdir()):
        visit(p)
    return result


def save_manifest(path, entries):
    with Path(path).open('w') as f:
        f.write('# v2 type\tmode\tsha256\tpath\tsize|target; includes directories\n')
        for rel, (kind, mode, sha, tail) in sorted(entries.items()):
            f.write('\t'.join((kind, mode, sha, rel, tail)) + '\n')


def load_manifest(path):
    result = {}
    for line in Path(path).read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        kind, mode, sha, rel, tail = line.split('\t', 4)
        result[rel] = (kind, mode, sha, tail)
    return result


def archive(root, path, prefix, entries):
    with tarfile.open(path, 'w:gz', dereference=False) as t:
        t.add(root, arcname=prefix, recursive=False)
        for rel in sorted(entries):
            t.add(Path(root) / rel, arcname=prefix + '/' + rel, recursive=False)


def verify_archive(path, prefix, manifest):
    expected, actual = load_manifest(manifest), {}
    with tarfile.open(path) as t:
        for m in t:
            name = m.name.rstrip('/')
            if name == prefix:
                continue
            if not name.startswith(prefix + '/') or '..' in Path(name).parts:
                raise ValueError('archive path outside its declared subject: ' + name)
            rel = name[len(prefix) + 1:]
            if rel in actual:
                raise ValueError('duplicate archive member: ' + rel)
            mode = oct(m.mode)
            if m.isfile() or m.islnk():
                if m.islnk() and (not m.linkname.startswith(prefix + '/') or '..' in Path(m.linkname).parts):
                    raise ValueError('hard link escapes archive subject: ' + rel)
                h = hashlib.sha256()
                size = 0
                with t.extractfile(m) as f:
                    for b in iter(lambda: f.read(1024 * 1024), b''):
                        h.update(b)
                        size += len(b)
                actual[rel] = ('file', mode, h.hexdigest(), str(size))
            elif m.isdir():
                actual[rel] = ('directory', mode, '-', '-')
            elif m.issym():
                actual[rel] = ('symlink', mode, '-', m.linkname)
            else:
                raise ValueError('unsupported archive member: ' + rel)
    if actual != expected:
        raise ValueError('archive differs from its per-entry manifest: ' + str(path))


def run_sessions(cc):
    """What a checkpoint keeps of the run's Claude folder: the run's own sessions (projects/run/),
    and nothing else. The folder also holds the account record, the account's synced skills and
    plugins, and caches; none of that is needed to resume a leg, and it stays on this machine."""
    keep = ('projects', 'projects/run')
    return {k: v for k, v in inventory(cc, True).items() if k in keep or k.startswith('projects/run/')}


def capture(run, dest, sid, expected_sha):
    run, dest = Path(run), Path(dest)
    ag, cc = run / '00_GIVE-THE-AGENT', run / 'CONTROL/.cc'
    fs = inventory(ag)
    native = run_sessions(cc) if sid else None
    save_manifest(dest / 'fs.sha256', fs)
    archive(ag, dest / 'fs.tar.gz', '00_GIVE-THE-AGENT', fs)
    verify_archive(dest / 'fs.tar.gz', '00_GIVE-THE-AGENT', dest / 'fs.sha256')
    if sid:
        save_manifest(dest / 'agent-files.sha256', native)
        archive(cc, dest / 'agent.tar.gz', '.cc', native)
        verify_archive(dest / 'agent.tar.gz', '.cc', dest / 'agent-files.sha256')
        data = transcript(run, sid).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected_sha:
            raise ValueError('aggregator transcript changed during checkpoint capture')
        (dest / 'transcript.jsonl').write_bytes(data)
        (dest / 'transcript.sha256').write_text(expected_sha + '  transcript.jsonl\n')
        if native['projects/run/' + sid + '.jsonl'][2] != expected_sha:
            raise ValueError('native archive and recorded boundary disagree')
    if inventory(ag) != fs or (sid and run_sessions(cc) != native):
        raise ValueError('a writer changed the aggregator state during capture; nothing committed')


def verify_checkpoint(d):
    d = Path(d)
    verify_archive(d / 'fs.tar.gz', '00_GIVE-THE-AGENT', d / 'fs.sha256')
    ck = read(d / 'checkpoint.json')
    if ck.get('subject') != 'aggregator':
        raise ValueError('checkpoint does not declare the aggregator as its only subject')
    if (d / 'agent.tar.gz').exists():
        verify_archive(d / 'agent.tar.gz', '.cc', d / 'agent-files.sha256')
        sid = ck['session']['session_id']
        sha = ck['session']['transcript_sha256']
        manifest = load_manifest(d / 'agent-files.sha256')
        if manifest['projects/run/' + sid + '.jsonl'][2] != sha or digest(d / 'transcript.jsonl') != sha:
            raise ValueError('native aggregator transcript is not the recorded checkpoint boundary')


def interview(run, label, fork):
    """An interview's own folder (J, 2026-09-29): the analyst's folder and its sessions exactly as the
    checkpoint of `label` stored them, restored into interview-workspaces/<label>__<fork>/ and a project of
    its own in the run's Claude folder (projects/iv-<fork>). Never the live folder: the interview may add
    and write there, and nothing it does touches the run. Prints the folder."""
    run = Path(run).resolve()
    d = run / 'CONTROL/snapshots' / label
    if not (d / 'COMMITTED').exists():
        raise ValueError('%s has no committed checkpoint' % label)
    verify_checkpoint(d)
    if not (d / 'agent.tar.gz').exists():
        raise ValueError('%s was closed files-only: its checkpoint holds no session to interview' % label)
    ws = run / 'interview-workspaces' / ('%s__%s' % (label, fork))
    if ws.exists():
        raise ValueError('the interview folder exists already: ' + str(ws))
    ws.mkdir(parents=True)
    def extract(tar, dest):
        with tarfile.open(tar) as t:
            try:
                t.extractall(dest, filter='fully_trusted')   # the archive was verified member by member above
            except TypeError:
                t.extractall(dest)
    extract(d / 'fs.tar.gz', ws)
    agd = ws / '00_GIVE-THE-AGENT'
    verify_tree(agd, d / 'fs.sha256')
    tmp = ws / '.sessions-restore'
    extract(d / 'agent.tar.gz', tmp)
    verify_tree(tmp / '.cc', d / 'agent-files.sha256', agent=True)
    proj = run / 'CONTROL/.cc/projects' / ('iv-' + fork)
    if proj.exists():
        raise ValueError('the interview project exists already: ' + str(proj))
    import shutil
    shutil.copytree(tmp / '.cc/projects/run', proj)
    shutil.rmtree(tmp)
    sid = read(d / 'checkpoint.json')['session']['session_id']
    if digest(proj / (sid + '.jsonl')) != read(d / 'checkpoint.json')['session']['transcript_sha256']:
        raise ValueError('the restored session is not the checkpoint boundary')
    settings(run, stage_of(label), ag=agd, hooks=False)
    print(agd)


def verify_tree(root, manifest, agent=False):
    if (run_sessions(root) if agent else inventory(root)) != load_manifest(manifest):
        raise ValueError('restored tree differs from its checkpoint manifest')


def locked(run, command):
    run = str(Path(run).resolve())
    if os.environ.get('AGGREGATOR_LOCK_RUN') == run:
        return subprocess.call(command)
    lock = Path(run) / 'CONTROL/.protocol.lock'
    with lock.open('a') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('aggregator launch or handler mutation is still running')
        env = dict(os.environ, AGGREGATOR_LOCK_RUN=run)
        return subprocess.call(command, env=env)


def cost(path, skip, tdir, sid, out, parent=''):
    """The cost of a step, from its transcript; subagents apart. Lines already counted at an earlier boundary of
    the same session are skipped by count, since that file is only appended to. A fork's first session skips its
    parent's messages by their ids: the CLI copies them into the fork with their ids and leaves the parent's other
    lines behind, so a count of the parent's lines skips the fork's own work (claude 2.1.289, 5 October 2026)."""
    import glob
    skip = int(skip)
    inherited = set()
    pp = os.path.join(tdir, parent + '.jsonl') if parent else ''
    if pp and os.path.exists(pp):
        with open(pp, encoding='utf-8', errors='replace') as f:
            for line in f:
                try:
                    u = json.loads(line).get('uuid')
                except (ValueError, AttributeError):
                    continue
                if u:
                    inherited.add(u)

    def usage_of(path, skip=0, inherited=frozenset()):
        tot = {'input_tokens': 0, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'output_tokens': 0}
        turns, models, n, dropped = 0, {}, 0, 0
        if not path or not os.path.exists(path):
            return tot, turns, models, n, dropped
        with open(path, encoding='utf-8', errors='replace') as f:
            for i, line in enumerate(f):
                n = i + 1
                if i < skip:
                    continue
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                if not isinstance(d, dict):
                    continue
                if d.get('uuid') and d['uuid'] in inherited:
                    dropped += 1
                    continue
                m = d.get('message') or {}
                u = m.get('usage') if isinstance(m, dict) else None
                if d.get('type') == 'assistant' and isinstance(u, dict):
                    turns += 1
                    for k in tot:
                        tot[k] += int(u.get(k) or 0)
                    if m.get('model'):
                        models[m['model']] = models.get(m['model'], 0) + 1
        return tot, turns, models, n, dropped

    main, turns, models, n, dropped = usage_of(path, skip, inherited)
    subs = {}
    if sid:
        for sp in sorted(glob.glob(os.path.join(tdir, sid, '**', '*.jsonl'), recursive=True)):
            t, tu, mo, nn, _ = usage_of(sp)
            subs[os.path.relpath(sp, tdir)] = {**t, 'assistant_turns': tu, 'models': mo, 'lines': nn}
    rep = {'main': {**main, 'assistant_turns': turns, 'models': models, 'transcript_lines': n,
                    'lines_skipped_as_already_counted': skip, 'inherited_from': parent or None,
                    'rows_skipped_as_inherited': dropped,
                    'inherited_ids_found': bool(inherited) if parent else None},
           'subagents': subs,
           'subagents_note': 'every transcript under the session\'s own directory, whole: cumulative '
                             'for the session, not for this step; a parent total that already includes '
                             'subagent usage is not known here, so the two are reported apart and never '
                             'summed',
           'note': 'sum of usage blocks on assistant turns; cache tokens counted apart'}
    with open(out, 'w') as f:
        json.dump(rep, f, indent=1)


def main(a):
    op, *args = a
    if op == 'settings': settings(*args)
    elif op == 'probe': return probe(*args)
    elif op == 'arm': print(arm_for(*args)[0])
    elif op == 'prepare': prepare(*args)
    elif op == 'confirm': return 0 if confirm(*args) else 1
    elif op == 'launch': return launch(*args[:3], api_ok='--api-ok' in args[3:])
    elif op == 'preclose': preclose(args[0], args[1], args[2] == '1', args[3] == '1')
    elif op == 'advance': return 0 if advance(*args) else 1
    elif op == 'capture': capture(*args)
    elif op == 'cost': cost(*args)
    elif op == 'verify-checkpoint': verify_checkpoint(*args)
    elif op == 'verify-tree': verify_tree(*args[:2], agent='--agent' in args[2:])
    elif op == 'interview': interview(*args)
    elif op == 'trust': seed_trust(*args)
    elif op == 'locked': return locked(args[0], args[1:])
    else: raise ValueError('unknown guard operation: ' + op)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except (ValueError, OSError, KeyError, tarfile.TarError) as e:
        sys.exit('REFUSING: ' + str(e))
