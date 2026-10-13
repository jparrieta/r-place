# Adjudication report, stage B4 (interim: packets 1 to 4 of 7)

Written at B4a-04 after packet 4 was ruled. It is rewritten whole after each packet; the figures below cover packets 1 to 4. Per-packet figures: `out/_adjudication-B4/packet-01/summary.md` to `packet-04/summary.md` (`out/_analysis/b4_packet_summary.py`). The sums: `out/_analysis/b4_cumulative.py --packets 1,2,3,4`. Packet 4's named_neither split and class 4 measure: `out/_analysis/b4_named_neither_split.py` and `out/_analysis/b4_packet_detail.py`. Packet 4 split at J's ruling of 13 October: `out/_analysis/b4_agreement_range.py`. The rulings: `out/disagreements.jsonl`. The boundary paragraphs: `out/_adjudication-B4/boundaries.md`, carried below with their item lists.

## Items adjudicated

Stage B3's inventory (`b3_classes.jsonl`, J's five classes) leaves 3,288 contested items: class 3 (the readers' lists differ) 2,393, class 4 (the readers agree on a list not inside my B1 grouping) 837, class 5 (no B1 grouping) 58.
- **Packet 1** ruled 491: the 18 gloss-only items, G01 (April Fools in the sub) and G02 (the sub's own business).
- **Packet 2** ruled 447: G03 (where the planning happens), G04 (calling people in to place), G05 (telling placers what to place) and G06 (strain, doubt and giving up).
- **Packet 3** ruled 500: G07 (choosing what to make and where) and the first 254 items of G08 (building and growing the mark).
- **Packet 4** ruled 461: the last 6 items of G08, G09 (keeping the mark against damage), G10 (finding who did it) and G11 (scripts, bots and extra accounts). 355 class 3, 105 class 4, 1 class 5.

Together 1,899 items: 1,369 class 3, 499 class 4, 31 class 5. 1,389 contested items remain for packets 5 to 7.

## The taxonomy split

The next table counts the rulings by taxonomy value, by packet and by class.

| taxonomy | all | packet 1 | packet 2 | packet 3 | packet 4 | class 3 | class 4 | class 5 |
|---|---|---|---|---|---|---|---|---|
| genuine-joint | 802 | 137 | 215 | 231 | 219 | 802 | 0 | 0 |
| scheme-ambiguous | 375 | 123 | 62 | 106 | 84 | 313 | 60 | 2 |
| author-error | 275 | 97 | 58 | 45 | 75 | 2 | 256 | 17 |
| item-is-a-bag | 193 | 20 | 44 | 76 | 53 | 156 | 37 | 0 |
| author-disagrees | 158 | 37 | 65 | 39 | 17 | 0 | 146 | 12 |
| reader-error | 96 | 77 | 3 | 3 | 13 | 96 | 0 | 0 |
| total | 1899 | 491 | 447 | 500 | 461 | 1369 | 499 | 31 |

How to read it:
- **Genuine-joint is the largest value, 802 (42.2%).** In packet 4 it is 219 of 461 (47.5%). A G09 theme often holds an alarm, a call to defend, the repair and the watch in one coder's theme; a G11 theme holds the scripts run and the argument over them. One reader places the leading act and the other adds a second. The count measures how rule 0 travelled, not the readers.
- **Scheme-ambiguous is 375 (19.7%).** Packet 4 had 84 (18.2%). 20 of them are the homeland flag's repair, which T3-021's `must_not_show` does not send to T3-065.
- **Item-is-a-bag is 193.** Packet 4 has 53. They are long defence threads and script threads where four themes or more have three concepts of their own.
- **Reader-error is 96.** Packet 4 has 13, the most since packet 1. Five come from G10 (neopets t12, TreePlace t03, kanye t29, nbaspurs t12, wine t15) and four from G11 (colombia t06, livecounting t07, RelientK t07 and ice_poseidon t19), where a discriminator or `decide_when_both` decides and one reader missed it.
- **Themes added beyond the placements.** In packets 1 to 3 and items 1 to 400 of packet 4, a theme on one or two concepts was added wherever the concept passed that theme's gate, even when no reader and not my B1 placed it. From item 401 of packet 4, J's ruling stopped that (next section).

## J's ruling on themes added (QB4-001), from item 401 of packet 4

I asked J at B4a-03 (QB4-001) whether to keep adding a one- or two-concept theme that no placement held. Meanwhile packet 4 was ruled as packets 1 to 3 were. J answered at 06:43 Berlin on 13 October: "Ask it to stop. The point is to try to adjudicate. I imagine that the additions are really just the analyst trying to be nice. And not go back on what others said". J's rulings at 06:47 Berlin, for the rest of packet 4 on:
1. The placements are the readers' and the analyst's (my B1). A ruling chooses among those placements and adds no theme beyond them.
2. A ruling takes the union of placements only when it names, for each theme it keeps, the separate concept that carries it; otherwise it chooses.

Items 1 to 400 of packet 4 and all of packets 1 to 3 stand as ruled. They are re-ruled at the start of B4a-05. Items 401 to 461 were ruled under J's rulings. A bag still lists its other themes under `also_present`, which places nothing. One bag from item 401 on lists a theme no reading named: bakchodi t09, with T3-006 for script attacks on the Pakistani and Belgian flags. wallstreetbets t11 and rust t11 list only themes a reading named.

The next table sets packet 4's two parts side by side, with the definitions of the agreement section below.

| packet 4 items | rulings | mean Jaccard before | primary before | mean Jaccard after | primary after | three themes placed | named_neither | a theme no placement held |
|---|---|---|---|---|---|---|---|---|
| 1 to 400 | 400 | 0.512 | 0.652 | 0.536 | 0.638 | 179 | 210 | 133 |
| 401 to 461 | 61 | 0.566 | 0.820 | 0.726 | 0.883 | 22 | 12 | 0 |

The two parts hold different families: items 1 to 400 are G08 to G10, items 401 to 461 are G11. The readers already agreed more on G11 before any ruling (0.566 against 0.512). The rise after the ruling is therefore not the effect of J's rule alone. The 12 named_neither rulings from item 401 on each keep a theme from my B1 grouping that neither reader placed.

## author-error and author-disagrees

author-error: 275 (packet 1 97, packet 2 58, packet 3 45, packet 4 75). author-disagrees: 158 (packet 1 37, packet 2 65, packet 3 39, packet 4 17). Both come almost wholly from class 4, where the readers agreed on a list my B1 grouping did not hold.

The next list gives, by packet, the class 4 items where I took the readers' list (author-error) and where I kept a B1 theme (author-disagrees):
- **Packet 1:** 89 and 29.
- **Packet 2:** 53 and 63; 8 are bags.
- **Packet 3:** 40 and 37. 19 more are bags and 21 scheme-ambiguous. Counting those by what the ruling holds, the readers' list was taken in 49, a B1 theme kept in 55, and 13 rulings hold neither.
- **Packet 4:** 74 and 17. 8 more are bags and 6 scheme-ambiguous. Counting by what the ruling holds, the readers' list was taken in 64 and a B1 theme kept in 32; 14 of those 32 are author-error rulings that take the readers' primary and keep a B1 theme beside it (costa_rica t07, TheHulk t06). 9 hold neither.

Packet 4 turned back toward the readers. Its class 4 items are mostly G10 and G11, where my B1 grouping missed the readers' themes often.

I cannot separate how much of each packet's split is the scheme and how much is my pull toward my own grouping. The blind sample at B4b tests the adjudicated stratum against fresh readers, and these items are part of it.

My commonest B1 errors:
- **Packet 1:** T3-031 placed on an in-joke with no canvas in it; T3-001 placed where nothing was posted as true; T3-063 on posts that are not canvas posts; T3-032 where the complaints were about the sub's own joke styling.
- **Packet 2:** calls for hands that my B1 had placed as the proposal (T3-033), the progress (T3-038) or a further piece (T3-041); placing troubles on the timer, a glitch or a phone (T3-074, 6); posted templates that my B1 had placed as one plan imposed (T3-091).
- **Packet 3:** links and coordinates that only show where the finished mark is (T3-026, 11 rulings); the readers' T3-004 (8), T3-033 (8) and T3-020 (7).
- **Packet 4:** in author-error rulings, the readers placed T3-170 (11), T3-005 (10), T3-021 (7), T3-088 (7), T3-087 (6) and T3-188 (5) where my B1 did not. Seven of the T3-088 items are glitches used to place more, which my B1 had put under T3-074; T3-088's `decide_when_both` gives "using one to place beyond the limit" to T3-088. My B1 also placed T3-087 where friendly work had been taken for an attack (T3-170) or where an organised room set its plan apart from rogue placers (T3-188).

The themes I kept against both readers in packet 4's author-disagrees rulings: T3-021 5, T3-170 4, T3-043 2.

## Fields by ambiguity

The next list counts the 375 scheme-ambiguous rulings by the field whose sentence failed, with packets 1 to 4 in brackets.

- must_show: 204 (78, 33, 54, 39)
- discriminators: 81 (39, 17, 23, 2)
- must_not_show: 66 (2, 6, 26, 32)
- decide_when_both: 24 (4, 6, 3, 11)

`must_not_show` rose again in packet 4, to 32. 20 of its failures are the homeland flag's repair on T3-021's `must_not_show`. `decide_when_both` rose to 11: T3-027's (6), T3-005's (3) and T3-088's (2).

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, over the four packets. Stage C1 opens with it.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-033 | 35 | 32 | 1 | 0 | 2 |
| T3-017 | 30 | 6 | 0 | 1 | 23 |
| T3-023 | 27 | 25 | 0 | 0 | 2 |
| T3-004 | 26 | 4 | 12 | 0 | 10 |
| T3-021 | 26 | 4 | 22 | 0 | 0 |
| T3-001 | 24 | 18 | 0 | 0 | 6 |
| T3-002 | 14 | 0 | 2 | 3 | 9 |
| T3-038 | 14 | 10 | 4 | 0 | 0 |
| T3-005 | 11 | 7 | 0 | 3 | 1 |
| T3-073 | 10 | 10 | 0 | 0 | 0 |
| T3-020 | 9 | 0 | 7 | 0 | 2 |
| T3-063 | 8 | 6 | 1 | 0 | 1 |

63 more themes failed on 141 rulings between them.

The sentences that failed most:
- **T3-033's `must_show`** "An idea of what the room should put on the canvas, offered to the room" (packet 2 9, packet 3 21). It does not say "first". T3-041's `must_not_show` gives "The room's first mark proposed" to T3-033, so a further piece beside a standing mark is T3-041, and readers placed it as T3-033 (conflict CC-019).
- **The homeland flag in the siblings' `must_not_show` lines** (packet 3 24, packet 4 22). T3-065's `must_show` takes the flag of the room's land, its proportions, its spot, its repair and calls for hands to it. No sibling's `must_not_show` says so. In packet 3 the failures fell on T3-004's, T3-020's, T3-041's, T3-038's, T3-033's and T3-082's. In packet 4 they fell on T3-021's `must_not_show` "An attack fought as such (T3-005); the mark reshaped against tampering (T3-055); watch through the night arranged as shifts (T3-141); a script that repairs (T3-028)." 20 of the 22 are the homeland flag: austria t05, india t13, malaysia t04, mexico t14, palestine t04, Peru t07, PORTUGALCARALHO t02, scotland t05, serbia t08, taiwan t05, theitalyplace t01, afip t04, canada t03, chile t03, colorado t03, korea t09, pakistan t05, texas t02, Jamaica t07 and thenetherlands t04. The other two are predators t06 (a member's own misplaced pixel, T3-170) and opticgaming t17 (attackers who repair what they broke, T3-119).
- **T3-073's `must_show`** "What happened to the work told: live reports of changes and attacks, what survived, what was moved and why, the story of its fights afterwards" (packet 4, 9). "live reports of changes and attacks" overlaps T3-005's "alarms" (the T3-005|T3-073 paragraph).
- **T3-005's `must_show`** (packet 4, 6). It names "calls to defend", and a call to defend with no attack in the words is T3-002 by packet 2's paragraph (redpandas t06, smite t06, cavestory t02, anarcho_capitalism t04).
- **T3-027's `decide_when_both`** (packet 4, 6). "T3-028 primary when the scripts are run" does not say how much running; "goes here when fairness is in question" leaves bot claims with no fairness argued without a home.
- **T3-022's `must_show`** (packet 4, 4). "crowded out" with no attack reaches a foothold lost before the mark stood.
- **T3-038's `must_show`** "Placing the mark and reports of its state" (packet 3, 9). It does not say "first".
- **T3-017's discriminator** (packet 1). Its "or the day" contradicts T3-031's own canvas condition.
- **T3-023's** "A change made to a whole sub for April Fools" and **T3-001's** "Members of the room themselves post something false as true for April Fools" (packet 1).

Single failures for stage C1's list: T3-092's own example "I added a little something for my bias" against its discriminator toward T3-060 (bangtan t10, packet 3); T3-082's "the room's subject" against "the room's own mark" (furry t01, packet 3); T3-006's `must_not_show`, which does not name T3-171 for a colour faction spreading (packet 4); T3-089's `must_show`, which names "a neighbour's agreed space" that T3-168 also takes (afip t05, malaysia t05); T3-088's `decide_when_both`, which does not say whether a concept holding both a script and accounts counts (iastate t02, uoft t13); and T3-027's `must_show`, written for "scripts or bots as such", which leaves an argument over the fairness of throwaway accounts with no home (TransFlagPlace t09).

## The named_neither rate

named_neither: 741 of 1,899 (39.0%). Packet 1: 84 of 491 (17.1%). Packet 2: 155 of 447 (34.7%). Packet 3: 280 of 500 (56.0%). Packet 4: 222 of 461 (48.2%).

Packet 1's came from three sources: a second or third theme added by a scheme rule that neither reader applied; a theme in a family the readers did not open; my own B1 theme kept against both readers. In packet 2, 97 of the 155 add only themes from my B1 grouping and 58 add a theme that no placement held. In packet 3, 123 and 157.

The next list splits packet 4's 222 the same way:
- **Only themes from my B1 grouping:** 89. The commonest: T3-087 13, T3-021 8, T3-042 7, T3-170 7.
- **A theme no placement held:** 133, all in items 1 to 400. The commonest: T3-065 31, T3-002 28, T3-073 13, T3-170 8.
- **The primary itself:** chosen by neither reader in 50 rulings. In 28 of them no placement held it.
- **How many themes:** 167 of the 222 place three themes. Over the packet, 201 of 461 rulings place three themes.

My reading of it. Three causes in packets 3 and 4, none of which I can weigh against my own pull:
- **The readings and boundaries send items to themes neither reader chose.** In packet 4 the homeland-flag reading put T3-065 on 31 rulings that no placement held, and packet 2's T3-002|T3-005 paragraph put T3-002 on 28 calls to defend with no attack in the words.
- **Primaries moved by count.** Where a theme held more concepts than the readers' primary, it went first, even when both readers agreed on the primary.
- **Small added themes.** A theme on one or two concepts of its own was added whenever it passed its gate.

J's ruling of 13 October stopped the third cause and the part of the first that adds themes no placement held. From item 401 on, every named_neither ruling keeps a theme from my B1 grouping.

## The unresolved count

unresolved: 79 of 1,899 (4.2%). Packet 1: 52 (10.6%). Packet 2: 10 (2.2%). Packet 3: 7 (1.4%). Packet 4: 10 (2.2%). The next lists name them by the reason the scheme did not decide.

Packet 1:
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
- **The attack or its target not shown** (T3-005 `must_show`), 2: linux t01 ('Stop messing with the Leafs man!', with no word whether the Leafs image is the room's work or a neighbour's) and osu t15 ('The most important fight', one concept).
- **Who changed the work not shown** (T3-087 `must_show`), 2: cavestory t06 (three title lines) and Dominican t09 (one '[hmmm]' screenshot).
- **Whose work not shown** (T3-139 `must_show`), 1: kpop t13 ('Get the hell off of play-yan you fucking monsters').
- **When or at whom the blame was laid not shown** (T3-058), 2: DestinyTheGame t14 (no time given, T3-058's discriminator against T3-087) and notredame t10 ('the red dot' with no room named).
- **One act that meets two themes** (T3-068 `must_show`), 1: hungary t05 ('make Slovakian flag Russian', a flag turned into another sign and griefing for fun at once).
- **Five acts of one concept each** (T3-192 `must_show`), 1: dallasstars t01.
- **A bot claim with no fairness in question, told after the loss** (T3-027 `decide_when_both`), 1: tampabaylightning t15 ('destroyed by bots last minute').

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

**T3-002|T3-005, a rally or a defence (12 items in packet 2; 9 more in packet 4).** The attack must be in the words. A call to "protect" a mark with no attacker in view is T3-002. Packet 2 items: btc t02, Clannad t02, crusaderkings t01, FlaggyFlag t02, harrypotter t01, monalisaclan t02, ohio t03, czech t01, malta t02, nin t10, thetreesnetwork t01, prequelmemes t02. Packet 4 items: masseffect t01, sooners t08, redpandas t06, smite t06, cavestory t02, anarcho_capitalism t04, feedthebeast t07, loliconsunite t02, tf2 t11.

**T3-070|T3-091, directions or one plan (7 items; CC-012):** stlouisblues t01, FloydVsVoid t02, heyyea t01, starryknights t02, ChronoTrigger t02, mylittlepony t04, PlaceNL t01. **T3-004|T3-070, the design or its directions (6 items):** berserk t06, foxstevenson t03, nyu t01, pitt t02, muse t02, suomi t06.

### Packet 3

**T3-033|T3-041, the first mark or a further piece (25 items; CC-019).** A proposal counts toward T3-041 when the room's mark already stands or is chosen. Items: truestl t02, cmu t01, metalgearsolid t04, muse t01, aoe2 t04, denmark t10, eagles t02, eve t03, gameofthrones t02, indieheads t13, KState t01, math t02, nuclearthrone t01, portal t02, purplecorner t03, rust t09, simonfraser t04, splatoon t03, suomi t02, touhou t08, ufl t01, blackmirror t05, borderlands t04, empiredidnothingwrong t11, winnipegjets t11.

**T3-038|T3-041, the first build or a further piece's (16 items).** Items: sakuragakuin t01, jerma985 t03, nuclearthrone t05, bobross t01, cavestory t01, dota2 t11, madokamagica t01, msu t02, parahumans t01, touhou t02, AyyMD t01, cubers t21, cubers t25, samuraijack t10, suomi t27, yumenikki t01.

**T3-004|T3-041, the look or an addition (14 items).** Items: ubreddit t03, ElderScrolls t05, funhaus t01, nin t03, radiohead t01, skyrim t02, bindingofisaac t03, DatBoi t04, factorio t09, placetardis t02, ProfessorLayton t02, starlightstage t12, borderlands t02, enterthegungeon t03.

**T3-004|T3-169 (8 items; CC-022):** bisexual t03, greyblob t02, monstercat t06, unturned t09, drawhelix t05, farmcarrots t08, neopets t14, wine t08. **T3-004|T3-038 (8):** portal t01, timbers t02, AvoArmy t01, calgaryflames t01, uoft t08, bitcoin t02, detroitlions t04, paydaytheheist t02. **T3-038|T3-070 (7):** berkeley t03, gameattack t04, virginiatech t03, planetside t08, bdsm t01, re_zero t06, formula1 t06. **T3-004|T3-020 (7):** blackmirror t02, borussiadortmund t03, minecraft t04, kingdomhearts t12, oneshot t01, nightinthewoods t02, utaustin t01. **T3-004|T3-033 (6):** frc t01, nlsscirclejerk t02, WPI t01, redhotchilipeppers t03, starlightstage t09, yugioh t04. **T3-020|T3-033 (1):** tetris t01.

**Carried from packet 2 into packet 3.** T3-002|T3-033 (10 items): chicubs t09, DiamondClub t01, foxes t01, hawks t05, kanye t01, schoolidolfestival t04, stardustcrusaders t01, unturned t03, wallstreetbets t01, warframe t01. T3-002|T3-038 (9 items): bostonbruins t02, enterthegungeon t01, ethoslab t01, forsen t01, habs t02, nyjets t04, the_pack t01, winnipegjets t01, wow t17. T3-004|T3-070 (9 items): crusaderkings t02, penguins t03, udub t01, drumcorps t06, kanye t05, Okami t06, pebble t04, placesnek t04, portal t03.

Readings written during packet 3: the homeland flag's look (T3-065, emblems T3-113); a design cut down to the hands (T3-004; T3-069 only when a piece is dropped for another; T3-042 when growth is set aside); a celebration while placement goes on (T3-009 for "done" celebrated, T3-026 for "up" or "for now").

### Packet 4

Four pairs split five or more of packet 4's items on their primaries and were ruled before its first item. Three more were ruled at item 401, when G11's pairs were met. The item lists are the packet 4 items that carry the pair in `boundary_ruling`.

**T3-005|T3-021, a fight or upkeep (67 items; B2's predicted pair 1; conflict CC-026).** Ruled as written by the discriminator and T3-005's `decide_when_both`. A concept counts toward T3-005 when an attack on the room's work is in the words and the room answers it as a fight: an alarm, a call to defend or fight back, holding the line, an attack reported repelled. A concept counts toward T3-021 when it watches or fixes, "with or without an attacker in view, where no fight is called". The Void, a named room or a bot eating the work is an attacker in the words. Naming who did it goes to T3-087, a watch through the night to T3-141 (CC-032), a script that repairs to T3-028 (CC-028), upkeep argued over growth to T3-042 (CC-027). Where count and placements both tie, the item is scheme-ambiguous on T3-005's `decide_when_both`, which names no tie, and both themes are placed. Items: aggies t03, aoe2 t05, austria t05, bangtan t06, bostonbruins t06, clg t04, cubers t10, earthbound t04, factorio t07, flashtv t09, frankocean t10, furry_irl t12, gorillaz t06, gravityfalls t02, GreenCorner t03, hellointernet t02, HomestarRunner t03, homestuck t04, leafs t02, leagueoflegends t16, nyjets t08, parrots t09, PinkVomitMonster t02, placestart t14, placetardis t03, portal t07, reddevils t15, rocketbeans t05, roosterteeth t04, shield t03, ss13 t06, stardewvalley t03, tf2 t12, TheFarLeftSide t03, TransFlagPlace t03, warriors t08, androidgaming t03, ChronoTrigger t03, clubpenguin t09, FinalFantasy t05, gameofthrones t14, jerma985 t04, metroid t09, MonkeyIsland t03, muse t05, necrodancer t05, oneshot t04, partyparrot t02, placeportalpattern t06, ScottPilgrim t03, simonfraser t09, stlouisblues t08, tagpro t03, tampabaylightning t03, TeamDignitas t04, redhotchilipeppers t08, anaheimducks t09, animalcrossing t04, AyyMD t02, bisexual t06, cloud9 t07, DestinyTheGame t08, dragonquest t02, kingdomhearts t20, sheffield t02, starcraft t07, theexpanse t05.

**T3-005|T3-073, an alarm or a report (9 items).** The two `must_show` lines overlap. A report addressed to the room so that it acts counts toward T3-005. A report of what changed, survived or was lost, with no call to fight, counts toward T3-073. Items whose split turns on a bare alarm with no call are scheme-ambiguous on T3-073's `must_show`. Items: apocalypserising t05, masseffect t06, mindcrack t02, terraria t08, daftpunk t05, 4chan t08, anime t11, neutralmilkhotel t03, texastech t03.

**T3-021|T3-038, first build or restored (3 items; CC-017).** Ruled as written. The same spot rebuilt after a loss is T3-021; a rebuild at a new spot is T3-022. Items: nerf t02, pitt t03, telegram t03.

**T3-005|T3-038 (5 items split; none tagged).** Neither theme has a discriminator against the other. Placing the first build counts toward T3-038; an attack answered as a fight toward T3-005.

**T3-020|T3-022, the first spot or a move after a loss (5 items; CC-033).** A spot found, tested or changed before the mark stands, or a move made while building to avoid a threat not yet met, counts toward T3-020. A move or restart after the work was destroyed, overpowered or crowded out counts toward T3-022. T3-022's "crowded out" reaches a foothold lost before the mark stood; those splits are scheme-ambiguous on T3-022's `must_show`. Items: mordhau t04, rutgers t04, toolband t04, dallasstars t13, detroitredwings t04.

**T3-027|T3-028, arguing scripts or running them (4 items; CC-029).** T3-027's `decide_when_both` puts T3-028 first "when the scripts are run" and does not say how much running. Ruled: each concept counts toward the act it does, and the larger part leads, as T3-006's `decide_when_both` says of its own pairs; a tie goes by placements. A script shared to wreck another room's work is not "for the room's work". Items whose readers split on which act leads are scheme-ambiguous on T3-027's `decide_when_both`. Items: pakistan t08, giantbomb t07, placecanada t12, placeDE t07.

**T3-027|T3-087, a bot claim or a culprit traced (4 items).** Neither theme has a discriminator against the other. Bots or new and empty accounts named as the source of damage to the room's work while placement goes on count toward T3-087. Bots judged to spoil the canvas or called unfair count toward T3-027, as do bot rumours where fairness is in question. A bot claim with no fairness in question and no damage traced while placing is not decided. Items: shitredditsays t05, sooners t10, tampabaylightning t15, foxes t04.

**T3-089|T3-168, a stale script or a neighbour spared (2 items).** Ruled by the discriminator: a call to stop or change the room's scripts so a neighbour's work stands counts toward T3-168, though T3-089's `must_show` also names "a neighbour's agreed space". Items: afip t05, malaysia t05.

**T3-005|T3-006 (CC-031)** and **T3-058|T3-073 (CC-034)** reached four items and were decided by their discriminators as met. One item carries T3-005|T3-006: rocketbeans t07.

Two readings were written while packet 4 was ruled:
- **The homeland flag kept and defended (from item 15).** Repairing the flag of the room's land, and calls to come and defend or protect it with no attack in the words, count toward T3-065; its expansion does too, unless a neighbour's space is named (T3-061). An attack on it, fought or raised as an alarm, counts toward T3-005. Watching it with no repair counts toward T3-021, and watch through the night toward T3-141. A reader's T3-021 on that repair is scheme-ambiguous on T3-021's `must_not_show`.
- **A call to fight and a call to defend (from item 16).** A call to fight ("Stay and Fight!", "fight back") counts toward T3-005: a fight has an opponent. A call to defend or protect with no attack in the words counts toward T3-002, or T3-065 for the homeland flag.

## Corrections made during the packets

Each correction went through `b4_rule_append.py --replace`, which rewrites the ruled line in place, marks it `revised`, and keeps the old ledger under a superseded name. 27 rulings have been corrected in place.
- **formula1 t05 and elitedangerous t01** (packet 1). T3-063 takes canvas posts only.
- **The T3-016 correction** (packet 2). bindingofisaac t02.
- **The T3-033 and T3-041 reading** (packet 2). clashroyale t02.
- **The homeland-flag reading** (packet 3). catalonia t07.
- **The cut-down reading** (packet 3). sadboys t03.
- **T3-170 for members' own misclicks** (packet 3). bisexual t04 and kpop t05.
- **Concepts of their own** (packet 3). ManningPlace t05, KState t04, rainbowgrid t01, dofus t01, skyrim t03, teamcube t04 and nerf t08. `out/_analysis/b4_own_support_check.py` has found none since, over the four packets.
- **Boundary tags** (packet 3). Eleven rulings gained a `boundary_ruling` with the ruling unchanged.
- **MonkeyIsland t03** (packet 4, at chunk 7). Ruled unresolved in chunk 6 on a full T3-005|T3-021 tie. The T3-005|T3-021 paragraph places both themes on a full tie, so it was revised to T3-005 and T3-021, scheme-ambiguous on T3-005's `decide_when_both`.

## The conflicts pass

`coder_conflicts.jsonl` holds 36 lines. CC-001 to CC-008 came from packet 1's notes, CC-009 to CC-016 from packet 2's, CC-017 to CC-025 from packet 3's, CC-026 to CC-036 from packet 4's, each read before its packet's first ruling. Packet 4's conflicts and the pairs they may explain:
- **CC-026:** keeping the mark against damage is named defence or repair in either order (T3-005|T3-021, T3-005|T3-087, T3-021|T3-073).
- **CC-027:** putting upkeep before growth is folded into the repair practice (T3-021|T3-042).
- **CC-028:** a script that keeps the mark is filed as repair or as a script practice (T3-021|T3-028).
- **CC-029:** running scripts and arguing whether they are fair are written as one practice (T3-027|T3-028, T3-028|T3-088, T3-027|T3-087).
- **CC-030:** sorting attacks from mistakes and friends from attackers (T3-087|T3-170, T3-087|T3-188, T3-170|T3-188).
- **CC-031:** the fight is named for defence and attack at once (T3-005|T3-006).
- **CC-032:** shifts and night watches over the mark (T3-021|T3-141).
- **CC-033:** moving the work, whatever the cause (T3-020|T3-022, T3-022|T3-039).
- **CC-034:** the end of the event, with loss, blame and memory together (T3-058|T3-073, T3-029|T3-058).
- **CC-035:** a large neighbouring project that takes art into itself, the taskbar (rocketbeans t07, hatsune t04).
- **CC-036:** a second-order theme whose note says it holds no shared practice, in 23 subs.

## Agreement before and after

Before is the two readers against each other. After is each reader against the ruling, over the items not unresolved. Both use stage B2's definition: mean Jaccard on placement sets, with primary match beside it. The next table gives both, by packet and over the four.

| | mean Jaccard before | primary match before | mean Jaccard after | primary match after |
|---|---|---|---|---|
| packet 1 (491; 439 after) | 0.486 | 0.578 | 0.633 | 0.697 |
| packet 2 (447; 437 after) | 0.537 | 0.678 | 0.603 | 0.706 |
| packet 3 (500; 493 after) | 0.475 | 0.598 | 0.473 | 0.535 |
| packet 4 (461; 451 after) | 0.519 | 0.675 | 0.562 | 0.671 |
| all (1,899; 1,820 after) | 0.503 | 0.630 | 0.565 | 0.649 |

The figure after is not a reliability figure. It is agreement following an adjudication I performed. In packet 3 it fell below the readers' agreement with each other. In packet 4 the mean Jaccard after rose above before (0.562 against 0.519), and the primary match after stayed level (0.671 against 0.675). Within packet 4, items 1 to 400 rose little (0.536 against 0.512) and items 401 to 461, ruled under J's rule, rose more (0.726 against 0.566); the section on J's ruling above gives the table and why the two parts are not a clean comparison. The blind sample's adjudicated stratum at B4b is the test of whether a stranger reaches these rulings.

## Whether stage B2's predictions held

`confusions.md` predicted nineteen pairs. A packet can show only the pairs whose themes it holds.

- **Packet 1 (G01, G02).** All four predicted pairs that could appear split readers: pair 3 (T3-001|T3-023, 20), pair 15 (T3-001|T3-095, 11), pair 19 (T3-015|T3-063, 7), pair 7 (T3-015|T3-075, 4). Three unpredicted pairs split as often or more: T3-017|T3-031 (17), T3-001|T3-048 (13), T3-023|T3-095 (11).
- **Packet 2 (G03 to G06).** Two of five predicted pairs split readers: pair 6 (T3-002|T3-033, 8) and pair 8 (T3-004|T3-070, 6). Five unpredicted pairs split as often or more: T3-002|T3-038 (10), T3-002|T3-070 (8), T3-002|T3-005 (7), T3-014|T3-153 (5), T3-070|T3-091 (5).
- **Packet 3 (G07, G08 in part).** Four of five predicted pairs split readers: pair 6 (10), pair 10 (T3-004|T3-038, 9), pair 8 (6), pair 5 (T3-004|T3-020, 5). Seven unpredicted pairs split as often or more than pair 5, three of them with T3-041.
- **Packet 4 (G08's end, G09 to G11).** Pair 1, T3-005|T3-021, held: 37 items whose readers put those two themes as their primaries, the commonest split of any packet so far. Pair 4 (T3-028|T3-070) split 2 and pair 16 (T3-087|T3-188) split 1. Five unpredicted pairs split four items or more: T3-021|T3-038 (6), T3-005|T3-038 (5), T3-005|T3-073 (5), T3-005|T3-006 (4) and T3-058|T3-073 (4). Four of the five hold T3-005 or T3-021. T3-027|T3-028 and T3-027|T3-087 split 3 each.

B2 predicted G09's main pair and missed its neighbours. T3-005 sits in four of packet 4's six commonest splits. Pairs 2, 9, 11, 12, 13 and 14 belong to families in packets 5 to 7.
