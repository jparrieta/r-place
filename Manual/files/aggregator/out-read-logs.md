# `out/_mem_reads-NN.jsonl` and out/_cite_reads-NN.jsonl

The read logs: one line for every call to `mem.py` and `cite.py`.

## What it holds

`_mem_reads-NN.jsonl`: `t`, `stage`, `verb`, `args`, `opts` (every option that differs from its default), `offset`, `limit`, `lines` served, `total`, and `refused`. `_cite_reads-NN.jsonl`: `t`, `stage`, `opts`, `verdict`, and `cited` (the `sub/code_id` of each quote returned). NN is `--stage`, else the `.stage` file the harness writes, else `$STAGE`.

## Who writes it, and when

The tools themselves, on every call; the analyst never writes them by hand. A helper's reads through the verbs are logged under the analyst's stage.

## Why it exists

Rule 1: "The log is an output ... Where your account of your reading and the log disagree, the log is right." The probe scores "the last three rooms you opened" from the `room` reads. E1 counts rooms read whole from the `room` and `forest` records, and A1 reports what it read "from the logs and not from memory".

## Where

[out/](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/) (the files appear at the first call of each stage).

Checked against: tools/mem.py, tools/cite.py, tools/probe.py, CONTRACT-aggregator.md rule 1, stages/STAGE-A1-reading-room-notes.md, stages/STAGE-E1-formalizing-audit.md.
