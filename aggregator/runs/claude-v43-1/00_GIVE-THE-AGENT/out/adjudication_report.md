# Adjudication report, stage B4 (interim: packets 1 and 2 of 7)

Written at B4a-02 after packet 2 was ruled. It is rewritten whole after each packet; the figures below cover packets 1 and 2. Per-packet figures: `out/_adjudication-B4/packet-01/summary.md` and `out/_adjudication-B4/packet-02/summary.md` (`out/_analysis/b4_packet_summary.py`). The sums over both: `out/_analysis/b4_cumulative.py --packets 1,2`. The rulings: `out/disagreements.jsonl`. The boundary paragraphs: `out/_adjudication-B4/boundaries.md`, carried below with their item lists.

## Items adjudicated

Stage B3's inventory (`b3_classes.jsonl`, J's five classes) leaves 3,288 contested items: class 3 (the readers' lists differ) 2,393, class 4 (the readers agree on a list not inside my B1 grouping) 837, class 5 (no B1 grouping) 58.
- **Packet 1** ruled 491: the 18 gloss-only items, G01 (April Fools in the sub) and G02 (the sub's own business).
- **Packet 2** ruled 447: G03 (where the planning happens), G04 (calling people in to place), G05 (telling placers what to place) and G06 (strain, doubt and giving up).

Together 938 items: 638 class 3, 277 class 4, 23 class 5. 2,350 contested items remain for packets 3 to 7.

## The taxonomy split

The next table counts the rulings by taxonomy value, by packet and by class.

| taxonomy | all | packet 1 | packet 2 | class 3 | class 4 | class 5 |
|---|---|---|---|---|---|---|
| genuine-joint | 352 | 137 | 215 | 352 | 0 | 0 |
| scheme-ambiguous | 185 | 123 | 62 | 150 | 33 | 2 |
| author-error | 155 | 97 | 58 | 2 | 142 | 11 |
| author-disagrees | 102 | 37 | 65 | 0 | 92 | 10 |
| reader-error | 80 | 77 | 3 | 80 | 0 | 0 |
| item-is-a-bag | 64 | 20 | 44 | 54 | 10 | 0 |
| total | 938 | 491 | 447 | 638 | 277 | 23 |

How to read it:
- **Genuine-joint is the largest value, 352 (37.5%).** In packet 2 it is 215 of 447 (48.1%). Packet 2's themes are coordination threads, where one coder's theme often holds calls for hands, directions, progress reports and proposals at once. One reader places the leading act alone and the other adds a second. The freeze's counting rule for T3-002, T3-033 and T3-038 decides the order once each concept is assigned to an act. The count measures how rule 0 travelled, not the readers.
- **Scheme-ambiguous is 185 (19.7%).** Packet 1 had 123 (25.1%); packet 2 had 62 (13.9%). The coordination families decide more often than the April Fools families did.
- **Item-is-a-bag is 64.** Packet 2 has 44 of them. They are long coordination threads where four themes or more have three concepts of their own. The largest is theblackvoid t05, with T3-006 placed for 31 named targets and fourteen themes under `also_present`.
- **Reader-error fell from 77 in packet 1 to 3 in packet 2:** fullcommunism t07 (T3-042), austria t10 (T3-017) and catalunya t08 (T3-196). Packet 1's were mostly a canvas-only test applied to non-canvas talk, which packet 2's families do not invite.
- **A second theme on one or two concepts** was added where the concept passes another theme's gate as its own act, for example T3-169 for one sign concept (TeamYellowPlace t05). This was not perfectly even in either packet. magictcg t09's megathread concept was left unplaced in packet 1, while similar single concepts were placed elsewhere.

## author-error and author-disagrees

author-error: 155 (packet 1 97, packet 2 58). author-disagrees: 102 (packet 1 37, packet 2 65). Both come almost wholly from class 4, where the readers agreed on a list my B1 grouping did not hold.

The two packets differ:
- **Packet 1.** In class 4 I took the readers' list in 89 items and kept a B1 theme in 29.
- **Packet 2.** In class 4 I took the readers' list in 53 items and kept a B1 theme in 63; 8 are bags.

Of packet 2's 65 author-disagrees rulings, 39 keep the readers' theme and add a theme from my B1 grouping under rule 0. 20 drop a reader's theme. 6 are empty rulings, where the words show no doing to place. The commonest themes kept against both readers are in G08 (building and growing the mark): T3-069 6, T3-038 6, T3-041 4. T3-084 (5) and T3-002 (4) follow.

I cannot separate how much of that reversal is the scheme and how much is my pull toward my own grouping. The blind sample at B4b tests the adjudicated stratum against fresh readers, and these items are part of it.

My commonest B1 errors:
- **Packet 1:** T3-031 placed on an in-joke with no canvas in it; T3-001 placed where nothing was posted as true; T3-063 on posts that are not canvas posts; T3-032 where the complaints were about the sub's own joke styling.
- **Packet 2:** calls for hands that my B1 had placed as the proposal (T3-033, 4), the progress (T3-038, 3) or a further piece (T3-041, 2), among 14 rulings that take T3-002; placing troubles on the timer, a glitch or a phone (T3-074, 6); posted templates that my B1 had placed as one plan imposed (T3-091, 2), among 6 rulings that take T3-070.

## Fields by ambiguity

The next list counts the 185 scheme-ambiguous rulings by the field whose sentence failed, with packet 1 and packet 2 in brackets.

- must_show: 111 (78, 33)
- discriminators: 56 (39, 17)
- decide_when_both: 10 (4, 6)
- must_not_show: 8 (2, 6)

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, over both packets. Stage C1 opens with it.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-017 | 29 | 5 | 0 | 1 | 23 |
| T3-023 | 27 | 25 | 0 | 0 | 2 |
| T3-001 | 24 | 18 | 0 | 0 | 6 |
| T3-002 | 12 | 0 | 2 | 3 | 7 |
| T3-033 | 9 | 9 | 0 | 0 | 0 |
| T3-063 | 8 | 6 | 1 | 0 | 1 |
| T3-095 | 7 | 3 | 0 | 2 | 2 |
| T3-032 | 6 | 6 | 0 | 0 | 0 |
| T3-014 | 6 | 1 | 0 | 0 | 5 |
| T3-048 | 5 | 5 | 0 | 0 | 0 |
| T3-015 | 4 | 1 | 0 | 0 | 3 |
| T3-100 | 3 | 3 | 0 | 0 | 0 |

36 more themes failed on 45 rulings between them, none more than three times.

The sentences that failed most:
- **T3-017's discriminator** "Is it the room's running in-joke carried into the canvas talk or the day (T3-031)" (packet 1). Its "or the day" contradicts T3-031's own canvas condition.
- **T3-023's** "A change made to a whole sub for April Fools" (packet 1). It does not say whose sub, and its "or by a sub acting together" reaches a members' flood.
- **T3-001's** "Members of the room themselves post something false as true for April Fools" (packet 1). It leaves April Fools play that is not posted as true with no theme, and it catches a member relaying an outside joke.
- **T3-033's** "An idea of what the room should put on the canvas, offered to the room" (packet 2, all 9). It does not say "first". T3-041's `must_not_show` gives "The room's first mark proposed" to T3-033, so a further piece beside a standing mark is T3-041, and readers placed it as T3-033.
- **T3-014's discriminator** "Is the chat the room's own planning place (T3-014), or where it meets other rooms (T3-153)?" (packet 2, 5). A shared server or another room's server is not named on either side.
- **T3-002's tests on the national flag** (packet 2, 5): its discriminator against T3-065 and its `must_not_show` "The national flag as the room's mark carries T3-065". Calls to build or protect the land's flag sit on both sides.

The other packet 2 failures are single sentences, among them:
- T3-074's `must_show` read as covering a member's exams and sleep;
- T3-036, T3-117 and T3-148 with no line between "too late", "the end registered" and "a design shown too late";
- T3-059 with no line against T3-069 when one piece is dropped for another;
- T3-137 speaking only of joins made;
- T3-170 naming misclicks but not glitches.

## The named_neither rate

named_neither: 239 of 938 (25.5%). Packet 1: 84 of 491 (17.1%). Packet 2: 155 of 447 (34.7%).

Packet 1's came from three sources:
- a second or third theme added by a scheme rule that neither reader applied, chiefly T3-097 on one concept and T3-095 or T3-032 at three;
- a theme in a family the readers did not open: T3-185, T3-126 and T3-157 from G02 items whose readers opened G01, and T3-069 or T3-090 beside T3-015;
- my own B1 theme kept against both readers.

In packet 2, 98 of the 155 add only themes from my B1 grouping. 57 add a theme that no placement held, mostly from a family next to the one the readers opened: T3-041 8, T3-153 4, T3-038 4, T3-015 3, T3-002 3.

The rate says the readers often stop at the first family that fits. Packet 2's items, filed under G03 to G06, often hold progress reports, further pieces and narrowing from G08 beside the leading act. The rate is also the measure of my pull toward my own reading, which no procedure removes. It doubled in packet 2 while class 4's yield fell, and 88 of the 239 are author-disagrees, where the theme is mine.

## The unresolved count

unresolved: 62 of 938 (6.6%). Packet 1: 52 (10.6%). Packet 2: 10 (2.2%). The next lists name them by the reason the scheme did not decide.

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
- **One concept with no doing to place** (author-disagrees in class 4, empty ruling in class 5), 6:
  - minecraft t17 ('/r/place Minecraft Server');
  - popheads t01 (a 'Dissertation' posted at a Discord user's request);
  - h3h3productions t27 ('Sweet');
  - shield t07 ('I don't get this at all...');
  - kuwait t09 ('MOI GUYS');
  - minecraft t18 ('place').
- **A pointer to another sub's thread on the room's canvas work** (T3-015 `must_show`), 1: Redox t02.
- **Naming a feature of a colour faction's ground** ('the Beam'; T3-070 `must_show`), 1: orderofthebluecorner t02.
- **A bare question with no answer** (T3-018 and T3-073 `must_show`), 2: THE_R t03 ('The R?'), parrots t15 ('I still have no idea what happened here').

## The boundary rulings

Each pair is one paragraph in `boundaries.md`. Each paragraph's ruling is summarised here with its item list.

### Packet 1

**T3-001|T3-023, the joke's stage (32 items).** A change to the sub's name, look, rules or subject made by its moderators, or by members flooding it "as a sub acting together", is T3-023. Members' own false claims in an unchanged sub are T3-001. Both, each with concepts of their own: the larger primary. Items: aceattorney t01, MMA t02, nlsscirclejerk t08, rit t02, totallynotrobots t06, totallynotrobots t08, AceOfAngels8 t01, clashroyale t03, enterthegungeon t02, flyers t05, furry t09, harrypotter t06, kilian t08, mylittlepony t08, porterrobinson t08, porterrobinson t09, ss13 t01, teslamotors t01, toolband t02, totallynotrobots t02, totallynotrobots t03, totallynotrobots t04, totallynotrobots t07, OneTrueEmilia t01, apocalypserising t01, formula1 t02, greece t07, polska t03, thetreesnetwork t02, totallynotrobots t01, ubc t02, zootopia t01.

**T3-001|T3-048, whose joke (20 items).** The source shown in the concepts decides. Where it cannot be read, the ruling is unresolved. A member relaying an organisation's joke is T3-048 by the discriminator, though T3-001's test catches it (conflict CC-002). Items: btc t04, bitcoin t06, feedthebeast t02, opticgaming t01, uofmn t01, baylor t02, GuildWars2 t01, GuildWars2 t10, runescape t07, rutgers t01, starlightstage t03, warframe t15, yugioh t10, yugioh t11, danganronpa t19, falcons t10, kamenrider t07, lego t07, simonfraser t02, ubreddit t02.

**T3-017|T3-031, the canvas condition (15 items here, with T3-001|T3-031: rwby t03).** T3-031 requires the canvas, and T3-017's and T3-001's discriminators do not. T3-031's own test governs: an in-joke with no canvas in it is T3-017. Every item is scheme-ambiguous on T3-017's discriminator. Items: cubers t30, ethereum t06, falcons t08, flashtv t04, freedomplanet t05, h3h3productions t06, h3h3productions t12, heyyea t07 (canvas in it: T3-031), indieheads t06, mls t07, PlaceNL t20, romania t22 (T3-130), SydneyFC t03, tf2 t09, torontoraptors t03.

**T3-001|T3-095, who staged the claim (8 items).** A test of a member's own fake is T3-001 "even when readers test it". A test of anyone else's claim is T3-095. In fivenightsatfreddys t03 and hearthstone t01 both readers put the tests of members' fakes under T3-095, so those are scheme-ambiguous. Items: linux t04, planetside t01, romania t12, swordartonline t03, thesimpsons t02, worldoftanks t02, fivenightsatfreddys t03, hearthstone t01.

**T3-023|T3-095, playing inside or working out (7 items).** Playing inside the change leads unless most concepts work it out. T3-095 is added at three concepts of its own. Items: paragon t08, hawks t07, smashbros t01, criticalrole t02, ElderScrolls t01, h3h3productions t23, transformers t01.

**T3-048|T3-095, open or known (6 items).** An open question whether an announcement is a joke is T3-095. Judging a known joke is T3-048. The larger share decides. Items: clg t08, gameofthrones t09, paladins t01, thesilphroad t02, btc t01, loltyler1 t01.

**T3-032|T3-097, the jokes or the look (5 items).** T3-032's "stop them or take them down" and T3-097's "requests to switch back" overlap. Complaints and end-requests about the sub's own joke look or rule go to T3-097; objections to the jokes as jokes go to T3-032. Items: anime_irl t16, anime_irl t17, hunterxhunter t03, pcmasterrace t02, survivor t10.

**T3-063|T3-185, applied or made (5 items).** A moderator's exception for the day, or a kind of post banned, counts as a rule made (T3-185). Members asking what the rules allow is T3-063. Items: anime_irl t05, destiny t06, ss13 t11, russia t12, leafs t12.

**T3-001|T3-017, a fake or ordinary posts (4 items).** Ruled as written. Items: ohio t01, homelab t03, planetside t05, titanfall t03.

**T3-015|T3-063, pointer or rule (4 items).** Removals with a pointer to a gathering thread count toward T3-015. A standing rule pointing to a standing thread, such as a requests sticky or Random discussion, is not a canvas gathering thread, and the discriminator does not separate the two. Items: fireemblem t08, futanari t06, serbia t15, stardustcrusaders t21.

**T3-023|T3-051, upvote bargains (4 items; conflict CC-007).** A bargain "if this gets N upvotes" is T3-051. It is T3-023 only where the change was made. Items: partyparrot t16, titanfall t05, warframe t06, warriors t04.

**T3-031|T3-048 (3 items) and T3-023|T3-031 (1).** This is the canvas condition beside other G01 themes. Play with the maker's joke content is T3-048, a mash-up played as the sub's day theme is T3-023, and T3-031 needs the canvas. Items: GuildWars2 t02, GuildWars2 t05, rocketleague t15; stardustcrusaders t10.

**T3-023|T3-048 (1 item).** A named organisation's reveal with no change to the sub in the words is T3-048. Item: rit t01.

**T3-023|T3-100 (1 item).** A look brought back two years later, which T3-100's "stay after the day" does not settle. Item: wallstreetbets t03.

**T3-023|T3-185 (1 item).** Was the rule meant to hold? Item: redhotchilipeppers t04.

**T3-001|T3-051 (1 item).** A promise traded for upvotes is T3-051. Item: 4chan t12.

Three gaps were ruled the same way each time they were met. Their items are in the unresolved list above:
- April Fools play that is not posted as true;
- another sub's change;
- moderators applying standing rules to non-canvas posts.

### Packet 2

Seven pairs split five or more of packet 2's items on their primaries and were ruled before its first item. Four of them are T3-002 against a sibling. The item counts below are the items that carry the pair in `boundary_ruling`, which include items whose readers split on an added theme.

**T3-002|T3-033, a call or a new mark (20 items).** The discriminator: "Count the concepts of each: is the larger share an idea of what to make offered to the room (T3-033), or hands called to a mark already chosen (T3-002)?" A concept naming a new mark for the room counts toward T3-033, even when it also asks for help. A call to a mark already named counts toward T3-002. A tie goes to T3-002 when the mark was already chosen, and to T3-033 when it was not. Items: androidgaming t01, anime t01, chicago t01, clashroyale t02, criticalrole t03, drumcorps t05, nascar t06, onepunchman t01, polyamory t01, rutgers t03, seahawks t01, TheAdventuresofTintin t01, twentyonepilots t02, chess t07, nlsscirclejerk t01, nonbinary t01, opticgaming t03, uiowa t01, gameattack t03, bigbang t01.

**T3-002|T3-038, a call or the work's progress (19 items).** The discriminator: "Count the concepts of each: is the larger share the work placed and its progress reported (T3-038), or hands called for it (T3-002)? An opening call does not lead because it comes first." A concept counts toward T3-002 when it calls, volunteers or answers a call ("come help", "I'm in", "on it"). It counts toward T3-038 when it places pixels or reports the work's state, and coordinates given as where the work in progress stands count there too (T3-038's discriminator against T3-070). A tie goes to T3-038 when the work was placed. Items: auburn t01, bindingofisaac t02, dallasstars t05, ghibli t01, gorillaz t03, newzealand t07, shrooms t06, streetfighter t04, transformers t02, bangtan t01, battlecats t05, cloud9 t03, FinalFantasy t02, foxstevenson t02, torontoraptors t04, traaaaaaannnnnnnnnns t01, rutgers t05, smashbros t04, xenoblade_chronicles t02.

**T3-014|T3-153, the room's own chat or a meeting place (18 items).** The discriminator: "Is the chat the room's own planning place (T3-014), or where it meets other rooms (T3-153)?" Another room must be in the chat in the words: invited into the room's Discord to talk, visited in its own, or met in a shared server. A Discord where the room alone plans is T3-014. Where a deal is struck there, T3-153's `decide_when_both` makes the deal's kind primary. Five items are scheme-ambiguous on the discriminator, because it does not name another room's server or a shared one. Items: armenia t08, bangtan t04, belgium t03, dmt t03, eve t10, FederationPlace t06, giivasunner t12, GreenCorner t02, metalgearsolid t08, ohio t08, paladins t25, placehearts t06, rocketbeans t04, theitalyplace t07, AcePlace t06, aoe2 t07, araragi t03, iceland t05.

**T3-002|T3-070, a call or directions (13 items).** T3-070's `decide_when_both`: "T3-070 when the directions lead, T3-002 when the call does; both with concepts of their own, rule 0." A call that names where the work is ("help us at 200, 300") counts as a call. A concept made mostly of coordinates, templates, colours, order of placing or how-to counts as directions. Teaching a newcomer how one pixel is placed is not a call; see the correction below. Items: bardmains t01, danganronpa t03, dankmemes t15, python t06, witcher t01, clg t01, harrypotter t15, cowchop t01, mysterydungeon t01, paragon t01, shield t01, Moondye7 t02, seventeen t01.

**T3-002|T3-005, a rally or a defence (12 items).** The discriminator: "Is the call to build or finish (T3-002), or to defend against an attack under way (T3-005)?" The attack must be in the words. A call to defend against an attacker, an alarm, or a report of an attack repelled counts toward T3-005. A call to build, finish or repair with no attack named counts toward T3-002, whose `must_show` names "rallies to build, finish or repair a work". A call to "protect" a mark with no attacker in view is T3-002. Items: btc t02, Clannad t02, crusaderkings t01, FlaggyFlag t02, harrypotter t01, monalisaclan t02, ohio t03, czech t01, malta t02, nin t10, thetreesnetwork t01, prequelmemes t02.

**T3-070|T3-091, directions or one plan (7 items; conflict CC-012).** The discriminator: "Are directions shared for use (T3-070), or one plan imposed against others (T3-091)?" Posting or updating a template counts toward T3-070. Telling members to follow the current plan counts toward T3-091, and so do declaring a copy stale, correcting placers who stray, and an official design thread. Items: stlouisblues t01, FloydVsVoid t02, heyyea t01, starryknights t02, ChronoTrigger t02, mylittlepony t04, PlaceNL t01.

**T3-004|T3-070, the design or its directions (6 items).** The discriminator: "Is the design still argued (T3-004), or its directions handed out (T3-070)?" Arguing which version, colour, letter or size counts toward T3-004, and so do corrections "to make the placed work match the design". Posting the template, grid, coordinates or placing order counts toward T3-070. Proposing a simplified design is T3-004; posting the simplified template is T3-070. Items: berserk t06, foxstevenson t03, nyu t01, pitt t02, muse t02, suomi t06.

Two pairs reached four items and were decided by their discriminators as met: T3-002|T3-062 (the room's own members or other subs' members) and T3-062|T3-084 (another sub's membership asked for hands, or another canvas group asked as a group). "Canvas group" is not defined, and greenbaypackers t12 is scheme-ambiguous on it.

## Corrections made during the packets

Each correction went through `b4_rule_append.py --replace`, which rewrites the ruled line in place, marks it `revised`, and keeps the old ledger under a superseded name.
- **formula1 t05 and elitedangerous t01** (packet 1). T3-063 takes canvas posts only.
- **The T3-016 correction** (packet 2, at item 146). The T3-002|T3-070 paragraph first said that teaching a newcomer to place counts as directions. T3-016's `must_show` names "how to pick a colour and place". So such teaching is T3-016 when it explains the event, and T3-070 only when it directs the room's own work. bindingofisaac t02, ruled before the correction, was revised to match.
- **The T3-033 and T3-041 reading** (packet 2, from item 140). T3-041's `must_not_show` gives "The room's first mark proposed" to T3-033, so a proposal of a further piece beside the room's standing mark is T3-041. T3-033's own test does not say "first", so these items are scheme-ambiguous on T3-033's `must_show`. clashroyale t02 was ruled before the reading, while a princess was already under way, and its proposals moved from T3-033 to T3-041 under `also_present`. I checked the T3-033 concepts of the 22 other packet 2 rulings that place it; each proposes a first mark.

## The conflicts pass

`coder_conflicts.jsonl` holds 16 lines. CC-001 to CC-008 came from packet 1's notes; CC-009 to CC-016 from packet 2's, read before its first ruling. Three of packet 2's conflicts explain splits ruled above:
- **CC-011:** showing newcomers where and how to place is named recruitment, instruction or explanation by different coders (T3-002|T3-070, T3-016|T3-070).
- **CC-012:** "getting everyone onto one plan" names publishing a template, holding placers to it, narrowing to one piece and asking moderators for an official project (T3-070|T3-091, T3-069|T3-091).
- **CC-013:** scaling a design to the hands present is written as working around the limit in some rooms and as doubting the room's strength in others (T3-074|T3-136). Peru t03 and sadboys t03 turn on it.

CC-014 (newcomers and returning fans in one note) explains the T3-044|T3-196 rulings.

## Agreement before and after

Before is the two readers against each other. After is each reader against the ruling, over the items not unresolved. Both use stage B2's definition: mean Jaccard on placement sets, with primary match beside it. The next table gives both, by packet and over both.

| | mean Jaccard before | primary match before | mean Jaccard after | primary match after |
|---|---|---|---|---|
| packet 1 (491; 439 after) | 0.486 | 0.578 | 0.633 | 0.697 |
| packet 2 (447; 437 after) | 0.537 | 0.678 | 0.603 | 0.706 |
| both (938; 876 after) | 0.510 | 0.626 | 0.618 | 0.701 |

The figure after is not a reliability figure. It is agreement following an adjudication I performed, and it rises because the ruling usually keeps one reader's list. It rose less in packet 2, where more rulings add a theme that neither reader chose; each such theme lowers the reader's Jaccard against the ruling.

## Whether stage B2's predictions held

`confusions.md` predicted nineteen pairs. A packet can show only the pairs whose themes it holds.

- **Packet 1 (G01, G02).** Four predicted pairs could appear, and all four split readers: pair 3 (T3-001|T3-023, 20 items whose readers split their primaries), pair 15 (T3-001|T3-095, 11), pair 19 (T3-015|T3-063, 7) and pair 7 (T3-015|T3-075, 4). Three pairs B2 did not predict split as often or more: T3-017|T3-031 (17), T3-001|T3-048 (13) and T3-023|T3-095 (11).
- **Packet 2 (G03 to G06).** Five predicted pairs hold a theme of these families. Two split readers: pair 6 (T3-002|T3-033, 8) and pair 8 (T3-004|T3-070, 6). Pair 4 (T3-028|T3-070), pair 17 (T3-044|T3-082) and pair 18 (T3-014|T3-152) split none. Five pairs B2 did not predict split as often or more: T3-002|T3-038 (10), T3-002|T3-070 (8), T3-002|T3-005 (7), T3-014|T3-153 (5) and T3-070|T3-091 (5).

Of the fourteen pairs named above as splitting readers, six were predicted. Four of the eight that B2 missed hold T3-001 or T3-002, the broadest theme of G01 and of G04. The remaining twelve predicted pairs belong to families in packets 3 to 7.
