
### Added after the section above, in the same leg

**The deal cluster.** Reading T3-010's 17 pairs found seven where a decide_when_both names T3-010 but no discriminator separates the pair: T3-012, T3-035, T3-039, T3-040, T3-084, T3-123 and T3-139. `mem.py gates` checks only `must_not_show` lines, so it does not see this shape. Seven questions were written into both gates (`out/_analysis/b2_newpairs_r1c.json`; scheme_edits 273 to 286). They are kind scheme-ambiguous, with `caused_by gates:A|T3-010` and 14 tier_history lines.

The final counts are:
- `scheme_edits.jsonl`: 286 lines, 202 gate-check mirrors and 84 edits that owe rechecks;
- `tier_history.jsonl`: 372 lines;
- `mem.py gates`: no defect; 28 pairs confirmed, 0 stale, 464 unconfirmed. The unconfirmed pairs are read before the freeze.

**The rechecks, final.** 697 recheck records, none owed. 22 items moved from my original placement: 18 author-errors and 4 edits doing their work.
- 70 records failed when first tried. An earlier recheck had already moved those items off the themes the later edits touch, so `mem.py` no longer counted them as owed; the record was right to refuse them.
- `mem.py recheck` takes about 4.5 seconds a record, and the first run went past the ten-minute foreground limit into the background. The rest ran in the foreground in slices (`--max`).
