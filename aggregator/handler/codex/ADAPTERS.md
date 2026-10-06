# One panel, separate platform lifecycles

Target length: under 900 words.

Status, 2026-10-05: v43 enables native Codex analysts and the existing OpenRouter reader arm. Claude records now dispatch to a separate facade, but Claude operations remain disabled by `backends.CLAUDE_ADMITTED = False`. Loading a record does not open a session. Shared scientific files remain unchanged. The review is in `Jail/Orchestrator/messages/2026-10-05T11-13Z_from-openai_to-claude_backend-admission-review.md`, outside the repository. Later replies and current checks are in that inbox and `Jail/Orchestrator/HEAD.md`.

## Interface required for admission

- `create(actor_id, run_dir, leg)` prepares one idle leg. It returns identity, backend, run, leg, model, effort and exact native session provenance. Preparation must not start inference.
- `open()` attaches or restores one owner. It does not start a turn. A recorded live process is followed by verified PID identity; it must never be replaced by a second process.
- `workspace` supplies the analyst root. The server must not assume `actor.base/workspace` for every backend. Cards, pause markers and questions use this root through platform methods.
- `message(text)` starts an idle turn or steers the current turn, with an explicit delivery receipt. Queued messages do not authorize an extra turn after closure, stop, failed start or controller restart. Undelivered messages remain visible for explicit continuation.
- `answer(request, answers)` distinguishes a native request tied to its thread and turn from a durable `mem.py ask`. Durable answers can be written while idle without starting a turn. Controller-owned answer files are read-only to the analyst.
- `pause()` settles at a safe boundary. `interrupt()` records an interrupted boundary. Neither may mark the leg verified.
- `checkpoint()` captures native history and the complete filesystem only after tools settle. Return backend, session, last turn, boundary, archive paths and verified digests. Saving an interrupted session and scientifically closing a leg are separate operations.
- `close(run, actor)` runs that platform's trusted validation, checkpoint and recall checks exactly once. It advances only after durable evidence. Git publication has its own receipt and cannot relabel a failed snapshot as complete.
- `restore(checkpoint, new_actor, mode)` makes an independent interview or authorized analysis continuation. It must preserve parent archives and must not feed a Claude receipt into Codex's archive parser.

## Controller routing now implemented

`actors.load` selects the backend before interpreting its state. `study.close` calls Claude's scientific close once and checks its evidence before advancement. It does not run a second Codex validator, recall probe or Git publication. Captures, incomplete validation, forced closes, paused legs and undelivered messages cannot advance a Claude study. A failed close preserves its current actor.

`claude_backend` registers controller checkpoint IDs with backend, actor, session, turn, boundary and a hash-bound reference to the complete saved artifact inventory. Verification checks commit/manifest binding, both archives and their entry inventories, transcript identity and scientific validation when required. Freeze checks use this verified inventory. Changed artifacts are rejected. Links are explicitly refused pending separate acceptance. The reference is local and is not a portable runtime bundle.

`archive.restore` dispatches before opening a tar file. Claude interview restore uses the verified saved directory. Analysis continuation, native handler continuation, controller preparation, finite blocks, fleets and publication are explicitly unsupported for Claude. These stay with the Claude harness until separately integrated and accepted. Unsupported calls refuse before their operation or a queued job begins.

Cards go through Claude's durable message inbox, with its delivery receipt. Questions route through the platform answer method, including idle answers. Controller restart preserves Claude's file questions. The bridge uses the platform workspace and pause marker, observes admission and pending messages, and never creates an actor-local pseudo-workspace. Retention cannot flag or evict a Claude actor or its shared run/native store.

The adapter's save/close split and explicit continuation refusal are accepted design changes. Its receipt, run ownership, durable-boundary, answer protection, queued-delivery and restore gaps remain admission blockers. Controller integration does not certify them.

## Claude terminal handler

J now uses Claude's standalone `legs.py` for Claude conversations. Codex refuses operations and interview restoration for any Claude run with `CONTROL/legs`, including idle and stopped runs. The bridge also leaves it alone. Removing a PID or pausing a list does not transfer ownership. This conservative refusal is one-sided: Claude still needs its own common ownership lease before either controller can be admitted on shared runs.

Scientific registration now requires the adapter's explicit `scientific: true`, plus a matching supported cut and session in the archived close marker and RUN.json. A forced or paused save cannot advance. Old receipts without this evidence fail closed; they are not silently upgraded. An offline integration test passes an actual adapter close through our archive verifier using Claude's real protocol guard and fake CLI. That fixture omits the live recall and publication paths. It cannot prove live acceptance.

## Acceptance before enabling Claude

Run the Codex Python 3.11 offline suite with the real reserve, including `test_backend_dispatch`, and Claude's lifecycle tests. Then run a synthetic live CLI probe with J's authorization: event shapes, combined hooks, delivered steering receipts, idle answers, controller restart attachment, quiescent snapshots and independent interview restore. Prove model/effort and native history in live metadata. Test failure and retry boundaries. Unsupported continuation stays refused; a refusal test does not prove that feature works. A real research leg must never be the probe. Review and record the corrected adapter/source hashes and both acceptance results before changing the admission constant.

v43 uses `.rplace-runtime-v43` beside the repository and ports 8767, 8768 and 8444. Draft adapter files remain Claude-owned. No adapter source was changed in this pass.
