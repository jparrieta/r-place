# The v37 run

*Kind of page: explanation: the previous run, for comparison.*

The aggregator's previous run: `gioia-j-sonnet-v37-20260908`. It ran contract v37, the version before this repository's v38, and the v38 design work began by reading its handler log.

Not shipped. This repository carries one full run, v38's; earlier runs are described, not included. The v37 instrument's texts are in the [history bundle](../archive/instrument-history.tar.gz), under `aggregator/v37/`.

## What it was

One analyst, a Claude Code session on J's Mac, worked inside `00_GIVE-THE-AGENT/` and saw nothing else. A handler, a Cowork session with the whole run folder mounted, closed stages, took checkpoints and answered the analyst in files. J opened and closed the analyst's session in Terminal and made the author's judgements. The handover of 2026-09-08 records that "every role is on `claude-sonnet-5`", instrument v37 with fingerprint `2e1e4686828a3c1e…`, eighteen stages in the older numbering (01 to 18), declared fork points at the close of 01, 06 and 09, and per-stage token ceilings at 04, 10 and 14.

Three defects stopped the run from starting and were fixed before stage 01: the fence denied the analyst its own folder, the analyst inherited the account's claude.ai connectors, and its config folder had no login. No fork was taken at 01.

## What it reached and learned

The handovers stop at stage 02. The resume notes and the handler's close-out, which sits in the run under `CONTROL/handler-log/` and in the Claude project, carry it further: the run closed on 2026-09-21 after all eighteen stages, with eighteen committed checkpoints from `start` to `step-18`. Stages 07, 08 and 09 ran in one session and built the model; five model files are byte-identical from the stage 09 snap to the stage 18 snap.

What the close-out carried forward to v38:

- The stage file and the close-check were frozen apart; six validator amendments followed.
- Packets must be sized against the reading tool: packets of 142 to 329 KB failed 21 times at stage 14; rebuilt at about 50 KB, all fourteen returned first time.
- Build, dispatch, check: "a launch that dispatches does nothing else; a launch that thinks dispatches nothing".
- The cheap reader fleet did 87 per cent of the tokens for 12 per cent of the cost on three metered stages.

It also left open questions: which null model is declared first at stage 17, 290 of 2,703 case themes with no placement, and two ordering claims whose snaps were deleted and retaken.

## How to resume or fork one of its steps

From `RESUME/README.md` in the run folder:

1. Run `RESUME/open-stage.sh` for step-09, the close where "the model is freshest", or `open-stage.sh step-10` for another close. It restores the checkpoint into a new dated folder under `~/Jail/interviews/`, verifies it file by file, prints the session id and opens the Claude Code CLI. `NO_OPEN=1` restores without opening.
2. Paste `PREAMBLE.md` as the first message. Without it the analyst tries to run the next stage.

What the README says to know first:

- It runs on the subscription only, not through OpenRouter; a session cannot change route once served.
- It works only in the Claude Code CLI; the desktop app, the web and the editor extension keep their own session stores.
- Each restore is a fresh copy, about 165 MB for step-09, and took 43 seconds in the test of 2026-09-22.
- On macOS the restore needs `umask 077`, which `open-stage.sh` sets; `restore_stage.sh` creates two folders before extracting and their modes otherwise fail the check. `RESUME/diagnose.sh` names the tree that differs.
- Every checkpoint carries `session.boundary_verified: false`; the restore checks the boundary itself and refuses on a mismatch.
- The restored folder holds the stage files for 10 to 18. The sandbox denies them to the analyst, not to a person at the terminal.

`RESUME/NOTE-TO-THE-VISITOR.md` is the message to send someone who will talk to the resumed analyst. It warns that a shared session is write access, and that the copy holds the coded Reddit material with real usernames.

A fork, as distinct from a resume, went through v37's `fork.sh` and `restore_stage.sh`, which [TOOLS-STATUS.md](../aggregator/instrument/tools/TOOLS-STATUS.md) lists as not ported to v38.

## Where it lives

The run folder is 5.2 GB in 9,333 files. Its checkpoint tarballs, one per step, are each over 95 MB. It is not in this repository: the repository carries one run, v38's. The v37 instrument's own texts are in the [history bundle](../archive/instrument-history.tar.gz), under `aggregator/v37/`.
