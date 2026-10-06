# How the case lead and its fleet remember

*Kind of page: reference.*

A room is coded by agents that do not keep anything in their heads between calls. What they know is on disk. This page says where.

## The room: STATE.json

[`STATE.json`](../../coder/rooms/armenia/STATE.json) is "the room's memory". `room.py status` rewrites it from the files (stage, branch, slices, verdict, codes). The scheduler adds what files cannot say: agents, notes, failures, `carried`. `start_yard_lead.py` records the lead's model, prompt version and store. `lead_archive.py` records the archive's path, sha256 and size, or, after a restore, `lead_store`. The paths in it are absolute paths on the machine that ran the room.

## The coders: journals and logs

Every agent works across many short processes. `emit` replays `out/_journal.jsonl` and `read.py` replays `out/_read.jsonl` on each call, so "the run state is on disk, not in your memory". An interrupted coder runs `read.py CORPUS state`; a non-zero cursor means it is resuming, and it carries on without re-reading.

A fleet coder sees its slice, the openings of earlier threads still running (marked as context), `brief.md`, and `timeline.md` and `lexicon.md` as the lead held them at dispatch. It is "not given any other coder's codes, case or notes". It has no saved native session: "Fleet coders retain their outputs and transcripts, without a resumable native session."

## The lead: ledger, notes, conversation

The lead's memory of the fleet is `out/ledger.md`, one entry per collected batch, kept by `fleet.py collect`, with the lead's strikes written under each. It keeps running notes in `out/_lead_notes.md`. The contract says why: "Your conversation will be compacted on a long run and a fork's lead has none; the ledger is what survives."

The lead also has a saved conversation. `codex_lead.py` runs it through the Codex app-server and, after each completed reply, commits a checkpoint of the whole store.

## The lead session store

A store at `_lead_sessions/<sub>-gpt56-calibration-v1/` holds:

- `STORE.json`: paths, model, effort, the Codex binary, the runtime fingerprint, the lifecycle text.
- `HEAD.json`: the last committed checkpoint.
- `native/lead/`: the lead's own Codex home (sessions, configuration, databases). The login file is copied in for a run and removed after.
- `workspace/room/`: the managed copy of the room; all coders and checks for this reading use it.
- `state/`: `runtime.json`, `lead.json` (thread ID, turn ID, final reply, history hash), `prompting.json`, `lead-opening.txt`.
- `objects/`, `checkpoints/`, `refs/`, `audit/` (named in CHECKPOINTS.md), and `RUNNING.json` while a turn runs.

## Resuming and forking

`turn` resumes the saved thread at its stable directory, checks the history hash, sends the message and checkpoints again. `fork --checkpoint C --name N` restores C and makes an independent native thread without a model turn. `restore` puts files and native state back "at the same absolute paths". In branch B the last `collect` stops before consolidation and is saved as `after-fleet`, the fork point. `room.py snapshot` and `fork` are older, filesystem-only, fresh-lead forks: they restore no conversation.

## Resume a lead from this repository

The code supports restoring an archive (`lead_archive.py restore`) and resuming a restored store (`codex_lead.py turn`). From the yard folder:

1. Join a split archive: `cat _lead_sessions/<sub>-gpt56-calibration-v1.tar.zst.part* > _lead_sessions/<sub>-gpt56-calibration-v1.tar.zst`, parts in order. Check `sha256sum` against `lead_archive_sha256` in `rooms/<sub>/STATE.json`.
2. Either `python3 -B _tools/lead_archive.py restore <sub>`, which checks the sha256, extracts with `zstd -qdc` and `bsdtar -xf`, rewrites `STORE.json` paths, updates `STATE.json` and deletes the archive; or extract by hand: `zstd -dc _lead_sessions/<sub>-gpt56-calibration-v1.tar.zst | tar -xf - -C _lead_sessions`.
3. `python3 -B _tools/codex_lead.py --store _lead_sessions/<sub>-gpt56-calibration-v1 status`, then `verify --checkpoint HEAD`.
4. `python3 -B _tools/codex_lead.py --store _lead_sessions/<sub>-gpt56-calibration-v1 turn --prompt-file follow-up.txt --label <new-label>`.

What blocks this in practice, from the code: both tools import `checkpoints.py`, and `turn --message collect` calls `verify_room.py`; both are in `_tools/`. But `codex_lead.py` refuses if the Codex binary's sha256, Python version, Python path or platform differ from `STORE.json` ("no silent upgrade allowed"). It needs a Codex login at `~/.codex/auth.json` or `--auth-source`. CHECKPOINTS.md says to keep "the original store path" because native history is not rewritten; the code rewrites only the descriptor paths. So a lead cannot be resumed from this repository alone on another machine: the files let you read the saved state (the conversation in `native/`, the checkpoints, the audit trail), and continuing it needs the same Codex build, a Codex login, and the original store path.

Checked against: _tools/lead_archive.py, _tools/codex_lead.py, _tools/room.py, _tools/start_yard_lead.py, CHECKPOINTS.md, CASE-LEAD-PROMPT.md, CONTRACT-case-lead.v32.md, CONTRACT-fleet-coder.v32.md, AGENT.v32.md, rooms/armenia/STATE.json
