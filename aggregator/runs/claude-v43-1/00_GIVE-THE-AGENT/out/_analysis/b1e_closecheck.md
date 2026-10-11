
### The close-check, B1e

`saturation.py report --stage B1` was rerun at the close and rewrote `stopping-B1.md` (384 lines); the decision file was not touched. `validate.py B1` reported, in full:

```
stage B1:
  scheme_current: 197 themes over 7786 placed second-order themes (13432 members)
  theme_discovery: 197 themes minted
  saturation B1: end; 705 of 705 rooms read (100.0% of the words); kinds 202, coverage 0.9985, unseen 20.03; rounds 20, markers 1,2,3
  pass 2 (B1d): met; chosen rooms read 108 of 108; rooms read in this pass 108; since its last new third-order theme 108 rooms and 148.1 average rooms, against 78 rooms and 72.1 average rooms (marker 1's empty run (72.1 average rooms, 78 rooms; floor 30 rooms))
  episodes seen twice: 1341
  scheme ships 197 themes in 21 families (14 rare)
  tier_history: 252 lines

warn   scheme_current.jsonl: second-order theme 2007scape/Arguing over the pixels that make the meme right is under 3 third-order themes (T3-004, T3-008, T3-031); rule 0 is single placement, a second one on the record with its why_not_one  [200 lines with this shape; first: 2007scape/Arguing over the pixels that make the meme right]
warn   scheme.jsonl T3-053 carries 2 exemplar(s); section 3 asks for three, each through `cite.py --room <sub> --code <id>`  [10 lines with this shape; first: T3-053]
warn   scheme.jsonl T3-128 is tier rare yet holds members from 3 rooms; say why it is not main

0 errors (0 distinct shapes), 211 warnings
```

The 200 warnings of the first shape are the record of rule 0: second-order themes under two or three kinds, each with its line in `multiplacement_log.jsonl`. The 10 of the second shape are the themes with fewer than three exemplars, named above. T3-128 is rare because its three rooms tell one episode (E1132).

**Ledgers at the close.**
- `scheme_current.jsonl`: 197 themes over 7,786 placed second-order themes, 13,432 placements;
- `scheme.jsonl`: 197 (183 main, 14 rare); `families.jsonl`: 21; `confusions.md`: 57 lines; `findings.jsonl`: 1;
- `theme_discovery.jsonl`: 197; `ideas-B1.jsonl`: 214; `kinds-B1.jsonl`: 13,657;
- `multiplacement_log.jsonl`: 6,663; `tier_history.jsonl`: 252; `unplaced-B1.jsonl`: 58; `episodes-B1.jsonl`: 1,341;
- `pass2-B1.jsonl`: 108; `pass2-chosen-B1.txt`: 108 rooms (125 lines);
- `saturation-B1.md`: 211 lines; `stopping-B1.md`: 384 lines;
- `handback-B1.md`: 896 words; `out/interview/B1e.md`: 698 words; `_head.md`: 2,281 words.
