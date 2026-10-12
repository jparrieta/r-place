
## Leg B2a-r3, build round 3, 2026-10-12

### The answers this leg was told to read

QB2-007 to QB2-011 were all applied at B2b-r2-p2:
- round 3 runs on the edited scheme with round 2's readers;
- `also_present` takes a theme only with three concepts of its own, and the bags were split;
- the 16 faulty lines are waived;
- the split was approved;
- the check reads the split layer.

Nothing in this leg rests on an assumption.

### What was built

Round 3 is the first round in which only the scheme changes (QB2-007), and the first with fleet ids (J, 2026-10-12).

**Items.** Round 3 serves 98 items: the 44 unsplit hard items and the 54 children of the six split bags. The six parents (2007scape t04, sweden t01, theblackvoid t12, ainbowroad t03, t04 and t07) are not served. `author_items.jsonl` keeps their lines as written, so it holds 104 lines.

**The packets.** `out/_analysis/b2_packets_fleet.py` built the round, with two changes this leg. It now reads the split layer by giving `packets.py`'s Store the `out/` path. It also leaves out any item whose children are in `out/recut/themes.jsonl`. The round has seven self-contained packets in `out/_packets-B2/round-3/`, cut from the order seeded with 20261013. The next table lists them.

| packet | items | bytes of item text |
|---|---|---|
| `P03-r3-1.md` | 10 | 113,527 |
| `P03-r3-2.md` | 13 | 112,021 |
| `P03-r3-3.md` | 15 | 42,159 |
| `P03-r3-4.md` | 15 | 48,792 |
| `P03-r3-5.md` | 15 | 88,494 |
| `P03-r3-6.md` | 15 | 31,082 |
| `P03-r3-7.md` | 15 | 91,999 |

Each packet is within J's caps: at most 15 items and 180,000 bytes of item text, with no item split. The items per packet are in `out/_analysis/b2_order_r3.json`. Beside the packets are `index.md` and `G01.md` to `G21.md`, built from the edited `scheme.jsonl`.

**Fleet ids.** Each item is headed by its room and its `T2-` id, and each concept by its `C` id. The builder stops if a room id would stand in an id position, and none did. `MANIFEST.json` gives each packet its item count and `codes_by_item`: the fleet theme id of each item with the fleet code ids served under it. With that entry, `fleet.py` rejects and reissues any line that cites a code its item does not hold (QB2-009). Returns are translated back to room ids with `out/_analysis/b2_translate_fleet.py` before scoring; the check translates them through `out/fleet_ids.jsonl` itself (QB2-010).

**RETURN-B2.md.** It is unchanged since B2b-r2-p2. It asks for fleet ids and carries the floor of three concepts of its own for `also_present`.

**Manifest.** `run_manifest.json` has a round-3 entry (`out/_analysis/b2_manifest_r3.py`). It records the same readers as round 2 (deepseek/deepseek-v4.1-flash, called directly, medium effort, max_tokens 128,000), the seed, 98 items, and every packet's bytes and hash.

**One packing matter for J.** Some packets hold several children of one parent; for example, packet 3 holds ainbowroad children beside one another. At round 2, readers took concepts from a sibling item in the same packet. With fleet ids and `codes_by_item`, `fleet.py` now catches such a citation and reissues the reader. Packing one item per room per packet was proposed at B2b-r2-p2 and not ruled on, so it is not applied.

### The close-check, B2a-r3

`validate.py B2` reported:

```
stage B2:
  leg: check (2 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  _fleet_raw/B2/round-2: 15 readers, 150 return lines, 16 waived by J (return_waivers.jsonl)
  author items 104, gold items 42, rounds scored 2, edits 295 (author-error 4), scheme ids 197 (scheme/scheme_current.jsonl)

warn   author_items.jsonl has 104 items; section 1 says forty to sixty
warn   scheme.jsonl: the pair T3-001|T3-017 touches an edited theme and is not confirmed against its current sentences (mem.py gates T3-001 T3-017 --confirm --reason ...)  [443 lines with this shape; first: T3-001|T3-017]

0 errors (0 distinct shapes), 444 warnings
```

The leg closes with `done.sh B2 --cut packets-out`. The dispatch sends each of the seven packets to three fresh readers.
