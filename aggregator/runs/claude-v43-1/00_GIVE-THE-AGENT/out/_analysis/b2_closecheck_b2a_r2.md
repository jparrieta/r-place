
### The rechecks the ten new items owed

The ten bags sit on themes that round 1's edits changed. The first run of `validate.py B2` in this leg therefore found 57 rechecks owed, over 30 edits (42 error lines). No edit can have moved a placement made after it. The check still asks for the record, so `out/_analysis/b2_rechecks_r2.py --show` printed each edit's changed sentence beside the items it owes. I read each and wrote one reason per edit. None moves a placement. The 57 records went in through `mem.py recheck`, all unchanged, with the concepts from each line's `support_by_theme`. `rechecks-B2.jsonl` now has 754 records, and none is owed.

### The close-check, B2a-r2

`validate.py B2` reported:

```
stage B2:
  leg: check (1 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  author items 50, gold items 40, rounds scored 1, edits 286 (author-error 4), scheme ids 197 (scheme/scheme_current.jsonl)

warn   scheme.jsonl: the pair T3-001|T3-017 touches an edited theme and is not confirmed against its current sentences (mem.py gates T3-001 T3-017 --confirm --reason ...)  [443 lines with this shape; first: T3-001|T3-017]

0 errors (0 distinct shapes), 443 warnings
```

The 443 warnings are the unconfirmed pairs that touch an edited theme. They are read and confirmed before the freeze. The check calls the leg "check" because round 1's dispatch folder holds DONE; this leg is round 2's build. The leg closes with `done.sh B2 --cut packets-out`. The dispatch sends the eleven parts of P03-r2 to each of three fresh readers. The check leg B2b-r2 scores fidelity against `author_items.jsonl` and against the rechecked placements, with pairwise agreement and alpha.
