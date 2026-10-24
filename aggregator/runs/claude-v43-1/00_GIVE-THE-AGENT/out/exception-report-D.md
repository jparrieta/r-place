# Exception report, stage D3

Built at D3c by `_analysis/d3c_exception_report2.py` (seed 2026102410) from the ledgers and their last rulings; no figure in it is typed. It reports the first return (served e15f9647...) and the re-check (served 46384686..., the version frozen at D3c, QD3-011), each line by its last ruling. 'Shared' lines are accepted specifications, paired elaborations and corrections; 'limits' are lines accepted with kind none (evidence limits); 'particulars' are locally supported particulars, with the NONPORTABLE lines counted apart. The model's top elements are read as prior.md's spine (a start, calls, building, keeping): R01, P01, P03, P05, A02, A01, A03.

## The composition criteria (prior.md section 3), with the shares

prior.md fixes no numerical cutoff. It asks for local adequacy over 705 rooms, a count of distinct shared changes apart from ledger lines, the curve of those changes over a seeded order of rooms, the share of rooms whose particulars touch the top elements, and the fixed-global verdicts, particulars and corrections met twice as diagnostics, with pre- and post-adaptation fit. Each is below, with its denominator.

### Ledger lines, by ruling

- **first return:** 42243 lines in 705 rooms. Specifications 20637, paired elaborations 1282, corrections 54, accepted proposals 729, limits 13981, particulars 484 and NONPORTABLE particulars 752, rejected 4324, pending 0, unruled 0.
  - Particulars are 2.9% of the lines and 5.2% of the lines that are not limits or rejected. Rooms carrying at least one particular: 493 of 705. Rooms by their particulars: 0: 212, 1 to 2: 317, 3 to 5: 138, 6 or more: 38.
  - Rooms with a particular on a top element (R01, P01, P03, P05, A02, A01, A03): 98 of 705 (13.9%).
- **re-check:** 53493 lines in 705 rooms. Specifications 25410, paired elaborations 1061, corrections 18, accepted proposals 2, limits 20941, particulars 699 and NONPORTABLE particulars 814, rejected 4548, pending 0, unruled 0.
  - Particulars are 2.8% of the lines and 5.4% of the lines that are not limits or rejected. Rooms carrying at least one particular: 525 of 705. Rooms by their particulars: 0: 180, 1 to 2: 297, 3 to 5: 171, 6 or more: 57.
  - Rooms with a particular on a top element (R01, P01, P03, P05, A02, A01, A03): 127 of 705 (18.0%).

### Distinct shared changes, apart from ledger lines

- Accepted elaborations and corrections: 2415 ledger lines (both ledgers). D3's pairs join them into 546 groups on one element each (926 pairs cross the two ledgers). 499 groups are met in two rooms or more: these are the distinct shared changes, over 2368 ledger lines. 47 groups stay in one room (a lone line whose pair was re-ruled, or a room's first-return line and its re-check repeat).
- Of the 499 distinct shared changes, 393 carry a re-check line (they are met against the frozen version) and 106 rest on first-return lines alone.
- Distinct shared changes by element (the ten most): P01 78, P05 59, K01 55, P04 55, P02 42, P03 32, P12 29, P07 18, P13 17, P11 15.
- prior.md asks that the two rooms be unlike in size, side or form. This report does not test that; it is D4's, where the branches are built from these keys.
- **The curve** (rooms in a seeded order, seed 2026102410; a shared change counts once its second room has entered). After 235 rooms: 122; after 470: 305; after all 705: 499. The first third adds 122, the second 183 and the last 194.
- The groups by their rooms: 2 rooms: 267, 3 to 5 rooms: 195, 6 to 20 rooms: 36, more than 20 rooms: 1. In any order of the rooms, a change met in two rooms counts only when the later of the two enters, so a set of changes each met in few rooms keeps growing to the end of the order. For these group sizes, the expected adds by third over random orders are 123, 190 and 186, against the seeded 122, 183 and 194. So the curve's shape comes from how many rooms each change is met in, and most changes are met in few rooms. prior.md names a curve that does not flatten over the last third as a sign of unbounded revision; on D3's pair groups the curve does not flatten. The pairs join two lines at a time and were not built to merge every line stating one change, so the group count can exceed the count of distinct changes; D4's keys may merge groups.
- Accepted `propose` lines are counted apart: they entered the model as 15 candidate elements (P23, P24, P25, P26, P27, P28, P29, P30, P31, P32, P33, P34, K05, K06, K07), and they are new elements, not changes to a standing one.

### Local adequacy, and fit before and after adaptation

- **Local status** (the labelers' revised local accounts, `rooms/<sub>/model-D-recheck.md`, 705 rooms): unresolved 705. Their own grade: composes-with-residue 705.
- The labelers marked a room unresolved where a claim stayed open in their own account. After the adjudication, no ledger line is pending: every line is accepted, a particular or rejected. The local status is reported as the labelers wrote it; it is not raised by my rulings, and a room is not called locally validated here.
- **Fit before and after adaptation.** Before: the fixed-global verdicts below, readers judging each room against the model as served. After: the labelers' grade above, on the room's adapted account. Exact local fit is not evidence of global composition by itself.

## The fixed-global verdicts, by version

- **First return (e15f9647...; the readers' agreed verdict, else my D3a-56 ruling):** cannot-tell 14, composes 201, composes-with-residue 489, does-not-compose 1, over 705 rooms; 163 rooms ruled where the readers split.
- **Re-check (46384686...; the readers' agreed verdict, else my G62 ruling):** cannot-tell 19, composes 630, composes-with-residue 56, over 705 rooms; 161 rooms ruled where the readers split.
- does-not-compose: picturegame at the first return (its kind in `uncomposed-D.md`); none at the re-check.
- cannot-tell at the re-check, by threshold: coded-share 19.
- validate.py's counts take the last ruling per room in `verdicts-D.jsonl`, else the first-return readers' agreed line, so they mix the two versions. The notes give both.

## Corrections met twice (section 2), reported apart

Accepted corrections, both ledgers, grouped by element and by the lifted node at the third or fourth level, two rooms or more: 19 groups, 19 of them cited in `model/history.jsonl`.
- A21 at T3-010: 20 lines (first return 20) in 20 rooms: ScottPilgrim, TsundereSharks, asexuality, buffalobills, croatia, dota2, funhaus, gravityfalls, italy, maryland, rit, singapore, straya, switzerland, telegram, transformers, turkey, uiuc, uoft, uva. Cited: yes.
- A21 at T3-014: 2 lines (first return 2) in 2 rooms: FloydVsVoid, jerma985. Cited: yes.
- A21 at T3-126: 2 lines (first return 2) in 2 rooms: destiny, rainbowgrid. Cited: yes.
- A21 at T3-188: 2 lines (first return 2) in 2 rooms: PlaceNL, denmark. Cited: yes.
- A21 at T4-006: 2 lines (first return 2) in 2 rooms: katawashoujo, newzealand. Cited: yes.
- A21 at T4-010: 2 lines (first return 2) in 2 rooms: FloydVsVoid, jerma985. Cited: yes.
- A21 at T4-014: 4 lines (first return 3, re-check 1) in 3 rooms: adventuretime, dallasstars, masseffect. Cited: yes.
- A21 at T4-016: 25 lines (first return 24, re-check 1) in 24 rooms: ScottPilgrim, TsundereSharks, asexuality, buffalobills, croatia, destiny, dota2, funhaus, gravityfalls, italy, lakers, maryland, rainbowgrid, rit, singapore, straya, switzerland, telegram, transformers, turkey, uiuc, uoft, uva, weezer. Cited: yes.
- A21 at T4-019: 2 lines (first return 2) in 2 rooms: PlaceNL, denmark. Cited: yes.
- P05 at T3-038: 3 lines (first return 1, re-check 2) in 3 rooms: monsterhunter, oneshot, thesilphroad. Cited: yes.
- P05 at T3-170: 3 lines (first return 1, re-check 2) in 3 rooms: bangtan, halo, portugal. Cited: yes.
- P05 at T4-006: 2 lines (re-check 2) in 2 rooms: polska, satania. Cited: yes.
- P05 at T4-007: 3 lines (first return 1, re-check 2) in 3 rooms: monsterhunter, oneshot, thesilphroad. Cited: yes.
- P05 at T4-013: 3 lines (first return 2, re-check 1) in 3 rooms: OnePiece, armok, leagueoflegends. Cited: yes.
- P05 at T4-019: 3 lines (first return 1, re-check 2) in 3 rooms: bangtan, halo, portugal. Cited: yes.
- R01 at T3-002: 4 lines (first return 3, re-check 1) in 4 rooms: androidgaming, hentai, transformers, transgender. Cited: yes.
- R01 at T3-033: 6 lines (first return 4, re-check 2) in 5 rooms: gravityfalls, hearthstone, katawashoujo, shitredditsays, tetris. Cited: yes.
- R01 at T4-005: 4 lines (first return 3, re-check 1) in 4 rooms: androidgaming, hentai, transformers, transgender. Cited: yes.
- R01 at T4-006: 8 lines (first return 6, re-check 2) in 7 rooms: Madeon, gravityfalls, hearthstone, katawashoujo, shitredditsays, tetris, vietnam. Cited: yes.
- Repeated corrections are candidates for clusters, never a failure threshold. The moves they caused are 172 (R01), 173 (P05), 176 (A21's bound) and 197 (P05's scope, with no change to the frozen model).

## P05's added clause: the scope decision at D3c (F-024; move 197; QD3-011)

The clause move 173 added to P05 ('until its keepers are told of it, and it is lost or given up where the telling does not reach them') fails in nine rooms whose re-check correction the ledger accepts. The scope is decided as a bound with a cluster branch, carried in F-024 and history line 172; the frozen words are unchanged. The trunk is the clause, bounded to rooms where the keepers can learn of a planned change only by being told and no informed member holds it.
- completeanarchy: R-completeanarchy-c187508d7ae3-022 (the keepers read the change from its shape: the branch)
- polska: R-polska-dadda7358f9a-049 (the keepers read the change from its shape: the branch)
- satania: R-satania-84df196116f3-022 (the keepers read the change from its shape: the branch)
- halo: R-halo-b988854ba168-036 (the keepers read the change from its shape: the branch)
- bangtan: R-bangtan-7efe23da0d0c-070 (the keepers read the change from its shape: the branch)
- thesilphroad: R-thesilphroad-a3f86618e239-018 (the keepers read the change from its shape: the branch)
- armok: R-armok-8852b2ab85f8-022 (informed members hold the change: a second limit)
- maryland: R-maryland-d1b6e2d1d5f3-017 (informed members hold the change: a second limit)
- oneshot: R-oneshot-e840e127e9b2-013 (informed members hold the change: a second limit)

## Rooms whose adaptations are all particulars

None, over 705 rooms and both ledgers: in every room at least one line is accepted or rejected rather than a particular. The contract's sentence, 'a model whose adaptations are all particulars has not composed', applies to no room and not to the set.
- A stricter reading: rooms with no shared line (specification, paired elaboration or correction) in the re-check: 0.

## Per element: rooms adapting it, by op (re-check; shared lines, accepted proposals and particulars)

| element | instantiate | restrict | add-condition | add-step | link | contradict | absent | propose | rooms with a correction | rooms with a particular |
|---|---|---|---|---|---|---|---|---|---|---|
| (none) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 240 | 0 | 239 |
| A01 | 143 | 88 | 10 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| A02 | 171 | 54 | 16 | 5 | 0 | 0 | 0 | 0 | 0 | 2 |
| A03 | 255 | 36 | 31 | 1 | 0 | 0 | 2 | 0 | 0 | 7 |
| A04 | 61 | 136 | 27 | 1 | 0 | 0 | 2 | 0 | 0 | 7 |
| A05 | 165 | 124 | 61 | 4 | 0 | 0 | 5 | 0 | 0 | 10 |
| A06 | 34 | 97 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 4 |
| A07 | 76 | 65 | 19 | 0 | 0 | 0 | 1 | 0 | 0 | 3 |
| A08 | 21 | 115 | 8 | 0 | 0 | 0 | 2 | 0 | 0 | 8 |
| A09 | 23 | 52 | 4 | 0 | 0 | 0 | 5 | 0 | 0 | 6 |
| A10 | 23 | 201 | 11 | 0 | 0 | 1 | 26 | 0 | 0 | 28 |
| A11 | 9 | 275 | 8 | 1 | 0 | 0 | 1 | 0 | 0 | 3 |
| A12 | 358 | 136 | 23 | 4 | 0 | 0 | 1 | 0 | 0 | 0 |
| A13 | 37 | 148 | 21 | 3 | 0 | 0 | 5 | 0 | 0 | 6 |
| A14 | 101 | 37 | 6 | 2 | 0 | 0 | 3 | 0 | 0 | 6 |
| A15 | 50 | 65 | 4 | 1 | 0 | 0 | 3 | 0 | 0 | 7 |
| A16 | 192 | 59 | 8 | 7 | 0 | 0 | 14 | 0 | 0 | 19 |
| A17 | 88 | 28 | 4 | 0 | 0 | 0 | 16 | 0 | 0 | 15 |
| A18 | 55 | 23 | 0 | 0 | 0 | 0 | 13 | 0 | 0 | 14 |
| A19 | 11 | 29 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| A20 | 41 | 40 | 4 | 0 | 0 | 0 | 1 | 0 | 0 | 2 |
| A21 | 42 | 15 | 3 | 0 | 0 | 0 | 11 | 0 | 2 | 0 |
| C01 | 96 | 60 | 26 | 15 | 1 | 0 | 2 | 0 | 0 | 4 |
| C02 | 97 | 35 | 3 | 0 | 0 | 0 | 21 | 0 | 0 | 30 |
| D01 | 0 | 0 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| D02 | 0 | 2 | 1 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| D03 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| D04 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| D05 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| D06 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| D07 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| D08 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| K01 | 354 | 37 | 35 | 111 | 4 | 0 | 1 | 0 | 0 | 20 |
| K02 | 514 | 3 | 5 | 9 | 0 | 0 | 2 | 0 | 0 | 14 |
| K03 | 124 | 7 | 1 | 0 | 0 | 0 | 18 | 0 | 0 | 23 |
| K04 | 443 | 13 | 9 | 9 | 5 | 0 | 4 | 0 | 0 | 36 |
| K05 | 501 | 7 | 6 | 10 | 3 | 0 | 2 | 0 | 0 | 26 |
| K06 | 305 | 36 | 8 | 14 | 4 | 0 | 1 | 0 | 0 | 5 |
| K07 | 88 | 30 | 3 | 1 | 0 | 0 | 15 | 0 | 0 | 22 |
| P01 | 686 | 3 | 42 | 54 | 70 | 0 | 0 | 0 | 0 | 57 |
| P02 | 673 | 11 | 41 | 69 | 74 | 0 | 1 | 0 | 2 | 41 |
| P03 | 647 | 3 | 13 | 31 | 141 | 0 | 0 | 0 | 0 | 26 |
| P04 | 643 | 5 | 34 | 114 | 46 | 0 | 0 | 0 | 0 | 11 |
| P05 | 602 | 229 | 112 | 91 | 103 | 0 | 2 | 0 | 9 | 45 |
| P06 | 554 | 15 | 21 | 29 | 11 | 0 | 1 | 0 | 0 | 17 |
| P07 | 566 | 19 | 59 | 37 | 45 | 0 | 4 | 0 | 0 | 24 |
| P08 | 541 | 7 | 42 | 75 | 47 | 0 | 1 | 0 | 0 | 17 |
| P09 | 488 | 36 | 19 | 16 | 26 | 0 | 3 | 0 | 0 | 38 |
| P10 | 252 | 37 | 10 | 32 | 7 | 0 | 52 | 0 | 0 | 63 |
| P11 | 641 | 27 | 28 | 62 | 35 | 0 | 1 | 0 | 0 | 20 |
| P12 | 639 | 9 | 11 | 57 | 34 | 0 | 0 | 0 | 0 | 81 |
| P13 | 284 | 36 | 48 | 63 | 36 | 3 | 2 | 0 | 0 | 15 |
| P14 | 247 | 60 | 40 | 83 | 28 | 0 | 3 | 0 | 0 | 6 |
| P15 | 585 | 17 | 5 | 8 | 18 | 0 | 9 | 0 | 0 | 6 |
| P16 | 582 | 18 | 89 | 53 | 44 | 0 | 1 | 0 | 0 | 27 |
| P17 | 314 | 24 | 17 | 10 | 12 | 0 | 5 | 0 | 0 | 15 |
| P18 | 382 | 20 | 5 | 11 | 8 | 0 | 5 | 0 | 0 | 20 |
| P19 | 264 | 48 | 34 | 15 | 6 | 0 | 9 | 0 | 0 | 12 |
| P20 | 298 | 24 | 22 | 51 | 9 | 0 | 3 | 0 | 0 | 13 |
| P21 | 141 | 19 | 2 | 4 | 2 | 0 | 2 | 0 | 0 | 2 |
| P22 | 195 | 30 | 10 | 7 | 3 | 0 | 8 | 0 | 0 | 14 |
| P23 | 436 | 61 | 59 | 61 | 46 | 0 | 1 | 0 | 0 | 10 |
| P24 | 573 | 3 | 4 | 24 | 23 | 0 | 1 | 0 | 0 | 18 |
| P25 | 155 | 34 | 20 | 26 | 21 | 0 | 1 | 0 | 0 | 8 |
| P26 | 492 | 13 | 3 | 10 | 9 | 0 | 2 | 0 | 0 | 23 |
| P27 | 457 | 44 | 12 | 13 | 30 | 0 | 1 | 0 | 0 | 44 |
| P28 | 66 | 18 | 5 | 5 | 4 | 0 | 5 | 0 | 0 | 6 |
| P29 | 117 | 12 | 5 | 5 | 1 | 0 | 6 | 0 | 0 | 9 |
| P30 | 56 | 8 | 2 | 3 | 1 | 0 | 6 | 0 | 0 | 8 |
| P31 | 397 | 25 | 1 | 7 | 0 | 0 | 2 | 0 | 0 | 4 |
| P32 | 145 | 29 | 10 | 3 | 8 | 0 | 8 | 0 | 0 | 8 |
| P33 | 52 | 32 | 3 | 5 | 0 | 0 | 1 | 0 | 0 | 2 |
| P34 | 3 | 1 | 1 | 0 | 1 | 0 | 6 | 0 | 0 | 5 |
| R01 | 639 | 7 | 0 | 2 | 0 | 0 | 0 | 0 | 5 | 12 |
| R02 | 509 | 5 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |

## Per room: particulars against accepted shared lines

Shared = accepted specifications, paired elaborations and corrections. Each cell: re-check / first return.

| room | shared | of them corrections | limits | particulars | NONPORTABLE | rejected |
|---|---|---|---|---|---|---|
| 2007scape | 58 / 52 | 0 / 0 | 8 / 3 | 2 / 2 | 0 / 1 | 5 / 8 |
| 49ers | 53 / 41 | 0 / 0 | 24 / 15 | 0 / 0 | 1 / 0 | 6 / 7 |
| 4chan | 49 / 39 | 0 / 0 | 30 / 20 | 7 / 7 | 3 / 2 | 4 / 5 |
| aceattorney | 47 / 38 | 0 / 0 | 21 / 13 | 1 / 1 | 1 / 0 | 6 / 5 |
| acecombat | 33 / 30 | 0 / 0 | 36 / 23 | 0 / 0 | 0 / 0 | 5 / 5 |
| AceOfAngels8 | 16 / 19 | 0 / 0 | 49 / 34 | 0 / 1 | 2 / 0 | 3 / 3 |
| AcePlace | 40 / 36 | 0 / 0 | 24 / 19 | 3 / 1 | 2 / 0 | 9 / 9 |
| achievement_hunter | 29 / 22 | 0 / 0 | 34 / 22 | 0 / 0 | 0 / 0 | 11 / 10 |
| adventuretime | 42 / 38 | 1 / 1 | 21 / 11 | 0 / 0 | 1 / 0 | 5 / 5 |
| aeon | 17 / 14 | 0 / 0 | 49 / 37 | 0 / 0 | 0 / 0 | 5 / 3 |
| aeskwadraat | 11 / 9 | 0 / 0 | 27 / 10 | 1 / 1 | 0 / 0 | 1 / 1 |
| afip | 27 / 21 | 0 / 0 | 34 / 27 | 0 / 0 | 0 / 0 | 8 / 8 |
| aggies | 50 / 43 | 0 / 0 | 21 / 14 | 1 / 1 | 0 / 0 | 8 / 4 |
| ainbowroad | 57 / 41 | 0 / 0 | 14 / 11 | 2 / 0 | 1 / 3 | 10 / 12 |
| albania | 34 / 29 | 0 / 0 | 33 / 13 | 1 / 0 | 0 / 0 | 2 / 2 |
| alberta | 29 / 26 | 0 / 0 | 35 / 23 | 1 / 0 | 4 / 5 | 6 / 5 |
| AMD | 46 / 37 | 0 / 0 | 18 / 11 | 4 / 3 | 1 / 2 | 9 / 9 |
| AmericanFlaginPlace | 61 / 48 | 0 / 0 | 13 / 10 | 0 / 0 | 0 / 0 | 11 / 14 |
| anaheimducks | 45 / 44 | 0 / 0 | 27 / 16 | 0 / 0 | 0 / 0 | 9 / 9 |
| anarchism | 45 / 44 | 0 / 0 | 29 / 18 | 2 / 1 | 2 / 1 | 8 / 5 |
| anarcho_capitalism | 45 / 37 | 0 / 0 | 23 / 18 | 2 / 2 | 2 / 0 | 8 / 12 |
| anarchocapitalism | 19 / 16 | 0 / 0 | 47 / 36 | 1 / 1 | 0 / 0 | 6 / 6 |
| androidgaming | 37 / 27 | 0 / 1 | 41 / 28 | 0 / 0 | 0 / 0 | 0 / 1 |
| animalcrossing | 45 / 35 | 0 / 0 | 25 / 17 | 1 / 1 | 0 / 2 | 7 / 7 |
| anime | 56 / 48 | 0 / 0 | 26 / 14 | 3 / 3 | 2 / 3 | 6 / 5 |
| anime_irl | 32 / 26 | 0 / 0 | 38 / 28 | 3 / 3 | 5 / 5 | 7 / 7 |
| aoe2 | 40 / 36 | 0 / 0 | 20 / 10 | 0 / 0 | 1 / 5 | 9 / 10 |
| apocalypserising | 26 / 23 | 0 / 0 | 36 / 26 | 2 / 3 | 0 / 0 | 10 / 8 |
| AprilKnights | 44 / 32 | 0 / 0 | 24 / 11 | 1 / 0 | 1 / 4 | 13 / 10 |
| araragi | 18 / 16 | 0 / 0 | 42 / 31 | 0 / 0 | 0 / 0 | 5 / 2 |
| archlinux | 49 / 36 | 0 / 0 | 20 / 13 | 1 / 1 | 1 / 1 | 5 / 7 |
| argentina | 53 / 50 | 0 / 1 | 12 / 6 | 2 / 1 | 1 / 0 | 8 / 11 |
| armenia | 34 / 30 | 0 / 0 | 23 / 10 | 0 / 0 | 0 / 1 | 11 / 9 |
| armok | 49 / 32 | 1 / 0 | 27 / 21 | 1 / 0 | 3 / 3 | 8 / 8 |
| aromantic | 16 / 15 | 0 / 0 | 49 / 38 | 1 / 0 | 1 / 1 | 4 / 3 |
| asexual | 27 / 19 | 0 / 0 | 32 / 22 | 0 / 0 | 2 / 2 | 9 / 10 |
| asexuality | 47 / 39 | 0 / 1 | 24 / 15 | 0 / 0 | 1 / 1 | 7 / 5 |
| asktransgender | 38 / 34 | 0 / 0 | 24 / 14 | 0 / 0 | 3 / 2 | 12 / 10 |
| auburn | 32 / 31 | 0 / 0 | 30 / 19 | 3 / 0 | 3 / 3 | 5 / 3 |
| australia | 47 / 39 | 0 / 0 | 19 / 9 | 10 / 10 | 1 / 0 | 10 / 12 |
| austria | 50 / 43 | 0 / 0 | 20 / 13 | 1 / 1 | 1 / 1 | 4 / 5 |
| austriahungary | 6 / 6 | 0 / 0 | 60 / 45 | 0 / 0 | 1 / 1 | 0 / 0 |
| AvoArmy | 45 / 34 | 0 / 0 | 13 / 8 | 2 / 1 | 0 / 0 | 4 / 2 |
| AyyMD | 49 / 48 | 0 / 0 | 20 / 10 | 1 / 0 | 1 / 1 | 4 / 3 |
| azerbaijan | 10 / 10 | 0 / 0 | 57 / 43 | 0 / 0 | 0 / 0 | 2 / 1 |
| azores | 4 / 2 | 0 / 0 | 62 / 49 | 0 / 0 | 0 / 0 | 1 / 1 |
| babymetal | 63 / 47 | 0 / 0 | 13 / 9 | 2 / 1 | 2 / 2 | 9 / 9 |
| bahrain | 13 / 11 | 0 / 0 | 51 / 39 | 2 / 1 | 0 / 1 | 4 / 4 |
| bakchodi | 45 / 38 | 0 / 0 | 18 / 12 | 1 / 1 | 0 / 0 | 11 / 8 |
| bangladesh | 34 / 32 | 0 / 0 | 35 / 22 | 3 / 1 | 1 / 2 | 6 / 5 |
| bangtan | 42 / 35 | 1 / 0 | 25 / 18 | 0 / 0 | 0 / 0 | 10 / 10 |
| bannedfromanime_irl | 1 / 2 | 0 / 0 | 44 / 29 | 0 / 0 | 1 / 1 | 3 / 2 |
| bardmains | 49 / 36 | 0 / 0 | 28 / 22 | 1 / 1 | 1 / 1 | 5 / 5 |
| batman | 31 / 30 | 0 / 1 | 36 / 24 | 1 / 1 | 3 / 1 | 3 / 1 |
| battlecats | 31 / 26 | 0 / 0 | 38 / 27 | 0 / 0 | 2 / 2 | 4 / 4 |
| baylor | 18 / 14 | 0 / 0 | 51 / 38 | 1 / 0 | 0 / 1 | 2 / 2 |
| bdsm | 16 / 15 | 0 / 0 | 47 / 34 | 0 / 0 | 0 / 1 | 5 / 4 |
| bees | 8 / 8 | 0 / 0 | 57 / 43 | 1 / 1 | 0 / 0 | 1 / 0 |
| belgium | 45 / 35 | 0 / 0 | 18 / 10 | 1 / 0 | 0 / 4 | 8 / 8 |
| berkeley | 35 / 34 | 0 / 0 | 23 / 11 | 2 / 2 | 2 / 1 | 12 / 10 |
| berserk | 48 / 37 | 0 / 0 | 25 / 17 | 1 / 1 | 0 / 0 | 9 / 9 |
| bigbang | 8 / 8 | 0 / 0 | 29 / 13 | 1 / 0 | 0 / 1 | 2 / 1 |
| bih | 31 / 25 | 0 / 0 | 37 / 25 | 2 / 1 | 0 / 1 | 4 / 4 |
| bindingofisaac | 64 / 51 | 0 / 0 | 16 / 11 | 0 / 0 | 1 / 3 | 11 / 6 |
| bisexual | 61 / 46 | 0 / 0 | 20 / 14 | 2 / 1 | 1 / 1 | 8 / 7 |
| bitcoin | 46 / 40 | 0 / 0 | 15 / 7 | 1 / 0 | 0 / 4 | 8 / 10 |
| blackmirror | 32 / 27 | 0 / 0 | 33 / 23 | 0 / 0 | 0 / 0 | 6 / 7 |
| bobross | 15 / 15 | 0 / 0 | 52 / 37 | 0 / 0 | 0 / 0 | 3 / 3 |
| borderlands | 23 / 20 | 0 / 0 | 39 / 26 | 3 / 0 | 6 / 9 | 8 / 7 |
| borussiadortmund | 55 / 43 | 0 / 0 | 23 / 16 | 0 / 0 | 1 / 1 | 4 / 4 |
| bostonbruins | 46 / 40 | 0 / 0 | 21 / 14 | 1 / 1 | 1 / 0 | 11 / 8 |
| bostonceltics | 42 / 34 | 0 / 0 | 21 / 13 | 1 / 1 | 1 / 1 | 7 / 9 |
| brasil | 58 / 49 | 0 / 0 | 8 / 3 | 1 / 2 | 3 / 3 | 5 / 7 |
| Bravenewbies | 5 / 7 | 0 / 0 | 62 / 49 | 1 / 0 | 0 / 1 | 0 / 1 |
| Braveryjerk | 6 / 8 | 0 / 0 | 56 / 41 | 2 / 1 | 0 / 1 | 5 / 3 |
| bretagne | 25 / 20 | 0 / 0 | 42 / 32 | 0 / 0 | 0 / 0 | 5 / 5 |
| btc | 31 / 26 | 0 / 0 | 25 / 15 | 2 / 1 | 6 / 9 | 8 / 8 |
| buffalo | 33 / 27 | 0 / 0 | 32 / 23 | 0 / 0 | 2 / 2 | 6 / 5 |
| buffalobills | 52 / 49 | 0 / 1 | 15 / 5 | 2 / 2 | 2 / 1 | 6 / 4 |
| buffalowizards | 21 / 19 | 0 / 0 | 41 / 30 | 1 / 1 | 3 / 2 | 5 / 4 |
| bulgaria | 49 / 39 | 0 / 0 | 22 / 14 | 2 / 1 | 3 / 2 | 6 / 6 |
| calgaryflames | 47 / 43 | 0 / 0 | 12 / 5 | 0 / 0 | 2 / 4 | 10 / 10 |
| calvinandhobbes | 35 / 27 | 0 / 0 | 31 / 14 | 0 / 0 | 3 / 1 | 5 / 3 |
| canada | 50 / 39 | 0 / 0 | 17 / 10 | 1 / 1 | 0 / 0 | 8 / 8 |
| canucks | 69 / 50 | 0 / 0 | 22 / 15 | 2 / 2 | 0 / 0 | 6 / 6 |
| cardinals | 47 / 36 | 0 / 0 | 27 / 18 | 0 / 0 | 1 / 1 | 4 / 4 |
| carletonu | 10 / 9 | 0 / 0 | 55 / 39 | 0 / 0 | 0 / 0 | 6 / 7 |
| catalonia | 39 / 30 | 0 / 0 | 33 / 16 | 1 / 0 | 4 / 3 | 4 / 2 |
| catalunya | 44 / 39 | 0 / 0 | 23 / 14 | 0 / 0 | 0 / 0 | 7 / 5 |
| catholicism | 45 / 39 | 0 / 0 | 22 / 14 | 0 / 0 | 2 / 0 | 10 / 10 |
| cavestory | 33 / 29 | 0 / 0 | 32 / 15 | 0 / 0 | 3 / 2 | 5 / 5 |
| CelticFc | 20 / 16 | 0 / 0 | 44 / 32 | 0 / 0 | 0 / 0 | 6 / 6 |
| cfb | 50 / 40 | 0 / 0 | 7 / 4 | 3 / 3 | 0 / 0 | 11 / 11 |
| cgpgrey | 35 / 32 | 0 / 0 | 36 / 27 | 0 / 0 | 1 / 0 | 6 / 6 |
| chelseafc | 50 / 47 | 0 / 0 | 24 / 14 | 1 / 2 | 0 / 0 | 3 / 6 |
| chess | 24 / 23 | 0 / 0 | 29 / 24 | 2 / 1 | 14 / 5 | 5 / 7 |
| chibears | 40 / 35 | 0 / 0 | 23 / 14 | 1 / 0 | 2 / 2 | 7 / 8 |
| chicago | 53 / 42 | 0 / 0 | 27 / 17 | 4 / 2 | 0 / 2 | 3 / 2 |
| chicubs | 55 / 41 | 0 / 0 | 14 / 9 | 1 / 1 | 1 / 0 | 13 / 12 |
| chile | 54 / 43 | 0 / 0 | 17 / 10 | 0 / 0 | 2 / 2 | 6 / 6 |
| ChronoTrigger | 36 / 28 | 0 / 0 | 23 / 17 | 0 / 0 | 0 / 0 | 12 / 9 |
| churchofhelix | 5 / 5 | 0 / 0 | 60 / 45 | 0 / 0 | 0 / 0 | 1 / 1 |
| cirkeltrek | 35 / 32 | 0 / 0 | 27 / 13 | 2 / 0 | 0 / 4 | 7 / 7 |
| CKCrusaders | 30 / 24 | 0 / 0 | 31 / 21 | 2 / 0 | 3 / 5 | 8 / 8 |
| Clannad | 21 / 17 | 0 / 0 | 47 / 19 | 2 / 1 | 1 / 2 | 0 / 1 |
| clashroyale | 42 / 40 | 0 / 0 | 25 / 12 | 5 / 4 | 0 / 0 | 5 / 4 |
| clg | 50 / 40 | 0 / 0 | 21 / 14 | 0 / 0 | 0 / 0 | 6 / 6 |
| cloud9 | 44 / 37 | 0 / 0 | 17 / 12 | 0 / 0 | 0 / 0 | 16 / 11 |
| clubpenguin | 43 / 38 | 0 / 0 | 23 / 14 | 2 / 2 | 3 / 2 | 6 / 5 |
| cmu | 33 / 26 | 0 / 0 | 36 / 16 | 0 / 0 | 0 / 0 | 4 / 3 |
| coldplay | 43 / 37 | 0 / 0 | 25 / 16 | 0 / 0 | 0 / 0 | 10 / 8 |
| colombia | 41 / 30 | 0 / 0 | 26 / 18 | 0 / 0 | 5 / 2 | 8 / 7 |
| colorado | 19 / 18 | 0 / 0 | 39 / 29 | 2 / 0 | 1 / 2 | 8 / 8 |
| columbia | 42 / 35 | 0 / 0 | 35 / 25 | 0 / 0 | 2 / 1 | 5 / 3 |
| completeanarchy | 53 / 44 | 1 / 0 | 17 / 12 | 0 / 0 | 0 / 0 | 8 / 6 |
| compsoc | 9 / 9 | 0 / 0 | 55 / 40 | 0 / 0 | 0 / 0 | 4 / 4 |
| Cornwall | 11 / 9 | 0 / 0 | 48 / 35 | 0 / 0 | 0 / 0 | 8 / 8 |
| corridor | 40 / 28 | 0 / 0 | 36 / 28 | 3 / 1 | 0 / 1 | 6 / 5 |
| COSI | 10 / 7 | 0 / 0 | 29 / 15 | 0 / 0 | 0 / 0 | 6 / 5 |
| costa_rica | 34 / 27 | 0 / 0 | 24 / 17 | 2 / 1 | 1 / 2 | 11 / 9 |
| counting | 12 / 9 | 0 / 0 | 20 / 17 | 2 / 2 | 22 / 20 | 8 / 7 |
| cowchop | 43 / 38 | 0 / 0 | 24 / 17 | 0 / 0 | 1 / 0 | 6 / 4 |
| criticalrole | 48 / 40 | 1 / 0 | 22 / 14 | 1 / 1 | 0 / 0 | 6 / 5 |
| croatia | 37 / 43 | 0 / 1 | 19 / 10 | 2 / 1 | 6 / 0 | 6 / 8 |
| crusaderkings | 48 / 34 | 0 / 0 | 21 / 16 | 2 / 1 | 4 / 3 | 12 / 11 |
| CryptoFR | 9 / 3 | 0 / 0 | 60 / 46 | 1 / 0 | 1 / 2 | 0 / 0 |
| crystalclear | 10 / 9 | 0 / 0 | 54 / 40 | 0 / 0 | 0 / 0 | 3 / 3 |
| CSUFoCo | 18 / 15 | 0 / 0 | 43 / 32 | 1 / 1 | 2 / 1 | 6 / 5 |
| cubers | 68 / 50 | 0 / 0 | 14 / 13 | 1 / 2 | 1 / 1 | 12 / 11 |
| cuboulder | 19 / 15 | 0 / 0 | 44 / 35 | 0 / 0 | 1 / 1 | 4 / 4 |
| czech | 47 / 38 | 0 / 0 | 9 / 5 | 0 / 0 | 7 / 7 | 10 / 9 |
| daftpunk | 39 / 41 | 0 / 0 | 33 / 16 | 0 / 0 | 0 / 0 | 4 / 3 |
| dallasstars | 47 / 40 | 0 / 1 | 20 / 10 | 1 / 0 | 4 / 3 | 5 / 4 |
| danganronpa | 48 / 40 | 0 / 0 | 17 / 13 | 1 / 1 | 1 / 0 | 5 / 4 |
| dankmemes | 27 / 22 | 0 / 0 | 43 / 34 | 4 / 3 | 3 / 3 | 4 / 3 |
| darksouls | 40 / 36 | 0 / 0 | 26 / 10 | 0 / 0 | 0 / 0 | 6 / 13 |
| DatBoi | 30 / 26 | 0 / 0 | 40 / 26 | 0 / 0 | 0 / 0 | 4 / 5 |
| davidbowie | 22 / 18 | 0 / 0 | 50 / 37 | 0 / 0 | 0 / 0 | 3 / 2 |
| day9 | 29 / 27 | 0 / 0 | 32 / 22 | 0 / 0 | 5 / 4 | 8 / 8 |
| dbz | 48 / 53 | 0 / 0 | 21 / 9 | 0 / 0 | 5 / 3 | 7 / 7 |
| DCFU | 22 / 17 | 0 / 0 | 40 / 27 | 0 / 0 | 2 / 2 | 7 / 10 |
| de | 66 / 52 | 0 / 0 | 10 / 4 | 3 / 2 | 1 / 1 | 6 / 6 |
| denmark | 57 / 45 | 0 / 1 | 18 / 12 | 1 / 1 | 0 / 0 | 8 / 9 |
| denverbroncos | 55 / 42 | 0 / 0 | 28 / 23 | 0 / 0 | 1 / 0 | 6 / 7 |
| destiny | 32 / 26 | 0 / 1 | 26 / 16 | 0 / 0 | 0 / 0 | 8 / 7 |
| DestinyTheGame | 47 / 42 | 0 / 0 | 24 / 12 | 0 / 0 | 0 / 0 | 3 / 7 |
| detroitlions | 46 / 39 | 0 / 0 | 25 / 15 | 0 / 0 | 0 / 0 | 3 / 4 |
| detroitredwings | 55 / 45 | 0 / 0 | 11 / 5 | 0 / 0 | 1 / 3 | 12 / 13 |
| DevonUK | 23 / 25 | 0 / 0 | 42 / 24 | 0 / 0 | 2 / 2 | 4 / 5 |
| diablo | 31 / 26 | 0 / 0 | 34 / 25 | 0 / 0 | 0 / 0 | 5 / 5 |
| DiamondClub | 12 / 14 | 0 / 0 | 54 / 38 | 0 / 0 | 0 / 0 | 1 / 2 |
| dmt | 19 / 18 | 0 / 0 | 46 / 28 | 0 / 0 | 0 / 0 | 3 / 0 |
| dofus | 16 / 13 | 0 / 0 | 49 / 37 | 0 / 0 | 0 / 0 | 3 / 2 |
| Dominican | 33 / 29 | 0 / 0 | 28 / 16 | 0 / 0 | 6 / 5 | 5 / 6 |
| donaldglover | 47 / 38 | 0 / 0 | 22 / 12 | 2 / 0 | 0 / 2 | 5 / 6 |
| Dorset | 21 / 18 | 0 / 0 | 42 / 28 | 0 / 0 | 0 / 0 | 7 / 8 |
| dota2 | 64 / 50 | 0 / 1 | 13 / 10 | 2 / 2 | 1 / 1 | 8 / 9 |
| dragonquest | 40 / 29 | 0 / 0 | 29 / 21 | 0 / 0 | 4 / 4 | 5 / 6 |
| drawhelix | 27 / 22 | 0 / 0 | 37 / 27 | 0 / 1 | 3 / 3 | 6 / 7 |
| drugs | 34 / 31 | 0 / 0 | 27 / 16 | 2 / 2 | 1 / 0 | 8 / 10 |
| drumcorps | 34 / 31 | 0 / 0 | 33 / 22 | 0 / 1 | 0 / 0 | 6 / 5 |
| duckgame | 37 / 32 | 0 / 0 | 32 / 23 | 1 / 0 | 1 / 1 | 4 / 4 |
| ducks | 16 / 13 | 0 / 0 | 50 / 37 | 3 / 1 | 4 / 6 | 2 / 2 |
| Dustforce | 30 / 24 | 0 / 0 | 29 / 16 | 0 / 0 | 0 / 0 | 3 / 4 |
| dwarffortress | 52 / 36 | 0 / 0 | 21 / 15 | 2 / 2 | 0 / 1 | 9 / 9 |
| eagles | 51 / 38 | 0 / 0 | 16 / 10 | 0 / 0 | 0 / 2 | 11 / 7 |
| earthbound | 46 / 39 | 0 / 0 | 24 / 16 | 0 / 0 | 0 / 0 | 10 / 9 |
| edboxes | 41 / 34 | 0 / 0 | 27 / 20 | 0 / 0 | 2 / 0 | 4 / 2 |
| eder | 15 / 11 | 0 / 0 | 41 / 33 | 2 / 0 | 5 / 5 | 8 / 6 |
| edmontonoilers | 43 / 39 | 0 / 0 | 22 / 12 | 4 / 3 | 0 / 0 | 10 / 8 |
| eesti | 39 / 33 | 0 / 0 | 23 / 15 | 0 / 1 | 0 / 0 | 10 / 10 |
| egypt | 31 / 23 | 0 / 0 | 36 / 24 | 0 / 0 | 0 / 0 | 9 / 9 |
| ElderScrolls | 21 / 16 | 0 / 0 | 48 / 35 | 1 / 0 | 0 / 1 | 6 / 8 |
| elitedangerous | 41 / 31 | 0 / 0 | 13 / 8 | 0 / 0 | 1 / 1 | 4 / 4 |
| ElSalvador | 25 / 24 | 0 / 0 | 41 / 28 | 1 / 0 | 0 / 0 | 4 / 5 |
| empiredidnothingwrong | 63 / 43 | 0 / 0 | 16 / 14 | 2 / 0 | 2 / 3 | 7 / 5 |
| england | 34 / 28 | 0 / 0 | 43 / 30 | 0 / 0 | 1 / 2 | 1 / 0 |
| enterthegungeon | 42 / 38 | 0 / 0 | 28 / 17 | 2 / 1 | 3 / 1 | 9 / 7 |
| epublica | 45 / 33 | 0 / 0 | 26 / 17 | 2 / 2 | 3 / 2 | 5 / 5 |
| EraseThePlace | 48 / 29 | 0 / 0 | 25 / 20 | 1 / 0 | 4 / 0 | 9 / 9 |
| esperanto | 44 / 34 | 0 / 0 | 22 / 14 | 4 / 0 | 0 / 4 | 7 / 5 |
| ethereum | 44 / 36 | 0 / 0 | 23 / 14 | 9 / 4 | 7 / 9 | 8 / 9 |
| ethoslab | 28 / 25 | 0 / 0 | 40 / 31 | 0 / 0 | 0 / 0 | 7 / 6 |
| europe | 61 / 53 | 0 / 0 | 9 / 4 | 3 / 3 | 1 / 3 | 10 / 4 |
| eve | 54 / 38 | 0 / 0 | 9 / 3 | 2 / 2 | 3 / 2 | 9 / 10 |
| evedreddit | 15 / 13 | 0 / 0 | 48 / 37 | 1 / 0 | 0 / 0 | 4 / 3 |
| evex | 42 / 33 | 0 / 0 | 24 / 16 | 0 / 0 | 0 / 0 | 7 / 8 |
| factorio | 49 / 37 | 0 / 0 | 17 / 6 | 0 / 0 | 1 / 1 | 7 / 12 |
| faeria | 42 / 31 | 0 / 0 | 30 / 22 | 1 / 0 | 0 / 1 | 7 / 5 |
| falcons | 46 / 37 | 0 / 0 | 31 / 23 | 3 / 4 | 0 / 1 | 11 / 8 |
| farmcarrots | 44 / 31 | 0 / 0 | 20 / 15 | 0 / 0 | 1 / 1 | 9 / 9 |
| FaroeIslands | 34 / 21 | 0 / 0 | 20 / 17 | 0 / 0 | 0 / 4 | 5 / 2 |
| FederationPlace | 47 / 37 | 0 / 0 | 29 / 20 | 0 / 0 | 1 / 0 | 10 / 7 |
| feedthebeast | 50 / 37 | 0 / 0 | 22 / 16 | 2 / 2 | 1 / 1 | 9 / 8 |
| Fez | 46 / 37 | 0 / 0 | 28 / 22 | 0 / 0 | 0 / 0 | 10 / 9 |
| FinalFantasy | 42 / 37 | 0 / 0 | 24 / 14 | 0 / 0 | 1 / 1 | 7 / 5 |
| finland | 35 / 29 | 0 / 0 | 26 / 16 | 1 / 0 | 0 / 1 | 7 / 8 |
| fireemblem | 59 / 40 | 0 / 0 | 13 / 6 | 1 / 1 | 0 / 0 | 10 / 11 |
| fivenightsatfreddys | 64 / 54 | 0 / 0 | 14 / 9 | 1 / 2 | 0 / 0 | 9 / 8 |
| FlaggyFlag | 22 / 19 | 0 / 0 | 35 / 23 | 0 / 0 | 1 / 1 | 1 / 1 |
| flashtv | 58 / 47 | 0 / 0 | 23 / 17 | 4 / 3 | 1 / 1 | 10 / 7 |
| FlipnoteStudio3D | 7 / 5 | 0 / 0 | 60 / 45 | 0 / 0 | 0 / 0 | 0 / 1 |
| floridagators | 44 / 39 | 0 / 0 | 14 / 7 | 1 / 1 | 0 / 0 | 14 / 10 |
| FloydVsVoid | 55 / 46 | 0 / 1 | 23 / 15 | 0 / 0 | 0 / 0 | 5 / 4 |
| flyers | 54 / 42 | 0 / 0 | 14 / 7 | 4 / 0 | 3 / 6 | 4 / 5 |
| formula1 | 46 / 45 | 0 / 0 | 20 / 6 | 3 / 1 | 2 / 2 | 6 / 4 |
| forsen | 48 / 35 | 0 / 0 | 23 / 14 | 0 / 0 | 1 / 1 | 8 / 11 |
| foxes | 47 / 37 | 0 / 0 | 22 / 14 | 3 / 2 | 2 / 2 | 8 / 7 |
| foxstevenson | 23 / 21 | 0 / 0 | 44 / 19 | 1 / 1 | 0 / 0 | 6 / 5 |
| france | 47 / 39 | 0 / 0 | 8 / 4 | 5 / 3 | 3 / 3 | 9 / 8 |
| frankocean | 63 / 46 | 0 / 0 | 17 / 12 | 2 / 1 | 1 / 3 | 9 / 7 |
| frc | 43 / 39 | 0 / 0 | 28 / 15 | 0 / 0 | 0 / 2 | 6 / 10 |
| freedomplanet | 27 / 21 | 0 / 0 | 37 / 27 | 2 / 1 | 1 / 2 | 7 / 7 |
| ftlgame | 40 / 36 | 0 / 0 | 22 / 14 | 0 / 0 | 2 / 1 | 10 / 8 |
| fullcommunism | 48 / 39 | 0 / 0 | 18 / 15 | 0 / 0 | 3 / 2 | 8 / 7 |
| funhaus | 52 / 43 | 0 / 1 | 12 / 11 | 1 / 0 | 0 / 1 | 5 / 5 |
| furry | 52 / 40 | 0 / 0 | 14 / 10 | 0 / 0 | 0 / 1 | 9 / 8 |
| furry_irl | 49 / 40 | 0 / 0 | 27 / 16 | 5 / 5 | 3 / 2 | 10 / 14 |
| futanari | 19 / 17 | 0 / 1 | 48 / 36 | 1 / 1 | 1 / 1 | 1 / 1 |
| futurama | 42 / 36 | 0 / 0 | 25 / 18 | 2 / 2 | 0 / 0 | 7 / 6 |
| fxKorea | 33 / 24 | 0 / 0 | 26 / 17 | 2 / 1 | 0 / 0 | 2 / 2 |
| GabrielDropout | 35 / 28 | 0 / 0 | 23 / 12 | 0 / 0 | 1 / 0 | 9 / 9 |
| gameattack | 34 / 29 | 0 / 0 | 41 / 31 | 0 / 0 | 1 / 1 | 7 / 7 |
| gameboy | 16 / 18 | 0 / 0 | 50 / 39 | 0 / 0 | 0 / 0 | 6 / 4 |
| gameofthrones | 51 / 45 | 0 / 0 | 25 / 16 | 1 / 1 | 1 / 1 | 11 / 9 |
| gamindustri | 51 / 39 | 0 / 0 | 29 / 18 | 0 / 0 | 0 / 1 | 5 / 5 |
| gatech | 59 / 43 | 0 / 0 | 14 / 8 | 0 / 0 | 1 / 0 | 7 / 9 |
| genderfluid | 17 / 15 | 0 / 0 | 50 / 37 | 0 / 0 | 0 / 0 | 2 / 2 |
| geometrydash | 30 / 29 | 0 / 0 | 37 / 25 | 2 / 2 | 2 / 2 | 8 / 7 |
| germany | 43 / 36 | 0 / 0 | 31 / 20 | 1 / 1 | 7 / 5 | 8 / 7 |
| ghibli | 27 / 23 | 0 / 0 | 41 / 29 | 1 / 0 | 2 / 1 | 4 / 4 |
| giantbomb | 57 / 46 | 0 / 0 | 17 / 12 | 1 / 1 | 0 / 0 | 7 / 6 |
| giivasunner | 47 / 41 | 0 / 0 | 16 / 9 | 2 / 1 | 2 / 2 | 12 / 12 |
| glasgow | 23 / 20 | 0 / 0 | 48 / 36 | 0 / 0 | 0 / 0 | 3 / 3 |
| globaloffensive | 46 / 46 | 0 / 0 | 17 / 12 | 2 / 1 | 1 / 0 | 7 / 6 |
| Goodboye | 51 / 36 | 0 / 0 | 22 / 16 | 0 / 0 | 1 / 0 | 12 / 12 |
| gorillaz | 59 / 34 | 0 / 0 | 26 / 18 | 0 / 0 | 1 / 1 | 7 / 10 |
| GranColombia | 36 / 23 | 0 / 0 | 38 / 26 | 1 / 0 | 0 / 1 | 5 / 7 |
| gratefuldead | 41 / 30 | 0 / 0 | 31 / 23 | 1 / 1 | 1 / 1 | 9 / 7 |
| gravityfalls | 40 / 37 | 1 / 1 | 25 / 16 | 0 / 0 | 3 / 1 | 4 / 3 |
| greece | 52 / 40 | 0 / 1 | 18 / 12 | 1 / 1 | 0 / 0 | 9 / 9 |
| greenbaypackers | 57 / 48 | 0 / 0 | 21 / 10 | 0 / 0 | 0 / 0 | 4 / 8 |
| GreenCorner | 32 / 29 | 0 / 0 | 31 / 25 | 2 / 0 | 4 / 3 | 5 / 3 |
| GreenEmpire | 7 / 8 | 0 / 0 | 44 / 29 | 0 / 0 | 0 / 0 | 3 / 1 |
| greenland | 5 / 5 | 0 / 0 | 45 / 31 | 0 / 0 | 0 / 0 | 0 / 0 |
| greenlattice | 60 / 46 | 0 / 0 | 16 / 13 | 0 / 0 | 0 / 0 | 4 / 3 |
| greyblob | 33 / 27 | 0 / 0 | 16 / 10 | 2 / 0 | 7 / 4 | 4 / 4 |
| GrowTheTree | 25 / 25 | 0 / 0 | 33 / 20 | 0 / 0 | 0 / 1 | 12 / 7 |
| GuardiansOfDatBoi | 32 / 28 | 0 / 0 | 29 / 16 | 1 / 1 | 0 / 0 | 2 / 2 |
| guatemala | 18 / 14 | 0 / 0 | 43 / 20 | 0 / 0 | 4 / 3 | 5 / 4 |
| GuildWars2 | 33 / 26 | 0 / 0 | 37 / 27 | 4 / 3 | 1 / 0 | 5 / 4 |
| h3h3productions | 42 / 38 | 0 / 0 | 27 / 20 | 1 / 1 | 1 / 0 | 8 / 6 |
| habs | 53 / 49 | 0 / 0 | 15 / 5 | 1 / 1 | 2 / 1 | 5 / 5 |
| halo | 54 / 44 | 1 / 0 | 12 / 7 | 0 / 0 | 1 / 1 | 10 / 13 |
| harrypotter | 52 / 47 | 0 / 0 | 20 / 13 | 0 / 0 | 1 / 0 | 11 / 8 |
| haskell | 38 / 26 | 0 / 0 | 20 / 9 | 0 / 0 | 0 / 0 | 3 / 3 |
| hatsune | 39 / 34 | 0 / 0 | 34 / 24 | 1 / 0 | 1 / 0 | 4 / 4 |
| hawks | 50 / 43 | 0 / 0 | 20 / 11 | 2 / 2 | 2 / 2 | 6 / 6 |
| hearthstone | 45 / 37 | 1 / 1 | 27 / 19 | 3 / 0 | 4 / 5 | 10 / 9 |
| hellointernet | 45 / 37 | 0 / 0 | 21 / 13 | 0 / 0 | 1 / 0 | 8 / 7 |
| hentai | 42 / 34 | 0 / 1 | 24 / 14 | 0 / 0 | 0 / 0 | 8 / 8 |
| heroesofthestorm | 53 / 38 | 0 / 0 | 9 / 5 | 1 / 0 | 1 / 2 | 16 / 15 |
| heyyea | 33 / 26 | 0 / 0 | 40 / 30 | 0 / 0 | 0 / 0 | 7 / 5 |
| homelab | 36 / 28 | 0 / 0 | 36 / 27 | 3 / 4 | 2 / 2 | 2 / 1 |
| HomestarRunner | 38 / 36 | 0 / 0 | 30 / 16 | 0 / 0 | 0 / 0 | 7 / 6 |
| homestuck | 51 / 33 | 0 / 0 | 20 / 15 | 1 / 0 | 2 / 1 | 10 / 12 |
| Homura | 12 / 8 | 0 / 0 | 41 / 28 | 0 / 0 | 0 / 0 | 4 / 5 |
| Honduras | 22 / 20 | 0 / 0 | 44 / 31 | 1 / 0 | 0 / 1 | 4 / 5 |
| hongkong | 31 / 27 | 0 / 0 | 32 / 23 | 0 / 0 | 0 / 0 | 7 / 6 |
| hoodr | 26 / 20 | 0 / 0 | 39 / 29 | 0 / 0 | 0 / 0 | 7 / 6 |
| hsv | 39 / 32 | 0 / 0 | 26 / 13 | 0 / 0 | 0 / 0 | 7 / 6 |
| httyd | 36 / 31 | 0 / 0 | 33 / 22 | 1 / 0 | 0 / 0 | 2 / 3 |
| hungary | 29 / 23 | 0 / 0 | 27 / 11 | 0 / 0 | 1 / 2 | 3 / 2 |
| hunterxhunter | 34 / 31 | 0 / 0 | 32 / 19 | 1 / 1 | 0 / 0 | 5 / 7 |
| hyperlightdrifter | 37 / 30 | 0 / 0 | 30 / 20 | 0 / 0 | 0 / 0 | 7 / 5 |
| iastate | 40 / 35 | 0 / 0 | 31 / 18 | 1 / 0 | 0 / 0 | 9 / 9 |
| ibo | 20 / 20 | 0 / 0 | 46 / 34 | 1 / 1 | 2 / 0 | 3 / 3 |
| ice_poseidon | 47 / 34 | 0 / 0 | 18 / 11 | 2 / 2 | 8 / 9 | 7 / 7 |
| iceland | 30 / 26 | 0 / 0 | 32 / 19 | 0 / 0 | 0 / 0 | 6 / 6 |
| ik_ihe | 16 / 16 | 0 / 0 | 48 / 35 | 0 / 0 | 2 / 2 | 5 / 3 |
| india | 52 / 43 | 0 / 0 | 15 / 8 | 3 / 1 | 0 / 1 | 8 / 9 |
| indieheads | 50 / 42 | 0 / 0 | 15 / 9 | 3 / 3 | 0 / 0 | 13 / 11 |
| indonesia | 52 / 45 | 0 / 0 | 12 / 5 | 1 / 1 | 2 / 2 | 11 / 9 |
| ireland | 54 / 42 | 0 / 0 | 11 / 4 | 1 / 1 | 0 / 2 | 6 / 9 |
| israel | 49 / 42 | 0 / 0 | 15 / 7 | 0 / 0 | 2 / 2 | 10 / 9 |
| italy | 52 / 45 | 0 / 1 | 14 / 7 | 1 / 1 | 0 / 0 | 14 / 12 |
| Jamaica | 31 / 31 | 0 / 0 | 37 / 26 | 1 / 1 | 0 / 0 | 6 / 6 |
| japan | 48 / 40 | 0 / 0 | 27 / 16 | 0 / 0 | 1 / 1 | 7 / 7 |
| jerma985 | 43 / 35 | 0 / 1 | 27 / 18 | 0 / 0 | 0 / 0 | 2 / 2 |
| k_on | 29 / 25 | 0 / 0 | 42 / 29 | 0 / 0 | 0 / 0 | 2 / 2 |
| kamenrider | 38 / 37 | 0 / 0 | 27 / 17 | 1 / 1 | 0 / 0 | 10 / 8 |
| kanye | 53 / 38 | 0 / 0 | 17 / 12 | 0 / 1 | 1 / 1 | 2 / 2 |
| katawashoujo | 28 / 26 | 0 / 2 | 35 / 24 | 2 / 2 | 0 / 0 | 9 / 7 |
| kcroyals | 33 / 27 | 0 / 0 | 34 / 18 | 1 / 1 | 0 / 0 | 8 / 7 |
| kerbalspaceprogram | 42 / 39 | 0 / 0 | 31 / 21 | 3 / 3 | 0 / 0 | 6 / 3 |
| kilian | 35 / 28 | 0 / 0 | 29 / 21 | 6 / 0 | 0 / 6 | 7 / 5 |
| kindafunny | 23 / 22 | 0 / 0 | 49 / 35 | 1 / 0 | 1 / 1 | 0 / 0 |
| kingdomhearts | 54 / 42 | 0 / 0 | 25 / 19 | 0 / 0 | 0 / 0 | 5 / 4 |
| kirby | 35 / 34 | 0 / 0 | 30 / 19 | 2 / 0 | 1 / 2 | 12 / 10 |
| konosuba | 40 / 34 | 0 / 0 | 26 / 14 | 0 / 0 | 0 / 1 | 1 / 3 |
| korea | 53 / 43 | 0 / 0 | 22 / 15 | 1 / 0 | 0 / 1 | 5 / 6 |
| kpop | 39 / 33 | 0 / 0 | 35 / 25 | 1 / 1 | 0 / 0 | 4 / 4 |
| KState | 35 / 29 | 0 / 0 | 27 / 18 | 0 / 0 | 2 / 1 | 8 / 8 |
| kurdistan | 35 / 29 | 0 / 0 | 25 / 17 | 1 / 0 | 0 / 1 | 9 / 9 |
| kuwait | 30 / 28 | 0 / 0 | 44 / 30 | 1 / 1 | 1 / 0 | 5 / 8 |
| lakers | 55 / 54 | 0 / 1 | 15 / 10 | 4 / 4 | 1 / 5 | 4 / 4 |
| landry | 14 / 10 | 0 / 0 | 37 / 24 | 1 / 1 | 1 / 1 | 3 / 4 |
| latin | 36 / 29 | 0 / 0 | 36 / 26 | 0 / 0 | 1 / 1 | 3 / 2 |
| latvia | 36 / 32 | 0 / 0 | 31 / 20 | 0 / 0 | 1 / 1 | 5 / 4 |
| leafs | 42 / 35 | 0 / 0 | 15 / 10 | 2 / 2 | 1 / 0 | 14 / 13 |
| leagueoflegends | 49 / 45 | 0 / 1 | 23 / 13 | 3 / 3 | 0 / 0 | 5 / 9 |
| lebanon | 44 / 34 | 0 / 0 | 22 / 13 | 1 / 0 | 0 / 1 | 5 / 5 |
| lego | 39 / 35 | 0 / 0 | 26 / 16 | 0 / 0 | 7 / 6 | 16 / 13 |
| lexington | 10 / 10 | 0 / 0 | 53 / 38 | 1 / 1 | 1 / 1 | 4 / 4 |
| lifeisstrange | 43 / 33 | 0 / 0 | 23 / 15 | 0 / 0 | 2 / 2 | 7 / 6 |
| linux | 49 / 30 | 0 / 0 | 26 / 20 | 3 / 1 | 4 / 7 | 12 / 11 |
| liquicity | 33 / 26 | 0 / 0 | 20 / 11 | 0 / 0 | 1 / 0 | 3 / 3 |
| lithuania | 37 / 29 | 0 / 0 | 33 / 24 | 0 / 0 | 0 / 0 | 5 / 5 |
| littlebusters | 7 / 6 | 0 / 0 | 59 / 44 | 0 / 0 | 0 / 0 | 1 / 2 |
| littlewitchacademia | 42 / 35 | 0 / 0 | 27 / 16 | 0 / 0 | 3 / 1 | 6 / 10 |
| livecounting | 19 / 17 | 0 / 0 | 49 / 37 | 1 / 2 | 4 / 1 | 2 / 3 |
| liverpoolfc | 42 / 35 | 0 / 0 | 22 / 15 | 0 / 0 | 0 / 0 | 9 / 6 |
| lofihiphop | 21 / 16 | 0 / 0 | 48 / 35 | 0 / 0 | 0 / 0 | 5 / 5 |
| loliconsunite | 50 / 36 | 0 / 0 | 27 / 21 | 0 / 0 | 0 / 0 | 3 / 3 |
| loltyler1 | 44 / 37 | 0 / 0 | 18 / 11 | 1 / 0 | 3 / 2 | 7 / 6 |
| lost | 37 / 31 | 0 / 0 | 25 / 18 | 1 / 1 | 0 / 0 | 8 / 6 |
| lovelive | 35 / 33 | 0 / 0 | 29 / 20 | 0 / 0 | 2 / 0 | 9 / 7 |
| lsu | 40 / 34 | 0 / 0 | 27 / 18 | 0 / 0 | 0 / 0 | 6 / 6 |
| luciomains | 33 / 27 | 0 / 0 | 30 / 21 | 1 / 1 | 0 / 0 | 12 / 11 |
| Lugarix | 3 / 3 | 0 / 0 | 63 / 49 | 0 / 0 | 0 / 0 | 1 / 1 |
| luxembourg | 31 / 23 | 0 / 0 | 43 / 33 | 0 / 0 | 0 / 0 | 3 / 2 |
| Madeon | 15 / 13 | 0 / 1 | 51 / 38 | 4 / 4 | 0 / 0 | 2 / 2 |
| madokamagica | 38 / 34 | 0 / 0 | 27 / 15 | 0 / 0 | 0 / 0 | 8 / 10 |
| magictcg | 46 / 38 | 0 / 0 | 15 / 9 | 0 / 0 | 1 / 1 | 6 / 5 |
| malaysia | 46 / 42 | 0 / 0 | 21 / 11 | 0 / 0 | 1 / 1 | 10 / 8 |
| malta | 30 / 26 | 0 / 0 | 32 / 20 | 0 / 0 | 1 / 2 | 8 / 6 |
| mamamoo | 11 / 9 | 0 / 0 | 56 / 42 | 0 / 0 | 0 / 0 | 2 / 2 |
| ManningPlace | 28 / 24 | 0 / 0 | 27 / 15 | 0 / 0 | 5 / 5 | 10 / 11 |
| Mario | 14 / 11 | 0 / 0 | 53 / 39 | 0 / 0 | 1 / 0 | 3 / 3 |
| mariokart | 8 / 9 | 0 / 0 | 57 / 41 | 1 / 0 | 6 / 7 | 1 / 2 |
| marvel | 21 / 21 | 0 / 0 | 43 / 29 | 1 / 0 | 6 / 5 | 2 / 3 |
| maryland | 43 / 42 | 1 / 1 | 18 / 6 | 3 / 0 | 3 / 2 | 7 / 7 |
| masseffect | 43 / 38 | 0 / 1 | 20 / 13 | 0 / 0 | 2 / 0 | 5 / 4 |
| math | 33 / 28 | 0 / 0 | 38 / 27 | 0 / 0 | 2 / 2 | 3 / 3 |
| mcgill | 28 / 27 | 0 / 0 | 39 / 26 | 0 / 0 | 0 / 0 | 7 / 8 |
| mcgillrobotics | 5 / 4 | 0 / 0 | 60 / 45 | 0 / 0 | 0 / 0 | 1 / 2 |
| mechanicalkeyboards | 42 / 31 | 0 / 0 | 27 / 20 | 1 / 1 | 0 / 0 | 4 / 6 |
| megaman | 47 / 37 | 0 / 0 | 19 / 11 | 0 / 0 | 0 / 0 | 13 / 14 |
| metalcore | 48 / 38 | 0 / 0 | 26 / 20 | 3 / 3 | 0 / 0 | 1 / 1 |
| metalgearsolid | 46 / 42 | 0 / 0 | 26 / 11 | 1 / 2 | 1 / 0 | 2 / 10 |
| metroid | 48 / 44 | 0 / 0 | 21 / 12 | 0 / 1 | 3 / 0 | 8 / 7 |
| mexico | 52 / 39 | 0 / 0 | 12 / 6 | 1 / 1 | 1 / 0 | 8 / 10 |
| miamidolphins | 47 / 44 | 0 / 0 | 20 / 11 | 0 / 0 | 1 / 1 | 4 / 3 |
| MiamiHurricanes | 35 / 31 | 0 / 0 | 34 / 22 | 0 / 0 | 1 / 0 | 5 / 6 |
| mindcrack | 50 / 39 | 0 / 0 | 17 / 12 | 1 / 1 | 1 / 1 | 7 / 7 |
| minecraft | 45 / 35 | 0 / 0 | 18 / 11 | 0 / 0 | 6 / 5 | 11 / 11 |
| minnesotavikings | 53 / 45 | 0 / 0 | 14 / 8 | 2 / 2 | 1 / 0 | 7 / 6 |
| miraculousladybug | 27 / 24 | 0 / 0 | 40 / 30 | 1 / 0 | 0 / 1 | 8 / 7 |
| mit | 27 / 26 | 0 / 0 | 41 / 27 | 0 / 0 | 0 / 0 | 4 / 3 |
| mizzou | 26 / 22 | 0 / 0 | 39 / 27 | 0 / 0 | 1 / 1 | 6 / 5 |
| mls | 53 / 45 | 0 / 0 | 16 / 8 | 2 / 3 | 0 / 0 | 6 / 6 |
| MMA | 40 / 44 | 0 / 0 | 27 / 14 | 3 / 2 | 0 / 0 | 6 / 4 |
| monalisaclan | 53 / 40 | 0 / 0 | 24 / 18 | 0 / 0 | 2 / 0 | 5 / 6 |
| monero | 41 / 34 | 0 / 0 | 21 / 12 | 0 / 0 | 0 / 0 | 12 / 10 |
| MonkeyIsland | 29 / 22 | 0 / 0 | 45 / 28 | 1 / 1 | 0 / 0 | 2 / 3 |
| monstercat | 43 / 33 | 0 / 0 | 31 / 21 | 1 / 1 | 1 / 1 | 7 / 6 |
| monsterhunter | 42 / 33 | 0 / 1 | 22 / 14 | 0 / 1 | 1 / 1 | 9 / 9 |
| montenegro | 20 / 17 | 0 / 0 | 43 / 30 | 0 / 0 | 0 / 0 | 6 / 4 |
| Moondye7 | 32 / 28 | 0 / 0 | 28 / 21 | 3 / 0 | 3 / 4 | 8 / 6 |
| mordhau | 24 / 19 | 0 / 0 | 36 / 25 | 0 / 0 | 0 / 0 | 9 / 10 |
| morrowind | 51 / 39 | 0 / 0 | 28 / 18 | 0 / 0 | 0 / 0 | 9 / 11 |
| msu | 40 / 35 | 0 / 0 | 28 / 15 | 0 / 0 | 0 / 0 | 6 / 7 |
| muse | 47 / 37 | 0 / 0 | 20 / 12 | 0 / 0 | 1 / 0 | 6 / 8 |
| mylittlepony | 64 / 48 | 0 / 0 | 14 / 9 | 1 / 1 | 0 / 0 | 6 / 7 |
| mysterydungeon | 29 / 23 | 0 / 0 | 30 / 15 | 0 / 0 | 0 / 0 | 4 / 3 |
| n64 | 12 / 14 | 0 / 0 | 54 / 39 | 0 / 0 | 1 / 0 | 1 / 0 |
| naruto | 42 / 36 | 0 / 0 | 13 / 6 | 0 / 0 | 0 / 0 | 7 / 6 |
| nascar | 48 / 40 | 0 / 0 | 28 / 19 | 1 / 1 | 0 / 0 | 12 / 10 |
| natsume | 16 / 12 | 0 / 0 | 43 / 31 | 0 / 0 | 1 / 0 | 3 / 5 |
| nbaspurs | 56 / 45 | 0 / 0 | 23 / 14 | 4 / 4 | 2 / 2 | 5 / 3 |
| necrodancer | 36 / 32 | 0 / 0 | 31 / 21 | 1 / 0 | 0 / 0 | 10 / 5 |
| neopets | 55 / 44 | 0 / 0 | 21 / 14 | 1 / 0 | 3 / 4 | 9 / 9 |
| nerf | 45 / 32 | 0 / 0 | 36 / 27 | 0 / 0 | 0 / 0 | 1 / 1 |
| neu | 39 / 30 | 0 / 0 | 16 / 11 | 0 / 0 | 0 / 0 | 18 / 16 |
| neutralmilkhotel | 31 / 26 | 0 / 0 | 40 / 25 | 1 / 1 | 0 / 0 | 5 / 6 |
| NewMexico | 43 / 40 | 0 / 0 | 26 / 14 | 0 / 0 | 0 / 0 | 6 / 6 |
| newzealand | 53 / 41 | 0 / 1 | 17 / 10 | 1 / 0 | 2 / 2 | 12 / 8 |
| NieR | 50 / 39 | 0 / 0 | 26 / 20 | 2 / 2 | 0 / 0 | 6 / 5 |
| nightinthewoods | 39 / 28 | 0 / 0 | 35 / 26 | 1 / 0 | 0 / 1 | 5 / 5 |
| nin | 51 / 37 | 0 / 0 | 16 / 7 | 0 / 0 | 2 / 2 | 7 / 7 |
| nintendo | 41 / 41 | 0 / 0 | 35 / 23 | 3 / 3 | 5 / 1 | 8 / 7 |
| nlsscirclejerk | 34 / 29 | 0 / 0 | 37 / 24 | 0 / 1 | 1 / 0 | 4 / 4 |
| nonbinary | 3 / 2 | 0 / 0 | 62 / 47 | 1 / 0 | 0 / 1 | 0 / 1 |
| norge | 36 / 30 | 0 / 0 | 23 / 9 | 0 / 0 | 3 / 0 | 8 / 9 |
| Northwestern | 35 / 29 | 0 / 0 | 35 / 26 | 0 / 0 | 4 / 4 | 5 / 4 |
| norway | 38 / 34 | 0 / 0 | 30 / 23 | 1 / 0 | 3 / 1 | 6 / 4 |
| notredame | 36 / 30 | 0 / 0 | 28 / 19 | 0 / 0 | 0 / 0 | 9 / 9 |
| NovaScotia | 4 / 5 | 0 / 0 | 60 / 46 | 0 / 0 | 0 / 0 | 3 / 2 |
| npr | 40 / 31 | 0 / 0 | 28 / 21 | 0 / 0 | 0 / 0 | 6 / 5 |
| nuclearthrone | 40 / 35 | 0 / 0 | 22 / 14 | 0 / 0 | 2 / 1 | 7 / 5 |
| nVade | 42 / 33 | 0 / 0 | 22 / 16 | 0 / 0 | 1 / 0 | 11 / 9 |
| nyjets | 56 / 49 | 0 / 0 | 17 / 11 | 0 / 0 | 0 / 0 | 3 / 1 |
| nyu | 24 / 22 | 0 / 0 | 44 / 33 | 1 / 0 | 5 / 4 | 3 / 1 |
| ockytop | 48 / 37 | 0 / 0 | 14 / 7 | 1 / 1 | 2 / 3 | 11 / 11 |
| ohio | 41 / 38 | 0 / 0 | 25 / 14 | 3 / 1 | 1 / 3 | 9 / 6 |
| Okami | 34 / 27 | 0 / 0 | 32 / 22 | 1 / 1 | 1 / 0 | 6 / 6 |
| OKState | 22 / 17 | 0 / 0 | 47 / 33 | 0 / 0 | 0 / 0 | 4 / 4 |
| oltp | 4 / 2 | 0 / 0 | 49 / 33 | 0 / 0 | 0 / 0 | 1 / 1 |
| oman | 19 / 17 | 0 / 0 | 45 / 34 | 0 / 0 | 0 / 0 | 5 / 3 |
| OnePiece | 66 / 51 | 0 / 1 | 12 / 7 | 1 / 1 | 1 / 1 | 6 / 8 |
| oneplus | 26 / 25 | 0 / 0 | 47 / 34 | 2 / 2 | 0 / 0 | 5 / 4 |
| onepunchman | 34 / 30 | 0 / 0 | 21 / 13 | 0 / 2 | 6 / 5 | 9 / 9 |
| oneshot | 29 / 25 | 1 / 0 | 30 / 20 | 2 / 2 | 3 / 0 | 10 / 12 |
| OneTrueEmilia | 26 / 19 | 0 / 0 | 49 / 38 | 1 / 1 | 0 / 0 | 3 / 3 |
| ontario | 11 / 11 | 0 / 0 | 59 / 46 | 1 / 1 | 0 / 0 | 2 / 1 |
| opticgaming | 52 / 43 | 0 / 0 | 18 / 12 | 1 / 0 | 2 / 3 | 6 / 5 |
| orderofthebluecorner | 30 / 23 | 0 / 0 | 29 / 21 | 1 / 2 | 2 / 1 | 13 / 8 |
| OrderOfTheKoi | 21 / 16 | 0 / 0 | 50 / 37 | 3 / 2 | 0 / 1 | 3 / 4 |
| osu | 55 / 43 | 0 / 0 | 20 / 12 | 0 / 0 | 1 / 1 | 9 / 10 |
| osugame | 67 / 40 | 0 / 0 | 10 / 6 | 1 / 0 | 0 / 1 | 7 / 12 |
| overwatch | 67 / 58 | 0 / 0 | 16 / 12 | 2 / 2 | 3 / 1 | 6 / 13 |
| pakistan | 52 / 52 | 0 / 0 | 18 / 8 | 1 / 0 | 2 / 1 | 7 / 7 |
| paladins | 63 / 50 | 0 / 0 | 22 / 15 | 6 / 2 | 0 / 1 | 6 / 13 |
| palestine | 33 / 27 | 0 / 0 | 28 / 21 | 1 / 0 | 2 / 2 | 9 / 8 |
| pansexual | 24 / 21 | 0 / 0 | 46 / 33 | 0 / 0 | 0 / 0 | 4 / 4 |
| parabola | 18 / 14 | 0 / 0 | 34 / 20 | 2 / 2 | 0 / 0 | 2 / 3 |
| paragon | 37 / 32 | 0 / 0 | 38 / 24 | 0 / 0 | 0 / 0 | 7 / 6 |
| parahumans | 54 / 41 | 0 / 0 | 21 / 13 | 1 / 1 | 2 / 1 | 7 / 5 |
| paranatural | 27 / 22 | 0 / 0 | 42 / 32 | 0 / 0 | 1 / 1 | 6 / 4 |
| parrots | 36 / 31 | 0 / 0 | 35 / 22 | 2 / 2 | 1 / 0 | 7 / 6 |
| partyparrot | 55 / 44 | 0 / 0 | 19 / 14 | 1 / 1 | 1 / 1 | 10 / 9 |
| pathofexile | 50 / 54 | 0 / 0 | 16 / 9 | 0 / 0 | 0 / 1 | 9 / 6 |
| patriots | 55 / 45 | 0 / 0 | 15 / 9 | 0 / 0 | 2 / 2 | 10 / 10 |
| paydaytheheist | 33 / 30 | 0 / 0 | 30 / 19 | 4 / 4 | 0 / 0 | 6 / 5 |
| pcmasterrace | 56 / 49 | 0 / 0 | 16 / 15 | 4 / 1 | 0 / 1 | 8 / 12 |
| pebble | 41 / 35 | 0 / 0 | 29 / 18 | 1 / 0 | 0 / 1 | 4 / 2 |
| penguins | 40 / 34 | 0 / 0 | 38 / 28 | 0 / 0 | 1 / 1 | 2 / 2 |
| pepe | 30 / 29 | 0 / 0 | 36 / 24 | 0 / 0 | 0 / 0 | 7 / 7 |
| Peru | 43 / 36 | 0 / 0 | 26 / 16 | 0 / 0 | 1 / 0 | 7 / 9 |
| peterdraws | 12 / 12 | 0 / 0 | 55 / 42 | 0 / 0 | 0 / 0 | 5 / 5 |
| pgang | 3 / 3 | 0 / 0 | 62 / 47 | 2 / 2 | 0 / 0 | 1 / 1 |
| philippines | 55 / 44 | 0 / 0 | 10 / 6 | 1 / 1 | 2 / 0 | 9 / 10 |
| phish | 43 / 38 | 0 / 0 | 24 / 17 | 0 / 0 | 0 / 0 | 10 / 8 |
| physical_removal | 43 / 37 | 0 / 0 | 21 / 14 | 3 / 4 | 0 / 0 | 10 / 9 |
| picturegame | 5 / 5 | 0 / 0 | 63 / 48 | 3 / 2 | 1 / 1 | 0 / 1 |
| Pigifs | 10 / 9 | 0 / 0 | 54 / 43 | 5 / 1 | 1 / 2 | 7 / 5 |
| PinkUnion | 34 / 28 | 0 / 0 | 32 / 21 | 1 / 1 | 0 / 0 | 11 / 10 |
| PinkVomitMonster | 30 / 22 | 0 / 0 | 29 / 21 | 0 / 0 | 1 / 0 | 14 / 15 |
| pitt | 42 / 38 | 0 / 0 | 17 / 7 | 2 / 0 | 0 / 3 | 12 / 11 |
| placecanada | 41 / 35 | 0 / 0 | 23 / 16 | 0 / 0 | 1 / 1 | 10 / 7 |
| placeDE | 48 / 38 | 0 / 0 | 18 / 12 | 0 / 0 | 0 / 0 | 12 / 12 |
| placehearts | 38 / 30 | 0 / 0 | 25 / 24 | 0 / 0 | 2 / 2 | 7 / 4 |
| placehfarts | 10 / 9 | 0 / 0 | 56 / 41 | 0 / 0 | 1 / 1 | 3 / 3 |
| PlaceNL | 54 / 46 | 1 / 2 | 22 / 13 | 1 / 0 | 0 / 1 | 6 / 3 |
| placeportalpattern | 38 / 28 | 0 / 0 | 32 / 22 | 2 / 0 | 0 / 1 | 9 / 8 |
| placesnek | 41 / 29 | 0 / 0 | 29 / 22 | 0 / 0 | 0 / 0 | 5 / 5 |
| placestart | 42 / 36 | 0 / 0 | 24 / 14 | 0 / 0 | 1 / 0 | 6 / 9 |
| placetardis | 43 / 35 | 0 / 0 | 30 / 17 | 0 / 0 | 0 / 0 | 7 / 8 |
| planetside | 48 / 41 | 0 / 0 | 29 / 21 | 2 / 2 | 1 / 1 | 2 / 2 |
| pokemon | 35 / 37 | 0 / 0 | 27 / 19 | 5 / 0 | 0 / 0 | 10 / 9 |
| PokemonSage | 1 / 1 | 0 / 0 | 64 / 50 | 0 / 0 | 0 / 0 | 2 / 0 |
| poland | 39 / 33 | 0 / 0 | 25 / 16 | 0 / 0 | 2 / 1 | 4 / 5 |
| polandball | 26 / 22 | 0 / 1 | 50 / 40 | 1 / 0 | 5 / 3 | 0 / 0 |
| polska | 42 / 40 | 1 / 0 | 16 / 9 | 0 / 0 | 2 / 0 | 14 / 14 |
| polyamory | 10 / 10 | 0 / 0 | 58 / 44 | 1 / 1 | 1 / 0 | 0 / 0 |
| popheads | 35 / 32 | 0 / 0 | 47 / 30 | 1 / 1 | 2 / 1 | 6 / 5 |
| portal | 46 / 32 | 0 / 0 | 30 / 15 | 2 / 0 | 3 / 4 | 4 / 4 |
| porterrobinson | 49 / 36 | 0 / 0 | 34 / 26 | 4 / 2 | 0 / 0 | 3 / 5 |
| portugal | 76 / 59 | 1 / 2 | 19 / 13 | 0 / 0 | 1 / 0 | 12 / 10 |
| PORTUGALCARALHO | 29 / 27 | 0 / 0 | 36 / 24 | 0 / 0 | 8 / 7 | 6 / 6 |
| predators | 50 / 38 | 0 / 0 | 20 / 12 | 1 / 1 | 0 / 0 | 11 / 11 |
| prequelmemes | 66 / 45 | 0 / 0 | 13 / 8 | 1 / 1 | 1 / 0 | 7 / 11 |
| Produce101 | 8 / 6 | 0 / 0 | 57 / 43 | 0 / 0 | 1 / 1 | 2 / 3 |
| ProfessorLayton | 29 / 22 | 0 / 0 | 45 / 32 | 0 / 0 | 0 / 0 | 7 / 7 |
| PUBATTLEGROUNDS | 40 / 31 | 0 / 0 | 29 / 19 | 2 / 3 | 0 / 0 | 9 / 7 |
| purdue | 55 / 45 | 0 / 0 | 12 / 4 | 2 / 2 | 0 / 2 | 7 / 7 |
| purplecorner | 41 / 33 | 0 / 0 | 27 / 19 | 0 / 0 | 1 / 0 | 9 / 9 |
| PurplePixels | 45 / 34 | 0 / 0 | 26 / 20 | 0 / 0 | 0 / 0 | 8 / 8 |
| pusheen | 19 / 17 | 0 / 0 | 46 / 33 | 0 / 0 | 1 / 0 | 8 / 8 |
| puzzleanddragons | 46 / 36 | 0 / 0 | 27 / 21 | 1 / 1 | 1 / 1 | 7 / 5 |
| python | 31 / 28 | 0 / 0 | 37 / 17 | 3 / 2 | 6 / 3 | 4 / 3 |
| qotsa | 34 / 27 | 0 / 0 | 34 / 23 | 0 / 0 | 1 / 1 | 7 / 9 |
| quebec | 59 / 45 | 0 / 0 | 16 / 11 | 1 / 1 | 2 / 1 | 8 / 6 |
| quq | 5 / 2 | 0 / 0 | 28 / 18 | 1 / 2 | 0 / 0 | 2 / 2 |
| radiohead | 59 / 44 | 0 / 0 | 13 / 7 | 0 / 0 | 0 / 0 | 9 / 10 |
| Rainbow6 | 48 / 37 | 0 / 0 | 19 / 13 | 3 / 3 | 0 / 0 | 6 / 8 |
| rainbowgrid | 31 / 24 | 0 / 1 | 42 / 28 | 0 / 0 | 0 / 0 | 3 / 3 |
| rangers | 49 / 37 | 0 / 0 | 24 / 16 | 1 / 1 | 0 / 2 | 3 / 8 |
| raocow | 34 / 30 | 0 / 0 | 33 / 22 | 2 / 2 | 2 / 0 | 3 / 3 |
| ravens | 40 / 33 | 0 / 0 | 29 / 17 | 3 / 0 | 1 / 4 | 4 / 4 |
| re_zero | 42 / 33 | 0 / 0 | 31 / 22 | 0 / 0 | 0 / 0 | 4 / 5 |
| ReBoot | 12 / 12 | 0 / 0 | 54 / 38 | 0 / 0 | 1 / 1 | 1 / 2 |
| reddevils | 65 / 52 | 0 / 0 | 14 / 7 | 0 / 0 | 0 / 0 | 7 / 8 |
| redhotchilipeppers | 38 / 35 | 0 / 0 | 34 / 23 | 1 / 1 | 1 / 0 | 3 / 5 |
| Redox | 2 / 1 | 0 / 0 | 62 / 48 | 1 / 1 | 1 / 1 | 1 / 1 |
| redpandas | 33 / 28 | 0 / 0 | 40 / 31 | 0 / 0 | 2 / 1 | 4 / 3 |
| redvsblue | 29 / 26 | 0 / 0 | 35 / 23 | 0 / 0 | 2 / 0 | 6 / 6 |
| RelientK | 31 / 29 | 0 / 0 | 36 / 22 | 3 / 0 | 0 / 3 | 10 / 8 |
| rhythmheaven | 37 / 28 | 1 / 0 | 33 / 23 | 3 / 0 | 0 / 0 | 7 / 8 |
| rickandmorty | 48 / 39 | 0 / 0 | 22 / 12 | 4 / 4 | 1 / 1 | 5 / 7 |
| ripcity | 45 / 38 | 0 / 0 | 17 / 10 | 0 / 0 | 0 / 0 | 11 / 11 |
| riskofrain | 20 / 17 | 0 / 0 | 46 / 29 | 0 / 0 | 0 / 0 | 4 / 3 |
| rit | 36 / 37 | 0 / 1 | 31 / 14 | 4 / 1 | 3 / 5 | 9 / 6 |
| rocketbeans | 58 / 46 | 0 / 0 | 16 / 9 | 0 / 0 | 0 / 0 | 12 / 5 |
| rocketleague | 63 / 43 | 0 / 0 | 11 / 8 | 1 / 2 | 2 / 0 | 5 / 9 |
| rojava | 17 / 16 | 0 / 0 | 40 / 22 | 0 / 0 | 0 / 0 | 2 / 4 |
| romania | 57 / 52 | 0 / 0 | 21 / 12 | 1 / 0 | 0 / 0 | 5 / 4 |
| roosterteeth | 45 / 39 | 0 / 0 | 23 / 14 | 1 / 0 | 1 / 1 | 4 / 3 |
| rotmg | 61 / 48 | 0 / 0 | 19 / 12 | 0 / 0 | 1 / 1 | 7 / 7 |
| rpi | 42 / 40 | 0 / 0 | 25 / 14 | 0 / 0 | 0 / 0 | 7 / 6 |
| runescape | 43 / 36 | 0 / 0 | 25 / 11 | 0 / 0 | 2 / 2 | 6 / 7 |
| rush | 34 / 32 | 0 / 0 | 35 / 24 | 3 / 2 | 1 / 1 | 3 / 3 |
| russia | 36 / 34 | 0 / 0 | 27 / 15 | 1 / 1 | 3 / 2 | 14 / 10 |
| Russiaclan | 43 / 36 | 0 / 0 | 23 / 16 | 0 / 0 | 3 / 3 | 5 / 3 |
| rust | 53 / 44 | 0 / 0 | 36 / 18 | 2 / 1 | 0 / 1 | 9 / 8 |
| rutgers | 61 / 48 | 0 / 0 | 10 / 6 | 0 / 0 | 0 / 0 | 6 / 7 |
| rwby | 45 / 43 | 0 / 0 | 22 / 15 | 0 / 0 | 0 / 0 | 8 / 6 |
| sabres | 41 / 39 | 0 / 0 | 24 / 15 | 0 / 0 | 3 / 1 | 6 / 7 |
| sadboys | 36 / 32 | 0 / 0 | 35 / 25 | 0 / 0 | 0 / 0 | 6 / 6 |
| sakartvelo | 9 / 7 | 0 / 0 | 54 / 41 | 0 / 0 | 1 / 1 | 3 / 4 |
| sakuragakuin | 34 / 30 | 0 / 0 | 33 / 19 | 1 / 1 | 0 / 0 | 13 / 9 |
| samuraijack | 66 / 43 | 0 / 0 | 24 / 16 | 5 / 4 | 0 / 0 | 4 / 8 |
| satania | 50 / 36 | 1 / 0 | 23 / 14 | 0 / 0 | 2 / 2 | 10 / 12 |
| sbu | 23 / 22 | 0 / 0 | 28 / 16 | 0 / 0 | 0 / 0 | 5 / 5 |
| schoolidolfestival | 42 / 30 | 0 / 0 | 31 / 20 | 1 / 1 | 0 / 0 | 7 / 8 |
| scotland | 51 / 47 | 0 / 0 | 22 / 9 | 0 / 0 | 0 / 1 | 8 / 6 |
| ScottPilgrim | 32 / 29 | 0 / 1 | 26 / 11 | 0 / 0 | 2 / 1 | 4 / 5 |
| scp | 39 / 32 | 0 / 0 | 35 / 30 | 1 / 0 | 1 / 1 | 6 / 4 |
| seahawks | 57 / 52 | 0 / 0 | 23 / 9 | 1 / 1 | 0 / 0 | 5 / 5 |
| seolhyun | 29 / 30 | 0 / 0 | 33 / 20 | 0 / 0 | 0 / 0 | 7 / 8 |
| serbia | 48 / 43 | 0 / 0 | 15 / 10 | 0 / 0 | 2 / 0 | 9 / 7 |
| seventeen | 10 / 10 | 0 / 0 | 40 / 28 | 2 / 0 | 3 / 3 | 3 / 3 |
| sheffield | 47 / 34 | 0 / 0 | 33 / 24 | 1 / 0 | 1 / 1 | 4 / 2 |
| shield | 38 / 29 | 0 / 0 | 27 / 20 | 2 / 1 | 2 / 1 | 10 / 9 |
| shishamo | 18 / 14 | 0 / 0 | 42 / 30 | 0 / 0 | 3 / 2 | 5 / 7 |
| shitredditsays | 36 / 30 | 0 / 1 | 30 / 15 | 4 / 4 | 1 / 0 | 7 / 6 |
| shrooms | 19 / 15 | 0 / 0 | 47 / 36 | 0 / 0 | 0 / 0 | 2 / 2 |
| signal | 7 / 7 | 0 / 0 | 55 / 41 | 1 / 1 | 0 / 0 | 4 / 3 |
| simonfraser | 41 / 30 | 0 / 0 | 30 / 21 | 3 / 1 | 0 / 2 | 7 / 4 |
| singapore | 48 / 43 | 0 / 1 | 19 / 10 | 0 / 0 | 0 / 0 | 4 / 4 |
| sips | 48 / 35 | 0 / 0 | 31 / 20 | 1 / 1 | 2 / 2 | 2 / 2 |
| sixers | 51 / 43 | 0 / 0 | 15 / 10 | 1 / 0 | 1 / 1 | 10 / 9 |
| skyrim | 46 / 37 | 0 / 0 | 17 / 10 | 1 / 0 | 0 / 1 | 7 / 7 |
| Slovakia | 30 / 28 | 0 / 0 | 28 / 20 | 1 / 0 | 2 / 1 | 10 / 9 |
| slovenia | 35 / 32 | 0 / 0 | 27 / 19 | 2 / 1 | 0 / 1 | 9 / 9 |
| smashbros | 50 / 40 | 0 / 0 | 22 / 14 | 2 / 2 | 1 / 1 | 9 / 6 |
| smite | 37 / 29 | 0 / 0 | 18 / 13 | 0 / 0 | 0 / 0 | 12 / 12 |
| snsd | 38 / 34 | 0 / 0 | 29 / 18 | 1 / 0 | 0 / 1 | 5 / 3 |
| sonicthehedgehog | 33 / 28 | 0 / 0 | 27 / 18 | 0 / 0 | 5 / 3 | 8 / 9 |
| sooners | 36 / 29 | 0 / 0 | 33 / 15 | 0 / 1 | 1 / 1 | 4 / 3 |
| southafrica | 40 / 36 | 0 / 0 | 20 / 14 | 2 / 2 | 1 / 0 | 11 / 9 |
| southpark | 33 / 28 | 0 / 0 | 38 / 26 | 2 / 1 | 1 / 1 | 4 / 4 |
| soylent | 29 / 20 | 0 / 0 | 33 / 19 | 2 / 2 | 0 / 0 | 3 / 2 |
| spacex | 13 / 13 | 0 / 0 | 43 / 26 | 1 / 1 | 6 / 2 | 1 / 1 |
| spacexmasterrace | 44 / 38 | 0 / 0 | 21 / 14 | 0 / 0 | 0 / 0 | 11 / 9 |
| spain | 44 / 37 | 0 / 0 | 21 / 11 | 2 / 2 | 5 / 5 | 8 / 7 |
| spelunky | 16 / 13 | 0 / 0 | 56 / 44 | 0 / 0 | 0 / 0 | 1 / 3 |
| splatoon | 43 / 34 | 0 / 0 | 28 / 16 | 0 / 0 | 2 / 3 | 2 / 4 |
| spongebob | 32 / 27 | 0 / 0 | 40 / 32 | 0 / 0 | 0 / 0 | 5 / 3 |
| SquareSpiral | 49 / 42 | 0 / 0 | 24 / 17 | 0 / 0 | 1 / 1 | 6 / 5 |
| ss13 | 44 / 42 | 0 / 0 | 26 / 14 | 0 / 0 | 2 / 1 | 9 / 7 |
| ssbpm | 36 / 28 | 0 / 0 | 30 / 21 | 6 / 7 | 0 / 0 | 9 / 7 |
| starbound | 38 / 32 | 0 / 0 | 23 / 10 | 0 / 0 | 1 / 1 | 3 / 4 |
| starcitizen | 71 / 51 | 0 / 0 | 15 / 12 | 1 / 1 | 0 / 0 | 7 / 8 |
| starcraft | 49 / 40 | 0 / 0 | 21 / 15 | 1 / 1 | 0 / 0 | 5 / 4 |
| stardewvalley | 48 / 41 | 0 / 0 | 27 / 18 | 0 / 0 | 0 / 0 | 7 / 8 |
| stardustcrusaders | 58 / 45 | 0 / 0 | 24 / 18 | 0 / 0 | 0 / 0 | 9 / 11 |
| stargate | 35 / 34 | 0 / 0 | 35 / 21 | 0 / 0 | 0 / 0 | 6 / 4 |
| starlightstage | 55 / 46 | 0 / 0 | 29 / 19 | 4 / 4 | 0 / 0 | 5 / 4 |
| starryknights | 37 / 30 | 0 / 0 | 32 / 22 | 0 / 0 | 0 / 0 | 8 / 8 |
| startrek | 28 / 22 | 0 / 0 | 29 / 21 | 3 / 3 | 3 / 2 | 11 / 11 |
| starvstheforcesofevil | 58 / 39 | 0 / 0 | 13 / 9 | 2 / 2 | 0 / 0 | 10 / 11 |
| stevenuniverse | 57 / 44 | 0 / 0 | 14 / 10 | 0 / 0 | 2 / 0 | 8 / 8 |
| stlouis | 48 / 32 | 0 / 0 | 30 / 18 | 1 / 1 | 0 / 0 | 5 / 7 |
| stlouisblues | 57 / 46 | 0 / 0 | 15 / 10 | 1 / 0 | 0 / 0 | 10 / 9 |
| strangerthings | 39 / 35 | 0 / 0 | 22 / 14 | 1 / 1 | 0 / 0 | 8 / 9 |
| straya | 45 / 37 | 0 / 1 | 21 / 9 | 1 / 0 | 0 / 1 | 5 / 9 |
| streetfighter | 28 / 26 | 0 / 0 | 44 / 30 | 1 / 1 | 1 / 1 | 3 / 2 |
| Summit1G | 30 / 22 | 0 / 0 | 34 / 24 | 1 / 0 | 2 / 4 | 11 / 9 |
| suomi | 61 / 43 | 0 / 0 | 9 / 6 | 0 / 1 | 1 / 1 | 6 / 7 |
| superman | 17 / 14 | 0 / 0 | 46 / 34 | 0 / 0 | 4 / 4 | 2 / 2 |
| survivor | 43 / 37 | 0 / 0 | 22 / 13 | 1 / 1 | 2 / 0 | 9 / 10 |
| sweden | 45 / 41 | 0 / 0 | 10 / 7 | 1 / 1 | 1 / 0 | 13 / 11 |
| SwissNeutralityZone | 39 / 33 | 0 / 0 | 25 / 17 | 0 / 0 | 0 / 0 | 9 / 8 |
| switzerland | 36 / 32 | 0 / 1 | 29 / 18 | 0 / 0 | 0 / 0 | 5 / 5 |
| swordartonline | 35 / 32 | 0 / 0 | 34 / 23 | 1 / 1 | 0 / 1 | 9 / 7 |
| SydneyFC | 13 / 15 | 0 / 0 | 46 / 29 | 2 / 2 | 1 / 0 | 0 / 1 |
| tagpro | 54 / 32 | 0 / 0 | 21 / 15 | 0 / 3 | 0 / 0 | 10 / 10 |
| taiwan | 40 / 40 | 0 / 0 | 23 / 11 | 1 / 0 | 2 / 1 | 10 / 10 |
| tampabaylightning | 42 / 37 | 0 / 0 | 18 / 10 | 0 / 0 | 0 / 0 | 9 / 8 |
| teamcube | 35 / 32 | 0 / 0 | 34 / 21 | 0 / 0 | 0 / 0 | 5 / 4 |
| TeamDignitas | 32 / 28 | 0 / 0 | 31 / 23 | 0 / 0 | 2 / 1 | 7 / 4 |
| TeamYellowPlace | 29 / 21 | 0 / 0 | 36 / 28 | 0 / 1 | 0 / 0 | 4 / 3 |
| telegram | 26 / 21 | 0 / 1 | 33 / 16 | 1 / 0 | 2 / 2 | 9 / 6 |
| Temple | 55 / 43 | 0 / 0 | 18 / 10 | 0 / 0 | 0 / 0 | 4 / 7 |
| tenma | 2 / 2 | 0 / 0 | 64 / 49 | 0 / 0 | 0 / 0 | 1 / 1 |
| terraria | 46 / 38 | 0 / 0 | 23 / 10 | 2 / 1 | 1 / 2 | 5 / 7 |
| teslamotors | 58 / 43 | 0 / 0 | 22 / 14 | 2 / 2 | 1 / 0 | 5 / 5 |
| tetris | 11 / 11 | 0 / 1 | 48 / 36 | 1 / 0 | 5 / 4 | 6 / 4 |
| texans | 53 / 43 | 0 / 0 | 22 / 16 | 0 / 0 | 2 / 0 | 8 / 5 |
| texas | 41 / 39 | 0 / 0 | 12 / 6 | 0 / 0 | 6 / 1 | 12 / 9 |
| texastech | 35 / 30 | 0 / 0 | 25 / 16 | 1 / 0 | 1 / 1 | 12 / 10 |
| tf2 | 45 / 38 | 0 / 0 | 10 / 3 | 2 / 2 | 0 / 0 | 13 / 13 |
| thailand | 46 / 40 | 0 / 0 | 29 / 18 | 2 / 2 | 1 / 0 | 2 / 3 |
| the_pack | 41 / 37 | 0 / 0 | 27 / 18 | 1 / 1 | 0 / 0 | 5 / 3 |
| THE_R | 7 / 4 | 0 / 0 | 34 / 20 | 0 / 0 | 0 / 0 | 2 / 2 |
| TheAdventuresofTintin | 11 / 8 | 0 / 0 | 54 / 41 | 1 / 0 | 0 / 1 | 3 / 3 |
| TheB1G | 33 / 30 | 0 / 0 | 18 / 7 | 0 / 0 | 2 / 3 | 16 / 16 |
| theblackvoid | 45 / 32 | 0 / 0 | 23 / 17 | 0 / 0 | 1 / 1 | 9 / 11 |
| thebluecorner | 61 / 42 | 0 / 0 | 11 / 9 | 0 / 0 | 1 / 0 | 14 / 14 |
| theexpanse | 55 / 40 | 0 / 0 | 20 / 15 | 1 / 1 | 1 / 0 | 5 / 5 |
| TheFarLeftSide | 55 / 43 | 0 / 0 | 18 / 14 | 0 / 0 | 0 / 0 | 6 / 8 |
| Thegreatblackhole | 30 / 20 | 0 / 0 | 39 / 16 | 1 / 0 | 0 / 3 | 7 / 6 |
| TheGreatGreenBox | 29 / 25 | 0 / 0 | 34 / 25 | 1 / 0 | 0 / 0 | 8 / 7 |
| TheHulk | 42 / 33 | 0 / 0 | 32 / 21 | 1 / 1 | 0 / 0 | 4 / 6 |
| TheID | 1 / 2 | 0 / 0 | 62 / 48 | 0 / 0 | 0 / 0 | 3 / 2 |
| theitalyplace | 47 / 46 | 0 / 0 | 15 / 13 | 0 / 0 | 4 / 0 | 8 / 8 |
| thenetherlands | 44 / 37 | 0 / 0 | 18 / 11 | 1 / 1 | 4 / 3 | 11 / 11 |
| thepointing | 29 / 27 | 0 / 1 | 31 / 20 | 3 / 0 | 0 / 3 | 7 / 6 |
| thesilphroad | 43 / 35 | 1 / 0 | 18 / 10 | 7 / 6 | 1 / 2 | 8 / 9 |
| thesimpsons | 36 / 33 | 0 / 0 | 34 / 22 | 1 / 1 | 0 / 0 | 8 / 4 |
| thetreesnetwork | 17 / 11 | 0 / 0 | 53 / 42 | 1 / 1 | 0 / 0 | 2 / 3 |
| timbers | 47 / 38 | 0 / 0 | 19 / 12 | 0 / 0 | 0 / 0 | 4 / 4 |
| tinytardis | 32 / 27 | 0 / 0 | 39 / 27 | 0 / 0 | 2 / 1 | 1 / 2 |
| titanfall | 44 / 40 | 0 / 0 | 24 / 14 | 2 / 1 | 1 / 0 | 8 / 8 |
| tokyo | 17 / 17 | 0 / 0 | 48 / 37 | 1 / 1 | 1 / 1 | 6 / 3 |
| toolband | 48 / 36 | 0 / 0 | 17 / 11 | 1 / 2 | 3 / 2 | 10 / 11 |
| torontoraptors | 55 / 41 | 0 / 0 | 24 / 14 | 2 / 0 | 0 / 2 | 8 / 9 |
| totallynotrobots | 49 / 41 | 0 / 0 | 30 / 20 | 1 / 1 | 2 / 1 | 2 / 1 |
| touhou | 57 / 44 | 0 / 0 | 21 / 15 | 1 / 1 | 0 / 0 | 5 / 5 |
| traaaaaaannnnnnnnnns | 47 / 40 | 0 / 0 | 28 / 19 | 1 / 1 | 0 / 0 | 5 / 3 |
| TransFlagPlace | 41 / 27 | 0 / 0 | 17 / 16 | 0 / 0 | 3 / 2 | 12 / 11 |
| transformers | 39 / 33 | 1 / 1 | 20 / 12 | 1 / 1 | 1 / 1 | 15 / 11 |
| transgender | 12 / 10 | 0 / 1 | 53 / 40 | 2 / 0 | 0 / 2 | 4 / 3 |
| TreePlace | 23 / 17 | 0 / 0 | 43 / 32 | 3 / 2 | 0 / 1 | 6 / 7 |
| trees | 44 / 39 | 0 / 0 | 12 / 9 | 4 / 4 | 0 / 0 | 13 / 10 |
| truestl | 32 / 27 | 0 / 0 | 31 / 16 | 1 / 0 | 4 / 5 | 4 / 7 |
| TsundereSharks | 40 / 32 | 0 / 1 | 25 / 18 | 0 / 0 | 0 / 0 | 9 / 8 |
| turkey | 60 / 54 | 0 / 1 | 13 / 4 | 0 / 1 | 0 / 1 | 7 / 6 |
| twentyonepilots | 41 / 35 | 0 / 0 | 36 / 25 | 3 / 2 | 1 / 1 | 3 / 3 |
| twice | 44 / 38 | 0 / 0 | 26 / 18 | 4 / 2 | 1 / 2 | 9 / 7 |
| twitch | 20 / 18 | 0 / 0 | 48 / 21 | 3 / 3 | 0 / 0 | 5 / 6 |
| twitchplayspokemon | 51 / 38 | 0 / 0 | 26 / 16 | 1 / 0 | 2 / 2 | 10 / 8 |
| ubc | 39 / 34 | 0 / 0 | 21 / 10 | 0 / 0 | 1 / 1 | 11 / 11 |
| ubreddit | 27 / 25 | 0 / 0 | 34 / 20 | 1 / 1 | 2 / 1 | 10 / 10 |
| ucf | 43 / 39 | 0 / 0 | 26 / 15 | 0 / 0 | 0 / 0 | 4 / 5 |
| udub | 26 / 29 | 0 / 0 | 32 / 22 | 0 / 0 | 2 / 1 | 11 / 7 |
| ufl | 29 / 19 | 0 / 0 | 37 / 26 | 0 / 2 | 0 / 0 | 8 / 10 |
| uiowa | 34 / 31 | 0 / 0 | 34 / 22 | 0 / 0 | 1 / 0 | 3 / 2 |
| uiuc | 52 / 47 | 0 / 1 | 13 / 2 | 2 / 2 | 0 / 0 | 7 / 5 |
| ukplace | 42 / 26 | 0 / 0 | 20 / 14 | 0 / 0 | 0 / 0 | 7 / 5 |
| ukraine | 24 / 28 | 0 / 0 | 32 / 22 | 0 / 0 | 3 / 1 | 10 / 9 |
| ultrahardcore | 22 / 18 | 0 / 0 | 43 / 23 | 2 / 2 | 0 / 0 | 2 / 3 |
| UMiami | 5 / 3 | 0 / 0 | 61 / 43 | 0 / 0 | 0 / 0 | 0 / 0 |
| undertale | 45 / 44 | 0 / 0 | 21 / 12 | 2 / 0 | 2 / 1 | 10 / 6 |
| unitedkingdom | 45 / 36 | 0 / 0 | 13 / 7 | 1 / 0 | 1 / 1 | 12 / 12 |
| UNLincoln | 4 / 3 | 0 / 0 | 62 / 49 | 0 / 0 | 0 / 0 | 0 / 0 |
| unturned | 46 / 39 | 0 / 0 | 18 / 12 | 1 / 0 | 0 / 1 | 10 / 8 |
| uofm | 53 / 41 | 0 / 0 | 12 / 7 | 0 / 0 | 1 / 1 | 11 / 8 |
| uofmn | 44 / 41 | 0 / 0 | 21 / 12 | 0 / 0 | 2 / 1 | 4 / 2 |
| uoft | 52 / 46 | 0 / 1 | 18 / 10 | 1 / 1 | 1 / 0 | 7 / 3 |
| UPenn | 23 / 18 | 0 / 0 | 44 / 30 | 0 / 0 | 0 / 0 | 5 / 6 |
| uruguay | 37 / 31 | 0 / 0 | 26 / 17 | 0 / 0 | 1 / 1 | 12 / 10 |
| utahjazz | 52 / 48 | 0 / 0 | 27 / 19 | 0 / 1 | 1 / 0 | 6 / 3 |
| utaustin | 59 / 47 | 0 / 0 | 17 / 11 | 0 / 0 | 2 / 1 | 8 / 5 |
| uva | 36 / 33 | 0 / 1 | 35 / 20 | 0 / 0 | 0 / 0 | 5 / 7 |
| uvic | 28 / 24 | 0 / 0 | 42 / 32 | 0 / 0 | 2 / 1 | 4 / 2 |
| uwaterloo | 50 / 44 | 0 / 0 | 18 / 9 | 0 / 1 | 0 / 1 | 5 / 7 |
| vegan | 42 / 34 | 0 / 0 | 21 / 12 | 1 / 0 | 2 / 3 | 8 / 9 |
| VelvetUnderground | 15 / 14 | 0 / 0 | 46 / 34 | 0 / 0 | 0 / 0 | 7 / 7 |
| vermont | 26 / 23 | 0 / 0 | 41 / 32 | 0 / 0 | 3 / 1 | 4 / 2 |
| vietnam | 11 / 11 | 0 / 1 | 54 / 40 | 0 / 0 | 2 / 2 | 3 / 3 |
| Villanova | 22 / 19 | 0 / 0 | 40 / 29 | 2 / 0 | 5 / 5 | 5 / 4 |
| vim | 10 / 10 | 0 / 0 | 29 / 16 | 2 / 0 | 12 / 10 | 5 / 6 |
| vinesauce | 42 / 35 | 0 / 0 | 26 / 17 | 2 / 1 | 3 / 1 | 6 / 6 |
| virginiatech | 44 / 41 | 0 / 0 | 21 / 10 | 0 / 0 | 0 / 1 | 7 / 4 |
| vocaloid | 39 / 33 | 0 / 0 | 25 / 17 | 1 / 1 | 1 / 1 | 6 / 5 |
| wales | 32 / 27 | 0 / 0 | 29 / 20 | 1 / 0 | 1 / 2 | 13 / 10 |
| wallstreetbets | 50 / 40 | 0 / 0 | 26 / 20 | 0 / 0 | 0 / 0 | 5 / 5 |
| warframe | 54 / 50 | 0 / 0 | 25 / 14 | 2 / 2 | 0 / 0 | 3 / 2 |
| wario | 2 / 3 | 0 / 0 | 62 / 47 | 0 / 0 | 1 / 1 | 1 / 0 |
| warriors | 49 / 50 | 0 / 0 | 18 / 4 | 0 / 0 | 2 / 0 | 5 / 4 |
| warthunder | 41 / 38 | 0 / 0 | 38 / 21 | 8 / 8 | 0 / 0 | 3 / 4 |
| watchmen | 3 / 2 | 0 / 0 | 63 / 49 | 0 / 0 | 0 / 0 | 1 / 1 |
| weezer | 54 / 44 | 1 / 1 | 15 / 13 | 1 / 1 | 0 / 1 | 4 / 4 |
| wholesomememes | 64 / 41 | 0 / 0 | 30 / 25 | 6 / 7 | 1 / 0 | 6 / 6 |
| wildhockey | 50 / 42 | 0 / 0 | 19 / 15 | 1 / 1 | 3 / 0 | 8 / 8 |
| wine | 33 / 28 | 0 / 0 | 37 / 24 | 1 / 1 | 6 / 5 | 8 / 6 |
| winnipegjets | 44 / 37 | 0 / 0 | 22 / 13 | 0 / 0 | 0 / 0 | 11 / 11 |
| WisconsinBadgers | 22 / 20 | 0 / 0 | 38 / 27 | 0 / 0 | 0 / 0 | 9 / 8 |
| witcher | 42 / 38 | 0 / 0 | 29 / 20 | 0 / 0 | 2 / 2 | 2 / 3 |
| worldoftanks | 50 / 43 | 0 / 0 | 27 / 16 | 0 / 0 | 1 / 1 | 4 / 4 |
| worldpowers | 32 / 23 | 0 / 0 | 40 / 28 | 2 / 1 | 1 / 1 | 8 / 9 |
| wow | 55 / 50 | 0 / 0 | 27 / 16 | 3 / 3 | 1 / 1 | 8 / 6 |
| WPI | 27 / 22 | 0 / 0 | 38 / 25 | 0 / 0 | 0 / 0 | 6 / 7 |
| wsu | 17 / 14 | 0 / 0 | 38 / 26 | 1 / 1 | 1 / 1 | 3 / 3 |
| xcom | 49 / 33 | 0 / 0 | 22 / 15 | 3 / 1 | 4 / 5 | 4 / 6 |
| xenoblade_chronicles | 38 / 29 | 0 / 0 | 32 / 21 | 0 / 0 | 0 / 0 | 9 / 8 |
| yerbamate | 1 / 1 | 0 / 0 | 64 / 49 | 0 / 0 | 0 / 0 | 1 / 1 |
| yogscast | 45 / 32 | 0 / 0 | 21 / 13 | 1 / 1 | 1 / 1 | 14 / 13 |
| yugioh | 51 / 42 | 0 / 0 | 32 / 19 | 6 / 6 | 0 / 0 | 4 / 5 |
| yumenikki | 32 / 25 | 0 / 0 | 35 / 25 | 0 / 1 | 0 / 0 | 6 / 6 |
| yuyuyu | 29 / 25 | 0 / 0 | 34 / 21 | 0 / 0 | 0 / 0 | 3 / 4 |
| zelda | 40 / 31 | 0 / 0 | 31 / 23 | 5 / 2 | 6 / 8 | 6 / 5 |
| zootopia | 55 / 37 | 0 / 0 | 20 / 13 | 1 / 3 | 2 / 0 | 8 / 9 |
