# r/blackmirror

| | |
|---|---|
| items in the 97-hour window | 659 |
| threads with an in-window item | 108 |
| chars of people's text in window | 108020 |
| items in the seven days before | 1688 |
| brief | to write |
| expected branch at threshold 500 | B, about 2 slice(s) |

What is here: `instrument/` (v30, whole), `record/coder_corpus.jsonl.gz` (the cut the coders
read; `run/` is built from it), `record/preweek.jsonl.gz` (what the brief writer reads),
`brief/` (the brief stage; `brief/out/brief.md` when one exists), and once started `run/`,
`snapshots/`, `forks/`. `STATE.json` is the room's memory; `room.py status` reads the files and
rewrites it.

To run this room, from this directory (`T` is `../../_tools/room.py`):

    python3 $T status
    python3 $T brief --model <id>          # only if the brief is to write; then launch the
    python3 $T message brief               #   brief writer with this message; then `check`
    python3 $T run --model <id>            # builds run/ from the record and the brief
    python3 $T message lead                # launch the case lead with this message
    python3 $T message coder --batch 01    # branch B: launch each coder with this, in turn
    python3 $T check --batch 01            # after each coder, before the lead collects
    python3 $T message collect --batch 01 --summary "..."   # to the lead
    python3 $T snapshot after-fleet        # when the last coder is collected (the fork point)
    python3 $T message finish --batch NN   # the lead's step 4 and 5, or:
    python3 $T fork <name>; python3 $T message fork --fork <name>
    python3 $T check                       # when the lead has closed

`../../CONTRACT-scheduler.md` says what the scheduler does between these commands and what it
looks for. `../../README.md` says how to do it in Claude Code or any other agent runner.
