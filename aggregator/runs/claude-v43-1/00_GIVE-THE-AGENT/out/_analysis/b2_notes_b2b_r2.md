
## Leg B2b-r2, round 2 rebuilt, 2026-10-12

### Why round 2 was rebuilt

Round 2's dispatch ran three times, and every reader was exhausted. There is no valid return. `out/_fleet_raw/B2/round-2/` holds DONE, `EXHAUSTED.tsv` and `log.jsonl`; nothing in it is scored. The handler gave two causes, both in the log.
- Every reader got HTTP 400 at part 6. Part 5 carried 149,007 input tokens and passed; part 6 would carry about 163,000. The provider's window looks to be about 164,000 tokens (the handler inferred this from the log; it is not confirmed). One conversation over eleven parts cannot fit, since the shared pages alone are about 95,000 tokens.
- Some readers closed part 1 with the packet's end line instead of `END-OF-RETURN`. `fleet.py` now names the marker in every message.

QB2-004 was answered before the dispatch: J confirmed my MANIFEST form for parts. J's ruling of 2026-10-12 replaces the parts design, so nothing rests on that answer any longer.

### J's ruling, as applied

The ruling asks for self-contained packets: at most 15 items and at most 180,000 bytes of item text each; no item split across packets; no MANIFEST group, part or parts; the same 50 items, shared pages and RETURN-B2.md, minus its parts paragraph.

`out/_analysis/b2_packets_r2b.py` built them with `packets.py`'s own `Store.item`. It keeps round 2's seeded order (seed 20261012, `out/_analysis/b2_order_r2.json`) and cuts it into consecutive packets, choosing the cut points that make the largest packet smallest. No item is over the cap; the largest, leagueoflegends t02, is about 87,000 bytes. Four packets would meet the caps, but one would hold 166,501 bytes of item text, close to the cap. I built five, so the largest holds 128,155 bytes and each reader has more room inside the window.

The next table lists the five packets that the dispatch must read, all in `out/_packets-B2/round-2/`.

| packet | items | bytes of item text | bytes in all |
|---|---|---|---|
| `P03-r2-1.md` | 15 | 58,210 | 58,656 |
| `P03-r2-2.md` | 12 | 96,519 | 96,965 |
| `P03-r2-3.md` | 9 | 128,155 | 128,599 |
| `P03-r2-4.md` | 3 | 125,484 | 125,928 |
| `P03-r2-5.md` | 11 | 97,101 | 97,547 |

Each packet numbers its items from 1 and says how many lines to return. `MANIFEST.json` gives each packet its own item count, with count_key position, and no group or part. The items per packet are in `out/_analysis/b2_order_r2b.json`. The shared pages beside them are `index.md` and `G01.md` to `G21.md`, unchanged from B2a-r2. Packet 4 holds three items: leagueoflegends t02, acecombat t05 and dota2 t05.

The packets are over FLEET.md's 50 KB ceiling by J's ruling, which sets the byte cap at 180,000 of item text. `packets.py`'s writer asserts 50 KB, so the helper writes the files itself.

**Superseded, not deleted.** The eleven parts `P03-r2-p1.md` to `P03-r2-p11.md` and their `MANIFEST.json` moved to `out/_analysis/b2_packets_round2_parts/`. The dispatch must not read them.

**RETURN-B2.md** loses its paragraph on parts. The batch field is now the name on the packet's title line, such as `P03-r2-3`. The parts version is kept as `out/_analysis/RETURN-B2_round2_parts.md`.

**Manifest.** `run_manifest.json` has a new round-2 entry from this leg (`out/_analysis/b2_manifest_r2b.py`). It supersedes the B2a-r2 entry, which stays. It records the five packets with bytes and hashes, J's caps, and the same reader settings: one provider (Relace) and medium effort.

### The close-check, B2b-r2

`validate.py B2` reported:

```
stage B2:
  leg: check (2 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  _fleet_raw/B2/round-2: 0 readers, 0 return lines
  author items 50, gold items 40, rounds scored 1, edits 286 (author-error 4), scheme ids 197 (scheme/scheme_current.jsonl)

ERROR  _fleet_raw/B2/round-2 holds a finished dispatch and pilot_rounds.jsonl has no line for round 2; the check leg scores it (fidelity, pairwise agreement, alpha) before it closes
warn   scheme.jsonl: the pair T3-001|T3-017 touches an edited theme and is not confirmed against its current sentences (mem.py gates T3-001 T3-017 --confirm --reason ...)  [443 lines with this shape; first: T3-001|T3-017]

1 errors (1 distinct shapes), 443 warnings
```

The error conflicts with J's ruling. The failed folder holds no reading, so there is nothing to score, and the check accepts no line without numbers. QB2-005 asks J how to record a failed dispatch. Meanwhile I write no `pilot_rounds.jsonl` line for round 2 and leave `_fleet_raw/B2/round-2/` as the dispatch left it. A diary line of kind ask at 03:56 carries the same question without an id; I wrote it with `mem.py log` by mistake, and QB2-005 is the record.

The 443 warnings are the unconfirmed gate pairs, read before the freeze.
