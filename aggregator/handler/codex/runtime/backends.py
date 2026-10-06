"""Platform routing and admission, without loading a native runtime on inspection."""
import importlib.util
from functools import lru_cache
from .common import *

# Change only after the offline and authorized synthetic live checks in ADAPTERS.md.
# Loading records is allowed now. It is not permission to run the draft adapter.
CLAUDE_ADMITTED = False
CLAUDE_BLOCK = 'Claude lifecycle admission is pending. See ADAPTERS.md and the 2026-10-05 backend review.'
CLAUDE_UNSUPPORTED = {'prepare', 'branch', 'blocks', 'fleet', 'handler', 'retention', 'continuation', 'publication'}


def name(state):
    backend = state.get('backend') or 'codex'
    if backend not in ('codex', 'openrouter', 'claude'):
        raise Error('Unknown backend: ' + str(backend))
    return backend


def require(state, operation):
    if name(state) != 'claude':
        return
    if operation in CLAUDE_UNSUPPORTED:
        raise Error('Claude does not support controller ' + operation + '. No platform operation was performed.')
    if not CLAUDE_ADMITTED:
        raise Error(CLAUDE_BLOCK)
    run = state.get('claude_run')
    if run:
        owner = inside(run) / 'CONTROL/legs'
        # The terminal handler keeps ownership between turns and after restart.
        # A PID or a running-job flag alone cannot establish a safe transfer.
        if owner.exists() or owner.is_symlink():
            raise Error('This run belongs to the Claude standalone handler (CONTROL/legs). '
                        'Use that handler; controller ownership transfer is not supported.')


def allowed(state, operation):
    try:
        require(state, operation)
        return True
    except Error:
        return False


def workspace(actor):
    if name(actor.state) == 'claude':
        return inside(actor.workspace)
    return actor.base / 'workspace'


def pause_marker(actor):
    return workspace(actor) / ('.pause' if name(actor.state) == 'claude' else 'out/PAUSE')


def capabilities(state):
    backend = name(state)
    error = None
    try:
        require(state, 'open')
    except Error as exc:
        error = str(exc)
    return {'backend': backend, 'admitted': error is None,
            'native_questions': backend == 'codex', 'durable_questions': backend in ('codex', 'claude'),
            'controller_retention': backend != 'claude', 'analysis_continuation': backend == 'codex',
            'publication_owner': 'harness' if backend == 'claude' else 'controller',
            'admission_error': error}


def require_run(run, operation):
    s = read(DATA / 'runs' / identity(run) / 'state.json', {})
    require(s, operation)
    for row in s.get('legs', {}).values():
        require(row, operation)
    # Legacy imported runs may have no backend tag. Check their actual actors too.
    for aid in {s.get('active_actor'), *[r.get('actor') for r in s.get('legs', {}).values()]} - {None}:
        require(read(actor_dir(aid) / 'state.json', {}), operation)


@lru_cache(maxsize=1)
def claude_module():
    path = CODEX.parent / 'claude-adapter/actor.py'
    spec = importlib.util.spec_from_file_location('rplace_claude_adapter', path)
    module = importlib.util.module_from_spec(spec)
    # Adapter imports its own sibling modules. No executable or session is opened.
    spec.loader.exec_module(module)
    return module
