# Adjudication report, stage B4 (packets 1 to 7: the full report)

Written at B4a-07, after packet 7, the last packet, was ruled. Every one of the 3,288 contested items has its ruling. Packet 7 was ruled from its first item under all of J's rulings of 13 October: (1) and (2) of 06:45 and 06:47 Berlin, the `also_present` ruling of 09:09 Berlin, the answers to QB4-002 and QB4-003, and the lone-B1 rule I chose under J's answer of 12:28 Berlin. Rulings written before an answer arrived in packets 1 to 6 were corrected through `b4_rule_append.py --replace`, keeping each superseded ledger. This report replaces the interim reports of B4a-01 to B4a-06; older versions are in the git history of this file and in the superseded ledgers `disagreements.superseded-*.jsonl`.

Where the figures come from:
- Per-packet figures: `out/_adjudication-B4/packet-01/summary.md` to `packet-07/summary.md` (`out/_analysis/b4_packet_summary.py`).
- The sums: `out/_analysis/b4_cumulative.py --packets 1,2,3,4,5,6,7`.
- The named_neither split and the class 4 measure: `out/_analysis/b4_named_neither_split.py --packet N` and `out/_analysis/b4_packet_detail.py --packet N`. Ranges within a packet: `out/_analysis/b4_agreement_range.py`.
- Checks: `b4_own_support_check.py` (a placed theme with no concept of its own), `b4_bag_named_check.py` (named themes in the bag test), `b4_lone_b1_check.py` (lone B1 themes in class 4) and, new at B4a-07, `b4_both_readers_dropped.py` (a ruling that leaves out a theme both readers placed).
- The re-rule drafts: `out/_adjudication-B4/rerule-B4a-05/`, `rerule-ap-B4a-05/`, `rerule-bag-B4a-06/`, `rerule-loneb1-B4a-06/` and `packet-07/corrections-01.jsonl`.
- The rulings: `out/disagreements.jsonl` (3,288 lines). The final placements: `out/assign_final.jsonl` (7,844 lines: class 1 2,566, class 2 1,990, ruled 3,288). The boundary paragraphs: `out/_adjudication-B4/boundaries.md`, carried below with their item lists.

## Items adjudicated

Stage B3's inventory (`b3_classes.jsonl`, J's five classes) leaves 3,288 contested items: class 3 (the readers' lists differ) 2,393, class 4 (the readers agree on a list not inside my B1 grouping) 837, class 5 (no B1 grouping) 58. All are ruled.
- **Packet 1** ruled 491: the 18 gloss-only items, G01 (April Fools in the sub) and G02 (the sub's own business).
- **Packet 2** ruled 447: G03 (where the planning happens), G04 (calling people in to place), G05 (telling placers what to place) and G06 (strain, doubt and giving up).
- **Packet 3** ruled 500: G07 (choosing what to make and where) and the first 254 items of G08 (building and growing the mark).
- **Packet 4** ruled 461: the last 6 items of G08, G09 (keeping the mark against damage), G10 (finding who did it) and G11 (scripts, bots and extra accounts).
- **Packet 5** ruled 409: G12 (attacking others' work), G13 (holding back from others' work) and G14 (space and help between rooms).
- **Packet 6** ruled 500: G15 (deals and alliances between rooms), G16 (factions and kindred rooms), G17 (national feeling and the flag), G18 (politics and the community's own quarrels), G19 (rivalry, taunts and victory) and the first 184 items of G20 (talk around the canvas).
- **Packet 7** ruled 480: the last 53 items of G20 (items 1 to 53: records, remakes, atlases and the creators' notice) and G21, the aftermath (items 54 to 480: the work celebrated, credited, told, mourned, kept, carried to a later canvas, and the canvas's end). 357 class 3, 118 class 4, 5 class 5.

## The taxonomy split

The next table counts the rulings by taxonomy value, by packet and by class.

| taxonomy | all | packet 1 | packet 2 | packet 3 | packet 4 | packet 5 | packet 6 | packet 7 | class 3 | class 4 | class 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| genuine-joint | 1651 | 137 | 216 | 231 | 239 | 269 | 256 | 303 | 1651 | 0 | 0 |
| author-error | 571 | 99 | 78 | 78 | 86 | 58 | 83 | 89 | 3 | 547 | 21 |
| scheme-ambiguous | 451 | 121 | 62 | 94 | 59 | 14 | 71 | 30 | 385 | 63 | 3 |
| item-is-a-bag | 255 | 21 | 43 | 72 | 50 | 32 | 20 | 17 | 202 | 53 | 0 |
| author-disagrees | 208 | 36 | 45 | 21 | 13 | 20 | 51 | 22 | 0 | 174 | 34 |
| reader-error | 152 | 77 | 3 | 4 | 14 | 16 | 19 | 19 | 152 | 0 | 0 |
| total | 3288 | 491 | 447 | 500 | 461 | 409 | 500 | 480 | 2393 | 837 | 58 |

How to read it:
- **Genuine-joint is half the rulings, 1,651 (50.2%).** In packet 7 it is 303 of 480 (63.1%), the highest share of any packet. G21's coders wrote the room's account of its finished work as one practice (conflict CC-063): the work celebrated, its makers credited, allies thanked, images kept, losses mourned and what happened told, all in one second-order theme. One reader places the leading act and the other adds a second. The count measures how rule 0 travelled, not the readers.
- **Author-error is 571.** Packet 7 has 89, 88 of them in class 4, where both readers placed a theme my B1 grouping lacked; the commonest were T3-043 (20), T3-117 (14), T3-073 (12) and T3-037 (9).
- **Scheme-ambiguous is 451 (13.7%).** Packet 7 has 30 (6.3%), the fewest share after packet 5. They are spread: T3-052's `must_show` 4, T3-009's 3, T3-164's 3, and single sentences.
- **Item-is-a-bag is 255.** Packet 7 has 17.
- **Reader-error is 152.** Packet 7 has 19. They include rulings where the T3-029|T3-073 paragraph decides (a plain or consoling account put under grief: foxstevenson t07, ultrahardcore t09) and where a test needs the room's own work or words the reader read from the canvas (uvic t04, nascar t12).
- **No ruling holds a theme no placement held**, and no `also_present` lists a theme that no reader and not my B1 named. Every class 4 ruling that keeps a theme only my B1 placed gives it three concepts or more (`b4_lone_b1_check.py`: 162 lines over the seven packets, 18 of them in packet 7).

## J's rulings on themes added (QB4-001), and the re-ruling of packets 1 to 4

I asked J at B4a-03 (QB4-001) whether to keep adding a one- or two-concept theme that no placement held. J answered at 06:43 Berlin on 13 October: "Ask it to stop. The point is to try to adjudicate. I imagine that the additions are really just the analyst trying to be nice. And not go back on what others said". J's rulings at 06:45 and 06:47 Berlin:
1. The placements are the readers' and the analyst's (my B1). A ruling chooses among those placements and adds no theme beyond them.
2. A ruling takes the union of placements only when it names, for each theme it keeps, the separate concept that carries it; otherwise it chooses.
3. Re-rule only the items in packets 1 to 4 whose ruling holds a theme no placement held, under (1) and (2), and keep the superseded ledger.

At B4a-05, 378 rulings were re-ruled under (3): packet 1 30, packet 2 58, packet 3 157, packet 4 133. The method, applied to every packet since:
- **The removed theme's concepts.** Each is read against the tests of the themes the placements hold. A concept counts toward a placed theme when that theme's `must_show` takes it and no field sends it to another placed theme. A `must_not_show` that sends it to a theme no placement holds does not stop it. Otherwise the concept is left out and named in the why.
- **Rule 0 inside the placements.** Order the placed themes by concept count, ties by how many of reading A, reading B and my B1 hold the theme; place at most three. A one- or two-concept theme is kept when it leads its level on placements; where themes tie at a level with equal placements, none is kept and the order ends. Where the top of the order is a tie on concepts and placements, all the tied themes are placed.
- **Unresolved** where no placement's test takes the material.

What the re-ruling did is set out in this report's B4a-05 version. Agreement after over packets 1 to 4 rose from 0.565 to 0.628, and named_neither fell from 741 to 485.

**A reading added at B4a-07.** The level rule could drop a theme both readers placed, with a concept of its own, on a placement count that only my B1 tipped. From kanye t28 (class 4) and msu t11 (class 3) on, such a theme is not dropped on that count. Two earlier packet 7 rulings were corrected under it: ChronoTrigger t06 (T3-157, placed by both readers, now stands) and mindcrack t11 (where T3-029's placements had been miscounted). `b4_both_readers_dropped.py` lists the packet 7 rulings that leave out a theme both readers placed: five, each because the theme holds no concept of its own (romania t17, paydaytheheist t03, destiny t08, fivenightsatfreddys t14, trees t12), none by the level rule.

## J's ruling on also_present (09:09 Berlin) and QB4-002

J's ruling of 09:09 Berlin, through the PI: "rule (1) extends to also_present. also_present lists only themes that a reader or your B1 named." QB4-002, answered at 09:20 Berlin: "yes. A theme a reader listed under its own also_present counts as named by that reader. also_present may list themes a reader placed, a reader listed under its own also_present, or your B1 named; nothing else." At B4a-05, `b4_ap_scan.py` found 128 lines in packets 1 to 4 listing 273 themes outside that set; each was corrected through `--replace`, and four bags that lost every theme at the three-concept floor were re-ruled by hand (archlinux t01, ireland t04, starvstheforcesofevil t02, de t02).

## QB4-003: named themes in the bag test, and the revisit

I asked J during packet 6 (QB4-003) whether a theme a reader listed under its own `also_present`, and that no placement holds, counts in the bag test. J answered at 11:29 Berlin: "count them. Themes a reader listed under its own also_present count in the bag test. Apply it to packet 6 and to the 43 rulings in packets 1 to 5 that out/_analysis/b4_bag_named_check.py lists, keeping the superseded ledger."

The test, as applied from packet 6's item 126 and throughout packet 7:
- **The themes counted** are the placed themes and every theme a reader listed under its own `also_present`.
- **A named theme's concepts of its own** are the item's concepts its `must_show` takes that no placed theme in the ruling already holds. The concepts a reader listed are read against the test, not taken on trust.
- **Four themes or more with three concepts of their own make a bag.** The bag places the largest act a placement holds (on a tie, the one with more placements) and lists every other counted theme with three concepts or more under `also_present`, twenty at most.
- **A placed theme with three concepts or more is never cut by the limit of three.** If a fourth reaches three, the item is a bag.

The revisit at B4a-06: the 64 lines the check listed in packets 1 to 6 were read; 45 became bags and 19 were kept. Four slips outside the list also became bags (utaustin t05, japan t05, loliconsunite t02, lebanon t02), and chibears t10 gained reader A's T3-050. The bags re-ruled then, by packet: packet 1 starcraft t03; packet 3 AvoArmy t01; packet 4 warriors t06; packet 5 TheFarLeftSide t04, wallstreetbets t06, india t08, croatia t04, cirkeltrek t08, AmericanFlaginPlace t08, osugame t07, europe t07, AMD t13, aoe2 t06, factorio t10, formula1 t10, kanye t06, masseffect t05, prequelmemes t08, heroesofthestorm t10, placeDE t04, quebec t04, toolband t09, czech t07, titanfall t07, india t04, mylittlepony t07, OnePiece t03, radiohead t04, theblackvoid t02, theitalyplace t11; packet 6 fivenightsatfreddys t08, philippines t08, suomi t10, turkey t06, rocketleague t05, cfb t02, denmark t05, frankocean t05, chibears t10, EraseThePlace t06, starcitizen t11, TransFlagPlace t05, elitedangerous t07, eagles t06. 26 older bags in packets 1 to 5 could list more named themes; J named only the 43, and they are carried open.

In packet 7 the check flags eight lines (would be a bag: europe t20, starcraft t11, formula1 t13, leafs t05, rickandmorty t08; bag could list: thebluecorner t09, philippines t11, brasil t09). Each why already weighs the named themes against their tests; once concepts held by placed themes or failing the test are set aside, each holds two concepts of its own or fewer. No ruling changed.

## J's answer on lone B1 themes, and the rule chosen

At B4a-05 I wrote a doubt: rule 0 inside the placements kept a one- or two-concept theme only my B1 placed even against two agreeing readers, so class 4 turned toward my B1. The PI put three options to J: (1) leave it, my B1 a full placement; (2) a theme only my B1 placed beats two agreeing readers only with three concepts or more of its own; (3) where both readers agree, their list stands and my B1 is a note. J answered at 12:28 Berlin: "Whatever the agent feels more comfortable with. They can also adapt the code definition if needed".

I chose option (2), with a condition:
- **The rule.** In class 4, a theme only my B1 placed stands against the two agreeing readers only with three concepts or more of its own. With fewer it is left out and named in the why.
- **The condition.** The readers' list then stands where its test takes concepts. Where my reading finds it takes none, the item is unresolved: no one-concept theme of mine is put in its place.
- **Class 3 is unchanged.** There the readers disagree and my B1 is the third placement; the level rule decides.

Why. Two independent readers agreeing is the case where my B1 carries the author's pull most. Three concepts is the scheme's own floor for a theme of its own (the bag rule and `also_present`). Option (3) would make the adjudication measure obedience, and would force a readers' theme whose test takes nothing.

At B4a-06 the rule changed 130 class 4 rulings in packets 1 to 6 (author-error 83, author-disagrees 40, scheme-ambiguous 7; unresolved 30). Packet 7 was ruled under it from the first item: of its 118 class 4 items, a B1 theme with three concepts or more stood in 18, the readers' list was taken in 91, and 9 are unresolved.

## author-error and author-disagrees

author-error: 571 (packet 1 99, packet 2 78, packet 3 78, packet 4 86, packet 5 58, packet 6 83, packet 7 89). author-disagrees: 208 (36, 45, 21, 13, 20, 51, 22). Both come almost wholly from class 4, where the readers agreed on a list my B1 grouping did not hold, and from class 5, where my B1 left the theme unplaced.

The next list gives, by packet, the class 4 items counted by what the ruling holds, whatever their taxonomy value:
- **Packet 1:** the readers' list taken 97, a B1 theme kept 21, an empty ruling 34, other 1.
- **Packet 2:** the readers' list 81, a B1 theme kept 26, empty 13, other 4.
- **Packet 3:** the readers' list 83, a B1 theme kept 29, empty 2, other 3.
- **Packet 4:** the readers' list 83, a B1 theme kept 15, empty 2, other 5.
- **Packet 5:** the readers' list 62, a B1 theme kept 21, empty 3.
- **Packet 6:** the readers' list 87, a B1 theme kept 32, empty 15.
- **Packet 7:** the readers' list 91 (3 of them bags), a B1 theme kept 18 (1 a bag), empty 9.

Over the seven packets the readers' list was taken in 584 class 4 items and a B1 theme kept in 162, each with three concepts or more; 78 are unresolved and 13 hold another shape. Two labels from earlier packets do not match the measure and are carried as they stand: 12 packet 4 author-error rulings from items 401 to 461 that keep a B1 theme beside the readers' list, and two packet 2 author-disagrees rulings that take the readers' list.

I cannot separate how much of each packet's split is the scheme and how much is my pull toward my own grouping. The blind sample at B4b tests the adjudicated stratum against fresh readers.

My commonest B1 errors:
- **Packet 1:** T3-031 placed on an in-joke with no canvas in it; T3-001 where nothing was posted as true; T3-063 on posts that are not canvas posts.
- **Packet 2:** calls for hands my B1 had placed as the proposal, the progress or a further piece; placing troubles (T3-074); templates my B1 had placed as one plan imposed (T3-091).
- **Packet 3:** links that only show where the finished mark is (T3-026); the readers' T3-004, T3-033 and T3-020.
- **Packet 4:** the readers' T3-005, T3-170, T3-021, T3-088 and T3-087.
- **Packet 5:** the readers' T3-006, T3-010, T3-068, T3-084, T3-151 and T3-137.
- **Packet 6:** the readers' T3-031 (19), T3-018 (10), T3-016 (6) and T3-065 (5); my B1 had read G20's talk as remarks on neighbours (T3-052).
- **Packet 7:** the readers placed T3-043 (20), T3-117 (14), T3-073 (12), T3-037 (9), T3-009 (7) and T3-157 (6) where my B1 did not. My B1 had read the aftermath as one act per theme: a celebration with no credit, an account with no end registered. Where my B1 gave one theme, the readers often saw two acts, each with concepts of its own.

The themes of mine kept against both readers in packet 7's author-disagrees rulings, each with three concepts or more, include: T3-003 (minecraft t21, eleven parts claimed with no placement holding T3-043; uwaterloo t12), T3-017 (fivenightsatfreddys t14 and trees t12, theme and header art the words never tie to the canvas), T3-087 and T3-005 (overwatch t14: who was behind the damage, and alarms calling the room to the fight), T3-052 (destiny t08: Kekistan, which the words make another room's work), T3-031 and T3-080 (philippines t12: the teasing of a late builder, and the upside-down flag's meaning argued), T3-014 (Temple t08), T3-009 (Rainbow6 t16) and T3-037 (chess t13).

## Fields by ambiguity

The next list counts the 451 scheme-ambiguous rulings by the field whose sentence failed, with packets 1 to 7 in brackets.

- must_show: 252 (76, 33, 51, 34, 2, 31, 25)
- discriminators: 114 (39, 17, 16, 2, 4, 32, 4)
- must_not_show: 57 (2, 6, 24, 8, 8, 8, 1)
- decide_when_both: 28 (4, 6, 3, 15, 0, 0, 0)

Packet 7's failures are almost all `must_show` sentences that do not say whose work, whose picture or which room's feeling they mean.

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, over the seven packets. Stage C1 opens with it.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-017 | 55 | 6 | 1 | 1 | 47 |
| T3-033 | 34 | 31 | 2 | 0 | 1 |
| T3-001 | 32 | 18 | 0 | 0 | 14 |
| T3-023 | 26 | 24 | 0 | 0 | 2 |
| T3-004 | 26 | 4 | 14 | 0 | 8 |
| T3-002 | 14 | 1 | 2 | 3 | 8 |
| T3-038 | 13 | 10 | 2 | 0 | 1 |
| T3-005 | 13 | 5 | 0 | 7 | 1 |
| T3-063 | 9 | 7 | 1 | 0 | 1 |
| T3-021 | 9 | 5 | 4 | 0 | 0 |
| T3-073 | 9 | 9 | 0 | 0 | 0 |
| T3-020 | 9 | 0 | 8 | 0 | 1 |

93 more themes failed on 202 rulings between them.

The sentences that failed most:
- **T3-017's discriminator** "Is it the room's running in-joke carried into the canvas talk or the day (T3-031), or the sub's ordinary subject going on (T3-017)?" (47: packet 1 23, packet 6 24). "or the day" contradicts T3-031's own `must_show`, "The room's own humour carried into canvas talk". Readers place a joke with no canvas in it under T3-031 by the discriminator, and under T3-017 by T3-031's test. The canvas-condition paragraph rules for T3-031's test, so every such item is scheme-ambiguous on this sentence. Packet 6: canucks t13, eder t01, edmontonoilers t12, ibo t03, ibo t05, india t14, paladins t04, paladins t26, planetside t02, totallynotrobots t15, zootopia t16, lego t04, survivor t04, chicago t08, empiredidnothingwrong t19, flashtv t12, kpop t09, oneshot t11, puzzleanddragons t07, starlightstage t08, wholesomememes t23, croatia t07, 4chan t22, futurama t14.
- **T3-001's discriminator** "Is the joke a fake posted as true for April Fools (T3-001), or the room's ordinary in-jokes and memes on any day (T3-031)?" (14: packet 1 6, packet 6 8). The same contradiction from T3-001's side.
- **T3-033's `must_show`** "An idea of what the room should put on the canvas, offered to the room" (31). It does not say "first"; T3-041's `must_not_show` gives the first mark to T3-033 (conflict CC-019).
- **T3-023's** "A change made to a whole sub for April Fools" (24). It does not say whether another sub's change counts.
- **The homeland flag in the siblings' `must_not_show` lines** (T3-004 14, T3-020 8, and others). T3-065's `must_show` takes the flag's build, spot, size, repair and calls for hands; no sibling's `must_not_show` says so.
- **T3-018's `must_show`** "whose character a figure is" (packet 6, 5). It reaches a bare name given to a neighbour's figure, which T3-052 also takes, and a mock reading kept up as a joke, which T3-031 takes.
- **T3-052's `must_show`** "Pictures around the room's mark noticed" (packet 6 4, packet 7 4). It presumes the room has a mark of its own and does not say whose picture a remarked picture is. Packet 7: drugs t16, norge t09, polska t11 and linux t13, each unresolved because the words do not say whose picture it is or that it sits beside the room's mark.
- **T3-009's `must_show`** "the work said to have lasted to the end" (packet 7, 3), against T3-073's "what survived". A plain statement that the work survived meets both; where a ruling turns on it, the item is scheme-ambiguous (dragonquest t08, gameboy t07). anime_irl t20 is unresolved: the words do not say the room made the pictures it marks.
- **T3-164's `must_show`** "Support or visibility felt through the canvas" (packet 7, 3). It does not say whether the room's attachment to its flag (AcePlace t13), a creed read into its mark (TreePlace t02) or a bare title of solidarity whose poster is not known (rojava t03) belongs; all three are unresolved.
- **T3-086's `must_show`** against T3-050's discriminator (a school rivalry is both); **T3-005's `decide_when_both`** (names no tie); **T3-073's `must_show`** against T3-005's "alarms"; **T3-027's `decide_when_both`**; **T3-006's discriminator** against T3-061 (packets 4 to 6).

Single failures and readings for stage C1's list, from packet 7:
- **T3-003's discriminator against T3-043** speaks only of crediting others, while T3-043's discriminator against T3-003 sends parts claimed after the work to T3-043. I followed T3-043's sentence where a placement held T3-043 (SquareSpiral t13, azores t01, prequelmemes t10, romania t17, patriots t17, pathofexile t20) and T3-003's where none did (minecraft t21, bindingofisaac t13, anarcho_capitalism t13). The two sentences should say the same thing.
- **"The work" in T3-073 and T3-058** is not said to be the room's own. I read it so: rivals' results are not T3-073's (uvic t04, destiny t08), and blame for another room's loss is not T3-058's (pathofexile t17, hungary t07).
- **T3-054's `must_show`** "the work rebuilt on a clone site" against T3-038's progress and T3-002's calls: no field says which theme takes calls and progress on a later canvas (twice t18 scheme-ambiguous; catholicism t09).
- **T3-111's `must_show`** "The canvas sub's or chat's future" does not reach a standing community's new project after the canvas (forsen t11, a song made by the community; paladins t21, unresolved).
- **T3-087's discriminator against T3-058** sends a culprit named after the close to T3-058, whose `must_show` takes only "a named room or group"; one person traced after the close has no theme (philippines t10).
- **T3-117's `must_show`** "regret at the end" does not say whether a late reader's regret at having missed the event, or a question about what the end will do to a work, registers it (corridor t12, unresolved; telegram t06).
- **T3-021's `must_show`** "cleaning stray ones" does not say whether cleaning a copy after the lock is upkeep or a record (TheFarLeftSide t19); I counted cleaned copies toward T3-105 throughout packet 7.
- **T3-037's `must_show`** "the canvas weighed as a whole" (AMD t22, the room's own effort judged; shitredditsays t06, why some works survive, unresolved).
- **T3-154's `must_show`** "implied rivals" (zootopia t10, kindred subs absent from the canvas); **T3-044's** newcomers (xenoblade t07, a helper from another room drawn to the game); **T3-156's discriminator against T3-031** (osu t10, a canvas-born joke turned on a rival); **T3-038's discriminator against T3-009** (oman t06, a finish reported plainly, unresolved); **T3-131's `must_show`** (thesimpsons t06, a sale offered with no argument, unresolved); **T3-017's `must_not_show`** (weezer t16, an exchange begun on the canvas and carried on in the sub's subject, unresolved); **T3-127's `must_show`** (metalcore t14, unresolved); **T3-011's `must_show`** and **T3-029's discriminator against T3-183** (anarchism t22 and opticgaming t12, whose work it was not said, unresolved); **T3-082's `must_show`** (nlsscirclejerk t07, what was found not said, unresolved); **T3-063's `must_show`** (touhou t17, the rules applied to a post that is not a canvas post, the gap of CC-004, unresolved).

The single failures from packets 3 to 6 are in this report's B4a-05 and B4a-06 versions and in the ledger.

## The named_neither rate

named_neither: 757 of 3,288 (23.0%). Packet 1: 47 of 491 (9.6%). Packet 2: 89 of 447 (19.9%). Packet 3: 146 of 500 (29.2%). Packet 4: 118 of 461 (25.6%). Packet 5: 104 of 409 (25.4%). Packet 6: 145 of 500 (29.0%). Packet 7: 108 of 480 (22.5%).

Every named_neither ruling keeps a theme from my B1 grouping that neither reader placed; none holds a theme no placement held. 131 of the 757 are author-disagrees. The next list splits them by packet:
- **The primary itself chosen by neither reader:** packet 1 20, packet 2 24, packet 3 49, packet 4 16, packet 5 25, packet 6 54, packet 7 21.
- **How many themes the ruling places** (one, two, three): packet 1 17, 17, 13; packet 2 9, 40, 40; packet 3 18, 42, 86; packet 4 6, 32, 80; packet 5 12, 18, 74; packet 6 21, 53, 71; packet 7 6, 25, 77.
- **The B1 themes kept most often:** packet 1 T3-017 15, T3-048 6, T3-023 6; packet 2 T3-069 8, T3-041 8, T3-038 6; packet 3 T3-041 14, T3-113 10, T3-070 9; packet 4 T3-042 9, T3-087 7, T3-170 7; packet 5 T3-150 11, T3-151 8, T3-061 7; packet 6 T3-010 13, T3-017 9, T3-149 5, T3-130 5; packet 7 T3-157 11, T3-105 10, T3-072 8, T3-073 7, T3-043 7.

My reading of it. named_neither measures my B1 grouping kept against both readers, mostly in class 3, where my B1 is the third placement and the level rule keeps a theme of mine alone at its level. In packet 7, 77 of the 108 rulings place three themes: my B1 adds a third act (what working together meant, a record kept, an ally thanked) beside the two the readers split on. In class 4 every kept theme of mine has three concepts of its own. The blind sample's adjudicated stratum will show whether strangers reach these rulings.

## The unresolved count

unresolved: 185 of 3,288 (5.6%). Packet 1: 66. Packet 2: 19. Packet 3: 9. Packet 4: 12. Packet 5: 6. Packet 6: 49. Packet 7: 24.

Packet 7, by the reason the scheme did not decide:
- **A bare title or image link that shows no act** (author-disagrees, class 5), 5: Summit1G t03, survivor t01, quebec t17, rangers t15, placehearts t14.
- **The words do not say whose work, whose picture or who speaks**, 8: drugs t16, norge t09, polska t11 and linux t13 (T3-052's `must_show`), anarchism t22 (T3-011's), opticgaming t12 (T3-029's discriminator against T3-183), metalcore t14 (T3-127's), rojava t03 (T3-164's).
- **An act the scheme names nowhere**, 7: thesimpsons t06 (a sale offered with no argument), weezer t16 (an exchange begun on the canvas and carried on in the sub's subject), shitredditsays t06 (why some works survive), corridor t12 (a late reader's regret), paladins t21 (a standing sub's new aim), TreePlace t02 (a creed read into the room's own mark), AcePlace t13 (attachment to the flag).
- **The words do not say what was found or done**, 3: nlsscirclejerk t07 (T3-082), anime_irl t20 (T3-009), oman t06 (a finish reported plainly, T3-038's discriminator).
- **The sub's rules applied to a post that is not a canvas post**, 1: touhou t17 (T3-063's `must_show`, the gap of CC-004).

Packet 6 by reason, and the lone-B1 additions of packets 1 to 6, are in this report's B4a-06 version. The main reasons over all packets: a bare title or pointer with no act (class 5); April Fools play not posted as true; another sub's April Fools change; moderators applying standing rules to non-canvas posts (CC-004); a room joke with no canvas in the words; the attack, its target or its culprit not shown; and, in packet 7, whose work or picture it is.

## The boundary rulings

Each pair is one paragraph in `boundaries.md`. Each paragraph's ruling is summarised here with its item list. Every paragraph applies under J's rulings: it sends a concept to its theme only where a placement holds that theme. The item lists of packets 1 to 5 are as written at B4a-05; the re-rules of B4a-06 kept each line's `boundary_ruling`.

### Packet 1

**T3-001|T3-023, the joke's stage (32 items).** A change to the sub's name, look, rules or subject made by its moderators, or by members flooding it "as a sub acting together", is T3-023. Members' own false claims in an unchanged sub are T3-001. Both, each with concepts of their own: the larger primary. Items: aceattorney t01, MMA t02, nlsscirclejerk t08, rit t02, totallynotrobots t06, totallynotrobots t08, AceOfAngels8 t01, clashroyale t03, enterthegungeon t02, flyers t05, furry t09, harrypotter t06, kilian t08, mylittlepony t08, porterrobinson t08, porterrobinson t09, ss13 t01, teslamotors t01, toolband t02, totallynotrobots t02, totallynotrobots t03, totallynotrobots t04, totallynotrobots t07, OneTrueEmilia t01, apocalypserising t01, formula1 t02, greece t07, polska t03, thetreesnetwork t02, totallynotrobots t01, ubc t02, zootopia t01.

**T3-001|T3-048, whose joke (20 items).** The source shown in the concepts decides. Where it cannot be read, the ruling is unresolved. A member relaying an organisation's joke is T3-048 by the discriminator (conflict CC-002). Items: btc t04, bitcoin t06, feedthebeast t02, opticgaming t01, uofmn t01, baylor t02, GuildWars2 t01, GuildWars2 t10, runescape t07, rutgers t01, starlightstage t03, warframe t15, yugioh t10, yugioh t11, danganronpa t19, falcons t10, kamenrider t07, lego t07, simonfraser t02, ubreddit t02.

**T3-017|T3-031, the canvas condition (15 items, with T3-001|T3-031: rwby t03).** T3-031's own test governs: an in-joke with no canvas in it is T3-017. Every item is scheme-ambiguous on T3-017's discriminator. Items: cubers t30, ethereum t06, falcons t08, flashtv t04, freedomplanet t05, h3h3productions t06, h3h3productions t12, heyyea t07, indieheads t06, mls t07, PlaceNL t20, romania t22, SydneyFC t03, tf2 t09, torontoraptors t03.

**T3-001|T3-095, who staged the claim (8 items).** A test of a member's own fake is T3-001; a test of anyone else's claim is T3-095. Items: linux t04, planetside t01, romania t12, swordartonline t03, thesimpsons t02, worldoftanks t02, fivenightsatfreddys t03, hearthstone t01.

**T3-023|T3-095, playing inside or working out (7 items).** Items: paragon t08, hawks t07, smashbros t01, criticalrole t02, ElderScrolls t01, h3h3productions t23, transformers t01.

**T3-048|T3-095, open or known (6 items).** Items: clg t08, gameofthrones t09, paladins t01, thesilphroad t02, btc t01, loltyler1 t01.

**T3-032|T3-097, the jokes or the look (5 items).** Items: anime_irl t16, anime_irl t17, hunterxhunter t03, pcmasterrace t02, survivor t10.

**T3-063|T3-185, applied or made (5 items).** Items: anime_irl t05, destiny t06, ss13 t11, russia t12, leafs t12.

**T3-001|T3-017 (4 items):** ohio t01, homelab t03, planetside t05, titanfall t03. **T3-015|T3-063 (4):** fireemblem t08, futanari t06, serbia t15, stardustcrusaders t21. **T3-023|T3-051, upvote bargains (4; CC-007):** partyparrot t16, titanfall t05, warframe t06, warriors t04. **T3-031|T3-048 (3) and T3-023|T3-031 (1):** GuildWars2 t02, GuildWars2 t05, rocketleague t15; stardustcrusaders t10. **Single items:** T3-001|T3-051, rit t01; T3-023|T3-100 (playing inside the change or asking to keep it after the day), wallstreetbets t03; redhotchilipeppers t04 and 4chan t12 on pairs met once.

### Packet 2

**T3-002|T3-033, a call or a new mark (20 items).** A concept naming a new mark for the room counts toward T3-033, even when it also asks for help. A call to a mark already named counts toward T3-002. A tie goes to T3-002 when the mark was already chosen, and to T3-033 when it was not. Items: androidgaming t01, anime t01, chicago t01, clashroyale t02, criticalrole t03, drumcorps t05, nascar t06, onepunchman t01, polyamory t01, rutgers t03, seahawks t01, TheAdventuresofTintin t01, twentyonepilots t02, chess t07, nlsscirclejerk t01, nonbinary t01, opticgaming t03, uiowa t01, gameattack t03, bigbang t01.

**T3-002|T3-038, a call or the work's progress (19 items).** Calls, volunteers and answers count toward T3-002; placing and reports of the work's state toward T3-038. Items: auburn t01, bindingofisaac t02, dallasstars t05, ghibli t01, gorillaz t03, newzealand t07, shrooms t06, streetfighter t04, transformers t02, bangtan t01, battlecats t05, cloud9 t03, FinalFantasy t02, foxstevenson t02, torontoraptors t04, traaaaaaannnnnnnnnns t01, rutgers t05, smashbros t04, xenoblade_chronicles t02.

**T3-014|T3-153, the room's own chat or a meeting place (18 items).** Another room must be in the chat in the words. Items: armenia t08, bangtan t04, belgium t03, dmt t03, eve t10, FederationPlace t06, giivasunner t12, GreenCorner t02, metalgearsolid t08, ohio t08, paladins t25, placehearts t06, rocketbeans t04, theitalyplace t07, AcePlace t06, aoe2 t07, araragi t03, iceland t05.

**T3-002|T3-070, a call or directions (13 items).** Items: bardmains t01, danganronpa t03, dankmemes t15, python t06, witcher t01, clg t01, harrypotter t15, cowchop t01, mysterydungeon t01, paragon t01, shield t01, Moondye7 t02, seventeen t01.

**T3-002|T3-005, a rally or a defence (12 items in packet 2; 3 more in packet 4).** The attack must be in the words. A call to "protect" a mark with no attacker in view is T3-002 where a placement holds T3-002; where none does, the call counts toward T3-005, whose `must_show` names "calls to defend". Packet 2 items: btc t02, Clannad t02, crusaderkings t01, FlaggyFlag t02, harrypotter t01, monalisaclan t02, ohio t03, czech t01, malta t02, nin t10, thetreesnetwork t01, prequelmemes t02. Packet 4 items: masseffect t01, sooners t08, anarcho_capitalism t04.

**T3-070|T3-091, directions or one plan (7 items; CC-012):** stlouisblues t01, FloydVsVoid t02, heyyea t01, starryknights t02, ChronoTrigger t02, mylittlepony t04, PlaceNL t01. **T3-004|T3-070, the design or its directions (6 items):** berserk t06, foxstevenson t03, nyu t01, pitt t02, muse t02, suomi t06.

### Packet 3

**T3-033|T3-041, the first mark or a further piece (25 items; CC-019).** A proposal counts toward T3-041 when the room's mark already stands or is chosen. Items: truestl t02, cmu t01, metalgearsolid t04, muse t01, aoe2 t04, denmark t10, eagles t02, eve t03, gameofthrones t02, indieheads t13, KState t01, math t02, nuclearthrone t01, portal t02, purplecorner t03, rust t09, simonfraser t04, splatoon t03, suomi t02, touhou t08, ufl t01, blackmirror t05, borderlands t04, empiredidnothingwrong t11, winnipegjets t11.

**T3-038|T3-041, the first build or a further piece's (16 items).** Items: sakuragakuin t01, jerma985 t03, nuclearthrone t05, bobross t01, cavestory t01, dota2 t11, madokamagica t01, msu t02, parahumans t01, touhou t02, AyyMD t01, cubers t21, cubers t25, samuraijack t10, suomi t27, yumenikki t01.

**T3-004|T3-041, the look or an addition (14 items).** Items: ubreddit t03, ElderScrolls t05, funhaus t01, nin t03, radiohead t01, skyrim t02, bindingofisaac t03, DatBoi t04, factorio t09, placetardis t02, ProfessorLayton t02, starlightstage t12, borderlands t02, enterthegungeon t03.

**T3-004|T3-169 (8 items; CC-022):** bisexual t03, greyblob t02, monstercat t06, unturned t09, drawhelix t05, farmcarrots t08, neopets t14, wine t08. **T3-004|T3-038 (8):** portal t01, timbers t02, AvoArmy t01, calgaryflames t01, uoft t08, bitcoin t02, detroitlions t04, paydaytheheist t02. **T3-038|T3-070 (7):** berkeley t03, gameattack t04, virginiatech t03, planetside t08, bdsm t01, re_zero t06, formula1 t06. **T3-004|T3-020 (7):** blackmirror t02, borussiadortmund t03, minecraft t04, kingdomhearts t12, oneshot t01, nightinthewoods t02, utaustin t01. **T3-004|T3-033 (6):** frc t01, nlsscirclejerk t02, WPI t01, redhotchilipeppers t03, starlightstage t09, yugioh t04. **T3-020|T3-033 (1):** tetris t01.

**Carried from packet 2 into packet 3.** T3-002|T3-033 (10 items): chicubs t09, DiamondClub t01, foxes t01, hawks t05, kanye t01, schoolidolfestival t04, stardustcrusaders t01, unturned t03, wallstreetbets t01, warframe t01. T3-002|T3-038 (9 items): bostonbruins t02, enterthegungeon t01, ethoslab t01, forsen t01, habs t02, nyjets t04, the_pack t01, winnipegjets t01, wow t17. T3-004|T3-070 (9 items): crusaderkings t02, penguins t03, udub t01, drumcorps t06, kanye t05, Okami t06, pebble t04, placesnek t04, portal t03.

Readings written during packet 3: the homeland flag's look (T3-065, emblems T3-113); a design cut down to the hands (T3-004; T3-069 only when a piece is dropped for another; T3-042 when growth is set aside); a celebration while placement goes on (T3-009 for "done" celebrated, T3-026 for "up" or "for now").

### Packet 4

**T3-005|T3-021, a fight or upkeep (90 items; B2's predicted pair 1; conflict CC-026).** Ruled as written by the discriminator and T3-005's `decide_when_both`. A concept counts toward T3-005 when an attack on the room's work is in the words and the room answers it as a fight; toward T3-021 when it watches or fixes, "with or without an attacker in view, where no fight is called". Naming who did it goes to T3-087, a watch through the night to T3-141 (CC-032), a script that repairs to T3-028 (CC-028), upkeep argued over growth to T3-042 (CC-027). Where count and placements both tie, the item is scheme-ambiguous on T3-005's `decide_when_both`, which names no tie, and both themes are placed. Items: aggies t03, aoe2 t05, archlinux t04, austria t05, bangtan t06, bostonbruins t06, clg t04, cubers t10, earthbound t04, factorio t07, flashtv t09, frankocean t10, furry_irl t12, gorillaz t06, gravityfalls t02, GreenCorner t03, hellointernet t02, HomestarRunner t03, homestuck t04, india t13, leafs t02, leagueoflegends t16, malaysia t04, mindcrack t02, nyjets t08, palestine t04, parrots t09, Peru t07, PinkVomitMonster t02, placestart t14, placetardis t03, portal t07, PORTUGALCARALHO t02, reddevils t15, rocketbeans t05, roosterteeth t04, serbia t08, shield t03, smite t06, ss13 t06, stardewvalley t03, taiwan t05, tf2 t12, TheFarLeftSide t03, theitalyplace t01, TransFlagPlace t03, warriors t08, afip t04, androidgaming t03, cavestory t02, chile t03, ChronoTrigger t03, clubpenguin t09, daftpunk t05, FinalFantasy t05, gameofthrones t14, israel t02, jerma985 t04, korea t09, metroid t09, MonkeyIsland t03, muse t05, necrodancer t05, oneshot t04, pakistan t05, partyparrot t02, placeportalpattern t06, ScottPilgrim t03, simonfraser t09, stlouisblues t08, tagpro t03, tampabaylightning t03, TeamDignitas t04, texas t02, redhotchilipeppers t08, anaheimducks t09, animalcrossing t04, AyyMD t02, cloud9 t07, DestinyTheGame t08, dragonquest t02, feedthebeast t07, kingdomhearts t20, placeDE t03, sheffield t02, starcraft t07, tf2 t11, theexpanse t05, thenetherlands t04, touhou t04.

**T3-005|T3-073, an alarm or a report (7 items).** A report addressed to the room so that it acts counts toward T3-005; a report of what changed, survived or was lost, with no call to fight, toward T3-073. Items: apocalypserising t05, terraria t08, 4chan t08, anime t11, bakchodi t06, neutralmilkhotel t03, texastech t03.

**T3-021|T3-038, first build or restored (3 items; CC-017).** The same spot rebuilt after a loss is T3-021; a rebuild at a new spot is T3-022. Items: nerf t02, pitt t03, telegram t03.

**T3-005|T3-038 (5 items split; none tagged).** Placing the first build counts toward T3-038; an attack answered as a fight toward T3-005.

**T3-020|T3-022, the first spot or a move after a loss (5 items; CC-033).** A spot found, tested or changed before the mark stands counts toward T3-020; a move or restart after the work was destroyed, overpowered or crowded out toward T3-022. Items: mordhau t04, rutgers t04, toolband t04, dallasstars t13, detroitredwings t04.

**T3-027|T3-028, arguing scripts or running them (4 items; CC-029).** Each concept counts toward the act it does, and the larger part leads; a tie goes by placements. Items: pakistan t08, giantbomb t07, placecanada t12, placeDE t07.

**T3-027|T3-087, a bot claim or a culprit traced (4 items).** Bots or new and empty accounts named as the source of damage while placement goes on count toward T3-087; bots judged unfair toward T3-027. Items: shitredditsays t05, sooners t10, tampabaylightning t15, foxes t04.

**T3-089|T3-168, a stale script or a neighbour spared (2 items).** A call to stop or change the room's scripts so a neighbour's work stands counts toward T3-168. Items: afip t05, malaysia t05.

**T3-005|T3-006 (CC-031)** and **T3-058|T3-073 (CC-034)** reached four items and were decided by their discriminators as met. One item carries T3-005|T3-006: rocketbeans t07.

### Packet 5

**T3-010|T3-149, a border or a truce (34 items; B2's predicted pair 2; conflict CC-037).** A concept counts toward T3-149 when a fight, an attack or a threat between the rooms is in the words, or the deal is named peace, truce, ceasefire or non-aggression; toward T3-010 when lines, overlaps, moves or shared space are settled and no fight or peace is named. Items: Thegreatblackhole t06, AMD t13, archlinux t03, bindingofisaac t05, detroitlions t06, edboxes t04, faeria t04, FederationPlace t04, finland t02, forsen t03, gravityfalls t05, liverpoolfc t14, newzealand t05, phish t04, placeportalpattern t04, prequelmemes t08, singapore t08, ss13 t09, switzerland t03, teslamotors t10, uiuc t11, uoft t10, worldoftanks t07, cowchop t02, buffalo t04, czech t07, neopets t04, overwatch t19, placesnek t03, soylent t02, sweden t03, titanfall t07, VelvetUnderground t04, colombia t03.

**T3-010|T3-151, a border or help traded (31 items; B2's predicted pair 11; CC-037).** Help offered or asked in return for help or for room counts toward T3-151; a line, overlap or move agreed with no help in the exchange toward T3-010. Help counts toward T3-151 only when the words name the return. Items: belgium t11, catalunya t05, chicago t10, chicubs t05, chile t04, Dorset t02, ElSalvador t02, europe t03, factorio t10, ftlgame t03, gameofthrones t13, hearthstone t13, kamenrider t04, littlewitchacademia t05, mls t10, Moondye7 t05, notredame t04, placestart t08, purdue t06, rwby t07, smashbros t08, timbers t03, unturned t05, uwaterloo t07, giivasunner t10, httyd t10, india t04, mylittlepony t07, placecanada t05, southafrica t04, theitalyplace t11.

**T3-010|T3-024, a line agreed or work spared (26 items; B2's predicted pair 13; CC-038).** A concept counts toward T3-010 when the neighbour is in the exchange in the words; toward T3-024 when the room spares the work with no neighbour's word in it. Items: 49ers t05, cirkeltrek t08, geometrydash t08, monsterhunter t04, PurplePixels t05, starcraft t10, TeamYellowPlace t02, asktransgender t03, python t08, aceattorney t09, armenia t04, bisexual t05, czech t06, esperanto t06, GrowTheTree t03, oneshot t03, PlaceNL t07, starbound t04, terraria t03, TransFlagPlace t02, babymetal t05, Fez t06, roosterteeth t05, stardustcrusaders t06, taiwan t06, theexpanse t04.

**T3-006|T3-061, destroying the rival's work or taking its space (18 items; CC-039).** Erase, destroy, ruin, black out, sabotage: T3-006. Expand into, take over for the room's flag, claim territory: T3-061. A bare call to "invade" or "attack" a named neighbour, with no space claimed and no damage named, counts toward T3-006. Items: borderlands t05, armenia t05, brasil t05, cirkeltrek t07, ireland t06, newzealand t04, overwatch t25, ukraine t03, utaustin t03, wallstreetbets t06, costa_rica t03, kurdistan t02, polska t05, purdue t08, stlouis t04, thailand t06, PlaceNL t06, teamcube t02.

**T3-010|T3-011, a border or help sent (14 items; CC-037 and CC-043).** Pixels sent to a neighbour's work with nothing asked in return count toward T3-011; lines, overlaps, moves and shared space settled toward T3-010. Items: sonicthehedgehog t04, cloud9 t09, formula1 t10, masseffect t05, minnesotavikings t12, pathofexile t11, samuraijack t03, sixers t06, transformers t06, Clannad t05, heroesofthestorm t10, nyjets t11, placeDE t04, quebec t04.

Readings applied in packet 5: T3-010's "with no fight to end" fails for a concept naming a fight, a threat, peace or a truce; a request for help is T3-084 by T3-011's `must_not_show`; help counts toward T3-151 only when the return is named; a request for space to the room that holds it is T3-035, a host ruling on many requests T3-162, a single grant T3-012; T3-079 needs national flags, T3-149 rooms already in contact, T3-078 kin felt in the words, T3-099 the bigger room's size in the words.

### Packet 6

`b4_packet_pairs.py --packet 6`: eight pairs split the readings' primaries on five items or more, and were ruled before the packet's first item. The item lists are the packet 6 items that carry the pair in `boundary_ruling`.

**T3-010|T3-149, a border or a truce (28 items; B2's predicted pair 2; conflicts CC-037 and CC-052).** Ruled as in packet 5: a fight, an attack or a threat between the rooms in the words, or a deal named peace, truce, ceasefire or non-aggression, counts toward T3-149; lines, overlaps, moves or shared space settled with none of these counts toward T3-010. The larger part leads. Items: adventuretime t06, clashroyale t07, cubers t07, denverbroncos t08, DestinyTheGame t09, empiredidnothingwrong t13, fivenightsatfreddys t08, Goodboye t02, mcgill t06, ockytop t05, philippines t08, suomi t10, thesimpsons t10, twice t16, weezer t06, ainbowroad t05, anarcho_capitalism t12, berkeley t05, cfb t02, denmark t05, frankocean t05, hatsune t03, kilian t06, lebanon t04, theitalyplace t02, AprilKnights t04, smite t08, thailand t08.

**T3-017|T3-031, ordinary talk or the room's joke around the canvas (24 items; CC-049).** Ruled as packet 1 ruled the pair: T3-031's own `must_show` governs. A running joke, catchphrase, meme or fandom wordplay played around the canvas work counts toward T3-031; the sub's ordinary subject going on, or a joke with no canvas in it, counts toward T3-017, which is placed beside another theme only with three concepts of its own. Items decided on the canvas condition are scheme-ambiguous on T3-017's discriminator. Items: canucks t13, eder t01, edmontonoilers t12, ibo t03, ibo t05, india t14, paladins t04, paladins t26, planetside t02, purdue t16, totallynotrobots t15, zootopia t16, lego t04, chicago t08, empiredidnothingwrong t19, flashtv t12, kpop t09, oneshot t11, puzzleanddragons t07, starlightstage t08, wholesomememes t23, croatia t07, 4chan t22, futurama t14.

**T3-001|T3-031, an April Fools fake or the room's joke (9 items; CC-049).** Ruled as written. Something false posted as true for April Fools by the room's members, and replies played inside it, count toward T3-001. The room's running joke played around the canvas work counts toward T3-031. April Fools play neither posted as true nor carried into canvas talk is packet 1's gap: it counts toward a placed T3-017 when the sub's ordinary subject goes on, and is otherwise left out. Items: danganronpa t18, GuildWars2 t18, spacexmasterrace t12, telegram t01, thesimpsons t04, twitchplayspokemon t09, wholesomememes t11, twentyonepilots t07, berserk t02.

**T3-023|T3-031, the sub's April Fools change or the room's joke (5 items; CC-049).** Neither theme has a discriminator against the other. Playing inside the sub's changed name, look, rules, subject or staged takeover counts toward T3-023 ("Playing along inside the takeover stays T3-023"); the room's running joke played around the canvas work counts toward T3-031. Items: twitchplayspokemon t05, kerbalspaceprogram t02, kerbalspaceprogram t03, leagueoflegends t05, survivor t04.

**T3-150|T3-151, an alliance or help traded (5 items; CC-052).** Ruled as written. An alliance proposed, named or joined, or a promise to defend each other, counts toward T3-150; help offered or asked in return for help or for room, with the return named, counts toward T3-151. Items: stlouisblues t03, nin t02, TeamYellowPlace t03, overwatch t22, starcraft t08.

**T3-031|T3-050, the room's joke or a taunt (4 items; CC-056).** Ruled as written: a concept aimed at a rival community, mocking, threatening or taunting it, counts toward T3-050 even in the room's joke register; a joke played among the room's members counts toward T3-031. Items: udub t07, canucks t38, farmcarrots t15, southafrica t03.

**T3-018|T3-052, a detail decoded or a neighbour noticed (5 items; CC-051).** A neighbouring picture noticed, asked about, liked, mocked, or named as some room's work counts toward T3-052; which character or reference a figure shows, worked out with a reason or a correction, counts toward T3-018. A bare name given to a neighbour's figure counts toward T3-052, and items that turn on it are scheme-ambiguous on T3-018's `must_show`. Items: twice t10, Mario t03, thailand t13, truestl t06, Redox t01.

**T3-018|T3-031, a detail decoded or the room's joke (1 item; CC-051).** A meaning worked out counts toward T3-018; a joke played on what the room drew, or a mock reading kept up as a joke, counts toward T3-031. Item: achievement_hunter t04.

**Carried from packet 5:** T3-010|T3-151 (6 items): malaysia t07, stlouis t05, yogscast t03, floridagators t08, japan t05, metalgearsolid t07.

**Below five, applied as met.** The homeland flag: where a placement holds T3-065, its calls for hands, build, spot, size and repair count toward it (T3-002's `must_not_show`: "The national flag as the room's mark carries T3-065"); where none does, toward the placed T3-002, T3-038, T3-004, T3-020 or T3-021 (mexico t11). National emblems added to the flag are T3-113. T3-016|T3-018 by the discriminator: the event as a whole explained, or a particular picture's meaning worked out.

**Readings applied in packet 6, carried into packet 7:**
- **G15 to G17.** Deals as in packet 5. A theme of the room's land is T3-065 where a placement holds it; the national pictures beside it T3-113; national feeling through the flag T3-145. Thanks for help go to T3-072; credit to makers T3-043.
- **G18.** T3-086 is the community's own quarrel carried onto the canvas. T3-130 is national politics; T3-080 a political symbol argued over, partisan marks included; T3-081 a canvas fight told in a nation's real history of war or occupation, not war talk between fandoms (T3-135). T3-179 is ideology argued from the canvas.
- **G19.** T3-050 is taunts at a rival community; T3-142 jokes about a people; T3-143 a joke's limits argued; T3-182 bigotry in the room's own talk answered; T3-146 and T3-177 covering swastikas and calling for them. T3-154 takes victory claimed or rivals called defeated; T3-050 mockery with no victory claimed. T3-155 is a salute after the fight.
- **G20.** T3-016 takes questions and answers about the event, its rules, the heat map and why subs make pictures. A glitch used to place more is T3-088; a glitch coped with while building T3-074; a glitch explained T3-016. T3-105 keeps records; T3-057 remakes them. A bare title naming r/place shows no act.

### Packet 7

`b4_packet_pairs.py --packet 7`: 480 items (class 3 357, class 4 118, class 5 5). Three pairs split the readings' primaries on five items or more: T3-009|T3-073 22, T3-009|T3-043 10, T3-029|T3-073 7. They were ruled before the packet's first item. The item lists are the packet 7 items that carry the pair in `boundary_ruling`.

**T3-009|T3-043, the work celebrated or its makers credited (62 items; B2's predicted pair 14; CC-063, CC-065).** Ruled as written by the discriminator and T3-009's `decide_when_both` ("Celebration with thanks or credit: the side with more concepts is primary"). Thanks to those who placed or helped, makers named, a member claiming a change they made, and disputes over who made it count toward T3-043. Thanks to another room as an ally count toward T3-072 where a placement holds it; where none does, toward T3-043. Congratulations and pride with no one thanked count toward T3-009. A concept that both thanks and celebrates counts toward the act its words lead with. Items (genuine-joint 46, author-error 16): AceOfAngels8 t05, albania t11, animalcrossing t03, babymetal t06, bangtan t07, Clannad t01, coldplay t06, criticalrole t07, eesti t04, ElderScrolls t04, empiredidnothingwrong t16, europe t20, eve t14, furry_irl t03, fxKorea t07, Goodboye t10, hellointernet t03, hyperlightdrifter t09, kanye t16, lsu t07, luciomains t06, metalcore t02, oneshot t05, pathofexile t12, phish t06, placeDE t08, polska t04, Rainbow6 t13, redhotchilipeppers t09, rocketbeans t10, scotland t06, ScottPilgrim t06, singapore t11, smashbros t05, spacexmasterrace t04, stlouisblues t10, strangerthings t11, straya t07, theexpanse t06, toolband t10, touhou t07, TransFlagPlace t07, transformers t07, TsundereSharks t09, turkey t13, wildhockey t08, yumenikki t05, anaheimducks t08, gamindustri t05, greenlattice t19, GuardiansOfDatBoi t09, kingdomhearts t24, malaysia t11, ssbpm t18, theexpanse t12, ChronoTrigger t06, loliconsunite t08, rickandmorty t08, SquareSpiral t13, tagpro t08, yugioh t17, portugal t29.

**T3-009|T3-073, the work celebrated or what happened to it told (29 items; B2's predicted pair 9; CC-063).** Ruled as written by the discriminator ("Is what happened to the work told (T3-073), or the finished work celebrated (T3-009)?") and T3-073's `decide_when_both`. Words that mark the work achieved count toward T3-009, the work said to have lasted to the end with joy or pride in the words included; words that tell what became of the work, as an account, count toward T3-073. A plain statement that the work survived meets both tests; where the ruling turns on it, the item is scheme-ambiguous on T3-009's `must_show`. Items (genuine-joint 25, scheme-ambiguous 2, author-error 2): denmark t09, FaroeIslands t05, hunterxhunter t09, leagueoflegends t18, norge t12, runescape t03, starcraft t11, vegan t10, vinesauce t02, androidgaming t02, blackmirror t07, day9 t06, dragonquest t08, flashtv t13, formula1 t13, gameboy t07, httyd t11, kamenrider t05, leafs t05, sheffield t08, smite t10, tampabaylightning t14, warframe t13, furry t18, yuyuyu t05, suomi t01, edboxes t08, k_on t07, spelunky t04.

**T3-029|T3-073, a loss mourned or told (18 items; CC-063, CC-068).** Ruled as written by the discriminator ("Is grief voiced (T3-029), or what happened told without it (T3-073)?") and T3-029's `decide_when_both` ("Grief with an account: T3-029 when grief leads, T3-073 when the account does"). Grief in the words counts toward T3-029; a loss reported with no grief in the words, or where the account leads and a sad face trails, toward T3-073. The end of the canvas itself, not a work's loss, is T3-117. Items (genuine-joint 14, author-error 2, reader-error 2): cuboulder t08, placetardis t08, PUBATTLEGROUNDS t10, splatoon t06, cubers t31, mindcrack t11, edmontonoilers t09, pebble t05, DatBoi t03, enterthegungeon t10, foxstevenson t07, Honduras t04, linux t19, metroid t10, ultrahardcore t09, dankmemes t16, frankocean t12, geometrydash t07.

**Below five, applied as met.** Each as written in `boundaries.md`:
- **T3-009|T3-117 (10 items):** 'place is over', signing off, regret at the end and a hope it returns count toward T3-117; the work marked achieved toward T3-009; a concept that opens with the end counts toward T3-117. Items: halo t17, kcroyals t07, minnesotavikings t13, patriots t15, ss13 t07, titanfall t12, unitedkingdom t06, ibo t06, teslamotors t13, muse t11.
- **T3-073|T3-105 (8 items):** a timelapse, screenshot or final image posted or asked for as a record counts toward T3-105; an account told in words toward T3-073. Items: bindingofisaac t13, pathofexile t17, hungary t07, pakistan t15, rangers t13, straya t10, mylittlepony t15, ripcity t11.
- **T3-009|T3-038 (5 items):** words that call a piece done and celebrate it count toward T3-009; progress toward T3-038. Items: miamidolphins t05, pathofexile t14, NieR t07, starryknights t01, startrek t10.
- **T3-054|T3-111 (5 items):** a later canvas planned or answered is T3-054; the sub's purpose decided T3-111. Items: AmericanFlaginPlace t16, greenlattice t20, thebluecorner t10, PlaceNL t18, Goodboye t11.
- **T3-057|T3-105 (3 items):** kept as it was is T3-105, a print included; remade in another medium T3-057, a logo recreated pixel by pixel in Paint included. Items: pcmasterrace t16, thenetherlands t12, aoe2 t12.
- **T3-018|T3-031 (3 items):** as packet 6 ruled it. Items: kerbalspaceprogram t12, ohio t11, osu t08.
- **T3-009|T3-104 (3 items):** "Praise while the work goes on is T3-104; once the work is called finished, T3-009." Items: ripcity t07, bobross t02, witcher t03.
- **T3-105|T3-156 (3 items):** a record kept is T3-105; the mark put on the sub's banner, flair, theme or sidebar T3-156. Items: ireland t14, uiuc t15, heroesofthestorm t08.
- **T3-031|T3-135 (2 items):** the canvas fight told in the fandom's terms counts toward T3-135; the fandom's joke played on the event with no clash in it toward T3-031. Items: splatoon t07, transformers t04.
- **T3-009|T3-026 (2 items):** as packet 3 ruled it. Items: colorado t05, harrypotter t02.
- **T3-038|T3-065 (2 items):** as packet 6 ruled the homeland flag. Items: malaysia t03, kuwait t04.

**Readings first applied in packet 7**, each named in its rulings' whys and listed in `boundaries.md`:
- A theme both readers placed, with a concept of its own, is not dropped by the level rule on a placement count only my B1 tips (kanye t28, msu t11; ChronoTrigger t06 corrected).
- On a clone canvas, the rebuild, the calls to it and its progress count toward T3-054; acts it does not name (the timer, a chat) count toward their own themes (catholicism t09; twice t18 scheme-ambiguous).
- "The work" in T3-073 and T3-058 is the room's own (uvic t04, destiny t08, pathofexile t17, hungary t07).
- Where a report of damage names the attacker in passing, the report leads (T3-073); T3-087 takes concepts whose point is who is behind the damage or why (nbaspurs t13, overwatch t14).
- T3-082 takes only a mark the room did not know of (mysterydungeon t08, MiamiHurricanes t06).
- T3-111 does not reach a standing community's new project (forsen t11, paladins t21).
- A cleaned copy of the final canvas after the lock is a record, T3-105 (straya t10, ireland t14, kanye t20, uiuc t15, frc t10, uofm t15).
- T3-156 takes only a mark from the canvas; theme or header art the words do not tie to the canvas is the sub's ordinary business, T3-017 (fivenightsatfreddys t14, trees t12), and flairs with no canvas mark are T3-185's (THE_R t04).

## Corrections made during the packets

Each correction went through `b4_rule_append.py --replace`, which rewrites the ruled line in place, marks it revised, and keeps the old ledger under a superseded name. 674 rulings have been corrected in place at least once (`b4_cumulative.py`): the 378 of the B4a-05 re-ruling, the 128 of the `also_present` correction, the 130 of the lone-B1 rule, the bag re-rules and slips under QB4-003, the boundary tags of packets 3 and 5, and earlier single corrections. Some lines were corrected twice. In packet 7, two lines were corrected after writing (`packet-07/corrections-01.jsonl`; old ledger `disagreements.superseded-20261013T131513Z.jsonl`): mindcrack t11, where T3-029's placements had been miscounted, and ChronoTrigger t06, where T3-157, placed by both readers, had been dropped on a count only my B1 tipped. `b4_own_support_check.py` finds no placed theme without a concept of its own over the seven packets.

## The conflicts pass

`coder_conflicts.jsonl` holds 72 lines. CC-001 to CC-008 came from packet 1's notes, CC-009 to CC-016 from packet 2's, CC-017 to CC-025 from packet 3's, CC-026 to CC-036 from packet 4's, CC-037 to CC-048 from packet 5's, CC-049 to CC-062 from packet 6's and CC-063 to CC-072 from packet 7's, each read before its packet's first ruling. Packet 6's conflicts are listed in this report's B4a-06 version. Packet 7's:
- **CC-063:** the room's account of its finished work written as one practice: celebrating it, crediting makers and allies, saving images, mourning losses and telling what survived (T3-009, T3-043, T3-072, T3-105, T3-029, T3-073). It explains most of packet 7's genuine-joint rulings.
- **CC-064:** the canvas's end and the work's end written as one practice of closing (T3-117 with T3-029, T3-009, T3-073, T3-105, T3-054, T3-017).
- **CC-065:** credit given, a share claimed and who made or saved the work disputed, as one practice (T3-043, T3-072, T3-030, T3-058, T3-126, T3-082, T3-003).
- **CC-066:** every way of keeping the finished work as one practice: records, remakes, the sub's emblem, an atlas, a later canvas (T3-105, T3-057, T3-156, T3-112, T3-054).
- **CC-067:** carrying the work to another canvas and deciding the canvas room's next life as one practice (T3-054, T3-111, T3-117, T3-022, T3-057).
- **CC-068:** judging a flawed or failed finish as one practice, whether by pride, grief, a joke, a victory or blame (T3-029, T3-009, T3-073, T3-154, T3-031, T3-058).
- **CC-069:** what the canvas meant, argued after it, as one practice: worth, cooperation, identity or ideology (T3-037, T3-157, T3-179, T3-164, T3-075).
- **CC-070:** completion claimed while the work goes on (T3-009, T3-026, T3-038, T3-104, T3-021, T3-041).
- **CC-071:** calls and questions that arrive after the close, answered as one practice of telling people it is over (T3-117, T3-016, T3-002, T3-021, T3-009).
- **CC-072:** as CC-008 to CC-062, a code grouped by exclusion, often a surviving title, so the note gives the scheme nothing to place.

## Agreement before and after

Before is the two readers against each other. After is each reader against the ruling, over the items not unresolved. Both use stage B2's definition: mean Jaccard on placement sets, with primary match beside it. The next table gives both, by packet and over the seven.

| | mean Jaccard before | primary match before | mean Jaccard after | primary match after |
|---|---|---|---|---|
| packet 1 (491; 425 after) | 0.486 | 0.578 | 0.673 | 0.735 |
| packet 2 (447; 428 after) | 0.537 | 0.678 | 0.671 | 0.745 |
| packet 3 (500; 491 after) | 0.475 | 0.598 | 0.612 | 0.644 |
| packet 4 (461; 449 after) | 0.519 | 0.675 | 0.661 | 0.732 |
| packet 5 (409; 403 after) | 0.467 | 0.623 | 0.638 | 0.687 |
| packet 6 (500; 451 after) | 0.454 | 0.510 | 0.600 | 0.595 |
| packet 7 (480; 456 after) | 0.500 | 0.650 | 0.669 | 0.731 |
| all (3,288; 3,103 after) | 0.491 | 0.614 | 0.646 | 0.694 |

The figure after is not a reliability figure. It is agreement following an adjudication I performed. Within packet 7 (`b4_agreement_range.py --ranges 1-53,54-480`), the rest of G20 had 0.544 before and 0.663 after; G21 had 0.495 before and 0.670 after. G21's readers agreed on primaries more often than on whole lists (primary 0.660, Jaccard 0.495): they saw the same leading act and differed on the second. The blind sample's adjudicated stratum at B4b is the test of whether a stranger reaches these rulings.

## Whether stage B2's predictions held

`confusions.md` predicted nineteen pairs. A packet can show only the pairs whose themes it holds.

- **Packet 1 (G01, G02).** All four predicted pairs that could appear split readers: pair 3 (T3-001|T3-023, 20), pair 15 (T3-001|T3-095, 11), pair 19 (T3-015|T3-063, 7), pair 7 (T3-015|T3-075, 4). Three unpredicted pairs split as often or more: T3-017|T3-031 (17), T3-001|T3-048 (13), T3-023|T3-095 (11).
- **Packet 2 (G03 to G06).** Two of five predicted pairs split readers: pair 6 (T3-002|T3-033, 8) and pair 8 (T3-004|T3-070, 6). Five unpredicted pairs split as often or more.
- **Packet 3 (G07, G08 in part).** Four of five predicted pairs split readers: pair 6 (10), pair 10 (T3-004|T3-038, 9), pair 8 (6), pair 5 (T3-004|T3-020, 5). Seven unpredicted pairs split as often or more than pair 5, three of them with T3-041.
- **Packet 4 (G08's end, G09 to G11).** Pair 1, T3-005|T3-021, held: 37 items. Pairs 4 (T3-028|T3-070) and 16 (T3-087|T3-188) split 2 and 1. Five unpredicted pairs split four items or more.
- **Packet 5 (G12 to G14).** All four predicted pairs that could appear split readers: pair 13 (T3-010|T3-024, 17), pair 2 (T3-010|T3-149, 10), pair 11 (T3-010|T3-151, 7) and pair 12 (T3-010|T3-150, 1). Unpredicted: T3-006|T3-061 (8), T3-010|T3-011 (7) and four more at three or four.
- **Packet 6 (G15 to G19, G20 in part).** The three predicted pairs that could appear split readers: pair 2 (14), pair 12 (4) and pair 11 (3). Seven unpredicted pairs split six items or more: T3-017|T3-031 (12), T3-001|T3-031 (7), T3-023|T3-031 (7), T3-150|T3-151 (6), T3-031|T3-050 (6), T3-018|T3-031 (6), T3-018|T3-052 (6).
- **Packet 7 (G20's end, G21).** Both predicted pairs held and were the two commonest splits: pair 9 (T3-009|T3-073, 22) and pair 14 (T3-009|T3-043, 10). Unpredicted: T3-029|T3-073 (7), and T3-009|T3-038, T3-009|T3-117, T3-073|T3-105 and T3-073|T3-117 at 4 each.

Over the seven packets, 17 of the 19 predicted pairs split readers at least once. Pairs 17 (T3-044|T3-082) and 18 (T3-014|T3-152) split no item's primaries. B2's strongest predictions were the ones that held most: pair 1 (37 items), pair 9 (22), pair 3 (20), pair 2 (24 over packets 5 and 6) and pair 13 (17). B2 missed G20's pairs with T3-031, where the room's joke meets ordinary talk, the April Fools themes, a taunt and a decoded detail; T3-017|T3-031 split readers in packet 1 and again in packet 6, on the same contradictory discriminator. It also missed G21's pairs with T3-073 and T3-117 beyond pair 9: grief against an account, and the canvas's end against the work's.
