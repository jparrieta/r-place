# Adjudication report, stage B4 (interim: packets 1 to 6 of 7)

Written at B4a-06, after packet 6 was ruled. During the same leg two answers from J changed rulings already written: QB4-003 (named themes count in the bag test; 11:29 Berlin) and J's answer of 12:28 Berlin on lone B1 themes, which let me choose the rule. Both were applied to packets 1 to 6 through `b4_rule_append.py --replace`, keeping each superseded ledger. This report is rewritten whole after each packet; the figures below cover packets 1 to 6 as they now stand. Older figures are in the git history of this file and in the superseded ledgers `disagreements.superseded-*.jsonl`. Per-packet figures: `out/_adjudication-B4/packet-01/summary.md` to `packet-06/summary.md` (`out/_analysis/b4_packet_summary.py`). The sums: `out/_analysis/b4_cumulative.py --packets 1,2,3,4,5,6`. The named_neither split and the class 4 measure: `out/_analysis/b4_named_neither_split.py --packet N` and `out/_analysis/b4_packet_detail.py --packet N`. Ranges within a packet: `out/_analysis/b4_agreement_range.py`. The re-rule drafts: `out/_adjudication-B4/rerule-B4a-05/`, `rerule-ap-B4a-05/`, `rerule-bag-B4a-06/` and `rerule-loneb1-B4a-06/`. The rulings: `out/disagreements.jsonl`. The boundary paragraphs: `out/_adjudication-B4/boundaries.md`, carried below with their item lists.

## Items adjudicated

Stage B3's inventory (`b3_classes.jsonl`, J's five classes) leaves 3,288 contested items: class 3 (the readers' lists differ) 2,393, class 4 (the readers agree on a list not inside my B1 grouping) 837, class 5 (no B1 grouping) 58.
- **Packet 1** ruled 491: the 18 gloss-only items, G01 (April Fools in the sub) and G02 (the sub's own business).
- **Packet 2** ruled 447: G03 (where the planning happens), G04 (calling people in to place), G05 (telling placers what to place) and G06 (strain, doubt and giving up).
- **Packet 3** ruled 500: G07 (choosing what to make and where) and the first 254 items of G08 (building and growing the mark).
- **Packet 4** ruled 461: the last 6 items of G08, G09 (keeping the mark against damage), G10 (finding who did it) and G11 (scripts, bots and extra accounts).
- **Packet 5** ruled 409: G12 (attacking others' work), G13 (holding back from others' work) and G14 (space and help between rooms).
- **Packet 6** ruled 500: G15 (deals and alliances between rooms), G16 (factions and kindred rooms), G17 (national feeling and the flag), G18 (politics and the community's own quarrels), G19 (rivalry, taunts and victory) and the first 184 items of G20 (talk around the canvas: explaining it, decoding it, joking about it). 345 class 3, 134 class 4, 21 class 5.

Together 2,808 items: 2,036 class 3, 719 class 4, 53 class 5. 480 contested items remain for packet 7 (the rest of G20 and G21).

## The taxonomy split

The next table counts the rulings by taxonomy value, by packet and by class.

| taxonomy | all | packet 1 | packet 2 | packet 3 | packet 4 | packet 5 | packet 6 | class 3 | class 4 | class 5 |
|---|---|---|---|---|---|---|---|---|---|---|
| genuine-joint | 1348 | 137 | 216 | 231 | 239 | 269 | 256 | 1348 | 0 | 0 |
| author-error | 482 | 99 | 78 | 78 | 86 | 58 | 83 | 3 | 459 | 20 |
| scheme-ambiguous | 421 | 121 | 62 | 94 | 59 | 14 | 71 | 363 | 55 | 3 |
| item-is-a-bag | 238 | 21 | 43 | 72 | 50 | 32 | 20 | 189 | 49 | 0 |
| author-disagrees | 186 | 36 | 45 | 21 | 13 | 20 | 51 | 0 | 156 | 30 |
| reader-error | 133 | 77 | 3 | 4 | 14 | 16 | 19 | 133 | 0 | 0 |
| total | 2808 | 491 | 447 | 500 | 461 | 409 | 500 | 2036 | 719 | 53 |

How to read it:
- **Genuine-joint is the largest value, 1,348 (48.0%).** In packet 6 it is 256 of 500 (51.2%). G15's deals hold a border, a truce, an alliance and help in one coder's theme (conflicts CC-037 and CC-052); G20's talk holds an explanation, a decoding and a joke (CC-050, CC-051). One reader places the leading act and the other adds a second. The count measures how rule 0 travelled, not the readers.
- **Author-error rose to 482**, from 334 at B4a-05. Most of the rise is the lone-B1 rule chosen this leg (section below): 83 class 4 rulings in packets 1 to 6 that had kept a one- or two-concept theme of mine now take the readers' list.
- **Scheme-ambiguous is 421 (15.0%).** Packet 6 has 71 (14.2%), against 14 in packet 5. 32 of them turn on two discriminators that disagree with T3-031's own test: T3-017's (24) and T3-001's (8).
- **Item-is-a-bag is 238.** Packet 5 rose from 3 to 32 under QB4-003, which counts the themes a reader listed under its own `also_present`. Packet 6 has 20.
- **Reader-error is 133.** Packet 6 has 19. Most are cases where a `must_not_show` or a `decide_when_both` decides and one reader missed it: kcroyals t09 (talk about the canvas is not T3-017), wholesomememes t09 (a glitch explained is T3-016 by T3-074's `decide_when_both`), kerbalspaceprogram t02 and t03 and mcgill t03 (playing along inside the sub's April Fools change stays T3-023).
- **No ruling holds a theme no placement held**, and no `also_present` lists a theme that no reader and not my B1 named. Every class 4 ruling that keeps a theme only my B1 placed gives it three concepts or more (`b4_lone_b1_check.py`: 144 lines).

## J's rulings on themes added (QB4-001), and the re-ruling of packets 1 to 4

I asked J at B4a-03 (QB4-001) whether to keep adding a one- or two-concept theme that no placement held. J answered at 06:43 Berlin on 13 October: "Ask it to stop. The point is to try to adjudicate. I imagine that the additions are really just the analyst trying to be nice. And not go back on what others said". J's rulings at 06:45 and 06:47 Berlin:
1. The placements are the readers' and the analyst's (my B1). A ruling chooses among those placements and adds no theme beyond them.
2. A ruling takes the union of placements only when it names, for each theme it keeps, the separate concept that carries it; otherwise it chooses.
3. Re-rule only the items in packets 1 to 4 whose ruling holds a theme no placement held, under (1) and (2), and keep the superseded ledger.

At B4a-05, 378 rulings were re-ruled under (3): packet 1 30, packet 2 58, packet 3 157, packet 4 133. The method, applied to every packet since:
- **The removed theme's concepts.** Each is read against the tests of the themes the placements hold. A concept counts toward a placed theme when that theme's `must_show` takes it and no field sends it to another placed theme. A `must_not_show` that sends it to a theme no placement holds does not stop it. Otherwise the concept is left out and named in the why.
- **Rule 0 inside the placements.** Order the placed themes by concept count, ties by how many of reading A, reading B and my B1 hold the theme; place at most three. A one- or two-concept theme is kept when it leads its level on placements; where themes tie at a level with equal placements, none is kept and the order ends. Where the top of the order is a tie on concepts and placements, all the tied themes are placed.
- **Unresolved** where no placement's test takes the material.

What the re-ruling did (calls to defend sent to T3-005 where no placement held T3-002; the homeland flag's repair to T3-021 and its design to the readers' T3-004 or T3-020 where no placement held T3-065; placed themes the old limit of three had cut now entering) is set out in this report's B4a-05 version. Agreement after over packets 1 to 4 rose from 0.565 to 0.628, and named_neither fell from 741 to 485.

## J's ruling on also_present (09:09 Berlin) and QB4-002

J's ruling of 09:09 Berlin, through the PI: "rule (1) extends to also_present. also_present lists only themes that a reader or your B1 named." QB4-002, answered at 09:20 Berlin: "yes. A theme a reader listed under its own also_present counts as named by that reader. also_present may list themes a reader placed, a reader listed under its own also_present, or your B1 named; nothing else." At B4a-05, `b4_ap_scan.py` found 128 lines in packets 1 to 4 listing 273 themes outside that set; each was corrected through `--replace`, and four bags that lost every theme at the three-concept floor were re-ruled by hand (archlinux t01, ireland t04, starvstheforcesofevil t02, de t02).

## QB4-003: named themes in the bag test, and the revisit

I asked J during packet 6 (QB4-003) whether a theme a reader listed under its own `also_present`, and that no placement holds, counts in the bag test. Meanwhile a bag needed four placed themes. J answered at 11:29 Berlin: "count them. Themes a reader listed under its own also_present count in the bag test. Apply it to packet 6 and to the 43 rulings in packets 1 to 5 that out/_analysis/b4_bag_named_check.py lists, keeping the superseded ledger."

The test as applied from packet 6's item 126 (paragraph in `boundaries.md`):
- **The themes counted** are the placed themes and every theme a reader listed under its own `also_present`.
- **A named theme's concepts of its own** are the item's concepts its `must_show` takes that no placed theme in the ruling already holds. The concepts a reader listed are read against the test, not taken on trust.
- **Four themes or more with three concepts of their own make a bag.** The bag places the largest act a placement holds (on a tie, the one with more placements) and lists every other counted theme with three concepts or more under `also_present`, twenty at most.
- **A placed theme with three concepts or more is never cut by the limit of three.** If a fourth reaches three, the item is a bag.

The revisit: the 64 lines the check listed in packets 1 to 6 were read; 45 became bags and 19 were kept, where the named themes' concepts did not hold three under their tests. Four slips outside the list, where four placed themes with three concepts each had been cut at the limit, also became bags: utaustin t05 and japan t05 (packet 6), loliconsunite t02 (packet 4) and lebanon t02 (packet 5). pcmasterrace t10 (packet 5), on the list, had also cut two placed themes at the limit. After packet 6's last chunk the check flagged seven packet 6 bags that might list one more named theme. Six hold two concepts or fewer under the test. One was a slip: chibears t10, where reader A's T3-050 holds three ('fuck the Finns', '/r/psu sends their regards.', 'change the Packers G to a Georgia G!'). It was re-ruled with T3-050 under `also_present`. 26 older bags in packets 1 to 5 could list more named themes; J named only the 43, and they are carried open.

The bags re-ruled, by packet: packet 1 starcraft t03; packet 3 AvoArmy t01; packet 4 warriors t06; packet 5 TheFarLeftSide t04, wallstreetbets t06, india t08, croatia t04, cirkeltrek t08, AmericanFlaginPlace t08, osugame t07, europe t07, AMD t13, aoe2 t06, factorio t10, formula1 t10, kanye t06, masseffect t05, prequelmemes t08, heroesofthestorm t10, placeDE t04, quebec t04, toolband t09, czech t07, titanfall t07, india t04, mylittlepony t07, OnePiece t03, radiohead t04, theblackvoid t02, theitalyplace t11; packet 6 fivenightsatfreddys t08, philippines t08, suomi t10, turkey t06, rocketleague t05, cfb t02, denmark t05, frankocean t05, chibears t10, EraseThePlace t06, starcitizen t11, TransFlagPlace t05, elitedangerous t07, eagles t06.

## J's answer on lone B1 themes, and the rule chosen

At B4a-05 I wrote a doubt: rule 0 inside the placements kept a one- or two-concept theme only my B1 placed even against two agreeing readers, so class 4 turned toward my B1 (44 of 86 in packet 5). The PI put three options to J: (1) leave it, my B1 a full placement; (2) a theme only my B1 placed beats two agreeing readers only with three concepts or more of its own; (3) where both readers agree, their list stands and my B1 is a note. J answered at 12:28 Berlin: "Whatever the agent feels more comfortable with. They can also adapt the code definition if needed".

I chose option (2), with a condition:
- **The rule.** In class 4, a theme only my B1 placed stands against the two agreeing readers only with three concepts or more of its own. With fewer it is left out and named in the why.
- **The condition.** The readers' list then stands where its test takes concepts. Where my reading finds it takes none, the item is unresolved: no one-concept theme of mine is put in its place.
- **Class 3 is unchanged.** There the readers disagree and my B1 is the third placement; the level rule decides.

Why. Two independent readers agreeing is the case where my B1 carries the author's pull most. Three concepts is the scheme's own floor for a theme of its own (the bag rule and `also_present`). Option (3) would make the adjudication measure obedience, and would force a readers' theme whose test takes nothing.

`b4_lone_b1_check.py` found 250 class 4 rulings in packets 1 to 6 keeping a lone B1 theme, 130 of them with fewer than three concepts. `b4_lone_b1_draft.py` built one draft per packet; each line drops the weak theme, keeps a scheme-ambiguous line on its field, and opens its why with the rule. The 130 lines changed: packet 1 11, packet 2 29, packet 3 31, packet 4 20, packet 5 23, packet 6 16. By taxonomy: author-error 83, author-disagrees 40, scheme-ambiguous 7; unresolved 30. Packet 6's chunks 12 to 20 were ruled under the rule. The superseded ledgers: `disagreements.superseded-20261013T103259Z.jsonl` to `-103319Z`.

## author-error and author-disagrees

author-error: 482 (packet 1 99, packet 2 78, packet 3 78, packet 4 86, packet 5 58, packet 6 83). author-disagrees: 186 (36, 45, 21, 13, 20, 51). Both come almost wholly from class 4, where the readers agreed on a list my B1 grouping did not hold, and from class 5, where my B1 left the theme unplaced.

The next list gives, by packet, the class 4 items counted by what the ruling holds, whatever their taxonomy value:
- **Packet 1:** the readers' list taken 97, a B1 theme kept 21, an empty ruling 34, other 1.
- **Packet 2:** the readers' list 81, a B1 theme kept 26, empty 13, other 4.
- **Packet 3:** the readers' list 83, a B1 theme kept 29, empty 2, other 3.
- **Packet 4:** the readers' list 83, a B1 theme kept 15, empty 2, other 5.
- **Packet 5:** the readers' list 62, a B1 theme kept 21, empty 3.
- **Packet 6:** the readers' list 87, a B1 theme kept 32, empty 15.

Over the six packets the readers' list was taken in 493 class 4 items and a B1 theme kept in 144, each with three concepts or more; 69 are unresolved and 13 hold another shape (bags and partial lists). At B4a-05 the counts over five packets were 329 and 220.

Two labels from earlier packets do not match the measure and are carried as they stand: 12 packet 4 author-error rulings from items 401 to 461 that keep a B1 theme beside the readers' list, and two packet 2 author-disagrees rulings that take the readers' list.

I cannot separate how much of each packet's split is the scheme and how much is my pull toward my own grouping. The blind sample at B4b tests the adjudicated stratum against fresh readers.

My commonest B1 errors:
- **Packet 1:** T3-031 placed on an in-joke with no canvas in it; T3-001 where nothing was posted as true; T3-063 on posts that are not canvas posts.
- **Packet 2:** calls for hands my B1 had placed as the proposal, the progress or a further piece; placing troubles (T3-074); templates my B1 had placed as one plan imposed (T3-091).
- **Packet 3:** links that only show where the finished mark is (T3-026); the readers' T3-004, T3-033 and T3-020.
- **Packet 4:** the readers' T3-005, T3-170, T3-021, T3-088 (glitches used to place more) and T3-087.
- **Packet 5:** the readers' T3-006, T3-010, T3-068, T3-084, T3-151 and T3-137.
- **Packet 6:** in author-error rulings the readers placed T3-031 (19), T3-018 (10), T3-016 (6), T3-065 (5), T3-030, T3-122 and T3-150 (4 each) where my B1 did not. My B1 had read G20's talk as remarks on neighbours (T3-052, lost in 9 rulings) where the readers saw the room's joke or a picture decoded.

The themes of mine kept against both readers in packet 6's author-disagrees rulings, each with three concepts or more: T3-010 6, T3-011 2, T3-084 2, and single themes such as T3-031 (masseffect t10, nine concepts of jokes with no clash told), T3-006 (survivor t21, five plans to write over the Danish flag), T3-004 (morrowind t06, seven concepts arguing which words go under Vivec), T3-037 (forsen t10), T3-057 (portugal t38, the FEUP claim made copypasta) and T3-135 (prequelmemes t09).

## Fields by ambiguity

The next list counts the 421 scheme-ambiguous rulings by the field whose sentence failed, with packets 1 to 6 in brackets.

- must_show: 227 (76, 33, 51, 34, 2, 31)
- discriminators: 110 (39, 17, 16, 2, 4, 32)
- must_not_show: 56 (2, 6, 24, 8, 8, 8)
- decide_when_both: 28 (4, 6, 3, 15, 0, 0)

Packet 6's discriminator failures are almost all the canvas condition: T3-017's discriminator against T3-031 (24) and T3-001's (8). Its `must_show` failures are spread: T3-018 5, T3-052 4, T3-030 2, T3-086 2 and single themes.

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, over the six packets. Stage C1 opens with it.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-017 | 54 | 6 | 0 | 1 | 47 |
| T3-033 | 34 | 31 | 2 | 0 | 1 |
| T3-001 | 32 | 18 | 0 | 0 | 14 |
| T3-023 | 26 | 24 | 0 | 0 | 2 |
| T3-004 | 26 | 4 | 14 | 0 | 8 |
| T3-002 | 14 | 1 | 2 | 3 | 8 |
| T3-005 | 13 | 5 | 0 | 7 | 1 |
| T3-038 | 12 | 10 | 2 | 0 | 0 |
| T3-073 | 9 | 9 | 0 | 0 | 0 |
| T3-020 | 9 | 0 | 8 | 0 | 1 |
| T3-063 | 8 | 6 | 1 | 0 | 1 |
| T3-021 | 8 | 4 | 4 | 0 | 0 |

83 more themes failed on 176 rulings between them.

The sentences that failed most:
- **T3-017's discriminator** "Is it the room's running in-joke carried into the canvas talk or the day (T3-031), or the sub's ordinary subject going on (T3-017)?" (47: packet 1 23, packet 6 24). "or the day" contradicts T3-031's own `must_show`, "The room's own humour carried into canvas talk". Readers place a joke with no canvas in it under T3-031 by the discriminator, and under T3-017 by T3-031's test. The canvas-condition paragraph rules for T3-031's test, so every such item is scheme-ambiguous on this sentence. Packet 6: canucks t13, eder t01, edmontonoilers t12, ibo t03, ibo t05, india t14, paladins t04, paladins t26, planetside t02, totallynotrobots t15, zootopia t16, lego t04, survivor t04, chicago t08, empiredidnothingwrong t19, flashtv t12, kpop t09, oneshot t11, puzzleanddragons t07, starlightstage t08, wholesomememes t23, croatia t07, 4chan t22, futurama t14.
- **T3-001's discriminator** "Is the joke a fake posted as true for April Fools (T3-001), or the room's ordinary in-jokes and memes on any day (T3-031)?" (14: packet 1 6, packet 6 8). The same contradiction from T3-001's side. Packet 6: danganronpa t18, GuildWars2 t18, telegram t01, thesimpsons t04, twitchplayspokemon t09, wholesomememes t11, twentyonepilots t07, berserk t02.
- **T3-033's `must_show`** "An idea of what the room should put on the canvas, offered to the room" (31). It does not say "first"; T3-041's `must_not_show` gives the first mark to T3-033 (conflict CC-019).
- **T3-023's** "A change made to a whole sub for April Fools" (24). It does not say whether another sub's change counts (porterrobinson t07 in packet 6).
- **The homeland flag in the siblings' `must_not_show` lines** (T3-004 14, T3-020 8, and others). T3-065's `must_show` takes the flag's build, spot, size, repair and calls for hands; no sibling's `must_not_show` says so.
- **T3-018's `must_show`** "whose character a figure is" (packet 6, 5). It reaches a bare name given to a neighbour's figure, which T3-052's "neighbours named" also takes (twice t10, Mario t03), and a mock reading kept up as a joke, which T3-031 takes (achievement_hunter t04).
- **T3-052's `must_show`** "Pictures around the room's mark noticed" (packet 6, 4). It presumes the room has a mark of its own (shitredditsays t03) and does not say whether the room's joint work is a neighbour's (rhythmheaven t11).
- **T3-086's `must_show`** "A dispute or rivalry from the community's own life" against T3-050's discriminator, which calls T3-086 "the community's own internal quarrel" (neu t07, gatech t09). A school rivalry is both.
- **T3-005's `decide_when_both`** (packet 4, 7) names no tie; **T3-073's `must_show`** (packet 4, 7) overlaps T3-005's "alarms"; **T3-027's `decide_when_both`** (packet 4, 6); **T3-006's discriminator** against T3-061 (packet 5, 4).

Single failures for stage C1's list, from packet 6:
- **T3-115's `must_show`** (re_zero t07): "a refusal on grounds of rivalry" without saying whether a rivalry inside the fandom, against a member's call, counts.
- **T3-147's `must_show`** (tampabaylightning t16): a bare video link about the event.
- **T3-030's `must_show`** (bangtan t15, rainbowgrid t04) and **T3-020's `must_not_show`** (mexico t01, Peru t01), met in G15 and G17.
- **T3-122, T3-141, T3-002, T3-163, T3-013, T3-019, T3-066, T3-172, T3-113, T3-142, T3-182, T3-046, T3-005, T3-057** `must_show`, and **T3-033's and T3-021's `must_not_show`**, once each; the sentences are in `packet-06/summary.md` through `b4_packet_detail.py`.
The single failures from packets 3 to 5 are in this report's B4a-05 version and in the ledger.

## The named_neither rate

named_neither: 649 of 2,808 (23.1%). Packet 1: 47 of 491 (9.6%). Packet 2: 89 of 447 (19.9%). Packet 3: 146 of 500 (29.2%). Packet 4: 118 of 461 (25.6%). Packet 5: 104 of 409 (25.4%). Packet 6: 145 of 500 (29.0%). At B4a-05 the figure over five packets was 616 (26.7%); the lone-B1 rule took it to 504 over those five.

Every named_neither ruling keeps a theme from my B1 grouping that neither reader placed; none holds a theme no placement held. 114 of the 649 are author-disagrees. The next list splits them by packet:
- **The primary itself chosen by neither reader:** packet 1 20, packet 2 24, packet 3 49, packet 4 16, packet 5 25, packet 6 54.
- **How many themes the ruling places** (one, two, three): packet 1 17, 17, 13; packet 2 9, 40, 40; packet 3 18, 42, 86; packet 4 6, 32, 80; packet 5 12, 18, 74; packet 6 21, 53, 71.
- **The B1 themes kept most often:** packet 1 T3-017 15, T3-048 6, T3-023 6; packet 2 T3-069 8, T3-041 8, T3-038 6; packet 3 T3-041 14, T3-113 10, T3-070 9; packet 4 T3-042 9, T3-087 7, T3-170 7; packet 5 T3-150 11, T3-151 8, T3-061 7; packet 6 T3-010 13, T3-017 9, T3-149 5, T3-130 5.

My reading of it. named_neither now measures my B1 grouping kept against both readers, mostly in class 3, where my B1 is the third placement and the level rule keeps a theme of mine alone at its level. In class 4 every kept theme of mine now has three concepts of its own. Packet 6's 54 primaries chosen by neither reader are mostly G20 items where my B1's theme held the most concepts (twitchplayspokemon t05's T3-023, Thegreatblackhole t01's T3-171). The blind sample's adjudicated stratum will show whether strangers reach these rulings.

## The unresolved count

unresolved: 161 of 2,808 (5.7%). Packet 1: 66. Packet 2: 19. Packet 3: 9. Packet 4: 12. Packet 5: 6. Packet 6: 49. At B4a-05 the count over five packets was 85; the lone-B1 rule added 27 there (packet 1 11, packet 2 9, packet 3 2, packet 4 2, packet 5 3).

Added by the lone-B1 rule, where my B1's weak theme left and the readers' test takes nothing:
- packet 1: austria t12, polandball t05, smashbros t01, survivor t28, redhotchilipeppers t12, PlaceNL t13, touhou t18, canucks t25, armok t04, btc t12, leafs t12;
- packet 2: dmt t03, shield t06, bulgaria t07, monstercat t14, chicago t01, ireland t12, suomi t26, kuwait t08, livecounting t06;
- packet 3: germany t19, kingdomhearts t21; packet 4: sonicthehedgehog t07, yogscast t11; packet 5: germany t08, monalisaclan t12, lakers t16; packet 6: futurama t15, azerbaijan t02, anarcho_capitalism t17, samuraijack t14.

Packet 6, by the reason the scheme did not decide:
- **A bare title, pointer or reaction that shows no act** (author-disagrees), 17, all class 5: albania t01, archlinux t13, kindafunny t03, mechanicalkeyboards t06, raocow t08, spacex t07, suomi t12, elitedangerous t10, mexico t19, anarchism t09, ik_ihe t05, japan t14, satania t01, satania t09, wow t05, smite t11, GranColombia t10.
- **The words do not say whose picture, what object or what was asked** (a placed theme's `must_show`), 10: romania t18 (T3-113), cardinals t09 and wallstreetbets t17 (T3-052), habs t13 (T3-005), orderofthebluecorner t12 (T3-002), costa_rica t10 (T3-182), tampabaylightning t16 (T3-147), porterrobinson t18 and Dustforce t02 (T3-018), futurama t11 (T3-057).
- **A room joke with no canvas in the words** (T3-017's discriminator), 8: india t14, survivor t04, empiredidnothingwrong t19, flashtv t12, oneshot t11, starlightstage t08, wholesomememes t23, 4chan t22.
- **April Fools play neither posted as true nor carried into canvas talk** (packet 1's gap; T3-001's discriminator), 6: danganronpa t18, telegram t01, thesimpsons t04, wholesomememes t11, twentyonepilots t07, berserk t02.
- **The lone-B1 rule**, 4: futurama t15, azerbaijan t02, anarcho_capitalism t17, samuraijack t14.
- **Class 4 where neither the readers' test nor a theme of mine takes the material**, 4: landry t04 (sincerity not shown), pakistan t27 (a question about an operation's name), porterrobinson t13 (another room's catchphrase as a greeting), Slovakia t02 (April Fools play with neither the canvas nor a sub change in the words).

The packet 1 to 5 lists by reason are in this report's B4a-05 version; the main ones are April Fools play not posted as true (13), another sub's change (8), moderators applying standing rules to non-canvas posts (6, CC-004), one surviving concept with no doing (packets 2 and 3), and the attack, its target or its culprit not shown (packet 4).

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

**Readings applied in packet 6, to carry into packet 7:**
- **G15 to G17.** Deals as in packet 5. A theme of the room's land is T3-065 where a placement holds it; the national pictures beside it T3-113; national feeling through the flag T3-145 (portugal t08's 'verti uma lágrima'). Thanks for help go to T3-072; credit to makers T3-043.
- **G18.** T3-086 is the community's own quarrel carried onto the canvas (Hello Internet's flag arguments in hellointernet t04 and halo t14's FixMCC; Bitcoin's scaling split; the Texans-Colts FTC mark). T3-130 is national politics; T3-080 a political symbol argued over, partisan marks included; T3-081 a canvas fight told in a nation's real history of war or occupation (belgium t06's buffer state, PlaceNL t12's colonisation), not war talk between fandoms (T3-135). T3-179 is ideology argued from the canvas.
- **G19.** T3-050 is taunts at a rival community; T3-142 jokes about a people (T3-050's `must_not_show`); T3-143 a joke's limits argued; T3-182 bigotry in the room's own talk answered; T3-146 and T3-177 covering swastikas and calling for them. T3-154 takes victory claimed or rivals called defeated; T3-050 mockery with no victory claimed (russia t13, gamindustri t15). T3-155 is a salute after the fight.
- **G20.** T3-016 takes questions and answers about the event, its rules, the heat map and why subs make pictures. A rule of the event is T3-016; a glitch used to place more T3-088; a glitch coped with while building T3-074; a glitch explained T3-016 (T3-074's and T3-088's `decide_when_both`). T3-105 keeps records; T3-057 remakes them as wallpapers, memes or copypasta. A bare title naming r/place shows no act.

## Corrections made during the packets

Each correction went through `b4_rule_append.py --replace`, which rewrites the ruled line in place, marks it revised, and keeps the old ledger under a superseded name. 672 rulings have been corrected in place at least once (`b4_cumulative.py`): the 378 of the B4a-05 re-ruling, the 128 of the `also_present` correction, the 130 of the lone-B1 rule, the bag re-rules and slips under QB4-003, the boundary tags of packets 3 and 5, and earlier single corrections listed in this report's B4a-05 version. Some lines were corrected twice. In packet 6, 32 lines were corrected after writing: the 14 bags, the 16 lone-B1 re-rules, utaustin t05 and japan t05. The last correction is chibears t10 (`disagreements.superseded-20261013T111959Z.jsonl`). `b4_own_support_check.py` finds no placed theme without a concept of its own over the six packets.

## The conflicts pass

`coder_conflicts.jsonl` holds 62 lines. CC-001 to CC-008 came from packet 1's notes, CC-009 to CC-016 from packet 2's, CC-017 to CC-025 from packet 3's, CC-026 to CC-036 from packet 4's, CC-037 to CC-048 from packet 5's and CC-049 to CC-062 from packet 6's, each read before its packet's first ruling. Packet 6's conflicts:
- **CC-049:** the room's joking written as one practice whether it is about the canvas, the sub's April Fools change, the sub's ordinary talk or a rival (T3-017|T3-031, T3-001|T3-031, T3-023|T3-031, T3-031|T3-050).
- **CC-050:** explaining what r/place is joined with bringing people into the work (T3-016 with T3-002 and T3-044).
- **CC-051:** looking at the canvas written as one practice of making sense of it: the event explained, a detail decoded, a neighbour named, an image recast as a joke (T3-016, T3-018, T3-052, T3-031).
- **CC-052:** as CC-037 in packet 5, in G15's own themes: truces, alliances, help traded and borders as one practice (T3-010|T3-149, T3-150|T3-151).
- **CC-053:** a deal's course written as one practice: made, invoked against a breach, disputed and retold (T3-149, T3-195, T3-030).
- **CC-054:** the homeland flag's calls, plan, spot, build, repair and defence written as one practice (T3-065 with T3-002, T3-038, T3-004, T3-020, T3-021).
- **CC-055:** the choice of what goes on or beside the flag, whether an emblem, a design detail, a further piece or a political mark (T3-113, T3-004, T3-041, T3-080).
- **CC-056:** joking between nations over the flags written as one practice of banter (T3-050, T3-142, T3-031, T3-081).
- **CC-057:** the room's own register (a game, a film, a crusade, communist history, a mock state) as the way the canvas work is done (T3-031 against T3-135 and the act's own theme).
- **CC-058:** after the close, victory, blame, the room's conduct and the lasting taunt written as one practice of settling what happened (T3-154, T3-058, T3-050, T3-073).
- **CC-059:** politics argued from the canvas as one practice (T3-130, T3-080, T3-179, T3-086, T3-145).
- **CC-060:** a colour faction's spreading, defence, faith and purity arguments as one practice (T3-171, T3-174, T3-005).
- **CC-061:** offensive material and the answers to it kept in one theme (T3-177, T3-146, T3-182, T3-143, T3-142).
- **CC-062:** as CC-008 to CC-048, a code grouped by exclusion, often a surviving title, so the note gives the scheme nothing to place.

## Agreement before and after

Before is the two readers against each other. After is each reader against the ruling, over the items not unresolved. Both use stage B2's definition: mean Jaccard on placement sets, with primary match beside it. The next table gives both, by packet and over the six.

| | mean Jaccard before | primary match before | mean Jaccard after | primary match after |
|---|---|---|---|---|
| packet 1 (491; 425 after) | 0.486 | 0.578 | 0.673 | 0.735 |
| packet 2 (447; 428 after) | 0.537 | 0.678 | 0.671 | 0.745 |
| packet 3 (500; 491 after) | 0.475 | 0.598 | 0.612 | 0.644 |
| packet 4 (461; 449 after) | 0.519 | 0.675 | 0.661 | 0.732 |
| packet 5 (409; 403 after) | 0.467 | 0.623 | 0.638 | 0.687 |
| packet 6 (500; 451 after) | 0.454 | 0.510 | 0.600 | 0.595 |
| all (2,808; 2,647 after) | 0.489 | 0.608 | 0.642 | 0.688 |

The figure after is not a reliability figure. It is agreement following an adjudication I performed. Agreement after rose in packets 1 to 5 against their B4a-05 figures (packet 5 from 0.612 to 0.638), because the lone-B1 rule took my weak themes out of class 4 rulings. Packet 6's readers agreed with each other least of the six packets (0.454, primary 0.510). Within packet 6 (`b4_agreement_range.py`), items 1 to 316 (G15 to G19) had 0.446 before and 0.593 after; items 317 to 500 (G20) had 0.468 before and 0.616 after. Items 1 to 125, ruled before QB4-003 was answered, had 0.615 after; items 126 to 275, 0.581; items 276 to 500, ruled under the lone-B1 rule, 0.605. The parts hold different families, so the differences are not the rules' effect alone. The blind sample's adjudicated stratum at B4b is the test of whether a stranger reaches these rulings.

## Whether stage B2's predictions held

`confusions.md` predicted nineteen pairs. A packet can show only the pairs whose themes it holds.

- **Packet 1 (G01, G02).** All four predicted pairs that could appear split readers: pair 3 (T3-001|T3-023, 20), pair 15 (T3-001|T3-095, 11), pair 19 (T3-015|T3-063, 7), pair 7 (T3-015|T3-075, 4). Three unpredicted pairs split as often or more: T3-017|T3-031 (17), T3-001|T3-048 (13), T3-023|T3-095 (11).
- **Packet 2 (G03 to G06).** Two of five predicted pairs split readers: pair 6 (T3-002|T3-033, 8) and pair 8 (T3-004|T3-070, 6). Five unpredicted pairs split as often or more.
- **Packet 3 (G07, G08 in part).** Four of five predicted pairs split readers: pair 6 (10), pair 10 (T3-004|T3-038, 9), pair 8 (6), pair 5 (T3-004|T3-020, 5). Seven unpredicted pairs split as often or more than pair 5, three of them with T3-041.
- **Packet 4 (G08's end, G09 to G11).** Pair 1, T3-005|T3-021, held: 37 items. Pairs 4 and 16 split 2 and 1. Five unpredicted pairs split four items or more.
- **Packet 5 (G12 to G14).** All four predicted pairs that could appear split readers: pair 13 (T3-010|T3-024, 17), pair 2 (T3-010|T3-149, 10), pair 11 (T3-010|T3-151, 7) and pair 12 (T3-010|T3-150, 1). Unpredicted: T3-006|T3-061 (8), T3-010|T3-011 (7) and four more at three or four.
- **Packet 6 (G15 to G19, G20 in part).** The three predicted pairs that could appear split readers: pair 2 (T3-010|T3-149, 14), pair 12 (T3-010|T3-150, 4) and pair 11 (T3-010|T3-151, 3). Seven unpredicted pairs split six items or more: T3-017|T3-031 (12), T3-001|T3-031 (7), T3-023|T3-031 (7), T3-150|T3-151 (6), T3-031|T3-050 (6), T3-018|T3-031 (6), T3-018|T3-052 (6). T3-002|T3-065 split 4.

G15's alliances and truces split as G14's deals did, on the pairs with T3-010 that B2 predicted. B2 missed G20's pairs with T3-031: the room's joke meets ordinary talk, the April Fools themes, a taunt and a decoded detail. T3-017|T3-031 split readers in packet 1 and again in packet 6, on the same contradictory discriminator. Pairs 9 (T3-009|T3-073) and 14 (T3-009|T3-043) belong to packet 7.
