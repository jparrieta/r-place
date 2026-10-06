# For agents: the yard handler

> **Layout in this repository (2026-10-02).** The yard's folders sit here under other names:
> `_instrument/` is `instrument/`, `_tools/` is `handler/tools/`, `_lead_sessions/` is `lead-sessions/`, and the
> scheduler's documents (CONTRACT-scheduler.md, CHECKPOINTS.md and the rest) are in `handler/`. `census/` and
> `rooms/` keep their names. The text below describes a working yard. The tools expect that layout
> (`_tools/` beside `_instrument/` and `rooms/`): to run them, copy these folders into a yard folder of
> yours under the yard's names. `handler/refresh_examples.py` refreshes `rooms/` here from the study's yard.

The scheduler's contract is [CONTRACT-scheduler.md](handler/CONTRACT-scheduler.md); how the yard works is [README.md](README.md). The case lead's instrument is `_instrument/v32/`.

- **Which rooms.** The population is `census/MASTER-census.csv`, `handable = 1`; [Manual/census.md](../Manual/census.md) says why. The scheduler codes the rooms in `STATUS.tsv` (rebuilt by `_tools/status.py`) from the bottom up, smallest first.
- **A room.** `rooms/<sub>/ROOM.md` is its front page, `STATE.json` its state. A verified room's run is in `run.tar.zst`; open it with `zstd -dc run.tar.zst | tar -x`, never in place.
- **Checking a room.** `python3 close_run.py . --record coder_corpus.jsonl --role lead` inside the unpacked run: the gate the room passed ([Manual/10-for-reviewers.md](../Manual/10-for-reviewers.md)).
- **Talking to a case lead.** `_tools/codex_lead.py` with the room's archive in `_lead_sessions/` ([CHECKPOINTS.md](handler/CHECKPOINTS.md)); it needs Codex.
- **Runners.** The launchers and checkpoints use Codex; the contracts, messages and checks do not ([README.md](README.md), "In Claude Code").
- **Do not** change the shipped example rooms. To build or run rooms of your own, copy the yard to a folder of yours and work there; unpack archives into a scratch folder.
