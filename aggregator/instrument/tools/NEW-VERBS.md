# New and changed verbs and options, v38 tools pass (2026-09-25)

One line each, in the form of STANDING-INSTRUCTIONS §1's verb list, for merging into STANDING §1,
HOW-TO-RUN.md and the stage files. Tiers: first-order concept (<sub>/cNNNN), second-order theme
(<sub>/tNN), third-order theme (T3-NNN), fourth-order theme (T4-NNN), aggregate dimension (D1).

```
python3 tools/mem.py <verb> ... --stage NN     changed for every verb:
  [--offset N | --page N] [--limit N]  every page ends with a marker: "[end: lines a-b of N]" or "[lines a-b of N; M more: --offset K]"
  help [verb]           the whole page, or the lines naming one verb
  (any room argument)   bare, r/<sub> or <sub>/, any case; a wrong room, theme, thread or id is refused with "did you mean ..." and exit 1
  (the read log)        out/_mem_reads-NN.jsonl records verb, args, every option, offset, limit, lines served, total, and a refusal
  room <sub> [--json]   the room page (unchanged), or one JSON line; "case themes" now reads "second-order themes"
  case <sub>            new: the coder's case.md, paged
  canvas <sub>          new: the six canvas fields, each linked artwork's placements by hour as a bar aligned like `when` (freeze at h73), the share of the room's region placed by its window and its pre-event members (pixels.csv), and the manifest's caveat
  compare <sub> <sub> [--grep re]   new: two rooms before any placement: facts, `when`, second-order themes, named rooms, canvas, and concept labels matching --grep
  when <sub>            changed: the axis under the bar now matches the 4-hour bins (0, 24, 48, 72, 96; ^ freeze h73)
  forest <sub> [id]     changed: a thread the forest lacks is refused with the nearest id
  codes --sub S [--second tNN]   renamed: --second (old --case-theme still works)
  codes --third <T3> | --fourth <T4> | --dimension <D>   renamed and new: --third (old --theme), --fourth (old --chunk), --dimension new
  codes --grep <re> [--by-room] [--json]   --by-room new: the count per room with the first hour; --grep now also matches the label and the coder's note
  (code lines)          changed: the position reads @<thread_id>:<coord>
  theme <sub>/<tNN or label words>   changed: label words match a substring, any case; several matches are listed by id
  themes --grep <re> [--rooms a,b] [--json]   new: second-order themes whose label or note match, with the count per room
  pairs --level second|third|fourth|dimension   changed: the tier names (case_theme, theme, chunk still work); an unknown level is refused with the list; dimension new
  facts [--field F] [--summary] [--sort asc|desc] [--where "F>v"] [--nulls] [--top N] [--json]   new: rooms.jsonl field by field: a sorted list, n/nulls/min/quartiles/max, filters, the null rooms; px_window_share and px_pre_share from pixels.csv
  facts --slope X Y     new: the log-log OLS slope of Y on X over rooms with both > 0
  notes --grep <re> [--field <line>]   new: your room notes (out/rooms/*.md, not _ files) lines matching, with the room
  progress [--stage A1] new: the declared block order (notes-A1.md, else sorted), each room noted, read or pending, and the last opened
  scheme [--brief] [T3-id]   new: one line per third-order theme (id, family, members, label: gloss) from scheme_current over the latest frozen scheme; with an id, that theme whole
  where <T3-id>         changed: reads the working grouping (scheme_current's members) when no assignments file exists
  rooms --with <id> | --without <id>   changed: an id that names nothing is refused instead of returning every room
  view [name] [--grep re] [--room sub]   new: a generated view in out/_views/, filtered; no name lists them
  wiki [page]           new: a generated wiki page (rooms/<sub>, model/<id>, or the bare name); no page lists them
  shelf <name> [--grep re] [--page N]   new options: matching lines with line numbers; one page of the work
  diary --last [n]      changed: n defaults to 5
  log "<text>" [--kind k] [--ids a,b] [--dry-run]   changed: the kind is checked against opened, dropped, merged, split, kept, move, abductive, question, comparison, note, helper and any `log --kind` a stage file names; --dry-run new
  reassign <sub>:<tNN> --theme T3-a[,T3-b] --reason "..."   new (2026-09-29): C1 to D6, a recut's re-placement, rewriting the theme's line of assignments_final.jsonl with the move recorded on it
  mint --label "..." --trigger <sub>:<tNN> [T3-id] [--dry-run]   changed: refused outside stages B1 and C1 to D6 (after B1 the discovery's stamp only); the trigger must be a second-order theme in the store; an id is minted once
  adjudicate <id> --decision d --reason "..." [--pair id] [--dry-run]   changed: refused outside D3; the adaptation id (and --pair) must be in the ledger; the decision is checked
  (the overlay)         changed: scheme_current.jsonl (out/scheme/ or out/) is laid over the latest frozen scheme when it is newer or none exists; placements fall back to its members when no assignments file exists
python3 tools/cite.py ...     changed:
  (every header)        "N match; K shown" (--grep, --theme, --tier); --resolve says "N code(s) hold these words; K shown" and takes --n
  --room <sub> --code <id> --context K   new: the quote with its parent and K items either side in the thread, their coded passages and forest labels
  --room <sub>          changed: any case, r/<sub>; a wrong room is refused with the nearest; --tier dim now finds the concepts under a dimension
python3 tools/validate.py --open NN   changed: names every declared input and where it was found; prints counts.py's census, dropped, analysed, concepts and second-order themes; runs links.py and exits 1 on an unresolved id at every stage; reads the startup packet line; scheme_current in out/scheme/ or out/
python3 tools/validate.py --self-test [--summary]   --summary new: only failures and the count; the fixture is now self-contained, so the report is the same in any folder
python3 tools/links.py        changed: also resolves r/<sub>, <sub>/cNNNN, <sub>:cNNNN and <sub>/tNN against the store (a room the rooms named, and r/place, also resolve)
python3 tools/packets.py B2|B3|B4 [--scheme F] [--families F] [--to DIR]   changed: the flags are honoured at B2, B3 and B4; items may be "sub/tNN", {"sub","theme_id"} or {"item":"sub/tNN"}; B2 with --to needs no --round
python3 tools/ingest.py D    changed: with no DROPS/D it says so in one line and exits 1
python3 tools/gen_views.py NN changed: data-structure.md above 2 MB holds a note pointing to `mem.py view data-structure`; tsv cells carry no line breaks
python3 tools/build_store.py --root R --join-canvas F   changed: F may be relative to --root
```

## v43.2, 2026-10-11 (J, after the B1e interview)

- `mem.py blind on --reason "..."`, `blind off`, `blind`: a blind window. Every read hides placements (placed lines, members, member counts, exemplars); `where`, `rooms`, `contrast`, `table`, `view`, `wiki`, `diff-*`, `finding(s)`, `adaptations`, `place`, `unplace`, `reassign`, `rechecks`, and `codes --third/--fourth/--dimension`, `pairs` above level second refuse; the diary drops placement lines and masks T3 ids. `--blind` does the same for one call. The read log marks each blind read; the tool guard refuses direct reads of placement files while the window is open.
- `--width N` (20 or more): mem.py clips each line of the page and logs the width and the lines clipped, in place of a shell `cut`, which the guard now refuses after mem.py, cite.py or a helper.
- `mem.py gates [T3-a [T3-b]] [--confirm --reason "..."]`: one-way discriminators, `must_not_show` lines sending material to a theme with no discriminator against it, ids the gates name that the scheme lacks; a pair side by side; confirmations in `out/gate_checks.jsonl`, stale when a gate changes.
- `mem.py gate T3-NNN --field F --now "..." --reason "..."` (B1, C1 to D6; B2's edits are `scheme_edits.jsonl`): records a gate change in `out/gate_history.jsonl` with the placements it could move and those it owes (all up to 30, a seeded sample of 30 above, all once more than one in ten of the sample moves). At B1 it writes the field into scheme_current.
- `mem.py recheck <sub>:<tNN> --change <edit:n|gate:n> --theme ... --codes ... --reason "..."` and `mem.py rechecks [--owed]`: `out/rechecks-NN.jsonl`. The checks of B1, B2 and C1 refuse a change with rechecks missing.
- `place` and B1 `mint` need `--codes` (the trigger's or member's concepts); `mint` needs `--gate`; `reassign` needs `--codes "T3-a=c1,c2;T3-b=c3"` and keeps `support_by_theme` on the line and the move.
- `tools/tokens.py`: token sizes measured from the dispatch's usage records (`--dispatched`), or estimated at the measured rate, never at an assumed one without saying so.
