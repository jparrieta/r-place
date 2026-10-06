# The store: what each file is, and what none of them is

Built by `tools/build_store.py` at stage 00 from the coders' documents, one run per room.
Read-only: nothing in a run
rewrites it. `tools/mem.py` reads it one page at a time and overlays your own tier files from
`out/` at query time, so a placement, fourth-order theme or dimension shown by `mem.py` is always
the current one.

**The clock.** `hour` is hours since the canvas opened, 1490976000 UTC (2017-03-31 16:00).
Placement stopped at hour 73; the window ends at 97. Negative hours are the pre-event week.

**The limit that holds on every row that has a parent.** a reply is a reply: posted after, not caused by. An interval between two
posts is elapsed time, never the speed of a decision.

## Files

| file | one line per | keys |
|---|---|---|
| `codes.jsonl` | first-order concept (115388; 175 retracted by the coder and dropped) | `sub`, `code_id`, `theme_id`, `second_order`, `first_order`, `text` (the participant's words), `start`, `end`, `item_id`, `thread_id`, `item_kind`, `author`, `created_utc`, `hour`, `coord` (forest coordinate), `state` (coded / unjoined), `batch`, `discovered_at`, `minted_in_stage`, `exchange_id`, `note` |
| `themes.jsonl` | second-order theme (7844) | `sub`, `theme_id`, `second_order`, `theme_note`, `n_codes` (after retraction), `n_codes_coder`, `code_ids`, `items`, `threads`, `first_hour`, `last_hour`, `regrouped_from` |
| `items.jsonl` | item of a coded thread (158227; no body) | `sub`, `thread_id`, `item_id`, `coord`, `parent_id`, `author`, `created_utc`, `hour`, `state` (coded / bridge / removed / dropped), `codes`, `dt_parent_sec`, `dt_thread_sec`, `depth`, `meta` |
| `threads.jsonl` | coded thread (42906) | `sub`, `thread_id`, `title`, `opener`, `opened_hour`, `last_hour`, `n_items`, `n_coded`, `n_dropped`, `n_authors`, `depth`, `first_code_hour`, `last_code_hour`, `codes`, `themes`, `read`, `verdict`, `reason` (the coder's disposition), `op_score`, `op_stickied`, `op_distinguished`, `op_flair` |
| `rooms.jsonl` | room (705) | the window (`threads_total`, `items_in_window`), the coder's dispositions (`threads_disposed`, `threads_read_in_full`, `threads_triaged`, `threads_out_of_scope`, `threads_coded`), `n_subreddits_named`, `n_off_platform`, the store counts, the onset hours, `coded_authors`, `top1_share`, `herfindahl`, `n_named_neighbours`, `forest` (the header counts); and, once the build joins them, the six canvas fields (joined: 705 rooms, 0 with six nulls) |
| `pointers.jsonl` | pointer the coder wrote (20110) | as written, plus `sub`; `relations.py` builds the mention graph from it |
| `transitions.jsonl` | coded turn answering a coded turn | written by `tools/transitions.py` |
| `_unjoined.jsonl` | code whose item the forest does not hold (38) | `sub`, `code_id`, `item_id`, `thread_id` |
| `_retracted.jsonl` | code the coder retracted (175) | the line as the coder wrote it; not in `codes.jsonl` |

## What the record holds, and what it does not

The threads here are **the threads the coders' codes point at**, with every item of each such
thread (158227 items in 42906 threads), but not their text: the participant's words the
store carries are the coded passages (`codes.jsonl`: `text`, `start`, `end`), and `cite.py` quotes
from them. `rooms.jsonl` carries `threads_total` and `items_in_window` for the whole window and
the forest header of every `trees/<sub>.md` repeats the counts. The coder's own documents are in
`package/<sub>/`: the pre-event brief (705 present), the case account, and the codes,
themes, thread dispositions and pointers as the coder wrote them. A pointer with `relation` null
was named in the case account and carries no relation label.

`meta` on an item: `score` (kept at 0 and below), `distinguished`, `stickied`, `edited`,
`link_flair_text`, `author_flair_text`, `retrieved_on`. The score and `stickied` are snapshots
taken at retrieval, weeks after the event: lower bounds with no timing. `distinguished` is reliable.

## What is not here

No canvas field outside `rooms.jsonl` (rule 7: joined there by `--join-canvas`, shown by `mem.py
room`, withheld by `--no-canvas`; a use is declared, rule 7). No third-order theme, fourth-order theme or
dimension: those are yours, in `out/`, and `mem.py` joins them for you. No item body. No
interpretation.

## The transitions ledger (`transitions.jsonl`)

One line per coded turn that answers a coded turn: 62838 lines in 42906 threads of 694 rooms;
53976 are direct replies (`hops` = 1), the rest reach their nearest coded ancestor through uncoded
turns the forest kept; 5426 are the same author answering themselves. Median interval 3573.0 s.
`from_case_themes` and `to_case_themes` carry second-order theme ids. `mem.py after <sub>/<code_id>`
reads it per code; `mem.py pairs --level second|third|fourth|dimension` lifts it through your own tier files and
prints the limit with every table.

**The limit:** a reply is a reply: posted after, not caused by. An interval is elapsed time, never the speed of a decision.

## The mention graph (`relations.jsonl`)

One line per (room, other) pair a room's coder recorded: 8304 pairs from 695 rooms, 4700 naming a room
of this study, 2148 reciprocated (the other room's coder recorded this room too). Labels, the pair's
most frequent: mentioned-only 3531, negotiated 1769, asked-help-from 784, gave-help-to 628, attacked-by 618, allied 509, attacked 418, destroyed-carelessly 30, mourned 17. Off-platform pointers are 639 lines with `other` null. `adjacent` (canvas
adjacency) is null: no adjacency file was given.

**The limit:** a pointer is a mention the coder read and recorded, not the whole of a room's
dealings with another.

## neighbours.jsonl

Ordered room pairs that touch: 9018 (each pair written both ways). Sharing an artwork 140; bordering on the atlas outline 3146; overlapping 1834; named in the coders' record 7252; both on the canvas and named 1450. Rooms with at least one neighbour: 702 of 705; artworks with an outline and a room of this frame: 1148; atlas entries not joined to artworks.jsonl by name: 0.

The atlas outline is one annotator's, drawn after the event; a border is where two outlines meet, not a negotiation. A mention is a pointer a coder recorded.
