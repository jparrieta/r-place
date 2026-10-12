
### QB2-011, answered: the check reads the split layer

The handler fixed the three error shapes in `tools/vlib.py` and `tools/checks/stage_B2.py`. They were faults of the check, not of the run.
- A split child counts as a second-order theme, and its parent stays one. `author_items.jsonl` and `gold_items.jsonl` resolve both.
- A split concept belongs to its child and to every theme it was split from. Records made before the split about a parent pass; a concept of a sibling child still fails.
- A round's n_items is held to the items its own MANIFEST sent (`out/_packets-B2/round-K/MANIFEST.json`), as the handler's correction says.

My assumption needed no revisit. I recorded the 526 rechecks and left these shapes to the check, which now passes. Round 3's packets carry the children, not their parents.

### The close-check, B2b-r2-p2, after the split

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

`author_items.jsonl` holds 104 lines: the six superseded parents kept as written, beside their 54 children. Round 3 sends 98 items. The 443 pair warnings are the unconfirmed pairs, read before any freeze. The leg closes with `done.sh B2`. Next comes round 3's build: `b2_packets_fleet.py --round 3` on the 98 items, with the superseded parents left out and fleet ids only. The 846 B1 bags wait for J.
