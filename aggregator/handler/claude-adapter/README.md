# Claude adapter for the OpenAI controller

Target length: under 1,350 words. As it stands on 6 October 2026.

Status, 6 October 2026: `legs.py` (LEGS.md) runs the v43 run's Claude legs with this actor, without OpenAI's controller, which keeps Claude refused until its own acceptance. Offline tests 20 of 20. Live on J's Mac, claude 2.1.289: `probe.py` 9 of 9 (5 October) and `probe_lifecycle.py` 14 of 14 (6 October). The run's harness is v43.2, whose `close.sh` counts a forked leg's own messages.

## Why

J, 2026-10-03 and 2026-10-05: Claude legs start, continue, pause and take messages without the terminal, several runs at once.

## Files

| File | What it does |
|---|---|
| `actor.py` | `ClaudeActor`, the controller's actor interface for a Claude leg or interview; `create()`, `close()`, `restore()` |
| `stream.py` | `Translator`: Claude stream-json into the panel's event names |
| `inbox_hook.py` | PostToolUse hook: gives the analyst J's messages in the middle of a turn, with a receipt |
| `probe.py` | live check of the raw CLI: stream shapes, the hook mid-turn, helper prompts, SIGINT and resume |
| `probe_lifecycle.py` | live acceptance of the actor itself in a synthetic run (below) |
| `legs.py`, `LEGS.md` | the leg handler for Claude Code and Cowork: open, close and run legs, and talk to any of them |
| `branches.py` | analysis branches as the Codex controller makes them: a new run from a verified close, committed to `analysis/<run>` (LEGS.md) |
| `tests/` | offline tests, a stand-in CLI, and `harness_stub.py`, a stand-in step.sh and close.sh that builds a complete snapshot |

## The interface (ADAPTERS.md)

| Call | What it does |
|---|---|
| `create(actor, run, leg)` | the run's `step.sh LEG --prepare`, then the store; no inference. The state carries the leg, model, effort and `provenance` (session, mode, parent, launch id). |
| `open()` | takes the one owner lease; follows a live process of the recorded turn (`attach`, by PID and start time); refuses a second owner while a process runs outside a recorded turn |
| `workspace`, `capabilities()` | the analyst's root (the run's `00_GIVE-THE-AGENT`, or an interview's copy) and what this backend can do. Cards go through `message()`. |
| `message(text)` | idle: starts a turn, carrying anything queued (`delivered_with_prompt`). During a turn: queued (`delivery: pending`) until the hook delivers it beside the next tool result, with a receipt (`receipt(id)`). Refused after the close. |
| `continue_queued()` | J's explicit word to send what waits as a turn of its own; nothing queued ever opens a turn by itself |
| `carry()` | for legs.py: J's messages still waiting when a leg has closed, marked carried, for the next leg's first message |
| `answer(key, answers)` | a `mem.py ask` answered: `out/_answers/<id>.md` written now, mode 444, never starting a turn; the analyst hears it with its next tool result or next turn |
| `pause()` | `.pause` in the folder and a note to the analyst |
| `interrupt()` | SIGINT, then SIGTERM, then SIGKILL; records an interrupted boundary. |
| `checkpoint()` | saves only, while the run is at this leg and its lock free: once the turn's process group is gone, the folder and the leg's session go to `captures/<time>-<turn>/` in the store, verified entry by entry. Never `close.sh`, never closed. |
| `close(force=False)` | the scientific close, once: the run's own `close.sh` (confirm, recall probe, trusted check, model audit, snapshot). The leg counts as closed only when the snapshot verifies whole (Receipts). A second call verifies the files again, returns the same receipt and runs nothing. A leg whose last turn did not complete needs `force`, recorded. |
| `restore(saved, new_actor, mode)` | `interview`: a copy of the saved folder in `interview-workspaces/<label>__<fork>/`, its session in `projects/iv-<fork>`, forked on its first turn, recorded in `CONTROL/interviews.tsv`. `continuation` is refused before anything is written. |
| `final()` | the last turn's result text |

A failed session confirmation, a CLI that ran another session than the leg's, or a turn that added a row under another session or a reply from another model than the arm's, or did not end on a new reply, fails the boundary (`status: failed`), whatever the result line said, on every turn. A turn that ends while another owner holds the run's lock is `uncertain`: nothing of the run is written until the lock is free.

## Receipts

Every receipt carries `backend: claude` and `format: rplace-claude-v1`, so the controller never hands it to the Codex archive parser.

- **Save** (`checkpoint()`): `kind: capture`, actor, session, last turn, boundary, `archive`, the `digests` of its six files, `verified: true`.
- **Close** (`close()`): `kind: close`, label, `checkpoint_id`, `snapshot` (path within the run), session, last turn, `digests`, `verified`, `scientific`, `cut`, `forced`, the log, and `publication`: publish.sh's report (`committed`, `pushed`, `committed, no remote`, `committed, push failed`, `no repository`, `nothing new`), parsed from its own lines. A failed snapshot exits before publication runs, so publication cannot relabel it.
  - `verified`: the receipt exists only if `MANIFEST.sha256` names every file of the snapshot and nothing else; the ten files a close holds are there; each matches; `COMMITTED` names checkpoint.json's `checkpoint_id`; the label, kind and session are the leg's; and the harness's `verify_checkpoint` passes (both archives entry by entry, the transcript at its boundary).
  - `scientific`: the harness's own `advance` rule (not forced or paused, validation complete). Only such a close advances a run.

## What the panel shows

`stream.py`'s docstring: the analyst's words, every tool call as one row, every helper's full prompt and reply, compactions and refusals as rows, never its thinking. A question (`mem.py ask`), an answer and a delivery are `item/tool/requestUserInput` (`isBlocking: false`), `rplace/questionAnswered` and `rplace/messageDelivered`.

## Verified live, and not

Verified on claude 2.1.289, in the probes' synthetic run: the stream's shapes; a message mid-turn delivered by the hook, with its receipt written outside the sandbox; live metadata naming session and model; a fork's history told by message ids; a fresh Claude folder (`CLAUDE_CONFIG_DIR`) needs its own login, once.

Not verified:
- That the CLI merges hooks from `--settings` with the project hooks of the research run itself.
- That the effort level holds: it is passed as `--effort`, and the stream does not report it back.

## Live acceptance, on the Mac

```
python3 aggregator/handler/claude-adapter/probe.py --model sonnet
python3 aggregator/handler/claude-adapter/probe_lifecycle.py --model claude-sonnet-5-5 --effort low
```

`probe_lifecycle.py` takes a full model id, since the close's model audit, as close.sh's, accepts a served model only when its name starts with the arm's. It builds a synthetic run in the controller's data folder (never a research run) with the real `protocol_guard.py`, `pretool_guard.py` and settings template, and `tests/harness_stub.py` as `step.sh` and `close.sh` (a complete snapshot; no snap, recall probe or publish.sh). In about six short turns it checks every call above: preparation without inference, a message mid-turn with its receipt and the code word quoted back, the session and model in live metadata, the event shapes, an idle answer, a restart that attaches to a running turn, a save that is not a close, a refused continuation, an interview that remembers, a failed start and its retry, and the close run once.

The synthetic run's Claude folder starts empty; if it cannot answer, the probe says how to log in. On the Mac the login is no file, so `--login-from` cannot copy it: log in once into the synthetic run, which the probe reuses. A dry run with the stand-in CLI passes every check except the interview's memory, which the stand-in cannot have.

## Offline tests

```
python3 aggregator/handler/claude-adapter/tests/test_adapter.py
python3 aggregator/handler/claude-adapter/tests/test_legs.py
```

## What OpenAI adds

Asked 2026-10-04, split 2026-10-05. Their `codex/runtime/claude_backend.py` and `backends.py` (2026-10-05) dispatch on `backend: claude` and verify Claude receipts apart from Codex archives. They keep Claude refused (`CLAUDE_ADMITTED = False`) until acceptance, and refuse Claude's prepare, blocks, branches, fleet, retention and continuation.

One study record names each leg's backend. Their data folder stays `.rplace-runtime-v43` beside the repository; `legs.py` keeps its records in each run's `CONTROL/legs/`.
