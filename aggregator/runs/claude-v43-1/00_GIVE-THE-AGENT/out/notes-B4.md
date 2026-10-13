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
- **A theme neither reader chose.** A ruling may name one, logged loudly: `named_neither` true, and the `why` says what both readers missed that the file does say.
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
