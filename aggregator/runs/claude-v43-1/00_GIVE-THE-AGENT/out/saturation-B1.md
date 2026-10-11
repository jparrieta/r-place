# Saturation, stage B1: the test (B1c) and the second pass (B1d)

## B1c, the saturation test, 2026-10-11

### The rule and the sample

The seed and the rule were written into `notes-B1.md` (section "Leg B1c") before the draw. The 705 read rooms, sorted by name, were shuffled with `saturation.py`'s own `shuffled`, seed cd472a6087a223d4 (`out/seed.txt`), tag "B1c". Rooms were taken from the head of that order until at least 30 rooms and 300 second-order themes were reached (`out/_analysis/b1c_sample.py`). The sample is 30 rooms, 317 second-order themes, 3,891 concepts and 24.8 average rooms of words.

The 30 rooms, in draw order: rainbowgrid, stardustcrusaders, kamenrider, ik_ihe, kurdistan, poland, france, vinesauce, oman, mexico, gatech, PlaceNL, VelvetUnderground, ubc, DevonUK, glasgow, wholesomememes, cardinals, picturegame, radiohead, sixers, Fez, sakuragakuin, math, scp, foxes, drawhelix, ChronoTrigger, TeamDignitas, hellointernet.

Each room was printed whole with its second-order themes, their notes, and every concept's label, hour and first 90 characters of words, with the recorded placements filtered out. I held only `mem.py scheme --brief`, the 197 labels. The kinds have no written gates yet (B1e writes them), so the labels were the gates. Each second-order theme got a fresh placement and a verdict before the room's recorded placements were looked at (`out/_analysis/b1c_fresh.psv`). Disagreements with the record were then judged one by one (`out/_analysis/b1c_disagreements.psv`).

### The count

The next table gives the fresh verdicts for the 317 second-order themes.

| Verdict | Themes |
|---|---|
| fits: a label takes the theme and its concepts | 299 |
| gate fails: two labels take it and nothing decides, or the label misdescribes it | 15 |
| bare: a bare title, link or reply, unplaced in the record too | 3 |
| new kind: a concept or theme no label can take | 0 |
| split: a kind shown to hold two doings | 0 |

Comparing with the record added 20 more themes where the gate fails. These are themes the fresh reading placed without hesitation, but where the record chose a different kind and the two labels cannot say which reading is right. The comparison also found 2 slips in the fresh reading (glasgow t03, PlaceNL t20). It found 1 recorded kind used beyond its label (kurdistan t03, T3-132 names a Discord) and 2 label overlaps in additional kinds (poland t07, gatech t04).

**What does not fit: 35 of 317 second-order themes (11.0%) in 20 of the 30 rooms meet a gate that fails. No concept needs a new kind and no kind needs a split.** By the concept test, the new kinds per hundred second-order themes in the sample are 0.

The 35 themes fall into three groups.

- **Two labels both take the theme (15).**
  - T3-003 against T3-038: stardustcrusaders t05, wholesomememes t07.
  - T3-074 against T3-136: vinesauce t08, scp t02.
  - T3-037 against T3-098: glasgow t02, cardinals t04.
  - T3-044 against T3-082, for the mark drawing outsiders to the room: DevonUK t02, hellointernet t12.
  - T3-068, T3-061 and T3-006, for replacing another nation's flag with one's own: kurdistan t02.
  - T3-024 against T3-010: stardustcrusaders t06.
  - T3-046 against T3-076: PlaceNL t14.
  - T3-016 against T3-074: wholesomememes t09.
  - T3-010 against T3-151: Fez t07.
  - T3-010 against T3-149, for non-aggression pacts: math t04.
  - T3-070 against T3-091, both naming templates: ChronoTrigger t02.
- **A label narrower than its use (5).**
  - T3-065 says national, and was used for the Devon county flag (DevonUK t01).
  - T3-115 says a rival fandom, and was used for Europe's call for help (gatech t07).
  - T3-063 says canvas posts, and was used for April Fools posts (wholesomememes t15).
  - T3-048 says the company, and a creator's own joke did not reach it in the record (wholesomememes t13).
  - T3-088 says extra accounts, and was used for a placement glitch (hellointernet t08).
- **No single label names the theme's doing (15 themes, 10 doings).** The labels take each concept, but not the whole. The 10 doings:
  - registering or hoping beyond the canvas's end: stardustcrusaders t17, oman t06, PlaceNL t19, ubc t09, sakuragakuin t11. The record put these in T3-016, T3-073 and T3-117.
  - watching and reporting the live canvas: france t09, cardinals t06.
  - gathering lone placers into a group: rainbowgrid t02.
  - drawing up the room's plan of operations: france t05.
  - enlarging the room's own mark: mexico t05.
  - a canvas thread taken over by side disputes: mexico t18.
  - organisers conceding that placers ignore the plan: PlaceNL t11.
  - crossposting designs between subs: PlaceNL t13.
  - routing posts to sister subs: wholesomememes t10.
  - April Fools talk with no fake staged: wholesomememes t12.

  Four of these doings were logged as ideas at the count, not when first seen (`ideas-B1.jsonl` lines 211 to 214). They are reporting the live canvas, conceding placers ignore the plan, gathering lone placers together, and planning the room's pixel operations. If all four became kinds, the sample's rate would be 1.26 new kinds per hundred second-order themes. If all ten did, it would be 3.15.

### The fresh reading against the record

The next table compares the fresh placements with the recorded ones. It covers the 313 second-order themes that both readings placed (`out/_analysis/b1c_totals.py`).

| Measure | Value |
|---|---|
| same primary kind | 263 (84.0%) |
| fresh primary among the recorded kinds | 281 (89.8%) |
| at least one kind shared | 297 (94.9%) |
| no kind shared | 16 (5.1%) |
| kinds per theme, fresh / recorded | 1.75 / 1.81 |
| recorded placements the fresh reading did not give | 165 of 565 |
| fresh placements the record does not hold | 147 of 547 |

The primary kinds hold across two readings by the same reader at different times. The placements as a whole hold less well: 165 of 565 recorded placements and 147 of 547 fresh ones have no match in the other reading. Primaries agree in 84 to 90% of themes, so most of these differences lie in the second and third kinds of rule 0. Stage B3 places from the gates. So the gates written at B1e must say when a second kind is owed, or the fleet will disagree there most.

### Beside it: the first pass's new kinds per hundred second-order themes

These figures were computed by room (`out/_analysis/b1c_discovery.py`). The rooms are in the order the first pass read them, and each mint in `theme_discovery.jsonl` is set at the end of its room. The `themes_read` field of `theme_discovery.jsonl` counts reads with repeats, so it is not used. Over the whole first pass: 197 mints in 7,844 second-order themes, 2.51 per hundred. There were 60 in the first hundred themes and 0 in the last hundred. The last mint, T3-197, came in room 661 of 705. 44 rooms and 520 second-order themes followed it with no new kind. The stopping rule counts 202 kinds, because it counts the PI's splits of T3-010 as new kinds.

The next table gives the first pass's mints by tenths of the rooms read.

| Rooms | Second-order themes | New kinds | Per hundred |
|---|---|---|---|
| 1 to 70 | 841 | 135 | 16.05 |
| 71 to 141 | 864 | 28 | 3.24 |
| 142 to 212 | 760 | 14 | 1.84 |
| 213 to 282 | 784 | 11 | 1.40 |
| 283 to 352 | 750 | 3 | 0.40 |
| 353 to 423 | 880 | 5 | 0.57 |
| 424 to 494 | 745 | 0 | 0.00 |
| 495 to 564 | 757 | 0 | 0.00 |
| 565 to 634 | 689 | 0 | 0.00 |
| 635 to 705 | 774 | 1 | 0.13 |

The test found 0 new kinds per hundred by the concept test. That matches the first pass's last four tenths: 1 new kind in 2,965 themes, 0.03 per hundred. If the four logged ideas became kinds, the test's rate would be 1.26 per hundred. That lies between the first pass's rates in rooms 213 to 282 (1.40) and rooms 283 to 352 (0.40). The kinds have saturated. The labels, read as gates, have not: one theme in nine meets a label that cannot decide or that says too little.

### Rooms for the second pass's chosen list

The rule names every room with a verdict other than fits. The rooms with a gate that fails (20): rainbowgrid, stardustcrusaders, kurdistan, france, vinesauce, oman, mexico, gatech, PlaceNL, ubc, DevonUK, glasgow, wholesomememes, cardinals, Fez, sakuragakuin, math, scp, ChronoTrigger, hellointernet. ik_ihe's only such verdict is a bare pointer. It is named here, but it gives the second pass nothing to test. The 9 rooms where every theme fit: poland, kamenrider, VelvetUnderground, picturegame, radiohead, sixers, foxes, drawhelix, TeamDignitas.

## B1d, the second pass

### The chosen list and the rule

`out/pass2-chosen-B1.txt` was written at B1d-01 before the first room was reread. It holds 108 rooms in three groups:
- the 20 rooms with a gate that failed at B1c;
- 23 more rooms with the most hesitations in the log (`out/_analysis/b1d_hesitations.py`: the top 20 by score, with ties at the twentieth score kept, 24 rooms, PlaceNL already in the first group);
- 65 more contrary rooms. These are the 66 rooms tagged "contrary room" in the B1 log through B1b-22, plus morrowind and Summit1G from the head; ubc, wholesomememes and Fez are already in the first group. `contrast.md` lists the contrast's two sides, not the contrary rooms, so this group may be short of the A1 heads' lists.

The rooms are read in the seeded order (`saturation.py order --stage B1`). Each room gets its A1 note, every second-order theme with every concept's words, and its forest whole. `mem.py reread` records each room in `pass2-B1.jsonl`. The pass stops when two things hold (J, 2026-10-07). Every chosen room has been read. The run since this pass's last new kind has reached marker 1's empty run, 78 rooms and 72.1 average rooms, and at least 30 rooms.

### The stretches

The next table gives each stretch, its new kinds and the run after it, from `saturation.py pass2 --stage B1`.

| Stretch | Leg | Orders | Rooms | Codes and themes | New kinds | Run after the stretch |
|---|---|---|---|---|---|---|
| 1 | B1d-01 | 47 (morrowind) to 184 (egypt) | 21 | about 974,000 bytes | 0 | 21 rooms, 21.4 average rooms |

Stretch 1 rooms, in order: morrowind, Summit1G, popheads, homelab, qotsa, aeskwadraat, falcons, canucks, cirkeltrek, kurdistan, theitalyplace, PinkVomitMonster, ubc, bobross, pcmasterrace, mariokart, rust, gatech, AprilKnights, flashtv, egypt. After it, 21 of the 108 chosen rooms are read. The next room is totallynotrobots.

Stretch 1 minted nothing, split nothing and merged nothing. It logged 28 place events into existing kinds (`kinds-B1.jsonl`) and 9 unplacements, so placements rose by 19, from 13,440 to 13,459. Most of the new placements are second or third kinds under rule 0. Four of the events and four of the unplacements belong to two moves that were reverted the same leg (popheads t04, mariokart t02; see `notes-B1.md`). It also wrote 23 rule 0 lines and 1 bag (theitalyplace t08) and 9 `tier_history.jsonl` lines. One kind was widened. T3-188 (disowning rogue offshoots of the work) had held one theme. It now holds 6 themes in 6 rooms: ainbowroad, cirkeltrek, polska, PlaceNL, denmark and gatech. This is the doing the B1c idea "conceding placers ignore the plan" named: an organised room tells others it does not control the placers acting in its name. At B1e its label is to become "separating the plan from placers it cannot control". The stretch did not meet the other three B1c ideas: reporting the live canvas, gathering lone placers together, and planning the room's pixel operations.

The gates that failed at B1c in kurdistan t02, ubc t09 and gatech t07 need B1e work, not new kinds. kurdistan t02 needs a discriminator between T3-068, T3-061 and T3-006. ubc t09 and gatech t07 need the label changes already listed for T3-117 and T3-115.
