#!/usr/bin/env python3
"""branches.py: analysis branches for the Claude arm, made as the Codex controller makes them
(codex/runtime/branches.py and publication.py), so that the two arms fork the same way.

A branch is a new run that starts from one verified close of another run, the parent. Everything up to
that close is inherited unchanged. The investigator may then replace stage cards and data before the
branch's first leg. Everything after that leg is the branch's own analysis.

The Codex verbs and records, with their Claude form:

| Codex controller | Claude (legs.py) | What it does |
|---|---|---|
| `branch SOURCE CHECKPOINT RUN --leg LEG` | the same | a draft branch from a verified checkpoint |
| `branch-put RUN PATH --file F [--stage NN]` | the same | replace a stage card or add data, while draft |
| `branch-status RUN` | the same | `BRANCH.json` and the publication |
| `prepare-branch RUN` | the same | seal, publish the setup to Git, prepare the first leg (no turn) |
| `publish-branch RUN` | the same | publish again after a failure, at an idle close; never reruns analysis |
| `BRANCH.json` | the same keys, `backend: claude` | status, source_run, checkpoint, checkpoint_sha256, after_leg, target_leg, changes |
| `check_order`, `seal` | the same rules | the first leg comes right after the fork point; sealed at the first leg |
| `verify_inputs` | the same | stage deliveries, the harness, the arms and the settings template (paths, modes, hashes; links refused) never change after the branch is made, but by `branch-put` |
| the first message's notice | the same text | the analyst is told it is a branch and what changed |
| `refs/heads/analysis/RUN` | the same | the branch's own Git branch; main is never touched |
| `refs/tags/analysis-checkpoints/CP` | the same | the parent's commit at the fork point |
| commits "Analysis RUN: setup before LEG", "Analysis RUN: verified LEG" | the same | one per verified close |
| publication blocked | the same | a close not committed, or not pushed when a remote is set, stops the next leg until publish-branch |

What differs, because a Claude run is a folder of the repository that its own harness runs:

- The branch is a run folder, `aggregator/runs/<SOURCE>--<name>/`, beside its parent. Its harness, stage
  drops and records come from Git: the commit that published the fork point (`publish.sh` commits every
  close), checked against the close's `instrument.tar.gz` (stage drops, harness, declarations, events) and
  its analyst's folder. The analyst's folder and the sessions come from the checkpoint (`fs.tar.gz`,
  `agent.tar.gz`), each verified against its manifest, with the fork point's checkpoint and the index up to
  it. `RUN.json` in the analyst's folder may differ from the checkpoint only in the token counts close.sh
  writes after the capture; the branch keeps the committed one, as the parent's next leg would.
- Its commits hold the run folder under the parent's folder name, plus `LINEAGE.json`, so `git diff` from the
  fork point shows only what the branch changed (Codex commits `workspace/` and `stage-deliveries/`).
- Main's `.gitignore` keeps `aggregator/runs/*--*/` off main. The branch's own `publish.sh` is this module's
  publisher: each close is committed to `analysis/<run>` through Git plumbing, with a temporary index, never
  the shared checkout. Its `step.sh` is a guard before the parent's (`step-parent.sh`): no leg before the setup
  is published or while publication is blocked, and the first leg only through legs.py, which adds the notice.
  `BRANCH.json` records both harness changes.
- Without a remote the commits stay local and the next leg may run (Codex needs the remote).
- The first leg continues the fork point's conversation, as every leg does (step.sh, v40), and the branch
  needs its own login once, as every run does.
- The parent's interviews stay with the parent: their sessions are not copied (they live outside any
  checkpoint and may have grown since the fork point); their rows move from `interviews.tsv` to `BRANCH.json`
  (`interviews_omitted`), so E2a lists the branch's own. The analyst's folder may hold links inside it, as a
  checkpoint may; the drops, harness and declarations may hold none.
  A branch never publishes an `interviews/`, `interview-workspaces/`, `.cc/` or `native/` folder at any depth.

    python3 branches.py publish RUN LABEL [KIND]     what the branch's publish.sh runs at each close
    python3 branches.py check-step RUN ARGS...       what the branch's step.sh runs before the parent's
"""
import contextlib
import fcntl
import hashlib
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import uuid
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
A = sys.modules.get('claude_legs_actor')   # legs.py's own copy, so that both raise the same Error
if A is None:
    _spec = importlib.util.spec_from_file_location('claude_branches_actor', HERE / 'actor.py')
    A = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(A)
Error = A.Error

NOTICE = ('This is analysis branch %s from %s after %s. The supplied files supersede remembered versions. Read the current '
          'stage card and data. Recorded changes: %s. Earlier validation belongs to the original inputs; do not claim those '
          'checks certify changed data. Keep the inherited trusted checks. ')   # codex/runtime/branches.py notice(), word for word
DATA_FOLDERS = ('package', 'trees', 'shelves', 'handling', 'attachments')
BLOCKED_SUFFIXES = ('.py', '.sh', '.exe', '.so', '.dylib', '.sqlite', '.db')
SECRET_NAMES = ('.credentials.json', 'credentials.json', 'auth.json', '.env', '.claude.json')
# never published, whatever .gitignore says: the login and sessions, the handler's records, checkpoints, interviews
NEVER = ('CONTROL/.cc/', 'CONTROL/legs/', 'CONTROL/snapshots/', 'interview-workspaces/', '_to_delete/')
# folders a branch never publishes at any depth, whatever .gitignore says, as Codex's publication.safe_files: the
# interviews' transcripts (E2 copies them into the analyst's handling/interviews/) and the sessions
PRIVATE_DIRS = {'interviews', 'interview-workspaces', '.cc', 'native'}
# the form of BRANCH.json's input hashes: 2 since 5 October 2026 (modes, links, arms and settings template)
INPUTS_VERSION = 2
PUBLISH = '''#!/usr/bin/env bash
# publish.sh LABEL [KIND], for an analysis branch (legs.py branch). The branch is committed to its own Git branch,
# analysis/<run>, through Git plumbing: main, the shared checkout and the Manual are left alone. It replaces the
# run's publish.sh; BRANCH.json records the change (harness_changed).
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
RUN="$(cd "$HERE/../.." && pwd -P)"
PY="${RPLACE_BRANCHES_PY:-$HERE/../../../../handler/claude-adapter/branches.py}"
python3 "$PY" publish "$(basename "$RUN")" "$1" "${2:-close}" || true
exit 0
'''
STEP = '''#!/usr/bin/env bash
# step.sh, for an analysis branch (legs.py branch): refuses a leg before the branch's setup is published, while its
# publication is blocked, and its first leg outside legs.py (which tells the analyst it is a branch); then runs
# the parent's step.sh, kept unchanged beside it as step-parent.sh. BRANCH.json records the change.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
RUN="$(cd "$HERE/../.." && pwd -P)"
PY="${RPLACE_BRANCHES_PY:-$HERE/../../../../handler/claude-adapter/branches.py}"
python3 "$PY" check-step "$(basename "$RUN")" "$@" || exit 1
exec bash "$HERE/step-parent.sh" "$@"
'''


def runs_dir():
    v = os.environ.get('RPLACE_LEGS_RUNS')   # the tests only
    return Path(v) if v else REPO / 'aggregator/runs'


def run_dir(name):
    A.identity(name)
    return (runs_dir() / name).resolve()


def git(top, *args, data=None, index=None, check=True):
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
    if index:
        env['GIT_INDEX_FILE'] = str(index)
    r = subprocess.run(['git'] + [str(a) for a in args], cwd=str(top), env=env, input=data, capture_output=True,
                       timeout=600, check=False)
    if check and r.returncode:
        raise Error('git %s failed: %s' % (args[0], r.stderr.decode(errors='replace').strip()[-800:]))
    return r.stdout


def toplevel(path):
    r = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=str(path), capture_output=True, text=True, check=False)
    if r.returncode:
        raise Error('%s is not inside a Git repository: a branch is published to Git, so it needs one' % path)
    return Path(r.stdout.strip())


def sha(path):
    return A.sha(path)


def tree_hash(root, skip=(), links=False):
    """One hash over a folder or a file: sorted relative paths, modes and file hashes (the Codex inventories, in one
    value). A link is never followed: refused (OpenAI review 15:50Z, finding 3), or, with links, recorded by its target
    when it stays inside the folder, as the harness's checkpoint inventory records it. Anything but a file, a folder
    or such a link is refused. Python's caches and Finder's files are not inputs; nor are the paths in skip."""
    h = hashlib.sha256()
    root = Path(root)
    if root.is_symlink():
        raise Error('A link where an input should be: %s' % root.name)
    entries = []
    if root.is_file():
        entries = [(Path(root.name), root)]
    elif root.is_dir():
        def unreadable(e):
            raise Error('An input folder cannot be read: %s' % e)
        for d, dirs, files in os.walk(root, onerror=unreadable):   # never descends through a link
            entries += [(Path(d, n).relative_to(root), Path(d, n)) for n in dirs + files]
    top = root.resolve()
    for rel, p in sorted(entries, key=lambda e: e[0].as_posix()):
        if '__pycache__' in rel.parts or p.name == '.DS_Store' or rel.as_posix() in skip:
            continue
        if p.is_symlink():
            target = os.readlink(p)
            res = (p.parent / target).resolve()
            if not links:
                raise Error('A link where an input should be: %s' % rel.as_posix())
            if os.path.isabs(target):   # it would point into the parent's folder from a branch
                raise Error('A link with an absolute target: %s' % rel.as_posix())
            if res != top and top not in res.parents:
                raise Error('A link that leaves its folder: %s' % rel.as_posix())
            h.update(('%s\tlink\t%s\n' % (rel.as_posix(), target)).encode())
        elif p.is_dir():
            continue
        elif not p.is_file():
            raise Error('Not a file or a folder: %s' % rel.as_posix())
        else:
            h.update(('%s\t%o\t%s\n' % (rel.as_posix(), stat.S_IMODE(p.lstat().st_mode), sha(p))).encode())
    return h.hexdigest()


def baseline_hash(run, skip=()):
    """The analyst's folder: as tree_hash, with its in-folder links (a checkpoint may hold them) recorded."""
    return tree_hash(Path(run) / '00_GIVE-THE-AGENT', skip, links=True)


def trusted_hash(run):
    """The harness and the run's declarations a branch may not change after it is made: CONTROL/harness, the arms
    and the settings template (Codex keeps a separate arm freeze)."""
    return hashlib.sha256('|'.join(tree_hash(run / x) for x in
                                   ('CONTROL/harness', 'CONTROL/arm.json', 'CONTROL/settings.template.json')).encode()).hexdigest()


def branch_of(run):
    return A.read(Path(run) / 'BRANCH.json')


def save(run, b):
    A.write(Path(run) / 'BRANCH.json', b)


def steps_module(run):
    p = run / 'CONTROL/harness/steps.py'
    spec = importlib.util.spec_from_file_location('claude_branches_steps', p if p.is_file() else
                                                  REPO / 'aggregator/instrument/tools/steps.py')
    st = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(st)
    return st


def num(d):
    """A leg's repeat number: 01 -> 1, r2 -> 2, none -> None."""
    x = d.get('round') or d.get('count')
    return int(str(x).lstrip('r')) if x else None


# ---- the fork point -------------------------------------------------------------------------------------------
def resolve(src, checkpoint):
    """The close label for a label (C1.C1a-04 or C1a-04) or a checkpoint id of the source run."""
    index = src / 'CONTROL/snapshots/INDEX.tsv'
    rows = [r.split('\t') for r in index.read_text().splitlines()[1:] if r.strip()] if index.exists() else []
    for r in rows:
        if checkpoint in (r[0], r[0].split('.', 1)[-1]) or (len(r) > 10 and checkpoint == r[10]):
            return r[0]
    raise Error('%s has no close %s (CONTROL/snapshots/INDEX.tsv)' % (src.name, checkpoint))


def verified_close(src, label):
    """The fork point's snapshot, verified whole as the adapter verifies a close, and allowed to advance a run."""
    d, ck = snapshot_ok(src, label)
    if not A.harness(src).advance(src, label):
        raise Error('Only a verified completed close seeds a branch: %s was forced, paused or did not validate' % label)
    return d, ck


def snapshot_ok(src, label):
    """A close's snapshot verified whole, as the adapter verifies a close: COMMITTED binds checkpoint.json, every
    file matches MANIFEST.sha256 and none is missing or extra, and both archives match their manifests. Says
    nothing about whether the close may advance a run (protocol_guard.advance)."""
    g = A.harness(src)
    d = src / 'CONTROL/snapshots' / label
    if not (d / 'COMMITTED').is_file():
        raise Error('%s is not committed' % label)
    ck = A.read(d / 'checkpoint.json') or {}
    if (d / 'COMMITTED').read_text().strip() != ck.get('checkpoint_id') or ck.get('label') != label:
        raise Error('The snapshot of %s does not bind its checkpoint' % label)
    if ck.get('kind') != 'agent-and-files':
        raise Error('%s was closed %s: its snapshot holds no session to go on from' % (label, ck.get('kind')))
    digests = {}
    for line in (d / 'MANIFEST.sha256').read_text().splitlines():
        if line.strip():
            value, name = line.split(None, 1)
            digests[name.strip().lstrip('*')] = value
    present = {p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()} - {'MANIFEST.sha256', 'COMMITTED'}
    if present != set(digests) or any(sha(d / n) != v for n, v in digests.items()) or A.CLOSE_FILES - set(digests):
        raise Error('The snapshot of %s differs from its manifest' % label)
    try:
        g.verify_checkpoint(d)
    except (ValueError, KeyError, OSError, tarfile.TarError) as e:
        raise Error('The snapshot of %s does not verify: %s' % (label, e)) from e
    return d, ck


def stage_order(run):
    rows = (run / 'DROPS/ORDER.tsv').read_text().splitlines()[1:]
    return [r.split('\t')[0] for r in rows if r.strip()]


def check_target(src, label, leg):
    """The branch's first leg comes right after the fork point, by Codex's check_order: the next stage's first
    leg if the fork point finished its stage, else the next repeat of the same step or the next step."""
    st = steps_module(src)
    try:
        d, last = st.parse(leg), st.parse(label.split('.', 1)[1])
    except (ValueError, KeyError) as e:
        raise Error('No such leg: %s' % e) from e
    nn, order = last['stage'], stage_order(src)
    fin = src / 'CONTROL/stage-state' / nn / 'FINISHED'
    finished = fin.is_file() and fin.read_text().strip().split('\t')[-1] == label
    if d.get('cont'):
        raise Error('A branch starts at a new leg, not at the continuation of a paused one')
    if finished:
        nxt = order[order.index(nn) + 1] if order.index(nn) + 1 < len(order) else None
        if nxt is None:
            raise Error('%s finished the last stage: no leg comes after it' % label)
        if d['stage'] != nxt or d['step'] != 'a' or num(d) not in (None, 1):
            raise Error('The fork point %s finished its stage: the branch starts at the first leg of %s' % (label, nxt))
        return d['stage']
    if d['stage'] != nn:
        raise Error('The fork point %s did not finish stage %s: the branch\'s first leg must be in stage %s' % (label, nn, nn))
    if nn == 'B2' and last['step'] == 'b' and d['step'] == 'a':
        ok = num(d) == (num(last) or 0) + 1
    elif d['step'] == last['step']:
        row = [r for r in st.table() if r['stage'] == nn and r['step'] == d['step']]
        ok = bool(row) and row[0]['repeat'] == 'yes' and num(d) == (num(last) or 0) + 1
    elif d['step'] == chr(ord(last['step']) + 1):
        ok = num(d) == num(last) if nn == 'B2' and d['step'] == 'b' else num(d) in (None, 1)
    else:
        ok = False
    if not ok:
        raise Error('%s does not come right after %s: a branch cannot skip or repeat a step' % (leg, label))
    return d['stage']


def ignored(top, paths):
    """Which of these repository paths main's .gitignore would leave out (patterns only, not the index). Paths
    travel NUL-separated, so no name is quoted; a git that fails is an error, never "nothing is ignored"."""
    if not paths:
        return set()
    r = subprocess.run(['git', 'check-ignore', '--no-index', '--stdin', '-z'], cwd=str(top),
                       input='\0'.join(paths).encode('utf-8', 'surrogateescape') + b'\0', capture_output=True, check=False)
    if r.returncode not in (0, 1):
        raise Error('git check-ignore failed: %s' % r.stderr.decode(errors='replace').strip()[-400:])
    return set(r.stdout.decode('utf-8', 'surrogateescape').split('\0')) - {''}


def candidates(top, src, label, prefix, parent_branch):
    """The commits that may have published the fork point, oldest first: on main, every "<kind> <label>" commit
    that touched the source run (publish.sh commits the whole repository, so another run's close of the same
    label can touch it too); in a parent branch, its own record."""
    if parent_branch:
        c = ((A.read(src / 'publication.json') or {}).get('commits') or {}).get(label)
        if not c:
            raise Error('The parent branch has not published %s; publish-branch %s first' % (label, src.name))
        return [c]
    A.identity(label)
    pattern = '^(close|interview-point|pause|finished) %s$' % label.replace('.', '[.]')
    out = git(top, 'log', '--reverse', '--format=%H', '-E', '--grep=' + pattern, 'HEAD', '--', prefix).decode().split()
    if not out:
        raise Error('No commit of %s on this branch of the repository: commit the parent (publish.sh does it at every '
                    'close) before branching from it' % label)
    return out


def extract_prefix(top, commit, prefix, dest):
    """The source run as that commit holds it, into dest (git archive; no links, no paths outside)."""
    with tempfile.TemporaryDirectory(prefix='branch-archive-') as tmp:
        tarpath = Path(tmp) / 'tree.tar'
        git(top, 'archive', '--format=tar', '-o', tarpath, commit, prefix)
        with tarfile.open(tarpath) as t:
            for m in t.getmembers():
                p = PurePosixPath(m.name)
                if not (m.isfile() or m.isdir()) or '..' in p.parts or p.is_absolute():
                    raise Error('The commit holds a link or an unsafe path: %s' % m.name)
                rel = PurePosixPath(*p.parts[len(PurePosixPath(prefix).parts):])
                if not rel.parts:
                    continue
                target = dest / str(rel)
                if m.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                with t.extractfile(m) as f, target.open('wb') as out:
                    shutil.copyfileobj(f, out)
                os.chmod(target, 0o755 if m.mode & 0o111 else 0o644)


def tokenless(data):
    """RUN.json without the token counts close.sh writes into it after the capture (close.sh step 4b)."""
    r = json.loads(data)
    for e in (r.get('legs') or []) if isinstance(r, dict) else []:
        if isinstance(e, dict):
            e.pop('tokens', None)
    return r


def compare(top, prefix, built, kept, sub):
    """Files under sub in the built run against the archived ones: (missing, extra, changed); a file Git ignores
    may be missing from the commit."""
    held = {p.relative_to(built).as_posix(): p for p in (built / sub).rglob('*') if p.is_file()} if (built / sub).is_dir() \
        else ({sub: built / sub} if (built / sub).is_file() else {})
    missing = [r for r in kept if r not in held and not set(r.split('/')[:-1]) & PRIVATE_DIRS]   # never published
    skipped = ignored(top, ['%s/%s' % (prefix, r) for r in missing])
    return ([r for r in missing if '%s/%s' % (prefix, r) not in skipped], [r for r in held if r not in kept],
            [r for r in held if r in kept and sha(held[r]) != kept[r]])


def agrees(g, top, prefix, built, snap, label):
    """The commit holds the run as the close left it: its analyst's folder agrees with the checkpoint, and its
    stage drops, harness, declarations and events with the close's instrument.tar.gz (the events with one more
    line, the close's own). Returns the committed RUN.json's bytes, or None when the commit has none."""
    fs = {'00_GIVE-THE-AGENT/' + rel: v[2] for rel, v in g.load_manifest(snap / 'fs.sha256').items() if v[0] == 'file'}
    missing, extra, changed = compare(top, prefix, built, fs, '00_GIVE-THE-AGENT')
    rj = built / '00_GIVE-THE-AGENT/RUN.json'
    run_json = rj.read_bytes() if rj.is_file() else None
    if '00_GIVE-THE-AGENT/RUN.json' in changed:
        changed.remove('00_GIVE-THE-AGENT/RUN.json')
        with tarfile.open(snap / 'fs.tar.gz') as t:
            kept = t.extractfile('00_GIVE-THE-AGENT/RUN.json').read()
        try:
            same = tokenless(run_json) == tokenless(kept)
        except ValueError:
            same = False
        if not same:
            changed.append('00_GIVE-THE-AGENT/RUN.json (beyond its token counts)')
    with tempfile.TemporaryDirectory(prefix='branch-instrument-') as t:
        t = Path(t)
        with tarfile.open(snap / 'instrument.tar.gz') as tar:
            for m in tar.getmembers():
                p = PurePosixPath(m.name)
                if not (m.isfile() or m.isdir()) or '..' in p.parts or p.is_absolute():
                    raise Error('The close\'s instrument archive holds an unsafe entry: %s' % m.name)
        untar(snap / 'instrument.tar.gz', t)
        archived = {p.relative_to(t).as_posix(): sha(p) for p in t.rglob('*') if p.is_file()}
        for sub in ('DROPS', 'CONTROL/harness', 'CONTROL/arm.json', 'CONTROL/settings.template.json',
                    'CONTROL/active_blocks.json'):
            kept = {r: v for r, v in archived.items() if r == sub or r.startswith(sub + '/')}
            if kept:
                m2, e2, c2 = compare(top, prefix, built, kept, sub)
                missing, extra, changed = missing + m2, extra + e2, changed + c2
        ev = 'CONTROL/handover-events.log'
        if ev in archived:
            before = (t / ev).read_text()
            now = (built / ev).read_text() if (built / ev).is_file() else ''
            tail = now[len(before):].strip('\n').split('\n') if now.startswith(before) else None
            if not tail or len(tail) != 1 or tail[0].split('\t')[1:3] != ['closed', label]:
                changed.append(ev + ' (not the archived events and the close\'s own line)')
    if missing or extra or changed:
        raise Error('missing %s; extra %s; changed %s' % (missing[:3], extra[:3], changed[:3]))
    return run_json


def untar(path, dest):
    with tarfile.open(path) as t:
        try:
            t.extractall(dest, filter='fully_trusted')   # every member was checked before
        except TypeError:   # a Python without extraction filters
            t.extractall(dest)


def fork_commit(g, top, src, label, prefix, snap, parent_branch, new):
    """The oldest commit that holds the run as the fork point left it, extracted into a new building folder.
    Returns (commit, the committed RUN.json, the folder)."""
    reasons = []
    for c in candidates(top, src, label, prefix, parent_branch):
        tmp = runs_dir().resolve() / ('.%s.building-%s' % (new, uuid.uuid4().hex[:8]))
        tmp.mkdir()
        try:
            extract_prefix(top, c, prefix, tmp)
            return c, agrees(g, top, prefix, tmp, snap, label), tmp
        except Error as e:
            reasons.append('%s: %s' % (c[:12], e))
            shutil.rmtree(tmp)   # this function's own extraction of a commit that is not the fork point
    raise Error('No commit holds %s as its close left it, so nothing was built (%s)' % (label, ' | '.join(reasons)[:1500]))


def create(source, checkpoint, new, leg):
    """A draft branch: the parent's run as committed at the fork point, its analyst's folder and sessions from
    the checkpoint, the fork point's checkpoint and index, BRANCH.json. No turn, no Git write."""
    A.identity(source)
    A.identity(new)
    leg = A.identity(str(leg).split('.', 1)[-1])
    if new == source or '--' not in new:
        raise Error('Name the branch <parent>--<name> (two hyphens), a new name: main ignores aggregator/runs/*--*/')
    src, dest = run_dir(source), run_dir(new)
    if dest.exists():
        raise Error('%s exists already; choose a new branch name' % new)
    top = toplevel(src)
    if not ignored(top, [str((dest / 'x').relative_to(top))]):
        raise Error('The repository does not ignore %s: add aggregator/runs/*--*/ to .gitignore first, so that main never '
                    'commits a branch' % dest.relative_to(top))
    parent_branch = branch_of(src)
    if parent_branch and parent_branch.get('status') == 'draft':
        raise Error('Cannot branch an unfinished setup')
    label = resolve(src, checkpoint)
    snap, ck = verified_close(src, label)
    stage = check_target(src, label, leg)
    g = A.harness(src)
    prefix = (A.read(src / 'publication.json') or {}).get('prefix') if parent_branch else str(src.relative_to(top))
    base, run_json, tmp = fork_commit(g, top, src, label, prefix, snap, parent_branch, new)
    try:
        # the analyst's folder is the checkpoint's (modes and times too); the commit's copy served the check
        shutil.rmtree(tmp / '00_GIVE-THE-AGENT')
        untar(snap / 'fs.tar.gz', tmp)   # verify_checkpoint checked every member
        g.verify_tree(tmp / '00_GIVE-THE-AGENT', snap / 'fs.sha256')
        if run_json is not None:
            (tmp / '00_GIVE-THE-AGENT/RUN.json').write_bytes(run_json)
        if parent_branch:
            for name in ('BRANCH.json', 'LINEAGE.json'):
                (tmp / name).unlink(missing_ok=True)   # this extraction's copy of the parent's records; Git keeps them
        # the sessions, as the checkpoint keeps them (projects/run), verified entry by entry
        cc = tmp / 'CONTROL/.cc'
        cc.mkdir(parents=True, exist_ok=True)
        os.chmod(cc, 0o700)
        with tempfile.TemporaryDirectory(prefix='branch-sessions-') as t2:
            with tarfile.open(snap / 'agent.tar.gz') as t:
                for m in t.getmembers():
                    p = PurePosixPath(m.name)
                    if not (m.isfile() or m.isdir()) or '..' in p.parts or p.is_absolute() or p.parts[0] != '.cc':
                        raise Error('The checkpoint\'s sessions hold an unsafe entry: %s' % m.name)
            untar(snap / 'agent.tar.gz', Path(t2))
            shutil.copytree(Path(t2) / '.cc/projects', cc / 'projects')
        g.verify_tree(cc, snap / 'agent-files.sha256', agent=True)
        # the parent's interviews stay with the parent: their transcripts live outside any checkpoint and may have
        # grown since the fork point (OpenAI review 15:50Z, finding 2). Their rows leave the branch's interviews.tsv,
        # so E2a lists only the branch's own; BRANCH.json keeps them, and the setup commit shows them gone
        ivs = tmp / 'CONTROL/interviews.tsv'
        omitted = [r for r in ivs.read_text().splitlines() if r.strip()] if ivs.exists() else []
        ivs.unlink(missing_ok=True)
        # the fork point's checkpoint and the index up to it: step.sh continues that close's conversation
        snaps = tmp / 'CONTROL/snapshots'
        snaps.mkdir(parents=True, exist_ok=True)
        shutil.copytree(snap, snaps / label)
        lines = (src / 'CONTROL/snapshots/INDEX.tsv').read_text().splitlines()
        kept = [lines[0]]
        for r in lines[1:]:
            kept.append(r)
            if r.split('\t')[0] == label:
                break
        (snaps / 'INDEX.tsv').write_text('\n'.join(kept) + '\n')
        h = tmp / 'CONTROL/harness'
        changed = {}
        for name, text in (('publish.sh', PUBLISH), ('step.sh', STEP)):
            changed[name] = sha(h / name) if (h / name).exists() else None
            if name == 'step.sh' and not (h / 'step-parent.sh').exists():   # a branch of a branch has it already
                os.replace(h / 'step.sh', h / 'step-parent.sh')   # the parent's, unchanged, which the wrapper runs
            (h / name).write_text(text)
            os.chmod(h / name, 0o755)
        b = {'backend': 'claude', 'status': 'draft', 'source_run': source, 'checkpoint': label,
             'checkpoint_id': ck['checkpoint_id'], 'checkpoint_sha256': sha(snap / 'MANIFEST.sha256'), 'after_leg': label,
             'target_leg': leg, 'target_stage': stage, 'base_commit': base, 'prefix': prefix, 'created_utc': A.now(),
             'changes': {}, 'inherited': [r.split('\t')[0] for r in kept[1:]], 'interviews_omitted': omitted,
             'harness_changed': {
                 'CONTROL/harness/publish.sh': {'before_sha256': changed['publish.sh'], 'sha256': sha(h / 'publish.sh'),
                                                'why': 'the branch is committed to analysis/<run>, never to main'},
                 'CONTROL/harness/step.sh': {'before_sha256': changed['step.sh'], 'sha256': sha(h / 'step.sh'),
                                             'why': 'a guard before the parent\'s step.sh, now step-parent.sh: setup '
                                                    'published, publication not blocked, the first leg through legs.py'}},
             'deliveries': tree_hash(tmp / 'DROPS'), 'trusted': trusted_hash(tmp),
             'baseline': baseline_hash(tmp), 'inputs_version': INPUTS_VERSION}
        save(tmp, b)
        os.replace(tmp, dest)
    except BaseException:
        A.write(tmp / 'BUILD-FAILED.json', {'utc': A.now(), 'reason': 'Branch setup interrupted; preserved for inspection'})
        raise
    return {'run': new, 'branch': summary(b), 'new_turn_started': False,
            'login': 'The branch has its own Claude folder: log in once with  CLAUDE_CONFIG_DIR="%s" claude'
                     % (dest / 'CONTROL/.cc')}


# ---- the setup, while draft ----------------------------------------------------------------------------------
def destination(run, b, path, stage=None):
    """Where a supplied file goes, by the Codex rules (codex/runtime/branches.py destination())."""
    if not isinstance(path, str) or '\\' in path:
        raise Error('Use a relative POSIX path')
    p = PurePosixPath(path)
    if not path or p.is_absolute() or str(p) != path or any(x in ('..', '.') or x.startswith('.') for x in p.parts):
        raise Error('Unsafe branch file path')
    if stage:
        order = stage_order(run)
        if stage not in order or order.index(stage) < order.index(b['target_stage']):
            raise Error('Stage delivery precedes the branch start')
        if p.parts[0] == 'stages':
            names = [q.name for q in (run / 'DROPS' / stage / 'stages').glob('STAGE-%s-*.md' % stage)]
            if len(p.parts) != 2 or p.name not in names:
                raise Error('Replace the existing card filename for this stage')
        elif p.parts[0] not in DATA_FOLDERS:
            raise Error('Stage uploads accept its card or data folders, not tools or control files')
        root, key = run / 'DROPS' / stage, 'stage/%s/%s' % (stage, path)
    else:
        if p.parts[0] not in DATA_FOLDERS + ('out',) or len(p.parts) < 2:
            raise Error('Workspace uploads must name a file in a data folder')
        if p.parts[0] == 'out' and (p.parts[1].startswith('_') or p.parts[1] in ('PAUSE', 'diary', 'inbox', 'requests', 'responses')):
            raise Error('Cannot replace control files or the audit record')
        root, key = run / '00_GIVE-THE-AGENT', 'workspace/' + path
    if p.suffix.lower() in BLOCKED_SUFFIXES or p.name in SECRET_NAMES:
        raise Error('Upload data or Markdown cards, not executables, native state or credentials')
    q = (root / path)
    for ancestor in [q] + list(q.parents):
        if ancestor == run:
            break
        if ancestor.is_symlink():
            raise Error('Branch paths cannot contain links')
    return q, key


def verify_inputs(run, b, pending=None):
    """Codex's verify_inputs: the stage deliveries and the trusted harness as recorded, and, until the setup is
    published, the analyst's folder too. A branch-put that was interrupted is repeated before anything else:
    then everything but its own targets must be as it was."""
    if (run / 'BUILD-FAILED.json').exists():
        raise Error('Branch creation failed; inspect the preserved files')
    if b.get('inputs_version') != INPUTS_VERSION:
        raise Error('This branch was made before its inputs were frozen with their modes, arms and settings template '
                    '(5 October 2026); its hashes cannot be checked. Make it again from its checkpoint.')
    want = {'deliveries': b['deliveries'], 'baseline': b['baseline']}
    skip = {'deliveries': (), 'baseline': ()}
    p = b.get('pending_put')
    if p:
        if not pending or any(p.get(k) != pending.get(k) for k in ('path', 'stage', 'sha256')):
            raise Error('A branch-put was interrupted (%s); repeat it first' % p.get('path'))
        want = {'deliveries': p['deliveries_rest'], 'baseline': p['baseline_rest']}
        skip = {'deliveries': tuple(p['drops']), 'baseline': tuple(p['workspace'])}
    if tree_hash(run / 'DROPS', skip['deliveries']) != want['deliveries']:
        raise Error('Branch stage deliveries changed outside branch-put')
    if trusted_hash(run) != b['trusted']:
        raise Error('Branch harness, arms or settings template changed outside its recorded setup')
    unpublished = not (A.read(run / 'publication.json') or {}).get('setup_commit')
    if (b['status'] == 'draft' or unpublished) and baseline_hash(run, skip['baseline']) != want['baseline']:
        raise Error('Branch data changed outside branch-put')


def put(new, path, source_file, digest, stage=None):
    """A supplied file in place, while draft, its change recorded (before and after hashes)."""
    run = run_dir(new)
    b = branch_of(run)
    if not b:
        raise Error('%s is not an analysis branch' % new)
    if b['status'] != 'draft':
        raise Error('Branch setup is sealed; create another branch to change inputs')
    pending = {'path': path, 'stage': stage, 'sha256': digest}
    verify_inputs(run, b, pending)
    q, key = destination(run, b, path, stage)
    if sha(source_file) != digest:
        raise Error('The supplied file does not match its hash')
    targets = [(q, key)]
    if stage and handed(run, stage):
        # step.sh delivers a stage's drop only at the stage's first leg; for a stage already handed, the analyst's
        # folder holds the delivered copy, which the change replaces too
        targets.append((run / '00_GIVE-THE-AGENT' / path, 'workspace/' + path))
    drops = [q.relative_to(run / 'DROPS').as_posix() for q, _ in targets if (run / 'DROPS') in q.parents]
    work = [q.relative_to(run / '00_GIVE-THE-AGENT').as_posix() for q, _ in targets if (run / '00_GIVE-THE-AGENT') in q.parents]
    if not b.get('pending_put'):
        b['pending_put'] = dict(pending, drops=drops, workspace=work, deliveries_rest=tree_hash(run / 'DROPS', drops),
                                baseline_rest=baseline_hash(run, work))
        save(run, b)
    for q, key in targets:
        before = sha(q) if q.is_file() else None
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_file, q)
        os.chmod(q, 0o644)
        old = b['changes'].get(key, {})
        b['changes'][key] = {'before_sha256': old.get('before_sha256', before), 'sha256': digest,
                             'bytes': q.stat().st_size, 'utc': A.now()}
    b['deliveries'] = tree_hash(run / 'DROPS')
    b['baseline'] = baseline_hash(run)
    b.pop('pending_put')
    save(run, b)
    return {'run': new, 'paths': [k for _, k in targets], 'complete': True, 'new_turn_started': False}


def handed(run, stage):
    log = run / 'CONTROL/handover-events.log'
    return log.is_file() and any(r.split('\t')[1:3] == ['handed', stage] for r in log.read_text().splitlines())


def own_closes(run, b):
    index = Path(run) / 'CONTROL/snapshots/INDEX.tsv'
    rows = [r.split('\t')[0] for r in index.read_text().splitlines()[1:] if r.strip()] if index.exists() else []
    return [r for r in rows if r not in b['inherited']]


def at_close(run, label):
    """Nothing has moved since the close of label: it is the run's last event, no leg is prepared, and the
    analyst's folder is the checkpoint's (RUN.json's token counts aside)."""
    run = Path(run)
    log = run / 'CONTROL/handover-events.log'
    rows = [r for r in log.read_text().splitlines() if r.strip()] if log.is_file() else []
    if not rows or rows[-1].split('\t')[1:3] != ['closed', label] or (run / 'CONTROL/pending_launch.json').exists():
        return False
    g, snap = A.harness(run), run / 'CONTROL/snapshots' / label
    now, kept = g.inventory(run / '00_GIVE-THE-AGENT'), g.load_manifest(snap / 'fs.sha256')
    rj_now, rj_kept = now.pop('RUN.json', None), kept.pop('RUN.json', None)
    if now != kept or (rj_now is None) != (rj_kept is None):
        return False
    if rj_now and rj_now[2] != rj_kept[2]:
        with tarfile.open(snap / 'fs.tar.gz') as t:
            archived = t.extractfile('00_GIVE-THE-AGENT/RUN.json').read()
        try:
            return tokenless((run / '00_GIVE-THE-AGENT/RUN.json').read_bytes()) == tokenless(archived)
        except ValueError:
            return False
    return True


def check_leg(run, leg):
    """Before a branch's leg is prepared (legs.py new_leg): the setup is sealed and committed (Codex seals at the
    first leg), the inputs are as recorded, the first leg is the target leg, and no publication is blocked.
    Returns the publication's lines, if it published now."""
    run = Path(run)
    b = branch_of(run)
    if not b:
        return []
    lines = []
    pub = A.read(run / 'publication.json') or {}
    if not pub.get('setup_commit'):
        lines = publish(run.name)['lines']
        b, pub = branch_of(run), A.read(run / 'publication.json') or {}
    else:
        verify_inputs(run, b)
    if not own_closes(run, b) and leg != b['target_leg']:
        raise Error('First branch leg must be %s' % b['target_leg'])
    blocked(run, b, pub)
    return lines


def blocked(run, b, pub):
    """Codex's publication gate: the last close committed to analysis/<run>, and pushed when a remote is set."""
    own = own_closes(run, b)
    if own and own[-1] not in pub.get('commits', {}) and own[-1] not in pub.get('skipped', {}):
        raise Error('Git publication is blocked: %s is not on analysis/%s. Use legs.py publish-branch %s before advancing; '
                    'do not rerun analysis' % (own[-1], run.name, run.name))
    if pub.get('push') == 'failed':
        raise Error('Git publication is blocked: analysis/%s did not reach the remote. Use legs.py publish-branch %s before '
                    'advancing' % (run.name, run.name))


def check_step(name, args):
    """The branch's step.sh, before the parent's: a leg in Terminal waits for the setup and the publication, and
    the first leg starts through legs.py, which tells the analyst it is a branch."""
    run = run_dir(name)
    b = branch_of(run)
    if not b:
        return
    pub = A.read(run / 'publication.json') or {}
    if not pub.get('setup_commit'):
        raise Error('The branch is not prepared: legs.py prepare-branch %s first' % name)
    if not own_closes(run, b):
        if b['target_leg'] not in args:
            raise Error('First branch leg must be %s' % b['target_leg'])
        if '--prepare' not in args:
            raise Error('The branch\'s first leg starts through legs.py, which tells the analyst it is a branch: '
                        'legs.py open %s %s' % (name, b['target_leg']))
    verify_inputs(run, b)
    blocked(run, b, pub)


def notice(run, leg):
    """The text before the first message of the branch's first leg (Codex's notice, word for word)."""
    b = branch_of(run)
    if not b or b.get('status') != 'sealed' or leg != b['target_leg'] or own_closes(run, b):
        return ''
    return NOTICE % (Path(run).name, b['source_run'], b['after_leg'], ', '.join(sorted(b['changes'])) or 'No file overrides')


def summary(b):
    return {k: v for k, v in b.items() if k not in ('baseline', 'deliveries', 'trusted')}


# ---- publication ------------------------------------------------------------------------------------------------
@contextlib.contextmanager
def publication_lock():
    p = Path(os.environ.get('RPLACE_LEGS_DATA') or REPO.parent / '.rplace-claude-legs') / 'publication.lock'
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def files_of(top, run, prefix):
    """The branch run's files that main's .gitignore would keep if they were the parent's; never the login,
    the sessions, the handler's records, the checkpoints, an interview at any depth, or a credential."""
    rows = []
    for p in sorted(run.rglob('*')):
        rel = p.relative_to(run).as_posix()
        parts = rel.split('/')
        if p.is_file() and not p.is_symlink() and not (rel + '/').startswith(NEVER) and p.name not in SECRET_NAMES \
                and rel != 'publication.json' and not set(parts[:-1]) & PRIVATE_DIRS:
            if '\n' in rel:
                raise Error('A file name holds a line break: %r' % rel)
            rows.append((rel, p))
    skip = ignored(top, ['%s/%s' % (prefix, rel) for rel, _ in rows])
    out = []
    for rel, p in rows:
        if '%s/%s' % (prefix, rel) in skip:
            continue
        if p.stat().st_size > 95 * 1024 ** 2:
            raise Error('File exceeds the Git publication limit: %s' % rel)
        out.append((rel, p))
    return out


def commit_snapshot(top, parent, prefix, run, metadata, title):
    """A commit whose tree is the parent commit's with the prefix replaced by the branch run (codex
    publication.commit_snapshot): a temporary index, never the shared one."""
    with tempfile.TemporaryDirectory(prefix='git-analysis-') as tmp:
        index = Path(tmp) / 'index'
        git(top, 'read-tree', parent, index=index)
        old = git(top, 'ls-files', '-z', '--', prefix, index=index)
        if old:
            git(top, 'update-index', '--force-remove', '-z', '--stdin', data=old, index=index)
        files = files_of(top, run, prefix)
        blobs = git(top, 'hash-object', '-w', '--stdin-paths',
                    data=''.join(str(p) + '\n' for _, p in files).encode('utf-8', 'surrogateescape')).decode().split()
        if len(blobs) != len(files):
            raise Error('git hash-object returned %d hashes for %d files' % (len(blobs), len(files)))
        entries = ['%s %s\t%s/%s' % ('100755' if p.stat().st_mode & 0o111 else '100644', blob, prefix, rel)
                   for (rel, p), blob in zip(files, blobs)]
        blob = git(top, 'hash-object', '-w', '--stdin',
                   data=(json.dumps(metadata, indent=2, ensure_ascii=False) + '\n').encode()).decode().strip()
        entries.append('100644 %s\t%s/LINEAGE.json' % (blob, prefix))
        git(top, 'update-index', '-z', '--index-info', data=''.join(e + '\0' for e in entries).encode('utf-8', 'surrogateescape'),
            index=index)
        tree = git(top, 'write-tree', index=index).decode().strip()
        return git(top, 'commit-tree', tree, '-p', parent, data=(title + '\n').encode()).decode().strip()


def save_ref(top, ref, commit):
    current = git(top, 'rev-parse', '--verify', '-q', ref, check=False).decode().strip()
    if current and current != commit:
        raise Error('Ref already points elsewhere: ' + ref)
    if not current:
        git(top, 'update-ref', ref, commit, '0' * 40)


def remote_ref(top, ref):
    out = git(top, 'ls-remote', 'origin', ref, check=False).decode().strip()
    return out.split()[0] if out else None


def publish(new, label=None, kind=None, seal_draft=True):
    """Publish the setup once (sealing a draft), then the close label at that close; push the branch and its tags
    atomically when a remote is set. Prints publish.sh's kind of lines, which close.sh and legs.py read. Never
    commits a close the folder has moved past (Codex: publish at an idle branch boundary)."""
    run = run_dir(new)
    b = branch_of(run)
    if not b:
        raise Error('%s is not an analysis branch' % new)
    top = toplevel(run)
    lines = []
    ref = 'refs/heads/analysis/' + new
    with publication_lock():
        pub = A.read(run / 'publication.json') or {}
        if not pub.get('setup_commit'):
            if own_closes(run, b):
                raise Error('The branch\'s first leg ran before its setup was published, so the setup\'s state is gone; '
                            'make a new branch')
            if b['status'] == 'draft' and not seal_draft:
                return {'run': new, 'ref': ref, 'commit': None, 'new_turn_started': False,
                        'lines': ['  git: the branch is a draft; nothing committed (prepare-branch seals and publishes it)']}
            verify_inputs(run, b)
            was = dict(b)
            if b['status'] == 'draft':
                b.update(status='sealed', sealed_utc=A.now())
                save(run, b)
            try:
                meta = {'kind': 'analysis-setup', 'run': new, 'backend': 'claude', 'source_run': b['source_run'],
                        'after_leg': b['after_leg'], 'target_leg': b['target_leg'], 'checkpoint': b['checkpoint'],
                        'checkpoint_id': b['checkpoint_id'], 'checkpoint_sha256': b['checkpoint_sha256'],
                        'parent_commit': b['base_commit'], 'changes': b['changes'], 'harness_changed': b['harness_changed'],
                        'validation': 'Inherited trusted validators; prior results certify original inputs only'}
                commit = commit_snapshot(top, b['base_commit'], b['prefix'], run, meta,
                                         'Analysis %s: setup before %s' % (new, b['target_leg']))
                tag = 'refs/tags/analysis-checkpoints/%s' % A.identity(b['checkpoint_id'])
                save_ref(top, tag, b['base_commit'])
                pub = {'ref': ref, 'base_commit': b['base_commit'], 'setup_commit': commit, 'prefix': b['prefix'],
                       'pending_commit': commit, 'pushed_commit': None, 'checkpoint': b['checkpoint'], 'commits': {},
                       'skipped': {}, 'tags': [tag]}
                A.write(run / 'publication.json', pub)
            except BaseException:
                save(run, was)   # still a draft: nothing was published
                raise
            lines.append('  git: committed "Analysis %s: setup before %s"' % (new, b['target_leg']))
        if label and label not in b['inherited'] and label not in pub['commits'] and label not in pub['skipped']:
            g = A.harness(run)
            d = run / 'CONTROL/snapshots' / label
            status = 'paused' if kind == 'pause' else 'verified' if g.advance(run, label) else None
            if not (d / 'COMMITTED').is_file():
                raise Error('%s has no committed checkpoint' % label)
            if status is None:
                pub['skipped'][label] = 'its close cannot advance the run (forced, or validation incomplete)'
                A.write(run / 'publication.json', pub)
                lines.append('  git: %s not committed: %s; the next close\'s commit holds its files' % (label, pub['skipped'][label]))
            elif not at_close(run, label):
                raise Error('The run has moved on since %s, so the folder no longer holds that close' % label)
            else:
                meta = {'kind': status + '-leg', 'run': new, 'backend': 'claude', 'leg': label,
                        'checkpoint_id': (d / 'COMMITTED').read_text().strip(), 'parent_commit': pub['pending_commit'],
                        'native_history': 'Private checkpoint, not stored in Git'}
                leg = label.split('.', 1)[-1]
                commit = commit_snapshot(top, pub['pending_commit'], pub['prefix'], run, meta,
                                         'Analysis %s: %s %s' % (new, status, leg))
                pub['commits'][label] = commit
                pub['pending_commit'] = commit
                if kind in ('finished', 'interview-point'):
                    tag = 'refs/tags/%s/%s' % (new, label.split('.', 1)[0] if kind == 'finished' else leg)
                    git(top, 'update-ref', tag, commit)
                    pub['tags'] = sorted(set(pub['tags']) | {tag})
                A.write(run / 'publication.json', pub)
                lines.append('  git: committed "Analysis %s: %s %s"' % (new, status, leg))
        commit = pub['pending_commit']
        local = git(top, 'rev-parse', '--verify', '-q', ref, check=False).decode().strip()
        known = [pub.get('pushed_commit'), pub['setup_commit']] + list(pub['commits'].values())
        if local and local not in known:
            raise Error('Local analysis ref changed independently; inspect before publishing')
        git(top, 'update-ref', ref, commit, local or '0' * 40)
        if not git(top, 'remote', check=False).strip():
            pub['push'] = 'no remote'
            lines.append('  git: no remote set; committed locally')
        else:
            remote = remote_ref(top, ref)
            if remote and remote not in known:
                raise Error('Remote analysis branch changed independently; inspect before publishing')
            refs = ['%s:%s' % (t, t) for t in pub['tags']]
            r = subprocess.run(['git', 'push', '--atomic', 'origin', '%s:%s' % (commit, ref)] + refs, cwd=str(top),
                               capture_output=True, text=True, check=False, env=dict(os.environ, GIT_TERMINAL_PROMPT='0'))
            if r.returncode or remote_ref(top, ref) != commit:
                pub['push'] = 'failed'
                lines.append('  git: committed analysis/%s; push failed; publish-branch %s pushes it' % (new, new))
            else:
                pub.update(push='pushed', pushed_commit=commit, pushed_utc=A.now())
                lines.append('  git: pushed analysis/%s' % new)
        A.write(run / 'publication.json', pub)
    return {'run': new, 'ref': ref, 'commit': pub['pending_commit'], 'lines': lines, 'new_turn_started': False}


def main(argv):
    if len(argv) >= 2 and argv[0] == 'check-step':
        try:
            check_step(argv[1], argv[2:])
        except (Error, OSError, ValueError) as e:
            print('REFUSING: %s' % e, file=sys.stderr)
            return 1
        return 0
    if len(argv) >= 3 and argv[0] == 'publish':
        try:
            # a close never seals a draft: only legs.py seals, before the first leg (Codex's seal)
            r = publish(argv[1], argv[2], argv[3] if len(argv) > 3 else 'close', seal_draft=False)
        except (Error, OSError, ValueError) as e:
            print('  git: the branch\'s publication failed, nothing pushed: %s' % e, file=sys.stderr)
            return 1
        print('\n'.join(r['lines']))
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
