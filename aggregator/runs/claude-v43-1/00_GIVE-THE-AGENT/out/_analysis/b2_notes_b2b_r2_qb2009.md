
### QB2-009, answered: the 16 lines waived, round 2 scored as it stands

J ruled (2026-10-12, 09:27 Berlin): no reissue of round 2. The 16 lines in `out/_analysis/b2_r2_return_problems.txt` are waived by name, in `out/return_waivers.jsonl` (`out/_analysis/b2_waivers_r2.py`). Each line names the round folder, the file, the item as the line writes it, the problem as listed, and J's ruling. The AyyMD line's reason also names its mistyped heading. `validate.py B2` skips the waived lines and counts them aloud.

Round 2 stays scored on third_order, as before. `pilot_rounds.jsonl` line 2, the verdicts and edits 287 to 295 stand unchanged; nothing rested on a reissue.

The 16 lines are reader faults:
- one incomplete line: packet 2 r1, ainbowroad t04;
- one mistyped heading: packet 5 r2, AyyMD t02 for t08;
- 14 lines citing concepts that are not the item's own.

The faults came from two things, and both are artefacts of room ids:
- **Room ids repeat across rooms.** c0006 names two different concepts in packet 2, one in each of two rooms.
- **Invented ids land on sibling codes.** A room's ids run in sequence, so an id a reader makes up within range nearly always names a real concept of a sibling theme. Examples are c0558 on sweden t01 and c1556 on ainbowroad t04, neither ever shown in their packets. Where two items of one room shared a packet (theblackvoid t09 and t12, ainbowroad t07 and t11), readers also took concepts from the other item.

From round 3 the fleet ids of `out/fleet_ids.jsonl` end both: no id repeats, and a made-up id lands on a real code about 7.5% of the time. `fleet.py` rejects, and reissues in the dispatch, a line citing an id not under its item. For that check, round 3's builder `out/_analysis/b2_packets_fleet.py` writes `codes_by_item` into each packet's MANIFEST entry: the item's fleet theme id, as the line writes theme_id, with the fleet code ids served under it. Tested on guatemala t02 (8 codes) and sweden t01 (310). No round-3 packet is built yet: QB2-010, the recut, waits for J's word.

### The close-check, B2b-r2-p2

`validate.py B2` reported:

```
stage B2:
  leg: check (2 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  _fleet_raw/B2/round-2: 15 readers, 150 return lines, 16 waived by J (return_waivers.jsonl)
  author items 50, gold items 40, rounds scored 2, edits 295 (author-error 4), scheme ids 197 (scheme/scheme_current.jsonl)

warn   scheme.jsonl: the pair T3-001|T3-017 touches an edited theme and is not confirmed against its current sentences (mem.py gates T3-001 T3-017 --confirm --reason ...)  [443 lines with this shape; first: T3-001|T3-017]

0 errors (0 distinct shapes), 443 warnings
```

The 443 warnings are the unconfirmed pairs that touch an edited theme; they are read before any freeze. The leg closes with `done.sh B2`. Round 3 opens (QB2-007). Its build waits for J's word on the recut (QB2-010), and its packets carry fleet ids.
