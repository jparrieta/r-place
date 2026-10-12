
### J's answers (13:47 Berlin), and the close

**QB2-012.** No round 4. A freeze leg of its own does three things: the 443 gate-pair confirmations, the cluster reads for T3-002, T3-033 and T3-038, and any sentence fix to that cluster. A fix made there is tested only by the gold round in B2c. My assumption was that rounds stop and this leg writes no edit. It held, so nothing here changes.

**QB2-013.** J ruled yes to both parts.
- The four lines are waived by name in `return_waivers.jsonl`, with the reason "item_is_a_bag true with no theme at the three-concept floor (also_present {}); the placement scored as given" and ruled_by J (`out/_analysis/b2_waivers_r3.py`). The file now holds 20 waivers: 16 from round 2 and 4 from round 3.
- `RETURN-B2.md` now says that a bag with no other theme at the three-concept floor is not flagged a bag: `item_is_a_bag` false, `also_present` `{}`. The round-3 text is kept as `out/_analysis/RETURN-B2_round3.md`.

**The also_present bound** (J, 13:47). In round 3 some bag returns listed up to 85 themes. `RETURN-B2.md` now says `also_present` names "twenty themes at most", each with at least three concepts of its own. It says twenty is a bound, not a goal. The validator and `fleet.py` apply the bound only where that exact phrase stands. They refuse a return with more than twenty themes, or with a theme that has fewer than three concepts. Returns already kept in rounds 1 to 3 are scored as given. B3's return specification does not exist yet. The head carries both rules into it, with the phrase word for word.

`validate.py B2` reported, after the waivers:

```
stage B2:
  leg: check (3 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  _fleet_raw/B2/round-2: 15 readers, 150 return lines, 16 waived by J (return_waivers.jsonl)
  _fleet_raw/B2/round-3: 15 readers, 150 return lines, 4 waived by J (return_waivers.jsonl)
  author items 50, gold items 40, rounds scored 3, edits 295 (author-error 4), scheme ids 197 (scheme/scheme_current.jsonl)

warn   scheme.jsonl: the pair T3-001|T3-017 touches an edited theme and is not confirmed against its current sentences (mem.py gates T3-001 T3-017 --confirm --reason ...)  [443 lines with this shape; first: T3-001|T3-017]

0 errors (0 distinct shapes), 443 warnings
```

The 443 warnings are the gate pairs the freeze leg confirms. The leg closes with `done.sh B2`.
