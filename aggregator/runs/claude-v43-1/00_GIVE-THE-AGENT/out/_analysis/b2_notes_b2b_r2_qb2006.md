
### The close-check after the rename (QB2-006)

After the rename, `validate.py B2` reported:

```
stage B2:
  leg: check (2 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  _fleet_raw/B2/round-2-failed: 0 readers, 0 return lines
  author items 50, gold items 40, rounds scored 1, edits 286 (author-error 4), scheme ids 197 (scheme/scheme_current.jsonl)

ERROR  stage output 'scheme_final.md' was not written
ERROR  stage output 'scheme_final.jsonl' was not written
ERROR  stage output 'stability-B2.md' was not written
ERROR  stage output 'pilot_report.md' was not written
warn   _fleet_raw/B2/round-2-failed returned but no pilot_rounds.jsonl line is flagged "gold": true; the gold figure is reported beside the last round's
warn   scheme.jsonl: the pair T3-001|T3-017 touches an edited theme and is not confirmed against its current sentences [443 lines with this shape]
```

The round-2 error is gone. The check treats every folder in `_fleet_raw/B2/` that holds DONE and is not named `round-N` as a gold or stability dispatch, so it reads the stage as finished and asks for the freeze outputs. The stage is not finished, and writing those files now would be false. `round-2-failed/` still holds the dispatch's own DONE file, which I leave untouched. QB2-006 asks J which fix he wants: move the folder out of `_fleet_raw/B2/`, have the dispatch rename DONE, or have the check skip folders named `*-failed`. Meanwhile the folder stays where J named it, and the leg stays open if `done.sh` refuses. The five packets in `out/_packets-B2/round-2/` are ready for the new dispatch either way.
