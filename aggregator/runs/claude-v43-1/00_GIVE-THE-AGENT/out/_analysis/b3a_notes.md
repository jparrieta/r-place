
### The build

**The allocation** (`out/_analysis/b3_allocate.py --seed 20261015`, written to `batches-B3.jsonl`).
- **Packing.** For each replicate, the 705 rooms are shuffled under the seed and packed by first fit into the open batches.
- **Large rooms.** A large room opens a batch served in parts, which first takes one ordinary room beside it.
- **Why that rule.** Two earlier drafts left large and near-large rooms alone in both replicates. Each such room was an island, and the connectivity gate could not pass on any of 20 redraws.
- **Redraws.** The final rule passed after 7 redraws.
- **Coverage, from the batches.** Each replicate holds the 705 rooms and the 7,844 items, every room whole, in one batch per replicate.
- **Gates.** Gate 1 holds: one reader per batch, and a room's two batches sit in different replicates. Gate 2 holds: the room-batch graph is one component.

The next table lists the counts.

| figure | value |
|---|---|
| batches (one reader each) | 624 (replicate 1: 310, replicate 2: 314) |
| batches served in parts | 313 |
| packet files | 1,080, every one under 50 KB (largest 50,878 bytes) |
| positions | 17,089 (15,688 readings, 624 duplicates, 777 gold copies) |
| gold copies per gold item | 19 or 20 |
| items per batch | 13 to 54, median 27 |

**The packets** (`out/_analysis/b3_packets_fleet.py`, in `out/_packets-B3/`).
- **Structure.** `index.md` and `G01.md` to `G21.md` come from `scheme_final.jsonl` with no exemplars. Each batch file has a title naming the batch and its replicate, the brief, a sibling block per room, the items in position order and the end line.
- **Fleet ids.** Only fleet ids appear: `T2-` ids in item headings and sibling blocks, `C` ids on concept lines.
- **Rooms.** A gold copy's room gets a sibling block like the batch's own rooms, so no reader can tell the copy from a corpus item.
- **Bag flags.** The ten flagged bags carry one line under the heading: "flagged as a bag: place from the concepts, not from the coder's grouping."
- **MANIFEST.json.** It gives each file the lines due from it, bytes, sha256, the count key and `codes_by_item`, and for parts the group, part and part count. It lists 17,089 due lines in all.

**One coder note held a room id.** nyjets t11's `theme_note` says "Code c0104 remains instead with...". The packet serves that code as its fleet id; the note's words are unchanged. No other label or note in the store holds a room id.

**Strings shaped like room ids.** Two packets (B059, B449) carry "t34" and "t90" in a warthunder participant's words. These are tank names (the T-34 and the T-90) and no id of any room in those packets; warthunder's themes run t01 to t15. Participants' words are never altered (QB3-002, point c).

**Items longer than a part.** Five placements run over two consecutive parts of one reader. leagueoflegends t02 (89 KB) is in B282 and B463. ainbowroad t11 (48 KB) is in B157, and twice in B523, as that batch's duplicate. The heading repeats with "(continued)", and the item's line is due after the part it ends in, so some parts are due 0 lines, B282-p2 for one (QB3-001, point 2; QB3-002, point d).

**The return specification.** `RETURN-B3.md` sets the order: rule 0 in the contract's words; the prediction line; the return line, with `bag` and with `also_present` under J's two rulings, word for word; the multiplacement record on the line; the second pass, one line per position carrying `revises`; the end marker and the confirmation.

**The manifest.** `run_manifest.json` has a B3 entry, 10 entries in all. It records the readers (deepseek/deepseek-v4.1-flash, direct, medium effort, max_tokens 128,000), the seed and its suffix, R, 624 agents, the counts, the groups (60 and 564), the frozen scheme's sha256 and `RETURN-B3.md`'s.

### The close-check, B3a

`validate.py B3` reported:

```
stage B3:
  batches 624, R 2, rooms 705, graph one component
  leg: build (0 dispatch folders with DONE)

ERROR  batches-B3.jsonl B001 lists item polska/t10 from a room not in its rooms; a batch holds whole rooms  [777 lines with this shape; first: B001]
ERROR  batches-B3.jsonl B157 holds room ainbowroad without 20 of its second-order themes (['t14', 't15', 't16']); no room is ever split  [10 lines with this shape; first: B157]
ERROR  batches-B3.jsonl: replicate 1 lacks 56 of the 7900 items assignment_items_expected counts (['2007scape/t15', '2007scape/t16', '2007scape/t17'])
ERROR  batches-B3.jsonl: replicate 2 lacks 56 of the 7900 items assignment_items_expected counts (['2007scape/t15', '2007scape/t16', '2007scape/t17'])

789 errors (4 distinct shapes), 0 warnings
```

**What the errors are.**
- **The 777 gold copies.** These are listed in `items` so that `n_items` counts every position. The check's whole-room rule has no exemption for them (QB3-001, point 3).
- **The other three shapes.** They come from the check reading the 56 children of the withdrawn split from `out/recut/`. It counts 7,900 items where the analysed set holds 7,844, and it says 10 rooms are split where the batches hold them whole (QB3-002, point a).

None of these is a fault in the batches. The leg stays open until the handler answers QB3-001 and QB3-002. Nothing is rebuilt meanwhile.
