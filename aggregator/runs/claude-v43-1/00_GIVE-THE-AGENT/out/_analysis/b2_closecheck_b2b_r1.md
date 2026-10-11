
### The close-check, B2b-r1

`validate.py B2` reported:

```
stage B2:
  leg: check (1 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  author items 40, gold items 40, rounds scored 1, edits 286 (author-error 4), scheme ids 197 (scheme/scheme_current.jsonl)

0 errors (0 distinct shapes), 443 warnings
warn   scheme.jsonl: the pair T3-001|T3-017 touches an edited theme and is not confirmed against its current sentences (mem.py gates T3-001 T3-017 --confirm --reason ...)  [443 lines with this shape; first: T3-001|T3-017]
```

The 443 warnings are pairs touching an edited theme that are not yet confirmed. They are read and confirmed before the freeze, where they become errors. The check counts 120 return lines because `round-1` holds only the three valid readers' `.jsonl` files; the failed attempts are `.failed.txt`.

The leg closes with `done.sh B2`. Round 2's build leg, B2a-r2, comes next.
