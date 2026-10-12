
## Leg B2a-r3-p2, the split withdrawn and round 3 rebuilt, 2026-10-12

### The split, withdrawn

**What was cut.** At B2b-r2-p2 (QB2-010) I split six bags of the hard set and one gold bag with `mem.py split`, in one blind window. 2007scape t04 became 14 children, sweden t01 10, theblackvoid t12 10, ainbowroad t03 8, ainbowroad t04 6 and ainbowroad t07 6. In the gold set, dankmemes t16 became 2. The 56 children are in `out/recut/themes.jsonl`, and their concepts in `out/recut/codes.jsonl`. I placed each child and recorded 526 rechecks for them. The B2a-r3 round 3 served 98 items: 44 unsplit items and 54 children.

**Why J withdrew it** (J, 2026-10-12, 12:04 to 12:10 Berlin). Bags are a coder problem. Second-order themes are the coders' to cut, and the aggregator takes them as given. The split was a mistake, so the run goes back to before any cut and goes on from there, inside this run, with nothing deleted.

**What the withdrawal did.**
- `out/recut/WITHDRAWN.json` holds J's ruling word for word. From it on, every tool reads the store as it was before the split: the six parents and the gold bag stand again, and the 56 children are gone from every view. `out/recut/` stays as written.
- `out/_analysis/b2_split_withdraw.py` moved the children's placement lines, unchanged and in order, to `out/_analysis/author_items_split_withdrawn.jsonl` (54 lines) and `out/_analysis/gold_items_split_withdrawn.jsonl` (2 lines). `author_items.jsonl` again holds 50 lines and `gold_items.jsonl` 40, the counts J named.
- `mem.py split` now refuses. A bag stays one item: one theme placed, and every other theme under `also_present` with at least three concepts of its own (QB2-008).

**Records that belong to the withdrawn split.** No figure counts these. `out/_analysis/b2_split_withdrawn_count.py` matched each file against the 56 children.
- `out/recut/` (themes and codes, kept as written).
- `out/_analysis/author_items_split_withdrawn.jsonl` and `gold_items_split_withdrawn.jsonl`.
- `rechecks-B2.jsonl` lines 888 to 1,413: 526 rechecks of the children, all from B2b-r2-p2. They stay in the file so that they still resolve. Lines 1 to 887 stand.
- The 56 lines of `out/fleet_ids.jsonl` marked `"split": true`.
- The 98-item round 3: its packets, moved to `out/_analysis/b2_packets_round3_split_withdrawn/`, its order, renamed `out/_analysis/b2_order_r3_split_withdrawn.json`, and the B2a-r3 round-3 entry in `run_manifest.json`.
- The cut files and scripts in `out/_analysis/`: `b2_split_*.txt`, `b2_split_run.py`, `b2_author_split.py` and `b2_rechecks_split.py`.
- In this file: "QB2-010: the bags split", "QB2-011, answered", "The close-check, B2b-r2-p2, after the split", and the B2a-r3 section.

The split wrote no line on a child in `scheme_current.jsonl`, `multiplacement_log.jsonl`, `tier_history.jsonl`, `exemplar_candidates.jsonl` or `scheme_edits.jsonl`, so nothing there needs superseding.

**What stands.** Round 2's scores. The 16 waivers in `return_waivers.jsonl` (QB2-009). Edits 287 to 295 and their 133 rechecks (records 755 to 887). The 31 confirmed gate pairs.

**The B1 bags.** This run splits none of them. J will decide how the coders recut them. J's ruling counts 841 B1 bags; my head said 846, and I have not reconciled the two counts.

### Round 3 is round 2's set

Round 3 serves round 2's 50 hard items, each bag as one item. The six parents are served whole; for example, sweden t01 is served as one item with its 310 concepts. `out/_analysis/b2_packets_fleet.py` now leaves out no parent when `out/recut/WITHDRAWN.json` exists. It built five self-contained packets from the order seeded with 20261013. The next table lists the packets.

| packet | items | bytes of item text |
|---|---|---|
| `P03-r3-1.md` | 12 | 89,418 |
| `P03-r3-2.md` | 13 | 135,742 |
| `P03-r3-3.md` | 8 | 98,208 |
| `P03-r3-4.md` | 7 | 98,843 |
| `P03-r3-5.md` | 10 | 95,887 |

Each packet is within J's caps: at most 15 items and 180,000 bytes of item text, with no item split. The items per packet are in `out/_analysis/b2_order_r3.json`. `index.md` and `G01.md` to `G21.md` are built from the edited `scheme.jsonl`. Each `MANIFEST.json` entry carries `codes_by_item`. `RETURN-B2.md` is unchanged.

**Fleet ids** (J, 12:15 Berlin: `fleet.py` refuses a packet with `codes_by_item` if any room code or room theme id appears in its text, headings included). `out/_analysis/b2_r3_roomid_scan.py` scanned the five packets and the 22 shared pages and found 0 room ids. The same pattern finds 50 room ids in `b2_order_r3.json`. All 50 item headings carry `T2-` ids, and all 4,094 concept lines carry `C` ids.

**Manifest.** `run_manifest.json` now has 6 entries. The new round-3 entry (`out/_analysis/b2_manifest_r3b.py`, leg B2a-r3-p2) records 50 items in 5 packets and supersedes the B2a-r3 entry. The readers are round 2's: deepseek/deepseek-v4.1-flash, called directly, medium effort, max_tokens 128,000.

Round 3 is the first round in which only the scheme changes (QB2-007). Its check compares it with round 2 item for item.

### The close-check, B2a-r3-p2

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

The leg closes with `done.sh B2 --cut packets-out`. The dispatch sends each of the five packets to three fresh readers.
