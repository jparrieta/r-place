# CLAUDE.md for the analyst's sessions

You run on the Claude platform: after `AGENT.md`, read `PLATFORM-claude.md` once, at stage A1. It names
your models, routes and how legs open and close; everything else is shared with the Codex platform.

Read `AGENT.md` first. Then, in this order and nothing else by default: `out/_head.md`, the
stage file you were told to read, `python3 tools/mem.py diary --last 5`, `python3
tools/validate.py --open NN`.

Rules that bind every turn:

- Write as you work: `mem.py log` at every moment the stage file names. Never write to
  `out/diary/` by any other route.
- Read files through the verbs (`mem.py`, `cite.py`). A raw file above about 25,000 tokens is
  paged; a `Read` that returns without an end marker has been truncated.
- `out/_probe/` and `out/_transcripts/` are the harness's; they open to you at stage E1.
- Never delete a file; supersede it with a new name.
- Log and snap every categorization move when you make it (`mem.py log --kind move`, then
  `python3 tools/snap.py NN move-<move>-<n>`); a move does not close the leg.
- Close with `bash tools/done.sh NN` at the end of a pass, or earlier when you choose, and with
  `--cut <name>` only where the stage file names a cut. A leg that fails the close-check is not
  closed; read the failure in your next packet. The head is at most 3,000 words.

On compaction, the harness re-injects the head and the stage file before your next write; what
the compactor must preserve, in this order: the method question in one sentence; the current
account; the reasons for the last revisions; the contrary rooms; the next comparison. After it,
re-read the head and reconcile it with the diary before any other write.
