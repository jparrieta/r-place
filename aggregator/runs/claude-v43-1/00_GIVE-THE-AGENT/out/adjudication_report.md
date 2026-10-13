# Adjudication report, stage B4 (interim: packets 1 to 5 of 7)

Written at B4a-05, after packet 5 was ruled. Earlier in the same leg, the 378 rulings of packets 1 to 4 that placed a theme no placement held were re-ruled under J's rulings of 13 October, and 128 `also_present` lists were corrected under J's ruling of 09:09 Berlin. It is rewritten whole after each packet; the figures below cover packets 1 to 5 as they now stand. Older versions of the figures are in the git history of this file and in the superseded ledgers `disagreements.superseded-*.jsonl`. Per-packet figures: `out/_adjudication-B4/packet-01/summary.md` to `packet-05/summary.md` (`out/_analysis/b4_packet_summary.py`, rerun for all five packets after packet 5). The sums: `out/_analysis/b4_cumulative.py --packets 1,2,3,4,5`. The named_neither split and the class 4 measure: `out/_analysis/b4_named_neither_split.py --packet N` and `out/_analysis/b4_packet_detail.py --packet N`. Ranges within a packet: `out/_analysis/b4_agreement_range.py`. The re-ruling's work lists and decisions: `out/_adjudication-B4/rerule-B4a-05/`; the `also_present` correction's: `out/_adjudication-B4/rerule-ap-B4a-05/`. The rulings: `out/disagreements.jsonl`. The boundary paragraphs: `out/_adjudication-B4/boundaries.md`, carried below with their item lists.

## Items adjudicated

Stage B3's inventory (`b3_classes.jsonl`, J's five classes) leaves 3,288 contested items: class 3 (the readers' lists differ) 2,393, class 4 (the readers agree on a list not inside my B1 grouping) 837, class 5 (no B1 grouping) 58.
- **Packet 1** ruled 491: the 18 gloss-only items, G01 (April Fools in the sub) and G02 (the sub's own business).
- **Packet 2** ruled 447: G03 (where the planning happens), G04 (calling people in to place), G05 (telling placers what to place) and G06 (strain, doubt and giving up).
- **Packet 3** ruled 500: G07 (choosing what to make and where) and the first 254 items of G08 (building and growing the mark).
- **Packet 4** ruled 461: the last 6 items of G08, G09 (keeping the mark against damage), G10 (finding who did it) and G11 (scripts, bots and extra accounts). 355 class 3, 105 class 4, 1 class 5.
- **Packet 5** ruled 409: G12 (attacking others' work), G13 (holding back from others' work) and G14 (space and help between rooms). 322 class 3, 86 class 4, 1 class 5.

Together 2,308 items: 1,691 class 3, 585 class 4, 32 class 5. 980 contested items remain for packets 6 and 7.

## The taxonomy split

The next table counts the rulings by taxonomy value, by packet and by class.

| taxonomy | all | packet 1 | packet 2 | packet 3 | packet 4 | packet 5 | class 3 | class 4 | class 5 |
|---|---|---|---|---|---|---|---|---|---|
| genuine-joint | 1117 | 138 | 216 | 232 | 240 | 291 | 1117 | 0 | 0 |
| scheme-ambiguous | 350 | 121 | 62 | 94 | 59 | 14 | 305 | 43 | 2 |
| author-error | 334 | 99 | 61 | 55 | 78 | 41 | 3 | 314 | 17 |
| author-disagrees | 208 | 36 | 62 | 44 | 22 | 44 | 0 | 195 | 13 |
| item-is-a-bag | 185 | 20 | 43 | 71 | 48 | 3 | 152 | 33 | 0 |
| reader-error | 114 | 77 | 3 | 4 | 14 | 16 | 114 | 0 | 0 |
| total | 2308 | 491 | 447 | 500 | 461 | 409 | 1691 | 585 | 32 |

How to read it:
- **Genuine-joint is the largest value, 1,117 (48.4%).** In packet 5 it is 291 of 409 (71.1%). A G14 theme often holds a border, a truce, an alliance, help traded and help sent in one coder's theme (conflicts CC-037 and CC-043). One reader places the leading deal and the other adds a second. The count measures how rule 0 travelled, not the readers.
- **Scheme-ambiguous is 350 (15.2%).** Packet 5 has 14 (3.4%), the fewest of any packet. Four of them turn on one sentence, T3-006's discriminator against T3-061.
- **Item-is-a-bag is 185.** Packet 5 has 3 (bostonceltics t08, pakistan t21, russia t05). Inside the placements a bag needs four placed themes with three concepts each, and few G14 items have four placements. The `also_present` correction took four bags out of packets 2 to 4 (archlinux t01, ireland t04, starvstheforcesofevil t02, de t02; section below).
- **Reader-error is 114.** Packet 5 has 16, most where a packet 5 boundary paragraph or a `must_not_show` decides and one reader missed it: buffalo t04 and VelvetUnderground t04 (non-aggression or peace named, T3-149), Northwestern t04 (a request for help is T3-084 by T3-011's `must_not_show`), gameboy t06 (T3-094's warning that a faction covers unapproved art).
- **Themes added beyond the placements.** In packets 1 to 3 and items 1 to 400 of packet 4, a theme on one or two concepts was added wherever the concept passed that theme's gate, even when no reader and not my B1 placed it. J's rulings of 13 October stopped that from packet 4's item 401, and the 378 rulings that did it were re-ruled at B4a-05. No ruling in packets 1 to 5 now holds a theme no placement held, and no `also_present` lists a theme no reader and not my B1 named.

## J's rulings on themes added (QB4-001), and the re-ruling of packets 1 to 4

I asked J at B4a-03 (QB4-001) whether to keep adding a one- or two-concept theme that no placement held. Meanwhile packet 4 was ruled as packets 1 to 3 were. J answered at 06:43 Berlin on 13 October: "Ask it to stop. The point is to try to adjudicate. I imagine that the additions are really just the analyst trying to be nice. And not go back on what others said". J's rulings at 06:45 and 06:47 Berlin:
1. The placements are the readers' and the analyst's (my B1). A ruling chooses among those placements and adds no theme beyond them.
2. A ruling takes the union of placements only when it names, for each theme it keeps, the separate concept that carries it; otherwise it chooses.
3. Re-rule only the items in packets 1 to 4 whose ruling holds a theme no placement held, under (1) and (2), and keep the superseded ledger.

Items 401 to 461 of packet 4 were ruled under (1) and (2) at B4a-04. At B4a-05 the rest were re-ruled under (3): 378 rulings, packet 1 30, packet 2 58, packet 3 157, packet 4 133. Every other ruled line already named a concept of its own for each placed theme, so rule (2) reached no other line. Each re-ruled line went through `b4_rule_append.py --replace`, which stamps it revised at leg B4a-05 and keeps the old ledger as `disagreements.superseded-<time>.jsonl`; thirteen such files were written, one per part.

The method, written in the diary before the first re-ruled line, and applied to packet 5:
- **The removed theme's concepts.** Each is read against the tests of the themes the placements hold. A concept counts toward a placed theme when that theme's `must_show` takes it and no field sends it to another placed theme. A `must_not_show` that sends it to a theme no placement holds does not stop it. Otherwise the concept is left out and named in the why.
- **Rule 0 inside the placements.** Order the placed themes by concept count, ties by how many of reading A, reading B and my B1 hold the theme; place at most three. A one- or two-concept placed theme is kept when it leads its level on placements; where placed themes tie at a level, none is kept and the tie ends the order. Where the top of the order is a tie on both concepts and placements, all the tied themes are placed (Clannad t05, Fez t06, Dustforce t08, aceattorney t10, androidgaming t06 in packet 5). Themes of three concepts or more tied on placements at the limit of three are left out together. A placed theme the old ruling cut by the limit of three may now enter.
- **Unresolved** where no placement's test takes the material.

What the re-ruling did, in the order met:
- **Calls to defend.** Packet 2's T3-002|T3-005 paragraph had sent a call to defend with no attack in the words to T3-002. Where no placement held T3-002, the call counts toward T3-005, whose `must_show` names "calls to defend". 28 packet 4 rulings changed this way. In packet 2 the move ran the other way where T3-002 was the placement and T3-005 was not (prequelmemes t02, monalisaclan t02).
- **The homeland flag.** The reading of packets 3 and 4 had sent the flag's build, repair and calls for hands to T3-065, which no reader placed in packet 4 and which my B1 seldom held. Calls to defend it now count toward T3-005; its repair and upkeep toward T3-021; its design and spot toward the readers' T3-004 or T3-020; its expansion toward a placed T3-041 or T3-061. 31 packet 4 rulings changed this way; in packet 3 the readers' T3-004 and T3-020 took most of it.
- **A further piece.** Packet 3's T3-033|T3-041 paragraph sent a proposal beside a standing mark to T3-041. Where no placement held T3-041, it counts toward the readers' T3-033 (proposals), T3-038 (placing and progress) or T3-004 (letters, size).
- **Reports of how the work fared** (T3-073) count toward T3-005 where a reader placed the alarm there, toward a placed T3-021 when they report damage to be fixed, and are otherwise left out.
- **Earlier corrections undone.** Four corrections made at B4a-03 had moved a ruling to a theme no placement held: catalonia t07 (back to the readers' T3-004), sadboys t03 (my B1's T3-069), bisexual t04 (T3-003) and kpop t05.
- **Placed themes the old limit of three had cut now enter**, by rule 0 inside the placements. In packet 4: T3-141 (homestuck t04, malaysia t04, taiwan t05, theexpanse t05), T3-088 (rocketbeans t05), T3-042 (lebanon t03, mindcrack t02, loliconsunite t02, hentai t03), T3-087 (masseffect t06, roosterteeth t04), T3-145 (croatia t05), T3-081 (PORTUGALCARALHO t02), T3-146 (israel t02), T3-022 (edmontonoilers t04) and others. Most are my B1's.
- **Unresolved rose by three**, all in packet 1: weezer t13, nbaspurs t17 and rainbowgrid t06, where no placement's test takes the material.

The next table sets the agreement and the named_neither count of packets 1 to 4 at B4a-04 and now, after the re-ruling and the `also_present` correction, with the definitions of the agreement section below.

| | rulings | mean Jaccard after, B4a-04 | mean Jaccard after, now | primary after, B4a-04 | primary after, now | named_neither, B4a-04 | named_neither, now |
|---|---|---|---|---|---|---|---|
| packet 1 | 491 | 0.633 | 0.656 | 0.697 | 0.717 | 84 | 58 |
| packet 2 | 447 | 0.603 | 0.638 | 0.706 | 0.721 | 155 | 117 |
| packet 3 | 500 | 0.473 | 0.583 | 0.535 | 0.637 | 280 | 173 |
| packet 4 | 461 | 0.562 | 0.640 | 0.671 | 0.726 | 222 | 137 |
| packets 1 to 4 | 1899 | 0.565 | 0.628 | 0.649 | 0.698 | 741 | 485 |

Packet 4's two parts, re-ruled: items 1 to 400, mean Jaccard after 0.625 against 0.512 before, primary after 0.702 against 0.652; items 401 to 461, 0.726 against 0.566, primary 0.883 against 0.820. The two parts hold different families (G08 to G10; G11), so the gap between them is not the rule's effect alone.

Agreement after rose in every packet. Part of the rise is mechanical: a theme no reader placed lowers both readers' Jaccard against the ruling, and those themes are gone. The rest is the readers' themes coming back where my additions had displaced them. Neither is evidence that the rulings are right.

## J's ruling on also_present (09:09 Berlin), QB4-002, and the correction

The PI's message at 07:09 UTC carried J's ruling of 09:09 Berlin on bakchodi t09: "rule (1) extends to also_present. also_present lists only themes that a reader or your B1 named. Apply it to the rulings you write from now on and to the ledger's existing also_present entries, keeping the superseded ledger. In bakchodi t09, T3-006 came from neither reader nor B1." I asked J (QB4-002) whether a theme a reader listed under its own `also_present` counts as named by that reader. J's answer (09:20 Berlin): "yes. A theme a reader listed under its own also_present counts as named by that reader. also_present may list themes a reader placed, a reader listed under its own also_present, or your B1 named; nothing else. Restore any entries your interim reading removed that this admits."

What was done:
- **The scan.** `out/_analysis/b4_ap_scan.py` (new, read-only) compares each ruled line's `also_present` with the themes the readers placed, the readers listed under their own `also_present`, and my B1 named. 128 lines in packets 1 to 4 listed a theme outside that set (packet 1 5, packet 2 32, packet 3 46, packet 4 45): 273 entries. The themes dropped most often: T3-002 29, T3-004 17, T3-041 16, T3-170 14, T3-073 14, T3-065 9, T3-070 8.
- **The correction.** Each line went through `b4_rule_append.py --replace` with the dropped themes named in its why. Four parts, each keeping the old ledger: `disagreements.superseded-20261013T072151Z.jsonl`, `-072154Z`, `-072158Z`, `-072202Z`.
- **Four bags re-ruled by hand.** Their `also_present` lost every theme at the three-concept floor, so they stopped being bags: archlinux t01 (packet 2, genuine-joint, T3-014, T3-013 and T3-152), ireland t04 (packet 3, author-disagrees, T3-004 and T3-080), starvstheforcesofevil t02 (packet 3, author-disagrees, T3-002 and T3-033), de t02 (packet 4, author-error, T3-005 and T3-021).
- **What stays.** 84 lines keep a theme that only a reader's own `also_present` named; QB4-002 admits those. Before J's answer I had read the ruling as placed themes only. That reading was used for a dry run only and removed nothing from the ledger, so nothing had to be restored.
- **From packet 5 on,** a ruling's `also_present` lists only placed themes.

## author-error and author-disagrees

author-error: 334 (packet 1 99, packet 2 61, packet 3 55, packet 4 78, packet 5 41). author-disagrees: 208 (packet 1 36, packet 2 62, packet 3 44, packet 4 22, packet 5 44). Both come almost wholly from class 4, where the readers agreed on a list my B1 grouping did not hold.

The next list gives, by packet, the class 4 items counted by what the ruling holds (`b4_packet_detail.py`), whatever their taxonomy value:
- **Packet 1:** the readers' list taken 97, a B1 theme kept 32, an empty ruling 23, other 1.
- **Packet 2:** the readers' list taken 64, a B1 theme kept 54, empty 4, other 2.
- **Packet 3:** the readers' list taken 59, a B1 theme kept 56, other 2.
- **Packet 4:** the readers' list taken 67, a B1 theme kept 34, other 4 (bags).
- **Packet 5:** the readers' list taken 42, a B1 theme kept 44.

Over the five packets the readers' list was taken in 329 class 4 items and a B1 theme kept in 220.

Two labels do not match the measure, and are carried as they stand because J's rule (3) re-rules only rulings that held a theme no placement held. In packet 4, 12 author-error rulings from items 401 to 461 keep a B1 theme beside the readers' list (bih t02, smashbros t06, yogscast t02, twitchplayspokemon t08, vinesauce t05, orderofthebluecorner t08, babymetal t12, bostonbruins t09, formula1 t15, thetreesnetwork t06, costa_rica t07, TheHulk t06); by §7 they are author-disagrees. In packet 2, two author-disagrees rulings take the readers' list. Counted by what the rulings hold, author-error would be 324 and author-disagrees 218.

I cannot separate how much of each packet's split is the scheme and how much is my pull toward my own grouping. The blind sample at B4b tests the adjudicated stratum against fresh readers, and these items are part of it.

My commonest B1 errors:
- **Packet 1:** T3-031 placed on an in-joke with no canvas in it; T3-001 placed where nothing was posted as true; T3-063 on posts that are not canvas posts; T3-032 where the complaints were about the sub's own joke styling.
- **Packet 2:** calls for hands that my B1 had placed as the proposal (T3-033), the progress (T3-038) or a further piece (T3-041); placing troubles on the timer, a glitch or a phone (T3-074, 6); posted templates that my B1 had placed as one plan imposed (T3-091).
- **Packet 3:** links and coordinates that only show where the finished mark is (T3-026, 11 rulings); the readers' T3-004 (8), T3-033 (8) and T3-020 (7).
- **Packet 4:** in author-error rulings, the readers placed T3-005 (11), T3-170 (11), T3-021 (8), T3-088 (7), T3-087 (6) and T3-188 (4) where my B1 did not. Seven of the T3-088 items are glitches used to place more, which my B1 had put under T3-074; T3-088's `decide_when_both` gives "using one to place beyond the limit" to T3-088.
- **Packet 5:** in author-error rulings, the readers placed T3-006 (8), T3-010 (7), T3-068 (4), T3-084 (3), T3-151 (3) and T3-137 (3) where my B1 did not. The three T3-137 items (borussiadortmund t04, hearthstone t12, paladins t19) are members whose effort moved to another room's build, which T3-137's `decide_when_both` sends there and my B1 had put under T3-011. In vietnam t05 my B1's T3-099 rested on knowing r/osugame was large; the words do not say so.

The themes I kept against both readers in author-disagrees rulings: packet 4 T3-021 6, T3-170 4; packet 5 T3-010 7, T3-150 6, T3-061 5, T3-151 4, T3-039 4.

## Fields by ambiguity

The next list counts the 350 scheme-ambiguous rulings by the field whose sentence failed, with packets 1 to 5 in brackets.

- must_show: 196 (76, 33, 51, 34, 2)
- discriminators: 78 (39, 17, 16, 2, 4)
- must_not_show: 48 (2, 6, 24, 8, 8)
- decide_when_both: 28 (4, 6, 3, 15, 0)

At B4a-04 `must_not_show` held 66, and 32 in packet 4; the re-ruling took packet 4's to 8, because the homeland flag's repair now counts toward the readers' T3-021. Packet 3 keeps 24: there the readers' own T3-004 and T3-020 took the flag's look and spot, and the split still turns on those themes' `must_not_show` lines. Packet 5's eight `must_not_show` failures are all single sentences, listed below.

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, over the five packets. Stage C1 opens with it.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-033 | 33 | 31 | 1 | 0 | 1 |
| T3-017 | 30 | 6 | 0 | 1 | 23 |
| T3-023 | 25 | 23 | 0 | 0 | 2 |
| T3-001 | 24 | 18 | 0 | 0 | 6 |
| T3-004 | 22 | 4 | 10 | 0 | 8 |
| T3-002 | 13 | 0 | 2 | 3 | 8 |
| T3-038 | 12 | 10 | 2 | 0 | 0 |
| T3-005 | 12 | 4 | 0 | 7 | 1 |
| T3-073 | 9 | 9 | 0 | 0 | 0 |
| T3-063 | 8 | 6 | 1 | 0 | 1 |
| T3-095 | 7 | 3 | 0 | 2 | 2 |
| T3-021 | 7 | 4 | 3 | 0 | 0 |

70 more themes failed on 148 rulings between them. Packet 5's T3-006 has 5 (four on its discriminator, one on its `must_not_show`).

The sentences that failed most:
- **T3-033's `must_show`** "An idea of what the room should put on the canvas, offered to the room" (31). It does not say "first". T3-041's `must_not_show` gives "The room's first mark proposed" to T3-033, so a further piece beside a standing mark is T3-041, and readers placed it as T3-033 (conflict CC-019).
- **The homeland flag in the siblings' `must_not_show` lines** (packet 3 24, packet 4 1). T3-065's `must_show` takes the flag of the room's land, its proportions, its spot, its repair and calls for hands to it. No sibling's `must_not_show` says so. In packet 3 the failures fall on T3-004's (10), T3-020's (6), T3-041's (4), T3-038's (2), T3-033's and T3-082's.
- **T3-073's `must_show`** "What happened to the work told: live reports of changes and attacks, what survived, what was moved and why, the story of its fights afterwards" (packet 4, 7). "live reports of changes and attacks" overlaps T3-005's "alarms".
- **T3-005's `decide_when_both`** "T3-005 when the attack and the fight lead, T3-021 when the watching and fixing do" (packet 4, 7). It names no tie.
- **T3-005's `must_show`** (4). The attack or its target is not in the words.
- **T3-027's `decide_when_both`** (packet 4, 6). "T3-028 primary when the scripts are run" does not say how much running; "goes here when fairness is in question" leaves bot claims with no fairness argued without a home.
- **T3-006's discriminator** "Is the rival's work destroyed (T3-006), or is its space taken for the room's own work (T3-061)?" (packet 5, 4: borderlands t05, armenia t05, kurdistan t02, polska t05). A call to "take over" or "invade" a neighbour's flag reads as an attack to one reader and as space taken to the other. The T3-006|T3-061 paragraph counts it toward T3-061 when the words take the space.
- **T3-022's `must_show`** (packet 4, 3). "crowded out" with no attack reaches a foothold lost before the mark stood.
- **T3-038's `must_show`** "Placing the mark and reports of its state" (packet 3, 9). It does not say "first".
- **T3-017's discriminator** (packet 1). Its "or the day" contradicts T3-031's own canvas condition.
- **T3-023's** "A change made to a whole sub for April Fools" and **T3-001's** "Members of the room themselves post something false as true for April Fools" (packet 1).

Single failures for stage C1's list. From packets 3 and 4: T3-092's own example "I added a little something for my bias" against its discriminator toward T3-060 (bangtan t10); T3-082's "the room's subject" against "the room's own mark" (furry t01); T3-006's `must_not_show`, which does not name T3-171 for a colour faction spreading; T3-089's `must_show`, which names "a neighbour's agreed space" that T3-168 also takes (afip t05, malaysia t05); T3-088's `decide_when_both`, which does not say whether a concept holding both a script and accounts counts (iastate t02, uoft t13); T3-027's `must_show`, which leaves an argument over the fairness of throwaway accounts with no home (TransFlagPlace t09). From packet 5:
- **T3-006's `must_not_show`** (penguins t09): one pixel left in a rival logo; the words do not say whether it was for fun (T3-192) or for the room's ends.
- **T3-046's `must_not_show`** (anarchism t11): it does not send an ideological argument made from the flag to T3-179, though T3-179's `must_show` names it.
- **T3-150's `must_not_show`** (ice_poseidon t15): two rooms agreeing to destroy a third room's banner is an alliance for a fight and a third room's work given up in a bargain (T3-067); neither field sends one to the other.
- **T3-010's `must_show`** "overlaps accepted or refused" (japan t10): it reaches a neighbour allowed onto the room's work, which T3-012's `must_show` names.
- **T3-194's `must_not_show`** "the deal itself" (pusheen t02): a plan put up for another room's comment is neither a settled deal nor a request for a held spot.
- **T3-078's `must_not_show`** (GranColombia t09): kinship carried by the venue and the request, not stated in the words.
- **T3-013's `must_not_show`** (Cornwall t01): an invitation to join kindred regional neighbours could be a hub or a call for hands (T3-062).
- **T3-115's `must_not_show`** (england t05): "No These /r/place spam posts are getting on my tits" is a refusal (T3-115) and a complaint about the flood (T3-075), and neither field decides.

## The named_neither rate

named_neither: 616 of 2,308 (26.7%). Packet 1: 58 of 491 (11.8%). Packet 2: 117 of 447 (26.2%). Packet 3: 173 of 500 (34.6%). Packet 4: 137 of 461 (29.7%). Packet 5: 131 of 409 (32.0%). At B4a-04 the figure over packets 1 to 4 was 741 (39.0%).

Every named_neither ruling keeps a theme from my B1 grouping that neither reader placed; none holds a theme no placement held. 186 of the 616 are author-disagrees. The next list splits them by packet:
- **The primary itself chosen by neither reader:** packet 1 31, packet 2 38, packet 3 53, packet 4 19, packet 5 30.
- **How many themes the ruling places:** packet 1 one 28, two 17, three 13; packet 2 15, 58, 44; packet 3 19, 63, 91; packet 4 7, 41, 89; packet 5 11, 31, 89.
- **The B1 themes kept most often:** packet 1 T3-017 17, T3-048 7, T3-023 6; packet 2 T3-069 11, T3-084 9, T3-041 9; packet 3 T3-041 17, T3-070 11, T3-113 10; packet 4 T3-087 14, T3-042 11, T3-021 9, T3-170 7, T3-141 6; packet 5 T3-150 14, T3-010 11, T3-151 11, T3-061 9, T3-012 7, T3-039 7.

My reading of it. named_neither now measures one thing: my B1 grouping kept against both readers. Two causes remain, and I cannot weigh either against my own pull:
- **Primaries moved by count.** Where a theme held more concepts than the readers' primary, it went first, even when both readers agreed on the primary.
- **Rule 0 inside the placements.** A one- or two-concept B1 theme that leads its level on placements is kept. Where the readers each placed one theme and my B1 placed three, the rule often keeps my third: 89 of packet 5's 131 named_neither rulings place three themes. In packet 5's class 4 items the rule kept a B1 theme in 44 and took the readers' list in 42. In two of its chunks, my B1 theme was kept in 7 of 7 and 8 of 9 class 4 items.

Rule (2) permits the union only with a separate concept per theme, and every kept theme has one; it does not require the union, and the rule 0 I apply inside the placements keeps more of my B1 themes than a choice would. The blind sample's adjudicated stratum will show whether strangers reach these three-theme rulings.

## The unresolved count

unresolved: 85 of 2,308 (3.7%). Packet 1: 55 (11.2%). Packet 2: 10 (2.2%). Packet 3: 7 (1.4%). Packet 4: 10 (2.2%). Packet 5: 3 (0.7%). The next lists name them by the reason the scheme did not decide.

Packet 1, added at the re-ruling (no placement's test takes the material):
- **weezer t13** (T3-017's discriminator). A running joke with no April Fools marker and no canvas: reader A's T3-001 needs a fake posted for April Fools, reader B's and my B1's T3-031 needs canvas talk.
- **nbaspurs t17** (author-disagrees). A moderator asks for a new downvote image: both readers' T3-023 needs an April Fools change, and my B1's T3-066 needs the room to decide.
- **rainbowgrid t06** (T3-064's `must_show`). Members show the rainbow grid and say a promotion on r/place was downvoted: both readers' T3-064 needs the room's own joke taken elsewhere.

Packet 1, ruled so at B4a-01:
- **April Fools play not posted as true** (the gap; T3-001 `must_show`), 13: 4chan t11, bisexual t09, schoolidolfestival t11, thesimpsons t03, 49ers t03, danganronpa t23, falcons t09, parahumans t07, berserk t04, GuildWars2 t07, vim t01, wholesomememes t14, portugal t15.
- **Another sub's change** (T3-023 `must_show`), 8: flashtv t14, megaman t04, iastate t01, katawashoujo t02, winnipegjets t03, Braveryjerk t01, liverpoolfc t03, bostonceltics t03.
- **The item shows no doing, or both readers placed what the words do not support** (author-disagrees), 8: lebanon t09, archlinux t12, greenbaypackers t05, python t09, 4chan t06, FlipnoteStudio3D t02, morrowind t11, catalonia t04.
- **Moderators applying standing rules to non-canvas posts** (T3-063 `must_show`, conflict CC-004), 6: yugioh t06, yugioh t12, metalcore t07, oneplus t05, twice t04, flashtv t10.
- **Whose joke is not shown** (T3-001 discriminator), 5: oneplus t09, danganronpa t19, kamenrider t07, lego t07, ubreddit t02.
- **A record of the change, not the change kept** (T3-100 `must_show`), 2: survivor t18, survivor t11.
- **Waiting for or remembering the sub's own joke** (T3-048 and T3-095 `must_show`), 2: halo t01, polandball t01.
- **A defence of the sub's own joke against too few objections** (T3-032 `must_show`), 2: ethereum t12, denverbroncos t02.
- **Single reasons**, 6: kurdistan t06 and lakers t07 (T3-095 discriminator); bardmains t09 (an April Fools joke's limits); de t22 (suspicion of the platform's motives); mindcrack t07 (nothing asked or settled); stardustcrusaders t21 (the pointer is not shown).

Packet 2:
- **One concept with no doing to place**, 6: minecraft t17, popheads t01, h3h3productions t27, shield t07, kuwait t09, minecraft t18.
- **A pointer to another sub's thread on the room's canvas work** (T3-015 `must_show`), 1: Redox t02.
- **Naming a feature of a colour faction's ground** (T3-070 `must_show`), 1: orderofthebluecorner t02.
- **A bare question with no answer** (T3-018 and T3-073 `must_show`), 2: THE_R t03, parrots t15.

Packet 3. All seven are one surviving concept or one exchange; conflict CC-025 names six of them: quebec t16 and bahrain t09 (a title with its body deleted), davidbowie t04 (T3-033 `must_show`), tampabaylightning t09 (T3-017 `must_show`), h3h3productions t30 (T3-049 `must_show`), AMD t20 (T3-003 `must_show`), samuraijack t25 (T3-052 `must_show`).

Packet 4:
- **The attack or its target not shown** (T3-005 `must_show`), 2: linux t01 and osu t15.
- **Who changed the work not shown** (T3-087 `must_show`), 2: cavestory t06 and Dominican t09.
- **Whose work not shown** (T3-139 `must_show`), 1: kpop t13.
- **When or at whom the blame was laid not shown** (T3-058), 2: DestinyTheGame t14 and notredame t10.
- **One act that meets two themes** (T3-068 `must_show`), 1: hungary t05.
- **Five acts of one concept each** (T3-192 `must_show`), 1: dallasstars t01.
- **A bot claim with no fairness in question, told after the loss** (T3-027 `decide_when_both`), 1: tampabaylightning t15.

Packet 5:
- **linux t03** (T3-137's `must_not_show`). The one concept, "/r/erasetheplace I'm writing a bot.", joins an outside sub's plan (T3-137, my B1), and that plan is to erase the canvas (T3-006, reading A). Neither theme's `must_not_show` sends the other's act away, and each holds one placement.
- **survivor t26** (T3-058's `must_show`). One member changes a Danish coworker's computer background at lunch. T3-058 needs blame laid in words; T3-178 needs members acting together.
- **PurplePixels t13** (author-disagrees, the packet's one class 5 item). Only the title "A request for the Purple Pixels..." survives; help (T3-084), space (T3-035) and a host's ruling (T3-162) would each take it. Both readers placed T3-084.

## The boundary rulings

Each pair is one paragraph in `boundaries.md`. Each paragraph's ruling is summarised here with its item list.

### Packet 1

**T3-001|T3-023, the joke's stage (32 items).** A change to the sub's name, look, rules or subject made by its moderators, or by members flooding it "as a sub acting together", is T3-023. Members' own false claims in an unchanged sub are T3-001. Both, each with concepts of their own: the larger primary. Items: aceattorney t01, MMA t02, nlsscirclejerk t08, rit t02, totallynotrobots t06, totallynotrobots t08, AceOfAngels8 t01, clashroyale t03, enterthegungeon t02, flyers t05, furry t09, harrypotter t06, kilian t08, mylittlepony t08, porterrobinson t08, porterrobinson t09, ss13 t01, teslamotors t01, toolband t02, totallynotrobots t02, totallynotrobots t03, totallynotrobots t04, totallynotrobots t07, OneTrueEmilia t01, apocalypserising t01, formula1 t02, greece t07, polska t03, thetreesnetwork t02, totallynotrobots t01, ubc t02, zootopia t01.

**T3-001|T3-048, whose joke (20 items).** The source shown in the concepts decides. Where it cannot be read, the ruling is unresolved. A member relaying an organisation's joke is T3-048 by the discriminator (conflict CC-002). Items: btc t04, bitcoin t06, feedthebeast t02, opticgaming t01, uofmn t01, baylor t02, GuildWars2 t01, GuildWars2 t10, runescape t07, rutgers t01, starlightstage t03, warframe t15, yugioh t10, yugioh t11, danganronpa t19, falcons t10, kamenrider t07, lego t07, simonfraser t02, ubreddit t02.

**T3-017|T3-031, the canvas condition (15 items, with T3-001|T3-031: rwby t03).** T3-031's own test governs: an in-joke with no canvas in it is T3-017. Every item is scheme-ambiguous on T3-017's discriminator. Items: cubers t30, ethereum t06, falcons t08, flashtv t04, freedomplanet t05, h3h3productions t06, h3h3productions t12, heyyea t07, indieheads t06, mls t07, PlaceNL t20, romania t22, SydneyFC t03, tf2 t09, torontoraptors t03.

**T3-001|T3-095, who staged the claim (8 items).** A test of a member's own fake is T3-001; a test of anyone else's claim is T3-095. Items: linux t04, planetside t01, romania t12, swordartonline t03, thesimpsons t02, worldoftanks t02, fivenightsatfreddys t03, hearthstone t01.

**T3-023|T3-095, playing inside or working out (7 items).** Items: paragon t08, hawks t07, smashbros t01, criticalrole t02, ElderScrolls t01, h3h3productions t23, transformers t01.

**T3-048|T3-095, open or known (6 items).** Items: clg t08, gameofthrones t09, paladins t01, thesilphroad t02, btc t01, loltyler1 t01.

**T3-032|T3-097, the jokes or the look (5 items).** Items: anime_irl t16, anime_irl t17, hunterxhunter t03, pcmasterrace t02, survivor t10.

**T3-063|T3-185, applied or made (5 items).** Items: anime_irl t05, destiny t06, ss13 t11, russia t12, leafs t12.

**T3-001|T3-017 (4 items):** ohio t01, homelab t03, planetside t05, titanfall t03. **T3-015|T3-063 (4):** fireemblem t08, futanari t06, serbia t15, stardustcrusaders t21. **T3-023|T3-051, upvote bargains (4; CC-007):** partyparrot t16, titanfall t05, warframe t06, warriors t04. **T3-031|T3-048 (3) and T3-023|T3-031 (1):** GuildWars2 t02, GuildWars2 t05, rocketleague t15; stardustcrusaders t10. **Single items:** rit t01, wallstreetbets t03, redhotchilipeppers t04, 4chan t12.

### Packet 2

**T3-002|T3-033, a call or a new mark (20 items).** A concept naming a new mark for the room counts toward T3-033, even when it also asks for help. A call to a mark already named counts toward T3-002. A tie goes to T3-002 when the mark was already chosen, and to T3-033 when it was not. Items: androidgaming t01, anime t01, chicago t01, clashroyale t02, criticalrole t03, drumcorps t05, nascar t06, onepunchman t01, polyamory t01, rutgers t03, seahawks t01, TheAdventuresofTintin t01, twentyonepilots t02, chess t07, nlsscirclejerk t01, nonbinary t01, opticgaming t03, uiowa t01, gameattack t03, bigbang t01.

**T3-002|T3-038, a call or the work's progress (19 items).** Calls, volunteers and answers count toward T3-002; placing and reports of the work's state toward T3-038. Items: auburn t01, bindingofisaac t02, dallasstars t05, ghibli t01, gorillaz t03, newzealand t07, shrooms t06, streetfighter t04, transformers t02, bangtan t01, battlecats t05, cloud9 t03, FinalFantasy t02, foxstevenson t02, torontoraptors t04, traaaaaaannnnnnnnnns t01, rutgers t05, smashbros t04, xenoblade_chronicles t02.

**T3-014|T3-153, the room's own chat or a meeting place (18 items).** Another room must be in the chat in the words. Items: armenia t08, bangtan t04, belgium t03, dmt t03, eve t10, FederationPlace t06, giivasunner t12, GreenCorner t02, metalgearsolid t08, ohio t08, paladins t25, placehearts t06, rocketbeans t04, theitalyplace t07, AcePlace t06, aoe2 t07, araragi t03, iceland t05.

**T3-002|T3-070, a call or directions (13 items).** Items: bardmains t01, danganronpa t03, dankmemes t15, python t06, witcher t01, clg t01, harrypotter t15, cowchop t01, mysterydungeon t01, paragon t01, shield t01, Moondye7 t02, seventeen t01.

**T3-002|T3-005, a rally or a defence (12 items in packet 2; 3 more in packet 4).** The attack must be in the words. A call to "protect" a mark with no attacker in view is T3-002. Under J's rulings this sends a call to T3-002 only where a placement holds T3-002; where none does, the call counts toward T3-005, whose `must_show` names "calls to defend". Packet 2 items: btc t02, Clannad t02, crusaderkings t01, FlaggyFlag t02, harrypotter t01, monalisaclan t02, ohio t03, czech t01, malta t02, nin t10, thetreesnetwork t01, prequelmemes t02. Packet 4 items: masseffect t01, sooners t08, anarcho_capitalism t04.

**T3-070|T3-091, directions or one plan (7 items; CC-012):** stlouisblues t01, FloydVsVoid t02, heyyea t01, starryknights t02, ChronoTrigger t02, mylittlepony t04, PlaceNL t01. **T3-004|T3-070, the design or its directions (6 items):** berserk t06, foxstevenson t03, nyu t01, pitt t02, muse t02, suomi t06.

### Packet 3

**T3-033|T3-041, the first mark or a further piece (25 items; CC-019).** A proposal counts toward T3-041 when the room's mark already stands or is chosen. Items: truestl t02, cmu t01, metalgearsolid t04, muse t01, aoe2 t04, denmark t10, eagles t02, eve t03, gameofthrones t02, indieheads t13, KState t01, math t02, nuclearthrone t01, portal t02, purplecorner t03, rust t09, simonfraser t04, splatoon t03, suomi t02, touhou t08, ufl t01, blackmirror t05, borderlands t04, empiredidnothingwrong t11, winnipegjets t11.

**T3-038|T3-041, the first build or a further piece's (16 items).** Items: sakuragakuin t01, jerma985 t03, nuclearthrone t05, bobross t01, cavestory t01, dota2 t11, madokamagica t01, msu t02, parahumans t01, touhou t02, AyyMD t01, cubers t21, cubers t25, samuraijack t10, suomi t27, yumenikki t01.

**T3-004|T3-041, the look or an addition (14 items).** Items: ubreddit t03, ElderScrolls t05, funhaus t01, nin t03, radiohead t01, skyrim t02, bindingofisaac t03, DatBoi t04, factorio t09, placetardis t02, ProfessorLayton t02, starlightstage t12, borderlands t02, enterthegungeon t03.

**T3-004|T3-169 (8 items; CC-022):** bisexual t03, greyblob t02, monstercat t06, unturned t09, drawhelix t05, farmcarrots t08, neopets t14, wine t08. **T3-004|T3-038 (8):** portal t01, timbers t02, AvoArmy t01, calgaryflames t01, uoft t08, bitcoin t02, detroitlions t04, paydaytheheist t02. **T3-038|T3-070 (7):** berkeley t03, gameattack t04, virginiatech t03, planetside t08, bdsm t01, re_zero t06, formula1 t06. **T3-004|T3-020 (7):** blackmirror t02, borussiadortmund t03, minecraft t04, kingdomhearts t12, oneshot t01, nightinthewoods t02, utaustin t01. **T3-004|T3-033 (6):** frc t01, nlsscirclejerk t02, WPI t01, redhotchilipeppers t03, starlightstage t09, yugioh t04. **T3-020|T3-033 (1):** tetris t01.

**Carried from packet 2 into packet 3.** T3-002|T3-033 (10 items): chicubs t09, DiamondClub t01, foxes t01, hawks t05, kanye t01, schoolidolfestival t04, stardustcrusaders t01, unturned t03, wallstreetbets t01, warframe t01. T3-002|T3-038 (9 items): bostonbruins t02, enterthegungeon t01, ethoslab t01, forsen t01, habs t02, nyjets t04, the_pack t01, winnipegjets t01, wow t17. T3-004|T3-070 (9 items): crusaderkings t02, penguins t03, udub t01, drumcorps t06, kanye t05, Okami t06, pebble t04, placesnek t04, portal t03.

Readings written during packet 3: the homeland flag's look (T3-065, emblems T3-113); a design cut down to the hands (T3-004; T3-069 only when a piece is dropped for another; T3-042 when growth is set aside); a celebration while placement goes on (T3-009 for "done" celebrated, T3-026 for "up" or "for now").

Under J's rulings each paragraph and reading sends a concept to its theme only where a placement holds that theme. At the re-ruling, where no placement held T3-041, T3-065 or T3-113, the concept went to a placed theme whose `must_show` takes it. The items keep their `boundary_ruling` tag, since the pair was still the split.

### Packet 4

Four pairs split five or more of packet 4's items on their primaries and were ruled before its first item. Three more were ruled at item 401, when G11's pairs were met. The item lists are the packet 4 items that carry the pair in `boundary_ruling`.

**T3-005|T3-021, a fight or upkeep (90 items after the re-ruling, 67 at B4a-04; B2's predicted pair 1; conflict CC-026).** Ruled as written by the discriminator and T3-005's `decide_when_both`. A concept counts toward T3-005 when an attack on the room's work is in the words and the room answers it as a fight: an alarm, a call to defend or fight back, holding the line, an attack reported repelled. A concept counts toward T3-021 when it watches or fixes, "with or without an attacker in view, where no fight is called". The Void, a named room or a bot eating the work is an attacker in the words. Naming who did it goes to T3-087, a watch through the night to T3-141 (CC-032), a script that repairs to T3-028 (CC-028), upkeep argued over growth to T3-042 (CC-027). Where count and placements both tie, the item is scheme-ambiguous on T3-005's `decide_when_both`, which names no tie, and both themes are placed. Items: aggies t03, aoe2 t05, archlinux t04, austria t05, bangtan t06, bostonbruins t06, clg t04, cubers t10, earthbound t04, factorio t07, flashtv t09, frankocean t10, furry_irl t12, gorillaz t06, gravityfalls t02, GreenCorner t03, hellointernet t02, HomestarRunner t03, homestuck t04, india t13, leafs t02, leagueoflegends t16, malaysia t04, mindcrack t02, nyjets t08, palestine t04, parrots t09, Peru t07, PinkVomitMonster t02, placestart t14, placetardis t03, portal t07, PORTUGALCARALHO t02, reddevils t15, rocketbeans t05, roosterteeth t04, serbia t08, shield t03, smite t06, ss13 t06, stardewvalley t03, taiwan t05, tf2 t12, TheFarLeftSide t03, theitalyplace t01, TransFlagPlace t03, warriors t08, afip t04, androidgaming t03, cavestory t02, chile t03, ChronoTrigger t03, clubpenguin t09, daftpunk t05, FinalFantasy t05, gameofthrones t14, israel t02, jerma985 t04, korea t09, metroid t09, MonkeyIsland t03, muse t05, necrodancer t05, oneshot t04, pakistan t05, partyparrot t02, placeportalpattern t06, ScottPilgrim t03, simonfraser t09, stlouisblues t08, tagpro t03, tampabaylightning t03, TeamDignitas t04, texas t02, redhotchilipeppers t08, anaheimducks t09, animalcrossing t04, AyyMD t02, cloud9 t07, DestinyTheGame t08, dragonquest t02, feedthebeast t07, kingdomhearts t20, placeDE t03, sheffield t02, starcraft t07, tf2 t11, theexpanse t05, thenetherlands t04, touhou t04.

**T3-005|T3-073, an alarm or a report (7 items).** A report addressed to the room so that it acts counts toward T3-005. A report of what changed, survived or was lost, with no call to fight, counts toward T3-073. Items: apocalypserising t05, terraria t08, 4chan t08, anime t11, bakchodi t06, neutralmilkhotel t03, texastech t03.

**T3-021|T3-038, first build or restored (3 items; CC-017).** The same spot rebuilt after a loss is T3-021; a rebuild at a new spot is T3-022. Items: nerf t02, pitt t03, telegram t03.

**T3-005|T3-038 (5 items split; none tagged).** Placing the first build counts toward T3-038; an attack answered as a fight toward T3-005.

**T3-020|T3-022, the first spot or a move after a loss (5 items; CC-033).** A spot found, tested or changed before the mark stands counts toward T3-020. A move or restart after the work was destroyed, overpowered or crowded out counts toward T3-022. Items: mordhau t04, rutgers t04, toolband t04, dallasstars t13, detroitredwings t04.

**T3-027|T3-028, arguing scripts or running them (4 items; CC-029).** Each concept counts toward the act it does, and the larger part leads; a tie goes by placements. A script shared to wreck another room's work is not "for the room's work". Items: pakistan t08, giantbomb t07, placecanada t12, placeDE t07.

**T3-027|T3-087, a bot claim or a culprit traced (4 items).** Bots or new and empty accounts named as the source of damage while placement goes on count toward T3-087; bots judged unfair count toward T3-027. Items: shitredditsays t05, sooners t10, tampabaylightning t15, foxes t04.

**T3-089|T3-168, a stale script or a neighbour spared (2 items).** A call to stop or change the room's scripts so a neighbour's work stands counts toward T3-168. Items: afip t05, malaysia t05.

**T3-005|T3-006 (CC-031)** and **T3-058|T3-073 (CC-034)** reached four items and were decided by their discriminators as met. One item carries T3-005|T3-006: rocketbeans t07.

Two readings written in packet 4 (the homeland flag kept and defended; a call to fight against a call to defend) were replaced at the re-ruling: each sends a concept to T3-065 or T3-002 only where a placement holds it; otherwise calls to defend count toward T3-005, repair and upkeep toward T3-021, expansion toward a placed T3-041 or T3-061.

### Packet 5

Five pairs split the readings' primaries on five items or more, and were ruled before packet 5's first item (`b4_packet_pairs.py --packet 5`): T3-010|T3-024 17, T3-010|T3-149 10, T3-006|T3-061 8, T3-010|T3-011 7, T3-010|T3-151 7. Every paragraph applies under J's rulings: it sends a concept to its theme only where a placement holds that theme. The item lists are the packet 5 items that carry the pair in `boundary_ruling`. Chunks 6 and 7 and item 409 were tagged after the packet was ruled (nine `--replace` lines, rulings unchanged).

**T3-010|T3-149, a border or a truce (34 items; B2's predicted pair 2; conflict CC-037).** Ruled as written by the discriminator. A concept counts toward T3-149 when a fight, an attack or a threat between the rooms is in the words, or the deal is named peace, truce, ceasefire or non-aggression. A concept counts toward T3-010 when lines, overlaps, moves or shared space are settled and no fight or peace is named. Items: Thegreatblackhole t06, AMD t13, archlinux t03, bindingofisaac t05, detroitlions t06, edboxes t04, faeria t04, FederationPlace t04, finland t02, forsen t03, gravityfalls t05, liverpoolfc t14, newzealand t05, phish t04, placeportalpattern t04, prequelmemes t08, singapore t08, ss13 t09, switzerland t03, teslamotors t10, uiuc t11, uoft t10, worldoftanks t07, cowchop t02, buffalo t04, czech t07, neopets t04, overwatch t19, placesnek t03, soylent t02, sweden t03, titanfall t07, VelvetUnderground t04, colombia t03.

**T3-010|T3-151, a border or help traded (31 items; B2's predicted pair 11; CC-037).** Help offered or asked in return for help or for room counts toward T3-151, whose `must_show` names "maintenance traded for room". A line, overlap or move agreed with no help in the exchange counts toward T3-010. Help counts toward T3-151 only when the words name the return. Items: belgium t11, catalunya t05, chicago t10, chicubs t05, chile t04, Dorset t02, ElSalvador t02, europe t03, factorio t10, ftlgame t03, gameofthrones t13, hearthstone t13, kamenrider t04, littlewitchacademia t05, mls t10, Moondye7 t05, notredame t04, placestart t08, purdue t06, rwby t07, smashbros t08, timbers t03, unturned t05, uwaterloo t07, giivasunner t10, httyd t10, india t04, mylittlepony t07, placecanada t05, southafrica t04, theitalyplace t11.

**T3-010|T3-024, a line agreed or work spared (26 items; B2's predicted pair 13; CC-038).** A concept counts toward T3-010 when the neighbour is in the exchange in the words: a request for room or a line, an answer to one, an overlap accepted or refused. A concept counts toward T3-024 when the room spares the work with no neighbour's word in it. Moving because a neighbour asked is T3-039 where a placement holds it; otherwise the move counts toward T3-010 when the words give the shift agreed. Items: 49ers t05, cirkeltrek t08, geometrydash t08, monsterhunter t04, PurplePixels t05, starcraft t10, TeamYellowPlace t02, asktransgender t03, python t08, aceattorney t09, armenia t04, bisexual t05, czech t06, esperanto t06, GrowTheTree t03, oneshot t03, PlaceNL t07, starbound t04, terraria t03, TransFlagPlace t02, babymetal t05, Fez t06, roosterteeth t05, stardustcrusaders t06, taiwan t06, theexpanse t04.

**T3-006|T3-061, destroying the rival's work or taking its space (18 items; CC-039).** Ruled concept by concept, by what the words say the taking is for. Erase, destroy, ruin, black out, sabotage: T3-006. Expand into, take over for the room's flag, claim territory: T3-061. A bare call to "invade" or "attack" a named neighbour, with no space claimed and no damage named, counts toward T3-006. Four items are scheme-ambiguous on T3-006's discriminator (borderlands t05, armenia t05, kurdistan t02, polska t05). Items: borderlands t05, armenia t05, brasil t05, cirkeltrek t07, ireland t06, newzealand t04, overwatch t25, ukraine t03, utaustin t03, wallstreetbets t06, costa_rica t03, kurdistan t02, polska t05, purdue t08, stlouis t04, thailand t06, PlaceNL t06, teamcube t02.

**T3-010|T3-011, a border or help sent (14 items; CC-037 and CC-043).** Neither theme has a discriminator against the other. Pixels sent to a neighbour's work with nothing asked in return count toward T3-011; lines, overlaps, moves and shared space settled count toward T3-010. Items: sonicthehedgehog t04, cloud9 t09, formula1 t10, masseffect t05, minnesotavikings t12, pathofexile t11, samuraijack t03, sixers t06, transformers t06, Clannad t05, heroesofthestorm t10, nyjets t11, placeDE t04, quebec t04.

Readings applied in packet 5, to carry into the later packets:
- **Fights and deals.** T3-010's "with no fight to end" fails for a concept naming a fight, a threat, peace or a truce, even where no placement holds T3-149. A truce invoked against a breach is T3-195.
- **Help.** A request for help is T3-084 by T3-011's `must_not_show`; help sent with nothing asked is T3-011; help counts toward T3-151 only when the return is named; T3-150's `decide_when_both` keeps help traded inside an alliance when defence or a fight is the frame. Thanks for help go to T3-072 by T3-122's `must_not_show`. A member whose effort moves to another room's build is T3-137, by T3-137's `decide_when_both`.
- **Space.** A request for space or permission to the room that holds it is T3-035; a host ruling on many requests is T3-162 (T3-012's `must_not_show`), a single grant T3-012; a warning that a faction covers unapproved art is T3-094.
- **Neighbours.** T3-079 needs national flags; T3-149 needs rooms already in contact; T3-078 needs kin felt in the words; T3-099 needs the bigger room's protection, and its size in the words; T3-071 is adoption into a neighbour's work; friendly work taken for vandalism is T3-170.

## Corrections made during the packets

Each correction went through `b4_rule_append.py --replace`, which rewrites the ruled line in place, marks it `revised`, and keeps the old ledger under a superseded name. 521 rulings have been corrected in place at least once (`b4_cumulative.py`): the 378 of the re-ruling, the 128 of the `also_present` correction, nine boundary tags in packet 5, and the earlier ones listed here; some were corrected twice. Four of the earlier ones were undone by the re-ruling, because they had moved a ruling to a theme no placement held: catalonia t07, sadboys t03, bisexual t04 and kpop t05.
- **formula1 t05 and elitedangerous t01** (packet 1). T3-063 takes canvas posts only.
- **The T3-016 correction** (packet 2). bindingofisaac t02.
- **The T3-033 and T3-041 reading** (packet 2). clashroyale t02.
- **The homeland-flag reading** (packet 3). catalonia t07.
- **The cut-down reading** (packet 3). sadboys t03.
- **T3-170 for members' own misclicks** (packet 3). bisexual t04 and kpop t05.
- **Concepts of their own** (packet 3). ManningPlace t05, KState t04, rainbowgrid t01, dofus t01, skyrim t03, teamcube t04 and nerf t08. `out/_analysis/b4_own_support_check.py` has found none since, over the five packets.
- **Boundary tags** (packet 3). Eleven rulings gained a `boundary_ruling` with the ruling unchanged.
- **MonkeyIsland t03** (packet 4). Ruled unresolved on a full T3-005|T3-021 tie, revised to place both themes as the paragraph rules.
- **Boundary tags** (packet 5). Thegreatblackhole t06, sonicthehedgehog t04, aceattorney t09, AMD t13, archlinux t03, armenia t04, belgium t11, bindingofisaac t05 and theitalyplace t11 gained a `boundary_ruling` with the ruling unchanged.

## The conflicts pass

`coder_conflicts.jsonl` holds 48 lines. CC-001 to CC-008 came from packet 1's notes, CC-009 to CC-016 from packet 2's, CC-017 to CC-025 from packet 3's, CC-026 to CC-036 from packet 4's, CC-037 to CC-048 from packet 5's, each read before its packet's first ruling. Packet 5's conflicts:
- **CC-037:** every dealing with a neighbour written as one practice: borders, truces, alliances, help traded and help given (T3-010|T3-149, T3-010|T3-150, T3-010|T3-151, T3-010|T3-011).
- **CC-038:** making room for a neighbour, whatever the reason: the room's own restraint, a border, a yield to a request, space granted (T3-010|T3-024, T3-024|T3-039, T3-010|T3-012).
- **CC-039:** taking a neighbour's ground written as one practice: raiding, annexing, converting, spreading a colour (T3-006|T3-061, T3-006|T3-068, T3-061|T3-171).
- **CC-040:** a call to attack and its refusal kept as one practice.
- **CC-041:** the argument over taking another's work folded into the act (T3-046 with T3-024, T3-010 or T3-006).
- **CC-042:** an old sports, school or fandom rivalry carried onto the rival's mark: attack, taunt and conversion as one practice.
- **CC-043:** help between rooms, whichever way it runs (T3-011|T3-084, T3-011|T3-151).
- **CC-044:** a host's admission and a guest's request, written from each side (T3-035|T3-162, T3-012|T3-162).
- **CC-045:** putting right the damage the room did to a neighbour.
- **CC-046:** who was there first, written with the blame and its fairness (T3-045|T3-087, T3-045|T3-046).
- **CC-047:** who speaks for the room, kept inside the deal.
- **CC-048:** a second-order theme whose note says it holds no shared practice.

## Agreement before and after

Before is the two readers against each other. After is each reader against the ruling, over the items not unresolved. Both use stage B2's definition: mean Jaccard on placement sets, with primary match beside it. The next table gives both, by packet and over the five.

| | mean Jaccard before | primary match before | mean Jaccard after | primary match after |
|---|---|---|---|---|
| packet 1 (491; 436 after) | 0.486 | 0.578 | 0.656 | 0.717 |
| packet 2 (447; 437 after) | 0.537 | 0.678 | 0.638 | 0.721 |
| packet 3 (500; 493 after) | 0.475 | 0.598 | 0.583 | 0.637 |
| packet 4 (461; 451 after) | 0.519 | 0.675 | 0.640 | 0.726 |
| packet 5 (409; 406 after) | 0.467 | 0.623 | 0.612 | 0.677 |
| all (2,308; 2,223 after) | 0.496 | 0.629 | 0.625 | 0.695 |

The figure after is not a reliability figure. It is agreement following an adjudication I performed. Packet 5's readers agreed with each other least of the five packets (0.467). The mean Jaccard after rose 0.145 above it, against 0.121 in packet 4. Within packet 5, items 126 to 250 (G13 and the start of G14) had a primary match of 0.856 before; items 251 to 409 (the rest of G14) had 0.491 before and 0.630 after. The blind sample's adjudicated stratum at B4b is the test of whether a stranger reaches these rulings.

## Whether stage B2's predictions held

`confusions.md` predicted nineteen pairs. A packet can show only the pairs whose themes it holds.

- **Packet 1 (G01, G02).** All four predicted pairs that could appear split readers: pair 3 (T3-001|T3-023, 20), pair 15 (T3-001|T3-095, 11), pair 19 (T3-015|T3-063, 7), pair 7 (T3-015|T3-075, 4). Three unpredicted pairs split as often or more: T3-017|T3-031 (17), T3-001|T3-048 (13), T3-023|T3-095 (11).
- **Packet 2 (G03 to G06).** Two of five predicted pairs split readers: pair 6 (T3-002|T3-033, 8) and pair 8 (T3-004|T3-070, 6). Five unpredicted pairs split as often or more: T3-002|T3-038 (10), T3-002|T3-070 (8), T3-002|T3-005 (7), T3-014|T3-153 (5), T3-070|T3-091 (5).
- **Packet 3 (G07, G08 in part).** Four of five predicted pairs split readers: pair 6 (10), pair 10 (T3-004|T3-038, 9), pair 8 (6), pair 5 (T3-004|T3-020, 5). Seven unpredicted pairs split as often or more than pair 5, three of them with T3-041.
- **Packet 4 (G08's end, G09 to G11).** Pair 1, T3-005|T3-021, held: 37 items. Pair 4 (T3-028|T3-070) split 2 and pair 16 (T3-087|T3-188) split 1. Five unpredicted pairs split four items or more: T3-021|T3-038 (6), T3-005|T3-038 (5), T3-005|T3-073 (5), T3-005|T3-006 (4) and T3-058|T3-073 (4).
- **Packet 5 (G12 to G14).** All four predicted pairs that could appear split readers: pair 13 (T3-010|T3-024, 17), pair 2 (T3-010|T3-149, 10), pair 11 (T3-010|T3-151, 7) and pair 12 (T3-010|T3-150, 1). Six unpredicted pairs split three items or more: T3-006|T3-061 (8), T3-010|T3-011 (7), T3-006|T3-068 (4), T3-011|T3-084 (4), T3-010|T3-035 (3) and T3-011|T3-151 (3).

B2 predicted G14's pairs with T3-010 well; every one of them split readers. It missed G12's T3-006|T3-061 and the help pairs, where T3-011 meets T3-084 and T3-151. Pairs 9 and 14 belong to packets 6 and 7.
