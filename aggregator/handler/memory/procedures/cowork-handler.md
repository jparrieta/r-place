# How the handler works from Cowork

Target length: under 450 words. Written 2026-10-06 by the handler. Holds the procedures learned while running A1; HANDLER.md and LEGS.md hold the rest.

## Mounts

- Run every `legs.py` client from the Jail mount: `cd $HOME/mnt/Jail/r-place`. From the r-place mount alone the client misses the heartbeat in `Jail/.rplace-claude-legs/` and says the handler is not running.
- The orchestrators' messages are in `$HOME/mnt/Jail/Orchestrator/messages/` (or the Orchestrator mount).
- The device shell stops after about three minutes. `run` takes no `--wait`: wrap it as `timeout 150 python3 ... run ...`. `wait` takes `--timeout`.

## Never

- No git from the Cowork shell, even with delete permission: on 2026-10-07 git still could not unlink inside `.git` (HEAD.lock, next-index lock, maintenance.lock, tmp objects) and the locks had to be moved to `Jail/_to_delete/`. Give J the commands instead. A `git status` there left an empty `.git/index.lock` it could not remove (2026-10-06 12:12Z), which would have failed `publish.sh`'s `git add`. It was moved to `Jail/_to_delete/r-place/.git/index.20261006T121237Z.lock` with a WHY.tsv line.
- No `mem.py` or other run tool from the handler: they write read-logs into the run.
- Never read `CONTROL/.cc`. Usage per leg comes from `CONTROL/legs/actors/<leg>/turns/<turn>/result.json`.
- Moving a file aside: check the target path first; if taken, put the UTC time before the extension (HANDLER.md rule 1). A plain `mv` overwrites.

## Following a list

- `scripts/tick.sh [SECONDS]` (copy it to the session's home first): one `wait`, the status, new closes with close-status, git lines and cost, any `guard.log`, defects and asks counts, and a scan of the chat for refusals and for any line where the analyst says it cannot reach J. Keep SECONDS at 100 or less, so the call ends inside three minutes.
- At each close: a diary line (checkpoint, minutes, cost increase, refusals) and a short report to J.
- Stop rule during A1 (J, 15:36 Berlin): stop the list only when a close cannot commit or push. Report everything else.
- `total_cost_usd` in result.json adds up across legs; a leg's cost is the increase over the previous leg's.

## Questions and words to the analyst

- Never answer the analyst. Draft for J, pass his approved words verbatim with `legs.py answer` or `say`, and record the decision in DECISIONS.tsv.

## Before a compaction or at session end

- Write a handover in `handovers/` with where the run stands, what is open and what to read first; bring the diary up to date.

## Tick interval (J, 2026-10-06 22:31 Berlin)

- One tick every 600 s: run `tick.sh 60`, report any close, then schedule the next tick with a `send_later` of 10 minutes back into the session, and end the turn. A close is reported at most about ten minutes late.

## At every close: omissions as well as additions (2026-10-07)

The audits check that what the analyst added comes from the record. They do not see what it left out. At every close, read the reasons the analyst logs for leaving content out, softening it or keeping a note as it stands (grep the leg's diary notes for "left", "kept minimal", "not put back", "omitted"). A reason that is not the study's goes to J at once. J, 7 October 2026: "national elements are very important here", and "we need to get as much variance on organizing behavior early on so that later we have enough to create the model".

## At every B1 close: reading depth (2026-10-07)
Run `python3 handler/memory/scripts/b1_depth.py <leg's events.jsonl>` (from the run folder). It sums the tool output the analyst saw between room-boundary logs and sets it against the room's codes plus second-order themes. Read whole, a leg shows about 55 to 90% of those bytes (large rooms lower, as the codes JSON carries quotes the print omits; for a room under 50%, compare with the full print of out/_analysis/b1_room.py) (B1b-02 59%, B1b-05 87%); below about 40% the analyst is reading headers and grepping concepts (B1b-03 36%, B1b-04 29%), and the read log does not show it. Shallow reads hide new kinds and bias the stopping rule toward an early stop: act at once (handler message quoting the stage), tell J, leave rereads to J. J (19:17): "well done with the intervention".
