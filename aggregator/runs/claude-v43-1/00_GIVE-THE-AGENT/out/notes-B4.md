# Notes, stage B4: adjudication

Opened at B4a-01, 2026-10-12. The PI's leg message (21:19Z) carries J's rulings of 12 October: the contested inventory is `out/b3_classes.jsonl` from `tools/assemble.py`. Classes 1 and 2 stand; classes 3, 4 and 5 go to adjudication, with the gloss-only reads that section 1 keeps whatever the class. The blind sample at B4b adds a third reader per item from an OpenAI model, as a separate arm reported apart. Figures before any ruling come from `out/_analysis/b4_prepare.py` (`b4_prepare.json`).

## The gold drop (section 2)

- **Dropped.** All 755 seeded gold placements, told apart by (item, agent, replicate) on `batches-B3.jsonl`'s gold tags. All 755 gold lines in `assign_raw.jsonl` sit on those keys. The 1,210 duplicates' second copies are dropped as well; they are no corpus reading.
- **What `assign_final.jsonl` reads.** Only the corpus copies, as `b3_classes.jsonl` does: 15,688 lines, two per item. No line of `assign_final.jsonl` carries an agent or a replicate.
- **Count.** The drop removes placements, not themes. `assign_final.jsonl` holds one line for each of the 7,844 items, which is `counts.py`'s `assignment_items_expected`.
- **Fidelity on the gold placements** is stage B3's figure, read and not recomputed: 0.645 against the gold key, primary match 0.816 (`fidelity-B3.md`).

## The selection (section 1, J 2026-10-12)

The next table gives the classes from `b3_classes.jsonl`.

| class | rule | items | here |
|---|---|---|---|
| 1 | the two lists equal, order included, and equal to my B1 grouping | 2,566 | stands |
| 2 | the two lists equal and a proper subset of my B1 grouping; B1's other themes kept | 1,990 | stands, tagged `b1_grouping_kept` |
| 3 | the two lists differ, order included | 2,393 | ruled |
| 4 | the two lists equal and not inside my B1 grouping | 837 | ruled |
| 5 | no B1 grouping: the items I left in `unplaced-B1.jsonl` | 58 | ruled |

- **The gloss-only reads.** The 18 placements into a family neither reader opened all fall in class 3, so the contested inventory is 3,288 items.
- **Class 3.** 1,140 items share a primary and differ on an added theme or the order. 1,253 differ on the primary.
- **Class 4.** In 692 of 837 items the readers' list shares no theme with my B1 grouping.
- **Class 5.** In 42 of 58 items the two readers agree.

## The packets (sections 5 and 7)

I expect to rule on 3,288 items in seven packets of at most 500, one packet a leg. Packet 1 takes the 18 gloss-only items first. After that, every packet runs by the family of the first reading's primary, then by the pair of primaries. A family that does not fit runs on into the next packet.

The next table lists the packets.

| packet | items | families |
|---|---|---|
| 1 | 491 | the 18 gloss-only items; G01 313; G02 162 |
| 2 | 447 | G03 to G06 |
| 3 | 500 | G07; G08 (254) |
| 4 | 461 | G08 (6); G09 to G11 |
| 5 | 409 | G12 to G14 |
| 6 | 500 | G15 to G19; G20 (184) |
| 7 | 480 | G20 (52); G21 |

## The ruling policy, declared before the first item (section 5)

- **A reader's `confidence` and `why`.** Neither is a prior. A "clear" reading against an "arguable" one counts for nothing in the ruling. A reader's `why` points at material, and I check what it points at against the item's concepts. The ruling rests on the concepts read against the scheme's `must_show`, `must_not_show`, `decide_when_both` and discriminators.
- **My B1 grouping is shown as the third placement.** This is J's three-placement design. It is labelled as mine, and I weigh it like a reading, not as a prior.
- **A theme neither reader chose.** A ruling may name one, logged loudly: `named_neither` true, and the `why` says what both readers missed that the file does say. From item 401 of packet 4 this is replaced by J's rulings of 13 October: a ruling chooses among the readers' placements and my B1 grouping and adds no theme beyond them (see "Packet 4" below).
- **When the scheme does not decide.** The ruling is empty and `unresolved` true. The quote is the sentence of the scheme that failed to decide. The item is carried, not resolved by preference.
- **Boundaries ruled once.** Where five or more items of a packet split their primaries on one sibling pair, I rule the boundary once. It gets one paragraph in `adjudication_report.md`, quoting the discriminator, logged as one ruling with its item list. It is then applied to each item, and each item carries `boundary_ruling`.
- **The taxonomy by class.**
  - Class 3: by the readers' split, with the five values of section 7.
  - Class 4: the readers agree outside my B1 grouping. If the ruling takes the readers' list, the error was mine at B1: `author-error`. If it keeps a B1 theme both readers left out, it overrules them: `author-disagrees`. `item-is-a-bag` or `genuine-joint` apply where the material says so.
  - Class 5: I left the item unplaced at B1. If the readers' placement holds, my leaving it out was wrong: `author-error`. If the item holds no doing to place, the ruling is empty and `unresolved` true, with `author-disagrees` where both readers agreed. A split is ruled by the split.
- **`reader-error` is suspected last.** It is never given where both readers made the same miss.
- **Concepts behind each theme placed.** `support_by_theme` is taken from the reader line that placed the theme: its `support`, or its multiplacement record's `support_additional` for an added theme. Each is checked against the item. Where neither reader placed a theme, I name the concepts. A bag keeps its unplaced themes under `also_present`, each with its concepts.
- **The quote.** It is the deciding participant's words, a substring of the concept's text in the store, which is the rule `cite.py` resolves. A `scheme-ambiguous` ruling quotes the scheme sentence of the field that failed instead. No ruling cites a room note.

## Blindness (section 6)

No v38 tool strips the packets, so a script does it: `out/_analysis/b4_adjudication_packets.py`.
- **Stripped:** agent, batch, replicate, position and timestamps, and the dispatch's reader id.
- **The two readings** are shown as reading A and reading B, in an order seeded by 20261016 per item, so the replicate cannot be read off the order. Each keeps its set, `confidence`, `why`, `read`, `families_opened`, `bag` and `also_present`.
- **The item's material** is rendered from the store as `mem.py theme` gives it: the label, the coder's `theme_note`, and each concept with its id, label and the participant's words. The member name, hour and thread columns are dropped; no ruling needs them.

## The conflicts pass (section 4), declared

The pass runs over the coders' `theme_note` alone, with no concepts beneath it, across rooms. It runs packet by packet: before a packet's first ruling, I read that packet's notes grouped by the readings' primaries. `coder_conflicts.jsonl` grows with each packet and is whole when the last packet is ruled. Why packet by packet: a single pass over all 3,288 contested notes before any ruling would fill a leg on its own, and a conflict is wanted beside the disagreements it explains.

## `assign_final.jsonl` while the packets run

It is rewritten at every adjudication leg by `out/_analysis/b4_assign_final.py` and holds every item of the analysed set:
- **Classes 1 and 2:** `b3_classes.jsonl`'s placement, with class 2 tagged `source: "b1_grouping_kept"`.
- **A ruled item:** the ruling.
- **A contested item not yet ruled:** `third_order` empty and `status: "pending_adjudication"`, with the readers' confidence, so no line claims a placement before its ruling.

## Packet 1, ruled at B4a-01 (2026-10-12)

All 491 items are ruled, in 20 blind chunks of 25 (`out/_adjudication-B4/packet-01/rulings-NN.jsonl`, appended by `out/_analysis/b4_rule_append.py`). `out/_adjudication-B4/packet-01/summary.md` holds the figures, and `adjudication_report.md` holds them as the interim report after packet 1 of 7. In brief:
- **Taxonomy:** genuine-joint 137, scheme-ambiguous 123, author-error 97, reader-error 77, author-disagrees 37, item-is-a-bag 20.
- **Counts:** unresolved 52 (10.6%); named_neither 84 (17.1%).
- **Fields that failed:** must_show 78, discriminators 39, decide_when_both 4, must_not_show 2.
- **Themes that failed most:** T3-017 29, T3-023 27, T3-001 24.
- **Agreement:** before, reader against reader, 0.486 mean Jaccard; after, each reader against the ruling, 0.633. The figure after is not a reliability figure.
- **Mapping:** `assign_final.jsonl` was rewritten (class 1 2,566, class 2 1,990, ruled 491, pending 2,797).

What changed during the packet, and why:
- **Two rulings corrected in place.** formula1 t05 and elitedangerous t01 had used T3-063 for removals of posts that are not canvas posts, and T3-063's `must_show` begins "Canvas posts handled under the sub's standing rules". `b4_rule_append.py` gained a `--replace` mode. It rewrites the named items in place, marks each line `revised` with the UTC time, and keeps the old file as `disagreements.superseded-20261012T221214Z.jsonl`.
- **Three gaps ruled the same way each time,** written into `boundaries.md`:
  - April Fools play not posted as true (unresolved on T3-001's `must_show`);
  - another sub's April Fools change (unresolved on T3-023's `must_show`);
  - moderators applying standing rules to non-canvas posts (unresolved on T3-063's `must_show`, conflict CC-004).
- **Paragraphs added to `boundaries.md`.** The T3-032|T3-097 paragraph was extended for the overlap of "stop them or take them down" with "requests to switch back". Seven pairs met on fewer than five items gained short paragraphs.
- **A practice to declare for the later packets: a second theme on one concept.** It is added where a scheme rule says "a concept of its own": T3-023's rule for T3-097 and T3-100, and T3-017's three-concept rule. Elsewhere a second theme on one or two concepts was added only where the concept plainly passes another theme's gate. Where it was not added, the concept is named in the ruling's why. Single-concept additions were not perfectly even across the packet (magictcg t09's megathread concept was left out); the report says so.
- **The reader-error count.** Of 77, 16 fell in chunk 18, single-concept G02 items. Two there were changed to scheme-ambiguous before writing (tagpro t15, twitch t04), because the readers had matched a test's literal words and that test does not state its canvas condition.
- **Class 4.** I took the readers' list in 89 items and kept a B1 theme in 29. My commonest B1 errors are listed in the report.

The next packet is packet 2: 447 items, G03 to G06, chunks built in `out/_adjudication-B4/packet-02/`. The conflicts pass runs over its notes before its first ruling, as declared.

`validate.py B4`, after packet 1:

```
stage B4:
  leg: adjudication
  settled items 7844 = assignment_items_expected
  rulings 491: {'genuine-joint': 137, 'scheme-ambiguous': 123, 'reader-error': 77, 'author-error': 97, 'author-disagrees': 37, 'item-is-a-bag': 20}
  classes 1: 2566, 2: 1990, 3: 2393, 4: 837, 5: 58; contested (3, 4, 5) 3288, ruled 491, outstanding 2797
  coder conflicts 8

warn   RETURN-B4.md is not yet written; the build leg owes it, and this leg was read as an adjudication leg because neither RETURN-B4.md, a stage-B4 manifest entry nor _packets-B4/ exists

0 errors (0 distinct shapes), 1 warnings
```

## Packet 2, ruled at B4a-02 (2026-10-12 to 13)

Before the first item:
- **The conflicts pass** read packet 2's notes alone, grouped by the readings' primaries, and added CC-009 to CC-016 to `coder_conflicts.jsonl` (16 lines now).
- **Seven boundaries were ruled once** in `boundaries.md` ("Packet 2"): every pair on which five or more items split their primaries (`out/_analysis/b4_packet_pairs.py`). Four are T3-002 against a sibling, so each paragraph says how a concept is counted toward one act or the other.

All 447 items are ruled, in 18 blind chunks of 25 (`out/_adjudication-B4/packet-02/rulings-NN.jsonl`). `packet-02/summary.md` holds the figures, and `adjudication_report.md` holds them with packet 1's as the interim report. In brief:
- **Taxonomy:** genuine-joint 215, author-disagrees 65, scheme-ambiguous 62, author-error 58, item-is-a-bag 44, reader-error 3.
- **Counts:** unresolved 10 (2.2%); named_neither 155 (34.7%), of which 98 add only themes from my B1 grouping.
- **Fields that failed:** must_show 33, discriminators 17, must_not_show 6, decide_when_both 6.
- **Themes that failed most:** T3-002 12, T3-033 9, T3-014 6.
- **Agreement:** before, reader against reader, 0.537 mean Jaccard; after, each reader against the ruling, 0.603. The figure after is not a reliability figure.
- **Mapping:** `assign_final.jsonl` was rewritten (class 1 2,566, class 2 1,990, ruled 938, pending 2,350).

What changed during the packet, and why:
- **The T3-016 correction (at item 146).** The T3-002|T3-070 paragraph had said that teaching a newcomer to place counts as directions. T3-016's `must_show` names "how to pick a colour and place". The paragraph now reads that such teaching is not a call, and is T3-016 when it explains the event. bindingofisaac t02 was revised by `--replace` (`revisions-01.jsonl`).
- **The T3-033 and T3-041 reading (from item 140).** T3-041's `must_not_show` gives "The room's first mark proposed" to T3-033. Proposals of a further piece beside a standing mark are T3-041, scheme-ambiguous on T3-033's `must_show`. clashroyale t02, ruled before the reading, was revised (`revisions-02.jsonl`). I checked the T3-033 concepts of the 22 other packet 2 rulings that place T3-033 with `out/_analysis/b4_theme_support_lines.py`; each proposes a first mark.
- **Class 4 went the other way.** In packet 1 I took the readers' list in 89 class 4 items and kept a B1 theme in 29. In packet 2 the figures are 53 and 63. Of packet 2's 65 author-disagrees, 39 keep the readers' theme and add mine under rule 0. The report says I cannot separate this from my pull toward my own grouping.
- **A batching slip, twice.** I put an Edit and the dry run that depends on it in one turn (revisions-01 and the chunk 12 fix). Both ran in order. I kept them apart from then on.

Readings applied in packet 2, to carry into the later packets (each from the theme's own sentences):
- **The counting rule for T3-002, T3-033 and T3-038.** Calls, volunteers and answers ("I'm in", "on it") count toward T3-002; placing and reports of the work's state, with coordinates of the work in progress, toward T3-038; a new mark named, even with a call for help, toward T3-033.
- **T3-065** takes the flag of the room's land, its calls and its proportions included (T3-002's `must_not_show`). **T3-169** takes the sub's name written; **T3-044** instead when bringing visitors in is the stated point.
- **T3-084** takes a request received from another room and another canvas group asked as a group; **T3-062** takes calls posted to other communities. "Canvas group" is undefined: scheme-ambiguous.
- **T3-074** needs the limit, the cooldown or a placing trouble while building. A member's exams, papers or sleep are not in its test (pakistan t10 scheme-ambiguous; rutgers t13 author-disagrees). With nothing built yet, doubt about the hands goes to **T3-136**, and a design scaled down to the hands to **T3-069**.
- **Smaller readings:**
  - T3-137 for following an outside sub's plan; T3-068 for another room's mark altered into the room's sign or joke;
  - T3-170 for friendly work mistaken for vandalism; T3-196 for former fans returning; T3-122 for greetings to or from neighbours;
  - T3-118 needs a loss; T3-125 for "we just wing it"; T3-141 for night shifts; T3-162 for vetting others' requests to build;
  - T3-116 for plans hidden from rivals; T3-111 for a canvas sub's future.

National, political and hate content is named in the whys as the words give it. Examples: "schleus de merde", an anti-German slur, in france t05; "until we reach the jews" in russia t04; the anarcho-capitalist and anarcho-communist flags in anarcho_capitalism t06; "Norwegian commie bastards" in texas t10.

The next packet is packet 3: 500 items, G07 and the first 254 of G08. Its conflicts pass runs over its notes before its first ruling.

`validate.py B4`, after packet 2:

```
stage B4:
  leg: adjudication
  settled items 7844 = assignment_items_expected
  rulings 938: {'genuine-joint': 352, 'scheme-ambiguous': 185, 'reader-error': 80, 'author-error': 155, 'author-disagrees': 102, 'item-is-a-bag': 64}
  classes 1: 2566, 2: 1990, 3: 2393, 4: 837, 5: 58; contested (3, 4, 5) 3288, ruled 938, outstanding 2350
  coder conflicts 16

warn   RETURN-B4.md is not yet written; the build leg owes it, and this leg was read as an adjudication leg because neither RETURN-B4.md, a stage-B4 manifest entry nor _packets-B4/ exists

0 errors (0 distinct shapes), 1 warnings
```

## Packet 3, ruled at B4a-03 (2026-10-13)

Before the first item:
- **The conflicts pass** read packet 3's notes alone and added CC-017 to CC-025 to `coder_conflicts.jsonl` (25 lines now).
- **Nine boundaries were ruled once** in `boundaries.md` ("Packet 3"): every new pair on which five or more items split their primaries. Three pairs from packet 2 carry over as written: T3-002|T3-033, T3-002|T3-038 and T3-004|T3-070.

All 500 items are ruled, in 20 blind chunks of 25 (`out/_adjudication-B4/packet-03/rulings-NN.jsonl`). `packet-03/summary.md` holds the figures, and `adjudication_report.md` holds them with packets 1 and 2 as the interim report. In brief:
- **Taxonomy:** genuine-joint 231, scheme-ambiguous 106, item-is-a-bag 76, author-error 45, author-disagrees 39, reader-error 3.
- **Counts:** unresolved 7 (1.4%); named_neither 280 (56.0%), of which 123 add only themes from my B1 grouping and 157 add a theme no placement held (`out/_analysis/b4_named_neither_split.py`).
- **Fields that failed:** must_show 54, must_not_show 26, discriminators 23, decide_when_both 3. 24 of the 26 `must_not_show` failures are the homeland flag or its emblems.
- **Themes that failed most:** T3-004 25, T3-033 25, T3-038 11.
- **Agreement:** before, reader against reader, 0.475 mean Jaccard and 0.598 primary match; after, each reader against the ruling, 0.473 and 0.535. The figure after fell below the figure before, the first packet where it did. It is not a reliability figure.
- **Mapping:** `assign_final.jsonl` was rewritten (class 1 2,566, class 2 1,990, ruled 1,438, pending 1,850).

What changed during the packet, and why:
- **Three readings,** each written in `boundaries.md` where it was first met: the homeland flag's look (from item 16), a design cut down to the hands (from item 12) and a celebration while placement goes on (from item 280). catalonia t07 and packet 2's sadboys t03 were revised to match. The chunk 12 draft first read T3-009 against T3-026 by their `must_not_show` timing; T3-026's `decide_when_both` already decides the pair, so six draft lines were changed before the write.
- **T3-170 for members' own misclicks (from item 430).** Its `must_show` names "members' own misclicks or misplaced pixels owned and forgiven". bisexual t04 and kpop t05 were revised to place it (`revisions-02.jsonl`).
- **The append tool's support convention.** `b4_rule_append.py` (lines 131 to 145) lets the primary give up the concepts it shares with added themes where it keeps others. It does not resolve overlaps among added themes, and it refuses a placed theme only when its list equals another's. The new read-only check `out/_analysis/b4_own_support_check.py [--leg B4a-03]` lists placed themes whose concepts all sit under the ruling's other themes. It found seven (ManningPlace t05, KState t04, rainbowgrid t01, dofus t01, skyrim t03 and teamcube t04, and packet 1's nerf t08). All were rewritten by `--replace` (`packet-03/revisions-03.jsonl`, `packet-01/revisions-01.jsonl`). The check finds none over the three packets, and I ran it after every later chunk.
- **Boundary tags.** Eleven packet 3 rulings applied packet 2's counting rule but carried no `boundary_ruling`. The tags were added with the rulings unchanged (`revisions-04.jsonl`, built by the new `out/_analysis/b4_br_tag_draft.py`); a row comparison against the superseded ledger shows only the tag, the `revised` stamp and the why changed.
- **A log correction.** The chunk 13 line said the readers' list was taken in "11 of 17" class 4 items. The chunk holds 16 class 4 and 3 class 5 items, and a correction line says 11 of 19.
- **QB4-001 asked.** Two sources lowered agreement. In 76 items both readers put T3-038 first, and my rulings kept it first in 27. 201 of 500 rulings place three themes, often with a one- or two-concept theme no placement held. I asked J whether packets 4 to 7 should keep adding such themes. Meanwhile packets 4 to 7 are ruled as packets 1 to 3 were.

Readings applied in packet 3, to carry into the later packets:
- **The homeland flag.** The flag of the room's land, its build, size, expansion, proportions, spot, repair and calls for hands, is T3-065. Emblems in or beside it are T3-113. A reader's T3-004, T3-020 or T3-041 on that work is scheme-ambiguous on that theme's `must_not_show`.
- **Borders and help.** A border with no protection stated is T3-004, scheme-ambiguous on T3-055's `must_show`. "Defend" with no attacker named is T3-002. Refresh advice is T3-070. Requests received are T3-084. Permission asked of a host is T3-035, and the host's grant T3-012. Relying on a bigger room's protection is T3-099.
- **Smaller readings:**
  - T3-170 for members' own misclicks owned and forgiven; T3-171 for a colour or pattern faction spreading (EraseThePlace, the ss13 greytide);
  - T3-068 for converting another's mark; T3-061 for taking a neighbour's space; T3-081 for "Campaña al desierto"; T3-130 for national politics (Brexit, imam hatip, Hayır, "Zuma Must Fall");
  - a known mark located for a member is T3-026; a mark the room did not know of is T3-082 (CC-021);
  - "I added a little something for my bias", T3-092's own example, goes to T3-060 by T3-092's discriminator (bangtan t10, scheme-ambiguous).
- **Rule 0 as applied.** At most three placements. Order by concept count; ties go by how many of the three placements (reader A, reader B, my B1) hold the theme. A one- or two-concept theme is added when it passes its gate; where several tie with no placement ahead, none is added. Each placed theme has a concept of its own.

National, political, hate, sexual and drug content is named in the whys as the words give it. Examples: "LULA PRESO AMANHÃ" in brasil t02 and "LULA PRESO AMANHA" in brasil t04; "some fake nigga kept replacing my work" in drugs t01; Hitler moustaches kept off Kekkonen in suomi t07; a Menorah "less prone to being plastered by swastikas" in israel t01; "Thin Blue Line" in AmericanFlaginPlace t10; "based Pinochet snek" in physical_removal t02; "dirty limies" in detroitredwings t03; "yiff me daddy /r/furry" in furry t01.

The next packet is packet 4: 461 items, the last 6 of G08 and G09 to G11. Its conflicts pass runs over its notes before its first ruling.

`validate.py B4`, after packet 3:

```
stage B4:
  leg: adjudication
  settled items 7844 = assignment_items_expected
  rulings 1438: {'genuine-joint': 583, 'scheme-ambiguous': 291, 'reader-error': 83, 'author-error': 200, 'author-disagrees': 141, 'item-is-a-bag': 140}
  classes 1: 2566, 2: 1990, 3: 2393, 4: 837, 5: 58; contested (3, 4, 5) 3288, ruled 1438, outstanding 1850
  coder conflicts 25

warn   RETURN-B4.md is not yet written; the build leg owes it, and this leg was read as an adjudication leg because neither RETURN-B4.md, a stage-B4 manifest entry nor _packets-B4/ exists

0 errors (0 distinct shapes), 1 warnings
```

## Packet 4, ruled at B4a-04 (2026-10-13)

Before the first item:
- **The conflicts pass** read packet 4's notes alone and added CC-026 to CC-036 to `coder_conflicts.jsonl` (36 lines now).
- **Four boundaries were ruled once** in `boundaries.md` ("Packet 4"): T3-005|T3-021 (B2's predicted pair 1), T3-021|T3-038, T3-005|T3-038 and T3-005|T3-073.

All 461 items are ruled, in 19 blind chunks (`out/_adjudication-B4/packet-04/rulings-NN.jsonl`). `packet-04/summary.md` holds the figures, and `adjudication_report.md` holds them with packets 1 to 3 as the interim report. In brief:
- **Taxonomy:** genuine-joint 219, scheme-ambiguous 84, author-error 75, item-is-a-bag 53, author-disagrees 17, reader-error 13.
- **Counts:** unresolved 10 (2.2%); named_neither 222 (48.2%), of which 89 add only themes from my B1 grouping and 133 add a theme no placement held, all 133 in items 1 to 400.
- **Fields that failed:** must_show 39, must_not_show 32, decide_when_both 11, discriminators 2. 20 of the 32 `must_not_show` failures are the homeland flag's repair on T3-021's `must_not_show`.
- **Themes that failed most:** T3-021 24, T3-005 10, T3-073 9, T3-027 7.
- **Agreement:** before, reader against reader, 0.519 mean Jaccard and 0.675 primary match; after, each reader against the ruling, 0.562 and 0.671. Not a reliability figure.
- **Mapping:** `assign_final.jsonl` was rewritten (class 1 2,566, class 2 1,990, ruled 1,899, pending 1,389).

What changed during the packet, and why:
- **QB4-001 answered, and the ruling rule changed at item 401.** J (06:43 Berlin): "Ask it to stop. The point is to try to adjudicate." J's rulings (06:47 Berlin), for the rest of packet 4: a ruling chooses among the readers' placements and my B1 grouping and adds no theme beyond them; it takes the union of placements only when it names, for each theme it keeps, the separate concept that carries it; otherwise it chooses. Chunk 17 had been read under the old practice; it was re-decided under the new rule before any line was written. Items 1 to 400 of packet 4, and packets 1 to 3, are re-ruled at the start of B4a-05, not now.
- **What the new rule did.** `out/_analysis/b4_agreement_range.py` (new, read-only) splits packet 4. Items 1 to 400: before 0.512 and 0.652, after 0.536 and 0.638, three themes placed in 179, a theme no placement held in 133. Items 401 to 461: before 0.566 and 0.820, after 0.726 and 0.883, three themes placed in 22, none beyond the placements. The two parts hold different families (G08 to G10 against G11), so the rise is not the rule's effect alone.
- **Rule 0 under the new rule.** Concepts count only toward placed themes; a concept whose act no placement holds is named in the why and left out of `support_by_theme`. Order by concept count, ties by how many of the three placements hold the theme. A one- or two-concept theme that a placement holds is kept when its concept passes the theme's gate and it leads its level on placements; where placed themes tie at a level, none is kept. A bag still names its other themes under `also_present`, which places nothing; bakchodi t09 lists T3-006, which no reading named.
- **Seven boundaries in packet 4's own families.** Beside the four ruled first: T3-020|T3-022 (from item 189; CC-033), and from item 401 T3-027|T3-028, T3-027|T3-087 and T3-089|T3-168. Two readings: the homeland flag kept and defended (from item 15) and a call to fight against a call to defend (from item 16).
- **One correction.** MonkeyIsland t03, ruled unresolved in chunk 6 on a full T3-005|T3-021 tie, was revised to place both themes, as the T3-005|T3-021 paragraph rules for a full tie (`packet-04/revisions-01.jsonl`).
- **Slips.** In chunk 5 a draft's write and its dry run went in one turn. They ran in order, and the later chunks kept them apart. After the compaction in chunk 16, the chunk 16 draft was written before the head was re-read and the reconciliation line logged. I then read the head and stage file, logged the line, checked the draft against the chunk file and fixed three whys before its dry run.

Readings applied in packet 4, to carry into the later packets:
- **The homeland flag** kept and defended: repair, calls for hands and its spot are T3-065; an attack on it, fought or raised as an alarm, T3-005; watching it T3-021; night watch T3-141.
- **Fights and calls.** A call to fight is T3-005; a call to defend or protect with no attack in the words is T3-002. A report with a call is T3-005; a report without one is T3-073.
- **Culprits.** Members doubting a damage was the room's own are tracing it (T3-087); a bare denial pointing at another room is T3-087 by T3-188's `must_not_show`; an organised room setting its plan apart from rogue placers is T3-188; friendly work taken for an attack is T3-170. A loss blamed after the close is T3-058.
- **Scripts.** Scripts made, shared, fixed or run for the room's work are T3-028; scripts to wreck another room's work are not. Arguing their fairness is T3-027; the larger part leads. Glitches used to place more, and extra accounts with concepts of their own, are T3-088. Accounts handed to someone else's bot are T3-120. A script changed to spare a neighbour is T3-168; the room's own versions fighting its plan are T3-089.

National, political, hate and slur content is named in the whys as the words give it. Examples: "pokatoličeni Srbi", a slur for Croats, in serbia t08; "od srba i ostale gamadi", Serbs called vermin, in bih t02; "Too many Pajeets", a slur for Indians, in 4chan t08; "porkies" and "randian" in bakchodi t06 and t11; "Indians , being the cheats they are" and "Saffron terrorists" in pakistan t08; "changed it to fags", a homophobic slur on the Leafs logo, in sabres t09; "Shadilay my brothers. Kek wills it!" in pepe t04; Richard Spencer and /pol/ in completeanarchy t12.

The next packet is packet 5: 409 items, G12 to G14. B4a-05 opens by re-ruling packets 1 to 3 and items 1 to 400 of packet 4 under J's rulings, as J directs.

`validate.py B4`, after packet 4:

```
stage B4:
  leg: adjudication
  settled items 7844 = assignment_items_expected
  rulings 1899: {'genuine-joint': 802, 'scheme-ambiguous': 375, 'reader-error': 96, 'author-error': 275, 'author-disagrees': 158, 'item-is-a-bag': 193}
  classes 1: 2566, 2: 1990, 3: 2393, 4: 837, 5: 58; contested (3, 4, 5) 3288, ruled 1899, outstanding 1389
  coder conflicts 36

warn   RETURN-B4.md is not yet written; the build leg owes it, and this leg was read as an adjudication leg because neither RETURN-B4.md, a stage-B4 manifest entry nor _packets-B4/ exists

0 errors (0 distinct shapes), 1 warnings
```

## The re-ruling of packets 1 to 4, at B4a-05 (2026-10-13)

The PI's message for B4a-05 carried J's rulings (06:45 and 06:47 Berlin): (1) the placements are the readers' and mine (B1), and a ruling chooses among them and adds no theme beyond them; (2) a ruling takes the union only when it names, for each theme it keeps, the separate concept that carries it, otherwise it chooses; (3) re-rule only the items in packets 1 to 4 whose ruling holds a theme no placement held, under (1) and (2), keep the superseded ledger, and do (3) before packet 5. QB4-001's answer was read with `mem.py asks` before the first write.

What was done:
- **The work list.** `out/_analysis/b4_rerule_list.py` (new, read-only) lists the rulings that hold a theme no placement held, with both readings blinded as A and B, my B1 grouping, the old ruling and each removed theme's concepts. Packet 1 30, packet 2 58, packet 3 157, packet 4 133: 378. Every other ruled line already named a concept of its own per placed theme, so rule (2) reached no other line.
- **The decisions.** One line per item in `out/_adjudication-B4/rerule-B4a-05/decisions-NN.jsonl`; `out/_analysis/b4_rerule_draft.py` (new) builds a draft from them and refuses a ruling theme no placement holds; `b4_rule_append.py --replace` wrote each draft after its dry run in a turn of its own. Thirteen parts: packet 1 one, packet 2 one, packet 3 four, packet 4 seven. Each kept the old ledger as `disagreements.superseded-<time>.jsonl`. `b4_own_support_check.py` found no theme without a concept of its own after any part. `b4_rerule_list.py` returns nothing for all four packets.
- **The method** is in the diary entry that opened the leg and in `adjudication_report.md`: a removed theme's concepts count toward a placed theme whose `must_show` takes them; rule 0 then runs inside the placements, so a placed theme the old limit of three cut may enter; unresolved where no placement's test takes the material.

What it changed:
- **Taxonomy over the four packets:** genuine-joint 825 (was 802), scheme-ambiguous 336 (375), author-error 292 (275), item-is-a-bag 186 (193), author-disagrees 162 (158), reader-error 98 (96). Unresolved 82 (79): weezer t13, nbaspurs t17 and rainbowgrid t06 were added, where no placement's test takes the material.
- **named_neither** fell from 741 to 484. Every one now keeps a theme from my B1 grouping; none holds a theme no placement held.
- **Agreement after,** each reader against the ruling: 0.627 mean Jaccard and 0.698 primary match over the four packets (was 0.565 and 0.649). Packet 3 rose from 0.473 to 0.581. Not a reliability figure.
- **Readings replaced.** The homeland-flag reading and the call-to-defend reading of packet 4, packet 2's T3-002|T3-005 paragraph and packet 3's T3-033|T3-041 paragraph now send a concept to their theme only where a placement holds it. Where none does, calls to defend count toward T3-005, the flag's repair toward T3-021, its look and spot toward the readers' T3-004 or T3-020, and a further piece toward the readers' T3-033, T3-038 or T3-004.
- **Four earlier corrections undone:** catalonia t07, sadboys t03, bisexual t04 and kpop t05 had been corrected to a theme no placement held.
- **Bags.** Several bags placed a theme no placement held; they were re-placed among the placements, and some stopped being bags (adventuretime t04, suomi t07, archlinux t04, israel t02, loliconsunite t02, placeDE t03).

What I doubt:
- **Rule 0 inside the placements keeps more of my B1 than a choice would.** A one- or two-concept B1 theme that leads its level is kept as a third theme. 89 of packet 4's 137 named_neither rulings place three themes. Rule (2) permits that union, since each kept theme has its own concept; it does not require it. I applied the rule declared at item 401 so that all four packets are ruled one way. If J reads "otherwise it chooses" as asking for fewer unions, the rule to change is the one-concept keep.
- **Two labels do not match the rulings.** 12 author-error rulings from packet 4's items 401 to 461 keep a B1 theme (by §7 author-disagrees), and 2 packet 2 author-disagrees rulings take the readers' list. Rule (3) does not reach them, so they stand and the report gives both counts.
- **Where both must_show lines take a concept,** I followed the reading that placed it, or the more specific test (a swastika alarm to T3-146, '24-7 supervision' to T3-141 by T3-021's `must_not_show`). These choices decide whether a one-concept theme survives.

Slips: two Edit calls on `adjudication_report.md` ran in one turn; both applied, and the later edits went one at a time.

National, political, hate and slur content named in the re-ruled whys as the words give it, for example: "pokatoličenim Srbima" (Catholicised Serbs, a slur for Croats) and the tricolour that vandals tried to make "Bulgarian or Arab" in serbia t08; "porkies" for Pakistanis and "Randia" for India in bakchodi t06; the swastika on the Pakistani flag and "To Bakchodi fuckers" in pakistan t05; the black Nazi symbol in the menorah in israel t02; "TheDonald users and KotakuInAction" miscolouring the trans flag in traaaaaaannnnnnnnnns t02; "franchutes" for the French in spain t09; the Moors and the Empire in PORTUGALCARALHO t02.

## J's ruling on also_present, and the correction, at B4a-05 (2026-10-13)

The PI's message at 07:09 UTC carried J's ruling of 09:09 Berlin on bakchodi t09: rule (1) extends to `also_present`, which lists only themes that a reader or my B1 named; apply it to the rulings written from now on and to the ledger's existing entries, keeping the superseded ledger. I asked J whether a theme a reader listed under its own `also_present` counts as named (QB4-002). J's answer (09:20 Berlin): yes; `also_present` may list themes a reader placed, a reader listed under its own `also_present`, or my B1 named, nothing else; restore any entries the interim reading removed that this admits.

What was done:
- **The scan.** `out/_analysis/b4_ap_scan.py` (new, read-only; `--reading placed|named`, `--ledger`) found 128 lines in packets 1 to 4 (5, 32, 46, 45) listing 273 themes outside the named set. Dropped most: T3-002 29, T3-004 17, T3-041 16, T3-170 14, T3-073 14, T3-065 9, T3-070 8. 84 lines keep a theme only a reader's own `also_present` named, which QB4-002 admits.
- **The correction.** Four `--replace` parts from `out/_adjudication-B4/rerule-ap-B4a-05/draft-apNN-named.jsonl`; old ledgers `disagreements.superseded-20261013T072151Z.jsonl`, `-072154Z`, `-072158Z`, `-072202Z`. `b4_rerule_draft.py` now takes several decision files. `out/_analysis/b4_ap_emptied_show.py` (new, read-only) printed the four bags left with no theme at the floor; each was re-ruled by hand: archlinux t01 (genuine-joint), ireland t04 and starvstheforcesofevil t02 (author-disagrees), de t02 (author-error).
- **The interim reading** (placed themes only) ran as a dry run and removed nothing from the ledger, so nothing had to be restored.
- **From packet 5 on,** `also_present` lists only placed themes, and a bag needs four placed themes with three concepts each.

## Packet 5, ruled at B4a-05 (2026-10-13)

Before the first item:
- **The conflicts pass** read packet 5's notes alone and added CC-037 to CC-048 to `coder_conflicts.jsonl` (48 lines now).
- **Five boundaries were ruled once** in `boundaries.md` ("Packet 5"): T3-010|T3-024, T3-010|T3-149, T3-006|T3-061, T3-010|T3-011 and T3-010|T3-151, each applied under J's rulings.

All 409 items are ruled, in 17 blind chunks (`out/_adjudication-B4/packet-05/rulings-NN.jsonl`). `packet-05/summary.md` holds the figures, and `adjudication_report.md` holds them with packets 1 to 4 as the interim report. In brief:
- **Taxonomy:** genuine-joint 291, author-disagrees 44, author-error 41, reader-error 16, scheme-ambiguous 14, item-is-a-bag 3.
- **Counts:** unresolved 3 (linux t03, survivor t26, PurplePixels t13); named_neither 131 (32.0%), every one from my B1 alone, none beyond the placements.
- **Fields that failed:** must_show 2, must_not_show 8, decide_when_both 0, discriminators 4. The one sentence that failed more than once is T3-006's discriminator against T3-061 (4).
- **Agreement:** before 0.467 mean Jaccard and 0.623 primary match; after 0.612 and 0.677. Not a reliability figure.
- **Class 4:** the readers' list taken in 42, a B1 theme kept in 44.
- **Boundary tags:** T3-010|T3-149 34, T3-010|T3-151 31, T3-010|T3-024 26, T3-006|T3-061 18, T3-010|T3-011 14. Chunks 6 and 7 and item 409 were tagged after the packet (nine `--replace` lines; old ledger `disagreements.superseded-20261013T081847Z.jsonl`).
- **Mapping:** `assign_final.jsonl` rewritten (class 1 2,566, class 2 1,990, ruled 2,308, pending 980). The summaries of packets 1 to 4 were rerun after the `also_present` correction.

Readings applied in packet 5, to carry into the later packets:
- **Fights and deals.** T3-010's "with no fight to end" fails for a concept naming a fight, a threat, peace or a truce, even where no placement holds T3-149. A shift agreed with no request in the words is T3-010; a move because a neighbour asked is T3-039 where placed.
- **Help.** A request for help is T3-084 by T3-011's `must_not_show`. Help counts toward T3-151 only when the return is named. T3-150's `decide_when_both` keeps help traded inside an alliance when defence or a fight is the frame. A member whose effort moves to another room's build is T3-137.
- **Space.** A request for space to the room that holds it is T3-035; a host ruling on many requests T3-162; a single grant T3-012; a warning that a faction covers unapproved art T3-094.
- **Neighbours.** T3-079 needs national flags; T3-149 rooms already in contact; T3-078 kin felt in the words; T3-099 the bigger room's protection and its size in the words; T3-071 adoption into a neighbour's work; T3-170 friendly work taken for vandalism.
- **Rule 0 at the top.** Where the top of the order ties on concepts and placements, all the tied themes are placed (Clannad t05, Fez t06, Dustforce t08, aceattorney t10, androidgaming t06). Themes of three concepts or more tied on placements at the limit of three are left out together.

What I doubt:
- **My B1 kept against both readers.** Rule 0 inside the placements keeps a one- or two-concept B1 theme alone at its level. In class 4 that turned the ruling toward my B1 in 44 of 86 items, 7 of 7 in chunk 7 and 8 of 9 in chunk 14. 89 of the 131 named_neither rulings place three themes. If J reads "otherwise it chooses" as asking for fewer unions, the rule to change is the one-concept keep.
- **Requests for room inside a host's work.** The T3-010|T3-024 paragraph counts "a request for room" toward T3-010. In theitalyplace t11 I left the requests for room inside Italy's flag out as T3-035's act, which no placement held, and counted only requests between neighbouring works toward T3-010. Counted the other way, T3-010 leads that item; the ruling's set is the same.
- **Where both must_show lines take one concept,** the choice can decide the item: england t05 ('No' with a flood complaint), falcons t15 ('Nope ... or you get nothing'). I counted a reply that answers a request toward T3-115 both times.

Slips:
- After the first compaction of the leg, `rulings-06.jsonl` was written before the head was re-read and the reconciliation line logged. I then logged the line and re-checked the draft (item 138).
- Three Edit calls on `b4_ap_scan.py` ran in one turn. All applied; later edits went one at a time.
- One diary line said I had asked J before `mem.py ask` ran; the ask followed at once.
- One diary line gave the dropped-theme counts from the placed reading; a later line corrected them from the superseded ledger.
- The chunk 14 dry run refused c0185 on hawks t06 (a concept of another theme); it was removed before the write.
- After the last compaction, chunk 16 was read before the head; the reconciliation line was logged before any write.

National, political, hate and slur content named in packet 5's whys as the words give it, for example: 'BURN THE DISGUSTING ANCRAP RAG!', the hammer and sickle and 'Yellow Hordes of Ancapistan' (TheFarLeftSide t05); a white-supremacist parody about purging 'the inferior colored people' (ssbpm t17); 'remove the Russian scourge' and 'generalgovernment' (czech t07); 'utrota dansken vid 16.00' (sweden t03); 'Manifest Destiny' (AmericanFlaginPlace t06); 'Pakistani's who want to vandalize' and 'homosuck' (india t04); 'la escoria de Chavez' (uruguay t04); 'argentinos nojentos' (portugal t11); a joke about Norwegian sailors and rapes (europe t10); 'BASH THE FASH' and the NKVD beside Rosa Luxemburg (fullcommunism t05); 'frog shagging bastards of the north' (malta t03); a red swastika planned on a logo (liquicity t07); r/Eagles' 'Nazi Flag', 'kill this Nazi scum' and 'anti semetic bullshit' (falcons t15); 'Purify the core' (theblackvoid t02).

The next packet is packet 6: 500 items, G15 to G19 and part of G20. Its conflicts pass runs first.

`validate.py B4`, after packet 5:

```
stage B4:
  leg: adjudication
  settled items 7844 = assignment_items_expected
  rulings 2308: {'genuine-joint': 1117, 'scheme-ambiguous': 350, 'reader-error': 114, 'author-error': 334, 'author-disagrees': 208, 'item-is-a-bag': 185}
  classes 1: 2566, 2: 1990, 3: 2393, 4: 837, 5: 58; contested (3, 4, 5) 3288, ruled 2308, outstanding 980
  coder conflicts 48

warn   RETURN-B4.md is not yet written; the build leg owes it, and this leg was read as an adjudication leg because neither RETURN-B4.md, a stage-B4 manifest entry nor _packets-B4/ exists

0 errors (0 distinct shapes), 1 warnings
```
