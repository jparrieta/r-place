# `package/store/rooms.jsonl`

One line per room of the frame: the census.

## What it holds

`sub`; `threads_total`, `items_in_window`; the coder's dispositions (`threads_disposed`, `threads_read_in_full`, `threads_triaged`, `threads_out_of_scope`, `threads_coded`); `threads_in_store`, `items_in_store`, `items_coded`; `codes`, `codes_retracted`, `themes`, `pointers`; `n_subreddits_named`, `n_off_platform`; `onset_first_code_hour`, `onset_median_code_hour`, `onset_last_code_hour`; `coded_authors`, `top1_share`, `herfindahl`; `n_named_neighbours`; `forest`; `brief`; `n_codes_mismatch_themes`; `thread_coded_share`, `item_coded_share`; after the join, the six canvas fields.

## Who writes it, and when

`build_store.py` at stage 00; `--join-canvas` adds the canvas fields.

## Why it exists

`counts.py` takes the census from it and FRAME.md names it as the list. Contract §5: `onset_first_code_hour` "is populated for every room" and carries the one clean contrast; `n_off_platform` goes with every verdict at the return. Rule 7 keeps the canvas fields here "and nowhere else". `mem.py facts` serves it field by field.

## Where

[package/store/rooms.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/rooms.jsonl).

Checked against: tools/build_store.py, tools/counts.py, tools/mem.py, CONTRACT-aggregator.md §5 and rule 7.
