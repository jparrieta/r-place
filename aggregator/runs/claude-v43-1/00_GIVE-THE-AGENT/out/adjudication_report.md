# Adjudication report, stage B4 (interim: packet 1 of 7)

Written at B4a-01 after packet 1 was ruled. It is rewritten whole after each packet; the figures below cover packet 1 only. Per-packet figures: `out/_adjudication-B4/packet-01/summary.md` (`out/_analysis/b4_packet_summary.py`). The rulings: `out/disagreements.jsonl`. The boundary paragraphs: `out/_adjudication-B4/boundaries.md`, carried below with their item lists.

## Items adjudicated

Stage B3's inventory (`b3_classes.jsonl`, J's five classes) leaves 3,288 contested items: class 3 (the readers' lists differ) 2,393, class 4 (the readers agree on a list not inside my B1 grouping) 837, class 5 (no B1 grouping) 58. Packet 1 ruled 491 of them: the 18 gloss-only items and families G01 (April Fools) and G02 (the sub's own business). By class: 320 class 3, 153 class 4, 18 class 5. 2,797 contested items remain for packets 2 to 7.

## The taxonomy split

The next table counts packet 1's rulings by taxonomy value and by class.

| taxonomy | all | class 3 | class 4 | class 5 |
|---|---|---|---|---|
| genuine-joint | 137 | 137 | 0 | 0 |
| scheme-ambiguous | 123 | 88 | 33 | 2 |
| author-error | 97 | 0 | 89 | 8 |
| reader-error | 77 | 77 | 0 | 0 |
| author-disagrees | 37 | 0 | 29 | 8 |
| item-is-a-bag | 20 | 18 | 2 | 0 |
| total | 491 | 320 | 153 | 18 |

How to read it:
- **Genuine-joint is the largest value.** Most class 3 splits in G01 and G02 are the two readers applying rule 0 differently. One reader places the leading theme alone and the other adds a second. Often the scheme's own rule adds the second at a set count: T3-023's `decide_when_both` adds T3-095 or T3-032 at three concepts, and T3-097 or T3-100 on one. That is a fact about how rule 0 travelled, not about the readers.
- **Scheme-ambiguous is next, at 123 (25%).** In these two families the scheme did not survive being handed over as often as the bags did.
- **Item-is-a-bag is 20.** The bag rule applied when four themes were needed: one placed, the others under `also_present`.
- **A second theme on one concept** was added where a scheme rule says "a concept of its own" (T3-097 and T3-100 under T3-023's rule). Elsewhere it was added only where the concept plainly passes another gate. This was not perfectly even: magictcg t09's one megathread concept was left unplaced, while similar single concepts were placed elsewhere.
- **Reader-error is 77, all in class 3.** It was assigned only where one reader's theme fails a condition its test states plainly, and never where both readers made the same placement. The common cases are a canvas-only test applied to non-canvas talk (T3-063, T3-031, T3-044, T3-121 in part), T3-095 placed on a member's own fake, and T3-048 placed where no maker's joke is in the words. Chunk 18, single-concept G02 items, holds 16 of them. That density is itself worth a look at stage C1.

## author-error and author-disagrees

author-error: 97; author-disagrees: 37. Both come almost wholly from class 4, where the readers agreed on a list my B1 grouping did not hold. There I took the readers' list in 89 items and kept a B1 theme in 29, so I yielded about three times in four. My commonest B1 errors are these:
- T3-031 placed on an in-joke with no canvas in it;
- T3-001 placed where nothing was posted as true;
- T3-063 placed on posts that are not canvas posts;
- T3-032 placed where the complaints were about the sub's own joke styling.

The author-disagrees rulings are where both readers took a window's restyle or post for April Fools with no April Fools in the words (T3-017 kept), or missed a theme from a family they did not open (T3-185, T3-069, T3-044).

## Fields by ambiguity

The next list counts the 123 scheme-ambiguous rulings by the field whose sentence failed.

- must_show: 78
- discriminators: 39
- decide_when_both: 4
- must_not_show: 2

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide. Stage C1 opens with it.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-017 | 29 | 5 | 0 | 1 | 23 |
| T3-023 | 27 | 25 | 0 | 0 | 2 |
| T3-001 | 24 | 18 | 0 | 0 | 6 |
| T3-063 | 8 | 6 | 1 | 0 | 1 |
| T3-095 | 7 | 3 | 0 | 2 | 2 |
| T3-032 | 6 | 6 | 0 | 0 | 0 |
| T3-048 | 5 | 5 | 0 | 0 | 0 |
| T3-100 | 3 | 3 | 0 | 0 | 0 |
| T3-064 | 3 | 3 | 0 | 0 | 0 |
| T3-015 | 3 | 0 | 0 | 0 | 3 |
| T3-022, T3-143, T3-097, T3-185, T3-016, T3-121, T3-126, T3-075 | 1 each | | | | |

The three sentences that failed most:
- **T3-017's discriminator** "Is it the room's running in-joke carried into the canvas talk or the day (T3-031)". Its "or the day" contradicts T3-031's own canvas condition.
- **T3-023's** "A change made to a whole sub for April Fools". It does not say whose sub, and its "or by a sub acting together" reaches a members' flood.
- **T3-001's** "Members of the room themselves post something false as true for April Fools". It leaves April Fools play that is not posted as true with no theme, and it catches a member relaying an outside joke.

## The named_neither rate

named_neither: 84 of 491 (17.1%). Most come from three sources:
- a second or third theme added by a scheme rule that neither reader applied, chiefly T3-097 on one concept and T3-095 or T3-032 at three;
- a theme in a family the readers did not open: T3-185, T3-126 and T3-157 from G02 items whose readers opened G01, and T3-069 or T3-090 beside T3-015;
- my own B1 theme kept against both readers.

The rate says the readers often stop at the first family that fits. It is also the measure of my pull toward my own reading, which no procedure removes. Of the 84, 29 are author-disagrees, where the theme is mine.

## The unresolved count

unresolved: 52 of 491 (10.6%). The next list names them by the reason the scheme did not decide.

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

## The boundary rulings

Each pair is one paragraph in `boundaries.md`; the paragraph's ruling is summarised here with its item list from packet 1.

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

## Agreement before and after

Before is the two readers against each other over packet 1's 491 items. After is each reader against the ruling over the 439 items not unresolved. Both use stage B2's definition: mean Jaccard on placement sets, with primary match beside it.

| | mean Jaccard | primary match |
|---|---|---|
| before (reader against reader) | 0.486 | 0.578 |
| after (each reader against the ruling) | 0.633 | 0.697 |

The figure after is not a reliability figure. It is agreement following an adjudication I performed, and it rises because the ruling usually keeps one reader's list.

## Whether stage B2's predictions held

Packet 1 holds only G01 and G02 items, so only four of `confusions.md`'s nineteen pairs could appear. Predicted pairs 3 (T3-001|T3-023: 20 items whose readers split their primaries), 15 (T3-001|T3-095: 11), 19 (T3-015|T3-063: 7) and 7 (T3-015|T3-075: 4) did split readers. Three pairs B2 did not predict split as often or more:
- T3-017|T3-031: 17;
- T3-001|T3-048: 13;
- T3-023|T3-095: 11.

The B2 pilot's own finding was that only T3-001|T3-023 among the predicted pairs split readers more than once. That pair is again the commonest split here. The other fifteen pairs belong to families in later packets, so whether they held is open until then.
