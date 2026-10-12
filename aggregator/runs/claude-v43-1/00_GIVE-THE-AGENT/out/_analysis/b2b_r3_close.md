
### The close-check, B2b-r3

`validate.py B2` reported:

```
stage B2:
  leg: check (3 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  _fleet_raw/B2/round-2: 15 readers, 150 return lines, 16 waived by J (return_waivers.jsonl)
  _fleet_raw/B2/round-3: 15 readers, 150 return lines
  author items 50, gold items 40, rounds scored 3, edits 295 (author-error 4), scheme ids 197 (scheme/scheme_current.jsonl)

ERROR  _fleet_raw/B2/round-3: a return on acecombat/t05 is a bag and names no also_present; rule 0 keeps every theme beyond the one placed, each with its own concepts  [4 lines with this shape; first: r3.jsonl line 6]
warn   scheme.jsonl: the pair T3-001|T3-017 touches an edited theme and is not confirmed against its current sentences (mem.py gates T3-001 T3-017 --confirm --reason ...)  [443 lines with this shape; first: T3-001|T3-017]

4 errors (1 distinct shapes), 443 warnings
```

The 4 errors are the four bag flags of QB2-013. J had not answered when the leg closed. I write no waiver without J's word, so the close-check refuses this close. The leg reopens on J's answer: with a waiver, I write the four lines into `return_waivers.jsonl` and close again.
