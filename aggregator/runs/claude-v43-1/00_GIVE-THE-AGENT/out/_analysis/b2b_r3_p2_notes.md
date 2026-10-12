
## Leg B2b-r3-p2, J's answers checked, 2026-10-12

J's answers to QB2-012 and QB2-013 (13:47 Berlin) came during leg B2b-r3 and were applied there, before its close (section "J's answers (13:47 Berlin), and the close", above). This leg read both answers again with `mem.py asks` and checked the files.

- **QB2-012.** The assumption was that rounds stop at round 3 and the check leg writes no scheme edit. J's answer matches it: no round 4; a freeze leg of its own confirms the 443 gate pairs, reads the T3-002/T3-033/T3-038 cluster and makes any sentence fix there, and only the gold round in B2c tests that fix. Nothing that rested on the assumption changes. This leg starts none of the freeze work.
- **QB2-013.** The assumption was that round 3 is scored with the four lines as given and that no waiver is written without J's word. Round 3's figures stand unchanged, since the bag flag entered no figure. `return_waivers.jsonl` holds 20 lines, 4 of them ruled by J at QB2-013. `RETURN-B2.md` carries the rule that a bag with no other theme at the three-concept floor is not flagged, and the phrase "twenty themes at most".

`validate.py B2` reported 0 errors and 443 warnings, the same report as at B2b-r3's close. The 443 warnings are the gate pairs the freeze leg confirms. The leg closes with `done.sh B2`.
