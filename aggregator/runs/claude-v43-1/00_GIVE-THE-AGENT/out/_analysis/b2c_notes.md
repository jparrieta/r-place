
## Leg B2c, the gold round and the stability rounds built, 2026-10-12

### QB2-014 applied: the tier word is "main"

J ruled at 15:06 Berlin that the frozen scheme's main tier is "main", the word of B1's `scheme.jsonl` and of C1's check. The handler changed `checks/stage_B2.py` to accept only "main" or "rare" on `scheme_final.jsonl`. After that change the freeze's file failed the check 183 times.

`out/_analysis/b2_freeze_main.py` superseded the file:
- the "common" files moved unchanged to `out/_analysis/scheme_final_common.jsonl` and `scheme_final_common.md`;
- `scheme_final.jsonl` was written again with "main" for the 183 themes and "rare" for 14, nothing else changed (checked field by field);
- `scheme_final.md` names the tier word and the new sha256, 4b471d29dd415fc0507b535f4d7595b40a5b9794ac36448d152a69ba7343e18d.

My assumption was that "common" would stand. J ruled "main", so the file and its header changed, and nothing else rested on the word. The gate check still reads 496 pairs, all confirmed, because the tier is not a gate field.

### The three rounds

Stage B2 section 5 asks for three rounds on the frozen scheme. The gold round serves the gold set to fresh readers. The two stability rounds serve the gold set to the same reader arm under two rewordings of the brief that change no test.

`out/_analysis/b2_packets_fleet2.py` built all three. It is round 3's fleet-id builder with three changes: it reads `gold_items.jsonl`, it takes the shared pages from `scheme_final.jsonl`, and it takes the brief from a file. The packets keep J's rules: fleet ids only, at most 15 items and 180,000 bytes of item text a packet, no item split, and `codes_by_item` in each MANIFEST entry.

**One seed, one cut.** All three rounds use seed 20261014. The same 40 items fall in the same 3 packets in the same order, so the brief is the only difference between the rounds. The next table lists the packets of each round.

| packet in each round | items | bytes of item text |
|---|---|---|
| first | 14 | 14,157 |
| second | 14 | 14,803 |
| third | 12 | 14,137 |

**The briefs.** The brief is the packet's opening paragraph.
- **Gold round:** the builder's own brief ("Place each second-order theme below onto the scheme, one line per item in the form the return specification gives...").
- **Stability round 1:** `out/brief-stab-1.md` ("For every item below, decide where it sits in the scheme and write one line for it...").
- **Stability round 2:** `out/brief-stab-2.md` ("Below are second-order themes to be placed on the scheme. Give each one its own line...").

Each brief tells the reader the same four things in other words: one line per item in the return specification's form, items numbered by position, ids copied exactly, and the packet complete in itself. The item count follows as its own sentence, the same in every round. No brief names a theme, a test or a placement.

**Checks.** Each round's folder (`out/_packets-B2/round-gold/`, `round-stab-1/`, `round-stab-2/`) holds `index.md`, `G01.md` to `G21.md`, the three packets and `MANIFEST.json`. `out/_analysis/b2_roomid_scan.py` found 0 room ids in all 75 files. The gold placements appear nowhere in the packets. The orders are in `out/_analysis/b2_order_rgold.json`, `b2_order_rstab-1.json` and `b2_order_rstab-2.json`.

**Return specification.** `RETURN-B2.md` is unchanged since B2b-r3. It carries fleet ids, the three-concept floor for `also_present`, the rule that a bag with no other theme at the floor is not flagged, and "twenty themes at most".

**Manifest.** `run_manifest.json` has three B2c entries (`out/_analysis/b2_manifest_b2c.py`), 9 entries in all. Each entry records the readers of rounds 2 and 3 (deepseek/deepseek-v4.1-flash, called directly, medium effort, max_tokens 128,000), the seed, the 40 items, every packet's bytes and hash, the frozen scheme's sha256 and the brief.

J runs the three dispatches. The check leg, B2d, scores the gold round against round 3. It writes the stability figure to `stability-B2.md` and writes `pilot_report.md`.

### The close-check, B2c

`validate.py B2` reported:

```
stage B2:
  leg: check (3 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  _fleet_raw/B2/round-2: 15 readers, 150 return lines, 16 waived by J (return_waivers.jsonl)
  _fleet_raw/B2/round-3: 15 readers, 150 return lines, 4 waived by J (return_waivers.jsonl)
  author items 50, gold items 40, rounds scored 3, edits 306 (author-error 4), scheme ids 197 (scheme_final.jsonl), frozen


0 errors (0 distinct shapes), 0 warnings
```

The leg closes with `done.sh B2 --cut packets-out`.
