
### The close-check, B2b-r2-p2: return lines that break the specification (QB2-009)

`validate.py B2` reported 44 errors in 9 shapes, all in `_fleet_raw/B2/round-2/`. `fleet.py` had accepted every line. `out/_analysis/b2_r2_return_problems.py` lists 16 of 150 lines in `out/_analysis/b2_r2_return_problems.txt`:
- One line is incomplete: `P03-r2-2/r1`, ainbowroad t04, has third_order and why only. It lacks confidence, read, exemplar_read, families_opened, t_start, t and support.
- One line mistypes its heading: `P03-r2-5/r2` position 7 returned AyyMD t02 where the packet holds t08. Its five support concepts are t08's.
- 14 lines cite concept ids that are not the item's own, in support, also_present or multiplacement_log. They are on sweden t01 (three readers), ainbowroad t04 (two), 2007scape t04 (two), theblackvoid t09, theblackvoid t12, leagueoflegends t02, dota2 t05, donaldglover t04, duckgame t02 and ainbowroad t07. Each cited id belongs to another second-order theme of the same room, except c1636 on 2007scape t04, which is not a concept of r/2007scape at all.

Every line carries its third_order, and the scores use nothing else. The stage says a return that fails the specification is reissued, not scored. Reissuing is the dispatch's work, not mine. QB2-009 asks J whether the dispatch reissues the ten affected returns (packet 2 r1, r2, r3; packet 3 r1, r2; packet 4 r1, r3; packet 5 r1, r2, r3), or the lines are scored as they stand with their errors on the record.

Meanwhile the scores stand as computed on all 150 lines (`pilot_rounds.jsonl` line 2). No edit rests on an affected line: edits 287 to 295 came from guatemala t02, nVade t04, n64 t02 and dofus t01, whose lines are all within the specification. The AyyMD t08 author-error verdict rests partly on the mistyped line, one of its two T3-023 placements. The bag figures (primary 1.000, also_present Jaccard 0.283) rest partly on the affected lines. If the returns are reissued, I rescore, write a superseding pilot_rounds line, and revisit these. The leg stays open until the close-check passes.
