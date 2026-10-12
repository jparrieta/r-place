
### QB2-006, answered: the failed dispatch moved out of `_fleet_raw/B2/`

J ruled at 06:55, and the handler placed the folder under that ruling. The check is not changed. I moved `out/_fleet_raw/B2/round-2-failed/` whole to `out/_analysis/fleet_B2_round2_failed/` (mv). Nothing was deleted, and its DONE, `EXHAUSTED.tsv`, `arm.json`, `log.jsonl` and 39 reader files are inside, untouched. The new path is where the failed first dispatch of round 2 lives; it holds no reading and is never scored. `_fleet_raw/B2/` now holds `round-1/` only, and J dispatches round 2 again into a fresh `round-2/`.

`validate.py B2` after the move:

```
stage B2:
  leg: check (1 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  author items 50, gold items 40, rounds scored 1, edits 286 (author-error 4), scheme ids 197 (scheme/scheme_current.jsonl)

warn   scheme.jsonl: the pair T3-001|T3-017 touches an edited theme and is not confirmed against its current sentences (mem.py gates T3-001 T3-017 --confirm --reason ...)  [443 lines with this shape; first: T3-001|T3-017]

0 errors (0 distinct shapes), 443 warnings
```

The 443 warnings are the unconfirmed gate pairs, read before the freeze. The leg closes with `done.sh B2 --cut packets-out`. The dispatch must read the five packets `P03-r2-1.md` to `P03-r2-5.md` in `out/_packets-B2/round-2/`.
