# Adjudication report, stage B4 (interim: packets 1 to 3 of 7)

Written at B4a-03 after packet 3 was ruled. It is rewritten whole after each packet; the figures below cover packets 1 to 3. Per-packet figures: `out/_adjudication-B4/packet-01/summary.md`, `packet-02/summary.md` and `packet-03/summary.md` (`out/_analysis/b4_packet_summary.py`). The sums: `out/_analysis/b4_cumulative.py --packets 1,2,3`. Packet 3's named_neither split and class 4 measure: `out/_analysis/b4_named_neither_split.py` and `out/_analysis/b4_packet_detail.py`. The rulings: `out/disagreements.jsonl`. The boundary paragraphs: `out/_adjudication-B4/boundaries.md`, carried below with their item lists.

## Items adjudicated

Stage B3's inventory (`b3_classes.jsonl`, J's five classes) leaves 3,288 contested items: class 3 (the readers' lists differ) 2,393, class 4 (the readers agree on a list not inside my B1 grouping) 837, class 5 (no B1 grouping) 58.
- **Packet 1** ruled 491: the 18 gloss-only items, G01 (April Fools in the sub) and G02 (the sub's own business).
- **Packet 2** ruled 447: G03 (where the planning happens), G04 (calling people in to place), G05 (telling placers what to place) and G06 (strain, doubt and giving up).
- **Packet 3** ruled 500: G07 (choosing what to make and where) and the first 254 items of G08 (building and growing the mark). 376 class 3, 117 class 4, 7 class 5.

Together 1,438 items: 1,014 class 3, 394 class 4, 30 class 5. 1,850 contested items remain for packets 4 to 7.

## The taxonomy split

The next table counts the rulings by taxonomy value, by packet and by class.

| taxonomy | all | packet 1 | packet 2 | packet 3 | class 3 | class 4 | class 5 |
|---|---|---|---|---|---|---|---|
| genuine-joint | 583 | 137 | 215 | 231 | 583 | 0 | 0 |
| scheme-ambiguous | 291 | 123 | 62 | 106 | 235 | 54 | 2 |
| author-error | 200 | 97 | 58 | 45 | 2 | 182 | 16 |
| author-disagrees | 141 | 37 | 65 | 39 | 0 | 129 | 12 |
| item-is-a-bag | 140 | 20 | 44 | 76 | 111 | 29 | 0 |
| reader-error | 83 | 77 | 3 | 3 | 83 | 0 | 0 |
| total | 1438 | 491 | 447 | 500 | 1014 | 394 | 30 |

How to read it:
- **Genuine-joint is the largest value, 583 (40.5%).** In packet 3 it is 231 of 500 (46.2%). A G07 or G08 theme often holds a proposal, its design, its spot, its placing and a further piece in one coder's theme. One reader places the leading act and the other adds a second. The count measures how rule 0 travelled, not the readers.
- **Scheme-ambiguous is 291 (20.2%).** Packet 1 had 123 (25.1%), packet 2 62 (13.9%), packet 3 106 (21.2%). Two failures make up 45 of packet 3's 106: T3-033's `must_show`, which does not say "first" (21), and the homeland flag, which the siblings' `must_not_show` lines do not send to T3-065 (24).
- **Item-is-a-bag is 140.** Packet 3 has 76, the most of any packet so far. They are long build threads where four themes or more have three concepts of their own. The largest is overwatch t13: T3-033 is placed and ten themes sit under `also_present`.
- **Reader-error is 83:** 77 in packet 1, 3 in packet 2, 3 in packet 3. Packet 3's three are PinkVomitMonster t03 (T3-061 with T3-004), Goodboye t08 (T3-073 with T3-090) and riskofrain t01 (T3-082).
- **A theme on one or two concepts** was added wherever the concept passed that theme's gate as its own act, at most three placements in all. Where two or more such themes tied with no placement ahead, none was added. Packet 3 applied this more often than packets 1 and 2, and it is one of the two causes of the fall in agreement below (QB4-001).

## author-error and author-disagrees

author-error: 200 (packet 1 97, packet 2 58, packet 3 45). author-disagrees: 141 (packet 1 37, packet 2 65, packet 3 39). Both come almost wholly from class 4, where the readers agreed on a list my B1 grouping did not hold.

The next list gives, by packet, the class 4 items where I took the readers' list (author-error) and where I kept a B1 theme (author-disagrees):
- **Packet 1:** 89 and 29.
- **Packet 2:** 53 and 63; 8 are bags.
- **Packet 3:** 40 and 37. 19 more are bags and 21 scheme-ambiguous. Counting those by what the ruling holds, the readers' list was taken in 49, a B1 theme kept in 55, and 13 rulings hold neither, such as baylor t05, where a known mark located by its maker is T3-026 against both readers' T3-082.

I cannot separate how much of the fall from packet 1 is the scheme and how much is my pull toward my own grouping. The blind sample at B4b tests the adjudicated stratum against fresh readers, and these items are part of it.

My commonest B1 errors:
- **Packet 1:** T3-031 placed on an in-joke with no canvas in it; T3-001 placed where nothing was posted as true; T3-063 on posts that are not canvas posts; T3-032 where the complaints were about the sub's own joke styling.
- **Packet 2:** calls for hands that my B1 had placed as the proposal (T3-033), the progress (T3-038) or a further piece (T3-041), among 14 rulings that take T3-002; placing troubles on the timer, a glitch or a phone (T3-074, 6); posted templates that my B1 had placed as one plan imposed (T3-091).
- **Packet 3:** links and coordinates that only show where the finished mark is. In 11 author-error rulings the readers placed T3-026 and my B1 did not; my B1 had placed such items as decoding (T3-018), directions (T3-070) or a find (T3-082). The readers' T3-004 (8), T3-033 (8) and T3-020 (7) were the next themes missing from my B1.

The themes I kept against both readers in packet 3's author-disagrees rulings: T3-082 5, T3-113 3, T3-056 3.

## Fields by ambiguity

The next list counts the 291 scheme-ambiguous rulings by the field whose sentence failed, with packets 1, 2 and 3 in brackets.

- must_show: 165 (78, 33, 54)
- discriminators: 79 (39, 17, 23)
- must_not_show: 34 (2, 6, 26)
- decide_when_both: 13 (4, 6, 3)

`must_not_show` rose from 8 to 34 in packet 3. 24 of its 26 failures there are the homeland flag and its emblems (see below).

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, over the three packets. Stage C1 opens with it.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-033 | 34 | 31 | 1 | 0 | 2 |
| T3-017 | 30 | 6 | 0 | 1 | 23 |
| T3-023 | 27 | 25 | 0 | 0 | 2 |
| T3-004 | 26 | 4 | 12 | 0 | 10 |
| T3-001 | 24 | 18 | 0 | 0 | 6 |
| T3-002 | 14 | 0 | 2 | 3 | 9 |
| T3-038 | 11 | 9 | 2 | 0 | 0 |
| T3-063 | 8 | 6 | 1 | 0 | 1 |
| T3-020 | 8 | 0 | 6 | 0 | 2 |
| T3-095 | 7 | 3 | 0 | 2 | 2 |
| T3-041 | 7 | 2 | 4 | 0 | 1 |
| T3-026 | 7 | 2 | 0 | 2 | 3 |

51 more themes failed on 88 rulings between them.

The sentences that failed most:
- **T3-033's `must_show`** "An idea of what the room should put on the canvas, offered to the room" (packet 2 9, packet 3 21). It does not say "first". T3-041's `must_not_show` gives "The room's first mark proposed" to T3-033, so a further piece beside a standing mark is T3-041, and readers placed it as T3-033. Conflict CC-019 shows coders writing both acts in the same words.
- **The homeland flag in the siblings' `must_not_show` lines** (packet 3, 24). T3-065's `must_show` takes the flag of the room's land, its proportions, its spot and its repair, and T3-065's `decide_when_both` sends emblems in or beside it to T3-113. No sibling's `must_not_show` says so. The failures fell on T3-004's (12: eesti t12, GranColombia t06, placeDE t10, texas t04, theitalyplace t10, austria t07, albania t07, guatemala t01, portugal t02, theitalyplace t03, bretagne t01, and morrowind t07 on another ground), T3-020's (6: romania t02, singapore t06, hongkong t02, kuwait t02, sakartvelo t01, brasil t02), T3-041's (palestine t03, argentina t05, Jamaica t10, and halo t13 on another ground), two on T3-038's (brasil t04, belgium t01), and one each on T3-033's (SwissNeutralityZone t01) and T3-082's (vietnam t04).
- **T3-038's `must_show`** "Placing the mark and reports of its state" (packet 3, 9). It does not say "first", so a further piece's progress sits on T3-038 and T3-041 at once.
- **T3-004's discriminators** against T3-041 (5) and against T3-169 (4) (packet 3).
- **T3-017's discriminator** "Is it the room's running in-joke carried into the canvas talk or the day (T3-031)" (packet 1). Its "or the day" contradicts T3-031's own canvas condition.
- **T3-023's** "A change made to a whole sub for April Fools" and **T3-001's** "Members of the room themselves post something false as true for April Fools" (packet 1).
- **T3-014's discriminator** against T3-153 and **T3-002's tests on the national flag** (packet 2).

Two single failures in packet 3 belong on stage C1's list. T3-092's `must_show` gives "I added a little something for my bias" as its own example, while its discriminator against T3-060 sends a piece "added to a shared mark" to T3-060 (bangtan t10; both readers placed T3-060). T3-082's `must_show` names "the room's subject" drawn, while its discriminator against T3-052 asks for "the room's own mark" (furry t01).

## The named_neither rate

named_neither: 519 of 1,438 (36.1%). Packet 1: 84 of 491 (17.1%). Packet 2: 155 of 447 (34.7%). Packet 3: 280 of 500 (56.0%).

Packet 1's came from three sources:
- a second or third theme added by a scheme rule that neither reader applied;
- a theme in a family the readers did not open;
- my own B1 theme kept against both readers.

In packet 2, 97 of the 155 add only themes from my B1 grouping and 58 add a theme that no placement held. (The interim report after packet 2 said 98 and 57. sadboys t03 moved between them when the cut-down reading revised its T3-069 to T3-004, which no placement held.)

The next list splits packet 3's 280 the same way:
- **Only themes from my B1 grouping:** 123. The commonest: T3-041 16, T3-113 10, T3-070 8, T3-004 8.
- **A theme no placement held:** 157. The commonest: T3-041 27, T3-065 14, T3-002 13, T3-070 11, T3-004 9, T3-038 8, T3-026 8.
- **The primary itself:** chosen by neither reader in 112 rulings. In 57 of them no placement held it.
- **How many themes:** 174 of the 280 place three themes. Over the packet, 201 of 500 rulings place three themes; packet 2 placed three in 117 of 447.

My reading of it. Three causes, none of which I can weigh against my own pull:
- **The readings and boundaries send items to themes neither reader chose.** The homeland-flag reading places T3-065 on 22 rulings, 19 as primary; in 14 of them no placement held it. The T3-033/T3-041 and T3-038/T3-041 boundaries put T3-041 on further pieces that the readers placed as a proposal or as progress.
- **T3-038 was put first by both readers in 76 items.** My rulings kept it first in 27. They moved it in 49: to T3-002 by the counting rule (11), to T3-041 for further pieces (10), to T3-004 for corrections (5), and to 16 other themes in the other 23. Its own concepts in those items were often one or two.
- **Small added themes.** A third theme on one or two concepts of its own was added whenever it passed its gate, and many of those no placement held.

The rate is also the measure of my pull toward my own reading, which no procedure removes. I asked J (QB4-001) whether packets 4 to 7 should add a one- or two-concept theme that no placement held. Meanwhile packets 4 to 7 are ruled as packets 1 to 3 were, so the seven packets stay comparable.

## The unresolved count

unresolved: 69 of 1,438 (4.8%). Packet 1: 52 (10.6%). Packet 2: 10 (2.2%). Packet 3: 7 (1.4%). The next lists name them by the reason the scheme did not decide.

Packet 1:
- **April Fools play not posted as true** (the gap; T3-001 `must_show`), 13: 4chan t11, bisexual t09, schoolidolfestival t11, thesimpsons t03, 49ers t03, danganronpa t23, falcons t09, parahumans t07, berserk t04, GuildWars2 t07, vim t01, wholesomememes t14, portugal t15.
- **Another sub's change** (T3-023 `must_show`), 8: flashtv t14, megaman t04, iastate t01, katawashoujo t02, winnipegjets t03, Braveryjerk t01, liverpoolfc t03, bostonceltics t03.
- **The item shows no doing, or both readers placed what the words do not support** (author-disagrees), 8: lebanon t09, archlinux t12, greenbaypackers t05, python t09, 4chan t06, FlipnoteStudio3D t02, morrowind t11, catalonia t04.
- **Moderators applying standing rules to non-canvas posts** (T3-063 `must_show`, conflict CC-004), 6: yugioh t06, yugioh t12, metalcore t07, oneplus t05, twice t04, flashtv t10.
- **Whose joke is not shown** (T3-001 discriminator), 5: oneplus t09, danganronpa t19, kamenrider t07, lego t07, ubreddit t02.
- **A record of the change, not the change kept** (T3-100 `must_show`), 2: survivor t18, survivor t11.
- **Waiting for or remembering the sub's own joke** (T3-048 and T3-095 `must_show`), 2: halo t01, polandball t01.
- **A defence of the sub's own joke against too few objections** (T3-032 `must_show`), 2: ethereum t12, denverbroncos t02.
- **Single reasons**, 6:
  - kurdistan t06 and lakers t07 (T3-095 discriminator);
  - bardmains t09 (an April Fools joke's limits: T3-143 is canvas-only, T3-032 short of three);
  - de t22 (suspicion of the platform's motives, no theme);
  - mindcrack t07 (nothing asked or settled);
  - stardustcrusaders t21 (the pointer is not shown).

Packet 2:
- **One concept with no doing to place** (author-disagrees in class 4, empty ruling in class 5), 6: minecraft t17, popheads t01, h3h3productions t27, shield t07, kuwait t09, minecraft t18.
- **A pointer to another sub's thread on the room's canvas work** (T3-015 `must_show`), 1: Redox t02.
- **Naming a feature of a colour faction's ground** ('the Beam'; T3-070 `must_show`), 1: orderofthebluecorner t02.
- **A bare question with no answer** (T3-018 and T3-073 `must_show`), 2: THE_R t03, parrots t15.

Packet 3. All seven are one surviving concept or one exchange, and conflict CC-025 names six of them as themes their coders grouped by exclusion:
- **A title with its body deleted** (class 5, empty ruling), 2: quebec t16 ('Une opportunité émerge!'), bahrain t09 ('R/place Bahrain').
- **First mark or further piece not shown** (T3-033 `must_show`), 1: davidbowie t04 ('Can we make like a mount rushmore with Freddie, Ozzy, and Jagger?').
- **Canvas or ordinary talk not shown** (T3-017 `must_show`), 1: tampabaylightning t09 ('Idea for new 3rd jersey').
- **A jab that falls short of a complaint** (T3-049 `must_show`), 1: h3h3productions t30.
- **A late apology with no placing** (T3-003 `must_show`), 1: AMD t20 ('Sorry im a day late').
- **A name with no doing** (T3-052 `must_show`), 1: samuraijack t25 ('Dont forget Frank Ocean').

## The boundary rulings

Each pair is one paragraph in `boundaries.md`. Each paragraph's ruling is summarised here with its item list.

### Packet 1

**T3-001|T3-023, the joke's stage (32 items).** A change to the sub's name, look, rules or subject made by its moderators, or by members flooding it "as a sub acting together", is T3-023. Members' own false claims in an unchanged sub are T3-001. Both, each with concepts of their own: the larger primary. Items: aceattorney t01, MMA t02, nlsscirclejerk t08, rit t02, totallynotrobots t06, totallynotrobots t08, AceOfAngels8 t01, clashroyale t03, enterthegungeon t02, flyers t05, furry t09, harrypotter t06, kilian t08, mylittlepony t08, porterrobinson t08, porterrobinson t09, ss13 t01, teslamotors t01, toolband t02, totallynotrobots t02, totallynotrobots t03, totallynotrobots t04, totallynotrobots t07, OneTrueEmilia t01, apocalypserising t01, formula1 t02, greece t07, polska t03, thetreesnetwork t02, totallynotrobots t01, ubc t02, zootopia t01.

**T3-001|T3-048, whose joke (20 items).** The source shown in the concepts decides. Where it cannot be read, the ruling is unresolved. A member relaying an organisation's joke is T3-048 by the discriminator, though T3-001's test catches it (conflict CC-002). Items: btc t04, bitcoin t06, feedthebeast t02, opticgaming t01, uofmn t01, baylor t02, GuildWars2 t01, GuildWars2 t10, runescape t07, rutgers t01, starlightstage t03, warframe t15, yugioh t10, yugioh t11, danganronpa t19, falcons t10, kamenrider t07, lego t07, simonfraser t02, ubreddit t02.

**T3-017|T3-031, the canvas condition (15 items here, with T3-001|T3-031: rwby t03).** T3-031 requires the canvas, and T3-017's and T3-001's discriminators do not. T3-031's own test governs: an in-joke with no canvas in it is T3-017. Every item is scheme-ambiguous on T3-017's discriminator. Items: cubers t30, ethereum t06, falcons t08, flashtv t04, freedomplanet t05, h3h3productions t06, h3h3productions t12, heyyea t07 (canvas in it: T3-031), indieheads t06, mls t07, PlaceNL t20, romania t22 (T3-130), SydneyFC t03, tf2 t09, torontoraptors t03.

**T3-001|T3-095, who staged the claim (8 items).** A test of a member's own fake is T3-001 "even when readers test it". A test of anyone else's claim is T3-095. In fivenightsatfreddys t03 and hearthstone t01 both readers put the tests of members' fakes under T3-095, so those are scheme-ambiguous. Items: linux t04, planetside t01, romania t12, swordartonline t03, thesimpsons t02, worldoftanks t02, fivenightsatfreddys t03, hearthstone t01.

**T3-023|T3-095, playing inside or working out (7 items).** Playing inside the change leads unless most concepts work it out. T3-095 is added at three concepts of its own. Items: paragon t08, hawks t07, smashbros t01, criticalrole t02, ElderScrolls t01, h3h3productions t23, transformers t01.

**T3-048|T3-095, open or known (6 items).** An open question whether an announcement is a joke is T3-095. Judging a known joke is T3-048. The larger share decides. Items: clg t08, gameofthrones t09, paladins t01, thesilphroad t02, btc t01, loltyler1 t01.

**T3-032|T3-097, the jokes or the look (5 items).** Complaints and end-requests about the sub's own joke look or rule go to T3-097; objections to the jokes as jokes go to T3-032. Items: anime_irl t16, anime_irl t17, hunterxhunter t03, pcmasterrace t02, survivor t10.

**T3-063|T3-185, applied or made (5 items).** A moderator's exception for the day, or a kind of post banned, counts as a rule made (T3-185). Members asking what the rules allow is T3-063. Items: anime_irl t05, destiny t06, ss13 t11, russia t12, leafs t12.

**T3-001|T3-017, a fake or ordinary posts (4 items).** Ruled as written. Items: ohio t01, homelab t03, planetside t05, titanfall t03.

**T3-015|T3-063, pointer or rule (4 items).** Removals with a pointer to a gathering thread count toward T3-015. A standing rule pointing to a standing thread is not a canvas gathering thread, and the discriminator does not separate the two. Items: fireemblem t08, futanari t06, serbia t15, stardustcrusaders t21.

**T3-023|T3-051, upvote bargains (4 items; conflict CC-007).** A bargain "if this gets N upvotes" is T3-051. It is T3-023 only where the change was made. Items: partyparrot t16, titanfall t05, warframe t06, warriors t04.

**T3-031|T3-048 (3 items) and T3-023|T3-031 (1).** The canvas condition beside other G01 themes. Items: GuildWars2 t02, GuildWars2 t05, rocketleague t15; stardustcrusaders t10.

**Single items.** T3-023|T3-048, a named organisation's reveal with no change to the sub: rit t01. T3-023|T3-100, a look brought back two years later: wallstreetbets t03. T3-023|T3-185, was the rule meant to hold: redhotchilipeppers t04. T3-001|T3-051, a promise traded for upvotes: 4chan t12.

Three gaps were ruled the same way each time they were met; their items are in the unresolved list above: April Fools play that is not posted as true; another sub's change; moderators applying standing rules to non-canvas posts.

### Packet 2

Seven pairs split five or more of packet 2's items on their primaries and were ruled before its first item. The item counts are the packet 2 items that carry the pair in `boundary_ruling`, which include items whose readers split on an added theme.

**T3-002|T3-033, a call or a new mark (20 items).** The discriminator: "Count the concepts of each: is the larger share an idea of what to make offered to the room (T3-033), or hands called to a mark already chosen (T3-002)?" A concept naming a new mark for the room counts toward T3-033, even when it also asks for help. A call to a mark already named counts toward T3-002. A tie goes to T3-002 when the mark was already chosen, and to T3-033 when it was not. Items: androidgaming t01, anime t01, chicago t01, clashroyale t02, criticalrole t03, drumcorps t05, nascar t06, onepunchman t01, polyamory t01, rutgers t03, seahawks t01, TheAdventuresofTintin t01, twentyonepilots t02, chess t07, nlsscirclejerk t01, nonbinary t01, opticgaming t03, uiowa t01, gameattack t03, bigbang t01.

**T3-002|T3-038, a call or the work's progress (19 items).** A concept counts toward T3-002 when it calls, volunteers or answers a call ("come help", "I'm in", "on it"). It counts toward T3-038 when it places pixels or reports the work's state, and coordinates given as where the work in progress stands count there too. A tie goes to T3-038 when the work was placed. Items: auburn t01, bindingofisaac t02, dallasstars t05, ghibli t01, gorillaz t03, newzealand t07, shrooms t06, streetfighter t04, transformers t02, bangtan t01, battlecats t05, cloud9 t03, FinalFantasy t02, foxstevenson t02, torontoraptors t04, traaaaaaannnnnnnnnns t01, rutgers t05, smashbros t04, xenoblade_chronicles t02.

**T3-014|T3-153, the room's own chat or a meeting place (18 items).** Another room must be in the chat in the words. A Discord where the room alone plans is T3-014. Five items are scheme-ambiguous on the discriminator, because it does not name another room's server or a shared one. Items: armenia t08, bangtan t04, belgium t03, dmt t03, eve t10, FederationPlace t06, giivasunner t12, GreenCorner t02, metalgearsolid t08, ohio t08, paladins t25, placehearts t06, rocketbeans t04, theitalyplace t07, AcePlace t06, aoe2 t07, araragi t03, iceland t05.

**T3-002|T3-070, a call or directions (13 items).** A call that names where the work is counts as a call. A concept made mostly of coordinates, templates, colours, order of placing or how-to counts as directions. Teaching a newcomer how one pixel is placed is T3-016 (the correction below). Items: bardmains t01, danganronpa t03, dankmemes t15, python t06, witcher t01, clg t01, harrypotter t15, cowchop t01, mysterydungeon t01, paragon t01, shield t01, Moondye7 t02, seventeen t01.

**T3-002|T3-005, a rally or a defence (12 items).** The attack must be in the words. A call to "protect" a mark with no attacker in view is T3-002. Items: btc t02, Clannad t02, crusaderkings t01, FlaggyFlag t02, harrypotter t01, monalisaclan t02, ohio t03, czech t01, malta t02, nin t10, thetreesnetwork t01, prequelmemes t02.

**T3-070|T3-091, directions or one plan (7 items; conflict CC-012).** Posting or updating a template counts toward T3-070. Telling members to follow the current plan, declaring a copy stale, correcting placers who stray, and an official design thread count toward T3-091. Items: stlouisblues t01, FloydVsVoid t02, heyyea t01, starryknights t02, ChronoTrigger t02, mylittlepony t04, PlaceNL t01.

**T3-004|T3-070, the design or its directions (6 items).** Arguing which version, colour, letter or size counts toward T3-004, and so do corrections "to make the placed work match the design". Posting the template, grid, coordinates or placing order counts toward T3-070. Items: berserk t06, foxstevenson t03, nyu t01, pitt t02, muse t02, suomi t06.

Two pairs reached four items and were decided by their discriminators as met: T3-002|T3-062 and T3-062|T3-084. "Canvas group" is not defined, and greenbaypackers t12 is scheme-ambiguous on it.

### Packet 3

Twelve pairs split five or more of packet 3's items on their primaries (`out/_analysis/b4_packet_pairs.py --packet 3`). Three carry over from packet 2 as written: T3-002|T3-033, T3-002|T3-038 and T3-004|T3-070. Nine were ruled before packet 3's first item. Each paragraph says how one concept counts toward one act or the other; the act with more concepts leads, and the other is added under rule 0 when it has concepts of its own. The item lists are the packet 3 items that carry the pair in `boundary_ruling`.

**T3-033|T3-041, the first mark or a further piece (25 items; conflict CC-019).** The discriminator: "Is the room's first mark proposed (T3-033), or a second piece beside an existing one (T3-041)?" A proposal counts toward T3-041 when the words or the item show the room's mark already standing or chosen; with no standing mark in view, it counts toward T3-033. A reader who placed a further piece as T3-033 read T3-033's `must_show`, which does not say "first"; those items are scheme-ambiguous on that field. Items: truestl t02, cmu t01, metalgearsolid t04, muse t01, aoe2 t04, denmark t10, eagles t02, eve t03, gameofthrones t02, indieheads t13, KState t01, math t02, nuclearthrone t01, portal t02, purplecorner t03, rust t09, simonfraser t04, splatoon t03, suomi t02, touhou t08, ufl t01, blackmirror t05, borderlands t04, empiredidnothingwrong t11, winnipegjets t11.

**T3-038|T3-041, the first build or a further piece's (16 items).** Neither theme has a discriminator against the other. Placing the room's first mark and reporting its state count toward T3-038; proposing, placing or reporting a further piece or an enlargement count toward T3-041. Where the item does not show which piece came first, the piece the room began first is the first mark. T3-038's `must_show` does not say "first", so an item whose split turns on a further piece's progress is scheme-ambiguous on that field. Items: sakuragakuin t01, jerma985 t03, nuclearthrone t05, bobross t01, cavestory t01, dota2 t11, madokamagica t01, msu t02, parahumans t01, touhou t02, AyyMD t01, cubers t21, cubers t25, samuraijack t10, suomi t27, yumenikki t01.

**T3-004|T3-041, the look or an addition (14 items).** The discriminator: "Is the existing mark's look settled (T3-004), or a new piece or enlargement added (T3-041)?" A concept counts toward T3-041 when it adds what the mark did not hold: a further figure, lettering beneath or beside it, an object around it, or a standing mark made bigger. A concept counts toward T3-004 when it changes the look of the mark as planned or placed: colours, letters, outline, shading, a detail inside the figure, the planned size, corrections. Items: ubreddit t03, ElderScrolls t05, funhaus t01, nin t03, radiohead t01, skyrim t02, bindingofisaac t03, DatBoi t04, factorio t09, placetardis t02, ProfessorLayton t02, starlightstage t12, borderlands t02, enterthegungeon t03.

**T3-004|T3-169, the design or the sub's name (8 items; conflict CC-022).** Any concept whose object is the sub's name or its short form counts toward T3-169, its letters, fit and colours included. T3-004 takes the look of the picture the name sits beside. Where the room's whole mark is the sub's name, T3-004's "letters, fonts" also reach it; those items are scheme-ambiguous on the discriminator. Items: bisexual t03, greyblob t02, monstercat t06, unturned t09, drawhelix t05, farmcarrots t08, neopets t14, wine t08.

**T3-004|T3-038, the look or the placing (8 items).** Placing pixels and reporting the work's state count toward T3-038. Arguing the look, and correcting placed pixels to match the design, count toward T3-004. Restoring damage is T3-021. A fix to the template's own error is T3-004. Items: portal t01, timbers t02, AvoArmy t01, calgaryflames t01, uoft t08, bitcoin t02, detroitlions t04, paydaytheheist t02.

**T3-038|T3-070, the work's place or directions (7 items).** Coordinates given as where the work stands count toward T3-038; a starting point, template, grid, colour order or "start at" given for others to place counts toward T3-070. A link that only shows where finished work is goes to T3-026. Items: berkeley t03, gameattack t04, virginiatech t03, planetside t08, bdsm t01, re_zero t06, formula1 t06.

**T3-004|T3-020, the look or the spot (7 items).** A concept that resizes or reshapes the mark to fit a spot counts toward T3-004; one that moves it or picks the spot counts toward T3-020. Items: blackmirror t02, borussiadortmund t03, minecraft t04, kingdomhearts t12, oneshot t01, nightinthewoods t02, utaustin t01.

**T3-004|T3-033, a subject or its look (6 items).** A concept that offers a subject to make counts toward T3-033 until the room has chosen one. Once a subject is chosen, a concept on its version, colours, letters, size or outline counts toward T3-004. T3-004's `must_show` opens with "which picture or version", which also reads as choosing the subject; items whose split turns on those words are scheme-ambiguous on it. Items: frc t01, nlsscirclejerk t02, WPI t01, redhotchilipeppers t03, starlightstage t09, yugioh t04.

**T3-020|T3-033, what or where (1 item carries the pair).** Neither theme has a discriminator against the other. A concept that names what to make counts toward T3-033; one that names where counts toward T3-020. Item: tetris t01.

**Carried from packet 2 into packet 3.** T3-002|T3-033 (10 items): chicubs t09, DiamondClub t01, foxes t01, hawks t05, kanye t01, schoolidolfestival t04, stardustcrusaders t01, unturned t03, wallstreetbets t01, warframe t01. T3-002|T3-038 (9 items): bostonbruins t02, enterthegungeon t01, ethoslab t01, forsen t01, habs t02, nyjets t04, the_pack t01, winnipegjets t01, wow t17. T3-004|T3-070 (9 items): crusaderkings t02, penguins t03, udub t01, drumcorps t06, kanye t05, Okami t06, pebble t04, placesnek t04, portal t03.

Two pairs reached four items and were decided by their discriminators as met: T3-021|T3-038 (first build or restored; conflict CC-017) and T3-026|T3-082 (a mark the room did not know of, or its own work announced; conflict CC-021). A member asking where a known mark is and being told is T3-026 (haskell t14, baylor t05); a mark shown that the room had not known of is T3-082 (riskofrain t01).

Three readings were written in `boundaries.md` while the packet was ruled. Each names the item where it was first met. Rulings made earlier that a reading would have decided differently were revised to match: catalonia t07 and sadboys t03.
- **The homeland flag (from item 16).** Work on the stripes, stars, proportions, colours, size, spot and repair of the flag of the room's land counts toward T3-065. Emblems in or beside it count toward T3-113. Readers' T3-004, T3-020 and T3-041 on that work are scheme-ambiguous on that theme's `must_not_show`. 22 packet 3 rulings place T3-065. catalonia t07 was revised to match.
- **A design cut down to the hands (from item 12; conflicts CC-013 and CC-020).** A smaller or simpler version of the same mark counts toward T3-004. T3-069 takes it only when one of the room's pieces is dropped for another, and T3-042 only when growth is set aside to keep what stands. Doubt that the room has the hands at all stays T3-136. sadboys t03 in packet 2 was revised from T3-069 to T3-004. day9 t04 shows both halves: the motto dropped for the logo is T3-069, and the TV cut from the logo is T3-004.
- **A celebration while placement goes on (from item 280).** T3-026's `decide_when_both` decides it: words that call a piece done, complete or finished and celebrate it count toward T3-009, during placement or after it. Words that show the mark up, still there or holding "for now" count toward T3-026. Where both halves are met, the item is scheme-ambiguous on T3-026's `decide_when_both`.

## Corrections made during the packets

Each correction went through `b4_rule_append.py --replace`, which rewrites the ruled line in place, marks it `revised`, and keeps the old ledger under a superseded name.
- **formula1 t05 and elitedangerous t01** (packet 1). T3-063 takes canvas posts only.
- **The T3-016 correction** (packet 2, at item 146). Teaching a newcomer to place is T3-016 when it explains the event, and T3-070 only when it directs the room's own work. bindingofisaac t02 was revised.
- **The T3-033 and T3-041 reading** (packet 2, from item 140). clashroyale t02 was revised from T3-033 to T3-041.
- **The homeland-flag reading** (packet 3). catalonia t07's senyera bars moved from T3-004 to T3-065.
- **The cut-down reading** (packet 3). sadboys t03 (packet 2) moved from T3-069 to T3-004.
- **T3-170 for members' own misclicks** (packet 3, from item 430). T3-170's `must_show` names "members' own misclicks or misplaced pixels owned and forgiven". bisexual t04 and kpop t05 were revised to place it.
- **Concepts of their own** (packet 3). `b4_rule_append.py` refuses a placed theme only when its concept list equals another's. The new read-only check `out/_analysis/b4_own_support_check.py` lists every placed theme whose concepts all sit under the ruling's other themes. It found seven: ManningPlace t05, KState t04, rainbowgrid t01, dofus t01, skyrim t03 and teamcube t04 in packet 3, and nerf t08 in packet 1. All seven were rewritten so each placed theme has a concept of its own, and the check now finds none over the three packets.
- **Boundary tags** (packet 3). Eleven packet 3 rulings applied packet 2's counting rule but carried no `boundary_ruling`. The tag was added and the rulings are unchanged (`out/_analysis/b4_br_tag_draft.py`): T3-002|T3-038 on nine items and T3-002|T3-033 on hawks t05 and stardustcrusaders t01.

## The conflicts pass

`coder_conflicts.jsonl` holds 25 lines. CC-001 to CC-008 came from packet 1's notes, CC-009 to CC-016 from packet 2's, CC-017 to CC-025 from packet 3's, each read before its packet's first ruling. Packet 3's conflicts and the splits they explain:
- **CC-017:** making the mark and keeping it are named as one building practice, while the scheme splits first build (T3-038), repair (T3-021) and defence (T3-005).
- **CC-018:** "what and where to draw" heads themes whose readings fall on T3-033, T3-004 and T3-020.
- **CC-019:** a further piece is proposed in the words used for the room's first mark (T3-033|T3-041).
- **CC-020:** a design cut down to the hands, as CC-013 in packet 2 (the cut-down reading).
- **CC-021:** telling people where the mark is is written as showing it, finding it and giving coordinates (T3-026|T3-082).
- **CC-022:** the sub's name on the canvas is filed as lettering, an addition, a sign for visitors and a dropped plan (T3-004|T3-169).
- **CC-023:** political and religious content argued for a national mark is written as design argument in most rooms and as a political inscription in one (T3-004, T3-113, T3-130).
- **CC-024:** arguing whether to grow the mark or hold it is named by one side (T3-041, T3-042, T3-061).
- **CC-025:** themes grouped by exclusion, as CC-008 and CC-016. Six of packet 3's seven unresolved items are among them.

## Agreement before and after

Before is the two readers against each other. After is each reader against the ruling, over the items not unresolved. Both use stage B2's definition: mean Jaccard on placement sets, with primary match beside it. The next table gives both, by packet and over the three.

| | mean Jaccard before | primary match before | mean Jaccard after | primary match after |
|---|---|---|---|---|
| packet 1 (491; 439 after) | 0.486 | 0.578 | 0.633 | 0.697 |
| packet 2 (447; 437 after) | 0.537 | 0.678 | 0.603 | 0.706 |
| packet 3 (500; 493 after) | 0.475 | 0.598 | 0.473 | 0.535 |
| all (1,438; 1,369 after) | 0.498 | 0.616 | 0.566 | 0.642 |

The figure after is not a reliability figure. It is agreement following an adjudication I performed. In packets 1 and 2 it rose, because the ruling usually kept one reader's list. In packet 3 it fell below the readers' agreement with each other, on Jaccard (0.473 against 0.475) and on the primary (0.535 against 0.598). Each theme added that neither reader chose lowers both readers' Jaccard against the ruling, and each primary moved off a theme both readers put first lowers the primary match. The named_neither section gives the counts. The blind sample's adjudicated stratum at B4b is the test of whether a stranger reaches these rulings.

## Whether stage B2's predictions held

`confusions.md` predicted nineteen pairs. A packet can show only the pairs whose themes it holds.

- **Packet 1 (G01, G02).** Four predicted pairs could appear, and all four split readers: pair 3 (T3-001|T3-023, 20 items whose readers split their primaries), pair 15 (T3-001|T3-095, 11), pair 19 (T3-015|T3-063, 7) and pair 7 (T3-015|T3-075, 4). Three pairs B2 did not predict split as often or more: T3-017|T3-031 (17), T3-001|T3-048 (13) and T3-023|T3-095 (11).
- **Packet 2 (G03 to G06).** Five predicted pairs hold a theme of these families. Two split readers: pair 6 (T3-002|T3-033, 8) and pair 8 (T3-004|T3-070, 6). Pairs 4, 17 and 18 split none. Five pairs B2 did not predict split as often or more: T3-002|T3-038 (10), T3-002|T3-070 (8), T3-002|T3-005 (7), T3-014|T3-153 (5) and T3-070|T3-091 (5).
- **Packet 3 (G07, G08 in part).** Five predicted pairs hold a G07 or G08 theme. Four split readers: pair 6 (T3-002|T3-033, 10), pair 10 (T3-004|T3-038, 9), pair 8 (T3-004|T3-070, 6) and pair 5 (T3-004|T3-020, 5). Pair 17 (T3-044|T3-082) split none. Seven pairs B2 did not predict split as often or more often than pair 5: T3-004|T3-041 (12), T3-033|T3-041 (11), T3-004|T3-033 (9), T3-002|T3-038 (9), T3-020|T3-033 (7), T3-038|T3-041 (7) and T3-038|T3-070 (7).

Twenty-two different pairs are named above as splitting readers, and eight of them were predicted. Three of packet 3's seven unpredicted pairs hold T3-041, and B2's list holds no pair with T3-041. Three of packet 2's five unpredicted pairs hold T3-002, and T3-002|T3-038 split readers again in packet 3. Pairs 4, 17 and 18 hold themes of packets 2 and 3 and split none there. The other eight predicted pairs (1, 2, 9, 11, 12, 13, 14, 16) belong to families in packets 4 to 7.
