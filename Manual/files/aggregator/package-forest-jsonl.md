# `package/forest.jsonl`

Every coded thread of every room as a reply tree, in one file.

## What it holds

One line per thread: `thread_id`, `community`, `title`, `hours_since_open`, `n_items`, `n_coded`, `n_dropped`, `retrieved_on`, and `tree`, a nested node with `coord` (Dewey; "0" is the submission), `item_id`, `parent_id`, `author`, `state` (coded, bridge, removed, dropped), `collapsed_n`, `dt_parent_sec`, `dt_thread_sec`, `code_ids`, `labels`, `sequence`, `coverage`, `meta` and `children`. The build adds `sub`.

## Who writes it, and when

`build_store.py` at stage 00 writes each room's `forest/forest.jsonl` from the coders' input into this one file, and derives the store's `items.jsonl` and `threads.jsonl` from it. `transitions.py` reads it to build the transitions ledger.

## The depth cut

Reply chains deeper than 490 are cut in this file, and only here. Each level of a tree is two levels of JSON, and the Python the repository pins (3.11) stops reading near 1,000, so a tree deeper than about 496 cannot be read. Only r/counting has such chains: members reply to each other one number at a time, and five of its threads reach 492 to 1,004 levels. `import_rooms.py` (`CUT_DEPTH`) cuts them when it renders the room, on J's instruction of 26 September 2026 to cut at 500; 490 keeps a margin under the limit.

- The node at depth 490 keeps its place and gains `cut_below`: `n_items` and `n_coded`, the replies removed under it. The thread gains `cut_at_depth`, `n_cut` and `n_coded_cut`.
- r/counting loses 1,564 of 6,242 items here, 38 of them coded. The 38 codes stay in `codes.jsonl` with their text, item and thread; the store lists them in `_unjoined.jsonl`, and the room's `tree_index.json` still gives each one's coordinate.
- The whole forest is kept beside the cut one, as the room's `forest/forest.uncut.jsonl` in the coders' input (`run/INPUT/coders/rooms/counting/`). No tool reads it; it is there for a reader on Python 3.12 or later, which opens the full depth.
- The room's `tree_index.json` and `trees/counting.md` are not cut: both are flat, one entry or one line per item, and hold every reply. The header counts (`n_items`, `n_coded`) are the uncut ones.

## Why it exists

METHOD: in Van de Ven and Poole's grammar "the forest is that grammar, and a coded turn is an incident." STANDING §1: "The forest is the coded record's shape", and "A reply is a reply": the tree shows order, not cause.

## Where

[package/forest.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/forest.jsonl).

Checked against: import_rooms.py, tools/build_store.py, tools/transitions.py, METHOD.md, STANDING-INSTRUCTIONS.md §1, package/forest.jsonl.
