# Notes, stage D3 (adjudication by element)

The model entered D3 frozen at pass 15 (e15f96470271763d9913e79ed8e332c164a1f176106eefacfe8ffac8e1b3fecd). A revision made here changes the model's hash; the model is frozen again, as one version, at D3c.

## What binds the rulings

- **J, 16 October, 12:59 Berlin** (through the PI):
  - Every count and reading of absent lines is split by `observation`. Only `observed-absent` and `not-needed` count as evidenced specification. `unobserved` and `not-testable` are limits of the evidence, counted apart and never as specification or correction.
  - `DROPS/D/REPAIRS.tsv` gives each room's same-session repairs: 378 rooms, 421 repairs. Where repairs bear on a ruling, repaired and unrepaired rooms are compared.
  - The labeler grade's lack of variation and the `RETURN-D2v` field defects are recorded for E2.
- **QD2-001 (J):** a dimension may stand as the element of restrict, add-condition and add-step. The eight such lines are ruled as they stand.
- **QD3-001 (J: yes to both):** each packet is read whole through `_analysis/d3_packet.py`, which selects what `mem.py adaptations --element` selects and prints every field. Rulings may be written per packet through `_analysis/d3_adjudicate_batch.py` from a rulings file (`_analysis/d3_rulings/`). The file gives a decision and a reason for every id, with no default; the writer makes the verb's checks and refuses the whole file on any failure.

## The ruling rules (logged before any line was ruled)

- **G1, instantiate.** Accept as specification when the source theme and the cited concepts show the element as stated, inside its range. Modify when the `how` claims more than the concepts show. Reject when the concepts show something else, and say what.
  - **G1a:** a member's own claim in the record to have started, made or first placed the mark shows R01's act. So do other members naming that member as its maker. A claim made after the work is weaker, and the reason says so.
  - **G1b:** each line is ruled on the line as read, with its concepts read where the `how` is doubtful. In each packet, ten lines drawn by `random.Random(20261016 + the packet's offset)` have their concepts read in full (`_analysis/d3_sample_packet.py`). A draw that finds an unsupported line sends the whole packet to be read whole.
- **G2, absent lines that mark an evidence limit** (`unobserved`, `not-testable`). Accept with kind `none` when the line gives a reason the record cannot show the element. The stage check admits no kind named "evidence limit", so kind `none` is how these lines are counted apart.
  - Where the room's placements carry the element, the concepts are read first.
  - Reject the line when the concepts show the element.
- **G3, evidenced absences** (`observed-absent`, `not-needed`). Accept as specification when the concepts show the absence or the lack of need. Otherwise reclassify as an evidence limit.
- **G4 and G5, elaborations and corrections.** Accept with `pair` when a second room's line makes the same elaboration or correction of the same element in substance, whatever its node. Otherwise the line is a particular if its evidence suffices, and pending if not.
  - Two accepted corrections that meet at the same third- or fourth-order node trigger the element's re-examination in the same leg (§2).
  - The count never chooses the revision.
- **G6.** A line that fails portability, or names its own room in `condition`, is a particular.
- **G7.** Repaired and unrepaired rooms are compared wherever repairs could bear on a ruling.
- **G8.** Every reason names its evidence.
- **G9 (logged at D3a-02, before P01's corrections were ruled).** A restrict or contradict line corrects its element only when two things hold. Its condition is one the element does not already state, and the room's concepts show the element failing without it.
  - A correction line whose content is that the cited concepts do not show the element (praise, a find, a bare title) records an evidence limit. It is accepted with kind `none`.
  - A line whose condition the statement already holds is reclassified by its concepts: specification where they show the element as stated.
  - Neither counts toward corrections met twice.
- **G10 (logged at D3a-03, before P02's lines were ruled).** P02 is shown when a concept shows a member or the room choosing, proposing or changing what the mark shows. That covers:
  - naming the picture to make, even in an unanswered proposal (a call that names the picture shows P01 and P02's lower range at once);
  - arguing or voting on the design;
  - taking the land's flag, emblems or the room's own logo as the mark by a stated choice;
  - deciding to sign the mark or not;
  - claiming or adopting a mark others made;
  - adding to the mark, enlarging it, or adding a personal piece.

  A concept that only announces, shows, locates, defends or admires a placed mark shows the result, not the settling. For P02 it is an evidence limit. A call that names no picture does not show P02.
- **G11 (logged at D3a-04, before P05's lines were ruled).** P05 is shown when a concept shows members keeping the room's placed work. That covers:
  - watching it, including a warning that it is being changed (P05's lower range);
  - repairing changed pixels;
  - calling or rallying to defend it under attack (a call to defend shows P01's hold form and P05 at once);
  - covering hours when others sleep, and handing the watch on;
  - hardening or shrinking its shape to hold it;
  - running scripts set to keep it;
  - putting upkeep before growth.

  A concept that only reports a loss, celebrates, locates, proposes or redesigns a mark does not show P05 (it may show P02, P12 or A10). Under G2 an absent line is rejected when its concepts show P05. As applied: keeping an ally's work beside the room's own is a paired elaboration, and a line where the room keeps nothing of its own is rejected (corridor-013, aeon-009); upkeep on a canvas opened after hour 73 is an elaboration, and edits to a copy after the close are evidence limits.
- **G12 (logged at D3a-05, before P04's lines were ruled).** P04 is shown when a concept shows a member doing one of these:
  - circulating a layout (a template, pixel plan, overlay or reference image that lays out the mark);
  - circulating coordinates that locate the mark (one coordinate is P04's lower range);
  - asking for a layout or for coordinates;
  - asking placers to keep to the layout.

  A script shows P04 only where the concept names the layout or coordinates it places from; otherwise it is A06's machine hands. A design proposed or argued with no layout shows P02, not P04. A call with no place or layout, a report that the mark is done, or a repair with no layout named does not show P04. As applied: locating the work by landmark or direction rather than coordinates is a paired elaboration, and so is a layout passed between rooms or used on a successor canvas.
- **G13 (logged at D3a-06, before P12's and P22's lines were ruled).** P12 is shown when a concept shows members recording what happened to their work or to the canvas around it. That covers:
  - saving or asking for screenshots, timelapses or images of the work;
  - reporting its fate (gone, survived, stood at the end, where it ended);
  - mourning a loss, imagining what the work would have been, atlas entries, and marking the end.

  A progress report during building, a call, or a celebration that only cheers does not show P12. P22 is shown only by a concept after placement ended (hour 73) in which members contest which version of the canvas or of the event is kept. That covers asking a cleanup of a shared copy to fix their work, taking part in it, arguing that damage should stay as history, and correcting accounts that describe their group wrongly. Recording alone after the close is P12. Editing a copy is P22 only where the version kept is at stake. Under G2, an absent line is rejected when its concepts show the element. As applied: a report that the work is gone is P12, while a report that it is being changed now is P05's watching (G11).
- **G13a (amendment, 16 October, D3a-06).** It was written after P22's lines other than absent were ruled and its absent lines were read, and before those were ruled. It makes two of G13's clauses exact.
  - **Correcting an account.** P22 is shown where, after hour 73, a member corrects or disputes another member's or a visitor's account of the room's work, its conduct or the event. That includes the account a question presupposes ('why did the room do nothing?'). A question that asserts nothing, once answered, is not a correction, and neither is a member's own report.
  - **The version kept, and damage as history.** P22 is shown where members set one version against another as the one that stands, where they propose keeping the damaged version in the room's records or keepsakes (sidebar, logo, stickers, poster), or where they argue that the damage is the work's history. A fond or joking reading of a flaw that keeps nothing marks the end (P12).

  It applies backwards to every P22 line ruled in the leg. One line changed: starcraft-051, from specification to evidence limit, re-ruled as an appended line.
- **G14 (logged at D3a-07, before K01's lines were ruled).** K01 is shown when a concept shows the host room's own posting keyed as April Fools play. That covers:
  - a fake post;
  - a joke takeover of the room (its name, banner, style, rules or front page);
  - parody run for the day;
  - members naming the April Fools licence for what they post;
  - members doubting that a post, claim or call in the room is meant.

  It is not shown by a concept that only explains r/place as Reddit's April Fools event. Nor is it shown by jokes about the canvas or a neighbour's art with no play in the room's own posting, or by a call to the canvas taken at face value. Under G2, an absent line is rejected when its concepts show K01. K01 is a condition, not a universal claim, so its absent lines are never corrections. Four readings were stated while ruling, logged, and checked backwards. None is an amendment; each says how a clause already written applies.
  - **The room's own venues.** The room's own chat or bot taken over counts (transformers-018, overwatch-062, rwby-042).
  - **Pranks run outside the room** (by another room, a creator, a company or a news site). These count only where members in the room engage the prank in an exchange: they play along, test or doubt it, or contest it. A bare share, a single like, praise or grade, or a report of another room's prank is an evidence limit. The contest clause was added at instantiate line 300; no earlier ruling changed.
  - **Unrun and running jokes.** These are evidence limits unless the record ties them to the day or the takeover ran:
    - a prank proposed, wished or planned and not shown run;
    - a family prank recounted;
    - a bare greeting;
    - a running joke of the room or the site, such as 'the moderators are asleep', urging rewrites, or 'if this gets N upvotes this becomes a themed subreddit'.
  - **G1b's draws.** A drawn line is unsupported when its quotes change the ruling that its how and labels would get.

## Where the mass is (`_views/rooms-x-elements.tsv`, `_analysis/d3_mass.py`)

| Lines | Count |
|---|---|
| All lines | 42,243 |
| Other than absent | 26,206 |
| Absent, evidence limits | 14,608 |
| Absent, evidenced | 67 |
| `propose` | 1,362 |

The heaviest elements by lines other than absent are P02 1,039, P05 1,004, P01 1,003, P04 980, P12 926 and K01 913. The arrows together hold 6,778 such lines, and lines naming a dimension hold 122. Each leg takes one element group: a fourth-order theme's elements, or one element with many lines.

## D3a-01: R01, the starter

R01's lines number 709, across 699 rooms. All are ruled, and none is pending.

| op | lines | accept | as evidence limit (kind none) | reject | particular | modify |
|---|---|---|---|---|---|---|
| instantiate | 579 | 566 | 0 | 5 | 7 | 1 |
| absent (all evidence limits) | 107 | 0 | 82 | 25 | 0 | 0 |
| restrict | 17 | 12 (correction) | 4 | 0 | 1 | 0 |
| add-condition | 3 | 1 (elaboration) | 1 | 0 | 1 | 0 |
| add-step | 3 | 2 (elaboration) | 0 | 0 | 1 | 0 |

**The correction, met twice, and move 172.**
- **The lines:** eleven rooms' restrict lines (Madeon-005, batman-016, futanari-009, androidgaming-013, hearthstone-008, hentai-003, katawashoujo-029, shitredditsays-004, tetris-005, transgender-005, vietnam-008) correct one clause of R01: *and whom others then join*. Six of them meet at T4-006, four of those at T3-033, and three meet at T4-005 (T3-002).
- **What the concepts show:** in every one, the starter's own act (asking, proposing, mapping, beginning, or placing alone), and no one shown joining that member.
- **Why the clause went:** R01's own range already ran from a member who only asks to a member who places alone. The statement therefore claimed more than its range. Where the records show anyone joining, they show it as an answer to a call, which the model already holds in P15, A02 and A01.
- **The revision:** the clause was split from the role (Grodal, Anteby and Holm's *splitting*) and left to those arrows. The statement now reads: *The starter: a member who proposes the mark, maps it or begins placing it. Others joining is not part of the role: it is the answer to the room's call (P15), in the order A02 and A01 state.*
- **No loosening:** the range is unchanged, so no room enters or leaves the role.
- **The record:** a `history.jsonl` line, a diary move and the snap `D3-move-splitting-172`. F-017 touches R01; it was re-examined in the same act and stands unchanged (`findings.jsonl` line 37).

**Accepted beside the revision, paired, and not folded into the statement:**
- the starter's acts shared among a few members (yugioh-009 with polandball-018);
- the start handed from one member to another (hunterxhunter-009 with shield-058).

Two rooms each are a thin warrant. They stand as shared elaborations for D4 to read, not as a change to the role.

**Particulars** (held in their rooms):
- two starts on canvases opened after hour 73 (AcePlace-029, TransFlagPlace-003);
- the starter of an enlargement as distinct from the first start (thailand-008);
- deference to a starter that gave no lasting command (metroid-012);
- a room taking up a sign begun outside it (loliconsunite-006);
- five lines that fail portability.

**Absent lines rejected (25).**
- **The pattern:** the labeler marked R01 unobserved only because no one was shown joining, while the cited concept shows a member proposing, mapping or beginning the mark. That is R01 as revised, and it was already inside the old range.
- **Three re-ruled under G1a:** thebluecorner-003, teamcube-023 and apocalypserising-029, each from evidence limit to reject.
- **Two absent lines left as evidence limits although the room's placements carry R01:** glasgow-024 points to a saltire already in progress, and ElderScrolls-008 was rejected.

**Instantiate lines rejected or modified (6).**
- belgium-001 adds to a flag that already exists;
- sonicthehedgehog-029 carries on a face already half built;
- uvic-002 calls to defend a placed logo;
- wholesomememes-002 asks others to help hearts that already exist;
- zootopia-002 cites only an instruction to place;
- TeamDignitas-001 is modified: the starter is reported, not named.

**Repairs (G7).** R01's rulings do not differ between lines in repaired rooms (381 lines) and unrepaired rooms (328 lines): reject 3.9% against 4.6%, evidence limits 11.5% against 13.1%, particular 1.8% against 0.9%.

**Disclosed limits.**
- Before QD3-001 was answered, packets were read through the verb, which clips each `how` at 90 characters.
- The first 25 instantiate reasons were worded as if every concept had been read; for most, only the line and its placement were read.
- After the answer, every ruled R01 line was re-read whole. One ruling changed (belgium-001).
- Every packet's seeded draw was read in full. One draw found an unsupported line (sonicthehedgehog-029), and that packet was read whole.

**The re-check.** R01 is a rewritten element, so the rooms whose adapted accounts rely on it go to the re-check (§5). The scope, `recheck-scope.json`, is set when the re-check is built, after the element groups.

### Close-check, D3a-01

`validate.py D3` reports 709 of 42,243 ledger lines ruled, and nothing wrong with the rulings. It fails on one shape alone, in five lines: P06, R02, K03, K04 and P19 carry status `candidate` from the C2 and C5 cuts, but the D3 check admits a candidate only with `since: D3`, a proposal accepted at this stage. Changing a status before these elements' own groups are ruled would pre-empt those rulings, and setting `since` to D3 would misstate their history. I asked as QD3-002 and changed neither.

**J's answer (QD3-002).** J said the question forgot that the analyst is doing induction. I may place these codes where I see fit, with some documentation, deciding from the knowledge of the population I have amassed. Rules are useful, but I should ask for the changes I need so that the knowledge shows; the rules should not bound the understanding. The handler changed the check to admit a candidate cut at an earlier stage, and `validate.py D3` now gives 0 errors.

**My reading of the five.** They keep status `candidate` for now. No rule binds them. The evidence that would decide them is their own D2 lines (lines other than absent: P06 in 564 rooms, K04 in 530, R02 in 500, P19 in 240, K03 in 124), and I have not read those yet. Each is re-admitted, bounded, withdrawn or kept when its group is read.

## D3a-02: P01, the room's calls

P01's lines number 1,021, across 704 rooms. All are ruled, and none is pending. No line was rejected or modified. Counts are from `_analysis/d3_group_close.py`.

| op | lines | specification | elaboration (paired) | evidence limit (kind none) | particular |
|---|---|---|---|---|---|
| instantiate | 723 | 692 | 0 | 1 | 30 |
| add-step | 155 | 2 | 141 | 0 | 12 |
| link | 60 | 1 | 52 | 0 | 7 |
| add-condition | 53 | 0 | 39 | 6 | 8 |
| absent (all `unobserved`) | 18 | 0 | 0 | 18 | 0 |
| restrict | 12 | 1 | 0 | 9 | 2 |
| all | 1,021 | 696 | 232 | 34 | 59 |

**What the instantiate lines show.** Every line accepted as specification cites a call: a member asks the room, or a kindred room, to place for a work. The calls run across P01's whole range:
- one unanswered post (bdsm-001, latvia-002, nonbinary-001);
- a run of calls (drumcorps-001, wales-002);
- cheering among the calls (alberta-003, bardmains-002, columbia-003, davidbowie-002);
- a set time for placing together (austria-018, lebanon-001, osugame-002, raocow-002).

Three kinds of call fit the statement as written. I name them so that the next stage can see them:
- calls whose target is another room's work (UMiami-001, falcons-001, homelab-001, placehfarts-001, wario-001, theblackvoid-001), the call that A15 turns against a rival;
- calls answered in part by machine (aeon-001, detroitredwings-002, heyyea-001, sbu-001, ukplace-001), which A06 holds;
- calls made in a room's thread by a visitor or a kindred group (AceOfAngels8-001, parabola-001).

The line nearest to a reject was alberta-003, a reader's "Good luck with the project :)". P01's range names cheering, and the room's calls are in alberta-002, so I accepted it. A stricter reading would reject it, and no other ruling turns on it.

**Particulars (59).**
- **Portability:** 35 lines fail it (rule 5): 30 instantiate lines, and anime-002, bulgaria-003, placehfarts-004, ravens-026 and patriots-007.
- **Supported in one room only (24):**
  - a call refused because of who made it (4chan-042);
  - a member's reason for joining, given once (foxes-038, 4chan-043, onepunchman-009);
  - a call withdrawn, reopened or renewed after a poor reception (raocow-053, raocow-054, lexington-010, rush-006);
  - defence divided from building, which bears on C01 (purdue-011);
  - spare accounts asked for (foxstevenson-012), translation offered (epublica-006), and a host's joke used as a reward (dota2-047);
  - a call's course local to its room (AceOfAngels8-002, OrderOfTheKoi-003, gratefuldead-015, polyamory-008, anarchocapitalism-017, ubreddit-057, wsu-012, giivasunner-061, newzealand-062, rpi-061, trees-019, lost-012).

**The elaborations (232, every one paired).** Each was accepted because a second room's line makes the same elaboration in substance (G4). They are shared changes, not a revision: P01 states the call, and these lines say what comes with it.
- **Calls recur after the start (link).** They recur after a loss, a failed attempt or a move (16 rooms), and during upkeep when the work is damaged (7). They follow a finished work, for the next one (10), and appear on successor canvases after hour 73 (6). In 8 rooms the visible mark itself brings helpers. A host's permission can open a call.
- **Conditions on calls (add-condition):**
  - reach and access (7 rooms);
  - helpers waiting for a target (5);
  - competing commitments (4);
  - calls timed to ordinary gatherings, such as game intermissions and streams (6);
  - calls at or after the close (5);
  - account eligibility (2);
  - an active subset rather than the membership (5);
  - outside audiences weighed (3);
  - the April Fools frame getting in the way (2);
  - the host's handling limiting reach (3).
- **Steps that come with calls (add-step):**
  - teaching newcomers the canvas, the timer and access;
  - moving coordination into chats;
  - seeking visibility through upvotes, stickies, signs and landmarks;
  - redirecting helpers to work under way;
  - incentives;
  - answers asking for direction;
  - answers reporting the member's own labour or cost;
  - the room's ordinary threads used as venues;
  - bare refusals (math-011 with wow-050);
  - members called by the room's own name for them (TheHulk-055 with thepointing-031).

**Reclassified as specification (4).**
- falcons-011 and penguins-005 (add-step) ask for a set time to place together, which P01's range already holds.
- sakuragakuin-005 (link) shows a start followed by a call, the order A02 states.
- nyu-002 (restrict) shows a call and its answers. P01 names the call and not its answer (G9).

**Evidence limits (34, kind `none`).**
- **Absent lines (18):** all are `unobserved`, and none is evidenced. Their concepts are announcements, welcomes, questions or celebrations with no call.
- **Restrict (9) and add-condition (6) lines:** each records that its cited concepts do not show a call, for example praise, a find on the canvas, a bare help title, a misread target (UNLincoln-003) or a visitor's request (mariokart-002).
- **Instantiate (1):** Bravenewbies-005 seeks upvotes and holds no call to place.
- Under G9 none of these counts as a correction.

**No correction met twice.** No P01 line was accepted as a correction. The two correction lines are particulars (lost-012, patriots-007). P01's statement and range stand as served. P01 is not rewritten, so it adds no room to the re-check.

**Repairs (G7).** Repaired rooms have 582 lines, 94.3% accepted. Unrepaired rooms have 439 lines, 94.1% accepted. Repairs made no difference to the rulings.

**Carried to later groups.**
- **A return arrow into P01.** Calls recur after a loss or a move in 16 rooms. The model holds no arrow back into P01 and says that no loop is grounded. I weigh such an arrow with the group for P10 and A10, with an order test written first.
- **Bare refusals.** In math-011 and wow-050 members refuse calls without giving a reason. F-014 records that refusals of attack calls give one. I weigh this with the group for P15 and A12.
- **What a mark brings back into its room** (open since C2). In 8 rooms the visible mark brought helpers.

**Disclosed limits.**
- The instantiate lines were read whole in pages of 30. Six seeded draws (verb offsets 326 to 826, 60 lines) found no unsupported line.
- After a compaction I re-read lines 120 to 179 whole before writing their rulings.
- One count command used awk with field references, which the guard rules I carry forbid. The counts it gave match `d3_group_close.py`.

### Close-check, D3a-02

`validate.py D3` reports 1,730 of 42,243 ledger lines ruled (R01's 709 and P01's 1,021), with 0 errors and 0 warnings.

## D3a-03: P02, the room settles what its mark shows

P02's lines number 1,070, across 704 rooms. All are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`.

| op | lines | specification | elaboration (paired) | correction (paired) | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 762 | 724 | 0 | 0 | 0 | 35 | 3 |
| add-step | 115 | 7 | 102 | 0 | 3 | 3 | 0 |
| link | 84 | 1 | 81 | 0 | 2 | 0 | 0 |
| add-condition | 55 | 2 | 49 | 0 | 0 | 4 | 0 |
| absent (27 `unobserved`, 4 `not-testable`) | 31 | 0 | 0 | 0 | 28 | 1 | 2 |
| restrict | 23 | 9 | 0 | 2 | 10 | 2 | 0 |
| all | 1,070 | 743 | 232 | 2 | 43 | 45 | 5 |

**What the instantiate lines show.** Every line accepted as specification cites members proposing a picture, arguing its design, taking a flag or emblem as the mark, signing it, adopting another's mark, or adding to it (G10). The range runs from one unanswered proposal (glasgow-006, winnipegjets-009) to designs argued over days (uvic-005, megaman-005). Three lines were rejected because their concepts show something other than settling:
- a sighting (Madeon-003);
- a defence call (OneTrueEmilia-009);
- marks found and their makers guessed (wallstreetbets-068).

**Absent lines.** None is evidenced. 28 are evidence limits: announcements, locations, defence and admiration with no settling. Two were rejected under G2 and G10 because their concepts name the picture to make (Bravenewbies-012, "coop... with EVE logo"; liquicity-009, "Trying to get the Liquicity logo on").

**Restrict lines.** Ten are evidence limits under G9. Seven of them come through a third-order theme of finding marks on the canvas (T3-082), which lifts into T4-006: finding is not claiming. Nine are specification, because P02 already holds what they restrict, for example an unanswered proposal or a signing decision. Two are particulars: anarchism-011 refuses to own a flag at all, and transgender-056 fails portability.

**The paired correction, not met twice.** PlaceNL-012 and portugal-013 correct P02 in substance. A change settled by some members was erased by the room's own keepers: in PlaceNL its defence script ("De huisjes worden allemaal weggepoetst"), in portugal its placers ("a hivemind apaga tudo"). They lift to different nodes (T3-028 under T4-009; T3-188 under T4-019), so they do not trigger the re-examination of §2.

**The shared patterns (232 elaborations, all paired).** Rooms are counted from the wording of my rulings.
- **A change held only where its keepers knew it (14 rooms).** In 13 rooms, members repairing to the old design or scripts set to its last form erased or blocked a settled change unless they were told. Examples: weezer "stop fixing the redesign"; aggies a quick vote "so a design change is not mistaken for an attack"; cubers alerting the chat; PlaceNL waiting for the member with script permission. In uruguay an ally's bots held the design.
- **Neighbours shaping the design (32 rooms).** Agreements, leave, requests, help received and promises to allies set where the mark goes, its size and its colours.
- **The design sized to the room (26 rooms).** Size and detail were fitted to the hands, space and upkeep the room expected (Jamaica, sadboys, strangerthings).
- **A finished work reopening the design (19 rooms).**
- **Designs settled in chats and brought back to the thread (18 rooms).**
- **Votes, polls, official rulings or asked agreement (14 rooms).**
- **Further pairs:**
  - the palette bounding the design;
  - additions waiting on the main mark;
  - started designs kept because changing them costs work;
  - signatures kept off shared marks or added so others know whose mark it is;
  - content refused because it does not belong;
  - the mark's meaning settled again after the close.

**Particulars (45).**
- **Portability:** 39 fail it (rule 5).
- **Supported in one room only (6):**
  - location as part of the mark's meaning (2007scape-038);
  - peace claims made with hearts and a dove (europe-062);
  - design judged by a member who does not place (indieheads-007);
  - language as cover for design talk (eesti-042);
  - a faction naming a feature of its field (orderofthebluecorner-005);
  - refusing to own a mark (anarchism-011).

**No revision of P02.** No correction is met twice, and P02's statement and range stand as served. The keepers pattern is a relation between settling and keeping, and its other end, P05 with A06's scripts, is not yet read. I weigh an arrow from keeping back into settling, or a condition on P02's "adds to it", when P05's group is read, with an order test written first. In the quotes the change is proposed before it is erased.

**Repairs (G7).** Repaired rooms have 585 lines, 95.7% accepted. Unrepaired rooms have 485 lines, 94.8% accepted. Repairs made no difference.

**Carried to later groups.**
- The keepers pattern goes to P05's group.
- A finished work reopening the design goes to the close group (A07 to A09), beside P01's calls after a completion.
- Neighbours shaping the design goes to the group for A04, A14 and A19.
- F-017 is not re-examined, because P02 is not revised. Its weak absence claim, that goals were rarely chosen between rivals, should be read against the P02 lines where rooms choose between designs when F-017 is next touched.

**Disclosed limits and corrections.**
- **Draw labels.** In the diary, the P01 draw ranges of D3a-02 are labelled 21 lines too high. Verb offset 326 covered instantiate 99 to 198, not 120 to 219, and P01's instantiate lines 699 to 722 fell in no draw. Every P01 line was read whole, so no ruling changes.
- **P02 draws.** Eight seeded draws covered P02's instantiate lines (verb offsets 202 to 902, 80 lines) and found no unsupported line. One draw was first run with its quotes filtered out; it was rerun whole and read.
- **Guard refusal.** One command used `cut -c` after `mem.py`, and the guard refused it.

### Close-check, D3a-03

`validate.py D3` reports 2,800 of 42,243 ledger lines ruled (R01's 709, P01's 1,021 and P02's 1,070), with 0 errors and 0 warnings. `validate.py --open D3` reports `EXPECTATIONS.jsonl` missing from the folder. The stage forbids reading it (E1 scores it), so it is the harness's to place, not mine.

## D3a-04: P05, the room keeps its placed work

P05's lines number 1,092, across 704 rooms. All are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py` and `_analysis/d3_pattern_counts.py`.

| op | lines | specification | elaboration (paired) | correction (paired) | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 655 | 630 | 5 | 0 | 0 | 17 | 3 |
| add-step | 127 | 19 | 103 | 0 | 2 | 3 | 0 |
| link | 93 | 2 | 88 | 0 | 0 | 3 | 0 |
| add-condition | 91 | 3 | 84 | 0 | 2 | 2 | 0 |
| absent (79 `unobserved`, 9 `not-testable`) | 88 | 0 | 0 | 0 | 83 | 1 | 4 |
| restrict | 38 | 13 | 7 | 4 | 13 | 1 | 0 |
| all | 1,092 | 667 | 287 | 4 | 100 | 27 | 7 |

**What the instantiate lines show.** Every line accepted as specification cites members keeping the room's placed work (G11). They watch it, repair changed pixels, call and rally to defend it, cover the night and hand the watch on, harden or shrink its shape, run scripts, and put upkeep before growth. The range runs from one member replacing a single pixel (totallynotrobots-015, oneplus-016) to shifts across time zones and scripts over days (chicubs-017, bostonbruins-015, KState-015). Three lines were rejected:
- a member fixing an image that is not the room's (corridor-013);
- an allied room's member offering a script that keeps that room's own figure (aeon-009, re-ruled from accept);
- a build that cannot gain ground and a proposal to move, which A10 holds (warthunder-017).

Seventeen instantiate lines fail portability. Five are elaborations: three keep work on a successor canvas or a host's land (nightinthewoods-015, sadboys-017, yuyuyu-005), and two meet a one-room line (hoodr-009, utahjazz-020).

**Absent lines.** None is evidenced. 83 are evidence limits. Four were rejected under G2 and G11 because their concepts show keeping (hunterxhunter-013, peterdraws-021, rpi-015, seventeen-017). One fails portability.

**Restrict lines.** Thirteen are evidence limits under G9: warnings with no defence shown, edits to a copy after the close, other rooms' work, attacks and growth. Thirteen are specification. Seven are paired elaborations: upkeep weighed against growth, members disputing whether to keep defending, and a room keeping some works while letting one go. Four are corrections. One fails portability.

**The correction, met twice, and move 173.**
- **The lines:** OnePiece-012 and leagueoflegends-053 are accepted corrections at T4-013. Both target the same clause of P05, "members watch it and repair changed pixels". monsterhunter-016 (T4-007) and portugal-029 (T4-019) meet them in substance.
- **What the concepts show:** members repaired an intended feature, a valid fix, an agreed change or a settled addition back to the form they knew. "people thought the fixing of it was attempted vandalism. I fell into that trap myself" [OnePiece/c0232]; "If someone would stop patching up the white glare" [leagueoflegends/c1854]; "whoever fixes the potion keeps undoing my work" [monsterhunter/c0165].
- **The alignment holds beyond the four.** Accepted P05 lines in 68 rooms carry the same mechanism, most as paired elaborations. Keepers who do not know a planned change take it for damage. Keepers check the intended form, or are told it, before they repair. Builders give a change up when keepers undo it (cubers-025, utahjazz-013, weezer-014). P02's lines showed the same mechanism from the design side in 14 rooms. (The history line says 67 rooms: its phrase search did not yet match portugal-029's wording.)
- **The order test** (`_analysis/d3_order_keepers.py`, its rules logged before it ran) holds in 7 of 11 rooms. There keepers erase the change first and, once told, switch within the hour: ripcity in two minutes, mcgill in twenty. In three rooms (leagueoflegends, monsterhunter, cubers) the room told its keepers in the thread, and they kept erasing for hours, or the builders gave the change up. The eleventh, tf2, fails on the order of the reports, not of the acts. One member reported their own earlier erasure after two others had switched.
- **The revision** (Grodal, Anteby and Holm's *relating*) relates the repair clause to P02. The statement now adds: *Repair restores the form the keepers know. A change the room has planned or agreed (P02) is therefore repaired away as damage until its keepers are told of it, and it is lost or given up where the telling does not reach them.*
- **No loosening:** the range is unchanged, so no room enters or leaves P05. "Puts upkeep before growth" stands.
- **The record:** a `history.jsonl` line, a diary move and the snap `D3-move-relating-173`. No finding touches P05. This closes the hypothesis carried from D3a-03, the keepers pattern into P02. It now sits in P05's statement, not in a new arrow.

**The shared patterns (287 elaborations, all paired).** Rooms are counted from the wording of my rulings, and a room may carry more than one pattern.
- **Keepers and the intended form (68 rooms):** the revision above.
- **Scripts in upkeep (21 rooms, specifications included).** Scripts keep the work, and the room's own scripts can work against it (uiowa-054, wildhockey-014, AmericanFlaginPlace-014).
- **Celebration or completion turning into upkeep (18 rooms).**
- **Upkeep weighed against growth (17 rooms).** Members weigh repair against growth, press growth beside upkeep, keep the placed part while building the rest, or use growth as defence (theblackvoid-020, placestart-016, traaaaaaannnnnnnnnns-017).
- **The shape and size chosen to hold the work (17 rooms).** The work is enlarged or moved to be easier to hold, its size argued both ways, its design simplified for upkeep, or kept legible so it is not taken for noise.
- **The room's own members as the damage (16 rooms).** These lines show internal fighting, members' mistakes, outward attacks that cost home upkeep, and members' own choices pulling pixels from a call to concentrate.
- **The visible work drawing its own keepers (13 rooms),** with newcomers recruited into upkeep.
- **Upkeep coordinated in chats (12 rooms).**
- **Further pairs:**
  - keeping begins again on successor canvases (6 rooms);
  - allies keep each other's work (6);
  - keeping costs members' time and rest (5);
  - sanctions and contact with placers (5);
  - would-be keepers need the work located (3);
  - dealings with neighbours (3);
  - watching the attackers' channels (2);
  - giving part up to keep the rest (2);
  - upkeep as a sign to neighbours that the room still holds the work (math-016 with hoodr-009);
  - taking down the posts that draw attackers (fivenightsatfreddys-022 with utahjazz-020).

**Particulars (27).**
- **Portability:** 23 fail it (rule 5), among them toolband-020, whose hit is "lost sleep".
- **Supported in one room only (4):**
  - a defence that steers an attack onto a third room's work (GuardiansOfDatBoi-015);
  - keeping a work through copies of it (TreePlace-012);
  - a member redirecting effort after the work changed form (futurama-058);
  - a consumer outcome of upkeep (soylent-041).

**Re-ruled in this leg.** Each re-ruling is an appended line, and the ledger keeps both lines.
- aeon-009: accept to reject, on corridor-013's ground.
- math-016 and hoodr-009: particular and specification to a paired elaboration, after a draw found hoodr-009.
- fivenightsatfreddys-022: particular to a paired elaboration with utahjazz-020.

**Repairs (G7).** Repaired rooms have 604 lines, 97.5% accepted. Unrepaired rooms have 488 lines, 96.1% accepted. Repairs made no difference.

**The re-check.** P05 is rewritten, so the rooms whose adapted accounts rely on it join R01's in the re-check (§5). The scope is set when the re-check is built.

**Carried to later groups.**
- Upkeep weighed against growth, and growth used as defence, go to D4 beside "puts upkeep before growth".
- Scripts working against the room's own keeping go to A06's group.
- Allies keeping each other's work, and dealings with neighbours, go to the group for A04, A14 and A19.
- Celebration turning into upkeep goes to the close group (A07 to A09).

**Disclosed limits and slips.**
- **Draws.** Seven seeded draws covered P05's instantiate lines (verb offsets 307 to 907, 70 lines) and found no unsupported line.
- **The order test** codes one episode per room. I chose rooms where my rulings named an erasing concept, so the test checks the mechanism's order; it is not a sample.
- **Pairs across ops.** Some link and add-step elaborations pair with add-condition lines (G4 pairs by substance, whatever the node).
- **Slips.** The guard refused one `cut -c` after `cite.py`. One add-step line (toolband-020) was first drafted as accepted. The batch check refused it as non-portable, and it was ruled a particular before anything was written.

### Close-check, D3a-04

`validate.py D3` reports 3,892 of 42,243 ledger lines ruled (R01's 709, P01's 1,021, P02's 1,070 and P05's 1,092), with 0 errors and 0 warnings. Every accepted elaboration and correction in P05's group has a pair.

## D3a-05: P04, the room's layout and its coordinates

P04's lines number 1,034, across 703 rooms. All are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py` and `_analysis/d3_pattern_counts.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 683 | 656 | 19 | 0 | 0 | 8 | 0 |
| add-step | 198 | 4 | 192 | 0 | 0 | 2 | 0 |
| absent (43 `unobserved`, 11 `not-testable`) | 54 | 0 | 0 | 0 | 47 | 0 | 7 |
| add-condition | 47 | 2 | 44 | 0 | 0 | 1 | 0 |
| link | 39 | 0 | 38 | 0 | 0 | 1 | 0 |
| restrict | 13 | 6 | 0 | 0 | 7 | 0 | 0 |
| all | 1,034 | 668 | 293 | 0 | 54 | 12 | 7 |

**What the instantiate lines show.** Every line accepted as specification cites a member doing one of these (G12):
- circulating a template, pixel map, grid, overlay, spreadsheet or reference image;
- giving or asking for coordinates;
- telling placers to follow the layout.

The range runs from one coordinate in a call (AprilKnights-009, '(543,228)') to official layouts with every pixel located and strays rebuked (archlinux-008, monalisaclan-011, starcraft-009). No instantiate line was rejected. Nineteen are paired elaborations:
- the work located by landmark or direction rather than coordinates (8 lines, among them GreenEmpire-002, 'Bottom Left!');
- a placed part used as the reference others build from (Fez-010, wine-009);
- work carried to a successor canvas (Honduras-008, gravityfalls-010, purplecorner-008, sadboys-013);
- a layout passed between rooms (germany-006, simonfraser-007, yuyuyu-004);
- the target image kept for those who place by hand beside the scripts (theitalyplace-009 with cmu-011);
- a revised layout reaching a member who had missed it (redpandas-013).

**Absent lines.** None is evidenced. 47 are evidence limits: announcements, chat invitations, relative places and titles whose images are not in the record. Seven were rejected under G2 and G12 because their concepts circulate or ask for a layout:
- COSI-006, a target repository;
- PinkVomitMonster-005, a reference image;
- aeskwadraat-006, a 38×16 design;
- buffalo-009, 'Do we have a plan somewhere yet?';
- lithuania-008, the flag plan;
- placehfarts-016, 'Our goal.';
- telegram-013, step images.

**Restrict lines.** None corrects P04. Six are specification: an agreed image shared, a picture to follow exactly, a final design to aim for, a reference with landmarks, a location, and a gridded picture the builders used. Seven are evidence limits.

**No correction, so no revision.** No P04 line was accepted as a correction, so §2 is not triggered and P04 stands as served.

**The shared patterns (293 elaborations, all paired).** Rooms are counted from the wording of my rulings, and a room may carry more than one pattern.
- **A layout guides only the placers it reaches (56 rooms).** This is move 173's mechanism seen from the layout's side. A revision must be announced where placers look, pinned, sent to placers one by one by private message, or the old template retired. Otherwise keepers restore the superseded version (CKCrusaders-053, ripcity-014, uofm-009, tf2-052). Some rooms build the recognisable part first so that others read the work as work (placeDE-053, witcher-016).
- **Chats.** The rulings of 71 rooms mention a chat, specifications included. The paired lines show plans made in a chat and relayed back to the thread, and invites kept open for those outside (argentina-068, placecanada-016, darksouls-054, pcmasterrace-017).
- **The layout itself checked and corrected (35 rooms).** Rooms check the layout against the canvas, fix missing rows and wrong pixels, settle colours and anchors, and make competing versions give way to one (cavestory-007, xenoblade_chronicles-011, predators-009).
- **Scripts, tools, overlays and spreadsheets (57 rooms, specifications included).** These include layouts fed to scripts, scripts kept on the current layout (monstercat-051, uofm-013) and tools that turn a picture into a grid.
- **Moves and restarts publish new coordinates (17 rooms).**
- **The work located by landmark or direction (15 rooms).**
- **A current view of the canvas, by refreshing before placing (13 rooms).**
- **A layout in a form placers can use (13 rooms):** coordinates on mobile, direct links, image hosts and working invites.
- **Newcomers taught what the canvas is and how to place (12 rooms).**
- **One plan made official or kept current in the organising post (12 rooms).**
- **Further pairs:**
  - a layout passed between rooms (8 rooms);
  - work carried to successor canvases (5 rooms);
  - the layout fitted to the room's hands and space (5 rooms);
  - keepers asking for the layout to repair by (4 rooms);
  - a placed part used as the reference (4 rooms);
  - coordinates given after the close so readers can find the work (corridor-007, baylor-008, titanfall-007).

**Particulars (12).**
- **Portability:** 9 fail it (rule 5).
- **Supported in one room only (3):**
  - a template kept to hold a truce with neighbours (dbz-067 and dbz-068, one room);
  - a public wall of shame for members who keep making wrong corrections (cirkeltrek-020).

  A search of P04's lines found no second room for either.

**Re-ruled in this leg.** Each re-ruling is an appended line.
- **corridor-007:** its pair changed from oneplus-008 to baylor-008. oneplus-008's coordinates come before the close (h+43.8, h+69.4), so they do not show readers finding a finished work.
- **witcher-015:** re-ruled from elaboration to specification after a draw read it whole. Its c0042 posts a lettering template.

**Repairs (G7).** Repaired rooms have 585 lines, 98.3% accepted. Unrepaired rooms have 449 lines, 98.0% accepted. Repairs made no difference.

**Carried to later groups.**
- **Whether the layout is how P05's keepers are told.** This would be an arrow from P04 into P05, weighed with an order test. The P04 lines show the telling (announcements, pins, messages, retired templates), and move 173 shows what happens without it.
- **Chats as the place where plans are kept and relayed.** No element lists T4-010, which these lines lift into. This goes to the unattached-lines leg.
- **A layout passed between rooms** goes to the group for A14 and A19.
- **Moves and restarts publishing new coordinates** go with A10 and P10.
- **Coordinates given after the close** go with P12.

**Disclosed limits and slips.**
- **Draws.** Seven seeded draws covered P04's instantiate lines (verb offsets 300 to 900, 70 lines), and none found an unsupported line. One draw corrected a kind (witcher-015).
- **Images.** Many P04 lines rest on images whose contents are not in the record. Where a concept names a plan, goal or design posted as an image, I read it as a layout circulated. Where a title alone was given, I counted it as an evidence limit (OrderOfTheKoi-023, gameboy-015).
- **A diary count.** The note logging add-step said 193 elaborations and 3 specifications. The batch outputs give 192 and 4, and a correction note follows it.

### Close-check, D3a-05

`validate.py D3` reports 4,926 of 42,243 ledger lines ruled (R01's 709, P01's 1,021, P02's 1,070, P05's 1,092 and P04's 1,034), with 0 errors and 0 warnings. All 295 pairs in P04's rulings files name a P04 line (`_analysis/d3_pair_check.py`).

## D3a-06: T4-027, the record after the close (P12 and P22)

The group holds two elements. P12 is the room's record of what happened to its work and to the canvas. P22 is the field's tentative entry from C4, in which members contest which version of the canvas and of the event is kept. All 1,759 lines are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `_analysis/d3_pattern_counts.py` and `_analysis/d3_field_entry_counts.py`.

**P22** (782 lines, 705 rooms):

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| absent (455 `unobserved`, 65 `not-testable`, 1 `observed-absent`) | 521 | 1 | 0 | 0 | 495 | 6 | 19 |
| instantiate | 158 | 140 | 0 | 0 | 0 | 4 | 14 |
| restrict | 76 | 51 | 0 | 0 | 25 | 0 | 0 |
| add-condition | 12 | 3 | 8 | 0 | 1 | 0 | 0 |
| add-step | 12 | 6 | 5 | 0 | 1 | 0 | 0 |
| link | 3 | 1 | 2 | 0 | 0 | 0 | 0 |
| all | 782 | 202 | 15 | 0 | 522 | 10 | 33 |

**P12** (977 lines, 705 rooms):

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 766 | 689 | 0 | 0 | 0 | 59 | 18 |
| add-step | 104 | 36 | 64 | 0 | 2 | 2 | 0 |
| absent (44 `unobserved`, 7 `not-testable`) | 51 | 0 | 0 | 0 | 50 | 0 | 1 |
| link | 24 | 9 | 15 | 0 | 0 | 0 | 0 |
| restrict | 18 | 9 | 0 | 0 | 8 | 1 | 0 |
| add-condition | 14 | 10 | 2 | 0 | 2 | 0 | 0 |
| all | 977 | 753 | 81 | 0 | 62 | 62 | 19 |

**Time.** I printed every concept's hour for P22's restrict, add-condition, add-step, link and instantiate lines (`_analysis/d3_line_hours.py`). Each line's concepts fall after hour 73, with one exception: india-061, a restrict line whose concept is at hour 61.3, was ruled an evidence limit. The labelers read P22 as the statement dates it.

**What P22's accepted lines show.** By a phrase search over my reasons, the 177 rooms where P22 is shown are these:
- **113 rooms correct or dispute an account of the room's work or conduct.** Examples are 'It did participate' (minecraft-055), who attacked whom (fivenightsatfreddys-058), and whether the work was made by hand or by script (porterrobinson-062).
- **33 rooms contest which image or copy stands.** Examples are TheB1G-023, yogscast-049 and philippines-036.
- **31 rooms ask for or take part in a shared cleanup.** Examples are 2007scape-052, partyparrot-041, formula1-035 and straya-032.
- **15 rooms argue that the damage is the work's history.** Examples are SquareSpiral-041, thesilphroad-030 and donaldglover-035.

The last three clauses together cover 71 rooms.

**What P22's rejects show.**
- **14 instantiate lines.** Their concepts show one of the following:
  - a member's cleaned copy with no version contested, which G13 places in P12 (radiohead-049, uofm-047, placestart-045);
  - another room's account (bangtan-040, malaysia-026);
  - a posting dispute (re_zero-034);
  - reports of fate (overwatch-079).
- **19 absent lines.** Their concepts show P22 itself, for example:
  - 'Remember it for what it was, not for what it became!' (predators-052);
  - 'Change the HI logo to match' the locked red dot (cgpgrey-046);
  - 'I think the timelapses encapsulate r/place much better' (babymetal-060).
- **One observed absence holds.** In ElSalvador-028 the members share a disputed flag with a neighbour rather than contest it.

**What P12's accepted lines show.**
- The 689 instantiate specifications cite what G13 lists:
  - screenshots and timelapses;
  - reports of fate;
  - mourning;
  - imagined art;
  - atlas and wiki entries;
  - the end marked.
- The range runs from one request ('Anybody have a screenshot?', Okami-023) to rooms that archive, write histories and rebuild timelapses from raw dumps (portugal-061, brasil-053).
- **The 18 rejected instantiate lines** show other acts. Six are progress posts or images during building (Jamaica-053, udub-032, vim-033, vim-034, neutralmilkhotel-020, thailand-036). The rest are:
  - live warnings that the work is being changed, which G11 assigns to P05 (PurplePixels-032, RelientK-052, TheGreatGreenBox-034);
  - calls or a member's own upkeep (glasgow-017, anarchocapitalism-016, germany-020, hoodr-018);
  - a layout (GabrielDropout-045);
  - a bare question (ducks-041);
  - an approval or admiration (redvsblue-044, qotsa-035, linux-056).
- **The one rejected absent line** (mamamoo-021) asks what happened to r/place, which is P12's lower range, as cgpgrey-050 shows.

**No correction, so no §2 re-examination.** Neither element has an accepted correction. P22's 76 restrict lines name conditions the statement already holds, or they record evidence limits. P12 stands as served.

**The shared patterns.** P12's 81 elaborations and P22's 15 are all paired. Rooms are counted from the wording of my rulings.
- **P12, recording entered from a loss with no celebration before it (14 rooms):** for example ghibli-028, pebble-035, starcitizen-071 and planetside-052. This bears on A08, which runs from celebration to recording.
- **P12, the outcome's account qualified or contested (11 rooms):** cardinals-048, gameboy-020 and scp-063, among others. This is the ground P22 holds.
- **P12, a fixed flaw turned into a joke or given a meaning (11 rooms):** a scar, a charm, an exhaust port (rwby-053, turkey-042, empiredidnothingwrong-057).
- **P12, members explain the event to those who missed it (9 rooms),** and the record is read and decoded (8 rooms).
- **P12, archive and data work, catalogues and other media (8 rooms).** Examples are a pixel feed logged to a file, prints, a game-world reconstruction and a survey.
- **P12, further pairs:**
  - relief and regret at the end (4 rooms);
  - cleaned or finished versions after the close (4 rooms);
  - saving the record against an expected loss (3 rooms);
  - failed attempts closed with thanks (2 rooms);
  - the host's moderation keeping records in view (unturned and nintendo);
  - records used as proof in a dispute (DCFU and worldpowers).
- **P22's elaborations:**
  - account correction apart from any cleanup (anime-062, magictcg-045, morrowind-048);
  - the meaning of the event contested (europe-037, texas-028, TransFlagPlace-032);
  - whether the work was kept by hand or by script (mylittlepony-054, pathofexile-057, rocketleague-041);
  - a preferred version kept beside the accurate one (stlouisblues-058, buffalobills-054);
  - the account tested against the record (uwaterloo-053, fivenightsatfreddys-059);
  - a loss the room could not repair before the close, sent to the cleaned copy (AyyMD-061, bih-058);
  - plans supplied to a cleaner (AyyMD-056).

**Particulars.**
- **P12, 62.** All of them fail portability.
- **P22, 10,** which also all fail portability:
  - DevonUK-049, Honduras-031, animalcrossing-039, bindingofisaac-032, neopets-035, simonfraser-037 (absent);
  - frankocean-054, india-028, ockytop-024, spain-023 (instantiate).

**Re-ruled in this leg.** Each re-ruling is an appended line.
- **starcraft-051 (P22).** It moved from specification to evidence limit under G13a, which applies backwards: a fond reading of a stray pixel as the figure 'winking' keeps nothing.
- **DCFU-056 (P12).** It moved from particular to an elaboration paired with worldpowers-050, once a second room used the record as proof.

**Move 174 (developing working hypotheses), P22.**
- P22 was ruled standing, and its range was rewritten. Two history lines record this (status; range).
- The statement stands as the field wrote it. The range named only the cleanup and the scars. It now also names, at its lower end, one member correcting a claim about the room's work. That form is the commonest, and the statement already holds it, so no room enters that the statement did not admit.
- The move was first logged as 'stabilizing', which is not one of the eight. History line 139 corrects the name, and my revise tool no longer admits it. The snap `D3-move-stabilizing-174` keeps its first name, and `D3-move-developing-174-renamed` follows it.

**Repairs (G7).** Repairs made no difference.
- P22: repaired rooms 0.943 accepted (420 lines), unrepaired 0.948 (362 lines).
- P12: repaired rooms 0.916 (537 lines), unrepaired 0.918 (440 lines).

**Carried to later groups.**
- **An arrow from a loss to recording, beside A08 (14 rooms).** It should be weighed with an order test against A10 and P10.
- **P12's records feeding P22's contests.** Records are used as proof or to test an account in DCFU, worldpowers, uwaterloo and fivenightsatfreddys.
- **P22's two forms for the clustering at D4:** accounts of the room's work and conduct (113 rooms), and the version of the canvas kept (71 rooms).
- **The host's moderation of records** goes with T4-002.
- **The re-check.** P22's status and range changed, so the rooms whose verdicts or local accounts rest on P22 go to the re-check (§5), with R01's and P05's.

**Disclosed limits and slips.**
- **Draws.** There were 10 seeded draws: two for P22 (verb offsets 546 and 646) and eight for P12 (170 to 870). None found an unsupported line.
- **The absent lines' reasons.** These were written by `_analysis/d3_absent_rulings.py` after every line was read whole. That script refuses any line needing a judgment (an evidenced absence, a non-portable line) that the map does not name. Each evidence-limit reason quotes the line's own concepts. A guard listed 80 lines whose labels share words with P22, and each was read again. One was moved to reject on its quote (foxes-034).
- **Counts by phrase** are over my own reasons, not over the members' words. A room may carry more than one pattern.
- **Images.** Many P12 lines rest on images not in the record. A picture of the finished work counts as a screenshot. A bare title during building counts as an evidence limit.
- **Slips.** My revise tool admitted a ninth move name (corrected above). The absent generator's first reason text named only G13, and I regenerated it to name G13a before writing.

## The field's entries

`out/sealed/FIELD.jsonl` names three tentative entries from C4. One line per id:
- **P22.** Instantiated in 153 rooms as returned (136 after ruling). Restricted in 75 rooms, none by an accepted correction (51 rooms' lines accepted as specification, 25 lines as evidence limits). Contradicted in none. Left absent in 521 rooms (495 evidence limits, 1 observed absence, 19 rejected because their concepts show it). Shown in 177 rooms in all. **Ruling: standing (rule 11), range rewritten; move 174, history lines 137 to 139.**
- **P21.** It belongs to a later group, and it stays tentative until that group rules it.
- **A21.** It belongs to a later group, and it stays tentative until that group rules it.

No entry stays tentative past the freeze.

### Close-check, D3a-06

`validate.py D3` reports 6,685 of 42,243 ledger lines ruled: R01's 709, P01's 1,021, P02's 1,070, P05's 1,092, P04's 1,034, P12's 977 and P22's 782. It reports 0 errors and 2 warnings. Both warnings are history lines 137 and 138, which name move 174 'stabilizing'. They stay as written, and line 139 records the correct name. All 81 pairs in P12's files and all 15 in P22's name a line of the same element (`_analysis/d3_pair_check.py`). The ledger holds 6,702 lines, 17 of them appended re-rulings across the legs. History holds 139 lines, elements 30 and arrows 21.

## D3a-07: K01, Keying (April Fools)

K01 stands alone in T4-001. Its statement reads: 'The host sub is keyed as play for April Fools: members post fakes and takeovers under the one-day licence, and a claim in it, a call to the canvas included, may be a joke.' Its range runs from one fake post in an ordinary sub to a sub given over to parody for a day and a half. It was cut at C5a-02 and restored at C5a-03, and no finding touches it. All 1,234 lines are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py` and from phrase counts over my own reasons.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 595 | 532 | 0 | 0 | 0 | 15 | 48 |
| absent (297 `unobserved`, 24 `not-testable`) | 321 | 0 | 0 | 0 | 320 | 1 | 0 |
| add-step | 196 | 35 | 146 | 0 | 11 | 4 | 0 |
| restrict | 67 | 49 | 0 | 0 | 18 | 0 | 0 |
| add-condition | 50 | 2 | 44 | 0 | 4 | 0 | 0 |
| link | 5 | 2 | 2 | 0 | 1 | 0 | 0 |
| all | 1,234 | 620 | 192 | 0 | 354 | 20 | 48 |

K01 is shown in 352 of 705 rooms (an accepted specification or elaboration). In 339 of them an instantiate line is accepted.

**What the accepted instantiate lines show.** By phrase count over the 532 reasons (a line may carry more than one form):
- **Fakes posted or run in the room: 268.** These include fake news, fake releases, bait, hoaxes and rickrolls.
- **A takeover or restyle of the room: 202.** The room's name, banner, style, rules, front page, bot or chat was taken over.
- **A claim doubted or tested as a joke: 110.**
- **The licence named for what a member posts: 17.**

98 lines sit at K01's lower range: one fake, a named licence, or one doubt. The upper range holds whole rooms given over to another game, club or university for the day. Examples are uoft and uwaterloo swapping rooms, greenbaypackers' one-name front page, and totallynotrobots' day-long pretence. In 16 accepted lines, a canvas call or canvas work sits beside the play and is kept apart from it.

**Restrict and add-condition: no correction.** The 67 restrict and 50 add-condition lines mostly say that the April Fools frame stayed local and that canvas calls were meant. K01 says only that a claim 'may be' a joke, so under G9 these lines correct nothing. They are specifications where they show the play, evidence limits where they do not, and paired elaborations where a second room shows the same condition.

**The 192 elaborations, by family** (all paired; the counts are lines, then rooms):

| family | lines | rooms | examples |
|---|---|---|---|
| a claim tested as a joke, or a literal reading repaired by the date | 33 | 29 | AMD-040, kpop-021, mariokart-010 |
| the licence bounded, policed or contested; the jokes judged | 28 | 26 | bostonceltics-026, stargate-055, rush-044 |
| the play's end marked, or the play outlasting its day | 22 | 21 | MMA-047, dankmemes-059, rwby-047 |
| the takeover resisted, resented or switched off; its cost | 15 | 13 | chelseafc-049, nbaspurs-027, worldoftanks-048 |
| the frame kept to its posts; canvas calls and work kept apart | 12 | 12 | 2007scape-045, HomestarRunner-041 |
| a fake as the premise of sincere talk; play and sincere talk interleaved | 12 | 12 | dallasstars-041, heroesofthestorm-056 |
| doubt about the day costs a real claim or call its uptake | 9 | 9 | chicago-046, cardinals-040, reddevils-030 |
| the takeover's rules enforced or lived inside | 9 | 8 | zelda-031, kerbalspaceprogram-042 |
| the joke made, or wished, real | 9 | 9 | kanye-039, warframe-059, spacex-011 |
| interface access: the joke reaches only members whose device shows it | 9 | 9 | cfb-029, rwby-046, picturegame-002 |
| the frame carrying a sincere act or real activity | 7 | 7 | lego-034, criticalrole-054, gameofthrones-057 |
| the play reaching outside: votes, searches, other rooms | 6 | 6 | MMA-046, kerbalspaceprogram-044 |
| a joke taken for real misleads or harms; jokes marked | 5 | 5 | AMD-042, ethereum-032 |
| the play as a tradition, or kept on record | 5 | 4 | GuildWars2-055, survivor-056 |
| a prank's offence repaired | 4 | 4 | geometrydash-045, stargate-056 |
| the play sending members to try what it featured | 4 | 4 | texans-030, zelda-034 |
| the play entering the canvas talk | 3 | 3 | undertale-046, polandball-007 |

Three pairs name a restrict line ruled specification: magictcg-034 with scotland-035, GuildWars2-055 with scp-046, and lego-034 with bisexual-050. The partner's evidence meets the same elaboration, but its own reading was K01 as stated.

**What the 48 rejects show.** All of them are instantiate lines. By phrase count:
- **19 show another room's or another source's prank, shared or reported.** Examples are argentina-034, liverpoolfc-043, megaman-047 and berkeley-022.
- **19 show joking that the record does not tie to the day.** Examples are Slovakia-024, portugal-053, Pigifs-013 and titanfall-046.
- **7 show a prank proposed, wished or planned, and not run.** Examples are Moondye7-029, gameofthrones-052, startrek-045 and philippines-029.
- **2 read the canvas as Reddit's event or make a joke call after it closed** (porterrobinson-048, pokemon-030).
- **1 recounts a family prank** (rangers-026).

**Absent lines.** None was rejected, and none records an evidenced absence. A guard listed 35 evidence-limit lines whose labels share words with K01, and each was read again. Most name the canvas as Reddit's April Fools event (DevonUK-038, msu-044). Others carry jokes, styling or 'fake news' that are not keyed to the room's own play: pgang-021's 'no bamboozles' is at hour 72.6, and soylent-032's 'anyone posting April Fools', at hour 77, means r/place posts.

**Particulars, 20.**
- **Failing portability (19):**
  - add-step: giivasunner-059, wine-043, zelda-032;
  - absent: eder-014;
  - instantiate: Pigifs-014, brasil-048, chess-023, counting-032, hearthstone-047, kirby-027, linux-049, marvel-029, minecraft-057, nin-039, rit-042, rotmg-030, slovenia-019, vim-029, worldpowers-044.
- **One room only:** worldpowers-045, where the April Fools frame is invoked to excuse overwriting another group's work, and members dispute it. A search of K01's lines found no second room.

**Re-ruled in this leg.** rotmg-032 moved from specification to reject by an appended line. Its offer, 'if this post gets 500 upvotes', is the site-wide meme that titanfall-046 and truestl-025 were rejected for, and nothing ties it to the room's takeover.

**No correction, so no §2 re-examination.** No restrict, add-condition or contradict line was accepted as a correction. K01 stands as served, and no move was made.

**Repairs (G7).** Repairs made no difference. Repaired rooms were 0.940 accepted (679 lines), and unrepaired rooms 0.951 (555 lines).

**Carried to later groups.**
- **K01's clause 'a call to the canvas included'.** Doubt reaches a canvas call in three rooms: geometrydash-046 doubts a call for help, cardinals-040 avoids the canvas as a prank, and chicago-046 ignores an invitation. In 28 lines (16 instantiate lines and 12 elaborations), the play is kept apart from canvas calls and work. This is a question for D4, not a correction: the statement says 'may be'. Whether keying lowers the uptake of calls (P01, A02) needs an order test.
- **The takeover's cost and its switching-off (15 lines) and interface access (9 lines).** These belong beside T4-002, the host's moderation, because most takeovers are the moderators' acts.
- **The play passing to other rooms and venues (6 lines), and swaps between named rooms.** These are relations between rooms, for the neighbour arrows (A04).
- **Doubt costing a real claim its uptake (9 rooms).** This is a mechanism K01's statement implies and no arrow carries.

**Disclosed limits and slips.**
- **Draws.** There were six seeded draws over the instantiate lines, at verb offsets 568 to 1068. Draw three (offset 768) found liverpoolfc-043 unsupported: its how names an April Fools takeover, and its quotes put the swap in r/soccer. That packet (instantiate lines 200 to 299) was read whole with every line's quotes. Lines 200 to 224, already ruled on their labels, did not change. The others found no unsupported line.
- **The shared-prank reading** was decided while I read instantiate lines 45 to 89. It was logged after their rulings were written, and a second diary line corrects the first one's wording.
- **The group close** tabulates rejects under the line's own kind ('specification'). The rulings store them with no kind.
- **A first phrase count** included the absent lines' reasons, which quote G14's clauses, and I discarded it. The counts above are over instantiate and elaboration reasons only.
- **Images.** Many lines rest on images not in the record. A fake whose words alone do not show it is a fake (diablo-016) is an evidence limit.
- **Compaction.** The context was compacted mid-leg. The head, the stage file and the diary were read again before any write.

### Close-check, D3a-07

`validate.py D3` reports 7,919 of 42,243 ledger lines ruled. That is the 6,685 ruled through D3a-06 and K01's 1,234. It reports 0 errors and 2 warnings, the same two as before: history lines 137 and 138, which name move 174 'stabilizing' (line 139 records the correct name). All 192 pairs in K01's files name a K01 line (`_analysis/d3_pair_check.py`). The ledger holds 7,937 lines, 18 of them appended re-rulings across the legs. History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561. None of those ledgers changed in this leg.
