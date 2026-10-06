# `out/_snap/`

Hashes of `out/` under a name: what existed when.

## What it holds

Files `NN-<label>.sha256`, each a header line and one line per file in `out/` with its sha256, size, the snap time and its path. Labels seen in the sources: `<leg>-<UTC stamp>` or `cut-<cut>-<leg>-<stamp>` at every close, and `move-<move>-<n>` for a move.

## Who writes it, and when

`close.sh` takes one at every close with the trusted `snap.py`. The analyst takes one for each categorization move (`snap.py NN move-<move>-<n>`); contract rule 18: snaps are write-once, and nobody deletes one.

## Why it exists

A move snap lets "a reviewer find the state before and after" (STANDING §2); E1 checks every move snap from C2 to D3 against `history.jsonl`. The analyst may read `_snap/` at any time (STANDING §2: "read them when you like"); it holds hashes only, so `protocol_guard.py` closes only `_probe` and `_transcripts` before E1.

## Where

[out/_snap/](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/_snap/).

Checked against: tools/snap.py, harness/close.sh, harness/protocol_guard.py, CLAUDE.md, STANDING-INSTRUCTIONS.md §2, CONTRACT-aggregator.md rule 18, stages/STAGE-E1-formalizing-audit.md.
