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
- **G15 (logged at D3a-08, before P03's lines were ruled).** P03 is shown when a concept shows a member reporting to the thread the state of the room's mark during the event (before hour 73): what is placed, done or missing, and where. That covers:
  - a progress report (begun, outline in, half done, nearly done);
  - a report that the work is done (P03's 'done'; the celebration around it is P11);
  - a report of what is missing or still needed (a part, a colour, a row);
  - a report that a part is damaged or gone while the work stands (P05's watching at once, G11);
  - a screenshot or image posted as the work's current state;
  - a correction of another member's report.

  It is not shown by a call for hands that reports no state (P01), or by a layout or coordinates given only to lay out or locate the mark (P04, G12). A coordinate reported with the state of the work there shows both. Nor is it shown by a cheer or 'we did it' that reports nothing of the work's state (P11), by a report of the work's fate after hour 73 (P12, G13), or by a question about the state that no one answers. A report on another room's work does not show it, unless the room builds or keeps that work with them; then the line is a paired elaboration. Under G2, an absent line is rejected when its concepts show P03. P03 is not a universal claim, so its absent lines are never corrections. Two readings were stated while ruling and logged. Neither is an amendment; each says how a clause already written applies, and each was checked backwards.
  - **'Done' and the cheer** (stated at instantiate line 152). A celebration whose words state the work made, finished, done, complete or accomplished carries P03's 'done', and the celebration itself is P11. A bare 'we did it!' or a cheer does not. One line changed: bahrain-006 ('so happy that we made it!'), from reject to specification, by an appended line.
  - **Successor canvases** (stated at instantiate line 500, after G11's precedent). An instantiate line whose reports come from a successor canvas after hour 73 is a paired elaboration, not a specification (sadboys-012). A search of the earlier accepted reasons found no such line.
  - **G1b's draws.** One draw of ten lines per 100-line instantiate packet. A drawn line is unsupported when its quotes change the ruling that its how and labels would get.
- **G16 (logged at D3a-09, before P11's lines were ruled).** P11 is shown when a concept shows members marking a work of the room's as up or achieved, at any hour. That covers:
  - announcing that the room's work is on the canvas ('we made it onto r/place', a post or link showing the mark as the room's), which shows P03's lower range at once (G15);
  - celebrating it ('we did it', pride, congratulations, a final image posted as done, the work said to have lasted to the end);
  - crediting makers and helpers (thanks, makers named, disputes over who made it, prizes or points given for the canvas work);
  - a member claiming their own part ('I helped', 'I did my part', the pixels or hours given);
  - saying what working together meant, or what the work meant to the group (being seen, not being alone);
  - an invitation to celebrate the work offline.

  The room's own word is enough. P11 does not require that the work be verified, finished, agreed or still standing. It is not shown by a progress or state report with no marking (P03), or by a member's placing told as a step in a build still under way. Nor is it shown by a call or a prize offered to recruit (P01), by saving images or reporting the work's fate (P12), by contesting the version kept (P22), by carrying the work on (P13), or by praise of another room's work or of the canvas at large. A bare mention of the event, a joke reception, or a prize for something other than the canvas work does not show it either. Under G9, a restrict line corrects P11 only if its condition is one P11 does not state and the room's concepts show P11 failing without it. Three forms are paired elaborations, not corrections, because P11 does not say a room marks only what is up: marking where no work is up (the form A07's bound names), a find made by others that the room marks as its own, and marking disputed inside the room. P11 is not stated as universal (logged at the group's opening), so its absent lines are never corrections. G2 and G3 rule them. A concept may show P03 and P11 at once. Readings stated while ruling, logged and checked backwards, none an amendment:
  - **Credit disputes** (who made the work: members, another room, or scripts) are P11's crediting, so specifications (wine-022, flyers-055, utaustin-047).
  - **A damaged final work claimed with pride** is P11 as stated. The fond reading of the flaw is P12 and keeping the damaged version is P22 (G13a). The same flaw made the room's cheer, in a link, is an elaboration (chicubs-051).
  - **A celebration followed by renewed upkeep** is P11 as stated. The upkeep is P05's.
  - **'Done' against announcement** (stated at instantiate line 300). A report that the work is done shows P11 when it marks the work to the room: a post, a collective 'we', an exclamation of pleasure, or 'on r/place'. A bare reply stating the state shows P03 only (anime_irl-042 and VelvetUnderground-043, rejected). Checked backwards: no change.
  - **A work announced with no maker named** is the room's own, by C1's reading rule (Madeon-012, bdsm-011). The clause on finds made by others therefore applies only where a field names the other room, and then the line is P11's crediting. No line was ruled under it.
  - **Successor canvases.** Marking a work made on a canvas opened after hour 73 is a paired elaboration, after G11's and G15's precedent (catholicism-056, hungary-030).
  - **Thanks to a helper.** Thanks to the helper of a work that stands is P11's lower range even mid-build (catalonia-028). Credit named in a plan or call before the work is up is an elaboration (planetside-036, vocaloid-056).
  - **Dissent beside marking.** An instantiate line that shows P11 as stated beside one member's dissent stays a specification (4chan-060, portugal-060). The dispute is an elaboration only where it is the line's point.
  - **The contest.** Praise for spoiling a rival's mark is A15, not P11 (sabres-030, rejected).
  - **Marking where no work is up (amendment, 18 October, D3a-13; J, QD3-007; applies backwards).** A07's bound is read in its own words: the close cut the work unfinished, and the room marks the attempt. Such a line names A07. Marking an attempt in any other case is a paired elaboration of P11 that no statement holds: a work lost, erased or given up before the close, a part left after the goal failed, or a plan stopped with no work placed. The sentence above that calls the family 'the form A07's bound names' is superseded. J leaned to stating the wider form in P11's own statement. I judged it better to keep the element and the bound as they are, for three reasons:
    - T4-026 is declared a completion ritual over 522 rooms, so the revision would need that construct amended too.
    - No line shows P11 failing; the family adds a form beside the statement.
    - A family of about 16 rooms is the subform level that D4's clustering weighs.

    The lines that rested on the wider reading are re-ruled by appended lines (section D3a-13).
- **G4a (amendment, 17 October, D3a-10; forward only).** It sets how an add-condition or add-step line is ruled when its condition or step already sits in the model. The D3a-10 blind check found rulings on such lines moving between specification, elaboration and particular.
  - **The element states it.** If the element's own statement holds the condition or step, the line is a specification, as G9 rules restrict lines.
  - **Another element states it.** If another element or arrow already states it, the line is a specification of its own element, and the reason names the other id. An example is P05's 'upkeep before growth' named in a P02 line. Such a line is not an elaboration, because it brings nothing new into the model.
  - **A counting rule.** If the condition is a rule for coding or counting rather than something members did, the line is ruled by its concepts alone.
  - **Nothing in the model states it.** If no part of the model states it and the room's concepts show it, the line is a paired elaboration where a second room shows it, and a particular where only one room does (G4, G6). The search for a second room is part of the ruling.

  It applies from D3a-10 forward and does not apply backwards. Earlier legs ruled some such lines as paired elaborations or particulars, and those rulings stand. I have asked J whether to apply it backwards (QD3-003).
  - **Backward (amendment, 18 October, D3a-11).** J answered QD3-003: 'Backward I would say.' The sentence above no longer holds. G4a applies backwards to every add-condition and add-step line of the closed groups (R01, P01, P02, P05, P04, P12 and P22, K01, P03 and P11). Each changed ruling is an appended re-ruling, and the earlier line stays in the ledger.
  - **What 'states it' means.** The relation the line adds must be stated: in the element's statement or range, in another element's statement or range, or in an arrow's connection, bound or mechanism. Another element naming the act alone does not state a link that no statement or arrow draws. This is how G4a was applied to P16, and the backward pass applies it the same way. A script handed to another room to run itself stays an elaboration, though P14 names scripts. Another room's bot set to keep the room's work is P14's range ('a shared bot holding several rooms' works'), so that line is a specification (RelientK-040 and spacexmasterrace-025, corrected at D3a-11).
  - **Link lines.** G4a as written covers add-condition and add-step lines only. At D3a-10 I cited it on P16's 33 link lines without an amendment, which was a slip. I asked J whether G4a should cover link lines (QD3-004).
  - **Link lines (amendment, 18 October, D3a-11).** J answered QD3-004: 'Amend G4a to cover link lines and apply it backwards to them as well.' A link line is a specification, naming the id, where the element's statement or range, another element's statement or range, or an arrow's connection, bound or mechanism already states the link it adds. A link that no part of the model states stays a paired elaboration with a second room, or a particular with one. The amendment applies backwards to the link lines of the closed groups, by appended re-rulings. P16's links were ruled this way at D3a-10 and stand.
  - **Instantiate and restrict lines (amendment, 18 October, D3a-12).** J, on the QD3-005 count: 'Extend G4a to the 16 instantiate and restrict lines and apply it backwards. Before ruling on A07's bound, set out your wider reading and the lines that rest on it; keep those as ruled until I decide.' G4a now covers instantiate and restrict lines. Where the element's statement or range, another element's statement or range, or an arrow's connection, bound or mechanism already states the form the line shows, the line is a specification of its element, and the reason names the id. Backwards, the amendment reaches the 16 lines the count found (`_analysis/d3_qd3005_count.jsonl`). The lines among them that rest on my wider reading of A07's bound keep their rulings until J decides (section D3a-12). I read the extension as applying forward too, to the groups still to rule, and I have asked J to confirm it (QD3-006). Corrections, particulars by construction, evidence limits and rejects stay outside the amendment, for the reasons given with the count.
- **G17 (logged at D3a-10, before P16's lines were ruled).** P16 is shown when a concept shows help passing between the room and another room, read from either room's record. That covers:
  - pixels given to another room's work, repair or defence of it, and help arriving from another room;
  - requests for help, made or arriving (a call to kindred rooms is also P01's);
  - barter of help for space, repair or defence (settled terms are also P08's);
  - thanks to helpers and the story of an alliance (also P11's credit where the help went to the room's work);
  - greetings, compliments and condolences between rooms;
  - the room's work taken into a neighbour's work;
  - refusals, including the general canvas requests that reach a room.

  Delivery need not be verified, and one member's help is in the range. Another community's chat or group counts as a room. P16 is not shown by borders or deals that are not about help (P08), by sparing or apology (P07), by attacks (P09), or by forming an alliance as such (P17). Nor is it shown by a call to the room's own members only, by a proposal inside the room to ask with no request made, by a retrospective wish, or by help within one room. P16 is not stated as universal, so its absent lines are never corrections. Draws follow G1b, one per 100-line instantiate packet. Under G4a, an add line whose condition another element or arrow states names it: help from spare capacity once the room's work is safe (A13's order), help given before the room has a work of its own (A13's bound), asking because hands run short (A13's mechanism), a border opening help (A14), helpers' changes repaired away (P05's clause on keepers), help held to terms or withdrawn (P08), host rules (P20), signing or the designer's assent (P02), kindred calls (P01), alliances (P17) and the close at hour 73. Readings stated while ruling, each logged at its draw, none an amendment:
  - **Forms the add lines elaborate.** An instantiate line that shows P16 as stated stays a specification when it also carries a form the add lines elaborate (help aimed at a third room, help passed as a script), as with P11.
  - **Space yielded is P08's.** A neighbour moving its own work to settle a border gives no help (day9-013, rejected, as dota2-034 reads). A request for space alone is P08's (UPenn-018, an evidence limit).
  - **Joint work.** Work done together with another room is P16's (malaysia-053, araragi-011, borussiadortmund-023, ravens-036). The alliance it may come with is P17's.
  - **Taken in.** A request that another room take the room's work into its own is help asked, the adoption G17 counts (battlecats-028, hatsune-017, tetris-025). The guest's side is P19's, a candidate.
  - **Helpers outside the room.** Help counts where the words place the helper outside the room, though no room is named (evedreddit-016, riskofrain-022, gameboy-029). It does not count where the words do not (ghibli-025, a partner moving a figure of the room's own subject; baylor-022, Mario-021). A bare greeting from a visitor who names no room carries no relation between rooms (ice_poseidon-064, rejected).
  - **Proposals to ask.** A member's 'we could ask' with no request made is not a request (gameattack-031, winnipegjets-025, zelda-020, rejected; vietnam-013, an evidence limit). A request reported made is one ('Done.', redpandas-025, lexington-019).
  - **Own damage undone.** Undoing the room's own damage on a neighbour's work is P07's restoration. An offer to repair the neighbour's work against any vandal is P16's (seahawks-028).
  - **Smaller forms.** A plan supplied by another room is help passed as a tool (eder-011). A warning to a neighbour under attack is help (swordartonline-012). A request made after hour 73 is still a request between rooms, though no help could follow on this canvas (sadboys-024).
- **G18 (logged at D3a-13, before P08's lines were ruled).** P08 is shown when a concept shows the room and another room talking terms about where their works meet or how each will treat the other's work. The talk may be by members, by an envoy, or in a chat, and it may be read from either room's record. That covers:
  - proposing or asking a border, a space, a truce, a ceasefire, a deal or a treaty (one offer or request with no reply is P08's lower range);
  - settling one: terms agreed, a line drawn, space granted or conceded by talk;
  - contesting one: disputing a border, refusing terms, or accusing the other room of breaking a deal;
  - holding each other to one: invoking or reminding of an agreed border or deal, complaining of a breach, or ending the agreement;
  - a member reporting to the room that such terms exist ('we have a treaty with them'), or asking members to keep to them.

  It is not shown by sparing a neighbour with no terms named (P07), by help or barter whose terms concern help only (P16; G17 counts terms that trade help for space as both), by an attack (P09), by taunts with no terms (P18), or by forming an alliance to defend each other (P17). Nor is it shown by locating the work by its neighbours (P04's landmark family), or by a member's report that neighbours exist. Candidates and tentative entries do not count as statements that hold a line under G4a. A host ruling guests by a standing regime (applications, votes, rules for guests) is P19's form, a candidate, so such a line is a paired elaboration. A dispute over who may commit the room to an agreement is P21's form, a tentative field entry, so such a line is a paired elaboration, carried to P21's group to be read again once P21 is ruled. A single request for space beside or inside another room's work, and its answer, are P08's terms as stated. Arrows that may hold an add or link line under G4a: A04 (keeping before border talk; its bound has late rooms asking for space first), A05 (a settled border before sparing), A14 (border talk before help), A17 (an attack call met by a truce or a deal) and A21 (tentative). P08 is not stated as universal, so its absent lines are never corrections; G2 and G3 rule them. Restrict and contradict lines fall under G9. Under G4a, as amended at D3a-12 and applied forward (QD3-006), instantiate and restrict lines whose form another statement holds are specifications naming it. Draws follow G1b: one draw of ten lines per 100-line instantiate packet. Readings stated while ruling, each logged when stated and checked backwards, none an amendment:
  - **Appeals with no terms** (stated at instantiate line 12; made exact at line 413). P09 names encroaching as an attack. So an appeal to another room to stop damaging or encroaching on the work is P07's 'appeal to attackers to stop' where it names no limit, place, condition or exchange and no settlement follows (CelticFc-012, iastate-020, portal-022). Where the talk names a limit or a place, or the other side agrees, moves or sets a limit, it is P08 (Clannad-011, colorado-016, haskell-017).
  - **Choices inside the room** that leave a neighbour room, with no talk to it, are P02 and P07 (Dorset-008, PinkUnion-018, ethoslab-012).
  - **Proposals to ask** (stated at instantiate line 111, as G17 reads them). A member's proposal inside the room to ask for space, permission or a treaty, with no request made, is not P08's terms. Ten lines were rejected under it, among them battlecats-029, catholicism-027 and fullcommunism-009. A request reported made is P08 ('Just posted in there').
  - **A host's answer** (stated at instantiate line 87; made exact at line 233). One request and its answer are P08's terms, whether the answer comes from a member, a moderator, a vote or an application to a host (albania-021, gamindustri-014, canucks-024). P19's form is the host's standing regime as the host's own record shows it.
  - **A lone placer** who speaks for no room is P05 and P07, not P08 (anaheimducks-029). Where peace is settled with the maker of a neighbouring work, and the record does not show whether that maker spoke for a room, the line is an evidence limit (uruguay-024).
  - **Joint marks** are P17's. They are P08 where the talk sets a border, a space or terms beside them (afip-017 rejected; FinalFantasy-022, cfb-016 and germany-013 accepted).
  - **Help traded for help** is P16's (falcons-033, nin-023, rangers-009, ufl-009, vegan-008, parrots-028). Help given on condition of non-interference is P08 (shishamo-008).
- **G19 (logged at D3a-14, before P07's lines were ruled).** P07 is shown when a concept shows restraint toward a work on the canvas that is not the room's own: the room or its members hold back from damaging it, or ask for that restraint. The work may be a neighbour room's, or a work whose room is not named. P07's statement names neighbours, but A16's connection and T4-015's prose ('refuse to cover others' work') count refusals of attacks on any room's work, so distance does not matter. The act may be read from either room's record, as G17 and G18 read help and terms. That covers:
  - sparing another's work: building around it, leaving its space, refusing to cover it, or choosing a site, size or design that leaves it (also P02 where the mark changes, as G18 reads choices inside the room);
  - declaring that the room means a neighbour no harm, or stating the room's norm against covering others' work;
  - asking the room's own members to spare a work, or arguing inside the room that covering it is wrong (one member's refusal is P07's lower range);
  - refusing an attack call, whether it comes from inside the room or from outside it (a streamer or another room);
  - reining in the room's own attackers: telling members to stop or not to retaliate, condemning their attack to the room, or a moderator's rule or removal against raids (also P20 where it removes posts by rule);
  - apologising for damage the room or its members did to another's work, at any hour, including damage done by mistake;
  - restoring a work the room damaged (P07's upper range; G17 reads undoing the room's own damage the same way);
  - appealing to placers or to a room to stop damaging or encroaching on a work, or not to cover it; one plea is the lower range, and a plea written on the canvas counts. Where the appeal also names a limit, a place, a condition or an exchange, or a settlement follows, it shows P08 at once. G18's reading on appeals sets when an appeal also shows P08; it does not take the appeal out of P07. (Corrected before any line was ruled: the first wording, 'with no terms named', would have excluded such appeals from P07.)

  It is not shown by:
  - terms talked between rooms with no restraint asked or shown (P08): a request for space for the room's own work, a deal, or a report that a treaty exists. A room sparing a work by a settled border, or a member reminding others of the border, shows P07 and P08 at once (A05's mechanism);
  - help given to another's work: pixels, repair against vandals, or defence (P16; seahawks-028);
  - the room keeping its own work: watching, repair or defence (P05). A plea to the attackers beside it is P07;
  - an attack, a call to attack, or an argument for covering (P09);
  - a taunt, a salute after the fight, or a claim of victory (P18);
  - an alliance as such (P17);
  - working out who damaged a work, or saying that a placer does not act for the room, with no apology, call to stop or condemnation (P06's form, a candidate);
  - restraint inside the room's own work, praise of a neighbour's work, or a member's report that neighbours exist.

  P07 is not stated as universal (logged at the group's opening), so its absent lines are never corrections. G2 and G3 rule them. Restrict and contradict lines fall under G9. Under G4a, as amended and applied forward (QD3-006), an add, link, instantiate or restrict line whose form another statement already holds is a specification, and the reason names that statement. The statements that may hold such lines are:
  - A05: sparing that rests on a settled border (its connection and mechanism), and sparing that comes first and tacit, rests on a norm of the room, refuses a raid or apologises (its bound);
  - A16: the attack call before the refusal, reining in or apology (its connection); reining in that needs an attack, and tacit sparing before any call (its bound); a refusal with a reason that states the room's norm or the attack's cost (its mechanism);
  - A17: an attack call met by a truce or a deal;
  - P08 (holding each other to terms), P09 (encroaching, raids on a streamer's call, and scripts as attacks), P14 (the room adjusting its machine hands), P02 (a design changed), P10 (a move after a loss), K02 (the judgment of too few hands), P20 (the host's rules), C01 (a sanction as decided order) and P05 (upkeep, and the form the keepers know).

  Candidates and tentative entries hold no line (G18). So a member saying that the room cannot stop every placer shows P21's form, attribution shows P06's form, and an add line of either form is a paired elaboration. Sparing or an apology on a canvas opened after hour 73 is a paired elaboration, after G11's and G15's precedent. Draws follow G1b: one draw of ten lines per 100-line instantiate packet, at verb offsets from 254 (after 125 absent, 75 add-condition and 54 add-step lines). Readings stated while ruling, each logged when stated and checked backwards, none an amendment:
  - **Restraint toward talk is not toward a work** (stated at instantiate line 105). Restraint or an apology that concerns only a contest in talk is P18's domain, not P07's. Examples are trolling or raiding another room's threads, and a row in words. Lines rejected: babymetal-029 and worldpowers-025. Evidence limits: canucks-043, homestuck-061 and unitedkingdom-056. Checked backwards: WPI-014 (line 77) also carries an apology for a taunter, but it stands on c0050's apology and redirect.
  - **Calls not to provoke** (stated at instantiate line 157). A general call to the room not to provoke or antagonise other rooms is P07's lower range (colorado-017, dbz-013, uofm-020). The absent line ProfessorLayton-029 was rejected under it.
  - **Smaller forms of the apology.** An apology from a placer who altered the room's work is P07's lower range, as G18 reads a lone placer (day9-028). An apology for a mistaken accusation is P06's form, not an apology for damage (japan-021, which stands on its border kept).
  - **Smaller forms of sparing.** Another room that withdraws its push to change the room's work shows restraint (katawashoujo-007). Relocating to leave another group's work, with no loss before it, is sparing, not P10 (foxstevenson-019; the absent lines OKState-021 and superman-022 were rejected). Restraint whose stated reason is that the room cannot win is sparing, with the attack's cost as the reason (mizzou-008, halo-012, hearthstone-027, MMA-025).
  - **What is not restraint.** An instruction inside the room to message attackers, with no appeal shown made, is not an appeal, as G17 and G18 read proposals to ask (pusheen-008). A call for help, or help offered with no damage by the room shown, is P16's (sabres-020, denverbroncos-025, heroesofthestorm-061). An attack put off for tactics is P09's planning (nintendo-017).
  - **A refusal whatever its reason.** A refusal of an attack call counts whatever its reason. Where the reason is the flood of canvas posts, it shows P20 at once (england-018).
  - **Restoring elsewhere.** Restoring a work the room damaged includes rebuilding it elsewhere or giving its makers another space (uva-007, ss13-039, nVade-038).
  - **G4a on P07's add and link lines.** An act cut off by the close names P22, as earlier groups did (osugame-033, foxes-023). Restraint undone until it reaches the keepers, placers or scripts names P05's clause, as P08's agreements did.
- **G20 (logged at D3a-15, before P09's lines were ruled).** P09 is shown when a concept shows the room attacking a work that is not its own, or members calling for, planning, claiming or reporting such an attack. The moves are the ones P09 names: erasing or covering, encroaching on a neighbour's space by expansion, converting a sign or work into the room's own, raiding on a streamer's call, planting a script, and altering a work as a joke. One member's call is P09's lower range, and a call need not be carried out. Encroaching counts whether or not the room meant harm, since P09 names encroaching as an attack (as G18 read it). That covers:
  - a call, plan or proposal to attack, convert or take over another's work, with or without a target named;
  - members' reports or admissions of the room's own attacks, retaliation included;
  - expansion into a neighbour's work that members admit or are told of;
  - a joke alteration of another's work by members of the room;
  - scripts or bots set against others' works.

  P09 is the room's own repertoire. A15, A16, A17 and A18 each order 'the room's first call or act against another room's work', and T4-020's prose counts members attacking others' work. Help, terms and apologies are exchanges in which both rooms act, so G17 to G19 read them from either room's record. An attack is one room's act on another's work, so P09 is not read that way:
  - an attack the room suffers, reported by its members, is P05's watching or defence, or P12's report of the work's fate, not the room's P09;
  - a visitor's call, threat or claim of an attack on the room's work is P09 of the visitor's room; in this room's record it shows P09 only where the room's members join it;
  - a member griefing the room's own work is not P09, since P09's object is others' work.

  It is not shown by:
  - a call to the canvas or for hands with no attack (P01), or defence of the room's own work (P05);
  - a taunt, a claim of victory, or a contest in talk, including flooding or raiding another room's threads and brigading people off the canvas (P18; the reading G19 set for restraint);
  - lettering aimed at a rival that covers no one's work (P18's taunt);
  - restraint, refusal or apology (P07), or terms (P08);
  - a move away after the work is overrun (P10), or a design choice that covers no one (P02).

  An attack call made after hour 73, when no placement is possible, is talk about the canvas and an evidence limit for P09. One that aims at a canvas opened after hour 73 is a paired elaboration, after G11's and G15's precedent. P09 is not stated as universal (T4-020 counts 231 of 705 rooms), so its absent lines are never corrections. G2 and G3 rule them. Restrict and contradict lines fall under G9. Under G4a, as amended and applied forward, the statements that may hold an add, link, instantiate or restrict line are:
  - A15 (the call to the canvas before the attack call; its bound, an attack as the room's first canvas act);
  - A16, A17 and A18 (the attack before restraint, border talk and taunts, with their bounds and mechanisms);
  - C02 (a tie from before the canvas named in the turn that calls for or carries out the attack);
  - K01 (a call to the canvas that may be a joke);
  - P14 (machine hands), P08 (contesting or breaking terms), P05 (defence, and repair that restores the form the keepers know), P10, K02, P20 and C01.

  Candidates and tentative entries hold no line: K03's quarrel, K04's colour faith, P06, P19 and P21. Draws follow G1b, one draw of ten lines per 100-line instantiate packet, from verb offset 226 (after 169 absent, 35 add-condition and 22 add-step lines).
- **G20, amendment 1 (D3a-15, 19 October 2026; applies backwards to every P09 line).** Two changes.
  - **'Told of'.** It covers a neighbour's account of the room covering, encroaching on or attacking the neighbour's work, not expansion only. Members of the room need not answer. Where members deny the act and name other actors, the concepts leave the act open, and the line is an evidence limit (lovelive-009, paragon-055). A question that members deny shows nothing (bahrain-014).
  - **The statements G4a may name for P09** also include P22, for a call that meets or follows the close (the precedent of osugame-033 and foxes-023), and P04, for coordinates asked for and given for a raid's target.
  - **Applied backwards.** uiowa-009 (rejected) was re-ruled to a specification, and DevonUK-052 (rejected) to an evidence limit. The other 11 instantiate rejects that name a visitor or a claim were checked. Each concerns an attack on the room's own work, or an attack offer that no member took up, so none changes. The four non-absent lines that mention a denial rest on members' own calls or admissions, or on a denial of collective blame only (argentina-046, ainbowroad-045, landry-011, utaustin-058). No line ruled before this leg named P04 or P22 for P09.
- **G20's readings, stated while ruling (D3a-15).**
  - **Defence is P05.** Acting against what covers the room's own work is P05, the Void included (bindingofisaac-015, metalgearsolid-060, shishamo-009, texans-040, xcom-039, yugioh-066). A call to retake a spot the speaker wrongly thought was the room's is also P05's, and here it was withdrawn (titanfall-058).
  - **The Void.** A general call to attack the Void's black is P09 (pcmasterrace-073). A member who joins the Void shows P09 at its lower range (bindingofisaac-014, Jamaica-058, necrodancer-056).
  - **Visitors.** A visitor's attack offer or call that no member takes up is not the room's P09 (archlinux-040, colombia-028, hearthstone-065, kamenrider-024, pakistan-047, thepointing-020, ravens-055, rotmg-048, freedomplanet-038).
  - **The room's own work.** A work the room adopted is its own (portugal-068, the Squirtle). Members or placers altering it do not show P09 (chelseafc-063, day9-027, gatech-059, kirby-038, linux-064, polska-027). Neither do fandom play against the room's own proposal (transformers-023) or factions of the room contesting its own portrait (dota2-070).
  - **What covers no one.** A design aimed at a rival that covers no one's work is P18's taunt or P02's design (bostonbruins-038, DatBoi-052).
  - **The content's motive.** Erasing content the room objects to is P09's erasing (catholicism-023).
  - **K02.** A line that cites only K02's judgment does not show P09 (rotmg-047).
  - **The close.** A call made after hour 73 is an evidence limit on instantiate and absent lines (warthunder-068, samuraijack-035, wallstreetbets-059, mysterydungeon-040). On add lines it is a specification naming P22. An attack made during placement and recounted after the close is P09 (utaustin-057, zootopia-059). A picture of the canvas edited after the close is P22's contest over the version kept (torontoraptors-059).
  - **The means.** P09 names no means. A glitch's burst of pixels (cardinals-059) and a rival's own script turned on it (rit-057, named under P14) are means of moves it names.
- **G21 (logged at D3a-16, before P18's lines were ruled).** P18 is shown when a concept shows the room's members carrying a contest in talk with a rival group. The moves are the ones P18 names: a taunt or chant, flooding the rival's threads, a claim of victory, a salute after the fight, and blame of attackers after the close. One member's taunt is P18's lower range. A taunt need not be meant in earnest: a joking taunt or a mock war against a rival counts, and K01 holds that a claim may be a joke. That covers:
  - a taunt, insult, threat or chant aimed at a rival group, in the room's threads or the rival's;
  - flooding, raiding or brigading another group's threads, and calls to do so;
  - a claim of victory over a rival, and gloating at a rival's loss;
  - a salute, a 'GG' or respect paid to a rival after a fight;
  - blame of a rival for the room's damage after the close, as P18's statement names;
  - lettering or an image aimed at a rival that covers no one's work (G20's reading);
  - an apology, or a call to stop, for a taunt or a row in words, where the room took part in that contest. G19 sent talk-only restraint here, and it ends the contest as the salute does.

  The rival is another group on the canvas or around it: a sub, a nation's room, a school's or a team's room, a colour faction, the Void, or a streamer's audience. The contest must be part of the event: in a canvas thread, about the canvas, or aimed at the rival's work or presence there. A bare mention of the event holds no act (the C1 reading rule).

  P18 is the room's own part in a contest. A taunt is one group's act toward another, as an attack is, so P18 is read as G20 reads P09, and not as G17 to G19 read exchanges:
  - a visitor's taunt, flood or claim of victory in the room's threads is the visitor's P18; it shows the room's P18 only where members join the contest, by answering in kind or carrying it on;
  - an argument among the room's own members, with no rival group as a party, is not P18.

  It is not shown by:
  - an attack on another's work (P09), defence of the room's work (P05), a call for hands (P01), or terms (P08);
  - the old quarrel named with no tie to the canvas (K03's form, a candidate that holds no line);
  - celebration of the room's own work with no rival named (P11), or a record of the work's fate or mourning with no rival blamed (P12);
  - members objecting to canvas posts flooding the host sub (P20), unless a rival group floods it;
  - a correction of an account of the room after the close (P22), unless it also blames or taunts a rival.

  After the close, threats, war chants and victory claims against a rival are P18, since its statement reaches past the fight (mysterydungeon-040 was so read under G20). P18 is not stated as universal (T4-021 holds 116 of 705 rooms), so its absent lines are never corrections. G2 and G3 rule them, and G9 rules restrict and contradict lines. Under G4a, the statements that may hold an add, link, instantiate or restrict line are:
  - A18 (the attack before the taunt, and its mechanism: an attack makes the rival a named party);
  - C02 (a tie from before the canvas names the rival) and K01 (a claim may be a joke);
  - P09, P05, P07, P08, P11, P12, P17, P20 and P22, and the arrows A16 and A17.

  Candidates and tentative entries hold no line: K03's quarrel, K04's colour faith, P06, P19 and P21. Draws follow G1b, one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset.
- **G21, amendment 1 (D3a-16, 19 October 2026; applies backwards to every P18 line).** G21 said 'blame of a rival for the room's damage after the close'. P18's statement says 'blame attackers after the close', so the blame counts whoever the attackers are, one placer with many accounts included. Applied backwards: lines that blame one placer after the close and were ruled before the amendment was written were already accepted on that reading (ethereum-044, Rainbow6-058). Among the rejects and evidence limits that name one placer, one changes. berserk-065, an absent line, rebukes the placer of a Half-Life logo after the close ('You're really being *that guy*'), and is re-ruled from an evidence limit to a reject. The others stand: rojava-039 and gameattack-061 are a report and mourning without reproach, cavestory-040 is during the event, and egypt-052 does not concern an attacker.
- **G21's readings, stated while ruling (D3a-16).** They apply G21 as amended and change no rule.
  - **Blame during the event** counts when it insults, condemns, threatens or disparages the rival's conduct ('cucks', 'losers', 'greedy', 'hogging', 'get out!': 4chan-074, Dustforce-045, kuwait-040, GuildWars2-035). A plain report, a complaint about the room's own experience, or a defence call that names the attacker, even in war words, is P05's or P08's (Peru-055, clubpenguin-019, mechanicalkeyboards-015, nintendo-028).
  - **After the close,** P18's statement names blame of attackers, so explicit blame of a rival or of one placer counts ('I blame Poland', 'some jerk': soylent-043, nerf-036, KState-035). Mourning or a record that names the cause without reproach is P12's (TsundereSharks-035, counting-051).
  - **Victory claims.** A claim of holding off a named rival or the attackers is a victory claim (Slovakia-033, esperanto-021, NieR-062, PinkVomitMonster-024). A concession or an assessment with no jab is not (dbz-042, wine-059).
  - **Answering a visitor.** A sarcastic retort, a dismissive 'lol' or 'Nice try', or a mock-war refusal carries the contest on (WPI-029, donaldglover-039, hearthstone-068, futurama-017). A flat denial, a question or a polite justification does not (fivenightsatfreddys-072, landry-012, phish-059). A member who returns a visitor's salute takes part (harrypotter-060, de-042, paranatural-058).
  - **Refusals.** A refusal that mocks the rival counts (ManningPlace-054). A plain refusal to move is P08's (Cornwall-049).
  - **Rivals.** Taunts traded during the event with one individual do not count (PUBATTLEGROUNDS-056, parabola-015, parrots-059). Fans of rival teams or faculties in a shared sub speak for rival groups (alberta-048, portugal-069). A mock war between two subs that never names the canvas is outside the event (Pigifs-016).
  - **Venues.** Brigading a rival's posts or raiding its chat is P18's flooding (chelseafc-068, osugame-056, argentina-045).
- **G22 (logged at D3a-17, before P10's lines were read or ruled).** P10 is shown when a concept shows the room, after its work or its spot is erased, overrun or taken, weighing fighting for the spot against moving, or moving. The moves are the ones P10 names: a new spot, a smaller version, a fresh start. One member asking where to rebuild after a loss is P10's lower range. That covers:
  - a call, proposal or question to rebuild elsewhere, smaller or anew after the work is lost or overrun;
  - a weighing of staying to fight against moving, voiced after a loss, whatever the room then does;
  - a report that the room moved, shrank the work or started again after a loss;
  - a move by a coalition's or an ally's plan after the loss, as A10's bound reads MiamiHurricanes.

  The loss comes first, as P10's statement says ('After the work is erased or overrun'). So P10 is not shown by:
  - a site chosen or changed before any loss, for design or space (P02's choice, or P04's location), or a move by terms agreed before any loss (P08);
  - relocating to spare another group's work with no loss before it (P07's sparing, as G19 read foxstevenson-019);
  - repair or defence of the work in its place with no move weighed (P05);
  - giving the work up with no move weighed. F-019 reads that as the other outcome after doubt and a loss, not a move. It is K02's 'defenders told to give up' or P12's mourning;
  - a plan to rebuild on a later canvas after the close (P13's carrying on), since no placement is possible after hour 73.

  A visitor's suggestion that the room move is the visitor's request (P08); it shows P10 only where the room's members take it up after a loss. A move whose new spot is taken from another's work is P10 and P09 at once (P09's paired family, 'the place the room needs'). P10 is not stated as universal (T3-022 holds 116 of 705 rooms and T3-124 17), so its absent lines are never corrections. G2 and G3 rule them: a `not-needed` or `observed-absent` line is a specification where the concepts show that no loss called for a move, or that the room met a loss and did not move. G9 rules restrict and contradict lines. A correction of P10 must state a condition P10 lacks and show P10 failing without it. Corrections met twice at one node trigger §2, and F-019, which touches P10 through A10, would then be re-examined. Under G4a, the statements that may hold an add, link, instantiate or restrict line are:
  - A10 (doubt about hands or room before the move, its bound and mechanism) and K02 (the judgment itself);
  - P05 (defence and repair, the alternative a room weighs), P07, P08 and P09 (moves to spare, by terms, or onto another's work);
  - P01 and P03 (calls to rebuild and building the new work), P02 (design), P12 (the record of the loss), P13 (carrying on) and P17 (a coalition's plan), and P22 for acts cut off by the close.

  Candidates and tentative entries hold no line: P06, P19, P21, R02, K03 and K04. Draws follow G1b, one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset.
- **G22's readings, stated while ruling (D3a-17).** They apply G22 and change no rule. Each was logged when stated, and the first was checked backwards.
  - **A push given up** (stated at instantiate line 100, checked backwards). A room may give up its own push to take another group's spot because it cannot win, and build elsewhere. That does not show P10. The spot was never the room's, A10's mechanism speaks of a spot the room holds, and G19 reads such restraint as P07's. One accepted line changed: anarcho_capitalism-028, by an appended re-ruling. Later lines: gratefuldead-031, sooners-026, leafs-025, starcitizen-026, titanfall-037, greenbaypackers-027 and rpi-018.
  - **Hands moved to another work** (stated at instantiate line 150). A room may move its hands from a lost or overrun work to another of its works, to build or keep it. That is P10's move (GabrielDropout-031, israel-028, mylittlepony-022, FinalFantasy-036, ScottPilgrim-008; the absent lines australia-023, aromantic-022 and gorillaz-039 are rejected). Joining another group's work after a loss is help (P16), not P10 (kpop-030). Giving the work up with no other work or spot named stays F-019's other outcome.
  - **The close.** A plan to rebuild on the canvas made after hour 73 is an evidence limit on instantiate, absent and restrict lines (duckgame-020, duckgame-021, totallynotrobots-022), as G20's reading ruled calls after the close. On add lines it is a specification naming P22 (Dominican-035, enterthegungeon-033, paydaytheheist-012). A restart on a successor canvas is P13's, by G22's later-canvas clause (AcePlace-010).
  - **Overrun under way.** P10's 'overrun' covers a work being encroached, or an advancing work about to cover it (lego-015, furry_irl-021, berserk-027, metroid-026, necrodancer-027, vocaloid-053). It does not cover a guess about a future overwrite with nothing advancing (kanye-011), or a site judged too close to a roaming threat (haskell-015).
  - **Planned sites.** A site the room has not yet built on, taken or avoided, is a change of site (P04), not 'its spot ... taken' (singapore-037, palestine-018, chelseafc-041, UPenn-013, chibears-036).
  - **Moves before a loss in restrict and add lines.** A condition that would widen P10 to the moves G22 gives to P07, P08 or P04, or to giving the work up, does not add to P10. The line is then ruled by its concepts, as P09's dota2-070 was. No such line showed P10 failing, so none is a correction.
  - **A fresh start in place, or repair.** Rebuilding a work in its place after it was gone or taken is P10's fresh start (pepe-045, finland-020, lofihiphop-023, DCFU-011). Restoring a work that still stands, or retaking the spot by fighting, is P05 (starryknights-017, CSUFoCo-025, newzealand-023).
  - **A loss and a call not linked.** A loss and a later call may come from different members, hours apart, in different threads. The line is then an evidence limit (kirby-022, patriots-024, mechanicalkeyboards-017, shrooms-019, popheads-008). In one thread they are read together (wsu-020).
  - **What a weighing is.** Weighing a smaller version or a fresh design against defence is P10's weighing (ChronoTrigger-010, columbia-010, eesti-021). Giving the work up rather than rebuilding on others' space is not (paragon-009).
- **G23 (logged at D3a-18, before K02's lines were read or ruled).** K02 is shown when a concept shows a member of the room judging that the room has too few hands, or too little room, for a work it wants. The forms are the ones K02 names: doubt about the room's numbers, a canvas judged too full, and a work judged absent or outclassed. One member saying there are not enough people is K02's lower range. Defenders told to give up, because the work cannot be held, is its upper end. That covers:
  - a statement that the room lacks people, hands or numbers to start, build, finish, hold or grow a work;
  - a judgment that the canvas, or the space the room wants, is too full for the work;
  - a judgment that a larger group, a script or bots outclass the room, so the work cannot be made or held;
  - a judgment that the room's work is not on the canvas, or failed, because the room could not make or keep it;
  - a call to stop defending or to give up, given because the room cannot hold the work.

  The judgment must be stated. So K02 is not shown by:
  - a call for hands that states no lack (P01's call; 'we need more people' is K02 only where it says the room has too few for the work);
  - a report of damage or loss with no judgment of the room's hands or room (P05, P12);
  - a design or site sized small, or a time limit, with no judgment of hands or room stated (P02, P04);
  - doubt about something else: a design, a neighbour's intent, whether to attack (P02, P08, P07);
  - a visitor's judgment of the room's numbers, unless members take it up; or a judgment about another group's hands, not the room's own.

  K02 is not stated as universal, so its absent lines are never corrections. G2 and G3 rule them: a `not-needed` or `observed-absent` line is a specification where the concepts show that the room had the hands and room it needed, or met strain without judging itself too few. G9 rules restrict lines. A correction of K02 must state a condition K02 lacks and show K02 failing without it. Corrections met twice at one node trigger §2, and F-019, which touches K02 through A10, would then be re-examined. Under G4a, the statements that may hold an add, link, instantiate or restrict line are:
  - A10 (doubt before the move after a loss, its bound's early moves by choice, and its mechanism) and P10 (the move that may follow);
  - A06's mechanism (upkeep outruns one pixel per interval, and members turn to scripts) and P14 (machine hands);
  - P05 (defence under attack), P01 (calls for hands), P02 (a design sized to the room), P16 and P17 (help asked of others, alliances for hands);
  - P12 (mourning a failed work), P13 (trying again next time), and P22 for acts cut off by the close.

  Candidates and tentative entries hold no line: P06, P19, P21, R02, K03 and K04. Draws follow G1b, one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset.
- **G23, amendment 1 (D3a-18, 19 October 2026, before any K02 line was ruled; it applies to every K02 line, and no line was ruled before it).** G23's fourth clause said 'a judgment that the room's work is not on the canvas, or failed, because the room could not make or keep it'. K02's statement names 'a work judged absent' as a form of the judgment itself, with no cause added. The clause now reads: a member stating or lamenting that the room's work is not on the canvas (K02's 'a work judged absent'), or that a work failed because the room could not make or keep it. A question that only asks where the work is, with no lament or judgment, does not show K02. The amendment was prompted by GuildWars2 c0166, 'Why don't we have a quaggan in Place?', read while ruling the first packet.
- **G23's readings, stated while ruling (D3a-18).** They apply G23 and change no rule. The first five were logged when stated. The last three are written here at the close, from the rulings that applied them.
  - **The close.** A judgment made on a successor canvas after hour 73 is an evidence limit (AcePlace-024), as G20's reading ruled acts after the close. On an add line, a judgment voiced after hour 73 about the event's canvas is a specification naming P22 (nuclearthrone-032), as P10's Dominican-035 was.
  - **Absent or lost.** A lament that the room never got a work up is K02's 'work judged absent'. A lament for a work that stood and was lost is P12's mourning, unless a lack of hands or room is stated (afip-002 and pusheen-029 against counting-002).
  - **Calls** (refined at instantiate line 300 and checked backwards). A call that states the size of the shortfall, a consequence of it or a doubt says the room has too few for the work, so it shows K02 (luciomains-021, placestart-034, mordhau-003). A bare exhortation is P01's call (VelvetUnderground-002, neu-032, sakuragakuin-008). babymetal-003 was re-ruled from reject to specification by an appended line.
  - **A count is not a judgment.** A count of helpers, a joke about the sub's size or a quip on the timer is not K02 (hentai-002, buffalo-002, cgpgrey-006).
  - **Time under the timer.** Time left, weighed against the placements a work needs, is a judgment of the room's hands (satania-010, naruto-003, redpandas-005).
  - **Strain in holding.** A member stating that even the present work is hard to keep is K02's lower range (oneplus-005, metalcore-002, mcgill-033). Fear of a neighbour with no judgment of the room's strength is not (anime_irl-039).
  - **Giving up.** A call to give up, or one member giving up, shows K02 where it states why the work cannot be held: a rival judged stronger, bigger works crowding it out, or the fight declared over (twitch-006, wales-027, wine-006, apocalypserising-052). A bare 'give up', or giving up with only the loss as the reason, does not (rutgers-007, alberta-013, math-025, twitch-003).
  - **Statements under G4a.** The list above names the statements expected to hold K02's lines. G4a's clause 2 lets any standing statement hold one, as P10's lines named P04 and P16, which G22's list did not name. K02's add lines named P04 (ghibli-014, starlightstage-002) and P07 (asktransgender-005). G23's own exclusions already give those statements a site choice and sparing.
- **G24 (logged at D3a-19, before P14's lines were read or ruled).** P14 is shown when a concept shows a member of the room adding placements by machine, or the room arguing over such placements or adjusting them. P14's statement names scripts, bots and spare accounts. T4-009, the theme it rests on, also names glitches used to place more (T3-088). One member running spare accounts is P14's lower range. A shared bot that keeps several rooms' works is its upper end. That covers:
  - a member writing, sharing or running a script or bot for a work, or asking members to run it, whether the work is the room's or another's (a script planted in an attack is P14 and P09 at once);
  - a member placing with spare, alternate or throwaway accounts or a glitch, or lending accounts or machines to a bot;
  - rooms pooling one bot target;
  - members arguing whether scripts, bots or spare accounts are fair, taking a side on them or refusing them, whether the machine hands are the room's or others' on the canvas;
  - members switching off or updating the room's scripts, changing the target or template a bot follows, or editing a script to spare a neighbour.

  The act or the stance must be stated. So P14 is not shown by:
  - another group's script or bot reported as damage or as a strength, with no stance on machine hands and no act by the room (P09, P05, P12; a judgment that scripts outclass the room is K02's);
  - placing by hand: shifts, staying up, a set time, coordination in a chat (P05, P01, P03), even where it works around the timer, since P14's statement names machine hands;
  - a template, an overlay or coordinates with no machine hands (P04);
  - a bare mention that bots exist on the canvas, with no stance;
  - a visitor's script, accounts or stance, unless the room's members take it up (the visitor rule);
  - a plan to run machine hands on a canvas opened after hour 73. That is P13's later canvas, and the line is an evidence limit, as G23's reading ruled judgments made there.

  Members arguing over the event's bots after hour 73 show P14's argument, since its statement sets no time on the argument. P14 is not stated as universal (T4-009's prose counts 236 of 705 rooms), so its absent lines are never corrections. G2 and G3 rule them: a `not-needed` or `observed-absent` line is a specification where the concepts show that the room built and kept its work with no machine hands and no argument over them. A stated refusal of scripts is an argument, so it shows P14, and the claim of absence fails. G9 rules restrict lines. A correction of P14 must state a condition P14 lacks and show P14 failing without it. Corrections met twice at one node trigger §2, and F-005, named in P14's evidence and A06's ground, would then be re-examined. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are:
  - A06 (upkeep under attack before the first script, its mechanism, and its bound: rooms that scripted the building or an attack from the start) and P05 (whose range names scripts among the forms of keeping);
  - P04 (the template a bot follows), P01 (calls to place) and P03 (posting the work's state);
  - P07 (sparing a neighbour), P08 (terms that set what a bot keeps), P09 (a script planted in an attack), P16 (a bot or accounts lent to another room's work) and P17 (coalitions);
  - K02 (a work judged outclassed by scripts), P20 (the host's line around canvas talk), C01 (a decided rule or sanction), P12 and P22 (records and contests after the close) and P13 (a later canvas).

  As G23's reading says, G4a's clause 2 lets any standing statement hold a line. Candidates and tentative entries hold no line: P06, P19, P21, R02, K03 and K04. Draws follow G1b, one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (569).
- **G24's readings, stated while ruling (D3a-19).** They apply G24's rule that the act or the stance must be stated, and change no rule. The first four were logged when stated. The last two are written here at the close, from the rulings that applied them.
  - **Proposals.** A proposal or request for machine hands that the room does not yet hold is not P14's act, so the line is an evidence limit ('Someone should mod that bot', 'If someone rewrites one of those scripts for us I will gladly run it'). A member who shares, writes or adapts a script, or puts their own spare accounts to the work, shows P14 whether or not its placements are verified ('Time to bring out the alts', 'I have a script that people can just run').
  - **Workarounds that do not place.** A glitch or timer trick that the room finds does not place (local display only, not registered, gone on refresh) adds no placement, so it is an evidence limit (argentina-013, kanye-016, nyjets-015). A tracker script that places nothing is not machine hands (python-015). A glitch that did place is P14's (Temple-060, furry_irl-011).
  - **Stances against reports.** Calling others' scripts cheating, unfair or no fun is a stance on machine hands, so it is P14's argument (falcons-017, stlouisblues-017). A report that another group's bots or accounts damaged the work, or a suspicion that bots are at work, is not (croatia-021, Honduras-011).
  - **A neighbour's machine hands.** A neighbour's script that keeps the room's work is P14's upper range when the room takes it up through a truce, an agreement or a credit (kingdomhearts-015 and -016, winnipegjets-014). A neighbour's offer that no member takes up is not (thailand-011, wow-009, linux-020, russia-006).
  - **Machine hands that place nothing.** Moderation bots, comment bots, template overlays and reference updaters are not P14 (futanari-016, shishamo-014, starryknights-008, touhou-016).
  - **Denials and pride.** A bare denial, or one member's report of not scripting, takes no side (halo-008, TeamYellowPlace-008). Pride in hand-made work, set against rooms that use bots, is a stance. So the two `observed-absent` lines fail (greyblob-012, theexpanse-017).
- **G25 (logged at D3a-20, before P13's lines were read or ruled).** P13 is shown when a concept shows members proposing, deciding or doing something to keep part of the room's temporary effort beyond the event. The forms are the ones P13 and T4-028 name. One member's wish to do better next time is P13's lower range. A canvas-born group announced to carry on is its upper end. That covers:
  - a later canvas: planning for next time, rebuilding on a canvas opened after hour 73, or declining to start again (T3-054 names the refusal too);
  - a new purpose for the sub or chat made for the canvas (T3-111);
  - the mark taken into the room's identity: banner, sidebar, flair, avatar, a running joke (T3-156);
  - a tie with another room carried past the canvas: crossovers, exchanges, sister rooms (T3-158);
  - the work remade elsewhere: games, models, fan art, wallpapers, prints, and the argument over selling them (T3-057, T3-131).

  A decision to keep something counts when it is made near the close or after it. It also counts when it is made while the room is still building, since A09's bound names a next canvas or an emblem planned during the build. The act or the proposal must be stated. So P13 is not shown by:
  - recording what happened: screenshots, timelapses, atlas entries, reports of the work's fate, mourning, the end marked (P12);
  - contesting which version of the canvas or the event is kept: a shared copy's cleanup, scars, corrected accounts (P22);
  - celebrating, crediting or saying what the work meant (P11);
  - placing, repairing or rebuilding on the event's canvas before hour 73, including a fresh start after a loss (P05, P10);
  - a bare mention that a later canvas exists, with no wish, plan or decision by the room;
  - a visitor's invitation to a later canvas or a tie, unless the room's members take it up (the visitor rule).

  P13 is not stated as universal (T4-028's prose counts 213 of 705 rooms), and many rooms' records stop at hour 73. So its absent lines are never corrections. G2 and G3 rule them: a `not-needed` or `observed-absent` line is a specification where the concepts show that the room ended its effort with nothing carried on. A stated refusal of a later canvas is a decision about what to keep, so it shows P13 (T3-054), and the claim of absence fails. G9 rules restrict and contradict lines. Since P13 is not universal, a room that kept nothing does not contradict it. A contradict line must show P13's statement failing where its form is present. Corrections met twice at one node trigger §2, and F-003 and F-004, named in P13's evidence, would then be re-examined. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are:
  - A09 (the first record before the first act of carrying on; its bound, a next canvas or emblem planned while building) and P12 (the record carried);
  - P11 (marking and credit), P22 (contests over the kept version), P20 (the host's line around canvas talk and the canvas sub), P17 (coalitions during the event) and P16 and P08 (help and terms between rooms);
  - P02 (the room's design of its mark), P10 (a fresh start on the event's canvas) and K01 (the April Fools frame).

  G4a's clause 2 lets any standing statement hold a line. Candidates and tentative entries hold no line: P06, P19, P21, R02, K03 and K04. Draws follow G1b, one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (544).
- **G25, timing (amendment, 19 October, D3a-20; applies backwards to this group's lines).** While I ruled P13's restrict lines and read its add-condition lines, I found that G25's sentence on timing reads A09's bound more widely than its words. QD3-007 settled that an arrow's bound is read in its own words (A07's, under G16). I read A09's bound the same way:
  - **The bound's own words.** Where a room planned its next canvas or its emblem while still building, carrying on comes first. A line that shows a later canvas, or the mark as the room's banner, sidebar image, logo, flair or emoji, planned or made before the close, is a specification that names A09.
  - **Near the close.** P13's statement places its decisions 'near the close and after it'. I read 'near the close' as the canvas's last twelve hours, from hour 61 to the close at hour 73. I set this before I printed any line's hours. The statement and the bound separate decisions made near the close from plans made while building. The bound's own counterexample (texans, hour 34.5) is a plan made in the middle of the event. Twelve hours is the last sixth of the canvas clock.
  - **Other forms begun while building.** A tie with another room carried on, the work remade elsewhere, or a new purpose for the canvas sub or chat, shown only before hour 61, is held by no statement. Such a line is a paired elaboration of P13 where a second room shows it, and a particular where only one room does (G4a, clause 4). A line whose concepts also show P13's form at hour 61 or later stays a specification.
  - **Restrict and contradict lines.** A line that argues this timing shows no P13 failing. The family adds a form beside the statement, as P11's family did at QD3-007, so under G9 it is an elaboration, not a correction.
  - **What it supersedes.** The sentence in G25 that counts every decision made while building through A09's bound.
  - **Backwards.** I find the P13 lines already ruled on that sentence by their concepts' hours (`_analysis/d3_line_hours.py --after 61`). I re-rule them by appended lines, and the earlier lines stay in the ledger.

  No element or arrow changes. The family 'keeping begun while building' goes to D4's clustering beside A09's bound, as P11's family did at QD3-007.
- **G25's readings, stated while ruling (D3a-20).** They apply G25 and its timing amendment and change no rule. Each was logged when it was first used.
  - **Questions.** A member who asks whether the room should start again, or regroup elsewhere, raises a later canvas, so the question is P13's lower range (schoolidolfestival-054, OrderOfTheKoi-037). A question about what will happen, with no wish or plan, is an evidence limit (telegram-038, -039 and -040).
  - **Whose work.** P13 keeps the room's own effort. Another room's drawing remade in a game, or a remake that others made and a member only shares, is an evidence limit (animalcrossing-038, opticgaming-054). A remake of the whole canvas, the room's work included, counts (minecraft-050).
  - **Not canvas work.** Keeping the host sub's own April Fools changes (flairs, banners, bots, styling) is not keeping canvas work (starlightstage-065, anime_irl-045, smashbros-056). Neither is a member's drawing of the sub's older symbol (empiredidnothingwrong-056).
  - **Newcomers.** Newcomers welcomed, visitors invited into an older chat, or members asked to stay active in the host sub are T4-025's or T4-010's ground, not P13's (counting-048, re_zero-037, slovenia-060).
  - **The mark as it ended.** Damage that the room adopts into its identity (an official red dot, a typo sub, a damaged name) is P13 as stated, the mark taken into identity (cgpgrey-044, earthbound-041, trees-045). P22's range names scars kept as history. A member's own cleaned image of the work is P22's form, not P13's (denverbroncos-061).
  - **The host's line.** Host members objecting to canvas talk or to a canvas-born identity, and moderators removing a later-canvas post by rule, are P20's statement (maryland-035, partyparrot-044, pathofexile-051, darksouls-060).
  - **Selling and rights.** Arguments over selling the work remade, or over others' marks in the shared art, are P13 as stated through T3-131 (donaldglover-034, kanye-050, globaloffensive-058).
  - **Routes into P13 (links).** The close as the occasion, and a chat or sub made for the event and given a new purpose, are P13's own statement. A record before carrying on is A09's connection. Any other route in is drawn by no arrow and is a paired elaboration, as P12's 'recording entered from a loss' was ruled: canvas help or deals as the reason for a tie kept, marking with no record between, and a damaged end redone elsewhere.
  - **Steps after a later canvas.** On a later canvas the room calls, designs, builds, defends and loses work again. No arrow runs from P13 back into the spine, so these steps are paired elaborations (the spine restarted). R01's successor-canvas pair (AcePlace-029, TransFlagPlace-003) is the same form at the start.
- **G26 (logged at D3a-21, before P20's lines were read or ruled).** P20 is shown when a concept shows the host sub's moderators or members drawing a line between the sub's own business and the canvas. The forms are the ones P20's statement and T4-002's eight themes name. One member asking for a megathread is P20's lower range. Moderators moving all canvas talk to a new sub and removing the rest is its upper end. That covers:
  - routing canvas talk into a megathread, or asking for one (T3-015);
  - removing, filtering or flairing canvas posts under the sub's rules, and members asking about or contesting the removals (T3-063);
  - changing the sub's posting rules around the canvas, and members arguing the change (T3-185);
  - pausing one of the sub's usual events for the canvas (T3-184);
  - moderators saying the canvas work is not the sub's, so members may go on but not in its name (T3-140);
  - opening a canvas sub, or asking for one, and sending canvas talk there (T3-090);
  - members objecting that canvas posts crowd out the sub's usual talk (T3-075);
  - members arguing whether the canvas, its fights or the time spent on it are worth anything (T3-037). A dismissal is one side of that argument. Praise counts only as a reply in such an argument; praise alone is marking (P11).

  The act or the stance must be stated. So P20 is not shown by:
  - moderation as such, with no line between the sub's business and the canvas: spam removal, ordinary rule enforcement, bans for other reasons (T4-002's 'mistaken for');
  - a rule change made only for the sub's own April Fools joke, with no word of the canvas (K01's frame);
  - calls, templates, plans or progress reports posted in a megathread or a canvas sub (P01, P04, P03). The megathread or the canvas sub is P20's; the building talk inside it is not;
  - a visitor's objection or dismissal, unless the room's members take it up (the visitor rule);
  - another sub's removal of the room's posts, reported in the room. That is the other sub's line, not this room's.

  P20's statement sets no time. So a dismissal of the canvas after hour 73 shows P20, although A20's mechanism does not reach it (F-010's bound, the transformers case). P20 is not stated as universal (T4-002's prose counts 274 of 705 rooms), so its absent lines are never corrections. G2 and G3 rule them: a `not-needed` or `observed-absent` line is a specification where the concepts show canvas talk carried in the sub with no line drawn around it. A stated objection, ruling or dismissal shows P20, and the claim of absence fails. G9 rules restrict and contradict lines. A correction of P20 must state a condition P20 lacks and show P20 failing without it. Corrections met twice at one node trigger §2, and F-010, named in P20's evidence and A20's ground, would then be re-examined. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are:
  - A20 (the first call before the host's first line; its bound: rules that remove the first call as it is posted, a canvas sub or megathread set up first, dismissals before the room calls; the arrow is partly constitutive);
  - P01 (calls), P03 (posting the work's state), P04 (templates and plans) and C01 (a decided rule or sanction);
  - K01 (the April Fools frame), P12, P22 and P13 (records, contests and a new purpose for the canvas sub after the close), and P16, P17 and P08 (other rooms).

  G4a's clause 2 lets any standing statement hold a line. Candidates and tentative entries hold no line: P06, P19, P21, R02, K03 and K04. Draws follow G1b, one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (453).
- **G26's readings, stated while ruling (D3a-21).** They apply G26 and change no rule. Each was logged when it was first used.
  - **Removals.** A removal shows P20 when the rule excludes a canvas post for its topic (off-topic, one game only, only teasers and album images). A removal for format alone, or under a general rule (title tags, flair, length, link form, account age, reposts, vote manipulation, low effort, an unnamed rule), is moderation as such (battlecats-046, dankmemes-028, paladins-056). A bare duplicate notice is a general rule. An explicit redirect of a canvas post into the canvas thread is routing (clashroyale-023 and lovelive-025, against overwatch-067; halo-004 was re-ruled to match).
  - **Canvas subs.** A sub made for the canvas has no business apart from it. So its founding post, its venues and its coordination draw no line (THE_R-004, AvoArmy-035, placestart-040). A canvas sub that names its host and the host's line around canvas talk shows P20 (theitalyplace-033). Its administrators disowning a members' separate project is T3-140 (epublica-032).
  - **Stickies.** A stickied canvas thread in a host sub, asked for, promised or made, is P20's megathread whatever its motive (bangladesh-021, lakers-045). A sticky inside a canvas sub is coordination (ManningPlace-041). A megathread's contents are not the act of routing (hatsune-032).
  - **Chats.** Moving canvas talk to a chat shows P20 only where a line is stated: to spare the sub, or 'you are free to talk about it in there' (cavestory-027, nbaspurs-031). Otherwise it is T4-010's ground (bardmains-013, kanye-015).
  - **Worth.** One member's dismissal is P20's lower range, 'bots are ruining the fun' included, with P14 beside it (shitredditsays-034, udub-030). Praise or appraisal alone is not, except as a reply in an argument (monstercat-030, splatoon-025; against 49ers-032, israel-018). Views on how to play or design the canvas are P02's or nothing (hunterxhunter-053, rainbowgrid-039). Refusing hand placing because of scripts is P14's (egypt-041).
  - **Other subs and moderators.** Another sub's line, discussed or reported here, is not this room's (btc-020). A host moderator acting in the room's own thread counts for the room (FederationPlace-031). Moderators ruling that canvas posts stay, unstickying a canvas thread, or reversing a canvas removal show P20 (acecombat-029, androidgaming-038, mylittlepony-048). Policing conduct inside a canvas thread, a banned member's posts, or rivalry insults is moderation as such (belgium-027, Okami-027, canucks-057).
- **G27 (logged at D3a-22, before P17's lines were read or ruled).** P17 is shown when a concept shows the room joining other rooms as partners: rooms that stand together beyond one deal or one act of help. The forms are the ones P17's statement and T4-018's five themes name. Two rooms agreeing to defend each other is P17's lower range. A council of kindred rooms holding a stretch of the canvas together is its upper end. That covers:
  - forming an alliance between rooms, proposing one, or acting on one, such as calling on allies by the alliance or defending an ally under it (T3-150);
  - meeting other rooms in a chat or channel shared by several rooms (T3-153);
  - gathering kindred rooms in a hub: a sub, thread or chat for several rooms of one kind (T3-013);
  - tallying kindred rooms' works: lists or maps of a group of rooms' works (T3-019);
  - making a joint mark: one work that two or more rooms design, build or claim together (T3-056). The same line may show P16's joint work (G17's reading).

  The act or the proposal must be stated. So P17 is not shown by:
  - one room's deal with a neighbour: a border, a truce, a non-aggression pact, space traded for help (P08);
  - help passing between rooms with no partnership named: pixels given, help asked, thanks to allies, greetings (P16);
  - sparing a neighbour (P07), or one room's rule over guests on its mark (P19, a candidate);
  - calls to kindred subs to place for the room's own work (P01);
  - the room's own chat (T4-010's ground), or a member visiting another room's chat to place for that room;
  - a visitor's alliance offer that no member takes up (the visitor rule).

  An attack made together by allies is P09 and P17 at once. A coalition formed on a canvas opened after hour 73 is a paired elaboration, after the successor-canvas precedent. A tie carried past the close is P13's. P17 is not stated as universal (T4-018's prose counts 146 of 705 rooms), so its absent lines are never corrections. G2 and G3 rule them: a `not-needed` or `observed-absent` line is a specification where the concepts show the room building and keeping its work with no coalition. An alliance, shared chat, hub, tally or joint mark shows P17, and the claim of absence fails. G9 rules restrict and contradict lines. Corrections met twice at one node trigger §2, and F-008, which holds A19's coalition order, would then be re-examined. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are:
  - A19 (the first upkeep before the first coalition; its bound: late rooms enter the canvas through other rooms; its mechanism: rooms facing the same threat defend each other's works);
  - P08 (terms), P16 (help), P07 (sparing), P09 and P18 (attacks and taunts made together), P01 (calls to kindred subs), P04 (templates shared across rooms) and P03 (posting the work's state);
  - C01 (a decided rule, a council's vote), P20 (a host's line) and P13 (ties carried past the close).

  G4a's clause 2 lets any standing statement hold a line. Candidates and tentative entries hold no line: P06, P19, P21, R02, K03 and K04. Draws follow G1b, one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (378).
- **G27's readings, stated while ruling (D3a-22).** They apply G27 and change no rule. Each was logged when it was first used.
  - **Alliances.** An 'alliance' whose only stated term is not to harm each other's work is P08's truce (GabrielDropout-024, indieheads-025, starvstheforcesofevil-030, traaaaaaannnnnnnnnns-021). An alliance with no stated terms, or with mutual defence or joint action, is P17's (dragonquest-034, nuclearthrone-022). An 'alliance' whose stated terms are help for restraint is P08's and P16's (tampabaylightning-017, as cowchop-014). Defence or upkeep given both ways between two rooms is P17's lower range (OneTrueEmilia-023, malta-018, teamcube-017). Protection given one way, by a host or a listing room, is P16's (evex-013; gatech-016's recognized-artwork status).
  - **Hosts and guests.** A tie in which one room's work lives on another room's mark or territory is P19's form, a candidate. With no alliance or partnership named by either side, it shows no P17 (hatsune-016, clubpenguin-018, rush-032, toolband-029). An alliance named and acted on with a host or a colour faction is P17's lower range, with P19's form beside it (farmcarrots-019, furry-033, rocketbeans-021, swordartonline-013, metalcore-027). A reading logged at instantiate line 150, that every r/placestart tie is P19's, contradicted the alliance reading. I withdrew it in the same leg and re-ruled metalcore-027 to match.
  - **Whose coalition.** P17's statement names the room as the one that joins. An alliance reported by visitors, or by makers of the room's work who came from another room, is that other room's (hearthstone-034, araragi-009; araragi-010 was re-ruled to match). A visitor's offer counts only once a member takes it up (flashtv-016 and lakers-036 against ufl-036).
  - **Proposals.** A proposal stated by the room's members counts, even inside the room, when it names a partner room or coalition (nintendo-021, redvsblue-030, gravityfalls-032). A call to cooperate that names no partner, or a claim of 'alliances' with none named, does not (purplecorner-023, toolband-029, gamindustri-023, seolhyun-019).
  - **Hubs.** Sending the room's work or talk to a hub of kindred rooms shows P17 (sooners-031, NovaScotia-017, sabres-021). The room's own chat or canvas sub does not (FederationPlace-013, satania-021).
  - **Tallies.** P17's lead clause and G27's governing sentence read each listed form as a way the room joins others. A comparison or count of kindred works after the canvas joins no one. So restrict lines that say so are specifications, not corrections (mcgill-019, nyu-025, sixers-023).
  - **After the close.** A pact proposed after hour 73 for later events is a tie carried past the close, P13's ground (ukplace-028; chibears-053 names P13).
- **G28 (logged at D3a-23, before P15's lines were read or ruled).** P15 is shown when a concept shows a member answering a call or a proposal with a short reply that joins, assents, reports their own part done or thanks, and that asks for nothing back. The forms are the ones P15's statement names. 'On it.' is its lower end and 'Did my part.' its upper end. A12 holds the order, a call before its answer, and the bare join as the usual form ('I'm in'). That covers:
  - joining a call for hands or for defence, an attack call among them ('I'm in', 'on it', 'count me in', 'I'll help');
  - assent to a proposal put to the room or to its members: a design, a plan, a move, a deal or terms ('sounds good', 'agreed', 'yes'). The proposal may come from another room, read from either room's record;
  - a member's report of their own part done, given in answer to a call ('done', 'placed mine', 'did my part');
  - thanks given in answer to a call, a proposal or an offer: to the caller, the maker of a template or plan, or the one who offered.

  The reply may come from a visitor who answers the room's call in the room's thread (the visitor rule). A reply that gives a reason beside its assent still shows P15: the statement sets no bar on reasons, and A12 calls the bare join the usual form, not the only one. The answer must be written. Placing with no written reply leaves no line (F-023's bound).

  P15 is not shown by:
  - the call, the proposal or the plan itself (P01, P02, P04, P08);
  - a reply that asks something back: a question (where, which colour, how), a request for help or space, or a condition ('as long as ...', P08's terms);
  - a refusal, a doubt or a counter-proposal, the dispreferred answer (A12, A16), or a reply that argues;
  - a report of the work's state given in answer to no call (P03 alone), a cheer or a claim of one's part answering no call or proposal (P11 alone), or thanks to another room for help with no call or offer answered (P16 alone);
  - a long post that does more than the four acts named.

  A concept may show P15 with P03, P11, P16, P08 or P09 at once. P15 is not stated as universal, so its absent lines are never corrections. G2 and G3 rule them. An `observed-absent` or `not-needed` line is a specification where the concepts show calls or proposals in the room with no written answer, or only answers that ask something back or refuse. A written reply that joins, assents, reports a part done or thanks shows P15, and the claim of absence fails. G9 rules restrict and contradict lines. Corrections met twice at one node trigger §2, and F-023, which grounds A12, would then be re-examined. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are:
  - A12 (the call before its answer; the bare join as the preferred answer; its bound: never counted as an order, and most calls get no written reply);
  - P01 (calls), P02 (proposals of design), P03 (state reports), P04 (templates and plans), P08 (terms), P11 (credit and a member's own part), P16 (help and thanks between rooms), P09 (attack calls) and A16 (an attack call refused with a reason).

  G4a's clause 2 lets any standing statement hold a line. Candidates and tentative entries hold no line: P06, P19, P21, R02, K03 and K04. Draws follow G1b, one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset, which the first draw's header confirms.
- **G28's readings, stated while ruling (D3a-23).** They apply G28 and change no rule. Each was logged when it was first used.
  - **Thanks.** Thanks shows P15 when it answers a turn that gives the thanker something for the work: a call, a proposal, an offer, a template, a source, directions or a correction (anime-005, catalonia-030, cmu-012, masseffect-003). Thanks from the caller to those who answered, thanks for help already given, and praise or thanks for a finished work are P11's crediting (TheB1G-016, ElSalvador-004, colorado-003). Thanks to another room for help, with no offer answered, is P16's (apocalypserising-015, thailand-003). Thanks for an explanation of the event, a meme or routine business answers no call about the work (cowchop-024, linux-006, livecounting-052).
  - **A part done.** A member's own part reported in the room's build thread answers the thread's call (albania-012, aromantic-008, danganronpa-005). 'Done' or 'It's done!' in answer to a call or proposal is a part done (TheFarLeftSide-017, homelab-007, monsterhunter-004). 'Already done!' about a work made before the proposal, 'They did it' about others, and a collective 'we did it' are P03's report or P11's cheer (Madeon-007, startrek-003, eder-006, feedthebeast-003). A part claimed after the close, in a recounting or celebration thread, is P11's (anarcho_capitalism-007, hunterxhunter-008).
  - **Asking back and doubting.** A join in the same reply as a question, or beside a doubt about the room's space or hands, is not bare (CSUFoCo-007, parabola-011, bigbang-004). A condition that is only timing ('if i see it started') asks nothing of the proposer and does not bar P15 (GuardiansOfDatBoi-003). A note or remark beside the join that asks nothing does not bar it either (genderfluid-009, rojava-010; witcher-004's restriction was rejected).
  - **Assent.** Assent to terms, a deal or an offer is P15's, with P08's terms beside it, since the reply line asks for nothing (destiny-020's restriction was rejected). Assent to a cheer, a declaration or an announcement is not assent to a proposal (SydneyFC-037, thetreesnetwork-009). A proposer committing to its own proposal answers no one (buffalowizards-003).
  - **Who answers.** A visitor or a neighbour answering the room's call or proposal in the room's thread counts (Dorset-015, hearthstone-030, rhythmheaven-013). An organizer's welcome or thanks that closes the exchange does not (h3h3productions-065, carletonu-009).
  - **Later canvases.** An answer given in the thread to a proposal about a later canvas stays P15, with P13 beside it. P15 sets no hour, and the act is in the thread (aeskwadraat-018).
- **G29 (logged at D3a-24, before C01's lines were read or ruled).** C01 is a claim with two sides. Most rooms worked without deciding how they were organized, and a decided element of order appears in few rooms. A line instantiates C01 when a concept shows either side in the room. The forms are the ones C01's statement and T4-011's prose name. Members saying the room has no plan, no leader or no rules ('We just wing it') are C01's lower end. A colour faction holding elections is its upper end. That covers:
  - a decided element of order: a vote taken or a poll held on the room's work; a member put in charge, named or elected as leader, coordinator or officer; an office or role given; an oath taken or renewed; a sanction decided against the room's own members (a ban, an exclusion, a named list of the room's vandals); the work divided among named teams or members by assignment or agreement; the work handed over to named members;
  - members saying the room works with no plan, leader or rules, or declining to decide.

  The element must be decided or put to the room as a rule. A poll opened counts; a bare suggestion to vote that no one takes up does not. A member assigning a part to themself alone is not a division of the work. Decided elements count at any hour. After hour 73, P13's carrying on stands beside them where they set up a lasting group.

  C01 is not shown by:
  - a call for hands (P01), a design argued with no decision rule (P02), a template, coordinates or a plan (P04; A11, alignment without decision), or a state report (P03);
  - a member starting or leading the work by acting, with no one naming or choosing them (R01's starter, P04's planner);
  - the host's moderators drawing a line around canvas talk (P20), or a host's rule over guests alone (P19's form, a candidate). A vote or ban decided inside a colour faction or host shows C01, with P19's form beside it;
  - an agreement with another room (P08, P17), unless it decides the room's own order.

  C01 is not stated as universal: its own statement says most rooms did not decide. So its absent lines are never corrections. G2 and G3 rule them. An `observed-absent` or `not-needed` line is a specification where the concepts show the room working with calls, plans and reports and no decided element, which is C01's majority clause. A decided element of order shows C01, and the claim of absence fails. G9 rules restrict and contradict lines. A correction must state a condition C01 lacks and show C01 failing without it. F-006's bound already holds that votes and divisions of the work appear in rooms not placed on the theme, and that decided order gathers in colour factions and hosts that vet requests. Corrections met twice at one node trigger §2, and F-006 would then be re-examined. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are:
  - P01, P02, P04 and A11 (calls, design and templates; alignment without decision), R01 (the starter), P03 (reports), P20 (the host's line), P05 (keeping), P13 (carrying on), K01 (the April Fools frame) and P08 and P17 (other rooms).

  G4a's clause 2 lets any standing statement hold a line. Candidates and tentative entries hold no line: P06, P19, P21, R02, K03 and K04. Draws follow G1b, one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset, which the first draw's header confirms.

  **G29's readings, stated while ruling (D3a-24).** They read G29 and change no ruling rule.
  - **A division of the work.** It shows C01 when one member assigns another named member or team a part ('You connect the bottom of the E, I'll work on the top'). It also shows C01 when members agree to a proposed split, when squads, teams or shifts are set, or when the room's members are split by what they do, with a task for each ('The artist among you, need to do proper outlines'). It does not show C01 when a member takes a part and leaves the rest to others as they were ('letting random's work on keeping the interior fixed'). Parts taken unprompted, one order of work given to every reader ('focus on the bottom first, then the middle'), and a split offered as a question with no answer shown do not show it either.
  - **Officers.** A room's or host's moderators or officers show C01 when they decide for the room by their office. That covers an executive decision, an approval or refusal of the room's work, a ban, a rule, and a priority, strategy or plan they declare ('This will be the new plan for now'). Members saying that a decision belongs to the officers also show it ('mod team to decide whether we go to war or back down'). A request to the moderators with no decision shown does not. A moderator's sticky of a plan that someone else made does not, and an official plan whose deciders are not shown does not.
  - **Named leaders and roles.** Members naming someone by title (leader, commanders, diplomats, representatives, president, a coordinator team) show the decided side. Thanks for organizing, spearheading or 'leading the charge', and praise as a figure ('like a real leader'), credit a member who led by acting (R01, P04). A role that a member names for themself, with no one shown giving it, is not a decided element. Offices opened and not shown filled are not one either.
  - **Handovers.** The keeper of the work may pass the work, or control of it, to named members, to a named shift, or to the room as a whole ('I'm passing on this open source maintainership of these pixels to you the community', T3-187's own case). That shows C01. A member leaving for the night who asks 'somebody' to keep the work does not, and a designer leaving a draft for anyone does not.
  - **Votes and agreement.** A vote taken or opened counts whatever its subject, alliances included; the tie itself stays P17's. A post or comment that puts a choice to the room with its options opens a vote ('Let's take a vote. White or red?'). One member's 'I vote for' in talk does not, a suggestion to vote that no one takes up does not, and a vote planned for later does not. A decision that the room or its chat is said to have reached by agreement, consensus or majority names its procedure and shows C01 ('We at the discord have agreed to keep the white border'). A decision reported only as 'decided in the Discord' is T4-010's backstage decision and does not. Members coming round to one colour after an argument is A11's alignment, not a decision taken. A vote on a host's own ritual or jokes is not a vote on the room's work.
  - **Sanctions and entry rules.** A sanction shows C01 when it is decided against the room's own members over its canvas work or its order: vandalism, attack suggestions, speaking for the room, or a chat's security rule. An entry rule for the room's organizing venue (screening, entry by invitation) shows it too. The host's moderation of talk under its standing rules does not, and P20's removals and megathreads do not. Jokes of bans and ranks in play (K01) do not, and another room's sanctions do not. A sanction whose ground the record does not give is an evidence limit.
  - **The lower end.** It speaks of how the room is organized. Members say that it has no leader, no structure, no organization or no coordination, that it 'goes by itself', or that it should have organized and did not. Drawing without a template ('winging it from a gold pixel') speaks of the design, and does not show it. Permission to place anywhere does not, and talk of leaderless collective art in general does not. A call for a leader, alone, is a call.
  - **Restrictions.** Some restrictions state a condition that C01 never claimed: obedience, binding every placer, an appointment, or effective control. C01's statement holds them. A restriction saying that the record cannot show the order inside unseen chats is an evidence limit. A restriction that counts as decided order what G29 does not, or that denies what G29 counts, conflicts with G29 and is rejected.
- **G30 (logged at D3a-25, before C02's lines were read or ruled).** C02 is a claim about some rooms, and it is untested for order. Its statement reads: 'In some rooms, a tie the room had before the canvas (a league or school rivalry, a nation's history, an ideology, lore) names the rival in the same turn that calls for or carries out the attack.' A line instantiates C02 when a concept shows one turn that holds two things, as F-013's checks did. A turn is one post with its title, or one comment.
  - **An attack.** Members of the room call for, plan, claim or report an attack on another's work, by the moves P09 names (G20).
  - **A rival named by a tie from before the canvas.** The turn names the tie: a league, conference or school rivalry, a war or event from the nation's history, an ideology, or a fandom's lore. Or the turn names as the target a group that the room's community was set against before the canvas, so that the act rests on the tie ('turning the Cubs logo completely red'; 'taking over "no step on snek" ancap flag'). For a nation or an ideology, the words must carry the tie: the history, the enmity or the creed. A neighbouring flag named only as a target is the canvas's rival.

  The tie is the room's, as C02's statement reads since pass 11: members speak for their own community. Any hour of the event counts. An attack call made after hour 73 is talk about the canvas and an evidence limit, as G20 reads it.

  C02 is not shown by:
  - a rival made by the canvas (a neighbour, an attacker, the Void, a colour faction) named with no tie from before the canvas, which is F-013's `refuted_by` reading; such a line shows P09 or P18 alone;
  - a tie and an attack in different turns, since the claim is one turn;
  - a colour faction's faith naming its rivals (F-013's bound; K04's form, a candidate that holds no line);
  - an old quarrel named with no attack in the turn (K03's form, a candidate), including a taunt at an old rival that covers no one's work, which is P18 alone;
  - a visitor's attack call that names the visitor's own tie, which is the visitor's room's (G20's reading of visitors), unless members of the room join it;
  - an attack that the room suffers from an old rival (P05's defence or P12's report), unless members call for or carry out an attack back in that turn.

  C02 is not stated as universal: it speaks of some rooms. So its absent lines are never corrections. G2 and G3 rule them. An `observed-absent` or `not-needed` line is a specification where the concepts show the room's attacks or contests with no tie from before the canvas, or no attack at all, since C02 claims only some rooms. A concept that shows C02 makes the claim of absence fail. G9 rules restrict and contradict lines. A correction must state a condition that C02 lacks and show C02 failing without it. C02 claims no order and no share of rooms. So C02's untested status holds a restriction saying that the tie did not choose the rival, or that the rival was also the neighbour, where the rival is still one known before the canvas. Where the rival is only the canvas's, F-013's `refuted_by` holds the restriction, and the line shows no C02. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are:
  - P09 and P18 (the attack, and the contest in talk); A15, A16, A17 and A18 (the call to the canvas before the attack call, and the attack before sparing, border talk and taunts);
  - K01 (a call that may be a joke), P08 (terms), P17 (allies chosen by prior ties), P05, P20, P22 and C01.

  Candidates and tentative entries hold no line: K03, K04, P06, P19, P21 and R02. Draws follow G1b, one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (544, after 540 absent and 4 add-condition lines), which the first draw's header confirms.

  **G30's readings, stated while ruling (D3a-25).** They read G30 and change no ruling rule.
  - **The tie names the rival** when the target stands in the tie from before the canvas. The target may be a league, division, conference or school rival ('Lets destroy the celtics'; 'change usc to nd'; 'WIPE OUT ARIZONA ON r/place! B1G Only!'). It may be a nation that the room's history names: a war, a lost land, an occupation or a match (the Falklands, MH17, Transylvania, 'No Era Penal'). It may be an enemy of the room's creed (communists for ancaps, the_donald for anarchists), or a rival game, brand or fandom (League for Dota players, Monero for Bitcoin, Star Wars for Trekkies, Skyrim for Morrowind's fans). Naming such a target is enough. A reason given beside it, such as convenience or a canvas grievance, is held by C02's untested status.
  - **Lore or history that only casts a canvas neighbour** leaves the rival the canvas's, as F-013's `refuted_by` reads. Examples: the Finns as less Viking, the Greeks as Factorio's biters, Tesla as Talos, a furry logo as Fenrir, Poland as the invader in AMD's borrowed joke, and Norway as the foe at a new San Jacinto.
  - **The room's own tie.** The creed or politics must be the room's community's (r/anarchism, r/anarcho_capitalism, r/vegan, r/physical_removal). One member's own politics do not count (mylittlepony, furry). Borrowed labels do not count (dankmemes' Balkan memes, hentai's 7-1), and neither do the members' politics in a room made on the canvas (placesnek). A national room's crusade meme against Turkey is no tie of its own nation's (lithuania).
  - **Nations.** The words must carry the tie. A national target named alone does not show C02, even an obvious old enemy ('to show them who is boss'; norway's call to destroy the Swedes; Korea's calls on Japan's flag, with the history only in other turns).
  - **The attack.** Lettering aimed at a rival covers no one's work unless the rival's fans repair it (patriots). A joke wish, a contest named, a pun with no target, help to another room, defence of the room's work, and changes to the room's own work are not attacks.
  - **Visitors** who call for attacks in the room's threads carry their own tie (chicubs' Cardinals fan, greece's Lithuanian visitor, osugame's Ohio State poster).
  - **Kin ties.** A wider old tie can hold back an attack ('Hockey is family'; the kinship of Blizzard's games). C02's statement does not reach this, and the one add-condition line that names it is a particular.
  - **Draws.** G30 named verb offset 544 for the first instantiate line. The first draw's header showed 99 instantiate lines there, so the lines start at 545, and the draws were taken at 545 and 645.
- **G31 (logged at D3a-26, before P21's lines were read or ruled).** P21 is the field's tentative entry from C4a, in T3-126 under T4-016 (Negotiated order), dimension D04. Its statement reads: 'Members dispute who may commit the room to an agreement with other rooms: they say that one member's agreement does not bind every placer, deny that a treaty speaks for them, or ask another group for a leader to deal with.' Its level is between rooms, and a room shows its side in its own members' talk. P21 is shown when a concept shows members of the room disputing, or stating the limits of, who may commit the room to an agreement with other rooms. That covers:
  - a member saying that one member's agreement, or the room's, does not bind every placer, or that the room cannot stop everyone who places in its name;
  - a member denying that a treaty, deal or alliance speaks for them or for the room ('You don't speak for me'), or refusing an agreement that others made in the room's name;
  - a member disclaiming that their own word commits the room (speaking for themself alone, or for a part of the room);
  - members asking another group for a leader, a representative or someone who can speak for it, so that the room can deal with it.

  The room's side is read from its own members' talk. A visitor who asks the room for a leader, or who says that the visitor's own room cannot bind its placers, shows P21 for the visitor's room. In this room's record it shows P21 only where the room's members answer that no one can commit the room, or dispute who can.

  P21 is not shown by:
  - an agreement proposed, made, kept or broken with no dispute over who may commit the room (P08's terms), or a coalition (P17);
  - a member speaking for the room with no dispute (R02's envoy, a candidate), or a decided element naming who negotiates, such as 'contact the mods' (C01), unless members dispute it;
  - an attack the room suffers from an ally's or a neighbour's placers (P05, P12), unless members say that the other room's agreement cannot bind those placers;
  - restraint asked of the room's own attackers (P07), unless members say that the room cannot stop them.

  P21 is not stated as universal. So its absent lines are never corrections. G2 and G3 rule them. An `observed-absent` or `not-needed` line is a specification where the concepts show agreements made or kept with no dispute over who commits the room, or no agreement at all. A concept that shows P21 makes the claim of absence fail. G9 rules restrict and contradict lines. A correction must state a condition that P21 lacks and show P21 failing without it. The field's provisional part, that an agreement or coalition prompts the dispute, is A21's order and is not P21's claim, so a restriction about what prompts the dispute is held by P21's statement or is an evidence limit. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are:
  - P08 (terms) and P17 (coalitions), with A04, A14 and A19 (the neighbour talk that keeping brings, help that names a deal, and coalitions that cannot bind every placer);
  - P07 (restraint and reining in the room's attackers), P09 (attacks), P05 (keeping), P18 (the contest in talk), C01 (decided order), K01 (play) and P20 (the host's line).

  Candidates and tentative entries hold no line: R02, P06, P19, K03, K04 and A21. Draws follow G1b, one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset, which the first draw's header confirms. When P21's status is ruled, the lines of P21's form carried from the groups of P08, P07, P09 and P17 are read again under G4a.

  **G31's readings, stated while ruling (D3a-26).** They read G31 and change no ruling rule. Move 175 later rewrote P21's frame to match them (D3a-26's section, below).
  - **Visitors' own forms.** A visitor's disclaimer, apology for the visitor's own placers, or request for a leader shows P21 for the visitor's room. Here it is rejected (instantiate) or kept as a limit (absent) unless the room's members answer: AMD, Summit1G, ftlgame, masseffect, pcmasterrace, romania, skyrim, survivor, ukraine and belgium at instantiate; aggies, aoe2, armok, clg, costa_rica, feedthebeast, frankocean, hongkong, malta, pokemon, roosterteeth, twice and wales at absent. Members who answer a visitor's apology with the limit show P21 (littlewitchacademia, lifeisstrange, tagpro). So do members who answer a visitor's request by saying that their room cannot commit the placers in question (norway, asexual).
  - **Another room's limit, stated by the room's member.** It counts, because the room's own talk carries it (dallasstars, europe, gameofthrones, bindingofisaac, warframe and destiny at instantiate; TheHulk, COSI, stardewvalley, neu and eve at absent).
  - **No limit stated.** An agreement reported, assented to, breached or rebuked, with no limit or dispute stated, is P08's (ChronoTrigger, monsterhunter, mls; lebanon's breach and rebuke, placecanada's 'Too late', placesnek).
  - **The room's own design.** A dispute over the room's design, priorities, leadership, or the place where it decides is C01's family (darksouls; philippines-025 and thebluecorner-038 at add-step; furry, purplecorner, touhou, and ohio's consensus before telling a neighbour).
  - **Disowning.** It shows P21 when it is set against an agreement or a stated commitment, or when it says that the room cannot control the placers (bostonceltics, heroesofthestorm, placehearts, pepe). A bare disowning or apology, with no agreement named, is the apology's form and stays a limit (armenia, npr, vegan, pathofexile).
  - **Refusals.** Refusing an agreement already made in the room's name shows P21 (TheB1G, brasil, france, osu, prequelmemes, purdue, Thegreatblackhole). Refusing a proposal on its merits is P08's deliberation (eagles, starbound, uofmn, palestine, mordhau).
  - **Hedged standing.** 'I think I speak for the community' and the like show the disclaimer form (factorio, megaman, undertale).
  - **Whose space or art.** Sending a request to the owner of a space or an art is not P21 (rpi, runescape, truestl). Saying which room speaks for a flag's placers is (norway, asexual).
  - **Play.** A disclaimer made in play still shows the form (mysterydungeon: 'I had no authority to make that decision, but fuck it').
- **G32 (logged at D3a-27, before A21's lines were ruled; three instantiate lines, AMD-032, Goodboye-066 and Peru-029, were seen while I checked the packet's shape).** A21 is the field's tentative arrow from C4a, P08 → P21, of kind order. Its connection reads: 'in a room carrying both, the first agreement with another room (a border, a truce or a deal) comes before the first dispute over who may commit the room'. Its mechanism: an agreement made in the room's name puts the members' compliance in question; members who did not make it say that it does not bind them, or that no one can bind every placer, and the other side asks who can speak for the group. It fails if, in a room carrying both, the dispute comes only before any agreement, or answers no agreement. P21 is read as it stands after move 175, so a stated limit counts as its dispute. The agreement is P08's: a border, truce, deal or permission with another room, or an alliance made between rooms. A coalition's call alone is P17's.

  A21 is not stated as universal. Like the other arrows, it claims an order that is counted inside each room and reported as a count of rooms. So its absent lines are never corrections, and G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show an agreement with no P21 form, a P21 form with no agreement, neither, or a P21 form that comes before any agreement (the reverse order, which the order test counts);
  - a concept that shows an agreement and, after it, a P21 form that answers it makes the claim of absence fail (reject);
  - `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A21 when its concepts show an agreement with another room and, after it, a P21 form that answers that agreement. The order is read from the concepts' hours (`cite.py`), from the transitions, or from a quote that names the earlier agreement ('we did have an agreement. Some of the people there just don't want to honor it'). It is rejected when:
  - the P21 form comes before any agreement, or answers none;
  - no P21 form is shown (P08 alone);
  - the agreement or the form is a visitor's own room's and the room's members do not answer (G31's visitor clause).

  A restrict or contradict line is ruled by G9's test, read for an arrow. A correction states a condition that A21 lacks and shows the order failing without it in the room's concepts. One such condition would be a P21 form that arises while terms are still being proposed, before any agreement. A restriction whose condition the connection or the mechanism already holds (that the agreement binds placers who did not make it, or that the dispute answers it) is a specification. Two accepted corrections with the same target and the same lifted node at the third or fourth level trigger §2's re-examination in this leg.

  The order test is written and logged before it runs. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P08, P21, P17, A19, A04, A14, C01 and P07. Candidates and other tentative entries hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines for the 37 instantiate lines, from the instantiate lines' first verb offset, which the draw's header confirms.

  **G32's readings, stated while ruling (D3a-27).** They read G32 and change no ruling rule.
  - **At the making.** A qualification that the maker adds while proposing or accepting terms is at the making, not after an agreement ('We have a deal! I can't speak for every member', polska; 'I approve that, but people are uncontrollable', finland; 'I speak of my own opinion' four minutes after 'Agreed!', Goodboye). So are a request for a leader and a disclaimer made while a proposal is open (destiny, jerma985, TsundereSharks).
  - **A claimed or announced agreement** that a member then disputes shows the order: the claim comes first ('Yes, official' answered 'We can't say that', harrypotter; 'Permission from who?', winnipegjets; a claimed deal with r/Factorio, catalunya).
  - **Refusals.** As in G31, refusing an agreement already made shows the order (osu, TheB1G, counting); refusing a proposal on its merits is P08's deliberation (eagles, starbound).
  - **Whose agreement.** The agreement must bind the room or the room it deals with. A third room's truce invoked in a request (pepe: AFIP's truce) leaves the limit answering a request, not an agreement.
  - **Visitors.** As G31: a visitor's own limit after an agreement is the visitor's room's (aggies, aoe2, malta, cowchop), unless the room's members answer with it (littlewitchacademia, tagpro).
  - **Draws.** The draw at verb offset 607 held all 37 instantiate lines, as G32 expected.
- **G33 (logged at D3a-28, before any of A02's lines was read or ruled).** A02 is a standing arrow from C2, R01 → P01, of kind order. Its connection reads: 'in a room carrying both, the first proposal or start of a mark comes before the first call for hands'. Its mechanism: 'A member who proposes or begins a mark gives the room something to answer, and calls for hands gather around it.' It fails if 'calls in a room come only before any proposal or start, or a proposal draws no call'. Its bound: 'Where the room calls for hands before anyone proposes what to make, the proposal answers the call instead.' C2 counted it in 64 of 89 rooms carrying both (0.719; null mean 0.473, p95 0.539). R01 is read as move 172 left it: the starter proposes, maps or begins the mark, and others joining is not part of the role (G1a's claims of having started count). P01 is read as at D3a-02: the room calls its own members, or kindred subs, to place for a work, to start, build, finish or hold it (a call to defend is P01's hold form, G11).

  A02 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show a start with no call, a call with no start, neither, the bound's reverse order, or a joint opening (below);
  - a concept that shows a start and, after it, a call for hands for that mark makes the claim of absence fail (reject);
  - `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A02 when its concepts show a member proposing, mapping or beginning the mark and, after it, the room calling for hands for that mark. The order is read from the concepts' hours (`cite.py`), the transitions, or a call that names a proposal or a start already made. It is rejected when:
  - the first call comes before any proposal or start (the bound's pattern, counted in the census as the bound);
  - the start and the call are one post, a joint opening, with no later call gathering around the mark: the order cannot be shown, and the census counts the joint opening apart;
  - only one end is shown;
  - the start or the call is a visitor's room's own and the room's members do not take it up (the visitor rule).

  A restrict or contradict line is ruled by G9, read for an arrow, as under G32. A restriction whose condition the connection, the mechanism or the bound already holds is a specification. That covers a call before any proposal (the bound), and a start and call in one post (the connection already requires 'before'). A correction states a condition that A02 and its bound lack and shows the order failing without it. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  **G33's amendment (D3a-28, 19 October, logged after the instantiate lines were ruled and the restrict lines read, before any restrict line was ruled; applies to A02's restrict lines and forward, not backwards, since no line was ruled under the sentence it reads).** G33 says that a restriction held by the connection, the mechanism or the bound 'is a specification'. G33 rules restrictions by G9, and G9 reclassifies such a line by its concepts. So: a restriction whose condition the connection, mechanism or bound holds is not a correction. It is a specification where its concepts show the order, a joint opening with a later call around the mark, or the bound's pattern. It is an evidence limit (kind `none`) where they show only a joint opening. The reason is G33's own instantiate rule: a lone joint opening does not show the order. Nor does it meet A02's `mechanism_fails_if` ('calls come only before any proposal or start, or a proposal draws no call'). A joint opening therefore neither holds nor fails the order, and the census counts it apart. A restriction whose concepts show a start drawing helpers with no call meets that falsifier, and G9 rules it as a correction.

  The order test is written and logged before it runs: the census of the rulings by room (the order, the bound, joint openings, one end only), beside C2's count. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are R01, P01, P15 (joining as the answer to a call), P02 (settling what the mark shows), P04 (layouts), A01 (calls before building), A12 (pledges answering calls) and F-021 (a work up after the first call). Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset, which the first draw's header confirms.

  **G33's readings, stated while ruling (D3a-28).** They read G33 and its amendment and change no ruling rule.
  - **Starts in words.** A start told in the present tense is a start under way ("I'm making a she slime", dragonquest). A start announced for later is a joint opening ("Let's start an English flag", england; "i'm gonna start building", pcmasterrace; 'I will start with the top left pixel', coldplay). So is an instruction given with the call ('Jag börjar med en blå plupp och sen följer ni efter', sweden).
  - **Questions.** A proposal put to the room as a question is a joint opening ("Let's do a Cubs logo on r/place Who's in?", chicubs), as G10 read a call that names its picture.
  - **Defence calls.** A call to defend or repair a mark is P01's hold form. It shows the order when a member's start comes before it, or when the record credits a starter of that mark (bulgaria, apocalypserising, Peru, SwissNeutralityZone).
  - **Existing marks.** A call for a mark already on the canvas shows the order only where the record shows a member's start or credits a starter. Otherwise it stays a limit (DatBoi, DevonUK, AMD, buffalo, glasgow, hatsune, genderfluid, kilian, zelda).
  - **Different marks.** A start and a call for different marks do not show the order (ChronoTrigger, cirkeltrek, edmontonoilers, harrypotter, placehearts).
  - **Late or disputed claims.** A start claimed only after a call that names no existing mark does not show the order ('I started all this! No joke!' at h+26.14, after a call at h+2.66, EraseThePlace). Nor does a start that members dispute (afip).
  - **A successor canvas** is not this canvas (TransFlagPlace, kirby).
  - **Draws.** The draws at verb offsets 298, 398 and 498 held all 215 instantiate lines (100, 100 and 15). In the 30 lines drawn, every labeler's account agrees with its quotes.
- **G34 (logged at D3a-29, before any of A01's lines was read or ruled).** A01 is a standing arrow from C2, P01 → P03, of kind order. Its connection reads: 'in a room carrying both, the first call for hands comes before the first build report'. Its mechanism: 'The room's call brings members to the canvas, who then build the mark and say how far it has come.' It fails if 'in a room, build reports come only before any call, or calls are followed by no build report at all'. Its bound: 'Where a member has begun the mark before any call, the call follows the first build report and recruits to a mark already started.' After Stigmergy's recut, C2 counted it in 81 of 126 rooms carrying both (0.643; null mean 0.505, p95 0.571). Its counterexample response still names 53 of 190 rooms, a count from before the recut; that field is carried with the fields the prose rule did not read. P01 is read as at D3a-02, with its hold form (G11). P03 is read by G15: a member reports to the thread the state of the room's mark before hour 73 (what is placed, done or missing, and where).

  A01 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show a call with no build report, a report with no call, neither, or the bound's pattern;
  - a concept that shows a call for the mark and, after it, a report of that mark's state makes the claim of absence fail (reject);
  - `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A01 when its concepts show a call for hands for a mark and, after it, a report of that mark's state (G15). The order is read from the concepts' hours (`cite.py`), the transitions, or a report that answers the call. A report that comes after an earlier call counts, even when it also calls again (what is missing, and a call to place it). It is rejected when:
  - the first report comes before any call, or the first call itself reports what is already placed and recruits to it: the work was begun before the call (the bound's pattern, counted in the census as the bound);
  - only one end is shown: a call with no report after it, or a report with no call;
  - what follows the call reports no state: a join or a pledge (P15, A12, as the latin audit found), a cheer, or coordinates and a template given only to locate or lay out the mark (P04, G12);
  - the report comes after hour 73 (P12), or reports another room's work, or the call or the report is a visitor's room's own and the room's members do not take it up (G15, the visitor rule).

  A restrict or contradict line is ruled by G9, read for an arrow, as under G32 and G33's amendment. A restriction whose condition the connection, the mechanism or the bound already holds is not a correction. It is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A correction states a condition that A01 and its bound lack and shows the order failing without it. A restriction whose concepts show calls followed by no build report in a room that built, or calls that brought no one, meets A01's `mechanism_fails_if`; G9 rules it a correction where its condition is not already stated. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  The order test is written and logged before it runs: the census of the rulings by room (the order, the bound, one end only, other), beside C2's count. Since A02's census found that the first-concept test counts a same-hour pair as failing, the census also names how many bound rooms open with a call that reports a start already placed (A02's order). Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P01, P03, R01 (the starter), A02 (a start before the call), P15 (joining as the answer to a call), A12 (pledges answering calls), P04 (layouts), P02 (settling or extending what the mark shows), P05 and A03 (keeping after building), P11 (marking the work up) and F-021 (a work up after the first call). Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (286, after 273 absent and 12 add-condition lines), which the first draw's header confirms.

  **G34's readings, stated while ruling (D3a-29).** They read G34's bound clause and its restrict rule and change no ruling rule.
  - **Starts inside the call.** A call whose words report a start or progress already placed recruits to a mark already started: the bound's pattern. A start told in the present tense counts, as G33 read such starts ('We're trying to make a Moogle, kupo! Help at (272, 528)', FinalFantasy; 'Building the Monado in /r/place!', xenoblade_chronicles). The census counts these apart: they are A02's order inside A01's bound.
  - **Calls for placed marks.** A call to finish, repair, defend, extend or improve a placed mark recruits to a mark already started, in the bound's own words ('Get that r/place logo looking good', bostonbruins; 'We have a Monokuma head on r/place but our work is far from over!', danganronpa). A new figure beside a placed one is a new mark ('Who wants to help me place a Chrono's cat next to him?', ChronoTrigger).
  - **When a call opens its mark.** A call opens its mark unless its words, or the answer's, show the mark already placed. A bare 'Come help us on r/place!' counts as opening (denmark). 'Already' in an answer ('I have already begun on some work', fullcommunism) does not by itself put the start before the call.
  - **What a report is.** A reply that names what is placed or being placed is P03's report ('Working on the E.', cfb; 'I gave you my grey brick, right between duck eyes', duckgame). A bare 'I'm working on it!', 'ahi vamos' or 'O shit we did it', a pledge, or advice reports no state (G15). An edit on the call post that reports the work comes after the call (borderlands, geometrydash).
  - **Restrictions.** Most restrict lines say that the record cannot show which placings the call caused. A01's connection claims an order counted inside each room, so that condition does not make it fail. Where the concepts show the order, the line is a specification.
  - **The close and the plan.** A call met by the close ('The event is over unfortunately, r/place has closed.', chess) is held by P12's 'the end marked', with P03 read only before hour 73. A call answered by requests for a plan or coordinates is held by P04's statement (hearthstone, splatoon). A lone builder after a call is held by K02's statement (flashtv, frankocean).
  - **Draws.** The draws at verb offsets 286, 386 and 486 held all 276 instantiate lines (100, 100 and 76). In the 30 lines drawn, 15 hows claim more than their quotes show, so every packet was read whole.
- **G35 (logged at D3a-30, before any of A03's lines was read or ruled).** A03 is a standing arrow from C2, P03 → P05, of kind order. Its connection reads: 'in a room carrying both, the first build report comes before the first act of upkeep or defence'. Its mechanism: 'Once a mark stands on a surface anyone can change, keeping it becomes the work: a finished part is something to lose.' It fails if 'in a room, upkeep and defence come only before any build report, or a reported build is never watched or repaired'. Its bound: 'Where the room's mark was found already placed by others, or a rival attacked before the room reported building, upkeep comes first.' After Stigmergy's recut, C2 counted it in 148 of 190 rooms carrying both (0.779; null mean 0.340, p95 0.389). Its counterexample response still names 109 of 291 rooms, a count from before the recut; that field is carried with the fields the prose rule did not read. P03 is read by G15. P05 is read as move 173 left it, by G11: watching, warning that the work is changed, repairing, calling to defend (P01's hold form), covering the night, hardening or shrinking the shape, scripts set to keep, and upkeep put before growth.

  A03 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show a build report with no upkeep, upkeep with no build report, neither, or the bound's pattern;
  - a concept that shows a report of the room's mark and, after it, upkeep or defence of that mark makes the claim of absence fail (reject);
  - `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A03 when its concepts show a report of the state of the room's mark (G15) and, after it, an act of upkeep or defence of that mark (G11). The order is read from the concepts' hours (`cite.py`), the transitions, or an upkeep act that names a build already reported ('It's done!', then 'time for upkeep now'). It is rejected when:
  - the first upkeep or defence comes before any report of building: the mark was found placed by others, or attacked before the room reported building (the bound's pattern, counted in the census as the bound);
  - the report and the upkeep are one concept or one post, as G15 reads a report that the work is damaged (P03 and P05's watching at once), and no earlier report of building is shown: the order cannot be read, and the census counts it apart;
  - only one end is shown, or what follows the report keeps nothing (a cheer, a call to build more);
  - the report or the upkeep concerns another room's work, comes after hour 73 (P12), or is a visitor's room's own and the room's members do not take it up (G15, the visitor rule).

  A restrict or contradict line is ruled by G9, read for an arrow, as under G34. A restriction whose condition the connection, the mechanism or the bound already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a, as extended to restrict lines). A correction states a condition that A03 and its bound lack and shows the order failing without it. A restriction whose concepts show a reported build that the room never watched or repaired meets A03's `mechanism_fails_if`; G9 rules it a correction where its condition is not already stated. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  The order test is written and logged before it runs: the census of the rulings by room (the order, the bound, one concept holding both, one end only, other), beside C2's count. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P03, P05, P01 (the hold form), P11 (marking the work up), P02 (planned changes, which P05's statement names), A01 (calls before building), P09 (attacks), P10 and A10 (moves after a loss), K02 (too few hands), A06 and P14 (scripts), P16 (help), A04 (neighbour talk after keeping), P12 (the record after hour 73) and P13 (carrying on). Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (227, after 183 absent, 42 add-condition and 1 add-step lines), which the first draw's header confirms.

  **G35's readings, stated while ruling (D3a-30).** They read G35 and change no ruling rule.
  - **One post, report then upkeep.** G35's own example ('It's done!', then 'time for upkeep now', monsterhunter) is two posts by two members. A single post whose words report the work made, finished, complete or placed and then turn to keeping it shows the order too ('We have built the American flag. Now we must maintain it.', AmericanFlaginPlace; 'Done... Maintain', Russiaclan).
  - **The report end stays strict (G15).** A bare 'We did it!', 'Great job', 'Success!' or 'now we have to maintain it' reports no state of the work, so such a line shows one end. 'We made it' counts as made, as G15 read bahrain. A cheer with an image of the work counts as the image. 'Looks great' and 'looks pretty good now' describe the work's state and count.
  - **Damage first.** A first report that is itself damage or repair ('OK our flag is being destroyed Gotta fix that.', australia) is P03 and P05 at once, the class G35 counts apart (J). A concept that reports building or progress while damage happens ('Eagles being spelled while someone tries to mess it up'), followed by a later act of upkeep, shows the order; four lines were moved from J to the order by this reading before any line was written (belgium-037, eagles-039, ethoslab-036, europe-042).
  - **Upkeep before the only report** is counted with the bound (Peru, bakchodi, bisexual). A line that drops upkeep as too costly shows no act of upkeep (TheFarLeftSide).
  - **What counts as upkeep.** A pledge or plan to keep the work counts as P05's talk ('I'll protect it now', redpandas). A placer's own correction of a misplaced pixel is not upkeep against change (predators, stlouis). Keeping a border black to avoid angering a neighbour is P07's sparing, not keeping (kindafunny).
  - **Draws.** The draws at verb offsets 227, 327, 427 and 527 held all 380 instantiate lines (100, 100, 100 and 80). In the 40 lines drawn, 17 hows claim more than their quotes show, and two drawn lines are NONPORTABLE, so every packet was read whole.
- **G36 (logged at D3a-31, before any of A04's lines was read or ruled).** A04 is a standing arrow from C2, P05 → P08, of kind order. Its connection reads: 'in a room carrying both, the first act of upkeep or defence comes before the first border talk, truce or deal'. Its mechanism: 'Keeping a mark against erosion brings the room up against the neighbours whose pixels erode it, and the room turns to talk with them.' It fails if 'border talk comes only before any upkeep or defence, or upkeep against a neighbour never turns to talk with it'. Its bound names the rooms where border talk comes first: late rooms asking for space before they have a mark to keep, a work found already placed, a room entering through another room's offer, neighbours present from the first post, and, by two coders at C5, first border talk that mostly offers terms before any damage. C2 counted it in 235 of 401 rooms carrying both (0.586; null mean 0.501, p95 0.539). P05 is read by G11, as move 173 left it. P08 is read by G18 and its readings: talk of terms with another room about where works meet or how each treats the other's work; an appeal with no terms is P07's, help for help is P16's, an alliance is P17's.

  A04 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show upkeep with no border talk, border talk with no upkeep, neither, or the bound's pattern;
  - a concept that shows upkeep or defence of the room's mark and, after it, border talk, a truce or a deal with another room makes the claim of absence fail (reject);
  - `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A04 when its concepts show upkeep or defence of the room's mark (G11) and, after it, P08's terms with another room (G18). The order is read from the concepts' hours (`cite.py`), the transitions, or one post whose words name the damage or the defence first and then propose or ask terms ('We have to stop this takeover!', then 'Maybe we can arrange something with r/rarepuppers'). The talk need not be with the room that caused the damage. It is rejected when:
  - the first border talk comes before any upkeep: space asked before the room has a mark to keep, terms offered before any damage, a work found placed, or entry through another room's offer (the bound's pattern, counted in the census as the bound);
  - only one end is shown;
  - what follows the upkeep is not P08's terms: an appeal with no terms (P07), help traded for help (P16), an alliance (P17), an attack (P09) or taunts (P18);
  - the upkeep or the talk is another room's own and the room's members do not take it up (the visitor rule), or it comes after hour 73.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G34 and G35. A restriction whose condition the connection, the mechanism or the bound already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a, as extended to restrict lines). A correction states a condition that A04 and its bound lack and shows the order failing without it. A restriction whose concepts show upkeep against a neighbour that never turns to talk meets A04's `mechanism_fails_if`; G9 rules it a correction where no statement holds its condition (fighting on is P09's and P18's; moving away is P10's; sparing with no terms is P07's). Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  The order test is written and logged before it runs: the census of the rulings by room (the order, the bound with terms first, one end, other), beside C2's count and the C5 range. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P05, P08, P07, P09, P10 and A10, P16, P17, P18, P21, A05, A14, A17, A19, A21, K02 and P20. Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (318, after 280 absent, 35 add-condition, 1 add-step and 1 contradict lines), which the first draw's header confirms.

  **G36's readings, stated while ruling (D3a-31).** They read G36 and change no ruling rule. Each was logged before any line it touched was written.
  - **Proposals to ask.** G36 reads P08 by G18 and its readings. So a member's proposal inside the room to ask another room, with no request shown made, is not P08's terms ('We need to talk to them.', DestinyTheGame; 'Diplomacy is our only option now', adventuretime). Such a line is rejected and counted apart. A request reported made, or under way by its speaker, counts ('I have tried to contact them.', WPI; 'I'm going into their discord to talk to them', gameofthrones). G36's own example pair (unturned, 'We have to stop this takeover!', then 'Maybe we can arrange something with r/rarepuppers') shows the order of words. Its second post is such a proposal, as is adventuretime's, so both of A04's support transitions show upkeep followed by a proposal to talk.
  - **Damage inside the talk (J).** Where the talk names the damage only as its reason or condition ('We will let your half-zia remain as long as you tell your brethren to stop invading the spoked B.', bostonbruins), or the talk is itself the means of defence ('Selten so viele Verhandlungen geführt um 50 Pixel zu verteidigen.', Moondye7), and no act of upkeep comes before it, the order cannot be read. The census counts these apart, as G35 counted J.
  - **A complaint to the other side is talk.** A complaint or appeal addressed to the other room that names the damage ('Why are you harassing our work????', harrypotter; 'please stop destroying our last line.', uva) is talk, not keeping. G11's watching warns the room's own members. Applied backwards before any line was written, it moved harrypotter-022 from the order to J.
  - **A loss or a move in place of upkeep.** The room moves away instead of talking terms, or seeks a new place by talk after its spot is lost (archlinux, Dominican, furry_irl, malta). P10 and A10 hold these, and K02 where the room says it lacks hands (iastate).
  - **What counts as upkeep.** A call to defend or protect counts before any damage, as P01's hold form ('We must protect her at all cost.', hatsune). A warning that a neighbour approaches does not ('Looks like Finland is gonna eat us up later.', chibears; 'all day its been coming closer', masseffect), since G11's watching warns that the work is changed.
  - **The neighbour's terms.** A neighbour's terms after the room's upkeep show the order, since G18 reads P08 from either room's record (cavestory, giantbomb, uwaterloo). A visitor's post that names both sides' fighting and then offers terms counts ('we are both wasting time/energy/effort fighting over it', livecounting; TheHulk, where the room takes up the terms).
  - **One post.** A post whose words name the upkeep first and then report or propose terms shows the order (glasgow, lost, zelda among the absent lines; brasil, terraria and vocaloid among the instantiate lines).
  - **The first act of each.** A line whose concepts show both patterns is classed by the first act of each, as the connection counts them. The first talk before the first upkeep is the bound (RelientK-027, patriots-052, warframe-034).
  - **The room's own encroachment.** Talk that answers the room's own covering of a neighbour is A17's order (the room's act against another work before its border talk; encroaching counts as an attack, G20). A restrict or add line with no upkeep before such talk is a specification naming A17. Where an act of upkeep comes first, the line shows A04's order, with A17 named (austria, ravens, sheffield, vermont).
  - **Upkeep that turns elsewhere.** Upkeep that turns to a move or to sparing with no terms is held by P10 or P07, as G36 says (nyjets, funhaus).
  - **Draws.** The draws at verb offsets 318 and 418 held all 181 instantiate lines (100 and 81). In the 20 lines drawn, 6 show the order, and 3 hows claim more than their quotes show (clg-030, uiuc-025, monsterhunter-029). Every packet was read whole, with every cited concept quoted.
- **G37 (logged at D3a-32, before any of A05's lines was read or ruled).** A05 is a standing arrow from C2, P08 → P07, of kind order and strength thin. Its connection reads: 'in a room carrying both, the first border talk, truce or deal comes before the first act of sparing a neighbour'. Its mechanism: 'A settled border gives the room a line to keep: members spare the neighbour's work by it and remind others of it.' It fails if 'sparing comes only before any border talk, or a settled border is followed by no sparing'. Its bound: 'Sparing often comes first and tacit, before any talk; the arrow holds where restraint rests on a border already settled.' At C5c-09 every room carrying both was read: the first sparing names a border, truce, deal, policy or agreement in 17 of 124 rooms, so the mechanism is theorised (F-020, whose statement names A05). C2 counted the order in 106 of 158 rooms (0.671; null mean 0.600, p95 0.658). P08 is read by G18 and its readings, as G36 used them (a proposal to ask with no request made is not P08's terms). P07 is read by G19 and its readings: sparing, a stated norm, asking members to spare, refusing an attack call, reining in the room's own attackers, apologising, restoring, and appealing to stop; not help (P16), keeping the room's own work (P05), an alliance (P17) or attribution (P06's form).

  A05 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show sparing with no border talk, talk with no sparing, neither, or the bound's pattern;
  - a concept that shows P08's terms with another room and, after it, sparing of a neighbour's work makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A05 when its concepts show P08's terms with another room (G18) and, after them, sparing of that or another room's work (G19). The order is read from the concepts' hours (`cite.py`), the transitions, or one post whose words name the terms first and the sparing after. A sparing or a reminder that names a border, truce or deal already settled shows the order in its own words, since the settlement comes before the sparing it names; the census counts such lines apart, as the mechanism shown in words, beside C5c-09's 17 of 124. The sparing may be read from either room's record, as G19 reads P07: the room keeping off a neighbour, or the neighbour keeping a deal with the room. A line is rejected when:
  - the first sparing comes before any border talk: tacit sparing, a norm of the room, a refused raid or an apology first (the bound's pattern, counted in the census as the bound);
  - only one end is shown;
  - the first end is not P08's terms (a proposal to ask with no request made, help only, an alliance as such, an appeal that is itself the restraint) or the second is not P07 (help, keeping the room's own work, an alliance);
  - the talk or the sparing is another room's own and the room's members do not take it up (the visitor rule), or it comes after hour 73.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G34 to G36. A restriction whose condition the connection, the mechanism or the bound already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a). A correction states a condition that A05 and its bound lack and shows the order failing without it. A restriction whose concepts show a settled border followed by no sparing meets A05's `mechanism_fails_if`; G9 rules it a correction where no statement holds its condition (a breach contested is P08's holding to terms; an attack after a deal is P09's and A17's; placers the room cannot bind are P21's). Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  The order test is written and logged before it runs: the census of the rulings by room (the order, the order named in words, the bound with sparing first, one end, other), beside C2's count and C5c-09's count. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P08, P07, A04, A14, A16, A17, A19, A21, P05, P02, P09, P10, P16, P17, P20, P21, K02 and C01. Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (340, after 277 absent, 60 add-condition and 2 add-step lines), which the first draw's header confirms.

  **G37's readings, stated while ruling (D3a-32).** They read G37 and change no ruling rule. Each was logged before any line it touched was written.
  - **Appeals (AP).** An appeal to spare a work is P08's terms only where it names a limit, a place, a condition or an exchange, as G19's own clause says. An appeal that names none, answered by restraint or an apology, is P07's exchange ('We would like to preserve our cube.', then 'we'll fill in the gaps around your cube.', drugs). Where the answer sets the limit, the terms and the sparing come at once, so the order cannot be read. The census counts these apart (chile, drugs, farmcarrots, funhaus).
  - **A report of an agreement (J).** A report that a truce or agreement exists places its making before the report. It does not place it before an earlier sparing that does not name it. A line whose only talk is such a report, beside an earlier unnamed sparing, cannot be ordered (hawks, TsundereSharks).
  - **Alliances.** An alliance as such names no terms (P17), so sparing 'because we are allies' is not A05's order (Goodboye, PinkUnion, megaman). An alliance stated as mutual promises not to touch is P08's terms (lovelive).
  - **An envoy disowned.** A member who disowns the room's envoy shows P21's form, not terms (maryland).
  - **The order named in words.** A line with a sparing or reminder that names an agreement already settled shows the order in words, even where an earlier sparing in the line names none, since a reported agreement cannot be dated against that sparing. J stays for lines with no such sparing. Applied before anything was written, it moved danganronpa-026 and littlewitchacademia-030 from J, and foxes-046 from the bound, to the order named in words.
  - **The second end.** It is restraint shown by the room or the neighbour: sparing, reining in, refusing, apologising, restoring, or asking the room's own members to spare. An appeal to the other side to keep terms is P08's holding each other to them, not sparing (redhotchilipeppers, strangerthings).
  - **An offer that sets its own limit.** An offer of restraint that sets its own limit in the same concept has both ends at once ('that will leave 529 and below clear for you all', predators; J).
  - **The host.** A host's approval is P08's answer. A host's standing rules for guests are P19's form, a candidate (warframe rests on the approval).
  - **Restrictions and P21.** Most restrictions say that an agreement restrains only the placers it reaches. P21 holds that condition. Such a line is held by P21 where its concepts show no sparing by the terms, and it shows the order, with P21 named, where they do. Lines that meet the falsifier, a settled border followed by no sparing, are held: a breach complained of is P08's holding to terms (rpi, timbers), terms rejected by members are P21's (eve, EraseThePlace, btc), and an attack after terms is P09's (cirkeltrek, ss13).
  - **Assent and counter-proposal (absent lines).** A counter-proposal is terms, not restraint ('i was hoping we could stop at the top part of the head and just make a small box', GuildWars2). An assent or a promise by the side asked to give way, after terms that name a limit, a place, a condition or an exchange, is the second end, as qotsa-047 ('OK, help us find some coordinates.') and katawashoujo-035 were ruled ('Ok, we can arrange that.', latvia). A neighbour's restraint counts only where it keeps a deal with the room ('TFLS apologizes. It is our intent to keep the parrot safe.', partyparrot; not metalcore, puzzleanddragons or WPI). A sparing reported at an unknown time cannot be ordered against an earlier agreement ('we moved it to the left so we didn't smush other people's hard work.', startrek; iceland).
  - **Draws.** The draws at verb offsets 340 and 440 held all 198 instantiate lines (100 and 98). In the first draw, 7 of 10 lines show the order, 5 of them named in words; in the second, 9 of 10, 4 named in words. One how claims more than its quotes (maryland-044, an 'accepted border'). Every packet was read whole, with every cited concept quoted.
- **G38 (logged at D3a-33, before any of A06's lines was read or ruled).** A06 is a standing arrow from C2, P05 → P14, of kind order and strength strong. Its connection reads: 'in a room carrying both, the first act of upkeep or defence comes before the first script, bot or extra account'. Its mechanism: 'Upkeep under attack outruns what one pixel per interval can hold, and members turn to scripts and spare accounts to keep up.' It fails if 'In a room, scripts and spare accounts come only before any upkeep or defence, or a room under strain never reaches for them.' Its bound: 'Where a room scripted the building itself from the start, machine hands come before any upkeep. Spare accounts can also serve an attack before any upkeep (canucks).' C2 counted it in 160 of 203 rooms carrying both (0.788; null mean 0.603, p95 0.655), and F-005, named in P14's evidence, states the same order. P05 is read by G11, as move 173 left it. P14 is read by G24 and its readings: the act or the stance must be stated; a proposal or request for machine hands the room does not hold is not P14's act; a neighbour's machine hands count only where the room takes them up; machine hands that place nothing are not P14.

  Two readings follow from the arrow's own words, as QD3-007 reads a bound in its words.
  - **The second end is machine hands put to work.** The connection names 'the first script, bot or extra account'. So the second end is a member of the room writing, sharing, running or adjusting a script or bot for the work, placing with spare accounts or a glitch, lending accounts to a bot, or rooms pooling one bot target (G24's first, second, third and fifth clauses). An argument over machine hands, a refusal of them, or a call that others' scripts are unfair is P14's statement but not this end. The census counts upkeep followed only by such an argument apart.
  - **The two ends can be one act.** G11 counts 'running scripts set to keep it' as upkeep, and that act is also P14's. So where the room's first upkeep is itself a script or spare accounts set to keep the work, with no earlier upkeep shown, the first act of each is one act, and the order cannot be read (J, counted apart, as G35 counted a report that is itself damage).

  A06 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show upkeep with no machine hands, machine hands with no upkeep, neither, or the bound's pattern;
  - a concept that shows upkeep or defence of the room's mark, or a warning that it is changed (G11's watching), and, after it, machine hands put to work makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A06 when its concepts show upkeep or defence of the room's mark (G11) and, after it, machine hands put to work (G24, as read above). The order is read from the concepts' hours (`cite.py`), the transitions, or one post whose words name the upkeep, the attack or the strain first and the machine hands after. Where the machine hands are named as the answer to upkeep under strain (keeping up, an attack outrunning the room, a constant maintenance), the census counts the line apart, as the mechanism in the members' words, beside C2's 117 transitions in 53 rooms. A line is rejected when:
  - the first machine hands come before any upkeep: a script that builds the mark from the start, or spare accounts or a bot serving an attack (the bound's pattern, counted in the census as the bound);
  - the first upkeep is itself a script or spare accounts set to keep the work, with no earlier upkeep shown (J);
  - upkeep is followed only by an argument over machine hands or a refusal of them (counted apart);
  - only one end is shown;
  - what follows the upkeep is not P14's act: a proposal for machine hands the room does not hold, another group's bots reported as damage (P09, P05) or as outclassing the room (K02), placing by hand (shifts, staying up), a template with no machine hands (P04), or machine hands that place nothing;
  - the upkeep or the machine hands are another room's own and the room's members do not take them up (the visitor rule), or the machine hands are first shown after hour 73.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G34 to G37. A restriction whose condition the connection, the mechanism or the bound already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a). A correction states a condition that A06 and its bound lack and shows the order failing without it. A restriction whose concepts show machine hands before any upkeep, in a room that did not script its building or an attack, meets the falsifier's first clause; G9 rules it a correction where no statement holds its condition. The falsifier's second clause, a room under strain that never reaches for machine hands, is read inside the arrow's population, the rooms carrying both. Where a room under strain keeps by hand, refuses scripts, judges its hands too few, or moves or gives up, the condition is held by P05's hand upkeep (shifts, covering the night), P14's argument, K02, or P10 and A10. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2, and F-005 would then be re-examined under rule 14.

  The order test is written and logged before it runs: the census of the rulings by room (the order, the mechanism in words, the bound with machine hands first, one act holding both, upkeep followed only by an argument, one end, other), beside C2's count and F-005. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P05, P14, A03, P01 (the hold form), P03, P04, P02, P09, P18, P10 and A10, K02, P16, P17, P08, P07, C01, P20, P12, P22, P13 and P21. Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (492, after 468 absent and 23 add-condition lines), which the first draw's header confirms.

  **G38's readings, stated while ruling (D3a-33).** They read G38 and change no ruling rule. Each was logged before any line it touched was written.
  - **The mechanism in words.** A post or a request that names an attack, a loss of the work or the strain of keeping up, and then the machine hands as its answer, shows the order in the members' words, since the answer comes after what it answers. This holds even where the script already existed ('The flag is under attack! Do your part with the chrome script', afip).
  - **Either word order.** A post that ties the machine hands to an attack or to the strain of keeping up shows the mechanism in words in either word order ('Ok, i'm using my accounts to defend it but there is a guy painting it using the red', israel). Applied before anything was written, it moved muse-042 from J to the mechanism in words.
  - **One act, with the mechanism later (JM).** Where the line's first upkeep is a script set to keep the work, and a later post names strain and calls for more machine hands, the line stays J, since its first acts are one act. The census counts it apart (neu, bitcoin, india, zootopia).
  - **A rival's scripts.** A warning that a rival is about to script, or a report of a rival's script, is not upkeep, as G36 read a warning that a neighbour approaches (TsundereSharks, rangers).
  - **A pledge.** A pledge to keep the work counts as upkeep, as G35 read it (texas).
  - **A reply that names nothing.** A reply in a defence thread that gives a script without naming the attack shows the order by the hours, not in words (calgaryflames, dota2).
  - **The first act of each.** A line is classed by the first act of each, as G36 read. Where the first machine hands come before any upkeep shown, the line is the bound's pattern, even where a later post names the mechanism (AmericanFlaginPlace, osugame).
  - **No order inside one sentence.** A hand watch and a script reported in one sentence have no order between them (wildhockey, J).
  - **Reports of machine hands already at work.** A report that machine hands were at work over the effort ('But apart from that it's only been me (and my 4 alts).', sixers) places their start before the report, but not after an earlier upkeep that does not name them, as G37 read a report of an agreement. So such a line cannot be ordered. A report in the present tense, a reply that answers the call, or one post that names the upkeep first is read at its hour (FederationPlace, bakchodi, pitt). Checked backwards before the absent lines were written, it moved no instantiate or restrict line.
  - **Draws.** The draw at verb offset 492 held all 61 instantiate lines. Of the 10 lines drawn, 1 shows the order by the hours and 3 name the machine hands as the answer to an attack; 2 hold both ends in one act, 2 come after hour 73 and 2 only propose a script. Three hows claim more than their quotes show (neu-016, pathofexile-019, drumcorps-015), so the packet was read whole, with every cited concept quoted.
- **G39 (logged at D3a-34, before any of A07's lines was read or ruled).** A07 is a standing arrow from C2, P03 → P11, of kind order and strength strong. Its connection reads: 'in a room carrying both, the first build report comes before the first marking of the finished work'. Its mechanism: 'A mark reported done gives the room a finished thing to point at, and the room marks it together: announcement, credit, pride.' It fails if 'In a room, celebration comes only before any build report, or a finished build is never marked.' Its bound: 'Where the room's first mark was found already made by others, the room celebrates the find before it builds anything itself. Where hour 73 cut the work unfinished, the room marks the attempt instead'. After Stigmergy's recut, C2 counted it in 139 of 182 rooms (0.764; null mean 0.378, p95 0.434). Its counterexample response still names 100 of 282 rooms, a count from before the recut, carried with the fields the prose rule did not read, as G35 noted for A03. P03 is read by G15 and its readings: a report of the state of the room's mark to the thread before hour 73. P11 is read by G16 and its readings, as amended at D3a-13 (QD3-007): the room marks a work as up or achieved, at any hour, on its own word.

  Three readings follow from the arrow's own words and from G15 and G16.
  - **One act can hold both ends.** G15 reads a celebration whose words state the work made, finished or done as P03's 'done' and P11 at once, and G16 reads an announcement that the work is on the canvas as P03's lower range and P11 at once. Where such a concept is the room's first report, with no earlier report of the build, the first act of each is one act and the order cannot be read (J, counted apart).
  - **The second end is the marking of a finished work.** The connection names 'the first marking of the finished work'. Marking an attempt is the bound's second sentence only where the close cut the work unfinished, read in its words (QD3-007). Marking an attempt that ended in any other way (a work lost, erased or given up before the close, a plan stopped) is the family that D3a-13 left as a paired elaboration of P11, carried to D4. It is not A07's order, and it is counted apart.
  - **The mechanism in words.** A marking that answers a report that the work is done ('It's done!', then 'We did it!'), in a reply or a later post, shows the mechanism in the members' words; the census counts it apart.

  A07 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show a build report with no marking, a marking with no build report, neither, or the bound's pattern;
  - a concept that shows a report of the room's build (G15) and, after it, a marking of the finished work (G16) makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A07 when its concepts show a report of the state of the room's mark (G15) and, after it, a marking of that work as up or achieved (G16). The order is read from the concepts' hours (`cite.py`), the transitions, or one post whose words report the build first and mark it after. A line is rejected when:
  - the first marking comes before any build report: a find made by others marked first, or a marking with no report of the room's own build before it (the bound's first sentence, counted in the census as the bound);
  - the close cut the work unfinished and the room marks the attempt (the bound's second sentence, counted as the bound);
  - the room's first report is itself a marking that states the work done or on the canvas, with no earlier report (J);
  - the marking is of an attempt that ended before the close in another way (the family, counted apart);
  - only one end is shown;
  - the report or the marking is another room's own and the room's members do not take it up (the visitor rule), or the only report comes after hour 73 (P12, as G15 reads it). A marking after hour 73 of a work reported during the event shows the order, since P11 is shown at any hour.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G34 to G38. A restriction whose condition the connection, the mechanism or the bound already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a). A condition no statement holds, shown in the concepts without the order failing, is ruled by G4a's last clause: a paired elaboration where a second room shows it, a particular where only one does; the family of D3a-13 pairs within itself. A correction states a condition that A07 and its bound lack and shows the order failing without it. A restriction whose concepts show celebration before any build report, in a room that neither found the work made nor was cut by the close, meets the falsifier's first clause; G9 rules it a correction where no statement holds its condition. The falsifier's second clause, a finished build never marked, is read inside the rooms carrying both: a work reported done and then kept, recorded or carried on with no marking is held by P05, P12 or P13 where those statements name the act. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  The order test is written and logged before it runs: the census of the rulings by room (the order, the mechanism in words, the bound, one act holding both ends, the family, one end, other), beside C2's count. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P03, P11, A01 and A03 (the spine around the build report), A08 and P12 (the record, and A08's bound, the record before the marking), A09 and P13 (carrying on), P22, P05, P01, P02, P04, P15 (the bare answer, whose upper end is 'Did my part.'), P16 (help credited), P17 (joint marks), K01 (the frame), K02, P10 and A10. Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (202, after 176 absent, 23 add-condition, 1 add-step and 1 contradict lines), which the first draw's header confirms.

  **G39's readings, stated while ruling (D3a-34).** They read G39 and change no ruling rule. Each was logged before any line it touched was written. Reading 1 was corrected once, as dated below.
  - **1. A marking alone.** A line whose concepts show only a marking, with no build report anywhere in them, shows one end, not the bound. **Corrected (20 October, D3a-34, before any restrict line was written; applies backwards).** As first stated, the reading also put a build report that comes after the first marking under the bound's first sentence. That widened the bound beyond its words, against QD3-007. The first sentence names only a work found already made by others and celebrated before the room builds. A marking that comes before a report that the work is still unfinished is held by P11's statement as G16 reads it: the room marks a work on its own word, and P11 does not need the work finished. It is not A07's order either, and the census counts it apart as an early marking. The three instantiate lines that rested on the first wording (archlinux-047, fireemblem-039, starryknights-037) were re-ruled by appended lines (`A07-rerule-reading1.jsonl`): the decision stays reject, and the reason and the census class change.
  - **2. A finished part.** A cheer for a finished part while the work is said to be unfinished is a report (P03), not the marking of the finished work ('THE G IS COMPLETE BOIS, WERE ALMOST THERE!', Summit1G).
  - **3. Thanks for a step.** Thanks or a cheer for a member's step, for one part or for progress while the work is still being built is not the marking of a finished work. A report that one part is finished is a build report ('We filled in the blue. Good job', AmericanFlaginPlace, one end; 'The letters have been complete!', then 'We did ti boys we have nice!', 2007scape, the order).
  - **4. A 'done' that marks.** A 'done' report carries the marking at once where G16 reads it so: a post, a collective 'we', an exclamation, or 'on r/place'. A plain reply that states the work made or shows its image, answered by a marking, is the mechanism in words ('Looks like it's a success', then 'We did it!!!', ReBoot).
  - **5. Reports inside markings.** A line whose reports all sit inside markings, with no separate report before the first marking, is J, even where a bare cheer comes first (PUBATTLEGROUNDS, bostonbruins). A line of bare cheers with no words on the work's state shows one end (AMD, MMA, Dustforce).
  - **6. Done, then destroyed.** A work marked as done and then destroyed before the close was finished, since P11 does not need the work standing, so it shows the order (battlecats). D3a-13's family is for attempts never finished.
  - **7. A member's own part.** A member's own part told as hours or effort ('I spent all night on it') is P11's claim of a part, not a report of the work's state (cloud9).
  - **8. A cheer, then damage.** A bare cheer followed only by reports of damage to the standing work, or by a telling of a build already done, does not show the work unfinished when it was cheered, so the order cannot be read (J: denmark, denverbroncos, europe, h3h3productions).
  - **Draws.** Four draws of ten lines, at verb offsets 202, 302, 402 and 502 (seed 20261016 plus the offset), classed by the rulings later written: 202, the order 4, J 4, one end 2; 302, the order 3, J 6, after hour 73 only 1; 402, the order 2, J 2, one end 2, after hour 73 or a visitor's report 4; 502, J 6, after hour 73 or a visitor's report 4. One how (paydaytheheist-038) claims a different decision than its quotes give. Every packet was read whole, with every cited concept quoted, because the class turns on G15's 'done' and the bare cheer.

- **G40 (logged at D3a-35, before any of A08's lines was read or ruled).** A08 is a standing arrow from C2, P11 → P12, of kind order and strength strong. Its connection reads: 'in a room carrying both, the first marking of the finished work comes before the first record of what happened to it'. Its mechanism: 'Marking the work together turns the room toward keeping it: members ask for the final image, the timelapse, the list of what changed.' It fails if 'In a room, records come only before any celebration, or a celebrated work is never recorded.' Its bound: 'On the late side the record often comes first, a screenshot of a work found rather than built (8 of 15 hold).' C2 counted it in 225 of 289 rooms (0.779; null mean 0.565, p95 0.609). Its counterexample response names 64 of 289 rooms that record before they celebrate, answered as a scope condition carried to the onset contrast; one of its two support transitions failed its audit (titanfall: the first line posts the final image, a record). P11 is read by G16 and its readings, as amended at D3a-13 (QD3-007): the room marks a work as up or achieved, at any hour, on its own word. P12 is read by G13 and G13a: saving or asking for screenshots, timelapses or images of the work; reporting its fate; mourning, imagining what the work would have been, atlas entries, and marking the end. P12 is shown at any hour, and work after hour 73 curates the record (J, 15 October). Contesting the version kept is P22, not P12.

  Three readings follow from the arrow's words and from G13 and G16.
  - **One act can hold both ends.** G16 reads 'a final image posted as done' and 'the work said to have lasted to the end' as P11, and G13 reads images of the work, its fate and the end marked as P12. Where such a concept is the room's first marking and its first record, the first act of each is one act and the order cannot be read (J, counted apart).
  - **The ends are the finished work's.** The first end is a marking of the work as up or achieved (G16). Marking an attempt, where the close cut the work (A07's bound) or the work was lost, erased or given up before it (D3a-13's family), is not a marking of the finished work; it is counted apart. The second end is a record of what happened to that work. A record made while the work is still being built, or of a loss before the work was finished, is a record of an unfinished work; P12 holds it at any hour, it is not A08's order, and it is counted apart as an early record.
  - **The mechanism in words.** A request for the final image, the timelapse or a record of what changed, or such a record saved, in reply to a marking or right after it in one post, shows the mechanism in the members' words; the census counts it apart.

  A08 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show a marking with no record, a record with no marking, neither, or the bound's pattern;
  - a concept that shows a marking of the room's work (G16) and, after it, a record of what happened to that work (G13) makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A08 when its concepts show a marking of the room's work as up or achieved (G16) and, after it, a record of what happened to that work (G13). The order is read from the concepts' hours (`cite.py`), the transitions, a reply, or one post whose words mark the work first and then record it in a separate act. A line is rejected when:
  - its first record is a screenshot or image of a work found rather than built, before any marking (the bound, counted as the bound);
  - the first record of the finished work comes before its first marking, in a room that built the work (record first, counted apart);
  - the room's first marking and first record are one act (J);
  - the marking is of an attempt, or the record is an early record (counted apart);
  - only one end is shown, or the act is P22's contest, P13's carrying on or a visitor's that the room does not take up.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G34 to G39. A restriction whose condition the connection, the mechanism or the bound already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a). A condition no statement holds, shown in the concepts without the order failing, is ruled by G4a's last clause: a paired elaboration where a second room shows it, a particular where only one does; D3a-13's family pairs within itself. A correction states a condition that A08 and its bound lack and shows the order failing without it. A restriction whose concepts show the room's own finished work recorded before any marking, in a room that did not find the work, meets the falsifier's first clause; G9 rules it a correction where no statement holds its condition. The falsifier's second clause, a celebrated work never recorded, is read inside the rooms carrying both: a marked work that is then kept, carried on or contested with no record is held by P05, P13 or P22 where those statements name the act. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  The order test is written and logged before it runs: the census of the rulings by room (the order, the mechanism in words, the bound, one act holding both ends, record first, the attempt, the early record, one end, other), beside C2's count. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P11, P12, P22 and A07 (the marking and the record around it), A09 and P13 (carrying on), P03 (images of the current state), P05 (keeping), P09, P10 and A10 (loss and moving), P16 and P17 (help and joint works), P20 (the host's line on records), K01 (the frame) and P02. Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (391, after the verb's header line and 375 absent, 12 add-condition and 3 add-step lines), which the draw's header confirms. As first written, this sentence named offset 390; the first draw's header showed 57 instantiate lines there, and the sentence was corrected before any line was read.

  **G40's readings, stated while ruling (D3a-35).** They read G40 and change no ruling rule. Each was logged before any line it touched was written.
  - **1. The end marked.** The event's end marked ('Place is over', 'r/place has ended') is P12's 'marking the end', but it is not a record of what happened to the work, so it is not A08's second end. A post that marks the end and thanks the makers is a marking (AcePlace).
  - **2. A survival claim.** A claim that the work survived, held, stayed on the final canvas or was etched permanently is P11 (the work said to have lasted, G16) and P12 (its fate, G13) at once. As the room's first marking it makes the line J. Where a request for or saving of an image, a timelapse or a list of changes follows it, the line is J with the mechanism later (JM, as A06 counted it), counted as joint.
  - **3. An image in the marking.** A final image posted as done, or an image or link in the marking post, holds both ends (oman, bangtan).
  - **4. A retelling.** A retelling of what happened to the work is P12's record (its range: 'a full account of the week'), so a retelling after a marking shows the order (msu, greece).
  - **5. Another room's work.** Marking another room's work, or an alliance, is not the room's marking of its own work (madokamagica, twitchplayspokemon).
  - **6. Gone after the marking.** A report that a marked work is gone is a record of what happened to it, so the order shows, after G39's reading 6 (metroid).
  - **7. Record first.** A08's counterexample response states that some rooms record before they celebrate (64 of 289), answered as a scope condition. A restriction whose concepts show the room's own standing work recorded before its first marking is held by that field of A08. It is a specification, counted in the census as record first. It is a correction only where its condition names something A08's fields do not state.
  - **8. The room's earlier marking.** Where a line's concepts show a record before a marking, the room's earlier markings in lines already ruled (A07's and P11's) are checked. Where one comes before the record, the room's first acts show the order, and the line is ruled so, citing that line (sips, sheffield, texas, theexpanse, uiuc). The check is made only for lines whose own concepts show a record first, since only those could count against the order.
  - **9. A cheer, then a timelapse.** A title or post that cheers and then gives a timelapse or image keeps the marking first in its words, so it is the mechanism in one post (placetardis, turkey). bostonbruins-049, first classed as one act, was moved to it before anything was written. A post that gives the record first and the cheer after is one act (Slovakia, rickandmorty).
  - **Draw.** The draw at verb offset 391 held all 58 instantiate lines. Of the 10 lines drawn, 3 show the order by the hours and 2 the mechanism in words. 4 hold both ends in one act, and 3 of those have a record asked for or given later. 1 shows one end. Five hows claim the order where the quotes show one act or one end (bangtan, argentina, scp, gorillaz, anaheimducks), so the packet was read whole, with every cited concept quoted.

- **G41 (logged at D3a-36, before any of A09's lines was read or ruled).** A09 is a standing arrow from C2, P12 → P13, of kind order and strength fair. Its connection reads: 'in a room carrying both, the first record of what happened comes before the first act of carrying the work on'. Its mechanism: 'A record of the work gives the room something to carry: the image into the banner, the plan into the next canvas.' It fails if 'In a room, plans to carry on come only before any record, or a recorded work is carried nowhere.' Its bound: 'Where a room planned its next canvas or its emblem while still building, carrying on comes before any record.' Its counterexample response: 'texans carries the work on at h34.5 and records at h73.2. Response: a scope condition; 32 of 145 rooms run this way.' C2 counted the order in 113 of 145 rooms (0.779; null mean 0.563, p95 0.628). No finding names A09. P12 is read by G13 and G13a, and by G40's readings 1 and 4: saving or asking for images, timelapses and atlas entries, reports of the work's fate, mourning, imagined art, retellings and the end marked, at any hour; contesting the version kept is P22. P13 is read by G25, its timing amendment and its readings: a later canvas, a new purpose for the canvas sub or chat, the mark taken into the room's identity, a tie with another room carried past the canvas, or the work remade elsewhere, proposed, decided or done; 'near the close' is hours 61 to 73; A09's bound is read in its own words.

  Four readings follow from the arrow's words and from G13 and G25.
  - **One act can hold both ends.** A post that saves or shows the record and carries it at once ('final image, our new banner', a wallpaper made of the final canvas, a timelapse posted as a keepsake for next year) is P12 and P13 in one act. Where it is the room's first record and its first act of carrying on, the order cannot be read (J, counted apart).
  - **The mechanism in words.** A record asked for, saved or given, and then carried into the banner, the sidebar, a print, a later canvas or a remake, in reply or in one post whose words record first and carry after, shows the mechanism in the members' words; the census counts it apart.
  - **Carrying on first.** A later canvas or the mark as the room's emblem (banner, sidebar image, logo, flair, emoji), planned or made before the close and before any record, is the bound's pattern (G25's timing amendment). Any other act of carrying on that comes before the room's first record is the case A09's counterexample response states (32 of 145 rooms); a restriction that shows it is held by that field, a specification counted as carry first, as G40's reading 7 held A08's record-first rooms. Other forms begun before hour 61 are also D3a-20's family, keeping begun while building, which pairs within itself.

  A09 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show a record with nothing carried, carrying on with no record, neither, or the bound's pattern;
  - a concept that shows a record (G13) and, after it, an act of carrying the work on (G25) makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A09 when its concepts show a record of what happened to the room's work or canvas (G13) and, after it, an act of carrying the work on (G25). The order is read from the concepts' hours (`cite.py`), the transitions, a reply, or one post whose words record first and carry after. A line is rejected when the carrying on comes first (the bound, or carry first, each counted apart), when the room's first record and first act of carrying on are one act (J), when only one end is shown, or when the act is P11's marking, P22's contest or a visitor's that the room does not take up.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G34 to G40. A restriction whose condition the connection, the mechanism, the bound or the counterexample response already holds is a specification where its concepts show the order, the bound's pattern or carrying on first, and an evidence limit (kind `none`) where they show none of these. A condition held by another statement is a specification naming it (G4a). A condition no statement holds, shown in the concepts without the order failing, is ruled by G4a's last clause: a paired elaboration where a second room shows it, a particular where only one does; D3a-20's family pairs within itself. A correction states a condition that A09's fields lack and shows the order failing without it. The falsifier's second clause, a recorded work carried nowhere, is read inside the rooms carrying both: a recorded work that is then marked, kept or contested with no carrying on is held by P11, P05 or P22 where those statements name the act. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  The order test is written and logged before it runs: the census of the rulings by room (the order, the mechanism in words, the bound, carry first, one act holding both ends, the family, one end, other), beside C2's count. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P12, P13, P22, P11, A08 and A07 (the close and its record), P20 (the host's line around the canvas sub), P17 and P16 (ties and help between rooms), P02 (the design of the mark), P05, P10 and A10 (keeping, moving after a loss), K01 (the frame) and K02. Candidates and tentative entries hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (562, after the verb's header line and 557 absent and 4 add-condition lines), which the draw's header confirms.

  **G41's readings, stated while ruling (D3a-36).** They read G41 and change no ruling rule. Each was logged before any line it touched was written.
  - **1. The room's earlier record.** Where a line's own concepts show carrying on before any record, the room's records in lines already ruled (A08's and P12's) are checked (`d3_a09_cross.py`). Where one comes first, the room's first acts show the order, and the line is ruled so, citing that line (2007scape, AyyMD, EraseThePlace, touhou). This mirrors G40's reading 8.
  - **2. A cleaned image.** A cleaned image of the work, shared with no contest over the version kept, is a record (G13). So it can be A09's first end (ireland, uiuc).
  - **3. A record, then next time.** A wish to do better next time is P13's lower range (G25). A post that records what happened and then wishes for next time shows the order in its words (bangladesh, blackmirror, raocow).
  - **4. A proposal, or one act.** A proposal that names the work but saves or shows no record ('the final result in the banner') shows one end (portugal, sweden, ockytop). A post that saves, asks for or shows the image and carries it at once is one act (fireemblem, ubc, chicubs).
  - **5. The bound needs no earlier record.** A later canvas or emblem planned while building is the bound only where no record of the room comes before it in its lines already ruled. Where one does, the order shows (touhou, pathofexile, pitt).
  - **6. The whole canvas.** Carrying the whole canvas on (a poster, a skin, r/place remade in a game) is carrying the work on, as pcmasterrace-070's poster was ruled (kerbalspaceprogram, globaloffensive).
  - **7. A proposal not carried out.** A condition that a proposal was not carried out (a print offered, an image proposed for the sidebar) is held by P13's statement. P13 counts carrying on proposed, decided or done (G25) (chile, habs).
  - **8. A retelling, then the sub, the chat or a tie.** A retelling of how members worked or defended is P12's record (G40's reading 4). A post that retells and then keeps the sub, the chat or a tie shows the order in its words (AvoArmy, quebec, radiohead).
  - **9. The end marked.** The end marked alone ('its over') is not a record of what happened (G40's reading 1). So it opens no order (aeskwadraat, fivenightsatfreddys).
  - **10. The mechanism in words.** The carrying act must take the recorded work itself (an image, a logo, a sprite, a design) into a banner, a sidebar, an avatar, a later canvas or a remake, in reply, in its thread or in one post. After a record, a next-time wish, a tie, the sub or chat kept, or a later canvas named without the work is the order.
  - **11. Carry first.** A remake, a print or a tie before the close and before the room's first record is carry first. Those before hour 61 are D3a-20's forms, noted in the census.
  - **12. The scope of reading 1's check.** A line shows carrying on before any record (a) where its concepts show carrying on and then a record, and (b) where they show an act of carrying on before the close with no record before it in the line. A line that shows only carrying on after the close shows one end and is not checked, as at the instantiate lines. Nor is a line whose first record and first act of carrying on are one act.
  - **13. First acts in absent lines.** An absent line's claim fails where its first record comes before its first act of carrying on. Where an act of carrying on comes first, the order is not shown, and the line stays an evidence limit, even if a later record is followed by a later act (brasil, bulgaria, cirkeltrek).
  - **14. A question that proposes.** A question that puts a carrying act to the room ('Do we want to hit up pxls.space or nah?') is a proposal, which P13 counts (G25). A bare 'What should we do?' is not (cfb, OrderOfTheKoi, aoe2).
  - **Draw.** The draw's header confirms 35 instantiate lines at verb offset 562. Of the 10 lines drawn, 5 show the mechanism in words (ireland, timbers, mexico, osu, cgpgrey) and 1 the order by the room's earlier record (2007scape). 1 is one act (fireemblem), and 2 show one end (patriots, portugal). 1 was ruled the bound (pitt) and later re-ruled to the order by reading 1. Four hows claim the order where the quotes show one act, one end or the bound (fireemblem, patriots, portugal, pitt), so the packet was read whole, with every cited concept quoted.

- **G42 (logged at D3a-37, before any of A10's lines was read or ruled).** A10 is a standing arrow from C2, K02 → P10, of kind order and strength thin. Its connection reads: 'in a room carrying both, the first doubt about the room's numbers or room comes before the first move after a loss'. Its mechanism: 'A room that judges it has too few hands to hold its spot stops fighting for it and moves.' It fails if 'In a room, a move comes with no doubt voiced before it, or doubt about numbers is followed by no move and no surrender.' Its bound, as C5c-09 left it: early moves by choice come before any doubt; in a late room the judgment can be written after the move (guatemala); a room inside a coalition can move by the coalition's plan (MiamiHurricanes); read whole, in 10 of the 21 rooms the judgment came before the move, in 10 the loss itself prompted the move and the judgment came after it or inside the move turns, and 1 did not move; after doubt and a loss, a room moves or gives the work up (F-019). Its counterexample response: anarcho_capitalism moves at h9.0 and voices doubt at h32.9, a scope condition, and guatemala and MiamiHurricanes are two more. C2 counted the order in 11 of 21 rooms (0.524; null mean 0.298, p95 0.429). F-019, a standing finding on this arrow (C5c-09, restated at C5c-12), counts 10 of 20. `mem.py findings --touching A10` returns none, so F-019 is re-examined only if A10 is revised. K02 is read by G23, its amendment and its readings. P10 is read by G22 and its readings: a move after the loss (a new spot, a smaller version, a fresh start, hands moved to another work, a coalition's plan), or a weighing of fighting against moving after a loss; not a site chosen before any loss, not giving up with no move weighed, and not a plan for a later canvas after hour 73.

  Five readings follow from the arrow's words and from G22 and G23.
  - **The mechanism in words.** A judgment of too few hands or room answered by a proposal, weighing or decision to move, in reply or in one post whose words judge first and move after, shows the mechanism in the members' words. The census counts it apart.
  - **One act.** A post that reports a move already made and gives the shortfall as its reason holds both ends in one act: the judgment is voiced with the move, as C5c-09 read 'inside the move turns'. Where it is the room's first doubt and its first move, the order cannot be read (J, counted apart).
  - **Move first.** A move after a loss that comes before any doubt in the room is the case A10's bound and counterexample response state (the loss itself prompts the move; anarcho_capitalism). A restriction that shows it is held by those fields, a specification counted as move first. A move by a coalition's or an ally's plan with no doubt of the room's own is the bound's coalition pattern, counted as the bound.
  - **Gave up.** Doubt followed by giving the work up, with no move, is F-019's other outcome and K02's upper end. The falsifier's second clause exempts surrender. Such a line shows one end of A10's order and is counted apart.
  - **A two-way check across lines.** Where a line's own concepts show a move before any doubt, the room's K02 lines already ruled are checked for an earlier doubt; where one comes first, the line shows the order, citing that line. Where a line's concepts show the order, the room's P10 lines already ruled are checked for an earlier move; where one comes first, the line shows move first, citing that line. The second half answers the one-way check disclosed at D3a-36 (A07 to A09 keep that check for D3c). Only accepted lines are read, and every concept cited is quoted.

  A10 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show doubt with no move, a move with no doubt, neither, giving up, or the bound's patterns;
  - a concept that shows K02's judgment (G23) and, after it, a move after a loss (G22) makes the claim of absence fail (reject), whatever the line's observation, where the line's first doubt comes before its first move (as G41's reading 13);
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A10 when its concepts show K02's judgment (G23) and, after it, P10's move or weighing after a loss (G22). The order is read from the concepts' hours (`cite.py`), the transitions, a reply, or one post whose words judge first and move after. A line is rejected when the move comes first (move first, or the bound where a coalition's plan moves the room), when the first doubt and the first move are one act (J), when doubt is followed by giving up (gave up), when only one end is shown, when the move is not P10's (a site chosen before any loss, a later canvas after hour 73), or when the act is a visitor's that the room does not take up.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G34 to G41. A restriction whose condition the connection, the mechanism, the bound or the counterexample response already holds is a specification where its concepts show the order, the bound's patterns or move first, and an evidence limit (kind `none`) where they show none of these. A condition held by another statement is a specification naming it (G4a): K02's upper end and F-019 for giving up; P10 for a move that needs a loss; P04 or P02 for a site chosen before any loss; P07, P08 or P09 for moves to spare, by terms or onto another's work; P17 for a coalition's plan; P13 or P22 for acts after the close. A condition no statement holds, shown in the concepts without the order failing, is ruled by G4a's last clause: a paired elaboration where a second room shows it, a particular where only one does. A correction states a condition that A10's fields and those statements lack and shows the order failing without it. Doubt followed by no move and no surrender after a loss meets the falsifier's second clause; it is a correction only where no statement holds it. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2, and F-019 would then be re-examined under rule 14.

  The order test is written and logged before it runs: the census of the rulings by room (the order, the mechanism in words, move first, the bound, one act, gave up, one end, other), beside C2's count and F-019's. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are K02, P10, P05, P04, P02, P07, P08, P09, P16, P17, P01, P03, P12, P13, P14 and A06, and P22, with F-019 for giving up. Candidates and tentative entries hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (389, after the verb's header line and 372 absent, 15 add-condition and 1 contradict line), which the draw's header confirms.

- **G42, amendment 1 (D3a-37, 20 October 2026, before any A10 line was written; it applies to every A10 line, and none was ruled before it).** The two-way check also covers lines whose first doubt and first move are one act. The room's accepted K02 and P10 lines are read for concepts before that act. An earlier doubt makes the line show the order, and an earlier move makes it move first, citing that line. With neither, one act stands. Lines that show one end only are not checked, except a line that shows a move with no doubt before it, which G42 already checks. Why: in A10, unlike A09, one act is common among the instantiate lines, and C5c-09 read the room's first acts across its whole record.
- **G42's readings (D3a-37).** They apply G42 and change no rule. Each was logged before the lines it governs were written.
  1. **One post.** Word order decides. A judgment voiced first and a move proposed, weighed or decided after is the mechanism in words (cloud9, bangladesh). A move proposed or reported first, with the shortfall given after as its reason, is one act (twice, seolhyun, indieheads). A post that states the doubt and reports an earlier move as past shows the move first (turkey-024, 'another migration').
  2. **No move.** Doubt after a loss, and then no move and no surrender, is the falsifier's second clause: the room keeps defending, retakes the spot or keeps scripting in place. A10's bound says that 'the arrow holds for those that move', and the arrow records the mechanism's failure as present. P05 holds the defence and P14 the scripts. Such a line is a specification, counted as no move. Doubt under pressure answered by defence in place is read the same way.
  3. **Doubt with no loss.** Too few hands to start or grow a work, or a design sized to the room, is K02's form with P02's design. P10 needs a loss. Moves before any loss for a site, terms or sparing are P04's, P08's and P07's. Those statements hold such lines.
  4. **A rebuild in place** after a loss is P10's fresh start. Restoring a work that still stands is P05's.
  5. **A refused move.** A move proposed or weighed and then refused still counts as the room's first move, since P10 counts a weighing whatever the room then does.
  6. **One act in a restrict line.** A restrict line whose first doubt and first move are one act, and which the two-way check cannot order, is an evidence limit.
  7. **Move only.** A line that shows a move after a loss with no doubt, in a room with no accepted K02 line, shows the falsifier's first clause. A10's connection does not reach it, since the room does not carry both. Where the room has an accepted K02 line at any hour, the line is move first.
  8. **A smaller version** (refined before any restrict line was written; the first wording counted dropping an overrun part as P10's). P10's smaller version needs an act on the work: a resize, a new or simpler design, or a part filled in. Defending only the part that remains, or letting a part go with no change to the work, is P05's keeping, with K02 where a judgment is stated. Moving the hands to another of the room's works after a loss is P10's move (G22's reading on hands). A push into another group's space, given up, is not P10's (G22's reading on pushes).
  9. **What counts as the earlier doubt.** G42's earlier doubt is any K02 judgment in an accepted K02 line, in the forms K02 names: doubt about numbers, a canvas judged too full, and a work judged absent or outclassed. rotmg's and portal's lines already read it so. wow-053 is the one line whose order rests on a lament that the work is absent. Read as stated hands only, it would be move first.

- **G43 (logged at D3a-38, before any of A11's lines was read or ruled).** A11 is a standing arrow from C2, P02 → P04, of kind transition and strength thin. It is the first arrow of that kind to be ruled. Its gloss: 'a template settles a design argued in a thread'. Its mechanism: 'Design talk in a thread is settled by someone posting a template that lays out the agreed design pixel by pixel.' (Pass 7 took the field's advice that a template proposes a pixel arrangement and does not fix the output.) It fails if 'Templates are revised in threads with no design talk before them, or design talk ends with no template', and the arrow records that failure as present. Its bound: 'Inside reply threads only; across rooms the first template often comes before any design talk (texas: template at h5.9, design talk at h23.5), so it is not an order between rooms.' Its counterexample response withdraws the order claim: 'the arrow is restated as a transition inside threads, with base_rate_beaten false'. C2 grounded it on 82 transitions in 36 rooms, where a template answers design talk in one reply thread. The room-level order, kept in the connection as a tested result, was not beaten: 111 of 185 rooms (0.600; null mean 0.618, p95 0.670). `mem.py findings --touching A11` returns F-017, which names A11 as theorised; it is re-examined only if A11 is revised. P02 is read by G10 and P04 by G12.

  Five readings follow from the arrow's words and from G10 and G12.
  - **The transition.** A line shows A11 when, in one thread, a concept of design talk (G10: naming the picture, arguing or voting on the design, choosing an emblem, signing, enlarging or adding) is answered by a concept that shows P04 (G12: a layout, coordinates, a request for them, or a request to keep to them). 'Answered' means that the P04 concept comes after the talk, in the same thread, as a reply to it or in the same exchange; the hours, the item ids, the packet's transitions or the forest show it. A layout that lays out the talked design, new or revised, is the mechanism in the members' words, and the census counts it apart. Coordinates, or a request for a layout, that answer the talk show the transition through P04's other forms.
  - **One post.** A post that argues or proposes a design and gives its layout in the same post holds both ends in one act. It is not a transition, and the census counts it apart.
  - **Template first.** A layout posted before any design talk, in the room or in the thread, is the bound's case and the reason the order claim was withdrawn. A restriction that shows it is held by the bound and the counterexample response, a specification counted as template first. Inside a thread, talk that follows a template and is answered by a revised template is a transition.
  - **Across threads.** Design talk in one thread and a layout in another is outside the arrow's claim ('inside reply threads only'). It is held by the bound and counted apart.
  - **One end.** Design talk that ends with no layout, or a layout revised with no design talk before it, is the failure the arrow records as present. A restriction that shows it is held by the mechanism's failure clause, a specification counted as talk only or layout only. A design settled by vote, by a moderator or in a chat with no layout in the thread is P02's range and talk only.

  A11 is not stated as universal, so its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where its concepts show talk only, a layout only, a layout first, the two ends across threads, one post, or neither;
  - a concept of design talk answered in its thread by a later P04 concept makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A11 when its concepts show the transition. It is rejected when they show a layout first only, one post, the two ends across threads only, one end only, or a P04 concept that does not answer the talk.

  A restrict, contradict, add-condition or add-step line is ruled by G9 and G4a. A condition that the bound, the counterexample response, the mechanism or its failure clause already holds is a specification where the concepts show the transition or the held case, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it. The statements expected are P02 and P04 themselves, P03 (posting the work's state, which F-022 finds largely apart from templates), P01, P05 (repair restores the known form), P15, R01, P07 and P08 (designs fitted to neighbours), K02 and P10 (designs sized to the room or redone after a loss), P16 and P17 (layouts passed between rooms), P21, P14 and A06 (scripts that place from a layout), and P12, P13 and P22 (layouts kept or used after the close). Candidates and tentative entries hold no line (R02, P06, P19, K03, K04). A condition no statement holds, shown in the concepts without the transition failing, is ruled by G4a's last clause: a paired elaboration where a second room shows it, a particular where only one does. A correction states a condition that A11's fields and those statements lack and shows the transition failing without it. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2, and F-017 would then be re-examined under rule 14.

  The test is written and logged before it runs: the census of the rulings by room (the transition, the mechanism in words, P04's other forms, one post, template first, across threads, talk only, layout only, held, one end, other, limit), beside C2's 82 transitions in 36 rooms and its room-level order (111 of 185, not beaten). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (330, after the verb's header line and 322 absent, 6 add-condition and 1 add-step line), which the draw's header confirms.

- **G43's readings (D3a-38).** They apply G43 and change no rule. The first three were logged before the lines they govern were written. The fourth is written here at the close, from the rulings that applied it.
  1. **A layout announced or promised.** A template announced, being made or promised in reply to design talk ('We're working on a smaller template', drumcorps; 'I'll change the graphic', latin) answers the talk with P04's act of making a layout for the room. It shows the transition through P04's other forms, not the mechanism in words, since no layout is posted in the line. A request to keep to an existing layout, and an anchor coordinate, are the same class.
  2. **A request answered by a layout.** A request for a layout answered by a layout shows P04 at both ends. A11 needs design talk (G10) first, so such a line shows one end. A post that names the picture and asks for a layout shows P02 and P04's request at once, and a layout that follows in its thread shows the transition (frc).
  3. **What 'settled' means.** A11's mechanism word 'settled' is read with what the model already states: pass 7's amendment (a template lays out a proposed arrangement and does not fix what is placed), P02's range ('a design argued over days and redone'), P04's range ('an official template the room asks everyone to follow against other versions') and P05's statement ('A change the room has planned or agreed (P02) is therefore repaired away as damage until its keepers are told of it'). A restriction that a template does not end the design talk for good is held by those statements and is no correction. Talk that resumes after a template is new design talk, answered again by a revised layout or ending with no layout. Whether the mechanism's word should be restated is asked of J (QD3-008). **J answered at D3a-39 (20 October): 'Option 2. But they should be able to decide on this'.** The word stays, and the question goes to D3c with the count, as the stated assumption said, so no ruling changes. J's second sentence makes such a question mine: where no correction triggers §2, I decide an element's or arrow's wording with a written reason, and log it. I decide A11's word at D3c.
  4. **Who answers, and when** (written at the close). A layout posted by the member who voiced the talk is an answer, since the mechanism names 'someone posting a template' (danganronpa, foxes, marvel, Braveryjerk). A layout posted much later in the same thread, with no reply marker and no reference to the talk, is not shown to answer it (buffalowizards, 36 hours later; mordhau, on another topic). A layout that names the talked design, or gives what the talk asked for, answers it with no reply marker (chicago, PlaceNL, dallasstars). A layout in another branch that names neither is not shown to answer, even an hour later (habs). The first rulings did not all apply this reading. A check of every transition line against the forests (`_analysis/d3_a11_reply_check4.py`) found six whose named layout does not answer the named talk. Appended lines re-rule them: four keep the transition with the talk and the answer corrected (drugs, raocow, reddevils, japan); one becomes talk only (habs); and one absent reject keeps its decision, with the submission as the talk answered (foxstevenson).

- **G44 (logged at D3a-39, before any of A12's lines was read or ruled).** A12 is a standing arrow from C2, P01 → P15, of kind transition and strength thin. It is the second arrow of that kind to be ruled. Its gloss: 'the cheapest answer to a call'. Its connection: 'a one-line pledge answers a call in the same thread (form-pass finding FP-01; never counted)'. Its mechanism comes from conversation analysis: 'A call is the first part of a pair: posted to a thread, it makes an answer from each reader the next thing due, given in the thread or by placing.' Joining is the preferred answer and comes bare, 'one line that commits and gives no reason'. Declining is the dispreferred answer and comes with a reason. It fails if 'The one-line pledges in a room answer no call, or every answer to a call is long and conditional.' It also fails if joins give reasons as often as refusals do, or if refusals come as bare as joins. The arrow marks that failure 'not-addressed', since the reason test ran on attack calls only (C3b). Its bound begins 'Never counted as an order.' At C5c-11, acceptances of calls to place gave no reason in 25 of 31, and refusals gave one in 3 of 3 (F-023). More than half of all calls carry no written reply, so the form is read on written, coded replies only. A12 has no counterexample response. C2 grounded it on three exemplars (lebanon, DestinyTheGame, pcmasterrace), and its audit passed one of them. `mem.py findings --touching A12` returns none. F-023 and F-014 ground the mechanism and the bound, and they are re-examined only if A12 is revised. P01 is read as at D3a-02, with its hold form (G11), and P15 by G28.

  Seven readings follow from the arrow's words, G28 and the reading of P01.
  - **The pair.** A line shows A12 when, in one thread, a concept of P01 is answered by another member's written concept of P15. P01's concept is a call to place for a work: to start, build, finish, hold or defend it, an attack call among them. P15's concept is a join, an assent, a report of the member's own part done, or thanks, and it asks nothing back (G28). 'Answered' is read as G43 reading 4 reads it: the answer replies to the call, stands in its exchange, or names it. A top-level reply answers a submission that holds the call. The caller's own later post is not an answer, since a pair needs two members.
  - **The bare join.** An answer that joins in one line and gives no reason ('On it', 'I'm in') is the mechanism in words, and the census counts it apart. A join that gives a reason, or runs long, still shows the pair (G28). The census counts it as a join with a reason, the case the failure clause weighs. A report of a part done, or thanks, given in answer to the call shows the pair through P15's other forms.
  - **A proposal answered.** Assent to a proposal that calls no one to place (a design choice, a plan's detail, terms with another room) shows P15 by its range, but not A12's first part. P15's statement and P02, P04 or P08 hold it, and the census counts it apart. A proposal that also asks members to place is a call.
  - **Call only.** A call with no written answer in its thread is the bound's case ('More than half of all calls carry no written reply'). The bound and F-023 hold it, and the census counts it as call only. Members who answer by placing and write nothing are the same case.
  - **Pledge only.** A one-line pledge that answers no call in its thread is the failure clause's first half. The census counts a line that shows only this as pledge only.
  - **Across threads.** A call in one thread and a pledge in another stand outside the connection ('in the same thread'). The census counts them apart.
  - **The dispreferred answer.** A refusal, a doubt, a counter-proposal or a reply that asks something back is not P15 (G28). A refusal with a reason is the mechanism's other half (A16, F-014). A bare refusal is the case the failure clause names. The census counts lines that show only these apart, as a refusal with a reason or a bare refusal.

  A12 is not stated as universal, so its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where its concepts show call only, a dispreferred answer, pledge only, the two ends across threads, a proposal answered, or neither end;
  - a call answered in its thread by another member's later written P15 concept makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A12 when its concepts show the pair. It is rejected when they show call only, pledge only, a proposal answered, the two ends across threads, the caller's own answer, or only a dispreferred answer.

  A restrict, contradict, add-condition or add-step line is ruled by G9 and G4a. A condition that the bound, the mechanism or its failure clause already holds is a specification where the concepts show the pair or a held case, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it. The statements expected are P01 and P15 themselves; F-023 and F-014, through the bound and the mechanism; A16 (an attack call refused with a reason); P08 (terms asked back); P02 and P04 (proposals, templates and plans); P03 and P11 (state reports and a member's own part); P16 (help and thanks between rooms); P09 (attack calls); P05 (keeping); P10 and K02 (calls after a loss or with too few hands); P14 and A06 (scripts); P17, A19 and P21 (coalition calls, and who may commit the room); A02 and A01 (calls after a start, and building after calls). Candidates hold no line (R02, P06, P19, K03, K04). A condition no statement holds, shown in the concepts without the pair failing, is ruled by G4a's last clause: a paired elaboration where a second room shows it, a particular where only one does. A correction states a condition that A12's fields and those statements lack, and shows the pair failing without it. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2. F-023 and F-014 would then be re-examined under rule 14.

  The test is written and logged before it runs: the census of the rulings by room (the pair; the bare join; a join with a reason; P15's other forms; a proposal answered; across threads; call only; pledge only; the dispreferred answer; held; other; limit), beside A12's exemplars and F-023's 25 of 31. Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (190, after the verb's header line and 162 absent, 21 add-condition and 6 add-step lines), which the first draw's header confirms.

- **G44's readings (D3a-39).** They apply G44, with G33's readings of starts and with G28, and change no rule. They were logged before the lines they govern were written.
  1. **What a call is.** A call asks members to place. It does so by an imperative, a question put to the room, a request for help, an invitation, or an instruction given with a start (a joint opening, G33's readings). A start told in the present tense, or a report of where work goes on, is a start (R01) or a state report (P03), not a call. A join that replies to it answers a start. The census counts it as a start joined, and an instantiate line that shows only this is rejected (adventuretime, armok, berkeley, aggies, cloud9). Sometimes that start or report itself answers a coded call for the same work, from another member, above it in the reply chain. Then the join stands in the call's exchange and shows the pair. The reason names the call from the room's record, and the census marks it (canucks, auburn, bostonceltics).
  2. **The answer's form.** A present-tense report of the member's own work, given in answer, is a join ('I'm working on it', 'doing my best'). A past or perfect report is a part done ('Done!', 'started placing already').
  3. **A reason.** A join gives a reason when it gives an account of why the member joins: a ground ('so I'm in'), a motive ('I need Isabelle'), or an appraisal of the damage ('Wow that was just plain disgusting.'). An assessment of the call ('Oh good idea!!!') is part of the preferred answer, not a reason. A join with a condition, or with a question back, is tagged apart.
  4. **A call with no code.** Some answers reply to a post with no code, with no coded call from another member above them. They cannot show the pair in the coded record, since the bound reads the form on written, coded replies only. The census counts them as an uncoded first part, and an instantiate line that shows only this is rejected (AmericanFlaginPlace, PinkVomitMonster).
  5. **After the close.** A call and its answer about a successor canvas after hour 73 are carrying on (P13), not A12's pair on this canvas (calgaryflames).
  6. **Several answers in one line.** The line takes its strongest form: a bare join, then a join with a reason, then a part done. Refusals, conditions and questions back in the same line are tagged for the census (`_analysis/d3_rulings/A12-tags-*.txt`).
  7. **An answer that only sets a condition or asks back** (settled while ruling the restrict lines, and applied to both ops). G28 does not count such a reply as P15 ('Yes but we need numbers.', 'sure, where are you drawing?'). A line whose only answers are of this kind is counted as a conditional answer, apart from the pair. A line with a clean join beside one shows the pair and is tagged. Where the condition is met in the same exchange and the member then commits, the line shows the pair (switzerland, rocketbeans). One instantiate line ruled before this reading had only such an answer (bretagne-032, 'Moi je suis la si y'a besoin'), and an appended line re-rules it.
  8. **The absent rule reads the line's own concepts** (written at the close). A reject needs the call and the written answer to it among the line's concepts. Where the answer replies to a call that is not among them, the line stays an evidence limit (sheffield, southafrica, wildhockey, wsu), although an instantiate line in the same case names the call from the room's record.

- **G45 (logged at D3a-40, before any of A13's lines was read or ruled).** A13 is a standing arrow from C2, P05 → P16, of kind order and strength fair. Its gloss: 'short of hands, a room turns to other rooms'. Its connection reads: 'in a room carrying both, the first act of upkeep or defence comes before the first help given, asked for or traded with another room'. Its mechanism: 'A room keeping its work under strain runs short of hands and turns to other rooms for help, and other rooms send it.' It fails if 'In a room, help is given, asked for or traded only before any upkeep or defence, or a room under strain never asks for or receives help.' The arrow records this failure as present. Its bound: 'Where a room helps a neighbour before it has a work of its own to keep, or comes to the canvas as another room's helper, exchange comes first.' Its counterexample response counts '69 of 240 rooms' that give or ask for help before their first upkeep, and names 'a second path where help is the room's first relation to the canvas'. C2 counted the order in 171 of 240 rooms carrying both (0.713; null mean 0.596, p95 0.642). `mem.py findings --touching A13` returns none. A14 (P08 → P16) names A13 as its stronger sibling, and F-020 reads A14's mechanism. P05 is read by G11, as move 173 left it, with G36's readings of upkeep. P16 is read by G17 and its readings.

  Three readings follow from the arrow's words, as QD3-007 reads a bound in its words.
  - **The second end is help passing.** The connection names 'the first help given, asked for or traded with another room'. So the second end is help given or offered to another room's work, help arriving from another room, a request for help made by the room or reaching it, or help bartered (G17's first three clauses). Greetings, compliments and condolences between rooms, an alliance as such, terms not about help, a call to the room's own members only and a proposal to ask with no request made are not this end. Thanks to helpers show help already given. They show the second end where the help they thank can be placed after the room's upkeep, by the reply chain, the hours or the thanks' own words.
  - **The first end is the room's own upkeep.** It is the room's members keeping the room's own placed work (G11), including a warning that the work is changed and a call to defend it (P01's hold form), as G36 read. Help that another room gives to the room's work is the second end, not the first. Where the first upkeep shown is itself done by another room's helpers, with no earlier upkeep by the room's members, the first act of each is one act, and the order cannot be read (J, counted apart).
  - **The direction of the help.** The mechanism names one direction: the room under strain asks, and other rooms send. G17's add lines also name help given from spare capacity once the room's work is safe as A13's order. So the census records, for each line that shows the order, whether its first help after the upkeep is the room asking for or receiving help, the room giving or offering help, or help traded.

  A13 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show upkeep with no help, help with no upkeep, neither, or help before any upkeep (the bound's pattern or the second path);
  - a concept that shows upkeep or defence of the room's own work and, after it, help passing between the room and another room, as read above, makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A13 when its concepts show upkeep or defence of the room's own work (G11) and, after it, help given, offered, asked for, received or traded with another room (G17, as read above). The order is read from the concepts' hours (`cite.py`), the transitions, the reply chain, or one post whose words name the upkeep, the attack or the strain first and the help after. Where the help is named as the answer to an attack, a loss or the strain of keeping the work, the census counts the line apart, as the mechanism in the members' words, beside C2's 106 transitions in 44 rooms. A line is classed by the first act of each, as the connection counts them (G36's reading). It is rejected when:
  - the first help comes before any upkeep: the room helps a neighbour, or comes to the canvas as another room's helper, before it has a work of its own to keep (the bound's pattern); or it asks for or receives help to start or build its work, or trades help for space, before any upkeep (the counterexample response's second path). The census counts the two apart;
  - the first upkeep shown is itself done by another room's helpers (J);
  - only one end is shown;
  - what follows the upkeep is not help, as read above;
  - the upkeep is of another room's work and not the room's own (the visitor rule; keeping an ally's work is help, the second end), or the help is first shown after hour 73.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G34 to G38. A restriction whose condition the connection, the mechanism, the bound or the counterexample response already holds is a specification where its concepts show the order, the bound's pattern or the second path, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a). A correction states a condition that A13, its bound and its counterexample response lack, and shows the order failing without it. The falsifier's first clause, help only before any upkeep, is the bound's case and the second path's. Its second clause, a room under strain that never asks for or receives help, is read inside the arrow's population, the rooms carrying both. Where a room under strain keeps by hand, scripts, judges its hands too few, or moves or gives up, the condition is held by P05's hand upkeep, A06 and P14, K02, or P10 and A10. Where help is asked and refused or does not come, P16's range holds it (refusals). Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  The order test is written and logged before it runs: the census of the rulings by room (the order, the order named in words, the bound's pattern, the second path, one act holding both, held, not help, one end, other, limit), with the direction of the first help among the order lines, beside C2's count, C2's 106 transitions and A14's count at C5c-09 (the first help names a deal or a border in 63 of 127 rooms where border talk comes first). Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P05, P16, A14, P08, P17, A19, P07, P09, P18, P01 (the hold form and kindred calls), K02, A10, P10, P14, A06, P02, P11, P20, P21, A03, A01, P12, P13 and C01. Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (366, after the verb's header line and 337 absent, 24 add-condition and 4 add-step lines), which the first draw's header confirms.

- **G45's readings (D3a-40).** They apply G45, with G11, G17 and G36 to G38, and change no rule. Each was logged before the lines it governs were written, except where a reading says it was applied backwards.
  1. **The first end from the room's record.** A coded upkeep post by the room's members above the line's concepts in their reply chain (the submission or a parent) can be the first end. The reason names it, and the census marks the line R, as G44 reading 1 did.
  2. **The order in words.** A request for help, or a post answered in reply by help, that names an attack, damage, a loss or the strain of keeping the room's own work shows the order in the members' words. The attack may be present or announced. Naming the attack is G11's watching, and the help answers it, in either word order (G38's reading). Help placed after the upkeep only by the hours or the thread is the order by the hours.
  3. **Help to another room.** The room's help to another room after its own upkeep shows the order, with the help given. The other room's strain is not the mechanism in words, which names the room's own work. Where the room's own upkeep is not shown, the line shows one end.
  4. **A request reaching the room** is the second end at its hour. Where the room's upkeep is shown only as already under way at a later hour, the first acts cannot be ordered (giivasunner, placetardis), as G38 read reports.
  5. **Trades for night cover.** Help or space given now so that another room keeps the work while members sleep makes the room's first upkeep shown the helpers' watch, one act. Lines that name the night shortage are marked JM (australia, ockytop, sweden), as A06's census marked JM.
  6. **A visitor's defence first.** A visitor's defence or repair that comes before any upkeep by the room's members is one act (afip, brasil, japan, AprilKnights, and pakistan's r/India helpers).
  7. **Help only.** A line whose only help is named as help to start or build, with no upkeep shown, is the second path (singapore, 2007scape). Other lines with only help show one end.
  8. **An uncoded first end.** An upkeep in a post with no code cannot be the first end, as G44 reading 4 read uncoded first parts (AmericanFlaginPlace, babymetal, rangers, texans).
  9. **Proposals.** Upkeep followed only by proposals to ask or plans to help inside the room is not help (G17's readings). A13's support transition aceattorney-044 is such a proposal, as G36 found A04's to be.
  10. **NONPORTABLE lines** are particulars by G6. Where their concepts show the order, the census counts it apart (detroitredwings-036). An absent NONPORTABLE line whose concepts show the order is rejected, since the claim of absence fails (thenetherlands-058).
  11. **Edited submissions** (settled while ruling the restrict lines, applied backwards). A code in a submission carries the submission's hour, though an edit added later carries it too. A code whose words show an edit or an update list ('Edit:', a report that the work is done or that placement has ended, thanks to placers, a running list of instructions) cannot be dated by that hour, so it cannot be the first end named from the room's record. Found at lakers c0144 ('R/Place has officially ended now', dated h+52.98). Applied backwards: two instantiate lines are re-ruled by appended lines (calgaryflames-052, spacexmasterrace-054), and three restrict lines were ruled without R before the write (aceattorney-045, anaheimducks-034, lakers-073).
  12. **Reports of help in absent lines** (stated in the absent note before the write). Thanks or a report of help places the help before it, but not after an earlier upkeep that it does not name, as G38 read reports. Such a line stays an evidence limit (bulgaria, hongkong, korea, polska, reddevils).

- **G46 (logged at D3a-41, before any of A14's lines was read or ruled).** A14 is a standing arrow from C2, P08 → P16, of kind order and strength thin. Its gloss: 'a settled border opens a channel for help'. Its connection reads: 'in a room carrying both, the first border talk, truce or deal comes before the first help given, asked for or traded with another room'. Its mechanism: 'Talk over a border opens a channel through which the two rooms then trade help: room for upkeep, pixels for protection.' It fails if 'In a room, help is traded only before any border talk, or settled borders are never followed by help between the two rooms.' The arrow records this failure as present. Its bound: 'Where a room's first relation to a neighbour is help, help comes first.' At C5c-09 every room carrying both was read. The first help named a deal, border, truce, alliance, an exchange or the neighbour relation as its ground in 63 of 127 rooms where border talk came first, against 23 of 67 where help came first, and I judged the mechanism shown in words on that contrast (F-020). Its counterexample response: '76 of 214 rooms trade help before any border talk. Response: uncertainty; the arrow is kept thin and theorised beside its stronger sibling A13.' C2 counted the order in 138 of 214 rooms carrying both (0.645; null mean 0.591, p95 0.636), from 108 transitions in 44 rooms. One of its three support transitions failed its audit (ElSalvador: the first help at h61.2, the first terms at h61.41). `mem.py findings --touching A14` returns none. F-020 reads A14's mechanism, and it is re-examined only if A14 is revised. P08 is read by G18 and its readings, with G36's and G37's readings of terms. P16 is read by G17 and its readings, with G45's reading of the second end.

  Four readings follow from the arrow's words, as QD3-007 reads a bound in its words.
  - **The first end is P08's terms between the room and another room.** It is proposing, asking, settling, contesting or holding to a border, a space, a truce or a deal, read from either room's record (G18). One offer or request with no reply is the lower range. These are not this end: a proposal inside the room to ask, with no request made; an appeal that names no limit, place, condition or exchange (P07's, by G18's and G37's readings); an alliance as such (P17), unless it is stated as promises about each other's work; help traded only for help (P16's, by G18's reading); and locating the work by its neighbours.
  - **The second end is help passing**, as G45 read it. It is help given or offered to another room's work, help arriving from another room, a request for help made by the room or reaching it, or help bartered (G17's first three clauses). Greetings, compliments and condolences, an alliance as such, sparing (P07), a call to the room's own members only and a proposal to ask are not this end. Thanks show help already given. They show the second end where the help they thank can be placed after the terms.
  - **One offer holding both ends.** G17 counts terms that trade help for space or restraint as both P08 and P16. Where the room's first terms are themselves an offer or a request of help in exchange for space or restraint, with no earlier terms or help, the first act of each is one act. The order cannot be read (J, counted apart), as G37 read an offer that sets its own limit. Where help is given, offered or asked later and names terms already offered or settled as its ground, the order is shown in the members' words ('As per the terms, we will help with the triangle', the quote F-020 cites).
  - **The channel.** The mechanism names help between 'the two rooms' that talked. The connection counts help with any other room. So the census records, for each line that shows the order, whether its first help after the terms passes with the room the terms were with, with a third room, or with a room the record does not name. Order lines whose help names an alliance, an exchange or the neighbour relation as its ground, and not terms, are marked NB, so that the census can be set beside F-020's wider count.

  A14 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show terms with no help, help with no terms, neither, or help before any terms (the bound's pattern);
  - a concept that shows P08's terms between the room and another room and, after it, help passing between the room and another room, as read above, makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A14 when its concepts show P08's terms between the room and another room (G18, as read above) and, after them, help given, offered, asked for, received or traded between the room and another room (G17, as G45 read it). The order is read from the concepts' hours (`cite.py`), the transitions, the reply chain, or one post whose words report terms settled or offered and then give, offer or ask for help on them. Where the help names terms already offered or settled as its ground or occasion, the census counts the line apart, as the mechanism in the members' words, beside F-020's 63 of 127. A line is classed by the first act of each, as the connection counts them (G36's reading). It is rejected when:
  - the first help comes before any terms (the bound's pattern, counted in the census as the bound);
  - the first terms and the first help are one offer, or the only terms shown are reported at an hour that cannot be placed against an earlier help that does not name them (G37's reading of a reported agreement); the census counts these as J;
  - the first end shown is not P08's terms, as read above (counted apart);
  - only one end is shown, or the terms or the help pass between other rooms and not the room (G17 and G18 read either room's record, not a third room's relations);
  - what follows the terms is not help, as read above: sparing by the terms is A05's order, and an attack after them is P09's and A17's (counted apart);
  - the help is first shown after hour 73, or the terms are.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G34 to G38 and G45. A restriction whose condition the connection, the mechanism, the bound or the counterexample response already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a). A correction states a condition that A14, its bound and its counterexample response lack, and shows the order failing without it. The falsifier's first clause, help only before any terms, is the bound's case. Its second clause, settled borders never followed by help between the two rooms, is read inside the rooms carrying both. Where terms are followed by sparing (A05 and P07), by a breach, an attack or a contest (P08's holding to terms, P09, A17, P18), by a move (P10), by help with a third room (A14's connection), or by placers the room cannot bind (P21), the condition is held. Where help is asked on the terms and refused or does not come, P16's range holds it (refusals). Where upkeep and not terms comes before the first help, A13 holds it. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  G45's readings 1, 4, 8, 9, 10, 11 and 12 say how an end is placed and dated, and they apply here with A14's ends in place of A13's: a coded post of terms above the line's concepts in their reply chain can be the first end, and the census marks the line R (reading 1); a request reaching the room is the second end at its hour (4); a post with no code cannot be the first end (8); proposals to ask are neither end (9); NONPORTABLE lines are particulars, and where their concepts show the order the census counts it apart, marked PO (10); a code in an edited submission cannot be dated by the submission's hour (11); a report of help or of terms in an absent line places the act before the report, but not after an earlier act that it does not name (12).

  The order test is written and logged before it runs: the census of the rulings by room (the order, the order named in words, the bound's pattern, one offer holding both, held, not terms, not help, one end, after the close, other, limit), with the channel of the first help among the order lines, beside C2's count, C2's 108 transitions, F-020's 63 of 127 and A13's census. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P08, P16, A13, A04, A05, A17, A19, A21, P05, P07, P09, P10, P17, P18, P20, P21, P01 (kindred calls), K02, A10, P02, P11, P12, P13 and C01. Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (342, after the verb's header line and 322 absent, 16 add-condition and 3 add-step lines), which the first draw's header confirms. The three instantiate packets hold 100, 100 and 16 lines.

- **G46's readings (D3a-41).** They apply G46, with G17, G18, G19, G37 and G45's readings, and change no rule. Each was logged before the lines it governs were written. Where a reading moved a spec row, the row was revised before any write.
  1. **One offer against one post.** An offer or request of help in exchange for space or restraint is one act (J). A post that states or agrees terms and then separately asks for or offers help, not as the exchange, shows the order in the post's words ('Put it next to him. We'll even help you build it', carletonu). A counter-offer that adds help in a reply after the first terms shows the order by the reply chain (AMD, aceattorney, texas).
  2. **Declarations.** A statement that a room will stop advancing into a neighbour's space, or leave the space it was taking, concedes space by talk (P08, and P07 at once). A bare statement of goodwill or no harm that concedes no space is P07 only (G19). Under it archlinux-055 and monero-052 moved from not terms to the order before the write, and eve-052 stays the bound.
  3. **Appeals.** An appeal that names no limit or place becomes P08 at the answer that agrees or sets one. Where the answer's help itself sets the place (help to move), the terms and the help come at once (J, as G37 read appeals; coldplay, skyrim). Where the answer agrees and then separately asks or offers help, the order shows in its words (esperanto, quebec, ukraine).
  4. **After the close.** Where both ends are first shown after hour 73, the line is after the close. acecombat-052 moved from J before the write, as ireland-036 was ruled.
  5. **The record's first act** (G45 reading 1). Where the coded post above the line's concepts itself holds both ends in one offer, the line is J (halo, poland).
  6. **Help for help** is not terms (G18). Lines whose only talk is help for help are not terms, and such help before any terms is the bound's case (greece, eve).
  7. **The room's own damage.** Undoing damage the room did is P07's restoration, not the second end (G17; stevenuniverse, pitt).
  8. **Edits.** An edit that adds help to a post of terms places the help after them (gatech). An edit that holds the first end cannot date it (G45 reading 11; raocow).
  9. **Reports and announcements of help** (settled while ruling the absent lines). A concept by the helping side, addressed to the helped room, that offers help, calls for it, or says help is being given now is the help at its hour ('Us people at the trans flag are trying to help ya!', rickandmorty). A concept that reports help as given before or as continuing, or a report by the helped side or a third party of help under way, places the help only before the report (G45 reading 12). Where a post gives help already under way as the ground of its own request, the help comes first (empiredidnothingwrong). Checked against every line already written, it changed no ruling.

- **G47 (logged at D3a-42, before any of A15's lines was read or ruled).** A15 is a standing arrow from C2, P01 → P09, of kind order and strength strong. Its gloss: 'a call's hands can turn on a rival'. Its connection reads: 'in a room carrying both, the first call to the canvas comes before the room's first call or act against another room's work'. Its mechanism: 'A call brings members to the canvas, and some of them turn its hands against a rival's work instead of, or before, building the room's own.' It fails if 'In a room, calls to attack come only before any call to place, or calls to place are never followed by a call or act against another room's work.' The arrow records this failure as present. Its bound: 'Where a room's first canvas act is an attack (edmontonoilers, canucks, anarcho_capitalism among the pass 1 story rooms), the attack call is the first call.' Its counterexample response counts '36 of 129 rooms' that call an attack before any call to place. It reads them as rooms with no mark of their own yet ('Since we aren't doing our own', canucks), a scope condition in the bound. C2 counted the order in 93 of 129 rooms carrying both (0.721; null mean 0.487, p95 0.55), and in 91 of 129 (0.705) with joining concepts taken out of P01, from 34 transitions in 19 rooms. `mem.py findings --touching A15` returns none. P01 is read as at D3a-02: the room calls its own members, or kindred subs, to place for a work, to start, build, finish or hold it (a call to defend is P01's hold form, G11). A join or a pledge is P15's, not a call. D3a-02 named the calls whose target is another room's work as 'the call that A15 turns against a rival'. P09 is read by G20, its amendment and its readings: the room's own call, plan, claim or report of an act against a work not its own, encroachment the room admits or is told of included. An attack the room suffers is P05's, a visitor's attack is the visitor's room's unless members join it, and a taunt is P18's.

  Five readings follow from the arrow's words, as QD3-007 reads a bound in its words.
  - **The first end is a call to place.** The connection names the first call to the canvas, and the counterexample response reads the call to place as one that names the room's own mark. So the first end is P01: a call to the room's own members or kindred subs to place for the room's work. An attack call is the second end, not the first. Where the room's first call is an attack call, the line shows the bound's pattern.
  - **One call holding both ends.** A call to place the room's work over, into or in place of another room's work is a call to place and an attack call at once (P09's family in which covering others' work is itself the building of the room's mark). Where the room's first call is such a call, with no earlier call to place, the first act of each is one act. The order cannot be read (J, counted apart), as G46 read one offer.
  - **The second end is the room's own.** It is the room's call, plan, claim or report of an act against another room's work (G20). A visitor's attack call that no member takes up, an attack the room suffers, a taunt, defence of the room's own work and a design that covers no one are not this end.
  - **What the attack is.** The mechanism names a rival's work, and G20 counts encroachment and joke alterations as attacks. So the census records, for each line that shows the order, whether its first act against another work is a call or plan to attack, an attack carried out, claimed or reported, or encroachment the room admits or is told of.
  - **The order in words.** Where the attack's own words name the call, or the hands it brought, as their source, the order shows in the members' words, the mechanism, and the census counts it apart.

  A15 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show a call to place with no attack, an attack with no call to place, neither, or the bound's pattern;
  - a concept that shows the room's call to place and, after it, the room's call or act against another room's work, as read above, makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A15 when its concepts show the room's call to place (P01) and, after it, the room's call or act against another room's work (P09, by G20). The order is read from the concepts' hours (`cite.py`), the transitions, the reply chain, or one post whose words call to place first and then, separately, call or act against another work. A line is classed by the first act of each, as the connection counts them (G36's reading). It is rejected when:
  - the room's first attack call or act comes before any call to place (the bound's pattern, counted in the census as the bound);
  - the room's first call to place is itself a call over another room's work, or the two are reported at hours that cannot be placed against each other (J);
  - the first end shown is not a call: a join, a pledge, a report of the work's state or a celebration (counted apart);
  - only one end is shown;
  - what follows the call is not the room's act against another work: a visitor's attack no member takes up, an attack the room suffers, defence, a taunt, or a design that covers no one (counted apart);
  - the attack is first shown after hour 73, or the call is.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G34 to G38, G45 and G46. A restriction whose condition the connection, the mechanism, the bound or the counterexample response already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a). A correction states a condition that A15, its bound and its counterexample response lack, and shows the order failing without it. The falsifier's first clause, attack calls only before any call to place, is the bound's case. Its second clause, calls to place never followed by a call or act against another work, is read inside the rooms carrying both. Where calls are followed by refusal, reining in or apology (A16, P07), by terms (P08, A04), by taunts only (P18), or only by building and keeping (A01, A03), the condition is held. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  G45's readings 1, 8, 10, 11 and 12, and G46's reading 9, say how an end is placed and dated, and they apply here with A15's ends in place of theirs: a coded call above the line's concepts in their reply chain can be the first end, and the census marks the line R; a post with no code cannot be the first end; NONPORTABLE lines are particulars, and where their concepts show the order the census counts it apart, marked PO; a code in an edited submission cannot be dated by the submission's hour; a report of an attack or a call in an absent line places the act before the report, but not after an earlier act that it does not name; and a report of an attack as already done places it only before the report, while a call or an act said to be under way now is at its hour.

  The order test is written and logged before it runs: the census of the rulings by room (the order, the order named in words, the bound's pattern, one call holding both, not a call, not the room's attack, one end, after the close, other, limit), with the kind of the first attack among the order lines, beside C2's two counts, its 34 transitions and the counterexample response's 36 of 129. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P01, P09, P15, A12, A16, A17, A18, C02, K01, P14, P08, P05, P10, K02, P20, C01, P22, P04, P02, P18, A01, A02 and R01. Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines in the single instantiate packet of 78 lines, from the instantiate lines' first verb offset (430, after the verb's header line and 408 absent, 17 add-condition and 4 add-step lines), which the draw's header confirms.

- **G47's readings (D3a-42).** They apply G47, with G11, G20 and the readings of G45 and G46, and change no rule. Each was logged before the lines it governs were written. Reading 18 corrects reading 4 by G46 reading 9, and it was applied backwards by two appended re-rulings.
  1. **The called work in the attack's words.** An attack that names the work a call was for, as what it makes room for, or the errand its hands left, shows the order in the members' words ('for space for her', ChronoTrigger; 'couldn't find the eve logo', eve).
  2. **Defence.** A call to defend is a call to place, G11's hold form. Building back over a rival's work laid on the room's own work is defence, P05's, and not the second end (eagles).
  3. **One call.** A call that places the room's work by changing another room's work holds both ends, and so does a call whose answer reads its own placement as the attack (drugs, bakchodi, AyyMD). A call to place the room's colour that names no other work is a call to place only (AprilKnights).
  4. **Acts under way** (corrected by reading 18). An attack said to be under way now is at its post's hour.
  5. **Proposals.** A proposal to the room to build is a call to start (factorio).
  6. **NONPORTABLE lines** are not marked PO where the only call is itself over another work, or where the attack cannot be placed after the call (europe, onepunchman, brasil).
  7. **Challenges.** A challenge to answer a rival on the canvas that names no act against its work is a call to the canvas, the first end (mexico, brasil).
  8. **One end and the bound.** A line whose concepts show only calls or acts against other works shows one end (ice_poseidon). The bound's pattern needs a call to place shown after the first attack (canucks, lakers).
  9. **Past placing.** A report that a member was already placing over another work places the act only before the report (brasil).
  10. **Figures and intruders.** A call to paint over a figure that the record does not show laid on the room's work is an act against another work (monero). Clearing works that the room names as intruders on its own place is defence (farmcarrots).
  11. **Neighbours' calls.** Another room's call to the room's members to place the room's own work is the first end (starcitizen).
  12. **Placement named in the call.** A post whose call names its own placement over another work holds both ends (startrek, drugs, popheads). A reply by another member that proposes such a placement comes after the call (scotland).
  13. **Edits.** An edit that adds an attack to a post places the attack after the post (utaustin).
  14. **Rooms that cover.** A room whose every call places its colour by covering what others built holds both ends in each call (theblackvoid).
  15. **Play** between the room's own sides is not an act against another work (transformers).
  16. **Visitors.** A visitor's attack call that no member takes up, with no call to place, shows neither of the room's ends (philippines).
  17. **Labour, place and ease.** An attack that names the called work's labour shows the order in words ('have half the work done already', spain). An attack that names only a place or an ease does not (scotland, muse).
  18. **Acts continuing from before** (settled while ruling the restrict lines, applied backwards). By G46 reading 9, an act reported as continuing from before is placed only before the report. Two instantiate lines move from the order to one call by appended re-rulings (buffalobills-059, floridagators-043). The other lines that rest on reading 4 name acts under way now.
  19. **Restrict conditions.** A condition that the order does not show the call as the cause is held by A15's connection, which counts an order and not a cause. A condition that taking space is the building itself is held by reading 2. A founding attack is held by the bound and reading 14, scarce space by K02, obligations for space by P08, and an answer to erasure by P05.
  20. **Templates.** A member's request for the template is not a call to place (TeamDignitas).
  21. **The room's own work.** A member's attack on the room's own work is not the room's act against another work (chicago).
  22. **Taunts on the canvas.** A taunt that the room writes as its message is P18's, not an attack (bostonbruins).
  23. **Enlargement.** An enlargement whose own placement covers another work holds both ends (cmu). A later expansion into a neighbour's art, told of after the first call, is encroachment after it (bisexual).
  24. **After the close.** Calls after hour 73, on this canvas or another, are after the close (cubers).
  25. **The record supplies the first end only** (G45 reading 1). A line whose own concept is defence is read by that concept (completeanarchy).
  26. **AC.** The census marks the lines whose words place the attack after the room's own work was complete. The order holds there, but the mechanism's words do not name such an attack.
  27. **Jokes.** A crude joke that names no other work is not an attack (denverbroncos, glasgow).
  28. **Denials.** Where members deny that the room controls an attack, the room's earlier attack call still counts, and the denial is P21's (megaman).
  29. **No actor.** A report of displacement that names no actor does not show the room's act (math).
  30. **Removal named.** A challenge whose words name the rival work's removal is an attack call (osu).
  31. **The called work turned.** An attack whose words name the called work as what turned on others shows the order in words (minecraft).
  32. **Visitors pointed elsewhere.** A member who points a visiting room's erasers at other works does not make the act the room's (stargate).
  33. **Explanations.** An explanation to a newcomer of how to place is not a call for the room's work (romania).
  34. **Not meant.** A proposal that its writer marks as not meant is K01's frame (twitchplayspokemon).
  35. **Building first.** Where the record shows the room's work built and then destroyed before the first attack among the concepts, the attack-first order is not the bound's pattern (thesilphroad).
  36. **Withdrawn plans.** A sincere plan that its writer later withdraws by an edit still shows the plan at its hour, and the withdrawal is A16's (re_zero, satania).

- **G48 (logged at D3a-43, before any of A16's lines was read or ruled).** A16 is a standing arrow from C2, P09 → P07, of kind order and strength strong. Its gloss: 'an attack call is refused inside the room'. Its connection reads: 'in a room carrying both, the room's first call or act against another room's work comes before its first sparing, refusal, apology or reining in'. Its mechanism begins: 'A call to attack makes an answer from the room due in its thread.' Members who do not want the attack 'refuse it, rein in the attackers or apologise to the target', and in written replies a refusal 'usually comes with a reason (23 of 38 read pairs, F-014)', a reason that states the room's norm or the attack's cost. It fails if 'In a room, sparing and restraint come only before any attack call, or attack calls draw no refusal. Or refusals of attack calls come as bare as acceptances.' The arrow records this failure as present. Its bound: 'Partly constitutive: reining in the room's own attackers needs an attack to rein in. Where sparing is tacit and comes first (touhou at h3.6, calgaryflames at h9.9), restraint precedes any attack call.' Its counterexample response counts '22 of 104 rooms spare before any attack call' and keeps the arrow strong 'with the tacit-sparing path as a scope condition'. C2 counted the order in 82 of 104 rooms carrying both (0.788; null mean 0.529, p95 0.606), from 127 transitions in 52 rooms where a refusal answers an attack call within minutes. Its three support transitions are refusals in reply (nyjets, leafs, Temple). `mem.py findings --touching A16` returns none. P09 is read by G20, its amendment and its readings, with G47's readings of what counts as the room's attack. P07 is read by G19 and its readings.

  Four readings follow from the arrow's words, as QD3-007 reads a bound in its words.
  - **The first end is the room's attack.** It is the room's call, plan, claim or report of an act against another room's work (G20). Defence of the room's own work or place, a visitor's call that no member joins, a taunt, play, a joke that names no work and an attack on the room's own work are not this end (G47's readings). A call that places the room's work over another room's work is an attack call here, since this arrow orders the attack, not the call to place.
  - **The second end is the room's restraint toward another room's work** (G19): sparing it, refusing an attack call, reining in the room's own attackers, apologising for damage, restoring what the room damaged, or stating the room's norm against covering others' work. An appeal against attacks on the room's own work is P07's (G19), but it is not the restraint the connection lists, so it is counted apart. A refusal of a visitor's attack call shows the answer the mechanism names, but not the connection's order, since the call is not the room's (G20). It is counted apart.
  - **The answer in the thread.** The mechanism names an answer that the attack call makes due in its thread. So the census records, for each line that shows the order, whether the restraint answers the attack call in its reply chain or thread, or follows it only by the hours.
  - **The reason.** The mechanism says that a written refusal usually gives a reason, the room's norm or the attack's cost. So the census marks each refusal or reining in that answers in the thread as giving a reason or as bare, beside F-014's 23 of 38.

  A16 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show an attack with no restraint, restraint with no attack, neither, or restraint first (the bound's pattern);
  - a concept that shows the room's attack and, after it, the room's restraint toward another room's work, as read above, makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A16 when its concepts show the room's call or act against another room's work (P09, by G20) and, after it, the room's sparing, refusal, apology, reining in or restoring (P07, by G19). The order is read from the concepts' hours (`cite.py`), the transitions, the reply chain, or one post whose words attack first and then, separately, hold back. A line is classed by the first act of each, as the connection counts them (G36's reading). It is rejected when:
  - the room's first restraint comes before any attack call or act (the bound's pattern, counted in the census as the bound);
  - the first attack and the first restraint are one act, or are reported at hours that cannot be placed against each other (counted apart);
  - the first end shown is not the room's attack, as read above (counted apart, with a refused visitor's call apart again);
  - what follows the attack is not restraint toward another's work: help, terms, defence, a taunt, an appeal against attacks on the room's own work, attribution or a move (counted apart);
  - only one end is shown;
  - the attack or the restraint is first shown after hour 73.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G34 to G38 and G45 to G47. A restriction whose condition the connection, the mechanism, the bound or the counterexample response already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a). A correction states a condition that A16, its bound and its counterexample response lack, and shows the order failing without it. The falsifier's first clause, restraint only before any attack call, is the bound's case. Its second clause, attack calls that draw no refusal, is read inside the rooms carrying both, where the attack is met by acceptance, by terms (A17, P08), by taunts (A18, P18) or by no reply (P15). Its third clause, refusals as bare as acceptances, is F-014's, and the census reports the reasons beside it. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  G45's readings 1, 8, 10, 11 and 12, G46's reading 9, and G47's readings 2, 8, 10, 13, 15, 16, 18, 21, 22, 27, 28, 32, 34 and 36 say how an end is placed and dated and what counts as the room's attack. They apply here with A16's ends in place of theirs: a coded attack call above the line's concepts in their reply chain can be the first end, and the census marks the line R; a post with no code cannot be the first end; NONPORTABLE lines are particulars, and where their concepts show the order the census counts it apart, marked PO; a code in an edited submission cannot be dated by the submission's hour; a report of an act as done or as continuing places it only before the report; and a plan that its writer withdraws later shows the plan at its hour and the withdrawal as restraint after it.

  The order test is written and logged before it runs: the census of the rulings by room (the order, answered in the thread or by the hours; the bound's pattern; one act; not the room's attack; a visitor's call refused; not restraint; one end; after the close; other; limit), with the reasons of the answers in the thread beside F-014's 23 of 38, and the shares beside C2's 82 of 104 and the counterexample response's 22 of 104. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P09, P07, A15, A17, A18, A05, P08, P05, P18, P15, P16, P10, K02, P20, P21, C01, C02, K01, P14, P22, P04 and A12. Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (357, after the verb's header line and 329 absent, 17 add-condition and 10 add-step lines), which the first draw's header confirms. The three instantiate packets hold 100, 100 and 37 lines.

- **G48's readings (D3a-43).** They apply G48, with G19, G20 and the readings of G45 to G47, and change no rule. Each was logged in the diary, with its rooms and codes, before the lines it governs were written: readings 1 to 51 in the instantiate pass, 52 to 88 in the restrict and add passes, and 89 to 111 in the absent pass. A later note corrects the log of reading 99, which called indieheads-061 an observed-absent line; the line is not one, and its reject stands. The readings fall under eight heads.
  1. **Whose call.** A call is a visitor's when its writer speaks to the room from outside: a visiting faction's proposal (reading 1), members named in the third person (12, 28), a request for help that members answer as coming from outside (27), a call its writer cross-posts from another room (40), and another team's fans asking for help (50). A refused visitor's call is counted apart. The target's plea is not the room's restraint (11, 48, 62, 74, 82), and neither is a reply whose writer's side cannot be read (67, 74, 103) or a visiting helper's (73). A writer who joins the room's effort and also belongs to the target speaks for the room (77, 102).
  2. **What the first end is.** A call to wreck things with no target named is an attack call ('Lets fuck this shit up', dota2; reading 14). So is a spread or a placement whose reply names the work it would cover (4, 15, 25, 60), a call against a neighbour that members say was there first (21, 30, 88), and a defence of a takeover as fair play (39). These are not the room's attack: a spread that names no other work (8), a temptation in jest or a mock war (16, 65, 91), an alarm (17), a taunt (34, 55), defence of the room's own work or place, retaking included (19, 22, 49, 76, 86, 93), an attack the room suffers (13, 57, 76, 80, 90, 93), a symbol or slogan that names no other work (68), and an addition to the room's own work (59).
  3. **Placing the ends.** A post with no code cannot be the first end (2). A coded post above the line's concepts in their reply chain can be the first end or the first restraint, and the census marks the line R (24, 36, 37, 47, 85). The room's act that a neighbour tells of is the room's act, meant or not (3, 58, 71). A report of the room's act as done or under way places it before the report, so a post that reports the act and holds back shows the order in its words (9, 35, 36, 43, 63, 75, 81, 92, 96, 98, 99). A call whose own words limit it is one act ('We will spare those that come in goodwill, such as creative artwork.', pcmasterrace; reading 33). Restraint before the first coded attack is the bound's pattern (24, 64, 87, 94, 100, 109, 111). A reply at hour 73.00 is at the close (7).
  4. **What restraint is.** Sparing, refusing, reining in, apology and restoring are restraint, and so is the caller's own withdrawal (31). These are not: attribution (20, 101), a deferral that keeps the attack (29, 79), terms (54, 100), a move (90, 93), an apology that keeps the act (61, 90), mock disapproval (77), a lack of hands or a promise to relay concerns (79), guilt or regret that does not stop the act (62, 111), a dispute over a taunt's words (41), and an answer that neither stops, spares, restores nor apologises (84). A bare why-question is not yet a refusal ('Y tho', ice_poseidon; reading 26). A question that names the norm, the cost or the room hurt is one (38, 44, 66, 83).
  5. **Reasons.** RSN marks a refusal or reining in that states a stance or norm, cites an agreement or alliance, names a cost, puts the room's own work first, or gives even a joke reason. BARE marks a refusal with no reason, a rebuke or a suggestion that gives none (6, 18, 42, 51, 72, 88). A line is marked by its first answer in the thread (6).
  6. **The thread and the hours.** An answer posted in the call's thread, but not in its reply chain, answers in the thread (32, 46). Where the first attack call draws no answer and the first restraint answers a later call elsewhere, the line shows the order by the hours (70, 78).
  7. **Restrict and add conditions.** A condition that a refusal can be bare, or that restraint does not show compliance, is held by the mechanism's word usually and by the connection, which counts an order (52). A joke reason does not show the order failing, and its wording goes to D3c (53).
  8. **Absent lines.** They are rejected by the first act of each, as instantiate lines are classed (89, 95). An observed-absent line whose concepts show an attack with no restraint, or neither end, is a specification (97, 102, 105, 109).

- **G49 (logged at D3a-44, before any of A17's lines was read or ruled).** A17 is a standing arrow from C2, P09 → P08, of kind order and strength fair. Its gloss: 'an attack call is met with a truce'. Its connection reads: 'in a room carrying both, the room's first call or act against another room's work comes before its first border talk, truce or deal'. Its mechanism: 'A call to attack is met by the room's relations with its neighbours: the room invokes a truce, or proposes a deal instead.' It fails if 'In a room, border talk comes only before any attack call, or attack calls are never answered with talk.' The arrow records this failure as present. Its bound: 'Early side only: on the late side border talk comes first (0 of 4 hold), since late rooms meet neighbours before any attack.' Its counterexample response counts '77 of 172 rooms talk borders before any attack call; all four late rooms do.' It answers with 'a scope condition (the late side) and fair strength'. C2 counted the order in 95 of 172 rooms carrying both (0.552; null mean 0.423, p95 0.477), from '73 transitions in 35 rooms where a truce or deal is invoked in reply to an attack call'. Of its three support transitions, czech passes the audit, and PlaceNL and thailand fail it, since in each the first border talk comes before the first attack. `mem.py findings --touching A17` returns none. P09 is read by G20, its amendment and its readings, with G47's and G48's readings of what counts as the room's attack. P08 is read by G18 and its readings.

  Four readings follow from the arrow's words, as QD3-007 reads a bound in its words.
  - **The first end is the room's attack,** read as G48 reads it: the room's call, plan, claim or report of an act against another room's work, with a visitor's call counted apart.
  - **The second end is the room's talk of terms with another room** (G18): proposing or asking a border, a space, a truce or a deal; settling one; contesting one; holding each other to one; or a member reporting such terms to the room or asking members to keep them. G18 reads this talk from either room's record, so a neighbour's offer or request to the room counts, one offer with no reply being P08's lower range. Restraint that names no terms is P07's and not this end (G18's appeals with no terms). So are help traded for help (P16), an alliance to defend each other (P17), taunts with no terms (P18), a member's proposal to ask with no request made, and a lone placer's talk (G18's readings).
  - **The answer in the thread.** The mechanism says the attack call 'is met' by this talk. So the census records whether the talk answers the attack in its reply chain or thread, or follows it only by the hours.
  - **Invoking or proposing.** The mechanism names two forms: the room 'invokes a truce, or proposes a deal instead'. So the census marks each answer in the thread as invoking terms already made (INV), proposing or settling new terms (DEAL), or another form of P08 (OTHER: contesting or refusing terms, a breach complaint, or a report of terms).

  A17 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show an attack with no talk of terms, talk of terms with no attack, neither, or the talk first (the bound's pattern);
  - a concept that shows the room's attack and, after it, talk of terms between the room and another room, as read above and classed by the first act of each (G48's reading 95), makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A17 when its concepts show the room's call or act against another room's work (P09, by G20) and, after it, talk of terms between the room and another room (P08, by G18). The order is read from the concepts' hours, the reply chain, coded posts above the concepts, or one post whose words attack first and then, separately, talk terms, as G48's readings place the ends. A line is classed by the first act of each. It is rejected when:
  - the first talk of terms comes before the first attack (the bound's pattern, counted in the census as the bound);
  - the first attack and the first talk of terms are one act, as when one post offers terms backed by a threat, or are reported at hours that cannot be placed against each other (counted apart);
  - the first end shown is not the room's attack (counted apart, with a visitor's call answered by terms apart again);
  - what follows the attack is not talk of terms: restraint that names no terms, help, a move, an alliance, a taunt or attribution (counted apart);
  - only one end is shown;
  - the attack or the talk is first shown after hour 73.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G45 to G48. A restriction whose condition the connection, the mechanism, the bound or the counterexample response already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a). A correction states a condition that A17, its bound and its counterexample response lack, and shows the order failing without it. The falsifier's first clause, border talk only before any attack call, is the bound's case. Its second clause, attack calls never answered with talk, is read inside the rooms carrying both, where the attack is met by restraint that names no terms (A16, P07), by acceptance, by taunts (A18, P18) or by no reply (P15). Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  G48's readings under its heads 1 to 3 (whose call, the first end, placing the ends) and 6 (the thread and the hours) apply here with P08 in place of P07, as do the readings of G45, G46 and G47 that G48 applied. Its heads 4 and 5 (what restraint is, and reasons) do not, since this arrow's second end is terms, and G18's readings decide what talk is terms. The target's reply is not set apart here, as it was under G48: talk of terms is between two rooms, and G18 reads it from either side. The bound names an early and a late side, which the lines do not show. So the census reports the bound's pattern by room, beside the counterexample response's count.

  The order test is written and logged before it runs: the census of the rulings by room (the order, answered in the thread or by the hours; the bound's pattern; one act; not the room's attack; a visitor's call answered; not terms; one end; after the close; other; limit), with the forms of the answers in the thread (INV, DEAL, OTHER), and the shares beside C2's 95 of 172 and the counterexample response's 77 of 172. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P09, P08, A16, A04, A05, A14, A21, P07, P16, P17, P18, P15, P05, P10, K02, P20, P21, C01, C02, K01, P14, P22, A15 and A18. Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (432, after the verb's header line and 422 absent, 7 add-condition and 2 add-step lines), which the first draw's header confirms. The two instantiate packets hold 100 and 56 lines.

- **G49's readings (D3a-44).** They apply G49, with G18, G20 and the readings of G45 to G48 that G49 names, and change no rule. Each was logged in the diary, with its rooms and codes, before the lines it governs were written: readings 1 to 67 in the instantiate pass, 68 to 99 in the restrict pass, 100 to 104 in the add passes, and 105 to 146 in the absent pass. Three later readings correct earlier logs before any row was built: reading 43 moves cfb-054 from the order to the bound, reading 45 moves neopets-055 from one act to the order in a post's words, and reading 126 moves ghibli-057 from an evidence limit to a reject. The readings fall under eight heads.
  1. **Whose call.** A call is a visitor's when its writer addresses the room from outside or invites it into an outside front (readings 4, 32, 49). A visitor's call answered by terms is counted apart (V), and one not answered by terms is not the room's attack (62). A visitor's threat against the room is an attack the room suffers (38). A writer's flair in the room places a call as the room's (62).
  2. **What the first end is.** A call to fight back or retaliate is the room's attack, and retaking the room's own work is defence (1, 25, 34, 48). A call to defend or reclaim a place that the reply says the neighbour held first, or holds by agreement, is the room's attack (18, 25, 48, 57). The room's act that a neighbour tells of is the room's act, even inside the neighbour's threat or plea (22, 68, 77, 106). A placement whose reply names the work it would cover is an attack call, as G48's reading 4 (84, 133, 136, 138). Fighting or clashing with named rooms over a space, and reciprocal overwriting, are the room's act (80, 126). A claim to a place backed by a threat of war is the room's attack (127). These are not: a jest (29, 125), a slogan or a spread that names no other work (20, 113), a taunt (139), and a member's account that the room was there first and defends (113, 139).
  3. **What talk of terms is (G18).** An alliance with the target, named as standing between the rooms, is terms held. Friendship, being supposed to work together, and a stated reciprocity with no agreement are not (2, 16, 17, 39, 60). The target's report that it is making an alliance with the room, given as the reason the attack will fail, is terms; an alliance proposed apart from the attack is P17's (61, 109). A member's proposal inside the room to ask, ally, compromise or make a truce, with no request made, is not terms (3, 14, 23, 37, 64, 74), and a request reported made is (11, 65). The target's or a neighbour's offer counts, one offer being the lower range, even when backed by its own threat (10, 26). Help traded for help is P16's, and help offered for an end to interference is terms (26, 81). Joint fights, and coalition plans that name no border, are P17's (15, 70, 77, 103). A third room's agreement that the target reports is not this room's terms (52); a sister room's treaty with the target is (30). A lone placer, or a maker not shown to speak for a room, does not talk terms (41, 76). An appeal to stop that names no place is P07's (93, 118), and disputing a space or a border contests terms (114, 115, 127).
  4. **Placing the ends.** A line is classed by the first act of each. A coded post above the line's concepts in their reply chain can be the first end or the first talk, and the census marks the line R (19, 28, 43, 75, 82, 84, 96). Coded talk before the first coded act of the room's is the bound's pattern (5, 28, 43, 46, 70, 78, 85, 97). A reply that reports terms made earlier is talk shown at the reply's hour, after the attack it answers, as every INV line is; so a post that reports the room's act as done or going on, and then talks terms, shows the order in its words (13, 24, 35, 45, 86, 93). One post that calls an attack and sets terms aside, cites a breach, or offers terms backed by a threat is one act (6, 42, 50, 87), and so are an act and talk at hours that cannot be placed (73, 88).
  5. **The thread and the hours.** Terms first shown in another thread than the first call follow it by the hours (54, 82, 94). An edit in the acting post that reports peace, talks or a plan sent shows the order in the post's words (9, 66).
  6. **Forms.** The first answer in the thread is marked INV where terms already made are invoked, DEAL where new terms are offered, asked or settled, and OTHER where it reports terms with a third room, contests terms, or mourns a breach (8, 19, 53, 64).
  7. **Restrict and add conditions.** A condition that the talk answers a complaint, an accusation or an act, and not a call, is held by the connection's 'call or act' (68). A condition that the agreement is invoked and not caused is held by the mechanism and the connection (69). A condition that talk can come first, or that a deal can oblige an attack on a third room, is held by the bound, the counterexample response and P17 (70). A condition that the talk answers an alarm or a defence call is held by the connection's first end (71). An attack met by assent is the falsifier's second clause, recorded present (100).
  8. **Absent lines.** They are rejected by the first act of each, as instantiate lines are classed, and NONPORTABLE lines are particulars, marked PO where the order shows (105, 122, 142). An observed-absent line whose concepts show an attack with no terms is a specification (116, 119, 128, 131, 134).

- **G50 (logged at D3a-45, before any of A18's lines was read or ruled).** A18 is a standing arrow from C2, P09 → P18, of kind order and strength fair. Its gloss: 'an attack is carried on in taunts'. Its connection reads: 'in a room carrying both, the room's first call or act against another room's work comes before the first taunt, chant, claim of victory or salute with a rival'. Its mechanism: 'An attack makes the rival a named party, and the contest is carried on in talk: taunts, chants, claims of victory, a salute after the fight.' It fails if 'In a room, rivalry talk comes only before any attack, or an attack is never followed by talk with or about the rival.' The arrow records this failure as present. Its bound: 'Early side only: no late-side room carries both.' Its counterexample response counts '12 of 68 rooms taunt before any attack, among them rooms whose rivalry comes from outside the canvas.' It answers that 'the arrow cannot be tested on the late side, so it is fair, not strong.' C2 counted the order in 56 of 68 rooms carrying both (0.824; null mean 0.591, p95 0.676), from '50 transitions in 14 rooms where a taunt answers an attack call'. Its pass 4 count found 2 of the 68 rooms with no taunt after the first attack. Of its three support transitions, rpi and anarcho_capitalism pass the audit, and clg fails it, since its first taunt (h12.62) comes before its first attack (h37.54). `mem.py findings --touching A18` returns none. P09 is read by G20, its amendment and its readings, with G47's, G48's and G49's readings of what counts as the room's attack. P18 is read by G21, its amendment and its readings.

  Five readings follow from the arrow's words, as QD3-007 reads a bound in its words.
  - **The first end is the room's attack,** read as G48 and G49 read it: the room's call, plan, claim or report of an act against another room's work. A visitor's call is counted apart. An attack the room suffers is P05's (G20). Where the room's taunt follows such an attack, the rival is a named party, as the mechanism says, but the connection's order is not shown, since the attack is not the room's. The census counts these lines apart.
  - **The second end is the room's contest in talk with a rival** (P18, by G21 as amended): a taunt, insult, threat or chant aimed at a rival group; flooding or raiding its threads, or a call to do so; a claim of victory, or gloating at a loss; a salute or respect paid after a fight; blame of attackers after the close; lettering aimed at a rival that covers no work; and an apology, or a call to stop, for a row in words that the room took part in. G21 reads P18 as the room's own part, as G20 reads P09. So a taunt by a visitor or by the target in the room's threads is not this end, unless members answer in kind or carry it on. These are not this end: a plain report, a defence call that names the attacker, restraint (P07), terms (P08), help (P16), an alliance (P17), celebration with no rival named (P11), and mourning with no rival blamed (P12).
  - **The rival.** The mechanism says that the attack makes 'the rival a named party'. So the census marks each order line SAME where the first taunt names, answers or aims at the attack's target, and ELSE where it aims at another group. The connection orders the first act of each, so both show the order.
  - **The answer in the thread, and the forms.** C2 grounded the arrow on transitions where a taunt answers an attack call. So the census records whether the first taunt answers the attack in its reply chain or thread, or follows it only by the hours or in a post's own words. It marks the first taunt of each order line by the forms the mechanism names: TAUNT (a taunt, insult, threat, chant or lettering), VICT (a claim of victory, or gloating), SALUTE (a salute, respect, or an apology or call to stop for the row), FLOOD (flooding or raiding threads) and BLAME (blame of attackers after the close).
  - **The close.** P18 reaches past the close: G21 counts threats, war chants and victory claims after hour 73, and P18's statement names blame of attackers after the close. So a taunt after hour 73 that follows an attack shown before it shows the order, and the census marks the line AC. An attack call first shown after hour 73 is talk about the canvas (G20), and the line does not show the order.

  A18 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show an attack with no taunt, a taunt with no attack, neither, or the taunt first (the bound's pattern);
  - a concept that shows the room's attack and, after it, the room's taunt with a rival, as read above and classed by the first act of each (G48's reading 95), makes the claim of absence fail (reject), whatever the line's observation;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A18 when its concepts show the room's call or act against another room's work (P09, by G20) and, after it, the room's taunt, chant, claim of victory, salute or other contest in talk with a rival (P18, by G21). The order is read from the concepts' hours, the reply chain, coded posts above the concepts, or one post whose words report the room's act as done or under way and then, separately, taunt, as G48's readings place the ends. A line is classed by the first act of each. It is rejected when:
  - the first taunt comes before the first attack (the bound's pattern, counted in the census as the bound, and marked PRE where the line's concepts name a rivalry from before the canvas, as the counterexample response names);
  - the first attack and the first taunt are one act, as when one post calls an attack in words that insult its target, or one design covers a work and mocks its makers, or they are reported at hours that cannot be placed against each other (counted apart);
  - the first end shown is not the room's attack (counted apart; a taunt that follows an attack the room suffers, and a visitor's call answered by taunts, apart again);
  - what follows the attack is not the room's taunt with a rival, as read above (counted apart);
  - only one end is shown;
  - the room's first attack is first shown after hour 73.

  A restrict or contradict line is ruled by G9, read for an arrow, as under G45 to G49. A restriction whose condition the connection, the mechanism, the bound or the counterexample response already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a). A correction states a condition that A18, its bound and its counterexample response lack, and shows the order failing without it. The falsifier's first clause, rivalry talk only before any attack, is the bound's case. Its second clause, an attack never followed by talk with or about the rival, is read with the mechanism's talk, the contest carried on (P18). It is read inside the rooms carrying both, where the attack is met by restraint (A16, P07), by terms (A17, P08), by acceptance (P15) or by no reply. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2.

  G48's readings under its heads 1 to 3 (whose call, the first end, placing the ends) and 6 (the thread and the hours), and G49's under its heads 1, 2, 4 and 5, apply here with P18 in place of P07 and P08, as do the readings of G45 to G47 that G48 applied. G48's heads 4 and 5 and G49's heads 3 and 6 do not, since this arrow's second end is a taunt, and G21's readings decide what talk is a taunt. As under G48, and not as under G49, the target's reply is set apart: a taunt is one room's act, and G21 reads it from the room's own record. The bound names an early and a late side, which the lines do not show. So the census reports the bound's pattern by room, beside the counterexample response's count.

  The order test is written and logged before it runs: the census of the rulings by room (the order, answered in the thread or by the hours; the bound's pattern; one act; not the room's attack; a taunt after an attack the room suffers; a visitor's call answered by taunts; not a taunt; one end; after the close; other; limit), with the forms, the rival marks (SAME, ELSE), the AC and PRE marks, and the shares beside C2's 56 of 68 and the counterexample response's 12 of 68. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P09, P18, A15, A16, A17, P05, P07, P08, P11, P12, P15, P16, P17, P20, P21, P22, C01, C02, K01, K02, P10 and P14. Candidates hold no line (R02, P06, P19, K03, K04). A rivalry from outside the canvas is K03's form where it is an old quarrel, and C02's where a tie from before the canvas names the rival in the attack turn. Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (442, after the verb's header line and 431 absent and 10 add-condition lines), which the first draw's header confirms. The two instantiate packets hold 100 and 17 lines.
- **G50, amendment 1 (D3a-45, 20 October 2026, before any A18 line was ruled; it applies to every A18 line, and no line was ruled before it).** G50 gave, as one act, a design that covers a work and mocks its makers. G20 reads a joke alteration of another's work as P09's move, and G21 reads lettering aimed at a rival as P18's taunt only where it covers no work. So a design that covers another's work is the attack, whatever its words say, and it is not also the first taunt. The first taunt is the next act that carries the contest on in talk, or lettering that covers no work. A post that calls an attack and, in its own words, taunts or abuses the rival group stays one act.
- **G50's readings (D3a-45).** They apply G50, with its amendment 1, G20, G21 and the readings of G45 to G49 that G50 names, and change no rule. Each was logged in the diary, with its rooms and codes, before the lines it governs were written: readings 1 to 62 in the instantiate pass, 63 to 115 in the restrict pass, 116 to 121 in the add-condition pass, and 122 to 204 in the absent pass. One later note corrects the closing tally of the log of readings 122 to 128 (window ab001_000 holds four rejects, not five); no row changed. The readings fall under eight heads.
  1. **Whose call, and whose taunt.** The target's reply, threat, offer or friendly note is set apart, even when signed by its room, and so is a member's amused reply to it (8, 36, 45, 59, 60, 77, 105). In a shared league, national or city sub, fans or members of rival clubs, teams or faculties speak for rival groups, so a taunt by one on the target's side is the target's reply (32, 94). A visitor's justification, slogan, chant, flood or sarcastic answer is the visitor's (36, 79, 107, 110). A call cross-posted from another room, and a call or taunt whose writer's side cannot be read, are not the room's (9, 108, 186). A visitor's call stays the visitor's, and a member's later act is the room's (102). A taunt that rests on a visitor's call to drive out a third room does not show the order (167). A reply that mocks the room's own member for ruining another's space speaks against the room's act (19), and thanks to an unknown placer for altering a rival's logo is not the room's act (201). No line shows a visitor's call answered by the room's taunts: where a visiting fan's call is followed by another rival's attack and the room's taunt at it, the taunt answers the attack the room suffers (97).
  2. **What the first end is.** An attack made during placement and told of after the close is the room's attack, placed before the report (1, 13). A call to fight back, give a rival a fight, retaliate or take revenge is the room's attack, even after an attack the room suffers (101, 125, 138, 170; G49 reading 1). A call to remove invaders from the room's own place, to take back what members say a neighbour stole, to retake land, to strike the Void in defence of the room's flag, or to sever a work that strangles the room's work, is defence (9, 15, 123, 141, 174, 199). A plan to erase a work that holds its place by agreement is the room's attack (54). The room's act that a neighbour or a visitor tells of, in a complaint, a charge, a plea, a request, a lament or a claim to have been there first, is the room's act (124, 129, 137, 143, 164, 169, 176, 182, 187, 198). A placement whose reply names the work it would cover is an attack call (184, 193; G48 reading 4). The room's attack also covers fighting or clashing with named rooms over space (31, 200, 203; G49 readings 80 and 126), a member's readiness to strike a work at an ally's request (126), a stance to cover anyone who builds on the room's chosen place (189), a call to erase content the room objects to (146), a covert attack (144), and a slogan that calls members to smash a rival (157). These are not the room's attack: a jest of war or a joking wish to alter a work (49, 87, 153), a proposal to expand that names no work (42), an argument among members over who attacked (41), contests between factions inside one room (167, 202), and a member of a shared city sub who griefs the room's own work (148). A member's flat denial of an act that a neighbour tells of leaves the act open (41), and a denial does not undo the room's call (104). A war call in a post with no code cannot be the first end (12).
  3. **What the room's taunt is (G21).** These count: a justification in sarcastic words (2); a joking taunt or a joke threat at the rival (11, 25); a declaration of war posted in the rival's sub or addressed to its representative (16, 73); a mock declaration of war, a mock-apologetic or mocking refusal, or a dismissive retort to the target (17, 30, 39, 43, 61, 91, 155); a rebuke that insults a visitor (18); lettering on the room's own space, or beside a rival's work, that covers no work (20, 159); mockery of the rival's flag, or a jab at the rival (29, 47); a threat to vandalize (113); a threat to downvote the rival's threads, which is flooding (114); an ultimatum (92); mock news of a work's death, and mock mourning (156, 165); condemnation or reproach of a rival group's conduct, which is blame (51, 96); a defence call that adds an insult beyond naming the attacker (133); shaming a raiding room after the close (162); and a line of an anthem aimed at the rival (56). These do not count: a plain justification or a rhetorical question (2, 17, 60); laughter alone in a report (5); a bare claim of success that names no rival (59, 159, 174, 179); a defence call that names or slights the attackers (66, 127, 179); a plain account that a neighbour stole, or keeps messing with the room (15, 133); a record that names a griefer without reproach (67, 148, 153); a plain refusal to move or to give territory back (128, 167); a request that a neighbour be smaller, which is terms (68); a joking objection inside talk of compromise (84); thanks and peace after an encroachment the room undoes (88); a challenge about another venue (82); a mock war that never names the canvas (135); a moral contrast with, or laughter at, rooms the room does not contest with (148, 201); an insult at the source of a borrowed design, and a dry remark to a member (141); mockery, accusation or shunning inside the room (83, 174, 204); and a slight at a rival's text in a report of its plan (204). A jab or a contest with one individual, one vandal or one self-named representative does not count (68, 89, 135, 159, 204), while G21's amendment 1 counts blame of one placer after the close (133, 150, 166). Jabs at diffuse opponents who form no group do not count either (116). A war cry, a cheer or an assent that answers the room's own attack call joins it (14, 37, 38, 141, 186).
  4. **Placing the ends.** A line is classed by the first act of each (G48 reading 95). Under amendment 1, a design that covers another's work is the attack, and so are a call to write an insult or a score over a work, lettering that alters a rival's area, a later act against the same work, and a notice of erasure with a courtesy apology; the first taunt is the next act (3, 14, 38, 130, 149, 154, 180). A post that reports the room's act as done or under way and then taunts, gloats or salutes shows the order in its words (6, 24, 28, 78, 85, 102, 103, 107, 134, 139, 166, 191, 196, 199, 202). A post that calls or plans an attack and taunts, abuses or condemns the rival in its own words is one act (4, 57, 71, 81, 120, 153, 194), and so is a call that boasts of taking a rival down again (141). A call that slights the target or names it by a common slighting name, that is framed as annoying the rival or teaching it a lesson, that boasts of the room itself, or that cites a rivalry from outside the canvas, is the call alone (4, 33, 49, 80, 95, 110, 172, 186). Acts at hours that cannot be placed against each other are one act (10, 93, 106). A coded post above the line's concepts can hold the first end, and the census marks such instantiate, restrict and add lines R (17, 46, 73, 112); absent rejects rest on such posts too (176, 184, 193, 198). A first taunt in another thread, minutes before an answer in the call's thread, places the line by the hours (52).
  5. **An attack the room suffers, and the bound.** A taunt of the room's that follows an attack it suffers, or its defence, is counted apart as SUF, even where the same answer calls for retaliation (7, 22, 35, 44, 53, 72, 79, 86, 100, 118). An attack the room suffers with no taunt of the room's is not the room's attack (7, 67). Where the room's own first attack comes after such a taunt, the line shows the bound's pattern, and SUF is kept for lines with no attack of the room's before the taunt (48, 64, 76, 90, 109, 114). Bound lines that name a rival from outside the canvas are marked PRE (65, 109). A taunt before any attack of the room's, followed only by attacks it suffers, shows one end (75). On absent lines, rivalry talk before the room's first attack does not make the claim fail (128, 148, 159, 174, 186, 194, 201, 204).
  6. **The rival, the forms, the thread and the close.** The first taunt is marked SAME or ELSE against the first attack's target (21, 37, 46, 51, 74, 108, 110). A rival alliance inside one game's sub is a rival group (23), and so are rival fans or faculty groups in a shared sub (32, 94, 142). A claim of victory in the call's thread, but not in its reply chain, answers in the thread (62; G48 head 6). A jab with a past score, a report that the room already destroyed the target, and a claim of having kept a rival at bay are claims of victory (40, 50, 100). A gracious note to the target after the fight, and a mock memorial to a displaced maker, are salutes (55, 139). A taunt after hour 73 that follows an attack shown before it shows the order and is marked AC (13, 26, 31, 69, 82, 85, 95, 101). An attack first shown after the close is talk about the canvas, and so are a retaliation plan and a list of targets named after it (72, 83, 142).
  7. **Restrict and add conditions.** They are ruled by G9 with G50's classes: S-O-A, S-O-H and S-BOUND are specifications, and EL-NA, EL-SUF, EL-NT, EL-ONE, EL-J, EL-AFTER and EL-V are evidence limits (63, 116). A condition that the order of first acts does not prove a cause is held by the connection, which counts an order (63). A condition that the taunt aims at another opponent is held by the connection, which names a rival and not the target, and the census marks the line ELSE (63). A condition that the taunt answers an attack the room suffers is held by the connection's first end, the room's attack (64). A condition that rivalry talk can come first, or from outside the canvas, is held by the bound and the counterexample response (65), and a rivalry cited in a call is a tie of the kind C02 names in the attack turn (95). A condition that the mockery answers one vandal or diffuse opponents is held by G21's reading of rivals (116). A condition that visiting celebrants be kept apart is held by G50, which sets the taunts of visitors apart (117).
  8. **Absent lines.** They are rejected by the first act of each, as instantiate lines are classed, from the line's concepts or the coded posts above them in their chain (122). NONPORTABLE lines are particulars, marked PO where the order shows (122, 135, 142, 159). The one observed-absent line shows an attack call after the close and two refusals, and is a specification (142).

- **G51 (logged at D3a-46, before any of A19's lines was read or ruled).** A19 is a standing arrow from C2, P05 → P17, of kind order and strength thin. Its gloss: 'under attack, works defend each other'. Its connection reads: 'in a room carrying both, the first act of upkeep or defence comes before the first alliance, shared chat, joint mark or request to host'. Its mechanism: 'A room keeping its work against attack joins other rooms whose works face the same threat, and they defend each other's works together.' It fails if 'In a room, coalitions come only before any upkeep or defence, or a room under attack never joins with another.' The arrow records this failure as present. Its bound reads: 'Late side: no late room of 4 holds; late rooms enter the canvas through other rooms (bretagne, MiamiHurricanes, yuyuyu).' The bound adds that the arrow is thin, counted 'on the coalition element without hosting (pass 4)', that its pass 2 lead instance 'sits in a room that joined a coalition before any upkeep', and that 'its yugioh transition ends on a hosting ruling'. Its counterexample response counts '51 of 157 rooms join a coalition before any upkeep; the late side mostly does.' It answers with 'a scope condition (the late side) and thin strength'. C2 grounded it on '52 transitions in 28 rooms where an alliance is proposed in reply to a call to defend'. Pass 4 counted the order in 87 of 121 rooms carrying both (0.719; null mean 0.614, p95 0.678), and found 7 of the 121 with no coalition after the first upkeep. Of its three support transitions, criticalrole passes the audit. naruto fails it, since its first coalition (h32.15) comes before its first upkeep (h39.06), and yugioh fails it, since its two codes are cited under different third-order themes. Of the eight rooms C2 sampled against it, six hold and two fail (lakers, bretagne). `mem.py findings --touching A19` returns none. F-008 holds A19's count, 'counted on coalitions without hosting', and says that pass 4 took the hosting themes out of the coalition element. P05 is read by G11, as move 173 left it, with G36's, G38's and G45's readings of upkeep. P17 is read by G27 and its readings.

  Five readings follow from the arrow's words, as QD3-007 reads a bound in its words.
  - **The first end is the room's own upkeep or defence** (G11), including a warning that the work is changed and a call to defend it (P01's hold form), as G36 and G45 read. Keeping an ally's work is P17's or P16's act, not the first end. Where the first upkeep shown is done by allies or by another room's helpers, before any upkeep by the room's members, the first act of each is one act (J; G45 reading 6).
  - **The second end is the room's coalition** (P17, by G27 and its readings): an alliance formed, proposed or acted on, including allies called on or defended under it; a chat shared by several rooms; a hub of kindred rooms; a tally of kindred works; and a joint mark. The connection lists an alliance, a shared chat and a joint mark. C2 counted the order on P17's coalition themes, which also hold hubs and tallies, so these count too. The census marks the form of the first coalition act: ALLY, CHAT, HUB, TALLY or JOINT.
  - **Hosting.** A request to host, or a tie in which one room's work lives on another room's mark with no alliance named, is P19's form. P19 is a candidate and holds no line (G27's reading of hosts and guests). The connection names a request to host, but pass 4 recounted the order without hosting, F-008 says so, and the bound reads the yugioh transition as ending on a hosting ruling. So a line whose only second end is hosting is counted apart (HOST), and the connection's words go to D3c. An alliance named and acted on with a host is P17's lower range (G27).
  - **The mechanism in words.** The mechanism names rooms whose works face the same threat and defend each other's works. So the census marks an order line MW where its first coalition act names an attack, a shared threat or defence given both ways, beside C2's 52 transitions in 28 rooms.
  - **The late side.** The bound names late rooms that enter the canvas through other rooms, and the lines do not show a room's side. So the census reports the bound's pattern by room, beside the counterexample response's 51 of 157. It marks ENTRY where a line's concepts show the room entering the canvas through another room's coalition, space or offer.

  A19 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them. No A19 absent line is `observed-absent` or `not-needed`. A concept that shows the room's upkeep or defence of its own work and, after it, the room's coalition, as read above and classed by the first act of each (G48's reading 95), makes the claim of absence fail (reject). A NONPORTABLE line is a particular (G6), marked PO in the census where its concepts show the order. The other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A19 when its concepts show upkeep or defence of the room's own work (G11) and, after it, the room's coalition (G27, as read above). The order is read from the concepts' hours (`cite.py`), the reply chain, coded posts above the concepts (G45 reading 1, marked R), or one post whose words name the upkeep, the attack or the threat first and the coalition after. A line is classed by the first act of each. It is accepted as a specification when the order shows in the reply chain or thread (O-A) or by the hours or in a post's words (O-H). It is rejected when:
  - the first coalition act comes before any upkeep (the bound's pattern and the counterexample response's, counted as the bound);
  - the first upkeep and the first coalition act are one act, as when one post calls the room to defend its work with named allies, allies keep the room's work before its members do, or the two are reported at hours that cannot be placed against each other (J, counted apart);
  - the only second end is hosting (HOST, counted apart);
  - what follows the upkeep is not a coalition: terms (P08), help with no partnership named (P16), sparing (P07), calls to kindred subs to place for the room's own work (P01), the room's own chat, a visitor's offer that no member takes up, or a call to cooperate that names no partner (NC, counted apart);
  - the first end shown is not the room's upkeep of its own work (NU, counted apart);
  - only one end is shown (ONE);
  - the room's first coalition is first shown after hour 73, or on a canvas opened after it (AFTER). A pact for later events is P13's (G27). A report after the close places the act only before the report, and not after an earlier upkeep that it does not name (G45 reading 12).

  A restrict or contradict line is ruled by G9, read for an arrow, as under G45 to G50. A restriction whose condition the connection, the mechanism, the bound or the counterexample response already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a). A correction states a condition that A19, its bound and its counterexample response lack, and shows the order failing without it. The falsifier's first clause, coalitions only before any upkeep, is the bound's case. Its second clause, a room under attack that never joins with another, is read inside the rooms carrying both. Where such a room keeps by hand or by scripts (P05, A06, P14), asks for or gets help with no partnership named (P16, A13), talks terms (P08, A04), fights back (P09, P18), spares (P07), or judges its hands too few and moves (K02, A10, P10), the statement named holds the condition. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2, and F-008 would then be re-examined.

  G45's readings 1, 4, 6, 8, 10, 11 and 12 apply here with P17 in place of P16, as do G36's readings of what counts as upkeep (a call to defend counts before any damage; a warning that a neighbour approaches does not; a complaint addressed to the other side is talk). G27's readings decide what a coalition is: an alliance whose only stated term is not to harm each other's work is P08's truce; defence given both ways is P17's lower range, and protection given one way is P16's; the room must be the one that joins; a proposal must name a partner; a comparison of kindred works after the canvas joins no one.

  The order test is written and logged before it runs: the census of the rulings by room (the order, in the thread or by the hours; the bound's pattern; one act; hosting only; not a coalition; not the room's upkeep; one end; after the close; other; limit), with the forms, the MW, R, ENTRY and PO marks, and the shares beside pass 4's 87 of 121 and 7 of 121 and the counterexample response's 51 of 157. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P05, P17, A13, A14, A04, A06, P16, P08, P07, P09, P18, P01, P03, P04, P14, P10, A10, K02, P13, P20, P21, A21, C01 and C02. Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (487, after the verb's header line and 477 absent and 9 add-condition lines), which the draw's header confirms. The one instantiate packet holds 69 lines.
- **G51's readings (D3a-46).** They apply G51, G11, G27 and the readings of G36 and G45 that G51 names, and change no rule. Each was logged in the diary, with its rooms and codes, before the lines it governs were written: readings 1 to 23 in the instantiate pass, 24 to 59 in the restrict pass, 60 to 63 in the add-condition pass, and 64 to 112 in the absent pass. Two later notes correct closing tallies. Window i487_000 holds O-A 4 and O-H 4, not 5 and 3, and the absent pass holds 20 rejects and 456 limits, not 22 and 454. No row changed because of them. Five lines were re-ruled by appended lines under readings 69, 93 and 94, and one reject was withdrawn before any build under reading 83. The readings fall under eight heads.
  1. **Whose act.** A writer who addresses the room's work as yours, writes for another group, or says they come from another room is a visitor (5, 99). A visitor's offer or call counts once a member takes it up (5, 13, 29), and not before (26, 29, 62, 112). A member's consent that sends the decision to the room's working sub does not show the room joining (110). A cross-posted message whose writer's side the words do not show is not the room's, and neither is a proposal or a hub announcement by a writer whose other posts speak for another room (83, 93, 94, 103, 111, 112; G50 reading 108). An alliance reported secured by a writer whose side the words do not show is read as the room's, by the default of the visitor rule (27). An act in another room's record stays in that record (96).
  2. **What the first end is.** A warning of a coming attack or threat is not upkeep (1, 35, 37, 41; G36). A warning that the work is overrun now, or failing now for want of hands, is watching (1, 37, 44). A request to a partner for help against an attack, coming or under way, is a call to defend (1, 31, 56). Coordinating upkeep scripts, entrenching against a neighbour and saving a shared league logo are upkeep (20, 27, 61). These are not upkeep: a loss report, a celebration that the work survived, a battle plan against a rival, a design choice, negotiation to defend, and a statement of strain (18, 21, 37, 41, 71, 75, 84). Where the first upkeep shown is an ally's or another room's, before any upkeep by the members, the first acts are one act (3, 9, 39, 57, 111; G45 reading 6).
  3. **What the room's coalition is (G27).** These count: an alliance formed, proposed with a named partner, taken up or acted on; a chat shared by several rooms (7, 29); a hub of kindred rooms (8, 32, 72); a joint project or mark (7, 34, 101); a treaty that includes mutual protection (86); and upkeep or defence given both ways (14, 18, 92, 100, 106, 109). These do not count: a proposal or a pact claim that names no partner (4, 6, 23, 25, 46, 51, 56); an alliance whose only term is non-harm, or one made with the threatening room, which is P08's truce (19, 51, 57, 65, 89, 111); protection given one way, recognized status, help from named rooms, help traded for building or for defence, and conditional help, which are P16's (7, 11, 17, 38, 45, 65, 105, 109, 112); a member's visit to another room's chat (26, 51); and the room's own chat or sub (67, 112). A spot inside another room's mark, a host's chat or a host's taskbar is P19's form, counted HOST (30, 43, 59, 63, 89, 112). A colour faction's alliance that protects a logo moved into its area is P17's lower range, with P19's form beside it (12).
  4. **Placing the ends.** A line is classed by the first act of each, from its concepts and the coded posts above them in their chain. Posts elsewhere in the room are not used (64, 109). A coded post above the concepts can hold the first end, and the line is then marked R (6, 13, 27, 33, 44, 61, 76, 87, 92, 95, 97, 107). A post that only forms or proposes an alliance shows one end. A post that holds the room's defence and the coalition together is one act (2, 3, 8, 20, 21, 57, 66, 85, 99, 104, 111). A post that calls for defence and then, as a further step, proposes joining named allies shows the order in its words (36, 52, 91). A statement that an alliance exists, that a named room is with the room, or that a collaboration is under way places the alliance only before the statement. An announcement of a new alliance dates at its own hour (54, 69, 70, 80, 97). A report after the close places the act only before the report (6, 10, 23, 39, 53, 63, 82, 104; G45 reading 12). A report that the room has been allied since the beginning dates its first coalition at the start (110). Edits and update lists cannot be dated (49, 59, 67, 91; G45 reading 11).
  5. **The bound's pattern and ENTRY.** A coalition proposed, joined, taken up or acted on before the room's first upkeep is the bound's pattern (4, 18, 28, 32, 40, 42, 49, 50, 55, 58, 60, 62, 67, 71, 74, 79, 84, 102, 105, 108, 110). An alliance taken up whose term is defence is the coalition end only, so a later call on it is the room's first upkeep (50, 55). ENTRY marks a room that enters its spot through another room's coalition, space or offer (12, 24, 35, 38, 49, 58, 59).
  6. **The threat and the mechanism.** TH marks a coalition that answers a warning of a coming threat, or a threat foreseen or named, with no upkeep before it (1, 16, 22, 35, 37, 41). MW marks an order line whose first coalition act names an attack, a shared threat or defence given both ways (14, 18, 20, 23, 37, 40, 52, 56).
  7. **Restrict and add conditions.** They are ruled by G9 with G51's classes. S-O-A, S-O-H and S-BOUND are specifications, and EL-NU, EL-NC, EL-HOST, EL-ONE, EL-J and EL-AFTER are evidence limits (24, 60). The connection counts an order and names no enemy. So it holds a condition that the order is not a cause, or that no common threat is shown (24, 60). The bound and the counterexample response, with K02, hold a condition that the coalition can come first, can let a room enter its spot, or can rest on affinity or on a shortage of users (24, 60). P07 and the falsifier's second clause, which A19 records as present, hold a room's advice not to help either side (58).
  8. **Absent lines and re-rulings.** Absent lines are rejected by the first act of each, as instantiate lines are classed. The one NONPORTABLE line, hearthstone-035, is a particular not marked PO (64, 88). Reading 69, applied backwards, re-ruled three lines whose first coalition is a statement after an earlier upkeep, from S-O-H to EL-J. Two author checks re-ruled warriors-049 (S-BOUND to S-O-A) and gatech-049 (EL-J to EL-ONE), and one withdrew canada-035's reject before any build (83, 93, 94). Two acts in other rooms' records come before halo's own call. They stay contrary facts (96).
- **G52 (logged at D3a-47, before any of A20's lines was read or ruled).** A20 is a standing arrow from C2, P01 → P20, of kind order and strength strong. Its gloss: 'calls flood the host sub, and the host draws a line'. Its connection reads: 'in a room carrying both, the first call to the canvas comes before the first line the host sub draws around canvas talk (a megathread, a removal by rule, a changed rule, a canvas sub, an objection to the flood, a dismissal of the canvas)'. Its mechanism: 'Calls to the canvas flood the host sub, and its moderators or members answer by drawing a line around canvas talk: one thread, removals, a canvas sub.' It fails if 'In a room, the line comes before any call, or the line's words name no canvas flood.' The arrow records this failure as present. Its bound begins: 'Partly constitutive: a removal by rule needs a post to remove, and an objection to the flood needs canvas posts.' It counts 23 of 155 rooms that draw the line first. In 9 the sub's rules remove the first call as it is posted, in 7 a canvas sub or a megathread is set up before the host sub carries any call, and in 7 members dismiss the canvas or object to other rooms' canvas posts before the room calls. It adds that a member's judgment of the canvas's worth after the close answers no flood (transformers, h80.40). Its counterexample response reads the removal of a call as it is posted as 'the same mechanism at no delay', and reads the canvas sub set up first and the early dismissal as scope conditions in the bound. C2 counted the order in 132 of 155 rooms carrying both (0.852; null mean 0.538, p95 0.594), from 29 transitions in 22 rooms. Pass 4 found 5 of 155 rooms with no line after the first call. Before hour 73, the calls come before the host's rulings in 102 of 118 rooms, before members' objections in 57 of 64, and before the whole line in 122 of 144. Its three support transitions passed the audit (nintendo, rocketleague, france). All four rooms C2 sampled against it hold, and in one of them (transformers) the mechanism fails. `mem.py findings --touching A20` returns none. F-010, filed under P20, states A20's count and is bounded as the arrow is. P01 is read as D3a-02 read it: a call to place on the canvas, for a work, to start, build, finish or hold it, posted in the room's threads. D3a-02 accepted, as P01 as written, calls whose target is another room's work and calls made in the room's thread by a visitor or a kindred group. A join, a pledge, a report of the work's state or a celebration is not a call (P15, P03, P11). P20 is read by G26 and its readings.

  Six readings follow from the arrow's words, as QD3-007 reads a bound in its words.
  - **The first end is a call posted in the room.** The connection names the first call to the canvas, and the mechanism names calls that flood the host sub. A visitor's call posted in the sub floods it as a member's call does, and D3a-02 read such calls as P01. So the first end is the first call to place on the canvas posted in the room's threads, by a member, a kindred group or a visitor. The census marks VC where the first call is a visitor's. A call made in another sub and reported in the room is the other sub's.
  - **The second end is the host sub's line** (P20, by G26 and its readings). The room's moderators or members route canvas talk to one thread or a canvas sub, remove canvas posts for their topic, change the sub's rules for the canvas, pause a usual event, say the work is not the sub's, object to the flood, or argue the canvas's worth. These are not this end: moderation as such, a rule change made only for the sub's own April Fools joke, building talk inside a megathread or canvas sub, praise alone, a visitor's objection that no member takes up, and another sub's line reported in the room. A room that is itself a canvas sub has no business apart from the canvas, so its founding post and its venues draw no line (G26).
  - **One act.** A megathread or canvas-sub post that is also the room's first call holds both ends in one act. A removal notice whose only record of the call is the post it removes shows the call inside the line, with no coded call before it, so the first act of each is one act. The census marks it RM, beside the bound's 9 rooms, which the counterexample response reads as the mechanism at no delay. Acts at hours that cannot be placed against each other are one act too (J, counted apart).
  - **The flood in words.** The falsifier's second clause names a line whose words name no flood. So the census marks an order line MW where its first line answers canvas posts: it routes, removes, gathers or objects to them, or names their number. It marks NF where the first line answers no post: a judgment of the canvas's worth, a disowning or a pause. NF lines show the order, and the mechanism does not reach them.
  - **The close.** P20's statement sets no time, and the bound reads a judgment of worth after the close as answering no flood. So a first line after hour 73 that follows a call made while the canvas ran shows the order, and the census marks it AC. A first call shown only after hour 73, for the closed canvas or a later one, is not this arrow's first end (AFTER).
  - **The bound.** A line drawn before the room's first call is the bound's pattern: a canvas sub or megathread set up first, or a dismissal or an objection to other rooms' canvas posts before any call is posted in the room. The census reports it by room, beside the counterexample response's 23 of 155.

  A20 is not stated as universal; it claims an order counted inside each room. So its absent lines are never corrections. G2 and G3 rule them:
  - an `observed-absent` or `not-needed` line is a specification where the concepts show a call with no line, a line with no call, neither, or the bound's pattern;
  - a concept that shows a call posted in the room and, after it, the host sub's line, as read above and classed by the first act of each, from the line's concepts or the coded posts above them in their chain, makes the claim of absence fail (reject), whatever the line's observation;
  - a NONPORTABLE line is a particular (G6), marked PO in the census where its concepts show the order;
  - the other `unobserved` and `not-testable` lines are evidence limits.

  An instantiate line shows A20 when its concepts show a call posted in the room (P01) and, after it, the host sub's line (P20). The order is read from the concepts' hours (`cite.py`), the reply chain, coded posts above the concepts (marked R), or one post whose words name the call or the flood first and the line after. A line is classed by the first act of each. It is accepted as a specification when the order shows in the reply chain or thread (O-A), or by the hours or in a post's words (O-H). It is rejected when:
  - the first line comes before any call (the bound's pattern, BOUND);
  - the first call and the first line are one act (J);
  - the first end shown is not a call: a join, a pledge, a report or a celebration (NC);
  - what follows the call is not the host sub's line: moderation as such, building talk in a megathread, praise alone, a visitor's objection that no member takes up, or another sub's line (NL);
  - only one end is shown (ONE);
  - the first call is first shown after hour 73 (AFTER).

  A restrict or contradict line is ruled by G9, read for an arrow, as under G45 to G51. A restriction whose condition the connection, the mechanism, the bound or the counterexample response already holds is a specification where its concepts show the order or the bound's pattern, and an evidence limit (kind `none`) where they show neither. A condition held by another statement is a specification naming it (G4a). A correction states a condition that A20, its bound and its counterexample response lack, and shows the order failing without it. The falsifier's first clause, the line before any call, is the bound's case. Its second clause, a line whose words name no flood, is recorded present, and the census marks it NF. The counterexample response weighed two alternatives: the arrow as a definition, and the line as the host sub's standing temper rather than an answer. So a condition that the line is standing policy, or that it answers the sub's own norms, is held there and by the bound. Two accepted corrections with one target and one lifted node at the third or fourth level trigger §2, and F-010 would then be re-examined.

  G45's readings 1, 8, 10, 11 and 12, and G46's reading 9, say how an end is placed and dated. They apply here with A20's ends in place of theirs, as do G26's readings of removals, canvas subs, stickies, chats, worth, and other subs and moderators. G50's reading 108 and G51's reading 103 decide a cross-posted message whose writer's side the words do not show.

  The order test is written and logged before it runs: the census of the rulings by room (the order, in the thread or by the hours; the bound's pattern; one act; not a call; not the host sub's line; one end; after the close; other; limit), with the MW, NF, AC, VC, RM, R and PO marks, and the shares beside C2's 132 of 155, pass 4's 5 of 155 and 122 of 144 before hour 73, and the counterexample response's 23 of 155. Under G4a, the statements expected to hold an add, link, instantiate or restrict line are P01, P20, P02, P03, P04, P11, P12, P13, P14, P15, P16, P17, P08, P21, P22, C01, K01, K02, A01, A02, A06, A12 and R01. Candidates hold no line (R02, P06, P19, K03, K04). Draws follow G1b: one draw of ten lines per 100-line instantiate packet, from the instantiate lines' first verb offset (447, after the verb's header line and 434 absent and 12 add-condition lines), which the draw's header confirms. The two instantiate packets hold 100 and 20 lines.
- **G52, amendment 1 (D3a-47, 20 October 2026, before any A20 line was ruled; it applies to every A20 line, and no line was ruled before it).** G52's instantiate paragraph lets one post whose words name the call or the flood first, and the line after, show the order. A flood is not a call, and G52's first end is a call posted in the room. A line that names the flood of canvas posts shows that canvas posts came before it. The bound reads this as partly constitutive, and the counterexample response weighed the arrow as a definition. So a post's words show the order only where they name calls posted in the room first, such as posts that ask members to place, help, defend or join, and the line after. A line whose words name only canvas posts, threads or spam shows the line alone, and the census marks it MW. Its first end must come from a coded call in the line's concepts, or in the coded posts above them in their chain.
- **G52's readings (D3a-47).** They apply G52, its amendment 1, G2, G3, G6, G9, G26 and the readings of G45 and G46 that G52 names, and change no rule. Each was logged in the diary, with its rooms and codes, before the lines it governs were written: readings 1 to 26 in the instantiate pass, 27 to 62 in the restrict pass, 63 to 66 in the add-condition pass, and 67 to 105 in the absent pass. Two logs gave wrong counts for window r567_000, and a later note corrects them by script. No row changed because of them. Three instantiate lines moved from O-A to J under reading 23. Two of them, pokemon-046 and singapore-044, moved before the build, by superseding files. The third, nintendo-063, moved after it, by an appended re-ruling, when a scan after reading 66 looked for the same kind of reply in every order row. The readings fall under eight heads.
  1. **What the first end is.** A call asks members to place, help, defend, join or keep the work. A warning that the work is changed or attacked is the call's hold form (3, 50). A question that asks members to join or act asks for hands, and so is a call (28), as are a petition that names the logo and its spot (9), a request to change the work (8), a call aimed at another room's work (10, 20), a script post that walks members through placing (4), and a proposal to move the work if enough people join (100). These are not calls: a proposal, and a question whether the room will make a work or why it has not (2, 13, 28, 89); a report or presentation of the work, a design question, and a warning with no ask (3, 13, 101); a post that shares scripts (89); a title that names visitors on the canvas (98); and a visitor's plea to spare its work (40, 50). A call shown only after hour 73 is not the first end (AFTER: 6, 11, 21, 60). VC marks a first call by a visitor or a kindred group (5, 15, 16, 26).
  2. **What the host sub's line is (G26).** These count: routing canvas talk to one thread, to an existing call thread or to another room's canvas sub (5, 23, 33, 37, 48, 85, 91, 97); a megathread, sticky or pin whatever its motive, and a request or promise of one (12, 19, 34, 46, 55, 59, 76, 79, 82, 85, 88, 91, 94); a removal of canvas posts for their topic (32, 45, 70, 100); a rule change or a flair for canvas posts (64, 85), a paused thread (59) and an unstickied canvas thread (31); an objection to the flood or to other rooms' canvas posts (5, 10, 51, 82, 88); a question or dismissal of the canvas's worth (25, 34, 57, 61, 73, 79, 85, 103); and a statement of the sub's topic that sends the canvas work elsewhere (103). These do not count: moderation as such, which covers format, caps, links, tags, flair reminders, karma, bare duplicate notices and removals under an unnamed or general rule (18, 32, 36, 44, 52, 60, 65, 84, 99, 102, 105); coordination threads and chats with no line stated (7, 16, 18, 42, 62, 74, 92, 102); a poster's removal of their own post (74, 84, 96, 99); a ban threat for griefing (78, 105); a visitor's objection that no member takes up (71, 93); another sub's line (29, 35, 87, 101); the sub's own April Fools joke and its posts, K01's frame (32, 44, 78, 81, 87, 90, 93, 96, 99, 102, 105); questions from members who see many canvas posts (78, 90, 105); and a canvas-born room's founding post, venues and moderation (29, 38, 68, 72, 96).
  3. **Placing the ends.** A line is classed by the first act of each, from its concepts and the coded posts above them in their chain (R marks a first end taken from such a post). Posts elsewhere in the room are not used. One post's words show the order only where they name calls posted in the room first and the line after (amendment 1; 16, 24, 104). A reply that points a call to a sticky, pinned thread or megathread already made reports a line at an hour the record does not show, so the ends cannot be placed (J: 23, 33, 41, 46, 48, 53, 63, 86, 95). A report that the room's own call thread was stickied places the sticky after that call (104). Updates edited into a submission, and reports that submissions are restricted, cannot be dated (38, 92).
  4. **One act.** A post that calls members and also makes itself the megathread, a canvas sub or the official thread holds both ends (41, 63, 77, 98, 101). A removal notice whose only record of the call is the removed post shows the call inside the line, marked RM (2, 49). 17 lines are one act.
  5. **The bound's pattern.** A line drawn before the first coded call is the bound's pattern: a megathread, a removal rule, a member's objection or a dismissal of the canvas before any call (3, 8, 14, 20, 25, 40, 50, 53, 58). In an absent line, a line first is an evidence limit, since the claim of absence does not fail (77, 80, 83, 89, 95, 101, 105).
  6. **The flood in words, MW and NF.** MW marks an order line whose first line routes, removes, gathers or objects to canvas posts, or names their number. NF marks one whose first line answers no flood: a sticky asked or made for visibility, a pinned call, a paused thread, or a judgment of the canvas's worth (19, 27, 31, 34, 55, 57, 59, 61). Under amendment 1, a line whose words name only the flood shows the line alone (1).
  7. **Restrict and add conditions.** They are ruled by G9 with G52's classes (27, 63). S-O-A, S-O-H and S-BOUND are specifications, and EL-J, EL-NC, EL-NL, EL-ONE and EL-AFTER are evidence limits. The connection counts an order, not a cause, so it holds a condition that the record does not show a flood causing the line (27). The falsifier's second clause, which A20 records as present, holds a line that answers no flood (27). The bound and the counterexample response hold the line drawn first and the sub's standing temper, and G26's readings of removals hold a removal that follows a format rule (27, 32, 36).
  8. **Absent lines and re-rulings.** Absent lines are rejected by the first act of each, as instantiate lines are classed (67). None is observed-absent or not-needed. The one NONPORTABLE line, counting-034, is a particular not marked PO, since its only line is a standing rule and no call is coded (80). The census tags of the twenty rejects in the first five absent windows were read from each row's words by the census rule. The rows from window ab101_067 on carry them in their words.

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
- **P21** (ruled at D3a-26). Instantiated in 80 rooms as returned (65 after ruling). Restricted in 65 rooms, none by an accepted correction (65 lines in 64 rooms accepted as specifications, 1 particular). Contradicted in none. Left absent in 582 rooms (483 evidence limits, 1 observed absence, 98 rejected because their concepts show it, PinkUnion-029 among them since D3a-27's re-ruling). Shown in 163 rooms by instantiate and absent lines, and in 212 with the restrict and add lines its statement holds (162 and 211 at D3a-26). **Ruling: standing (rule 11), statement's frame rewritten to 'dispute, or state the limits of'; move 175, history lines 140 and 141.**
- **A21** (ruled at D3a-27). Instantiated in 37 rooms as returned (22 after ruling). Restricted in 65 rooms: 36 by accepted corrections, paired in two families; 25 lines accepted as specifications; 4 evidence limits. Contradicted in none. Left absent in 605 rooms (536 evidence limits, 2 evidenced absences, 67 rejected because their concepts show it). Shown in 114 rooms; the P21 form comes first in 49 (36 at the making of terms, 13 with no agreement), 1 room both. **Ruling: standing with a bound (rule 11), after §2's re-examination; connection aligned with P21, the mechanism's request clause dropped; move 176, history lines 142 to 150.**

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

## D3a-08: P03, Direct information sharing

P03 stands alone in T4-007 (direct information sharing: members tell each other the state of the work). Its statement reads: 'The room builds its mark, and members report its state to the thread: what is placed, done or missing, and where.' Its range runs from one report that the logo is half done to reports on each part of a mark over two days. It has stood since C2's first pass, and no finding touches it. All 948 lines are ruled under G15, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_group_rulings.py`, `d3_field_entry_counts.py`, `d3_family_counts.py` and phrase counts over my own reasons.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 664 | 640 | 1 | 0 | 0 | 15 | 8 |
| absent (38 `unobserved`, 8 `not-testable`) | 46 | 0 | 0 | 0 | 29 | 0 | 17 |
| link | 138 | 3 | 129 | 0 | 2 | 4 | 0 |
| add-step | 69 | 9 | 45 | 0 | 13 | 2 | 0 |
| add-condition | 16 | 1 | 11 | 0 | 2 | 2 | 0 |
| restrict | 15 | 2 | 6 | 0 | 6 | 1 | 0 |
| all | 948 | 655 | 192 | 0 | 52 | 24 | 25 |

702 rooms have a P03 line. P03 is shown in 650 of the 705 rooms: an accepted specification or elaboration in any op, or an absent line rejected because its concepts show it. In 625 of them an instantiate line is accepted. 52 rooms have P03 lines and none shows it.

**What the accepted instantiate lines show.** By phrase count over the 640 specification reasons (a line may carry more than one form):
- **The work done, finished, complete or made: 272.**
- **Progress, a start, or work under way: 271.**
- **Where the work stands (coordinates or a location): 187.**
- **Damage, loss or a fix while the work stands: 85.**
- **What is missing or still needed: 35.**
- **An image posted as the current state: 29.**
- **A correction (of a report, a coordinate or a row): 10.**

497 reasons read P03 as stated. 120 sit at its lower range: one report, such as one pixel placed, one 'X is on r/place' post or one location. 17 carry P03's 'done' alone, 2 its upper range, and 4 the overlap G11 names, where damage reported while the work stands is P03 and P05's watching at once.

**Restrict, add-condition and add-step: no correction.** Under G9, the 15 restrict and 16 add-condition lines correct nothing. What they add sits inside the statement, or is a condition that a second room shows: the work built by a few members or by another room's hands, the reports carried through a chat, or a work that already exists. They are specifications where they show P03, evidence limits where they do not, and paired elaborations where a second room shows the same condition. Of add-step's 13 evidence limits, 8 show only a move to a chat (T4-010's ground): Fez-013, calvinandhobbes-009, indieheads-010, physical_removal-008, stardustcrusaders-040, telegram-010, wales-033 and wildhockey-008.

**The 192 elaborations, by family** (all paired; the counts are lines, then rooms; no line falls in two families):

| family | lines | rooms | ops | examples |
|---|---|---|---|---|
| after a loss or a move, the room builds again and reports the new work | 88 | 87 | link 88 | Cornwall-032, PUBATTLEGROUNDS-029, SquareSpiral-031 |
| the room's sharing split between the thread and a chat, with reports or decisions brought back | 20 | 19 | add-step 17, three others 1 each | AprilKnights-013, Fez-014, masseffect-032 |
| building and reports continue on a successor canvas after hour 73 | 17 | 14 | link 13, add-condition 3, instantiate 1 | magictcg-049, rotmg-045, sadboys-012 |
| a neighbour's terms or a host's permission opens the space | 14 | 13 | link 13, add-condition 1 | MMA-033, notredame-056, stargate-052 |
| a member's screen checked against the refreshed or persisted canvas | 10 | 10 | add-step 7, add-condition 2, restrict 1 | enterthegungeon-010, rotmg-011, auburn-053 |
| parallel or duplicate builds, with reports deciding where hands go | 9 | 8 | add-step 7, two others 1 each | FinalFantasy-013, bretagne-053, gameboy-010 |
| building and keeping alternate or overlap in the same reports | 7 | 7 | add-step 4, link 3 | the_pack-019, sixers-015, oneshot-039 |
| a report that the work exists answers a call to make it again | 5 | 5 | add-step 4, restrict 1 | Madeon-006, batman-019, uva-053 |
| members report the part they take on, and so divide the work | 4 | 4 | add-step 4 | factorio-011, lego-009 |
| a work built by a group outside the room, its reports carried in the room's thread | 4 | 4 | restrict 2, two others 1 each | araragi-008, nlsscirclejerk-054 |
| one place kept for the work's current state | 3 | 3 | add-step 2, add-condition 1 | splatoon-026, yugioh-073 |
| contest with a rival interleaved with building | 3 | 3 | link 3 | lakers-083, sabres-027 |
| a work built and reported by a few members, not the room as a body | 2 | 2 | restrict 1, add-condition 1 | metroid-008, peterdraws-002 |
| a script takes on part of the placing | 2 | 2 | link 2 | ScottPilgrim-024, globaloffensive-015 |
| a report must reach the builders and keepers, or they work on the wrong thing | 2 | 2 | link 2 | berserk-030, placeDE-061 |
| a finished work reopens building | 2 | 2 | link 2 | fireemblem-056, splatoon-057 |

**What the 25 rejects show.**
- **Instantiate, 8.** Two cheer or credit and report no state (Goodboye-004, paragon-012). Four are records after hour 73 (Mario-008, aeon-008, azerbaijan-003, yuyuyu-003). One is a visitor reporting another room's heart (AceOfAngels8-004), and one an unclear 'operation was a success' (germany-004).
- **Absent, 17.** Each line's concepts show P03 during the event, so the claim of absence fails. Eleven post the work on the canvas or say where it is, at P03's lower range: for example Lugarix-007 ('LAX officially in /r/place!'), TheID-006, parabola-021 and pgang-006. In natsume-012 the makers are unknown, and the room keeps the figure with a template, as in the outside-builders family. Two report work under way and where (carletonu-013, ontario-014). Four report a pixel placed, a part added or a fix (azores-008, cgpgrey-010, heyyea-011, OneTrueEmilia-011).

**Absent lines.** None records an evidenced absence. A guard listed 11 evidence-limit lines whose labels share words with P03, and each was read again. They hold calls (Braveryjerk-013, UMiami-009, polyamory-014, wario-007), a plan (Homura-014), records after hour 73 (livecounting-012, tetris-018) and thanks (thetreesnetwork-017). UNLincoln-012 reports damage to a logo that a second member corrects as another school's. In sakartvelo-008, a member points to Georgian flags others had placed. In falcons-013, c0104 taunts a call to erase another's work for its lack of progress, and c0161 is a visitor's question at hour 74.7.

**Particulars, 24.**
- **Failing portability (22):**
  - instantiate: AprilKnights-010, AyyMD-004, CKCrusaders-005, CryptoFR-002, DCFU-004, counting-005, dallasstars-009, greyblob-005, kirby-005, kurdistan-003, linux-012, python-010, skyrim-003, ss13-008, vim-006;
  - link: donaldglover-015, gravityfalls-051, miraculousladybug-053;
  - add-step: AprilKnights-022, geometrydash-010;
  - add-condition: shield-061;
  - restrict: counting-012.
- **One room only (2):** rocketleague-010, where members hurry the main shape into place so that defenders can tell the work from damage; and palestine-059, where a finished work is carried into the room's own banner. A search of P03's lines found no second room for either.

**Re-ruled in this leg.** bahrain-006 moved from reject to specification by an appended line, under G15's 'done' reading.

**No correction, so no §2 re-examination.** No restrict, add-condition or contradict line was accepted as a correction. P03 stands as served, and no move was made.

**Repairs (G7).** Repairs made no difference that bears on a ruling. Repaired rooms were 0.962 accepted (505 lines), and unrepaired rooms 0.932 (443 lines).

**Carried to later groups.**
- **The return to building.** 88 link lines in 87 rooms show a loss or a move followed by building again and new reports. No standing arrow draws this return. It sits beside A10 (moving when hands are too few) and the calls that recur after a loss, carried from D3a-02. It is a candidate for D4, after an order test.
- **Chats (T4-010).** The thread and a chat split the sharing in 19 rooms, and 8 add-step lines show only the move to a chat. Members outside the chat depend on what comes back to the thread.
- **Parallel builds (9 lines) and outside builders (4).** These bear on the unit: who builds and reports the room's mark.
- **Successor canvases (17 lines).** Building goes on after hour 73 on other canvases, beside P13 (carrying the work on).
- **Neighbours' terms and hosts' permissions (14 lines)** go to the neighbour arrows (A04, A14).

**Disclosed limits and slips.**
- **Draws.** There were seven seeded draws over the instantiate lines, at verb offsets 132 to 732, ten lines each. None found an unsupported line.
- **The 'done' reading** was stated at instantiate line 152. It re-ruled bahrain-006, which had been rejected as a bare cheer.
- **A phrase count** first matched 'end' inside 'sends'. It was rerun with word bounds.
- **The group close** tabulates rejects under the line's own kind ('specification'). The rulings store them with no kind.
- **Images.** Many reports rest on images not in the record. A report the words do not carry is an evidence limit (UPenn-007).
- **Compaction.** The context was compacted once in the leg, while the absent lines were being ruled. The head, the stage file and the diary were read again before any write.

### Close-check, D3a-08

`validate.py D3` reports 8,867 of 42,243 ledger lines ruled. That is the 7,919 ruled through D3a-07 and P03's 948. It reports 0 errors and 2 warnings, the same two as before: history lines 137 and 138, which name move 174 'stabilizing' (line 139 records the correct name). All 192 pairs in P03's files name a P03 line (`_analysis/d3_pair_check.py`). The ledger holds 8,886 lines, 19 of them appended re-rulings across the legs (bahrain-006 is this leg's). History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561. None of those ledgers changed in this leg.

## D3a-09: P11, the room marks a work that is up

P11 stands alone in T4-026 (marking a finished work: announcing, celebrating and crediting it). Its statement reads: 'When a work is up, the room marks it: announces it, celebrates it, credits makers and helpers, reports members' own parts and says what working with strangers meant.' Its range runs from one 'We did it!' post to threads of credit and reflection at the close. It has stood since C2's first pass. F-021 touches it, and arrows A07 (P03 to P11) and A08 (P11 to P12) run into and out of it. All 951 lines are ruled under G16, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_group_rulings.py`, `d3_field_entry_counts.py`, `d3_family_counts.py` and phrase counts over my own reasons.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 716 | 675 | 18 | 0 | 0 | 17 | 6 |
| absent (48 `unobserved`, 5 `not-testable`, 1 `observed-absent`, 1 `not-needed`) | 55 | 1 | 0 | 0 | 42 | 0 | 12 |
| add-step | 70 | 46 | 20 | 0 | 4 | 0 | 0 |
| restrict | 45 | 23 | 7 | 0 | 14 | 1 | 0 |
| add-condition | 42 | 33 | 7 | 0 | 0 | 2 | 0 |
| link | 23 | 4 | 16 | 0 | 1 | 2 | 0 |
| all | 951 | 782 | 68 | 0 | 61 | 22 | 18 |

704 rooms have a P11 line. P11 is shown in 646 of the 705 rooms, and in 627 of them an instantiate line is accepted. 58 rooms have P11 lines and none shows it. One of them, pebble, records an evidenced absence.

**What the accepted instantiate lines show.** By phrase count over the 675 specification reasons (a line may carry more than one form):
- **Celebration ('we did it', pride, congratulations, cheers): 431.**
- **Thanks and credit to makers and helpers: 371.**
- **Members' own parts (pixels, hours, a piece claimed): 181.**
- **The work announced or shown on the canvas: 142.**
- **What working together meant (community, unity, support, alliance): 103.**
- **The work said to have lasted to the end: 101.**
- **Prizes (medals, game codes, points): 5.**
- **An invitation to celebrate offline: 1.**

575 reasons read P11 as stated, and 97 sit at its lower range: one 'we did it', one announcement, one cheer or one thank-you. Three rest on credit disputes.

**Restrict and add-condition: no correction.** Most of these lines say that a celebration does not prove a verified, finished, agreed or lasting work, or that upkeep goes on after it. P11 claims none of these, because it rests on the room's own word (G16). The lines are specifications where their concepts show the marking. They are evidence limits where the concepts do not: the 14 restrict limits are bare titles, jokes, a prize for an in-game feat, finds shared and attempts still under way. They are paired elaborations where they show a form P11 does not state.

**The 68 elaborations, by family** (all paired; the counts are lines, then rooms; no line falls in two families):

| family | lines | rooms | ops | examples |
|---|---|---|---|---|
| marking where no work is up: an attempt, a remnant or a lost work thanked or praised (A07's bound) | 24 | 14 | instantiate 10, add-step 5, link 4, restrict 3, add-condition 2 | warthunder-058, battlecats-049, ultrahardcore-031 |
| marking disputed inside the room: some celebrate, others call it a failure, deny it stood, or object to honouring it | 14 | 13 | add-condition 5, add-step 5, restrict 4 | singapore-046, kcroyals-046, h3h3productions-035 |
| a record of the work occasions its marking (A08's late-side order) | 9 | 9 | link 9 | belgium-056, dota2-057, titanfall-053 |
| progress celebrated before the work is up | 8 | 8 | add-step 4, instantiate 4 | FinalFantasy-046, ProfessorLayton-063 |
| credit named in a plan or call before the work is up | 4 | 4 | add-step 2, instantiate 2 | planetside-036, vocaloid-056 |
| a flaw at the close, read fondly, made the room's cheer | 3 | 3 | link 3 | chicubs-051, uofm-056 |
| a marked work reopens building | 2 | 2 | add-step 2 | monero-030, taiwan-033 |
| recognition sought from the creators the work depicts | 2 | 2 | add-step 2 | funhaus-055, gameattack-053 |
| marking a work made on a successor canvas after hour 73 | 2 | 2 | instantiate 2 | catholicism-056, hungary-030 |

**What the 18 rejects show.**
- **Instantiate, 6.**
  - Three are bare reports of the state, which is P03: anime_irl-042 ('It's complete.'), VelvetUnderground-043 ('mostly done') and nightinthewoods-043 ('Got the G done y'all, now for the rest').
  - One is a locating exchange (furry_irl-047), and one a find inside another room's work (TheAdventuresofTintin-007).
  - One is praise for spoiling a rival's logo (sabres-030).
- **Absent, 12.** Each line's concepts show P11, so the claim of absence fails:
  - announcements (TheID-026, bretagne-017, warthunder-062) and a cheer (THE_R-023);
  - thanks to helpers (carletonu-031, ghibli-047);
  - the part made, marked at the close (DiamondClub-043, foxstevenson-043);
  - an attempt marked (aeskwadraat-016, wsu-037);
  - praise of the room's icon (qotsa-031), and progress and plan credit (planetside-037).

  wsu-037 was marked `observed-absent`. Its 'Take my upvote for the good effort though' marks the lost attempt, so the absence is not observed.

**Absent lines.** One evidenced absence stands: pebble-032 (`not-needed`). The room tallies and mourns an icon left unfinished in two places and marks nothing, so P11's condition, a work up, is not met. A guard listed 9 evidence-limit lines whose labels share words with P11, and each was read again:
- faction pride under threat (GreenCorner-050);
- progress, 'almost done' or a part finished (GuildWars2-043, Produce101-015, ik_ihe-034);
- appeals (NovaScotia-026);
- an ally's thanks for help with its own work (TeamYellowPlace-028);
- a game cheer (ducks-044) and a prank (ontario-031);
- thanks to another room for its own figure (streetfighter-049).

**Particulars, 22.**
- **Failing portability (21):**
  - instantiate: CryptoFR-003, KState-030, calgaryflames-034, indonesia-027, ethereum-036, finland-030, lego-042, linux-052, popheads-057, python-043, ravens-048, rit-046, seventeen-038, tetris-014, texas-025, transgender-010, wine-049;
  - add-condition: littlewitchacademia-048, neopets-067;
  - restrict: counting-045;
  - link: futanari-056.
- **One room only:** nuclearthrone-041, where a host moderator removes a thank-you to another room's helpers as unrelated to the game. A search of P11's lines found no second room.

**Re-ruled in this leg.** None.

**No correction, so no §2 re-examination.** No restrict, add-condition or contradict line was accepted as a correction. P11 stands as served, and no move was made.

**Repairs (G7).** Repairs made no difference. Repaired rooms were 0.960 accepted (500 lines), and unrepaired rooms 0.956 (451 lines).

**Carried to later groups.**
- **Marking where no work is up (24 lines, 14 rooms).** A07's bound already names it. A07's group should weigh whether it belongs in that bound or in P11's statement.
- **A record before the marking (9 links).** Rooms post the final image or timelapse, and the celebration follows. This is the late-side order A08's bound notes, for A08's group.
- **Marking disputed (14 lines, 13 rooms).** Some of these disputes run during the event (greece-053 at hour 18, singapore-046, truestl-028). They sit beside P22's contests after the close, for P22 and the clustering.
- **Credit disputes over scripts and other rooms** (flyers-055, utaustin-047, pakistan-015, overwatch-074, wine-022). These go beside A06 (scripts) and the neighbour arrows.
- **Recognition from the depicted creators** (funhaus-055, gameattack-053, NieR-054, theexpanse-050). This is a channel outside the rooms that no element names.
- **The host's moderation of marking** (nuclearthrone-041) goes to T4-002.
- **A marked work reopening building** (monero-030, taiwan-033). This sits beside P03's finished work reopening building and the open item of a finished work reopening calls.

**Disclosed limits and slips.**
- **Draws.** There were eight seeded draws over the instantiate lines, at verb offsets 168 to 868, ten lines each (the last over 16 lines). None found an unsupported line.
- **The 'done' against announcement reading** was stated at instantiate line 300. Its log line says it was checked backwards with no change. That check was run after the log line was written. It found five accepted lines that rest only on a finish, and each marks the work to the room, so the claim holds. The order was a slip.
- **The pair check** was first run without one rulings file (67 of 68 pairs). It was rerun over every file.
- **The group close** tabulates rejects under the line's own kind ('specification'). The rulings store them with no kind.
- **Images.** Many marks rest on images not in the record. P11 rests on the words, so a deleted image does not undo a congratulation (gravityfalls-044).
- **Head edits.** Four edits to the head ran as one parallel batch, which the rules forbid. All four landed, and the head was checked after them: its words, its links and the edited lines.

### Close-check, D3a-09

`validate.py D3` reports 9,818 of 42,243 ledger lines ruled. That is the 8,867 ruled through D3a-08 and P11's 951. It reports 0 errors and 2 warnings, the same two as before: history lines 137 and 138, which name move 174 'stabilizing' (line 139 records the correct name). All 68 pairs in P11's files name a P11 line (`_analysis/d3_pair_check.py`). The ledger holds 9,837 lines, 19 of them appended re-rulings across the legs, none from this leg. History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561. None of those ledgers changed in this leg.

## D3a-10: the blind re-rule check (J, 16 October, 19:08 Berlin)

J asked for a blind re-rule check at D3a-10 and again before the D3c freeze: about 50 lines from closed groups, with the pairs left for the handler's kappa. The rules were logged before the draw.
- **The sample.** 50 lines were drawn by `_analysis/d3_blind_sample.py` (seed 2026101610): R01, P01, P02, P05, P04 and K01 seven each, P12 and P22 four each. The sample is in `_analysis/d3_blind/sample-D3a-10.json`.
- **Exclusions.** P03 and P11 were left out because I ruled them in this conversation, and their rulings sit in my working context, so a re-rule would not be blind. Non-portable lines were left out because they are particulars by construction.
- **Blindness.** The lines were read through `_analysis/d3_blind_packet.py`, which prints every field but no decision, kind, pair or reason of mine. Quotes came through `cite.py`. One search of P02's lines for a pair had its decisions stripped. The ruling rules were read; the sections D3a-01 to D3a-07 were not.
- **The files.** The blind rulings were written to `_analysis/d3_blind/blind-rulings-D3a-10.jsonl` before any comparison. The pairs went to `_analysis/d3_blind/blind-pairs-D3a-10.jsonl` (`_analysis/d3_blind_pairs.py`). Each pair holds both rulings and reasons, and a flag for originals written before their element's revision in its leg (11 of 50).

**The blind rulings.** All 50 were accepted: 40 as specifications, 3 as paired elaborations and 7 as evidence limits. The originals were 36 specifications, 5 elaborations, 8 evidence limits and 1 particular.

**Raw agreement, for the record (the kappa is the handler's).** The decisions agree in 49 of 50 pairs, and decision and kind together in 46. By op, every instantiate (32), absent (7), add-step (4) and link (1) pair agrees. The four disagreements are all on add-condition lines (3 of 4) or restrict lines (1 of 2):
- **gratefuldead-015 (P01, add-condition).** The original ruled a particular: whether repeated calls are one operation depends on a hand-over, a reading local to the room. The blind ruling made it a specification: the relaunched thread is a call, and the condition is a counting rule.
- **detroitlions-006 (P02, add-condition).** The original ruled a paired elaboration (a next picture waits on the mark under way, with borderlands-022). The blind ruling made it a specification, holding that P05's 'upkeep before growth' already states the condition.
- **2007scape-018 (P05, add-condition).** The original ruled a paired elaboration (members explain their keeping by their group's game habits, with theexpanse-022). The blind ruling made it a specification without searching for a pair. The difference lies in the search, not in a rule.
- **denmark-039 (P22, restrict).** The original ruled an evidence limit: the corrected account concerns another room's rainbow. The blind ruling read it as a correction of an account of the room's work after the close. The difference is whose rainbow it was, and whether G13a's 'the event' covers a neighbour's work.

**What the check shows.** No drift shows on instantiate or absent lines. Where an add-condition or restrict line names a condition that another element already states, or that only one room shows, the rulings move between specification, elaboration and particular. My later legs (P11) lean to specification, and my earlier legs to elaboration with a pair. That boundary was not fixed by a written rule. Before P16's lines were ruled, I fixed it forward with G4a, a dated amendment, and asked J whether it applies backwards (QD3-003, open). The handler's kappa may still call for more. No ruling was changed by the check.

**Slip.** The first diary line on the blind counts gave figures from memory, and they were wrong. A second line corrects them from a count of the file.

## D3a-10: P16, help between rooms

P16 stands alone in T4-017 (help between rooms). Its statement reads: 'Rooms help one another's works and trade help: they give pixels to a neighbour's mark, ask other rooms for help, barter help for space or repair, thank their allies, greet them, and turn requests away.' Its range runs from one member placing a pixel on a neighbour's flag to rooms trading night-time repairs for room on their mark. It has stood since C2's second pass. Arrows A13 (P05 to P16) and A14 (P08 to P16) run into it. The findings query names no finding touching P16; F-008, which states A13's order, sits in its evidence list. All 985 lines are ruled under G17 and G4a, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py` (written in this leg; it reproduces P11's table above), `d3_field_entry_counts.py`, `d3_family_counts.py` and phrase counts over my own reasons.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 669 | 642 | 0 | 0 | 0 | 22 | 5 |
| absent (107 `unobserved`, 6 `not-testable`) | 113 | 0 | 0 | 0 | 98 | 1 | 14 |
| add-condition | 96 | 81 | 13 | 0 | 0 | 2 | 0 |
| add-step | 48 | 32 | 15 | 0 | 1 | 0 | 0 |
| link | 33 | 23 | 9 | 0 | 0 | 1 | 0 |
| restrict | 26 | 22 | 0 | 0 | 4 | 0 | 0 |
| all | 985 | 800 | 37 | 0 | 103 | 26 | 19 |

701 rooms have a P16 line. P16 is shown in 589 of the 705 rooms, and in 566 of them an instantiate line is accepted. 112 rooms have P16 lines and none shows it. None records an evidenced absence.

**What the accepted instantiate lines show.** By phrase count over the 642 specification reasons (a line may carry more than one form):
- **Requests for help, made or arriving: 323.**
- **Barter or mutual help (in return, for space, mutual upkeep or defence): 272.**
- **Thanks and credit to helpers: 194.**
- **Help between kindred rooms (a league, a city, a fandom, a nation's neighbours): 115.**
- **Greetings, compliments and welcomes: 58.**
- **Help sent once the room's own work is safe (A13's order): 55.**
- **Refusals: 46.**
- **A rival team's or school's room on either side: 32.**
- **Help given before the room has a work of its own (A13's bound): 5.**
- **Help asked because the room's hands run short (A13's mechanism): 4.**

126 reasons sit at P16's lower range: one request, one offer, one thank-you or one greeting.

**Restrict and add-condition: no correction.** Most restrict lines would require that help be delivered, follow negotiated terms, be agreed between the rooms, or come from a room's own members. P16 claims none of these: it names offers, requests, greetings and refusals among its acts. No restrict line shows P16 failing without its condition. The four restrict limits are a proposal inside the room to ask (vietnam-014), a proposal and a wish after the close (diablo-055), a wish after the close (corridor-026) and an unnamed partner (ghibli-025). Under G4a, most add-condition lines name a condition that A13, A14, P05, P08, P01, P02, P17 or P20 already states, so they are specifications that name it. Where nothing in the model states the condition, the line is a paired elaboration or, with one room, a particular.

**The 37 elaborations, by family** (all paired; the counts are lines, then rooms; RelientK-040 is counted once, under the tool family):

| family | lines | rooms | ops | examples |
|---|---|---|---|---|
| a tie from before or outside the canvas grounds or limits help (a league, a place, a nation, a member of two groups; the friendly side of C02) | 11 | 11 | add-condition 6, add-step 5 | hawks-043, FaroeIslands-016, geometrydash-025, lost-048 |
| help given or traded against a third room | 11 | 11 | add-condition 5, add-step 5, link 1 | purdue-021, thailand-020, texastech-056 |
| an apology or a repaired wrong opens help (P07 to P16; no arrow draws it) | 6 | 6 | link 6 | DCFU-054, japan-032, neopets-070 |
| help passed as a tool: a script shared, fixed or run for another room | 5 | 5 | add-step 5 | aeon-011, RelientK-040, spacexmasterrace-025 |
| help refused because a script would place it | 2 | 2 | add-condition 2 | rangers-018, rust-036 |
| a design or layout shaped so other rooms can help | 2 | 2 | link 2 | eesti-041, roosterteeth-031 |

**What the 19 rejects show.**
- **Instantiate, 5.**
  - One is a border concession, P08's (day9-013: 'moving the first letter for you as a gesture of friendly cooperation in the agreement').
  - Three are proposals inside the room to ask, with no request made (gameattack-031, winnipegjets-025, zelda-020).
  - One is a greeting from a visitor who names no room (ice_poseidon-064).
- **Absent, 14.** Each line's concepts show P16, so the claim of absence fails:
  - credit to a kindred room for making the work (Homura-022);
  - a call between kindred groups to join against a third (TheGreatGreenBox-016, as GreenEmpire-004);
  - outreach or requests reaching other rooms (WisconsinBadgers-016, lexington-019, anarchocapitalism-032, oltp-013);
  - help offered from outside the room (gameboy-029, crystalclear-022);
  - members' hands on other rooms' works (natsume-027, scp-031, paranatural-035);
  - joint work between kindred rooms (ravens-036, rojava-025), and a request to be taken in by a hub (tetris-025).

  WisconsinBadgers-016 and oltp-013 were marked `not-testable`.

**Absent lines.** No line is marked `observed-absent` or `not-needed`, so P16 has no evidenced absence. The 98 evidence limits are requests to the room's own readers, helpers whom the words do not place outside the room, border and space talk (P08), and proposals to ask. A guard listed 61 limits whose labels share a word with P16 ('help' in most). I read each again, and quoted the ones where a helper might stand outside the room; one changed (oltp-013).

**Particulars, 26.**
- **Failing portability (23):**
  - instantiate: Northwestern-022, PORTUGALCARALHO-021, Slovakia-014, aoe2-020, auburn-018, cavestory-018, cirkeltrek-028, counting-021, crusaderkings-018, dbz-020, ethereum-018, eve-018, flyers-012, hearthstone-033, hungary-021, lakers-027, lakers-030, mariokart-005, monstercat-017, ockytop-012, sixers-021, spacex-007;
  - absent: nyu-030.
- **One room only (3).** A search of P16's lines found no second room for any of them.
  - foxes-039: an attacker from another group turned helper by the work itself.
  - xcom-018: help grounded in the room's own trouble finding space.
  - thenetherlands-029: the room's framing of a friendly day grounds a request to help a neighbour.

**Re-ruled in this leg.** None.

**No correction, so no §2 re-examination.** No restrict, add-condition or contradict line was accepted as a correction. P16 stands as served, and no move was made.

**Repairs (G7).** Repairs made no difference. Repaired rooms were 0.949 accepted (531 lines), and unrepaired rooms 0.960 (454 lines).

**Carried to later groups.**
- **The giver's side of A13.** 55 instantiate reasons send help once the room's own work is safe, and links name it (corridor-067, lithuania-060, smashbros-029, placetardis-060). Help given before a work of its own is A13's bound (hearthstone-042, wow-051, wow-016). These go to A13's group, with F-008.
- **A border opening help** (cloud9-060, h3h3productions-064) goes to A14's group.
- **An apology or a repaired wrong opening help** (6 links) has no arrow. It goes beside A16 and A17.
- **Ties from before the canvas grounding help** (11 lines) go beside C02 and K03, for the clustering.
- **Help against a third room** (11 lines) goes beside A15 and A19.
- **Scripts refused as help and help passed as a tool** (7 lines) go beside A06 and P14.
- **Guests and hosts** (battlecats-028, hatsune-017, clubpenguin-017, metalcore-023, orderofthebluecorner-032, yuyuyu-007) go to P19's group.
- **A request made after hour 73** (sadboys-024) goes beside the close.

**Disclosed limits and slips.**
- **Draws.** There were seven seeded draws over the instantiate lines, at verb offsets 258 to 858, ten lines each (the last over 69 lines). None found an unsupported line.
- **The compaction.** The context was compacted after instantiate lines 0 to 99. I did the hook's steps, logged them, and re-read the handback, the elements, A13, A14 and the last history lines before ruling on.
- **One reason was corrected before writing.** undertale-026's c0090 proposes spending clicks on a neighbour's flag; it does not report it. The ruling rests on c0246.
- **The first absent file**, `P16-absent.jsonl` (13 rejects), is superseded by `P16-absent-r2.jsonl` after oltp-013 was read again. The first never reached the ledger, and the pair check ran over the 19 files in use.
- **The add-condition counts** were first logged with P08 at 9 and with P17 and A14 left out. A grep showed 7 lines held to terms and 2 kept apart, and a second line gives the full counts.
- **The group close** tabulates rejects under 'specification'. The rulings store them with no kind.
- **A stray token** (`for_x=1`) was typed into one command. It ran and changed nothing.
- **A refused command.** While trimming the head, I sent a no-op heredoc as a probe. The rules forbid both; the permission check refused it, and nothing ran.

### Close-check, D3a-10

`validate.py D3` reports 10,803 of 42,243 ledger lines ruled. That is the 9,818 ruled through D3a-09 and P16's 985. It reports 0 errors and 2 warnings, the same two as before: history lines 137 and 138, which name move 174 'stabilizing' (line 139 records the correct name). All 37 pairs in P16's files name a P16 line (`_analysis/d3_pair_check.py`). The ledger holds 10,822 lines, 19 of them appended re-rulings across the legs, none from this leg. History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561. None of those ledgers changed in this leg. The blind check's files are in `_analysis/d3_blind/`. QD3-003 is open.

## D3a-11: G4a applied backwards (QD3-003, QD3-004)

J answered QD3-003: 'Backward I would say.' During the leg J answered QD3-004: 'Amend G4a to cover link lines and apply it backwards to them as well.' Both amendments are written under G4a in the ruling rules, dated 18 October. I logged the rules for the pass before I re-ruled any line.

**Scope.** The pass read again every add-condition, add-step and link line of the closed groups that stood as a paired elaboration or a particular: R01, P01, P02, P05, P04, P12 and P22, K01, P03 and P11. It also checked P16's add lines, which G4a ruled at D3a-10. It did not re-rule instantiate, restrict, contradict or absent lines, and it changed no correction, so moves 172 to 174 stand.

**How.** For each line I asked one question. Is the relation the line adds already stated in its element's statement or range, in another element's statement or range, or in an arrow's connection, bound or mechanism? `_analysis/d3_arrows_brief.py` prints the arrows' parts for this. Where one statement held a whole family, `_analysis/d3_g4ab_family_rows.py` wrote the family's rows from a phrase over my earlier reasons. It keeps each line's own evidence and adds the statement the line now names. I read the ids it chose before the batch writer ran, and I ruled the other lines one by one. Each change is an appended re-ruling, and the earlier line stays in the ledger. The 636 re-rulings came from 19 files in `_analysis/d3_rulings/`: `G4aB-*` for add lines and `G4aL-*` for links. Each file was checked and run dry before it was written.

**What changed** (`_analysis/d3_rerule_transitions.py --leg D3a-11`):
- 614 paired elaborations became specifications.
- 11 particulars became specifications.
- 11 elaborations kept their kind and took a new pair, because their first pair had become a specification.
- 2 of the 625 changes to specification are P16 lines ruled at D3a-10 (below). The other 623 are in the closed groups.

The add and link lines of each group, before the leg and after it (`_analysis/d3_g4a_before_after.py`; a cell with one figure did not change; the 'after' figures match `d3_opkind.py`):

| group | op | lines | specification | elaboration | correction | evidence limit | particular | reject |
|---|---|---|---|---|---|---|---|---|
| R01 | add-condition | 3 | 0 | 1 | 0 | 1 | 1 | 0 |
| R01 | add-step | 3 | 0 → 1 | 2 | 0 | 0 | 1 → 0 | 0 |
| P01 | add-condition | 53 | 0 → 9 | 39 → 32 | 0 | 6 | 8 → 6 | 0 |
| P01 | add-step | 155 | 2 → 3 | 141 | 0 | 0 | 12 → 11 | 0 |
| P01 | link | 60 | 1 → 11 | 52 → 44 | 0 | 0 | 7 → 5 | 0 |
| P02 | add-condition | 55 | 2 → 31 | 49 → 20 | 0 | 0 | 4 | 0 |
| P02 | add-step | 115 | 7 → 46 | 102 → 63 | 0 | 3 | 3 | 0 |
| P02 | link | 84 | 1 → 43 | 81 → 39 | 0 | 2 | 0 | 0 |
| P05 | add-condition | 91 | 3 → 65 | 84 → 22 | 0 | 2 | 2 | 0 |
| P05 | add-step | 127 | 19 → 69 | 103 → 53 | 0 | 2 | 3 | 0 |
| P05 | link | 93 | 2 → 34 | 88 → 56 | 0 | 0 | 3 | 0 |
| P04 | add-condition | 47 | 2 → 35 | 44 → 12 | 0 | 0 | 1 → 0 | 0 |
| P04 | add-step | 198 | 4 → 93 | 192 → 104 | 0 | 0 | 2 → 1 | 0 |
| P04 | link | 39 | 0 → 27 | 38 → 12 | 0 | 0 | 1 → 0 | 0 |
| P12 | add-condition | 14 | 10 | 2 | 0 | 2 | 0 | 0 |
| P12 | add-step | 104 | 36 → 45 | 64 → 55 | 0 | 2 | 2 | 0 |
| P12 | link | 24 | 9 → 10 | 15 → 14 | 0 | 0 | 0 | 0 |
| P22 | add-condition | 12 | 3 → 11 | 8 → 0 | 0 | 1 | 0 | 0 |
| P22 | add-step | 12 | 6 → 10 | 5 → 1 | 0 | 1 | 0 | 0 |
| P22 | link | 3 | 1 → 3 | 2 → 0 | 0 | 0 | 0 | 0 |
| K01 | add-condition | 50 | 2 → 6 | 44 → 40 | 0 | 4 | 0 | 0 |
| K01 | add-step | 196 | 35 → 76 | 146 → 105 | 0 | 11 | 4 | 0 |
| K01 | link | 5 | 2 → 3 | 2 → 1 | 0 | 1 | 0 | 0 |
| P03 | add-condition | 16 | 1 | 11 | 0 | 2 | 2 | 0 |
| P03 | add-step | 69 | 9 → 13 | 45 → 41 | 0 | 13 | 2 | 0 |
| P03 | link | 138 | 3 → 107 | 129 → 26 | 0 | 2 | 4 → 3 | 0 |
| P11 | add-condition | 42 | 33 → 35 | 7 → 5 | 0 | 0 | 2 | 0 |
| P11 | add-step | 70 | 46 → 51 | 20 → 15 | 0 | 4 | 0 | 0 |
| P11 | link | 23 | 4 → 18 | 16 → 3 | 0 | 1 | 2 → 1 | 0 |
| P16 | add-condition | 96 | 81 | 13 | 0 | 0 | 2 | 0 |
| P16 | add-step | 48 | 32 → 34 | 15 → 13 | 0 | 1 | 0 | 0 |
| P16 | link | 33 | 23 | 9 | 0 | 0 | 1 | 0 |
| all | | 2078 | 379 → 1004 | 1569 → 955 | 0 | 61 | 69 → 58 | 0 |

No other op changed, so each group's other rows stand as its leg's table gives them. The group totals change by these rows: for example, P05 now has 811 specifications and 143 elaborations of 1,092 lines, and P04 has 817 and 147 of 1,034. P16's row in this table is its add-step row after the correction below; the D3a-10 table stands as written then.

**What the re-ruled lines name** (`_analysis/d3_g4ab_tally.py --prefix G4aB-,G4aL- --total`; a line that names two ids counts under each, and 11 lines name two):
- **The line's own element: 255.** Of these, 105 are P05's lines (upkeep before growth, covering the night, hardening the shape) and 72 are P04's. K01's own clause ('a claim … may be a joke') and its takeovers hold most of K01's.
- **P10: 104.** These are the 88 links of P03's rebuild family, 10 of P04's links and 6 of P02's lines: 'a new spot, a smaller version, a fresh start'.
- **P05: 88.** By a phrase count over the reasons, 68 name its clause on the form the keepers know (a planned change repaired away until the keepers are told), 15 'upkeep before growth', 4 its rallying to defend and 1 the night or the shape.
- **K02: 28** (too few hands or too little room, for designs sized to the hands). **P16: 23** (help and barter). **P22: 22** ('After placement ends': the close, corrected accounts, the cleanup). **P08: 22** (borders and deals held). **P07: 19** (sparing neighbours). **C01: 13** (a vote, a sanction, a division of the work). **A07: 13** (A07's bound, marking an attempt the close cut short). **A08: 9** (A08's bound, 'On the late side the record often comes first').
- **Fewer than 8 each:** P17 7 (joint marks); K01, P20 and A06 4 each; A10, A19, P01 and A04 3 each; P12 and P14 2 each (P14's range, 'a shared bot holding several rooms' works'); A16, A03, A20, P13 ('the mark in its banner') and A13 1 each.

**One form can differ in kind by op.** The add-step line h3h3productions-009 declares the logo done and moves the work to an addition above it. Adding to a mark is P02's own statement, so the line is a specification. The link line uiuc-052 adds that a finished work reopens the design. No statement or arrow draws that relation, so it stays a paired elaboration (with giivasunner-062). The step is stated; the relation is not.

**Families that stay paired elaborations**, because no statement or arrow states the relation they add:
- chats that take the call's organizing off the record (GreenCorner-011);
- teaching members how the canvas works (MMA-012);
- calls renewed after a loss, a move or a completion;
- visibility, landmarks and directions given in a form each device can use (nyjets-011);
- successor canvases (catholicism-056, hungary-030);
- a visible mark drawing helpers or keepers, and layouts passed between rooms;
- scripts that hold a work against a change members want (dota2-071);
- a host's approval deciding where the room builds, which is P19's side, a candidate (pakistan-022, re-paired);
- members bounding K01's licence by their own norms (catholicism-044), play outlasting the day, and jokes made real;
- P12's records gathered as data or archives (placeDE-058) and its meanings of flaws;
- P11's disputes over the marking, progress celebrated before the work is up, and recognition sought from the creators a work depicts (funhaus-055).

**P03's rebuild family.** I carried 88 P03 links in 87 rooms at D3a-08 as 'rebuilding after a loss or move … no arrow'. They now name P10's statement, which holds the fresh start after a loss. No arrow runs from P10 to P03, but the statement holds the relation, so the family is no longer carried as unstated.

**P11's links.** Nine links now name A08's bound: the record of the work comes before its marking (belgium-056, dota2-057). Four name A07's bound: the attempt is marked when the close cut the work short (aeon-016, columbia-052). One particular, nuclearthrone-041, names P20's 'remove canvas posts by rule'.

**P22, and move 174's list.** Move 174's history line lists elaborations 'left to D4'. It names 16 lines. 14 of them are now specifications on P22's own statement: 12 add lines (anime-062, europe-037, AyyMD-056) and 2 links (AyyMD-061 and bih-058, a cleanup of a shared copy asked to fix the work). fivenightsatfreddys-059, a restrict line, was already a specification. uwaterloo-053 stays a paired elaboration: an account tested against the record ties P12's records to P22's contests, and nothing in the model states that tie. The history line stays as written. This note records where its list now stands.

**P16, corrected.** At D3a-10 I ruled RelientK-040 and spacexmasterrace-025 as help passed as a tool. Each is another room's bot or script set to keep the room's work, which P14's range states ('a shared bot holding several rooms' works'). I missed the range then. Both are now specifications of P16 naming P14. The other three lines of that family (aeon-011, sips-020, phish-026) hand a script to another room to run itself. No statement holds that, and they stay elaborations.

**The pair check** (`_analysis/d3_pair_kind_check.py`, over every accepted elaboration). After the pass, 23 accepted elaborations had a pair whose latest ruling is no longer an accepted elaboration. Six were add lines inside G4a, and `G4aB-pairfix.jsonl` fixed them. batman-020 now names P17. wholesomememes-043 and wine-013 rest on P02's own statement. cloud9-054, drawhelix-019 and feedthebeast-024 took new pairs in their own families. The check now finds 17 of 1,018:
- **7 pair an add line with a partner ruled before this leg** as a specification or a correction, at D3a-01 to D3a-07: GuildWars2-055, lego-034, magictcg-034, coldplay-013, DCFU-056, uwaterloo-053 and yugioh-009. They stand under G4. G4 pairs a line with a second room's line that makes the same point in substance, whatever the partner's node.
- **10 are instantiate or restrict lines, which G4a does not cover.** Seven are P11 instantiate lines that mark an attempt where no work is up: Thegreatblackhole-038, albania-032, battlecats-048, chess-011, columbia-049, kamenrider-021 and ultrahardcore-031. The other three are redpandas-013 (P04), yuyuyu-005 (P05) and Madeon-006 (P03, restrict). They stand under G1, G9 and G16 with their pairs kept. QD3-005 asks J whether G4a's second clause should reach them.

**Carried items that changed.**
- **Rebuilding after a loss or move (P03)** is now named by P10's statement. It leaves the carried list.
- **P11's marked attempts and record-first marking.** The add and link lines now name A07's and A08's bounds. The instantiate lines wait on QD3-005.
- **The layout telling keepers (P04 into P05), and upkeep against growth.** The add and link lines now name P05's clause on the form the keepers know and its 'upkeep before growth'. redpandas-013 waits on QD3-005.
- **P22's elaborations left to D4.** Only uwaterloo-053 remains (above).
- The other carried items are unchanged. They include calls recurring after a loss, a finished work reopening the design, an apology opening help, scripts refused as help, and P19's guests and hosts.

**No move.** No element's statement, range or arrow changed. The pass changed the kinds of lines, not the model. It accepted no correction, so no §2 re-examination is due.

**Slips.**
- **Counts from memory.** A diary line gave K01's split and P04's figures from memory, and some were wrong. A later line corrects them from `d3_g4ab_tally.py`.
- **The QD3-005 count.** The question says the pass 'has moved 628 such lines from paired elaboration to specification'. At that moment 628 re-rulings were written. 620 of them moved to specification (609 from paired elaboration and 11 from particular), and 8 kept their kind with a new pair. The pair fixes then added 5 changes and 3 re-pairings. The question does not depend on the count.
- **G4a on P16's links (D3a-10).** I cited G4a on link lines before any amendment covered them. J's answer to QD3-004 now covers them.
- **P14's range (D3a-10)**, missed for two P16 lines and corrected above.
- **Two Edits in one turn.** I sent two Edits to one helper, `d3_g4ab_tally.py`, in one turn, against the rule on parallel writes. Both applied, and the helper's total agrees with the ledger (636 re-rulings by both counts).

### Close-check, D3a-11

`validate.py D3` reports 10,803 of 42,243 ledger lines ruled, unchanged, since this leg wrote re-rulings only. It reports 0 errors and the same 2 warnings (history lines 137 and 138, move 174's 'stabilizing'; line 139 records the correct name). The ledger holds 11,458 lines: 10,822 at the leg's start and 636 re-rulings from this leg. That makes 655 appended re-rulings in all. The pair check finds 17 elaborations whose pair is no longer an elaboration, each accounted for above. History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561. None of those ledgers changed in this leg. QD3-003 and QD3-004 are answered, and QD3-005 is open.

### QD3-005: the count J asked for (after the first close)

J answered QD3-005: 'First count how many instantiate and restrict lines would move; keep them as ruled until I decide.' My meanwhile was the same: those rulings stand as written. So no ruling rested on a wrong assumption, and no ruling changed. I logged the rules for the count before I read any line. The result is a working file, `_analysis/d3_qd3005_count.jsonl`, with one row per line read. Nothing was written to `adjudications.jsonl`.

**The population** (`_analysis/d3_qd3005_population.py`). The eleven closed groups hold 7,320 instantiate and restrict lines. I read the 68 that G4a's second clause could reach: 63 paired elaborations and 5 particulars ruled on one room's evidence. The others stay outside the count, each for a reason:
- 6,771 specifications already have the kind the clause would give.
- 233 particulars by construction (portability false, or the room named in the line) stay particulars under rule 5, whatever the model states.
- 119 evidence limits and 110 rejects rest on what the concepts show, not on where a form sits in the model.
- 18 corrections were accepted because the element as it stood failed in the room, and moves 172 and 173 rest on them. Another element's statement does not undo that failure.
- 1 line is a modify (R01).

The first run counted 9 one-room particulars. The reasons of four P22 lines say 'NONPORTABLE', which the helper's pattern missed. They are particulars by construction, and the helper now reads that word.

**The test.** I applied G4a's four clauses as amended at D3a-11, with the same reading of 'states it' as the add-line pass. Where the pass had already ruled a family, I followed it.

**The count** (`_analysis/d3_qd3005_check.py`: all 68 lines appear once, none is missing and none is extra):

| outcome | lines | where |
|---|---|---|
| would move to specification | 16 | P11 13 (instantiate 10, restrict 3), P03 restrict 1, P04 instantiate 1, P05 instantiate 1 |
| uncertain | 1 | R01 restrict 1 (a particular) |
| would change kind, not to specification | 2 | R01 instantiate 2 (particular to paired elaboration) |
| stays as ruled | 49 | P04 18, P11 12, P05 11, P03 6, P01 1, P02 1 |

- **The 16 that would move.** All 16 are paired elaborations now.
  - 13 P11 lines would name A07's bound, the family 'marking where no work is up' (D3a-09). They are Thegreatblackhole-038, albania-032, battlecats-048, chess-011, columbia-049, homelab-034, kamenrider-021, raocow-022, ultrahardcore-031 and warthunder-057 (instantiate), and homelab-035, mizzou-011 and warthunder-058 (restrict).
  - Madeon-006 (P03, restrict) is a report that the work already exists, answering a call to make it again. It would name P03's own statement and A01's bound, as its pair spacexmasterrace-010 does.
  - redpandas-013 (P04) is a revised layout that a placer missed until challenged. It would name P05's clause on the form the keepers know, as its pair twice-012 does.
  - yuyuyu-005 (P05) defends the host's land where the room is to write its mark. It would name P16 (defence of another room's work, help traded for space), as its pair starcitizen-013 does.
- **Uncertain: thailand-008** (R01, restrict, a one-room particular). It separates the member who starts an enlargement from the unobserved first start. P02's 'adds to it or enlarges it' states the enlargement, so clause 2 would make the line a specification of R01 naming P02. But the line is about whom the coder took as the starter, so clause 3 (a coding rule, ruled by its concepts) may govern it instead.
- **A change of kind, not a move: AcePlace-029 and TransFlagPlace-003** (R01, particulars). Each is a start on a board opened after the close. Successor canvases stayed elaborations in the add-line pass, so nothing in the model states the form. But the two rooms show the same form, so clause 4 would pair them instead of holding each as a particular.
- **The 49 that stay**, by family: landmarks (8), successor canvases (9 across P03, P04, P05 and P11), layouts passed between rooms (3), a placed part as the reference (2), outside builders (2), progress celebrated before the work is up (4), credit named before the work is up (2), marking disputed or denied inside the room (4), upkeep and growth weighed, disputed or reversed (4), whether to keep defending (2), and single lines (chats, a screen checked against the refreshed canvas, a few members building, a layout for hand placers beside scripts, the work's state as a signal of the hold, posts taken down, one work let go, calls run in parallel, a refusal to own a mark). Each family stayed an elaboration in the add-line pass, or no statement holds it.

**Pairs.** Each of the 16 is paired with a line that the pass already made a specification, or with another of the 16. No staying elaboration has its pair among the 16, so no pair would break. If the 16 moved, the 10 open-boundary lines listed above would all be resolved. The elaborations whose pair is another kind would fall from 17 to the 7 older ones.

**A reading to weigh with the count.** A07's bound reads: 'Where hour 73 cut the work unfinished, the room marks the attempt instead.' Five of the 13 P11 lines match those words: albania-032, chess-011, homelab-034, homelab-035 and ultrahardcore-031. The other eight mark a work lost, or left unfinished, before the close. For kamenrider-021 the reason does not fix the hour. They rest on the D3a-09 reading of the family 'marking where no work is up' as A07's bound (24 lines in 14 rooms). I carried that reading to A07's group, to weigh whether the form belongs in the bound or in P11's statement. The add and link lines of the family were re-ruled on the same reading this leg (battlecats-049, columbia-050, columbia-052, indonesia-056). If A07's group keeps the bound to the close, those lines and these eight need a fresh look. The reading is not an amendment, and the count follows it as stated.

### Close-check, D3a-11 (after the count)

No ledger changed after the first close. The ledger still holds 11,458 lines, 10,803 of them ruled. History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561. The new files are `_analysis/d3_qd3005_population.py`, `d3_qd3005_check.py`, `d3_latest_grep.py`, `d3_line_fields.py` and the count file. QD3-005 stays open: the 68 lines stand as ruled until J decides.

## D3a-12: G4a extended to instantiate and restrict lines; A07's bound read wider

J's message on the QD3-005 count (18 October, 23:22 Berlin): 'Extend G4a to the 16 instantiate and restrict lines and apply it backwards. Before ruling on A07's bound, set out your wider reading and the lines that rest on it; keep those as ruled until I decide.' The amendment is written under G4a above. Below, I set out the wider reading first. I wrote this part before I ruled any line that names A07.

### My wider reading of A07's bound, and the lines that rest on it

**The bound's words.** A07 runs from P03 (building and reports) to P11 (marking the work). Its bound reads: 'Where the room's first mark was found already made by others, the room celebrates the find before it builds anything itself. Where hour 73 cut the work unfinished, the room marks the attempt instead: "We almost did it!" (ultrahardcore), a watermark mourned (totallynotrobots).' The second sentence names one case: the close came while the work was still unfinished, and the room marks the attempt.

**My reading.** At D3a-09 I wrote into G16 that P11 does not say a room marks only what is up. I named 'marking where no work is up' as 'the form A07's bound names'. In ruling, I took the bound to cover any marking where no finished work stands when the room marks it:
- an attempt the close cut short, which is the bound's own case;
- a part or remnant left standing when the goal had already failed;
- a work lost to attack, erased or given up before the close;
- a plan that the close stopped before any work was placed.

The bound's words cover only the first. The reading widened the bound from the close cutting a work to any absence of a finished work at the time of marking. It is a reading, stated in G16, not an amendment. At D3a-09 I carried it to A07's group, to weigh whether the form belongs in A07's bound or in P11's statement.

**What the reading decided.**
- **At D3a-09:** it made a family of 24 paired elaborations in 14 rooms, and it decided two absent lines as rejects, because their concepts mark an attempt.
- **At D3a-11:** G4a, applied backwards, moved the family's 11 add and link lines, and 2 P12 add lines, to specifications naming A07.
- **For this leg:** it makes 13 of the 16 counted instantiate and restrict lines specifications naming A07.

**The 28 lines that cite the reading,** by what their concepts show. I took the hours from `cite.py` or from my reasons.

| what the concepts show | lines | instantiate and restrict (elaborations now) | add, link and P12 (specifications naming A07 now) | absent (rejects now) |
|---|---|---|---|---|
| the close cut an unfinished work, marked at or after the close (the bound's words) | 9 | albania-032, chess-011, homelab-034, homelab-035, ultrahardcore-031 | aeon-013, aeon-016, chess-056, chess-059 | |
| mixed: the goal failed before the close and a part still standing is marked at the close, or the close stopped a plan with no work placed | 3 | kamenrider-021 | kamenrider-022 | aeskwadraat-016 |
| a work lost, given up or left unfinished before the close | 16 | Thegreatblackhole-038, battlecats-048, columbia-049, raocow-022, warthunder-057, warthunder-058, mizzou-011 | battlecats-049, columbia-050, columbia-052, faeria-048, indonesia-056, indonesia-059, raocow-057, portal-048 | wsu-037 |

The evidence, in short:
- **The bound's words.**
  - albania c0048, at hour 73.17: 'we managed to build half of the eagle before the game closed; we are proud of half our flag'.
  - chess: the knight was unfinished at the close. c0063 'Rip r/place' comes at hour 74.11, and c0072 says 'Means a lot even if it never got finished!'.
  - homelab c0053, at hour 79.28: 'I can see the logo started but we ran out of time'.
  - ultrahardcore c0213: the close came 'before we were done'.
  - aeon c0004 and c0005: the close came when the drawing was nearly finished.
- **Mixed.**
  - kamenrider c0022, at hour 59.9: 'we didn't achieve our goals, but at least we got a part of Mighty on the canvas!'. Then c0041, at hour 73.17: 'it's Game Over. At least you can see the eye'.
  - aeskwadraat: c0003, at hour 69.96, is still shrinking the design for want of people. Then c0005, at hour 73.27: 'place is gestopt ... Leuk geprobeerd' ('place has stopped ... a nice try').
- **Before the close.**
  - Thegreatblackhole c0056: bots killed the work by hour 72.2.
  - battlecats c0185, at hour 65.6: 'It has been destroyed now, but we did it!'.
  - columbia: the work was 'paved over by a blue blob'.
  - faeria: a half-built work was given up.
  - indonesia c0118, at hour 73.48: 'WE HAVE NO FLAG', in a thread mourning a lost flag.
  - raocow c0052, at hour 73.27: 'we had it up for a couple hours'.
  - warthunder c0081, at hour 58.9: the plane is 'half way through' and 'kinda ... a WWII wreck'.
  - mizzou: the spot was lost, and the room had no final spot.
  - portal c0040, at hour 27.0: 'This isn't going anywhere'.
  - wsu: the work was drawn over by hour 53.1.

**The lines that rest on the wider reading: 19** (the mixed 3 and the 16 before the close). They keep their present rulings until J decides:
- 8 instantiate and restrict lines stay paired elaborations: Thegreatblackhole-038, battlecats-048, columbia-049, kamenrider-021, raocow-022, warthunder-057, warthunder-058 and mizzou-011.
- 9 add, link and P12 lines stay specifications naming A07: battlecats-049, columbia-050, columbia-052, faeria-048, indonesia-056, indonesia-059, kamenrider-022, raocow-057 and portal-048. portal-048 also names A10's bound for the work given up.
- 2 absent lines stay rejects: aeskwadraat-016 and wsu-037.

**What a narrower reading would change.** Suppose the bound covers only a work cut by the close. Then:
- the 8 instantiate and restrict lines stay paired elaborations, among themselves;
- the 9 specifications return to paired elaborations, unless another statement holds them (portal-048 could stand on A10's bound alone);
- the 2 absent rejects need a fresh reading, to see whether their concepts show P11 as stated;
- G16's sentence that names the family as the form of A07's bound needs an amendment.

The other choice that I carried at D3a-09 is to state the form in P11's own statement, which would change the element.

**Lines that cite the reading but do not rest on it.**
- 42 P11 absent lines are evidence limits whose reasons test 'nor an attempt marked'. They are limits under either reading.
- pebble-032 (`not-needed`) mourns an unfinished icon and marks nothing.
- ReBoot-053 names A07 as the arrow's order, not its bound.

**A slip found while setting this out.** My D3a-11 reason for raocow-057 says 'a work cut unfinished by hour 73'. But c0052 says the work was up 'for a couple hours' and the canvas 'ended unsuccessfully'. The work was lost before the close, as raocow-022's reason says. The ruling rests on the wider reading and stays as J asks. The reason's wording is wrong.

**Asked.** QD3-007 asks J whether the bound should be read this widely. QD3-006 asks whether the extension applies forward, and whether it reaches the three lines the count found outside the 16.

### The ruling

I ruled 8 of the 16 lines, from `_analysis/d3_rulings/G4aIR-D3a12.jsonl`. The file was checked, run dry and written once. All 8 moved from paired elaboration to specification (`_analysis/d3_rerule_transitions.py --leg D3a-12`):
- **Madeon-006** (P03, restrict) is a report of a work already done, answering a call to make it. That is P03's own report and A01's bound (the call recruits to a mark already started), as spacexmasterrace-010 is ruled.
- **redpandas-013** (P04, instantiate) is a revised layout undone until it reaches the room's placers. That is P05's clause on the form the keepers know, as twice-012 is ruled.
- **yuyuyu-005** (P05, instantiate): members defend the host's land where the room is to write its mark. That is P16's help between rooms, as starcitizen-013 is ruled.
- **albania-032, chess-011, homelab-034 and ultrahardcore-031** (instantiate) **and homelab-035** (restrict) mark a work the close cut unfinished. That is A07's bound in its own words.

**Kept as ruled.**
- The 8 instantiate and restrict lines on the wider reading stay paired elaborations (QD3-007).
- thailand-008, AcePlace-029 and TransFlagPlace-003 stay as ruled (QD3-006).

**Pairs** (`_analysis/d3_pair_kind_check.py`). 11 of 1,010 accepted elaborations now pair with a line of another kind:
- the 7 older ones listed at D3a-11;
- 4 P11 lines on the wider reading, whose partners are specifications on the same reading: Thegreatblackhole-038 and battlecats-048 with indonesia-056, and columbia-049 and kamenrider-021 with faeria-048. Both sides wait on QD3-007.

The other four lines on the wider reading pair among themselves: raocow-022, warthunder-057 and warthunder-058 with mizzou-011, and mizzou-011 with warthunder-058. No line I ruled here left an elaboration without its pair.

**No move.** No element, range or arrow changed. The leg changed the kinds of 8 lines and no correction was accepted.

### Close-check, D3a-12

`validate.py D3` reports 10,803 of 42,243 ledger lines ruled, unchanged, and 0 errors. Its 2 warnings are the old ones on history lines 137 and 138. The ledger holds 11,466 lines: 11,458 at the leg's start and 8 re-rulings from this leg, so 663 re-rulings are appended in all. History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. QD3-006 and QD3-007 are open.

## D3a-13: J's answers to QD3-006 and QD3-007

Both answers came during the leg, after P08's group was opened and before any P08 line was ruled. I acted on them first.

**QD3-006.** J's leaning: 'apply the extension forward; thailand-008 stays as ruled; pair AcePlace-029 and TransFlagPlace-003 as one paired elaboration. But you know these rooms: do what you judge best, and record why.' I judged the same.
- **Forward.** This was my meanwhile, so nothing rested on a wrong assumption.
- **thailand-008 stays a particular.** The line is about whom the coder took as the starter, which is clause 3's ground. Its concept, an apology for a third flag meant to enlarge the work, shows no start.
- **AcePlace-029 and TransFlagPlace-003 are now a paired elaboration of R01.** Each shows a start on a board opened after the close. No statement holds that, and two rooms show it, so clause 4 pairs them. Successor canvases are paired the same way elsewhere.

**QD3-007.** J's leaning: 'state the wider form in P11's own statement, as a revision of the element, rather than stretch A07's bound. If you would rather not revise an element in D3, keep the bound to the close cutting the work. You are the one who has read the population: judge which is best, and record why.' I kept the bound to its words and did not revise P11. The amendment and its three reasons are written under G16. In short:
- P11's fourth-order theme is a completion ritual over 522 rooms.
- No line shows P11 failing.
- The family of about 16 rooms is the subform level that D4's clustering weighs.

**Re-rulings** (`_analysis/d3_rulings/G16A-D3a13.jsonl`, 15 lines; checked, run dry, written once; the ledger now holds 11,481 lines):
- **Back to paired elaborations, within the family: 9 lines** that named A07 on the wider reading. They are battlecats-049 (pair Thegreatblackhole-038), columbia-050 (mizzou-011), columbia-052 (indonesia-059), faeria-048 (kamenrider-021), indonesia-056 (raocow-022), indonesia-059 (columbia-052) and kamenrider-022 (faeria-048) for P11, and raocow-057 and portal-048 for P12, each the other's pair. raocow-057's new reason corrects the D3a-11 wording.
- **Read again: 2 absent lines** that were rejects. aeskwadraat-016 (a plan stopped by the close, then 'a nice try') and wsu-037 (a lost work's 'good effort') show the family's form. They show neither P11 as stated nor a clean absence of it, so both are now evidence limits.
- **Reasons corrected, kind and pair kept: 2 lines.** mizzou-011 and warthunder-058 no longer say that A07's bound names their form.
- **Paired: 2 lines,** AcePlace-029 and TransFlagPlace-003 (QD3-006).

The 9 lines on the bound's own words keep their rulings as specifications naming A07. They are albania-032, chess-011, homelab-034, homelab-035 and ultrahardcore-031, ruled at D3a-12, and aeon-013, aeon-016, chess-056 and chess-059.

**Pairs.** The pair check now finds 7 elaborations whose pair is another kind: the 7 older ones. The family's elaborations all pair within the family.

**No move.** No element, range or arrow changed. The family 'marking an attempt that ended without a finished work' (P11, about 16 rooms) is carried to D4's clustering as a candidate subform of the completion ritual.

## D3a-13: P08, borders, truces and deals

P08 is the standing element of T4-016 (Negotiated order). The field's tentative entry P21 sits under the same fourth-order theme and takes its own group. P08's statement reads: 'Rooms propose, settle and contest borders, truces and deals with neighbours by talk, through envoys, and hold each other to them.' Its range runs from a one-line border agreed in a thread to treaties across languages kept and broken over a day. It has stood since C2's first pass. A04 (P05 to P08) runs into it; A05 (to P07), A14 (to P16) and the tentative A21 (to P21) run out of it; A17 runs from P09 to it. No finding touches P08. All 969 lines are ruled under G18 and G4a, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_field_entry_counts.py`, `d3_family_counts.py` and `d3_g4ab_tally.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 589 | 544 | 0 | 0 | 3 | 15 | 27 |
| absent (129 `unobserved`, 4 `not-testable`) | 133 | 0 | 0 | 0 | 124 | 1 | 8 |
| add-step | 127 | 93 | 25 | 0 | 5 | 4 | 0 |
| add-condition | 68 | 35 | 31 | 0 | 1 | 1 | 0 |
| link | 36 | 24 | 11 | 0 | 1 | 0 | 0 |
| restrict | 16 | 10 | 1 | 0 | 5 | 0 | 0 |
| all | 969 | 706 | 68 | 0 | 139 | 21 | 35 |

703 rooms have a P08 line. P08 is shown in 546 of the 705 rooms, and in 530 of them an instantiate line is accepted. 157 rooms have P08 lines and none shows it. No line records an evidenced absence.

**What the rulings show**, by rooms whose reasons name a form (`d3_field_entry_counts.py`; a room can show several):
- truces, treaties, peace or pacts: 222 rooms;
- borders or boundaries: 186;
- moves or relocations settled by talk: 146;
- terms that trade something (in return, in exchange, for help, for space): 82;
- permission or approval: 79;
- talk carried in a chat (Discord, IRC, Telegram): 75;
- envoys, diplomats, ambassadors or representatives: 32;
- agreements broken or contested as broken: 24.

42 rooms' reasons place the line at P08's lower range: one offer, one request, one claim or one report.

**Restrict: no correction.** Most restrict lines say that the record shows a proposal and not a settlement, or a member's commitment and not every placer's. P08 claims neither: its statement holds proposing, and its range holds agreements kept and broken. So no restrict line shows P08 failing. 10 are specifications by their concepts. 5 are evidence limits, where the concepts show no terms at all (CelticFc-013, cuboulder-017, k_on-014, penguins-024, uiowa-052). norway-016 is a paired elaboration of P21's form.

**Add and link lines under G4a**, by what the specifications name (`d3_g4ab_tally.py --prefix P08-addcond`, `P08-addstep`, `P08-link`):
- **P05's clause on the form the keepers know: 28 add lines (11 add-condition, 17 add-step).** The room's own keepers or scripts undo an agreed change until they are told, so the agreement has to be carried to them: harrypotter-028, giantbomb-034, skyrim-053, rotmg-017. megaman-035 names P05's 'upkeep before growth' instead.
- **A04: 21 lines (3 add-condition, 7 add-step, 11 link).** Border talk comes during building, at a new site, or before the room has a mark to keep, which is A04's bound. darksouls-058 names A04's connection and mechanism instead.
- **K02: 6.** Terms are accepted because the room judges it would lose the fight (korea-022, israel-025, farmcarrots-023).
- **P16: 5.** Space is traded for help.
- **A14: 3.** Help comes before or after border terms, A14's connection and bound.
- **A05: 3.** Sparing comes before talk, or talk is missing before attacks.
- **P02: 3.** Terms are refused, or made, by what the mark shows.
- **A17: 2.** A call to fight is met by a truce.
- **P14: 2.** One script or bot holds both rooms' works.
- **P20: 2.** An automoderator removes a peace request, or members object to a flood of petitions.
- **K01: 1** (a truce offered as a joke) and **C01: 1** (war or retreat left to the moderators).
- **P08's own statement or range: 75.**

**The 68 elaborations, by family** (all paired; lines, then rooms; `d3_family_counts.py`):

| family | lines | rooms | ops | examples |
|---|---|---|---|---|
| P21's form, a tentative entry: an agreement that cannot bind every placer, a member disclaiming that their word commits the room, or a counterpart needed who can act for the group | 30 | 29 | add-condition 19, add-step 10, restrict 1 | bisexual-030, sixers-042, splatoon-015, liquicity-024 |
| P19's form, a candidate: a host's approval rights or standing rules over guests | 9 | 9 | add-condition 7, add-step 2 | gamindustri-016, maryland-016, warframe-052 |
| a room's expansion into a neighbour prompting terms (no arrow runs from P02's enlarging to P08) | 5 | 5 | link 5 | czech-028, factorio-024, placecanada-028 |
| terms that sacrifice a third room's work | 3 | 3 | add-step 3 | Dustforce-021, germany-014, uofmn-054 |
| working out who placed the damage before taking responsibility under terms (P06's form, a candidate) | 3 | 3 | add-step 3 | faeria-022, megaman-034, ucf-016 |
| border talk on a successor canvas | 3 | 3 | link 3 | ainbowroad-041, frankocean-058, sadboys-038 |
| terms pressed by a stronger neighbour | 3 | 3 | add-condition 3 | borussiadortmund-027, earthbound-020, eesti-045 |
| terms across a rivalry from before the canvas | 2 | 2 | add-step 2 | AyyMD-057, edmontonoilers-063 |
| a work read as abandoned before terms | 2 | 2 | add-step 2 | NewMexico-024, hoodr-019 |
| records used as proof of who was first | 2 | 2 | add-step 2 | costa_rica-052, worldpowers-023 |
| few hands drawing a neighbour into terms (K02 states the judgment, not its link to P08) | 2 | 2 | link 2 | redhotchilipeppers-006, rwby-024 |
| damage destroying trust in terms | 2 | 2 | add-condition 2 | GreenCorner-030, eesti-044 |
| a truce that ends with the canvas | 2 | 2 | add-step 1, link 1 | liverpoolfc-031, reddevils-043 |

**What the 35 rejects show.**
- **Instantiate, 27:**
  - 10 proposals inside the room to ask, with no request made (reading at line 111);
  - 6 cases of help traded for help (P16);
  - 5 choices or tacit yielding inside the room (Dorset-008, PinkUnion-018, ethoslab-012, freedomplanet-017, mordhau-016);
  - 3 appeals to stop damage with no terms (P07);
  - 1 joint mark with no terms (afip-017);
  - 1 request to a lone placer (anaheimducks-029);
  - 1 report of other factions' agreements in general (minecraft-023).
- **Absent, 8.** Each line's concepts show P08, so the claim of absence fails:
  - talks reported (CSUFoCo-023);
  - a sign's terms settled between two DC rooms (DCFU-009);
  - claims to space traded (TreePlace-018);
  - requests for space made (WisconsinBadgers-014, guatemala-019, tetris-024);
  - a placement offered and accepted (carletonu-018);
  - a peace invoked (buffalowizards-014).

  buffalowizards-014 and carletonu-018 were marked `not-testable`.

**Absent lines.** No line is marked `observed-absent` or `not-needed`, so P08 has no evidenced absence. The 124 evidence limits show calls, defence, locations, help (P16), alliances (P17), appeals (P07) and choices inside the room, with no terms talked between rooms. For the three lines whose placements carry P08, I read the concepts first.

**Particulars, 21.**
- **Failing portability (17):**
  - instantiate: FaroeIslands-013, RelientK-019, RelientK-020, ainbowroad-017, chicago-021, czech-025, dragonquest-021, drawhelix-027, elitedangerous-020, frankocean-025, furry_irl-023, gameofthrones-029, lakers-029, spain-010, startrek-020;
  - absent: bahrain-010;
  - add-step: monsterhunter-026.
- **One room only (4).** A search of P08's lines found no second room for any of them.
  - starvstheforcesofevil-027: a neighbour agrees to move because its scripts can carry the move.
  - floridagators-055: a room mediating between two other rooms.
  - onepunchman-023: priority in a claim to space by a community's age.
  - utahjazz-031: outreach to a neighbour, blamed for drawing resistance, withdrawn.

**Re-ruled in this leg.**
- liverpoolfc-031 changed from particular to a paired elaboration. When the links were read, reddevils-043 showed the other side of the same truce ending with the canvas.
- Four reasons were reworded with they/them, with the same rulings (`P08-pronouns.jsonl`).

**No correction, so no §2 re-examination.** No restrict, add-condition or contradict line was accepted as a correction. P08 stands as served, and no move was made.

**Repairs (G7).** Repairs made no difference. Repaired rooms were 0.939 accepted (522 lines), and unrepaired rooms 0.946 (447 lines).

**Carried to later groups.**
- **P21's form** (30 lines, 29 rooms) goes to P21's group. Once P21's status is ruled, these lines are read again under G4a.
- **P19's form** (9 lines) goes to P19's group.
- **Border talk before the room has a mark to keep** (21 add and link lines name A04's bound or connection) goes to A04's group. It is the commonest route the add and link lines show into P08.
- **Agreed changes carried to the keepers** (28 add lines name P05's clause). Agreements with neighbours are among the changes the clause covers, for P05's re-check rooms.
- **Terms against a third room and terms across a rivalry from before the canvas** go beside A15, A19, C02 and K03, as P16's families do.
- **Expansion into a neighbour prompting terms** (5 links; no arrow) and **few hands drawing terms** (2 links) go to the clustering.
- **Attribution before responsibility** (3) goes beside the candidate P06.
- **Records as proof in a contest over space** (2) go beside P12's records in P22's contests (uwaterloo-053).
- **Border talk on successor canvases** (3) joins the successor-canvas families of P05, P04, P11 and R01.

**Disclosed limits and slips.**
- **Draws.** There were six seeded draws over the instantiate lines, at verb offsets 328 to 828, ten lines each. The first covered 99 of its packet's lines in the verb's order. None found an unsupported line.
- **Counts logged before the tally.** The first notes on the add-condition and add-step lines gave counts by named statement from my own count, and some were wrong (P05, K02, A04). Later notes correct them from `d3_g4ab_tally.py`.
- **Pronouns.** Four reasons gave members a pronoun the record does not state. They were re-ruled with the same decisions (see above). Pronouns for the fictional characters in the artworks stay.
- **liverpoolfc-031** was first ruled a particular, before the link lines that held its pair were read.
- **Two Edits in one turn.** While updating the head, I sent two Edits to `_head.md` in one turn, against the rule on parallel writes. Both applied to different passages, and the head was then checked whole (3,000 words; links resolve).

### Close-check, D3a-13

`validate.py D3` reports 11,772 of 42,243 ledger lines ruled: the 10,803 before this leg and P08's 969. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 12,455 lines: 969 first rulings and 20 re-rulings from this leg (15 under G16's amendment and QD3-006, 4 pronoun corrections, 1 pair found). That makes 683 appended re-rulings in all.
- **Pairs.** All 69 pairs in P08's files name a P08 line (`d3_pair_check.py`). Across the ledger, 7 elaborations, the 7 older ones, pair with a line of another kind.
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged.
- **Questions.** QD3-006 and QD3-007 are answered, and no question is open.

## D3a-14: J's answers to QD3-006 and QD3-007, read again

I read both answers at the start of the leg (`mem.py asks`). Both were acted on at D3a-13 (section above), so no work rested on an assumption. QD3-006's meanwhile was that G4a's extension applies forward. It matches J's leaning, and this leg applies it to P07's instantiate and restrict lines. The 15 re-rulings under G16's amendment stand.

## D3a-14: P07, sparing, reining in, apology and appeal

P07 is the standing element of T4-015 (Live and let live). Its statement reads: 'Rooms spare their neighbours' work, rein in their own attackers, apologise for damage and appeal to attackers to stop.' Its range runs from one member refusing to cover a neighbour to a room restoring a work it had damaged. It has stood since C2's first pass, and pass 7 removed 'without a written agreement' from its statement. A05 (P08 to P07, thin) and A16 (P09 to P07, strong) run into it, and no arrow runs out of it. No finding touches P07. All 933 lines, in 699 rooms, are ruled under G19 and G4a, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_field_entry_counts.py`, `d3_family_counts.py` and `d3_g4ab_tally.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 615 | 593 | 0 | 0 | 0 | 16 | 6 |
| absent (124 `unobserved`, 1 `observed-absent`) | 125 | 1 | 0 | 0 | 107 | 2 | 15 |
| add-condition | 75 | 56 | 16 | 0 | 2 | 1 | 0 |
| add-step | 54 | 38 | 10 | 0 | 4 | 2 | 0 |
| link | 35 | 21 | 13 | 0 | 1 | 0 | 0 |
| restrict | 29 | 17 | 2 | 0 | 9 | 1 | 0 |
| all | 933 | 726 | 41 | 0 | 123 | 22 | 21 |

P07 is shown in 575 of the 705 rooms, and in 554 of them an instantiate line is accepted. 124 rooms have P07 lines and none shows it. One line records an evidenced absence (montenegro-021).

**What the rulings show.** These are counts of rooms whose reasons name a form. Each count is a pattern over the reasons, a room can show several forms, and the counts are rough.
- apologies: 165 rooms;
- appeals to stop or to spare: 148;
- refusals of attack calls or of proposed covering: 145;
- reining in the room's own members: 138;
- restoring or rebuilding a damaged work: 109;
- sparing by site, size or design: 83;
- sparing by an agreement, truce or deal: 74;
- a stated norm: 42.

**Restrict: no correction.** The 29 restrict lines say one of four things: restraint is selective; one member's word does not bind every placer; a refusal or an apology does not show compliance; or the cited concepts show no restraint. P07 claims neither universal compliance nor restraint toward every work, so no restrict line shows P07 failing. 17 are specifications by their concepts. 9 are evidence limits, where the concepts show no restraint (for example ik_ihe-012, kanye-029 and ukplace-044). Two are a pair of P21's form (FloydVsVoid-031, flyers-052), and one fails portability.

**Add and link lines under G4a**, by what the specifications name (`d3_g4ab_tally.py --prefix P07-addcond,P07-addstep,P07-link`; NieR-032 names two):
- **A05: 20.** Its bound holds sparing that comes first and tacit, before any talk, or that rests on the room's own norm. Its mechanism holds sparing by a settled border or space, kept and reminded. Examples: MonkeyIsland-017, chelseafc-034, kilian-019, vegan-059.
- **A16: 18.** Its mechanism holds restraint whose reason is the attack's cost (retaliation, a fight the room cannot win, its reputation, its allies) or the room's norm. Its connection holds the room's act against another's work coming before its apology or reining in. Examples: kindafunny-013, uva-059, bisexual-064, nascar-048.
- **P05: 17.** Restraint that holds only once it reaches the room's keepers, placers or scripts: a forgotten script that undoes a peace, defenders who repair a neighbour's intended pixels, plans sent to placers who have not seen them (python-026, flashtv-069, seolhyun-053, minnesotavikings-013).
- **P08: 5.** Deals that hold sparing, and help on condition of non-interference (germany-012, newzealand-058).
- **P22: 2.** A restoration and an apology cut off by the close (osugame-033, foxes-023).
- **C01: 1.** A host moderator's ban warning against recruiting defacement (greenbaypackers-013).
- **P07's own statement, or the line ruled by its concepts as a counting rule: 53.** About thirty add lines are rules for reading the record ('does not prove every placer complied', 'attribute restraint to particular speakers'), and each is ruled by its concepts.

**The 41 elaborations, by family** (all paired; lines, then rooms; `d3_family_counts.py`):

| family | lines | rooms | ops | examples |
|---|---|---|---|---|
| P06's form, a candidate: damage worked out as the room's own mistake, or as another's doing, before an apology, yielding or peace | 11 | 11 | add-condition 1, add-step 3, link 7 | nerf-016, japan-031, theitalyplace-017, Russiaclan-055 |
| restraint drawn by the room's ties to the target's makers (allies, kin, a conference, a fandom, a shared history) while others are attacked | 10 | 10 | add-condition 7, link 3 | k_on-013, wildhockey-018, WisconsinBadgers-055, PurplePixels-015 |
| P21's form, a tentative entry: the room cannot stop every placer acting in its name | 5 | 5 | add-condition 3, restrict 2 | costa_rica-053, twice-028, flyers-052 |
| a neighbour's help as the reason to spare its work | 4 | 4 | add-condition 2, link 2 | uruguay-028, southafrica-040, Okami-013 |
| the attack, or amends to one room, sent onto a third room's work | 4 | 4 | add-condition 3, add-step 1 | hsv-024, CKCrusaders-055, chibears-033 |
| the room's own loss as the reason to spare others | 3 | 3 | add-step 3 | armenia-039, mindcrack-028, anarcho_capitalism-017 |
| competing duties of restraint: sparing one work costs another | 2 | 2 | add-step 2 | neopets-065, purplecorner-020 |
| a layout obtained to restore a neighbour's work | 2 | 2 | add-step 1, link 1 | opticgaming-024, PlaceNL-066 |

The helper misses PurplePixels-015, whose reason holds '; ' inside a parenthesis; read by hand, it belongs to the second family.

**What the 21 rejects show.**
- **Instantiate, 6:**
  - restraint toward talk only (babymetal-029, worldpowers-025);
  - help and a condolence (denverbroncos-025, the unsupported draw);
  - a call for help (sabres-020);
  - an instruction to message attackers, with no appeal made (pusheen-008);
  - an attack put off for tactics (nintendo-017).
- **Absent, 15.** Each line's concepts show P07, so the claim of absence fails:
  - an assurance of no harm (Homura-020, lego-025);
  - sparing by site or yielding (OKState-021, TheAdventuresofTintin-017, Villanova-025, marvel-020, superman-022, wsu-022);
  - calls not to provoke (ProfessorLayton-029, nightinthewoods-027);
  - an objection to a war call, and an attack withdrawn (Pigifs-028, acecombat-020);
  - appeals (VelvetUnderground-027, scp-029, starryknights-011).

**Absent lines.** 124 lines are marked `unobserved` and one `observed-absent`. The room's placements carry P07 in none of them. 107 are evidence limits: calls, defence, loss reports, help (P16), terms (P08), host rules and celebrations, with no restraint toward another's work. montenegro-021 is an evidenced absence: a visitor asks for a deal so both designs stay, and the room answers that it cannot. P07 is not stated as universal, so that line is not a correction.

**Particulars, 22.**
- **Failing portability (21):**
  - instantiate: Dominican-026, GranColombia-025, Moondye7-017, Northwestern-018, Russiaclan-007, battlecats-022, day9-015, ethereum-015, germany-010, guatemala-017, lakers-026, linux-066, onepunchman-028, thepointing-012, torontoraptors-025, virginiatech-007;
  - absent: borderlands-032, nyu-028;
  - add-condition asktransgender-016, add-step armok-024, restrict onepunchman-029.
- **One room only (1).** vocaloid-054: repair reached by a member's change of view in the thread. A search of P07's lines found no second room.

**No correction, so no §2 re-examination.** No restrict, add-condition or contradict line was accepted as a correction. P07 stands as served, and no move was made.

**Repairs (G7).** Repairs made no difference. Repaired rooms were 0.961 accepted (509 lines), and unrepaired rooms 0.946 (424 lines).

**Carried to later groups.**
- **P06's form** (11 lines) goes beside the candidate P06, with P08's 3 lines of the same form. Working out who did the damage, or finding one's own mistake, comes before an apology or peace.
- **P21's form** (5 lines) goes to P21's group with P08's 30.
- **Restraint by ties to the target's makers** (10 lines) and **help as the reason to spare** (4) go to the clustering. Both bear on the account's condition between its best and its most threatening room: what decides whom a room fights and whom it spares.
- **The attack sent onto a third room's work** (4) joins P08's family of terms that sacrifice a third room's work, beside A15, A19, C02 and K03.
- **The room's own loss as the reason** (3) goes beside A10 and P10.
- **Restraint carried to the keepers** (17 add and link lines name P05's clause) goes with P08's 28 such lines to P05's re-check rooms.
- **Restraint and apologies that concern only talk** (the reading at line 105) go beside P18.

**Disclosed limits and slips.**
- **Draws.** Seven seeded draws covered the instantiate lines, at verb offsets 254 to 854, ten lines each (the last over 16 lines). Two found an unsupported line.
  - Draw 2 (offset 354) found denverbroncos-025. Instantiate lines 99 to 198 were then read whole with every line's quotes, through a new helper, `_analysis/d3_window_quotes.py`. One other ruling changed: babymetal-029 was rejected.
  - Draw 7 (offset 854) found worldpowers-025. Lines 599 to 614 were read whole with quotes, and nothing else changed.
- **G19 corrected before any line was ruled.** Its appeal clause first said 'with no terms named', which would have taken appeals that also name a limit or place out of P07.
- **Counts logged before the tally.** The restrict note first gave 18 specifications and 8 evidence limits. The family counts were typed before `d3_family_counts.py` ran. Correction notes followed from the tallies, and the families matched.
- **An unchecked claim.** One note said packet 1 held no case of a later reading. It was corrected in the same leg: packet 1 holds close cases, all accepted, and no reject.
- **A refused command.** The permission check refused a grep piped to `cut -c`, and I used the latest-ruling helper instead.

### Close-check, D3a-14

`validate.py D3` reports 12,705 of 42,243 ledger lines ruled: the 11,772 before this leg and P07's 933. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 13,388 lines: 933 first rulings from this leg and no re-rulings. That leaves 683 appended re-rulings in all.
- **Pairs.** All 41 pairs in P07's files name a ruled P07 line (`d3_pair_check.py`). Across the ledger, 7 elaborations, the 7 older ones, pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. The model's hashes are unchanged (elements 4b4e277f…, arrows e0ba1b0b…).
- **Questions.** None is open.

## D3a-15: P09, attacks on others' work

P09 is the standing element of T4-020 (dimension D08). Its statement reads: 'Rooms attack others' work by the recurring moves the canvas affords: erasing, encroaching, converting a sign, raiding on a streamer's call, planting a script, altering a work as a joke.' Its range runs from one member's call to deface a rival to a coordinated raid. It has stood since C2's first pass. A15 (P01 to P09) runs into it, and A16, A17 and A18 run out of it. No finding touches P09. G20 was written before any line was ruled, and amended once in this leg (above). All 886 lines, in 703 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_field_entry_counts.py`, `d3_family_counts.py`, `d3_g4ab_tally.py` and a new helper, `d3_latest_ids.py`, which lists ids by their latest ruling.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 558 | 494 | 1 | 0 | 6 | 29 | 28 |
| absent | 169 | 1 | 0 | 0 | 145 | 1 | 22 |
| restrict | 77 | 41 | 0 | 0 | 33 | 3 | 0 |
| add-condition | 35 | 24 | 4 | 0 | 7 | 0 | 0 |
| link | 25 | 7 | 13 | 0 | 2 | 3 | 0 |
| add-step | 22 | 10 | 8 | 0 | 2 | 2 | 0 |
| all | 886 | 577 | 26 | 0 | 195 | 38 | 50 |

P09 is shown in 510 of the 705 rooms, and in 467 of them an instantiate line is accepted. 193 rooms have P09 lines and none shows it. G20 took T4-020's count, 231 rooms, as the reason P09 is not universal. The return shows P09 in more than twice as many rooms. Many accepted lines lift through other fourth-order themes, such as T4-016's border work and T4-006, T4-013 and T4-014. P09 is still not universal, since 193 rooms show no attack, so no absent line is a correction. The gap between 231 and 510 is a fact about T4-020's placements. I report it and change no ruling for it.

**Restrict: no correction.** The 77 restrict lines mostly ask for an enacted attack, a room-level campaign, a named target or a stated motive. P09 needs none of these: its range starts at one member's call, and a call need not be carried out. Other restrict lines restate G20: an attack the room suffers, a visitor's call, the room's own work altered, or a call after the close. Each line is a specification where its concepts show P09 (41). It is an evidence limit where they do not (33). Three fail portability. No restrict line shows P09 failing.

**Add and link lines under G4a.** The specifications name these statements (`d3_g4ab_tally.py --prefix P09`):
- **P22: 8.** A call that meets or follows the close at hour 73 (anaheimducks-067, croatia-014, quebec-065), and a picture of the canvas edited after it (torontoraptors-059).
- **A16: 5.** An attack call answered by a refusal that states the room's norm (roosterteeth-053, samuraijack-074). Restraint that comes before the call (canada-056, criticalrole-059). Acceptance as the preferred answer (teamcube-056).
- **P05: 4.** An attack that uses the keepers' repair of the form they know (austria-062, theblackvoid-015). Defence on the room's own work (donaldglover-038). Growth after upkeep (wallstreetbets-065).
- **P14: 3.** Scripts adjusted against another's work (rit-057, loltyler1-041, unitedkingdom-053).
- **A17: 2, A18: 2, K01: 1, P04: 1.** An attack call met by the room's alliances, and border talk before it (canucks-076, DatBoi-057). The contest carried on in talk after the attack (completeanarchy-056, shitredditsays-043). A joke claim under the day's licence (OnePiece-072). Coordinates asked for a raid's target (dankmemes-063).
- **P09's own statement, or the line ruled by its concepts as a reading rule.** The rest of the accepted add and link lines.

**The 26 elaborations, by family.** All are paired, and the counts give lines, then rooms (`d3_family_counts.py`):

| family | lines | rooms | ops | ids |
|---|---|---|---|---|
| the place the room needs for its work is taken from another's work (a new spot after a loss, or a place the room insists on) | 4 | 4 | link 4 | russia-064, liquicity-036, paladins-077, 2007scape-039 |
| retaliation: an attack the room suffers prompts its attack on the attacker's work | 4 | 4 | add-step 1, link 3 | AMD-057, leafs-056, Clannad-019, k_on-016 |
| the target chosen by its weak defence, with no tie to its makers | 3 | 2 | add-condition 1, add-step 2 | zelda-048, zelda-047, theblackvoid-057 |
| the attack shrunk to the hands and effort the room has | 3 | 3 | add-step 2, link 1 | destiny-009, fullcommunism-065, sabres-005 |
| covering others' work is itself the building of the room's mark | 2 | 2 | add-condition 1, instantiate 1 | Thegreatblackhole-046, theblackvoid-056 |
| an attack on another's work made to protect the room's own | 2 | 2 | add-condition 1, link 1 | anarcho_capitalism-047, lakers-082 |
| judging hands or space too small for the room's own work turns it to attack | 2 | 2 | add-condition 1, link 1 | kurdistan-054, canucks-040 |
| a loss turns members from rebuilding to attacking another's work | 2 | 2 | link 2 | dbz-072, loltyler1-046 |
| a target chosen because it shares the room's colours, so few pixels change | 2 | 2 | add-step 2 | latvia-023, luxembourg-054 |
| a simple pattern draws passers-by who extend it over others' work | 2 | 2 | add-step 1, link 1 | shitredditsays-042, opticgaming-040 |

Five families concern why and when a room attacks (13 lines): retaliation, protection, a loss, too few hands, and the attack shrunk to the hands. They put P05, P10 and K02 before P09, and no arrow in the model does that. Three families concern where and what a room attacks (9 lines): the place it needs, weak defence and shared colours. One family is the Void's form, in which the attack is the work. The tenth is a simple pattern that passers-by extend over others' work, beyond the room's control.

**What the 50 rejects show.**
- **Instantiate, 28:**
  - an attack the room suffers, by visitors or another room (Goodboye-042, TheHulk-029, WPI-030, duckgame-028, foxes-036, parabola-014, winnipegjets-053);
  - defence of the room's own work, or a defence call withdrawn (bindingofisaac-015, metalgearsolid-060, shishamo-009, texans-040, xcom-039, yugioh-066, titanfall-058);
  - the room's own work altered by members or placers (chelseafc-063, day9-027, gatech-059, kirby-038, linux-064, polska-027);
  - a visitor's attack offer that no member took up (archlinux-040, colombia-028, hearthstone-065, kamenrider-024, pakistan-047, thepointing-020);
  - fandom play against the room's own proposal (transformers-023), and K02's judgment alone (rotmg-047).
- **Absent, 22.** Each line's concepts show P09, so the claim of absence fails:
  - an attack or cover the room is told of (COSI-027, Cornwall-048, DCFU-010, colorado-033, evedreddit-033, livecounting-033, miraculousladybug-058);
  - a member's call or plan to take or cover another's work (Dorset-009, Honduras-036, bangtan-042, carletonu-035, nin-054, riskofrain-047, twitch-046);
  - covering or encroaching admitted (Produce101-013, ScottPilgrim-033, hatsune-041, seventeen-045);
  - a member who joined the Void (Jamaica-058, necrodancer-056);
  - an attack reported by a member (lego-049, ubreddit-051).

**Absent lines.** 146 are marked `unobserved`, 22 `not-testable` and one `observed-absent`. 145 are evidence limits: calls, defence, loss reports, help, terms, taunts and celebrations, with no attack on another's work. mit-029 is an evidenced absence: the room notes that a larger work would mean fighting a banner, and it defends its small logo instead.

**Particulars, 38.**
- **Failing portability (32):** 28 instantiate lines, 3 restrict lines (borderlands-016, empiredidnothingwrong-062, patriots-046) and 1 absent line (mariokart-022).
- **One room only (6).** A search of all 886 P09 lines through `d3_line_search.py` found no second room for these:
  - cubers-074: attack calls on a canvas opened after hour 73;
  - bees-009: converting a work to punish its makers for encroaching on a third room's work;
  - falcons-058 and falcons-059: erasing a rival so the saved final picture does not hold it;
  - dwarffortress-033: helping the Void because canvas posts feel like spam. philippines-041 gives the same motive, but against the room's own flag, which is not P09.
  - witcher-056: a neighbour's complaint turning a member to attack the complainant's work.

**No correction, so no §2 re-examination.** No restrict, add-condition or contradict line was accepted as a correction. P09 stands as served, and no move was made.

**Repairs (G7).** Repairs made little difference. Lines in repaired rooms were 0.910 accepted (479 lines), and in unrepaired rooms 0.889 (407 lines).

**Carried to later groups.**
- **The five 'why and when' families** (13 lines) go to the clustering and the order tests: P05, P10 and K02 before P09. Retaliation and protection bear on the account's condition between its best and its most threatening room, what decides whom a room fights. The loss and hands families go beside A10 and P10.
- **The three 'where and what' families** (9 lines) go beside C02. C02 names a prior tie in some rooms, and these rooms choose by the place they need and by cost.
- **The Void's form** (2 lines) goes beside K04's colour faith, a candidate.
- **P21's form** appears beside P09 specifications and elaborations (smashbros-059, ScottPilgrim-033, opticgaming-040), and goes to P21's group.
- **Attacks after the close** (8 add lines name P22; cubers-074's successor canvas) go beside P22.

**Disclosed limits and slips.**
- **Draws.** Six seeded draws covered the instantiate lines, at verb offsets 226 to 726, ten lines each. Draw 6 found winnipegjets-053 unsupported: c0066 vows to change the room's own lettering. Lines 499 to 557 were read whole with every line's quotes, and timbers-010 kept its ruling.
- **Five re-rulings, appended.**
  - uiowa-009: a reject that misread G20 (it led to amendment 1).
  - theblackvoid-056: a specification that became Thegreatblackhole-046's pair once that line was read.
  - kurdistan-054: a particular written before canucks-040 was read.
  - DevonUK-052: a reject that read two concepts without the member's answer naming Cornwall.
  - liquicity-034: an evidence limit that read c0064 without its thread, found when the link line liquicity-036 read the same turn differently.
- **Two reasons edited before the check.** A claim in uoft-055's reason, and one in wario-004's, were not supported by the record. Both were rewritten from the record before the file was checked.

### Close-check, D3a-15

`validate.py D3` reports 13,591 of 42,243 ledger lines ruled: the 12,705 before this leg and P09's 886. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 14,279 lines: 886 first rulings and 5 re-rulings from this leg. That makes 688 appended re-rulings in all.
- **Pairs.** All 26 pairs in P09's files name a ruled P09 line that is an accepted elaboration (`d3_pair_check.py`, `d3_pair_kind_check.py --elements P09`). Across the ledger, 1,156 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind.
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. The model's hashes are unchanged (elements 4b4e277f…, arrows e0ba1b0b…).
- **Questions.** None is open.

## D3a-16: P18, the contest in talk

P18 is the standing element of T4-021 (Rivalry, dimension D08). Its statement reads: 'Rooms carry a contest with a rival room in talk: they trade taunts, flood the rival's threads, claim victory, salute the rival after the fight and blame attackers after the close.' Its range runs from one taunt in a thread to days of chants, victory claims and an after-the-fight salute. A18 (P09 to P18) runs into it, and no arrow runs out of it. No finding touches P18. G21 was written before any P18 line was read, and amended once in this leg (above). All 778 lines, in 698 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_field_entry_counts.py`, `d3_family_counts.py`, `d3_g4ab_tally.py`, `d3_latest_ids.py` and a new helper, `d3_reject_kinds.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 457 | 373 | 0 | 0 | 0 | 16 | 68 |
| absent (226 `unobserved`, 4 `not-testable`) | 230 | 0 | 0 | 0 | 205 | 3 | 22 |
| restrict | 45 | 25 | 0 | 0 | 20 | 0 | 0 |
| add-step | 24 | 18 | 0 | 0 | 5 | 1 | 0 |
| add-condition | 14 | 7 | 0 | 0 | 7 | 0 | 0 |
| link | 8 | 2 | 6 | 0 | 0 | 0 | 0 |
| all | 778 | 425 | 6 | 0 | 237 | 20 | 90 |

P18 is shown in 404 of the 705 rooms, and in 361 of them an instantiate line is accepted. 294 rooms have P18 lines and none shows it. T4-021 holds 116 rooms, so P18, like P09, is shown in many rooms whose talk was placed under other fourth-order themes. P18 is not stated as universal, so no absent line is a correction.

**What the specifications show.** These are rough counts of lines whose reasons match a pattern. The first matching pattern takes each line, and 116 lines match none: retorts, threats, chants and rows in words.
- victory claims, including holding off a named rival: 79 lines in 77 rooms;
- blame of attackers after the close: 23 lines in 22 rooms;
- salutes, 'good game' and the contest's end: 20 lines in 19 rooms;
- mock wars and war declarations: 20 lines in 19 rooms;
- flooding, raiding or brigading a rival's threads or chat: 9 lines in 8 rooms;
- insults, curses, taunts, jabs and gloating: 221 lines in 208 rooms.

**Restrict: no correction.** Most of the 45 restrict lines ask for a reciprocal campaign, two coherent rooms or a verified attacker. P18 needs none of these, since one taunt is its lower range. The other lines restate G21: the contest must be part of the event, a rival is a group, internal play does not count, and a visitor's taunt is the visitor's. Each line is a specification where its concepts show P18 (25), and an evidence limit where they do not (20).

**Add and link lines under G4a.** Two specifications name another statement. placehfarts-012 names A18: an attack proposal comes before a victory claim. the_pack-043 names P20: members debate whether a rival may advertise in the room. The other specifications rest on P18's own statement, or are reading rules ruled by their concepts.

**The 6 elaborations, by family.** All are paired; the counts give lines, then rooms (`d3_family_counts.py`):

| family | lines | rooms | ops | ids |
|---|---|---|---|---|
| contest talk opened from a neighbour's request about space, with no attack before it | 3 | 3 | link 3 | evedreddit-032, qotsa-043, aceattorney-057 |
| an attack the room suffers, not one it makes, brings the rival into its contest talk during the event | 3 | 3 | link 3 | rangers-065, starryknights-060, uvic-056 |

Both families put something other than the room's own attack before the contest in talk. A18 orders the room's first attack before its first taunt, and P18 names being attacked only for blame after the close. Both families go to the order tests beside A18.

**What the 90 rejects show.**
- **Instantiate, 68.** They are sorted roughly by the first matching pattern over the reasons (`d3_reject_kinds.py`):
  - about 40 rest on a visitor's taunt, chant, salute, claim or accusation that no member answers in kind;
  - about 12 are records of the work's fate or of defence, P12's or P05's;
  - about 9 are defence calls, terms, refusals or restraint, P05's, P08's or P07's;
  - 7 others: a neighbour's own record (denverbroncos-070), a joke to the room's own members (evex-022), a flat denial (fivenightsatfreddys-072), listening in a rival's chat (monalisaclan-064), sympathy for a third room (palestine-016), corrections of accounts (placecanada-059, P22's) and a concession (wine-059).
- **Absent, 22.** Each line's concepts show P18, so the claim of absence fails. They hold:
  - slogans, threats or vows against a rival faction (GreenEmpire-037, dankmemes-026, darksouls-030, faeria-059, morrowind-054);
  - curses or pejorative labels (RelientK-059, monstercat-039, mordhau-033, re_zero-038);
  - jabs at a rival's conduct (GuildWars2-035, kuwait-041);
  - claims of holding off attackers or a named rival (PinkVomitMonster-024, paragon-056);
  - retorts or a victory boast (SwissNeutralityZone-033, TreePlace-041, hearthstone-068, hyperlightdrifter-034, nlsscirclejerk-021, uiowa-018);
  - a returned salute (paranatural-058), a victory claim with mockery (halo-019), and blame after the close (berserk-065).

**Absent lines.** 226 are marked `unobserved` and 4 `not-testable`. 205 are evidence limits: calls, defence, records, celebration, terms, attack calls (P09's), visitors' talk and members' talk among themselves, with no contest carried by the room.

**Particulars, 20.**
- **Failing portability (19):** 16 instantiate lines and 3 absent lines (nyu-058, redpandas-059, vim-039).
- **One room only (1):** sooners-049. An insult in talk turns members toward a takeover, the reverse of A18's order. A search of P18's lines found no second room; sooners-048 is the same room.

**No correction, so no §2 re-examination.** No restrict, add-condition or contradict line was accepted as a correction. P18 stands as served, and no move was made.

**Repairs (G7).** Repairs made no difference. Lines in repaired rooms were 0.856 accepted (424 lines), and in unrepaired rooms 0.862 (354 lines).

**Carried to later groups.**
- **The two families** (6 lines) go to the order tests beside A18. Contest talk can open from border talk or from an attack the room suffers, not only from the room's own attack.
- **sooners-049**, talk turning to attack, goes beside A18 and P09's 'why and when' families.
- **The visitor-led contests** (about 40 instantiate rejects) are the other room's P18 seen from its target. They bear on reading P18 room by room, and go to the clustering.
- **Old quarrels and ties.** Many taunts invoke school, league or national rivalries. They go with C02, K03 and K04's group.
- **Talk-only restraint** (apologies and calls to stop inside a contest) stays beside P07, as G19 placed it.

**Disclosed limits and slips.**
- **Draws.** Five seeded draws covered the instantiate lines, at verb offsets 269 to 669, ten lines each. Draw 2 (offset 369) found earthbound-044 unsupported: its how read defence talk, and its quote opens 'Screw the task bar'. Lines 100 to 199 were then read whole with every line's quotes, through `d3_window_quotes.py`. The whole read also changed gratefuldead-063 to a reject.
- **Two re-rulings, appended.** NieR-062 was a reject read as a record of defence. It was re-ruled to a specification, to agree with Slovakia-033's claim of holding off rivals. berserk-065 was an evidence limit, re-ruled to a reject when G21 amendment 1 was applied backwards.
- **G21 amended.** It first said 'a rival' for blame after the close, against P18's 'attackers'.
- **Counts logged before the tally,** twice, and corrected in notes: the lines with quotes read in the first packet (30, not 39), and the add-step kinds (18 and 5, not 17 and 6).
- **The verb's count.** The verb's footer says 779 lines, but it lists 778 distinct ids (`d3_verb_ids2.py`). The extra unit is its header line. A first version of that helper did not stop at the verb's last page, ran past 120 seconds into the background, and was stopped before any other step.
- **A Write and its check in one turn.** P18-absent-180.jsonl was checked in the turn that wrote it, against the rule. The check passed before the ledger write, which ran alone.
- **A refused command.** The permission check refused a hash command that piped `cut -c` beside a helper. It was run again without `cut`.

### Close-check, D3a-16

`validate.py D3` reports 14,369 of 42,243 ledger lines ruled: the 13,591 before this leg and P18's 778. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 15,059 lines: 778 first rulings and 2 re-rulings from this leg. That makes 690 appended re-rulings in all.
- **Pairs.** All 6 pairs in P18's files name a ruled P18 line that is an accepted elaboration (`d3_pair_check.py`). Across the ledger, 1,162 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. The model's hashes are unchanged (elements 4b4e277f…, arrows e0ba1b0b…).
- **Questions.** None is open.

## D3a-17: P10, the room moves after a loss

P10 is a standing element of T4-014. Its statement reads: 'After the work is erased or overrun, the room weighs fighting for the spot against moving, and moves: a new spot, a smaller version, a fresh start.' Its range runs from a lone member asking where to rebuild to a room relocating together within two hours. A10 (K02 to P10) runs into it, and F-019 touches it through A10. G22 was written before any P10 line was read, and its readings are written under it (above). All 840 lines, in 697 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_field_entry_counts.py`, `d3_family_counts.py`, `d3_g4ab_tally.py` and `d3_reject_kinds.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 276 | 225 | 0 | 0 | 1 | 19 | 31 |
| absent (253 `unobserved`, 63 `not-testable`, 19 `not-needed`, 1 `observed-absent`) | 336 | 19 | 0 | 0 | 258 | 28 | 31 |
| restrict | 89 | 47 | 0 | 0 | 39 | 3 | 0 |
| add-step | 77 | 43 | 8 | 0 | 24 | 2 | 0 |
| add-condition | 43 | 21 | 0 | 0 | 21 | 1 | 0 |
| link | 16 | 7 | 1 | 0 | 7 | 1 | 0 |
| contradict | 3 | 2 | 0 | 0 | 1 | 0 | 0 |
| all | 840 | 364 | 9 | 0 | 351 | 54 | 62 |

P10 is shown in 300 of the 705 rooms, and in 223 of them an instantiate line is accepted. 397 rooms have P10 lines and none shows it. T3-022 holds 116 rooms and T3-124 holds 17, so most rooms that move after a loss had their talk placed under other themes. P10 is not stated as universal, so no absent line is a correction.

**What the specifications show.** These are rough counts. Each pattern is matched only against the reason's closing clause, and the patterns overlap.
- a weighing of fighting for the spot against moving: 59 lines in 54 rooms;
- a smaller version: 44 lines in 40 rooms;
- a fresh start: 72 lines in 67 rooms;
- hands moved from a lost work to another of the room's works: at least 6 lines in 5 rooms;
- a new spot or a move: 255 lines in 225 rooms (this pattern also takes the G3 absent lines).

**Restrict and contradict: no correction.** Most restrict lines ask that P10 count only a completed or collective move. P10's range starts at one member asking where to rebuild, and G22 counts a weighing whatever the room then does, so their condition is already stated. Other restrict lines ask that P10 admit moves made before any loss: to spare a neighbour, on a request or terms, to avoid competition, or ahead of harm not yet come. G22 gives those moves to P07, P08 and P04, so P10 does not fail without the condition. Each line is a specification where its concepts show P10 (47), and an evidence limit where they do not (39). The three contradict lines say P10 fails because a room moved before its work was erased. MiamiHurricanes-016 is a coalition's move that A10's bound reads by name. necrodancer-027 moves ahead of the advancing taskbar, which 'overrun' covers. rpi-018 is a push given up. None shows P10 failing.

**Add, link and contradict lines under G4a.** 27 specifications name another statement:
- P05 (4): keepers told to stop repairing a work being moved (berserk-029, ftlgame-023, necrodancer-028, seahawks-040);
- P04 (4): coordinates or one plan circulated for the new site (TheHulk-057, day9-018, day9-019, indieheads-020);
- A10 (4): a move on a judgment of too few hands to hold the spot (reddevils-017, dota2-024, snsd-038, MiamiHurricanes-016);
- P08 (4) and P16 (2): a move made on terms, or with help offered or not given;
- P22 (3): acts cut off by or made after the close;
- P09 (3): a new spot taken from another's work, which G22 reads as P10 and P09 at once (anarcho_capitalism-029, russia-016, streetfighter-028);
- K02, P17 and P02 (1 each): a destination judged by room and hands, alliances weighed, the smaller work's design argued.

Evidence limits on add lines follow P09's dota2-070: a condition that would widen P10 to moves G22 excludes does not add to P10, and the line is ruled by its concepts.

**The 9 elaborations, by family.** All are paired, and none is stated in the model:

| family | lines | rooms | ops | ids |
|---|---|---|---|---|
| copies of the work made while it stands, so one loss does not end it | 3 | 3 | add-step 3 | ethoslab-055, twitchplayspokemon-038, rotmg-024 |
| the rebuilt work reuses pixels already on the canvas | 2 | 2 | add-step 2 | PUBATTLEGROUNDS-030, flashtv-067 |
| the rebuilt design takes the damage into itself | 2 | 2 | add-step 2 | battlecats-036, animalcrossing-017 |
| regret for the lost work opens the fresh start | 2 | 2 | add-step 1, link 1 | pusheen-014, OrderOfTheKoi-018 |

The first family adds a step before the loss, which P10 does not have: a backup or copy. It also shows in concepts of other lines (SwissNeutralityZone c0041, russia c0094, texas c0184, toolband c0090, placeportalpattern c0080, simonfraser c0056). The other three add what the rebuilt work takes from the canvas, from the attack, or from the room's regret.

**What the 62 rejects show.**
- **Instantiate, 31.** Sorted by reason, with the helper's first-match groups corrected by hand:
  - no loss shown before the move, 8 (Moondye7-022, PurplePixels-024, Rainbow6-033, ethoslab-013, furry-036, vegan-010, ice_poseidon-020, purplecorner-024);
  - a move on terms or a request, P08's, 8 (detroitlions-020, dragonquest-028, earthbound-023, factorio-034, foxes-019, paladins-040, peterdraws-009, tinytardis-022);
  - a planned site taken or avoided, 4 (egypt-004, palestine-018, singapore-037, stardustcrusaders-020);
  - sparing or restraint, P07's, 4 (OKState-011, Okami-018, frc-025, nVade-006);
  - a push for another's spot given up, 4 (anarcho_capitalism-028, gratefuldead-031, leafs-025, sooners-026);
  - another group's loss or move, 2 (croatia-015, overwatch-049);
  - a restart on a successor canvas, P13's, 1 (AcePlace-010).
- **Absent, 31.** Each line's concepts show P10, so the claim of absence fails:
  - a move or a new spot after a loss (Cornwall-030, Peru-063, TransFlagPlace-022, chess-010, cuboulder-022, denmark-005, kuwait-067, littlewitchacademia-039, partyparrot-049, romania-008, shishamo-010, thetreesnetwork-022, twitch-027, wsu-020);
  - a fresh start (DCFU-011, DatBoi-033, FlaggyFlag-027, apocalypserising-010, finland-020, lofihiphop-023, rojava-023, unitedkingdom-019);
  - a weighing (ChronoTrigger-010, columbia-010, eesti-021, spacexmasterrace-019);
  - hands moved to another work (aromantic-022, australia-023, gorillaz-039);
  - a smaller version (asexual-010, guatemala-020).

**Absent lines.** 258 are evidence limits: calls, defence, repair, records, celebration, terms, site choices, attack calls and visitors' moves, with no move after a loss. 19 are specifications by G3. Their concepts show that no loss called for a move (17), or that the room met a loss and stayed (nin-033, starryknights-017).

**Particulars, 54.** All fail portability (G6): 19 instantiate, 28 absent, 3 restrict, 2 add-step, 1 add-condition and 1 link line. No line is a one-room particular.

**No correction, so no §2 re-examination.** No restrict, add-condition or contradict line was accepted as a correction. P10 stands as served, no move was made, and F-019 is not re-examined.

**Repairs (G7).** Lines in repaired rooms were 0.850 accepted (448 lines), and in unrepaired rooms 0.875 (392 lines). No ruling rests on the difference.

**Carried to later groups.**
- **The four families** (9 lines) go to the clustering. The copies family goes beside A10's bound and F-019, since it is a step a room takes before any loss.
- **Doubt and a move with no loss** (nightinthewoods-025, hearthstone-025, and doubt sizing a first design in aeskwadraat-004 and sadboys-063). A10's bound names early moves by choice, made before any doubt. These rooms voice doubt first and move with no loss. They go to the order tests beside A10.
- **Moves before a loss** (most restrict and add evidence limits) are P04's, P07's and P08's. They bear on A10's bound, not on P10.
- **Calls after a move** (giantbomb-041, ethereum-016, TheGreatGreenBox-020) go beside 'calls recurring after a loss (P01, P10, A10)'.
- **The line between P05 and P10.** G22's reading puts a rebuild in place after the work was gone with P10, and the repair of a standing work with P05. Both go to the clustering.

**Disclosed limits and slips.**
- **Draws.** Three seeded draws covered the instantiate lines, at verb offsets 460, 560 and 660 (the last over 76 lines), ten lines each. Every drawn line's quotes gave the ruling its how and labels give, so no packet was read whole with quotes.
- **Two re-rulings, appended.** anarcho_capitalism-028 changed from a specification to a reject when the reading on pushes was applied backwards. xenoblade_chronicles-036 changed from a reject to a specification. Its rejection read the move as made before any loss, but the room's c0038 and c0069 (ruled at xenoblade_chronicles-037) report the void destroying the original first.
- **Counts logged before the tally,** three times, and corrected in later notes: the concepts cited for instantiate lines 0 to 49 (32, not 29); a count of restrict lines on moves before a loss, typed from memory (by grep, 4 and 5 lines name G22's exclusion); and the link kinds (7 and 7, not 6 and 8).
- **A compaction** came mid-leg, after G22 was written and before it was logged. The hook's four steps were done first, and the opening note and G22 were logged after them.

### Close-check, D3a-17

`validate.py D3` reports 15,209 of 42,243 ledger lines ruled: the 14,369 before this leg and P10's 840. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 15,901 lines: 840 first rulings and 2 re-rulings from this leg. That makes 692 appended re-rulings in all.
- **Pairs.** All 9 pairs in P10's files name a ruled P10 line that is an accepted elaboration (`d3_pair_check.py`). Across the ledger, 1,171 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. The model's hashes are unchanged (elements 4b4e277f…, arrows e0ba1b0b…).
- **Questions.** None is open.

## D3a-18: K02, the room judges its hands or room too few

K02 is a standing condition of T4-012. Its statement reads: 'The room judges that it has too few hands or too little room for the work it wants: doubt, a canvas judged too full, a work judged absent or outclassed.' Its range runs from one member saying there are not enough people to defenders told to give up. A10 (K02 to P10) runs from it, and F-019 touches it through A10. G23 was written before any K02 line was read. It was amended once before any line was ruled, and its readings are written under it (above). All 747 lines, in 700 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_field_entry_counts.py`, `d3_family_counts.py`, `d3_g4ab_tally.py`, `d3_group_rulings.py` and `d3_reject_kinds.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 556 | 511 | 0 | 0 | 1 | 9 | 35 |
| absent (136 `unobserved`, 9 `not-testable`) | 145 | 0 | 0 | 0 | 134 | 0 | 11 |
| restrict | 22 | 5 | 0 | 0 | 17 | 0 | 0 |
| add-step | 14 | 11 | 0 | 0 | 1 | 2 | 0 |
| add-condition | 9 | 5 | 0 | 0 | 4 | 0 | 0 |
| link | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| all | 747 | 533 | 0 | 0 | 157 | 11 | 46 |

K02 is shown in 520 of the 705 rooms, and in 506 of them an instantiate line is accepted. 180 rooms have K02 lines and none shows it. No absent line is `not-needed` or `observed-absent`, so no line records an evidenced absence. K02 is not stated as universal, so no absent line is a correction.

**What the specifications show.** These are rough counts. Each pattern is matched only against the reason's closing clause, and the patterns overlap (38 lines name both hands and room).
- too few hands, numbers or manpower: 328 lines in 323 rooms;
- the room outclassed or outnumbered, or the work judged unable to be made or held: 101 lines in 100 rooms;
- too little room, or a canvas judged too full: 93 lines in 92 rooms;
- a work judged absent: 17 lines in 16 rooms;
- defenders or members told to give up: 8 lines in 7 rooms;
- none of these patterns: 47 lines, mostly the lower range (doubt voiced, a call that states the shortfall, time weighed against the timer).

**Restrict and add-condition lines: no correction.** Most restrict lines ask that K02 count only a judgment that is stated, made by the room's own members and voiced while placement runs. G23 already states each condition, so K02 does not fail without it. Each line is a specification where its concepts show K02 (5) and an evidence limit where they do not (17). minnesotavikings-063 is an evidence limit: c0322's author is the Browns-side builder of c0108, judging the visitors' own hands. Four add-condition lines are held by K02's statement, since K02 is the room's judgment, and its range ends at defenders told to give up (apocalypserising-052, overwatch-011, paladins-007, redpandas-005). nuclearthrone-032 names P22. Four are evidence limits.

**Add-step and link lines under G4a.** 10 specifications name another statement:
- P05 (3): growth capped, or the shape hardened, so the room's hands keep what stands (TheFarLeftSide-003, gameofthrones-022, metalgearsolid-038);
- P02 (3): the design sized to the hands judged available (rust-003; asktransgender-005 with P07; starlightstage-002 with P04);
- P04 (1): a site chosen away from a scripted group (ghibli-014);
- P16 (1): an extension called off and its hands sent to a neighbour's work (hongkong-015);
- P12 (1): a destroyed work mourned and not rebuilt for lack of hands (popheads-006);
- P22 (1): a judgment voiced after the close (nuclearthrone-032).

Three more are K02 as stated: a squeezed-out work given up (twitch-006), the judgment recurring through recruitment and later plans (vinesauce-007), and a canvas judged too full (bigbang-007). No add or link line names A10's move. In K02's add and link lines, the judgment is followed by a smaller design, capped growth, a new site, help sent elsewhere, giving up or mourning.

**No elaborations.** One step is drawn by no statement and shows in no second room, so it is a particular: in falcons-018, members dispute whether a warning that bots make manual work futile informs helpers or costs the room its helpers.

**What the 46 rejects show.**
- **Instantiate, 35.** Sorted by reason:
  - a site or design fitted with no judgment (P04, P02), 8 (TheAdventuresofTintin-006, lovelive-017, mysterydungeon-004, oneshot-004, porterrobinson-005, quebec-005, rhythmheaven-004, timbers-025);
  - a visitor's judgment, or one about another group's hands, 7 (WisconsinBadgers-003, lithuania-005, shishamo-024, ssbpm-002, tokyo-003, ukplace-003, yumenikki-004);
  - doubt about something else, or futility with no reason given, 6 (corridor-012, sakartvelo-002, twitch-003, theblackvoid-002, pansexual-002, parrots-002);
  - a call that states no lack (P01), 4 (VelvetUnderground-002, bostonbruins-011, neu-032, placesnek-002);
  - a count, a joke or a quip on size or the timer, 4 (buffalo-002, cgpgrey-006, hentai-002, liverpoolfc-003);
  - a loss or the work's state reported with no judgment (P12, P05), 3 (afip-002, homestuck-018, sheffield-028);
  - a judgment that the room can manage, 3 (achievement_hunter-019, gameofthrones-004, norge-004).
- **Absent, 11.** Each line's concepts show K02, so the claim of absence fails:
  - too few hands stated (crystalclear-018, megaman-012, mordhau-003, neopets-027, placestart-034, starryknights-016);
  - the room outnumbered or outclassed (notredame-024, wales-027, wine-006);
  - strain in keeping even a modest work (mcgill-033);
  - a work not kept against constant attack, by amendment 1 (counting-002).

**Absent lines.** 134 are evidence limits: calls that state no lack, damage reports, moves after a loss, celebrations, visitors' doubts and acts after the close. None is a specification, since no line is `not-needed` or `observed-absent`.

**Particulars, 11.** Ten fail portability (G6): 9 instantiate lines and 1 add-step line (ElderScrolls-002). One is a one-room particular (falcons-018).

**No correction, so no §2 re-examination.** No restrict or add-condition line was accepted as a correction. K02 stands as served, no move was made, and F-019 is not re-examined.

**Repairs (G7).** Lines in repaired rooms were 0.916 accepted (406 lines), and in unrepaired rooms 0.933 (341 lines). No ruling rests on the difference.

**Carried to later groups.**
- **Doubt that sizes the work before any loss.** In rust-003, starlightstage-002 and asktransgender-005, and in instantiate lines such as rpi-004, nyu-005, pitt-025 and paragon-007, the judgment is followed by a smaller design, and the cited concepts name no loss before it. A10 names only the move after a loss. These rooms go to the order tests beside A10, with P10's aeskwadraat-004 and sadboys-063.
- **Upkeep before growth after the judgment** (TheFarLeftSide-003, gameofthrones-022, metalgearsolid-038) goes beside P05 and A06. No arrow from K02 to P05 is drawn.
- **Giving up after the judgment** (twitch-006, popheads-006, apocalypserising-052, wales-027) goes beside F-019's other outcome.
- **Doubt answered inside the room** (falcons-018, and the instantiate lines planetside-007, serbia-004 and singapore-004) goes beside 'doubt costing uptake'.
- **The line between K02 and P12.** A lament for a lost work, and a lament that the room could not keep it, go to the clustering (afip-002 and pusheen-029 against counting-002).

**Disclosed limits and slips.**
- **Draws.** Six seeded draws covered the instantiate lines, at verb offsets 169, 269, 369, 469, 569 and 669 (the last over 56 lines), ten lines each. Two drawn lines were not supported by their quotes: hentai-002 (a count of helpers) and yumenikki-004 (the Swedish neighbour's judgment). So packets [200, 300) and [500, 556) were read whole with quotes before they were ruled.
- **One re-ruling, appended.** babymetal-003 changed from reject to specification when the reading on calls was refined.
- **Portability flags.** The quote windows do not print NONPORTABLE tokens. 'lost' was first written for homelab-022 and indonesia-021 without a check, and `d3_packet.py` then confirmed it. It showed 'germany' for konosuba-002, which was corrected before the file was checked.
- **A count expected before the tally.** For K02-inst-350 I expected 44 accepts and 5 rejects; the tool gave 43 and 6, and the tool's figure was logged.
- **A stray command.** One command carried a no-op shell assignment ('for_x=1;'), against the permission rules. It wrote nothing, and it was logged.
- **A compaction** came mid-leg, after the instantiate lines were ruled. The hook's four steps were done first.

### Close-check, D3a-18

`validate.py D3` reports 15,956 of 42,243 ledger lines ruled: the 15,209 before this leg and K02's 747. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 16,649 lines: 747 first rulings and 1 re-ruling from this leg. That makes 693 appended re-rulings in all.
- **Pairs.** K02's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,171 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. The model's hashes are unchanged (elements 4b4e277f…, arrows e0ba1b0b…).
- **Questions.** None is open.

## D3a-19: P14, machine hands

P14 is a standing process of T4-009 (Workarounds). Its statement reads: 'Members add placements with scripts, bots and spare accounts, and the room argues over these machine hands and adjusts them.' Its range runs from one member running spare accounts to a shared bot holding several rooms' works. A06 (P05 to P14) runs into it, and F-005 is named in its evidence. G24 was written before any P14 line was read, and its readings are written under it (above). All 962 lines, in 701 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_field_entry_counts.py`, `d3_family_counts.py`, `d3_g4ab_tally.py` and `d3_group_rulings.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 271 | 265 | 0 | 0 | 0 | 2 | 4 |
| absent (356 `unobserved`, 39 `not-testable`, 2 `observed-absent`) | 397 | 0 | 0 | 0 | 358 | 3 | 36 |
| restrict | 101 | 63 | 0 | 0 | 37 | 1 | 0 |
| add-step | 121 | 99 | 4 | 0 | 18 | 0 | 0 |
| add-condition | 50 | 44 | 1 | 0 | 5 | 0 | 0 |
| link | 22 | 20 | 1 | 0 | 1 | 0 | 0 |
| all | 962 | 491 | 6 | 0 | 419 | 6 | 40 |

P14 is shown in 320 of the 705 rooms, and in 248 of them an instantiate line is accepted. 381 rooms have P14 lines and none shows it. T4-009's prose counts 236 rooms, so many rooms that used or argued over machine hands had that talk placed under other themes. No line records an evidenced absence: the two `observed-absent` lines were rejected, because their members set their hand-made work against bots. P14 is not stated as universal, so no absent line is a correction.

**What the specifications show.** These are rough counts. Each pattern is matched against the whole reason, and the patterns overlap.
- scripts or bots: 407 lines;
- spare, alternate or throwaway accounts: 173 lines;
- arguments, stances and refusals: 89 lines;
- glitches used to place more: 10 lines.

Matched against the closing clause, 42 lines in 40 rooms stand at P14's lower range (one member's spare accounts), and 8 lines in 6 rooms at its upper range (a bot keeping several rooms' works).

**Restrict lines: no correction.** Most restrict lines ask that P14 count only verified deployment by the room's own members. P14's statement holds the room arguing over machine hands, and G24 counts scripts shared or written and members' own spare accounts. So the condition would narrow P14 below its statement, and each line is a specification where its concepts show P14 (63). The 37 evidence limits are proposals for machine hands the room did not hold (12), workarounds that did not place (5) and one tracker, reports of others' bots (3), visitors' offers (2), and hand placing, overlays and constraints.

**Add-condition, add-step and link lines under G4a.** 83 specifications name another statement:
- P05 (39): scripts keep the form the room knew, so a planned or agreed change is undone until their runners update them. This is P05's own clause, 'repaired away as damage until its keepers are told', and P05's range names scripts;
- P08 (12): scripts edited to keep terms with neighbours;
- P10 (10): scripts retargeted after a move;
- A06 (8): machine hands used for building from the start (its bound), or brought in for upkeep after a hand-made build;
- P04 (7): one template or plan the scripts follow;
- P09 (3), C01 (3: a vote or a rule for who may change the bot's target), P16 (2), P07 (2) and P20 (1).

Four lines name two statements. The rest are P14 as stated: safety and trust arguments, teaching members to run scripts, adjusting accounts and versions.

**The 6 elaborations, one family.** All are paired, and none is stated in the model:

| family | lines | rooms | ops | ids |
|---|---|---|---|---|
| the room's script is released, changed, troubleshot and kept in a chat, so access to the chat governs what the machine hands keep | 6 | 6 | link 1, add-condition 1, add-step 4 | WPI-056, ukplace-010, calgaryflames-012, reddevils-011, theitalyplace-013, wallstreetbets-018 |

WPI-056 was first ruled a particular. It was re-ruled to a paired elaboration by an appended line when ukplace-010 showed the same step in a second room.

**What the 40 rejects show.**
- **Instantiate, 4.** Each cites only a visitor's machine hands: a neighbour's own scripts (RelientK-011), a visiting script author's edit (newzealand-008), a neighbour's throwaway accounts (placeportalpattern-017), and a script offered to the room from outside (russia-006).
- **Absent, 36.** Each line's concepts show P14, so the claim of absence fails:
  - a stance on machine hands, 18 (2007scape-020, Russiaclan-014, babymetal-017, bardmains-016, berkeley-008, egypt-016, falcons-016, feedthebeast-019, floridagators-007, greyblob-012, littlewitchacademia-016, naruto-014, paladins-020, shitredditsays-012, stardewvalley-013, stlouisblues-017, theexpanse-017, yogscast-019);
  - scripts or bots shared, written, adapted or run, or members called to their spare accounts, 12 (armok-012, chess-014, formula1-008, foxstevenson-013, freedomplanet-009, ice_poseidon-013, japan-009, leafs-017, pepe-014, serbia-010, transformers-026, vim-009);
  - a glitch used to place, 6 (PurplePixels-010, anime_irl-011, battlecats-016, cardinals-015, denverbroncos-017, furry_irl-011).

**Absent lines.** 358 are evidence limits: hand placing and repair, calls, templates and overlays, reports of others' bots, moderation and comment bots, proposals, and workarounds that did not place.

**Particulars, 6.** All fail portability (G6): esperanto-007 ('telegram'), linux-068 ('linux'), totallynotrobots-012 ('python'), ohio-011 and osu-014 ('ohio', both about the 'Script Ohio' lettering, not machine hands), and zelda-010 ('lost'). No line is a one-room particular.

**No correction, so no §2 re-examination.** No restrict or add-condition line was accepted as a correction. P14 stands as served, no move was made, and F-005 is not re-examined.

**Repairs (G7).** Lines in repaired rooms were 0.952 accepted (519 lines), and in unrepaired rooms 0.953 (443 lines). No ruling rests on the difference.

**Carried to later groups.**
- **P14's two forms.** P14's statement joins using machine hands with arguing over them. So a room that refused scripts shows P14 (mindcrack-013, greyblob-012, theexpanse-017). The clustering should separate the rooms that used machine hands from those that only argued over them or refused them.
- **Scripts as P05's keepers** (39 lines). The largest named family puts scripts inside P05's clause on planned changes. It goes beside P05's revision (move 173) and A06.
- **Machine hands at building** (8 lines naming A06's bound) go to the order tests beside A06 and F-005.
- **The chat family** (6 lines) goes beside 'chats (T4-010)'.
- **Neighbours' machine hands, offered or taken up** (kingdomhearts-015, winnipegjets-014, aggies-062; thailand-011, wow-009, linux-020, russia-006) go beside P16 and P08.

**Disclosed limits and slips.**
- **Draws.** Three seeded draws covered the instantiate lines, at verb offsets 569, 669 and 769 (the last over 71 lines), ten lines each. One drawn line was doubtful: russia-006, a script offered 'for you' from outside. So packet [200, 271) was read whole with quotes before it was ruled.
- **One re-ruling, appended.** WPI-056 changed from particular to paired elaboration.
- **A count typed before the tally.** The restrict note gave '7' workarounds that did not place. The script gave 5 and one tracker, and a later note corrected it.
- **A ledger count logged one note late.** The note for absent [0, 50) gave the ledger count in the next note.
- **An Edit and its check in one turn.** While rewriting the head, one word count ran beside an Edit, which the rules forbid. The count was run again in a later turn: 3,000 words.

### Close-check, D3a-19

`validate.py D3` reports 16,918 of 42,243 ledger lines ruled: the 15,956 before this leg and P14's 962. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 17,612 lines: 962 first rulings and 1 re-ruling from this leg. That makes 694 appended re-rulings in all.
- **Pairs.** All 6 pairs in P14's files name a ruled P14 line (`d3_pair_check.py`). Across the ledger, 1,177 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. The model's hashes are unchanged (elements 4b4e277f…, arrows e0ba1b0b…).
- **Questions.** None is open.

## D3a-20: P13, carrying on

P13 is a standing process of T4-028 (Transition). Its statement reads: 'Near the close and after it, the room decides what of its temporary effort to keep: a later canvas, a new purpose for its canvas sub, the mark in its banner, ties with other rooms, the work remade elsewhere.' Its range runs from a wish to do better next year to a canvas-born collective announcing a group to carry on. A09 (P12 to P13) is the only arrow into it, and F-003 and F-004 are named in its evidence. G25 was written before any P13 line was read. Its timing sentence was amended during the leg, and its readings are written under it (above). All 959 lines, in 704 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_field_entry_counts.py`, `d3_family_counts.py`, `d3_g4ab_tally.py` and `d3_pair_check.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 325 | 302 | 5 | 0 | 0 | 12 | 6 |
| absent (395 `unobserved`, 9 `not-testable`) | 404 | 0 | 0 | 0 | 397 | 2 | 5 |
| add-step | 73 | 46 | 21 | 0 | 6 | 0 | 0 |
| add-condition | 61 | 48 | 11 | 0 | 2 | 0 | 0 |
| restrict | 55 | 39 | 1 | 0 | 14 | 1 | 0 |
| link | 36 | 19 | 17 | 0 | 0 | 0 | 0 |
| contradict | 5 | 2 | 1 | 0 | 0 | 2 | 0 |
| all | 959 | 456 | 56 | 0 | 419 | 17 | 11 |

P13 is shown in 292 of the 705 rooms, and in 274 of them an instantiate line is accepted. 412 rooms have P13 lines and none shows it. T4-028's prose counts 213 rooms. No line records an evidenced absence: all 404 absent lines are `unobserved` or `not-testable`, and many rooms' records stop at hour 73. P13 is not stated as universal, so no absent line is a correction.

**The timing amendment.** While I ruled the restrict lines and read the add-condition lines, I found that G25 counted every decision made while building through A09's bound. The bound names only a next canvas and an emblem. QD3-007 read A07's bound in its own words, so I read A09's bound the same way. I set 'near the close' at hour 61 before I printed any line's hours. Two helpers found the lines: `d3_line_hours.py`, and `d3_mixed_hours.py` (new), which reads the hours from the store. 17 lines were re-ruled by appended lines (`P13-rerule-01.jsonl`). 7 became paired elaborations, and 10 kept their kind with corrected reasons. The add-condition, add-step, link and absent lines were ruled under the amended rule. The full text is under G25.

**What the specifications show.** These are rough counts, by phrase in the reason:
- P13's lower range (one member's wish, proposal or start): 78 lines;
- A09 named (a next canvas or an emblem planned while building, or a record before carrying on): 34 lines;
- P20 named (the host's line around canvas talk): 5 lines; P02 named (a design argued on a later canvas): 1 line.

The rest are P13 as stated: later canvases taken up or declined, banners, flairs and headers, kept subs and chats, ties, and the work remade in games, prints, posters and fan art.

**Restrict and contradict lines: no correction.** Most restrict lines ask for uptake, agreement or a finished successor. P13's range starts at one member's wish, so these conditions are stated. The 14 restrict evidence limits are:
- records, the end marked, reports of fate or locating posts (apocalypserising-058, babymetal-059, osugame-051, polandball-009);
- no canvas work (de-069, empiredidnothingwrong-056, fivenightsatfreddys-052, starlightstage-065);
- a report or a question with no plan (funhaus-020, telegram-038);
- another room's work remade (animalcrossing-038), a remake made by others and shared (opticgaming-054), a celebration (Dominican-048), and newcomers welcomed (counting-048).

The 5 contradict lines argue that keeping begins before the close. One shows it near the close (TeamDignitas-021, hour 62). One shows it through an emblem that A09's bound names (miamidolphins-034). minecraft-050 shows a remake made while building, which is a paired elaboration. Two are particulars. No line shows P13 failing.

**The 56 elaborations, eight families.** All are paired, and no statement or arrow holds them:

| family | lines | rooms | ops | ids |
|---|---|---|---|---|
| keeping begun while building: a new purpose for a chat, a tie, or the work remade, shown only before hour 61 | 12 | 11 | instantiate 5, restrict 1, contradict 1, add-condition 1, add-step 2, link 2 | archlinux-034, israel-053, quebec-055; cubers-067, parahumans-051, quebec-056; gorillaz-058, minecraft-050, homestuck-060, asexuality-049, porterrobinson-058, heroesofthestorm-060 |
| the spine restarted on a later canvas: calls, design, building, defence and loss again, with no arrow from P13 | 9 | 9 | add-step 8, link 1 | FlaggyFlag-039, bindingofisaac-022, cubers-068, esperanto-057, furry_irl-052, gamindustri-037, gravityfalls-050, greenlattice-052, purplecorner-025 |
| declining or scaling down carrying on for its cost (labour, fatigue, money) or because the event's limit made it | 8 | 8 | add-condition 5, add-step 3 | denmark-041, naruto-044, theblackvoid-051, thebluecorner-057, theexpanse-056, acecombat-035, aoe2-040, lego-046 |
| choosing or leaving a later canvas by how it works: bots, captchas, timer, traffic, failures | 8 | 8 | add-condition 3, add-step 5 | ockytop-055, patriots-044, placehearts-058, AcePlace-061, aeskwadraat-019, greyblob-043, italy-064, sadboys-014 |
| canvas help, deals or cooperation as the reason for a tie kept | 8 | 8 | link 8 | belgium-057, miraculousladybug-052, mylittlepony-058, parahumans-055, scotland-044, stlouisblues-061, the_pack-054, weezer-034 |
| rules and roles that carry the kept group or chat on: goals, content rules, moderators, officers, elections | 6 | 5 | add-condition 2, add-step 3, link 1 | TheFarLeftSide-058, loliconsunite-053, AmericanFlaginPlace-060, AprilKnights-053, denmark-042, AprilKnights-019 |
| carrying on entered from marking, with no record between | 3 | 3 | link 3 | coldplay-062, starlightstage-067, utahjazz-062 |
| a damaged end as the reason to redo the work elsewhere | 2 | 2 | link 2 | frc-044, furry_irl-056 |

The pattern helper missed three lines of the first family by their wording (gorillaz-058, minecraft-050, porterrobinson-058). I counted them by hand from their reasons.

**What the 11 rejects show.**
- **Instantiate, 6.** satania-034 is ordinary posting with no word of the canvas (the unsupported draw). opticgaming-062 is a lament (P12's). rocketbeans-038 is advice on how a future event should be timed, and it carries nothing of the room's effort. nVade-052 seeks a deal ahead of the shared copy's cleanup (P22's contest, with P08's terms). skyrim-013 and stlouis-047 are neighbours' offers that no member takes up (the visitor rule).
- **Absent, 5.** Each line's concepts show P13, so the claim of absence fails: a member asks about regrouping elsewhere near the close (OrderOfTheKoi-037); print-ready files and a print wished for (colombia-041, thesilphroad-032); canvas flair and 'There's always next year' while building, which A09's bound names (PinkVomitMonster-019, hunterxhunter-048).

**Absent lines.** 397 are evidence limits: celebration, credit and the end marked (P11, P12), records and cleanups (P22), the host sub's April Fools changes, newcomers welcomed, chats with no canvas link, plans on the live canvas, and forms of the while-building family. I read the quotes of 16 candidates before ruling.

**Particulars, 17.** All fail portability (G6): 'minecraft' 9 (Moondye7-035, TeamDignitas-020, babymetal-055, babymetal-056, ice_poseidon-053, ice_poseidon-054, miamidolphins-033, minecraft-049, xcom-033), 'lost' 3 (GreenCorner-053, bih-031, israel-052), 'cirkeltrek' 1 (PlaceNL-048), 'ethereum' 1 (ethereum-039), and 3 whose reasons do not name the hit (placecanada-053, runescape-051, taiwan-036). No line is a one-room particular.

**No correction, so no §2 re-examination.** No restrict, add-condition or contradict line was accepted as a correction. P13 stands as served, no move was made, and F-003 and F-004 are not re-examined.

**Repairs (G7).** Lines in repaired rooms were 0.976 accepted (543 lines), and in unrepaired rooms 0.964 (416 lines). No ruling rests on the difference.

**Carried to later groups.**
- **The while-building family** (12 lines) goes beside A09's bound. The order tests and D4 should ask whether the bound names too few forms, or whether 'near the close' is the timing of a subform.
- **Three routes into P13** (13 lines) are candidate arrows: help or deals between rooms to a tie kept (P16 or P08 to P13), marking to carrying on with no record between (P11 to P13), and a damaged end to a remake elsewhere. They go beside A08 and A09.
- **The spine restarted** (9 lines) goes beside R01's successor-canvas pair (AcePlace-029, TransFlagPlace-003). It is a possible loop from P13 back to R01 and P01, which the account does not ground.
- **Cost and how a later canvas works** (16 lines). The clustering may separate rooms that rest from rooms that move on.
- **Roles for the kept group** (6 lines) go beside C01 and P13's upper range.
- **P13's two ends.** 78 specifications sit at the lower range. The clustering should separate one member's wish from a room's decision.

**Disclosed limits and slips.**
- **Draws.** Four seeded draws covered the instantiate lines, at verb offsets 544, 644, 744 and 844 (the last over 25 lines), ten lines each. satania-034 was not supported, so packet [200, 300) was read whole with quotes before it was ruled.
- **A rule read too widely.** G25's timing sentence read A09's bound more widely than its words. I found it during the leg, amended G25 with a dated amendment, and applied it backwards by 17 appended re-rulings. The contradict rulings were written before the amendment: minecraft-050 changed kind, and TeamDignitas-021 and miamidolphins-034 got corrected reasons.
- **Compaction.** The context was compacted after the instantiate lines. I did the hook's four steps, then read `handback-C5.md` and the model again before the next write.
- **A long window.** One `d3_window_quotes.py` window ran past two minutes and moved to the background. I waited it out in the foreground before the next step.
- **Two refused commands.** Twice a command put `cut -c` after a helper's output. The permission check refused both, and I ran them again whole.
- **A helper pattern.** `d3_family_counts.py` missed three lines by wording, and I counted them by hand.
- **Two Edits in parallel.** While rewriting the head, two Edits to it ran in parallel, which the rules forbid. They touched separate passages and both succeeded. The later edits ran one at a time, and the word count (2,997) ran in a turn apart.

### Close-check, D3a-20

`validate.py D3` reports 17,877 of 42,243 ledger lines ruled: the 16,918 before this leg and P13's 959. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 18,588 lines: 959 first rulings and 17 re-rulings from this leg. That makes 711 appended re-rulings in all.
- **Pairs.** All 56 pairs in P13's files name a ruled P13 line (`d3_pair_check.py`). Across the ledger, 1,233 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. The model's hashes are unchanged (elements 4b4e277f…, arrows e0ba1b0b…).
- **Questions.** None is open.

## D3a-21: P20, the host's line

P20 is a standing process of T4-002 (Boundary work), and it is the theme's only element. Its statement reads: 'The host sub draws a line around canvas talk: moderators gather it into a megathread, remove canvas posts by rule, change posting rules, pause the sub's usual events or disown the work; members open a canvas sub, object to the flood or argue the canvas's worth.' Its range runs from one member asking for a megathread to moderators moving all canvas talk to a new sub and removing the rest. A20 (P01 to P20) runs into it, and F-010 (bounded) is its finding. G26 was written before any line was read, and its readings are written under it (above). All 920 lines, in 704 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_field_entry_counts.py`, `d3_family_counts.py` and `d3_pair_check.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 392 | 320 | 0 | 0 | 0 | 6 | 66 |
| absent (327 `unobserved`, 14 `not-testable`, 1 `not-needed`) | 342 | 0 | 0 | 0 | 324 | 3 | 15 |
| add-step | 80 | 45 | 11 | 0 | 21 | 3 | 0 |
| restrict | 69 | 26 | 0 | 0 | 43 | 0 | 0 |
| add-condition | 30 | 15 | 7 | 0 | 7 | 1 | 0 |
| link | 7 | 2 | 3 | 0 | 1 | 1 | 0 |
| all | 920 | 408 | 21 | 0 | 396 | 14 | 81 |

P20 is shown in 310 of the 705 rooms, and in 289 of them an instantiate line is accepted. 394 rooms have P20 lines and none shows it. T4-002's prose counts 274 rooms. The one evidenced absence, TheB1G-056 (`not-needed`), was rejected: its member argued against a canvas sub that another member had just opened. P20 is not stated as universal, so no absent line is a correction.

**What the specifications show.** These are rough counts, by phrase in the reason:
- megathreads and stickies, asked for, promised or made: 113 lines;
- arguments over the canvas's worth, dismissals among them: 60 lines;
- canvas subs opened or used by a host's members: 44 lines;
- P20's lower range (one member's request, objection or dismissal): 74 lines;
- other statements named: A20 2 (its mechanism and its bound), P17 2, P02 1, P04 1, P14 1.

**Restrict lines: no correction.** Most restrict lines ask that a removal concern canvas talk, that a rule be new or enforced, or that a line be shown to work. G26's reading on removals already holds the first. P20's range, which starts at one member's request, holds the second. P20 does not claim that the line works. So 26 are specifications. The 43 evidence limits are general rules and repost habits, canvas subs' own business, April Fools changes, another sub's line discussed, curiosity, doubt and refused requests.

**The 21 elaborations, five families.** All are paired, and no statement or arrow holds them:

| family | lines | rooms | ops | ids |
|---|---|---|---|---|
| members cross or miss the line drawn: they post outside the megathread, miss the sticky on mobile, seek exposure, or carry on in the host after the talk was routed out | 8 | 8 | add-condition 5, add-step 3 | europe-032, portugal-057, stardustcrusaders-036, suomi-053, turkey-036, nintendo-066, pokemon-026, sabres-037 |
| the event's short life shapes the line: no canvas sub for three days, and requests and complaints withdrawn once the end or the length is known | 4 | 4 | add-condition 2, add-step 2 | borussiadortmund-040, polska-038, 49ers-033, xcom-029 |
| the host's removals drive members to a canvas sub or a chat | 3 | 3 | add-step 3 | anime-052, armenia-038, canada-044 |
| the line or a worth argument entered from celebration, a record or an attack, not from calls | 3 | 3 | link 3 | AMD-055, cardinals-044, paladins-080 |
| the line's automation catches ordinary uses of the word 'place' | 3 | 2 | add-step 3 | norge-051, stardustcrusaders-037, stardustcrusaders-041 |

**What the 81 rejects show.**
- **Instantiate, 66.**
  - General or format rules applied to canvas posts, 28: battlecats-046, criticalrole-022, dankmemes-028, drugs-043, futanari-008, futurama-028, halo-004 (re-ruled), hearthstone-053, india-024, kerbalspaceprogram-049, kingdomhearts-048, leagueoflegends-017, lego-039, metalcore-035, opticgaming-045, overwatch-067, paladins-056, pcmasterrace-054, stardustcrusaders-009, startrek-039, tagpro-042, twitch-036, utaustin-043, uwaterloo-044, vinesauce-042, wholesomememes-049, wholesomememes-050, wildhockey-034.
  - Canvas subs' own founding, venues or coordination, 20: AcePlace-020, AmericanFlaginPlace-050, AvoArmy-035, EraseThePlace-030, Goodboye-030, ManningPlace-041, THE_R-004, TheFarLeftSide-020, TreePlace-031, afip-028, edboxes-027, epublica-042, farmcarrots-030, nVade-044, placeDE-023, placesnek-021, placestart-040, theblackvoid-044, thebluecorner-045, tinytardis-039.
  - Praise or appraisal alone, 4: 49ers-032, israel-018, neopets-022, sabres-038.
  - Other, 14: design talk, P02's (austria-047, hunterxhunter-053, rainbowgrid-039); moderation as such (Okami-027, canucks-057); P14's and P16's grounds (egypt-041, teslamotors-047); the sub's April Fools megathread (anime-049); an opening post on what the flag means (palestine-008); advice on playing (physical_removal-034); a megathread's contents (hatsune-032); where a plan sits in a thread (giantbomb-050); a post judged late (furry_irl-040); and an observation that no flood came (gamindustri-031).
- **Absent, 15.** Each line's concepts show P20, so the claim of absence fails: canvas stickies asked, promised or made in hosts (gatech-026, littlewitchacademia-056, metalgearsolid-051, ohio-049, pusheen-025); routing into one thread or out of the host (frc-033, geometrydash-047, giivasunner-021, purdue-033, ufl-053); objections and dismissals (HomestarRunner-042, glasgow-038, theexpanse-046, udub-030); and TheB1G-056, the `not-needed` line.

**Absent lines.** 324 are evidence limits: calls, celebrations and records, chats, April Fools changes, conduct moderation and canvas subs' own business. I read the quotes of 23 candidates before ruling.

**Particulars, 14.**
- By G6, 9: counting-033 ('counting'), feedthebeast-050 ('minecraft'), loltyler1-028 ('osu'), math-032 ('math'), sooners-038 ('twice'), unitedkingdom-024 ('lost'), ice_poseidon-045 ('twitch'), sheffield-024 ('sheffield') and telegram-033 ('telegram').
- One room, with no statement holding the form and no second room's elaboration, 5:
  - a line drawn inside a chat by shutting event members out (AvoArmy-036);
  - a line drawn to shield the series' author from the canvas's attention (parahumans-044);
  - the host's rules changing how a member calls, P20 back to P01 (drugs-046);
  - spam irritation turned into joining the void (dwarffortress-032);
  - a private canvas sub that shuts helpers out (ockytop-054).

**No correction, so no §2 re-examination.** No restrict, add-condition or link line was accepted as a correction. P20 stands as served, no move was made, and F-010 is not re-examined.

**Repairs (G7).** Lines in repaired rooms were 0.883 accepted (503 lines), and in unrepaired rooms 0.914 (417 lines). The repaired rooms hold more rejects (54 against 27). No ruling rests on the difference.

**Carried to later groups.**
- **The line crossed** (8 lines). P20 says the line is drawn, not that it holds. The clustering may separate hosts whose line held from hosts whose members crossed it.
- **The clock and the line** (4 lines) go beside A20's bound and F-010: the event's short life shaped how much line a host drew.
- **Removals to other venues** (3 lines) are a possible order inside P20, a removal before a canvas sub or a chat. They go beside A20's bound, which names a canvas sub or megathread set up before any call.
- **Routes into P20** (3 lines) from celebration, records and attacks go beside A20 and A08.
- **Canvas-born rooms.** The 20 rejects and many limits for canvas subs bound P20 to rooms with business apart from the canvas. D4 should read canvas-born rooms as having no host's line, except where they name one.
- **The one-room particulars** stay in their local models.

**Disclosed limits and slips.**
- **Draws.** Four seeded draws covered the instantiate lines, at verb offsets 453, 553, 653 and 753 (the last over 92 lines), ten lines each. Every drawn line's labels agreed with its quotes, so each packet was ruled from its labels, read whole.
- **One re-ruling, appended.** halo-004 was accepted on a bare 'Existing Thread or Topic' notice. When overwatch-067 made the reading on duplicate notices explicit, I re-ruled halo-004 to reject (`P20-rerule-01.jsonl`).
- **A broad reading.** Stickies in hosts count as megathreads whatever their motive. That reading was set at bangladesh-021. A pattern count finds at least 28 lines whose reasons name a canvas sticky in a host, across instantiate, restrict, add-step and absent. In most of them the sticky is the only ground. A narrower reading, stickies only where they contain canvas talk, would move most of those lines to evidence limits.
- **A count corrected before logging.** I first wrote that this reading decided 'about a dozen' lines. The pattern count gave at least 28, and I corrected the sentence before the close.

### Close-check, D3a-21

`validate.py D3` reports 18,797 of 42,243 ledger lines ruled: the 17,877 before this leg and P20's 920. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 19,509 lines: 920 first rulings and 1 re-ruling from this leg. That makes 712 appended re-rulings in all.
- **Pairs.** All 21 pairs in P20's files name a ruled P20 line (`d3_pair_check.py`). Across the ledger, 1,254 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. The model's hashes are unchanged (elements 4b4e277f…, arrows e0ba1b0b…).
- **Questions.** None is open.

## D3a-22: P17, coalitions

P17 is a standing process of T4-018 (Meta-organization), and it is the theme's only element. Its statement reads: 'Rooms join other rooms in coalitions: they meet in shared chats, form alliances, gather kindred rooms in a hub, tally kindred rooms' works and make joint marks.' Its range runs from two rooms agreeing to defend each other to a council of kindred rooms holding a stretch of the canvas together. A19 (P05 to P17, thin) runs into it, and F-008 holds A19's coalition order. G27 was written before any line was read, and its readings are written under it (above). All 808 lines, in 702 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_field_entry_counts.py`, `d3_family_counts.py`, `d3_pair_check.py` and `d3_reason_phrases.py` (new at this leg).

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 351 | 320 | 0 | 0 | 0 | 8 | 23 |
| absent (275 `unobserved`, 50 `not-testable`) | 325 | 0 | 0 | 0 | 269 | 4 | 52 |
| restrict | 70 | 25 | 4 | 0 | 39 | 1 | 1 |
| add-condition | 27 | 13 | 7 | 0 | 7 | 0 | 0 |
| add-step | 25 | 16 | 0 | 0 | 8 | 1 | 0 |
| link | 10 | 7 | 3 | 0 | 0 | 0 | 0 |
| all | 808 | 381 | 14 | 0 | 323 | 14 | 76 |

P17 is shown in 383 of the 705 rooms, and in 315 of them an instantiate line is accepted. 319 rooms have P17 lines and none shows it. T4-018's prose counts 146 rooms. No absent line was `observed-absent` or `not-needed`. P17 is not stated as universal, so no absent line is a correction.

**What the specifications show.** These are rough counts, by phrase in the reason:
- P17 as stated (alliances acted on, councils and alliance chats, hubs, joint marks): 180 lines;
- P17's lower range (two rooms defending or keeping each other's works, an alliance with no stated terms, a proposal): 145 lines;
- other statements named, 28: A19 8 (rooms enter the canvas through another room's build; a coalition offered before upkeep, the exception its bound names; allies defend each other's works), P08 8, P05 3 (an agreed joint design repaired away until the keepers are told), A16 2, P04 2, P09 2, C02 1, P13 1 and P16 1.

**Restrict lines: no correction.** Most restrict lines say that a proposal, an invitation or a chat link is not a formed coalition. G27 counts the stated proposal, and the restriction notes what the record lacks, so 39 are evidence limits. 25 are specifications. P17's range starts at two rooms agreeing. Its statement names shared chats and names the room as the one that joins. A comparison of kindred works joins no one. One restriction was rejected: armok-026's 'fusion of your axe and our God' is a joint mark.

**The 14 elaborations, three families.** All are paired, and no standing statement or arrow holds them:

| family | lines | rooms | ops | ids |
|---|---|---|---|---|
| members not held by a tie made in the room's name: they deny it, refuse it or deface an ally's work (P21's form, a tentative entry; carried to P21's group) | 6 | 6 | restrict 4, add-condition 2 | EraseThePlace-022, habs-034, osu-034, turkey-032, halo-042, snsd-031 |
| a tie from before the canvas bars an alliance: division and conference rivals, a nation's history (C02 holds the rival named in an attack turn, not a refused alliance) | 5 | 5 | add-condition 4, link 1 | TheB1G-052, uofmn-055, eagles-023, palestine-056, poland-055 |
| a colour faith born on the canvas decides allies and ends alliances | 3 | 2 | link 2, add-condition 1 | PurplePixels-064, PurplePixels-019, TheGreatGreenBox-028 |

**What the 76 rejects show.**
- **Instantiate, 23.** The concepts show a deal, help, a guest's tie or another room's coalition, and no partnership of the room's own:
  - non-aggression 'alliances' and truces (P08), 6: GabrielDropout-024, cloud9-018, indieheads-025, starvstheforcesofevil-030, traaaaaaannnnnnnnnns-021, taiwan-021;
  - space for help, or help for restraint (P08 and P16), 4: cowchop-014, rush-032, tampabaylightning-017, toolband-029;
  - a guest on a host's mark, with no alliance named (P19's form), 3: chess-017, clubpenguin-018, hatsune-016;
  - one-way help or protection, or a call that names no partner (P16), 4: evex-013, placetardis-024, stevenuniverse-034, purplecorner-023;
  - visitors' offers that no member takes up, 3: flashtv-016, greenbaypackers-034, lakers-036;
  - another room's coalition, which the room's members helped, 2: hearthstone-034 and araragi-010 (re-ruled);
  - a pact proposed after the close for later events (P13's ground), 1: ukplace-028.
- **Restrict, 1:** armok-026.
- **Absent, 52.** The concepts show P17, so the claim of absence fails:
  - members' proposals of an alliance, a pact or joint defence with a named room, 35, among them ManningPlace-033, NieR-036, Peru-031, formula1-021, indonesia-014, kcroyals-035, seahawks-031, starbound-029, trees-034 and gravityfalls-032;
  - hubs and chats of kindred rooms used, 7: NovaScotia-017, alberta-033, asktransgender-020, ik_ihe-027, rojava-026, sabres-021, ubreddit-025;
  - joint work or joint upkeep with another room, 5: anarchism-028, furry_irl-029, globaloffensive-033, portal-030, rwby-032;
  - defence or watching given both ways, 3: lifeisstrange-030, sakuragakuin-031, vegan-017;
  - an alliance named and acted on, 1: k_on-025;
  - a visitor's offer taken up by a member, 1: ufl-036.

**Absent lines.** 269 are evidence limits: calls and requests for help, visitors' offers and reports, truces and border deals, one-way help, the room's own chat, and 'allies' with no partner named. I read the quotes of every reject and of about 30 other candidates before ruling. A guard pattern listed 21 limits that mention alliances for a second look, and one of them moved to reject (gravityfalls-032).

**Particulars, 14.**
- By G6, 13: instantiate 8 (Moondye7-018 'placestart', chibears-030 'chicago', cirkeltrek-029 'czech', dwarffortress-023 'minecraft', flyers-013 'pakistan', minecraft-024 'minecraft', quebec-030 'canada', snsd-030 'placehearts'), restrict 1 (dankmemes-025 'pinkunion') and absent 4 (Villanova-031 'osu', colorado-029 'placehearts', magictcg-025 'italy', spacex-024 'spacex').
- One room, with no statement holding the form and no second room's elaboration, 1: yumenikki-020, a member learning a chat tool to reach another room's channel.

**No correction, so no §2 re-examination.** No restrict, add-condition or link line was accepted as a correction. P17 stands as served, no move was made, and F-008 is not re-examined.

**Repairs (G7).** Lines in repaired rooms were 0.907 accepted (431 lines), and in unrepaired rooms 0.867 (377 lines). The unrepaired rooms hold more rejects (43 against 33). No ruling rests on the difference.

**Carried to later groups.**
- **Members not held by the room's tie** (6 lines) go to P21's group, beside A21 (tentative).
- **Ties from before the canvas that bar alliances** (5 lines) go beside C02, which names the rival only in attack turns. The clustering may read C02 more widely: such a tie decides both whom a room fights and whom it will not join.
- **Colour faiths** (3 lines in 2 rooms) go beside the contrary room, thebluecorner. A faith born on the canvas decides allies as well as rivals.
- **A19's order.** Four add-step lines and one link line show rooms entering through another room's build, or offering a coalition while building, before upkeep. A19's bound already names both. They support reading A19 as one route into P17, not the only one.
- **P17's count.** P17 is shown in 383 rooms, against the 146 that T4-018's prose counts. 35 of the 52 absent rejects are members' proposals, which G27 counts. A narrower reading, formed coalitions only, would move those lines and part of the 145 lower-range lines to evidence limits.
- **Host and guest ties with an alliance named** (farmcarrots-019, furry-033, rocketbeans-021, swordartonline-013, metalcore-027) go to P19's group.
- **The one-room particular** stays in its local model.

**Disclosed limits and slips.**
- **Draws.** Four seeded draws covered the instantiate lines, at verb offsets 378, 478, 578 and 678 (the last over 51 lines), ten lines each. The first run at 478 took `--limit 10`, so it held the packet's first ten lines, not a draw. I kept that file and drew again over 100 lines (`d3_draw_P17_478-100.txt`). Every drawn line's labels agreed with its quotes, so each packet was ruled from its labels, read whole.
- **Three re-rulings, appended.**
  - metalcore-027, reject to accept: the reading I logged at instantiate line 150, that every r/placestart tie is P19's, contradicted the alliance reading, and I withdrew it.
  - araragi-010, accept to reject: araragi-009's quotes show that the makers and their team-up came from r/anime_irl, as at hearthstone-034.
  - PurplePixels-019, particular to elaboration: its quotes show that the refusal follows from the convention's ban on Purple's war on blue, not from the venue its code label named.
- **A superseded file.** `P17-absent.jsonl` was built before gravityfalls-032 moved to reject. It was never written to the ledger; `P17-absent-v2.jsonl` was.
- **The family counter** reads PurplePixels-019's first reason, so it misses that line. I counted the colour-faith family by hand.
- **A shell variable.** One counting command set a shell variable, which the head's rules forbid. It ran, and its output was a count only. I used full paths after it.

### Close-check, D3a-22

`validate.py D3` reports 19,605 of 42,243 ledger lines ruled: the 18,797 before this leg and P17's 808. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 20,320 lines: 808 first rulings and 3 re-rulings from this leg. That makes 715 appended re-rulings in all.
- **Pairs.** All 14 pairs in P17's files name a ruled P17 line (`d3_pair_check.py`). Across the ledger, 1,268 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. The model's hashes are unchanged (elements 4b4e277f…, arrows e0ba1b0b…).
- **Questions.** None is open.

## D3a-23: P15, the bare answer

P15 is a standing process placed in the form-pass tier FP-01, with no dimension, so its lines are carried through no third-order tier. Its statement reads: 'A member answers a call or proposal in one line that joins, assents, reports a part done or thanks, and the line asks for nothing back.' Its range runs from 'On it.' to 'Did my part.' A12 (P01 to P15, never counted as an order) runs into it, grounded on F-023. G28 was written before any line was read, and its readings are written under it (above). All 789 lines, in 705 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_field_entry_counts.py`, `d3_pair_check.py` and `d3_reason_phrases.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 646 | 594 | 0 | 0 | 0 | 3 | 49 |
| absent (64 `unobserved`, 6 `not-testable`, 9 `observed-absent`) | 79 | 9 | 0 | 0 | 67 | 1 | 2 |
| restrict | 38 | 34 | 0 | 0 | 1 | 1 | 2 |
| add-condition | 6 | 5 | 0 | 0 | 1 | 0 | 0 |
| add-step | 9 | 9 | 0 | 0 | 0 | 0 | 0 |
| link | 11 | 11 | 0 | 0 | 0 | 0 | 0 |
| all | 789 | 662 | 0 | 0 | 69 | 5 | 53 |

P15 is shown by an accepted instantiate line in 579 of the 705 rooms. The helper counts 598 rooms as showing it, but that count also takes restrict specifications, which here mostly state where P15 stops. Every room has a P15 line. The nine `observed-absent` lines are specifications. Eight show calls or proposals met only by confusion, correction, refusal, jokes or praise, and one shows no call at all, so no answer was needed. P15 is not stated as universal, so no absent line is a correction.

**What the specifications show.** These are rough counts, by phrase in the reason:
- P15 as stated (a join, assent, own part or thanks in answer to a call or proposal): 530 lines;
- P15's lower range or lower end (a bare 'on it', a join to the thread's call, thanks for something given): 60 lines; its upper end ('did my part'): 7 lines;
- restrict and add-condition lines whose condition P15's statement holds: 35;
- other statements named, 14: A02 6 (a visible start brings the join), A12 4, and C01, K02, P03 and P11 once each;
- lines with another element beside P15 (P08's terms, P09's attack, P16's help, P14's scripts, P13's carrying on): 79.

**Restrict lines: no correction.** 34 restrict lines say that praise, cheers, thanks or answers to non-calls are not P15, or that a reply asking something back is not bare. P15's statement says both, so these are specifications. One is an evidence limit (swordartonline-007, an uncoded remainder). Two were rejected because they bar what G28 counts: assent to a deal (destiny-020) and a note beside a join (witcher-004).

**No elaborations.** Six lines looked like a family of joins that wait on a visible start, an outline or a template: ProfessorLayton-017, indieheads-004, torontoraptors-008, armok-067, dofus-052 and guatemala-006. A02's mechanism holds them: 'A member who proposes or begins a mark gives the room something to answer.' They are specifications naming A02.

**What the 53 rejects show.**
- **Instantiate, 49.**
  - Praise, credit, cheers, a claim of one's part, or thanks for a finished work or for help already given, answering no call (P11), 25: AceOfAngels8-012, Cornwall-011, ElderScrolls-039, EraseThePlace-002, KState-011, ReBoot-015, SydneyFC-037, anarcho_capitalism-007, bobross-016, bulgaria-013, catalunya-005, colorado-003, counting-041, eder-006, esperanto-008, feedthebeast-003, freedomplanet-004, hunterxhunter-008, natsume-002, placeportalpattern-004, sakuragakuin-049, scp-018, ssbpm-003, transgender-007, yuyuyu-023.
  - Closing thanks or welcome from the caller, the offerer or an organizer, 6: ElSalvador-004, TheB1G-016, TransFlagPlace-008, carletonu-009, h3h3productions-065, terraria-036.
  - State reports that are not the member's own part (P03), 6: Madeon-007, daftpunk-010, oman-009, shitredditsays-007, startrek-003, zelda-003.
  - Thanks to another room for help or a greeting (P16), 3: apocalypserising-015, iastate-005, thailand-003.
  - Replies that ask something back or join beside a doubt, 3: CSUFoCo-007, parabola-011, bigbang-004.
  - Other, 6: thanks for an explanation or a routine update (cowchop-024, linux-006, livecounting-052), approval of an announcement (thetreesnetwork-009), a proposer committing to its own proposal (buffalowizards-003), and a war cry answering a report (orderofthebluecorner-055, P18).
- **Restrict, 2:** destiny-020 and witcher-004.
- **Absent, 2.** Each line's concepts show P15, so the claim of absence fails: a member thanking a visitor's offer (landry-015), and 'Checking in' with the member's part (megaman-013).

**Absent lines.** 67 are evidence limits: calls with no recorded answer, praise and greetings, questions, conditional or qualified acceptances, joins beside a doubt (wales-018, worldpowers-004), and unsolicited offers. I read the quotes of 11 candidates. A guard pattern listed 32 limits for a second look, and none moved.

**Particulars, 5.** All by G6: chess-015 ('chess'), malta-003 ('france'), osugame-003 ('ohio'), counting-042 ('counting') and vim-041 ('linux').

**No correction, so no §2 re-examination.** No restrict, add-condition or link line was accepted as a correction. P15 stands as served, no move was made, and F-023 is not re-examined.

**Repairs (G7).** Lines in repaired rooms were 0.918 accepted (414 lines), and in unrepaired rooms 0.936 (375 lines). The repaired rooms hold more rejects (31 against 22). No ruling rests on the difference.

**Carried to later groups.**
- **Where P15 stops.** The rejects mark P15's edge with P11 (credit and cheers for a made work), P03 (state reports) and P16 (thanks for help). The clustering may read the call and its answer as running from P01 through P15 to P11's thanks at the close.
- **Joins that wait on a start.** Six lines show members joining once a start, an outline or a template is visible, as A02's mechanism states. They go beside A02 and A12 for the order tests.
- **The count.** P15 is shown in 579 rooms, far beyond F-023's sample of 80. A12's bound still holds: the form is read on written, coded replies only, and acceptance by placing leaves no line.

**Disclosed limits and slips.**
- **Draws.** Seven seeded draws covered the instantiate lines, at verb offsets 95, 195, 295, 395, 495, 595 and 695 (the last over 46 lines). The first draw, at 94, held 99 instantiate lines, which showed that the lines start at 95. I kept that file, used its ten lines as read, and drew again at 95. Every drawn line's labels agreed with its quotes, so each packet was ruled from its labels, read whole.
- **A slow helper.** `d3_verb_ids.py` ran past the time limit and went to the background. I stopped it before going on and took the op totals from the packet helper.
- **A refused command.** At the opening, a `cut -c` after a model read was refused by the permission check. I used scripts after it.
- **The helper's room count.** `d3_field_entry_counts.py` counts restrict specifications as showing the element. For P15 they mostly state where P15 stops, so I report 579 rooms from instantiate lines. The same count gave P17's 383 rooms at D3a-22, which included 29 rooms by restrict lines.

### Close-check, D3a-23

`validate.py D3` reports 20,394 of 42,243 ledger lines ruled: the 19,605 before this leg and P15's 789. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 21,109 lines: 789 first rulings from this leg and no re-ruling. Appended re-rulings stay at 715.
- **Pairs.** P15's files hold no pairs (`d3_pair_check.py`). Across the ledger, 1,268 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. The model's hashes are unchanged (elements 4b4e277f…, arrows e0ba1b0b…).
- **Questions.** None is open.

## D3a-24: C01, decided order

C01 is a standing claim, placed in T4-011 ('Decided order') and the form-pass tier FP-08, in dimension D02. Its statement reads: 'Most rooms worked on their marks without deciding how they were organized: a decided element of order (a leader, a vote, an oath, a sanction, a division of the work) is coded in 46 of 705 rooms (F-006).' Its range runs from rooms that say they wing it to colour factions holding elections. No arrow touches it. G29 was written before any line was read, and its readings are written under it (above). All 777 lines, in 705 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_field_entry_counts.py`, `d3_c01_sides.py`, `d3_pair_check.py` and `d3_reason_phrases.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 108 | 80 | 0 | 0 | 0 | 0 | 28 |
| absent (465 `not-testable`, 19 `unobserved`) | 484 | 0 | 0 | 0 | 421 | 1 | 62 |
| restrict | 122 | 94 | 0 | 0 | 14 | 1 | 13 |
| add-condition | 39 | 32 | 3 | 0 | 2 | 0 | 2 |
| add-step | 23 | 15 | 5 | 0 | 0 | 1 | 2 |
| link | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| all | 777 | 222 | 8 | 0 | 437 | 3 | 107 |

**Where C01 is shown.** Accepted instantiate lines show it in 76 rooms. In 62 more lines, all absent, the concepts show it, so the claim of absence was rejected; two rooms hold both. C01 is shown in 136 rooms in all (`d3_c01_sides.py`). By the reasons' wording, 119 of these rooms hold a decided element, and 21 hold a line naming the lower end (17 hold only the lower end). The helper counts 249 rooms, but it also takes restrict and add specifications, which mostly state conditions C01 never claimed. No absent line is `observed-absent` or `not-needed`, so no absent line is a specification of the majority clause. The 421 limits are rooms whose record, as read, shows neither side.

**The count against F-006.** The return shows a decided element in about 119 rooms, against the 46 coded at C3. The majority clause still holds: the other 586 rooms show no decided element in the return. F-006's count stands as a count of coded rooms. Its bound already says that votes and divisions of the work appear in rooms not placed on the theme. The difference is a fact to carry to the verdicts leg and to D3c's re-read. No ruling is revisited because of it.

**What the specifications show.** These are rough counts, by phrase in the reason:
- C01's minority clause is named 29 times, the lower end 15 and the majority clause 5;
- other statements named: P20 13 (the host's line, apart from order over the canvas work), K01 5 (mock ranks, bans and votes in play), P17 5 (a tie decided by vote stays P17's), A11 4 and P04 4 (templates and plans), F-006's bound 4, R01 3, P08 3, P02, P12 and P13 twice each, and P14, P15, A01 and P05 once each.

**Restrict lines: no correction.** 94 restrict lines are specifications. Most place the room in C01's minority with a decided element, or state a limit that C01 never claimed (obedience, binding every placer, an appointment, effective command). 14 are evidence limits: the record cannot show what unseen chats decided. 13 were rejected:
- they count as decided order what G29 does not: GranColombia-010 (a venue demanded), bindingofisaac-041 (a member's own part and an open call), catalunya-012 (one member's consensus norm), dbz-008 (a vote suggested), portugal-022 (a chat decision with no procedure);
- they deny what G29 counts: littlewitchacademia-014 (commanders and diplomats named), monstercat-011 (T3-125's own exemplar, 'Nope, just refresh and click'), russia-009 ('there is zero coordination at this stage', narrowed to one proposal);
- they rest on own parts, restraint or an allocation no concept shows: terraria-008, timbers-028, wildhockey-009, wine-012;
- it does not bear on C01: funhaus-052 (whether there is a Discord).

**Elaborations, 8, in two paired families** (counted by hand, since the family counter reads first reasons):
- **Decided order reaching only the members inside its venue or faction** (add-condition, 3 rooms): ainbowroad-010 (decisions do not reach the thread's repairers), rocketleague-012 ('less than 20 people ... organized ... rest of that were randoms') and thebluecorner-010 (the faction's order, not everyone placing blue). No standing statement holds where decided order reaches inside a room.
- **Where or how the room decides, contested or questioned** (add-step, 5 rooms): GreenCorner-013 (elections during an attack), germany-042 (a closed chat against the thread), romania-017 (a rule tying changes to Discord), fivenightsatfreddys-015 (the sub against its own Discord) and pathofexile-016 (the project leaders' own chat).

The 8 pairs name ruled C01 lines, and none is left without its partner.

**What the 107 rejects show.**
- **Instantiate, 28.** The concepts show neither side by G29:
  - self-assignment and members' own parts, 6: drawhelix-014, hentai-007, redpandas-011, smite-011, yogscast-012, fxKorea-011;
  - orders of work and plans, 5: calgaryflames-013, floridagators-008, portal-014, redvsblue-009, transformers-007;
  - proposals not taken up, or offered as questions, 4: onepunchman-015, homestuck-019, scotland-008, GrowTheTree-009;
  - calls and self-started work, 6: 4chan-014, CKCrusaders-007, DiamondClub-008, Dominican-014, egypt-015, TreePlace-006;
  - talk of the design, 3: Thegreatblackhole-011, swordartonline-008, morrowind-008;
  - other, 4: an official plan with no deciders (denmark-011), the scripts' keeper leading by acting (wallstreetbets-019), a split agreed with a neighbour (hoodr-008), and a designer's draft left for anyone (survivor-022).
- **Restrict, 13** (above). **Add-condition, 2:** dwarffortress-014 (chat decisions with no procedure) and ethereum-009 (a proposed plan). **Add-step, 2:** swordartonline-053 (a choice left to anyone) and vermont-013 (self-assignment).
- **Absent, 62.** The concepts show C01, so the claim of absence fails:
  - polls or votes opened or taken, 13: AMD-013, GuardiansOfDatBoi-010, chile-029, clubpenguin-027, czech-020, drugs-014, fireemblem-008, halo-032, harrypotter-013, patriots-013, radiohead-013, sheffield-033, taiwan-013;
  - a decision reached by agreement or consensus, 10: Homura-012, animalcrossing-011, armenia-040, enterthegungeon-014, germany-041, giantbomb-017, kilian-011, neopets-031, starbound-013, theexpanse-016;
  - named teams, shifts or splits of members, 8: AmericanFlaginPlace-018, buffalobills-017, eagles-012, forsen-013, heroesofthestorm-026, italy-011, orderofthebluecorner-008, rickandmorty-024;
  - offices given or named by title, 6: falcons-015, fullcommunism-029, lovelive-018, paragon-018, placestart-014, rocketbeans-010;
  - officers deciding by office, 4: PinkUnion-010, berkeley-023, strangerthings-010, twitchplayspokemon-014;
  - rules, approvals, entry rules and sanctions, 7: asktransgender-011, greenbaypackers-014, ockytop-027, placecanada-021, placeportalpattern-036, roosterteeth-015, stlouis-014;
  - handovers and assignments, 3: satania-011, suomi-027, texas-009;
  - the lower end, 11: PinkVomitMonster-033, ScottPilgrim-012, calvinandhobbes-010, cowchop-031, liquicity-007, rwby-013, slovenia-009, ss13-018, stardustcrusaders-010, thenetherlands-010, unitedkingdom-009.

**Absent lines.** The 421 limits are `not-testable` or `unobserved` lines whose concepts show calls, plans, templates, chats, reports, self-started work, credit for organizing, or decisions reported from unseen chats. A guard pattern listed 178 limits for a second look, and none moved after four more quotes.

**Particulars, 3.** hearthstone-015 (G6, 'spongebob'), maryland-009 (G6, 'maryland'), and turkey-012 (G4a: a vote moved to private messages to shield it from a rival's raid, met in no second room).

**No correction, so no §2 re-examination.** No restrict, add-condition or add-step line was accepted as a correction. C01 stands as served, no move was made, and F-006 is not re-examined.

**Repairs (G7).** Lines in repaired rooms were 0.853 accepted (422 lines), and in unrepaired rooms 0.865 (355 lines). No ruling rests on the difference.

**Carried to later groups.**
- **The count.** A decided element is shown in about 119 rooms, against the 46 coded (F-006). It goes to the verdicts leg and D3c's re-read.
- **The two families.** Decided order's reach goes beside A19's bound (coalitions cannot bind every placer). Contests over where the room decides go beside the chats item (T4-010).
- **C01's edges.** P20 (the host's line), K01 (play) and P17 (ties decided by vote) are named 23 times in the specifications.

**Disclosed limits and slips.**
- **Draws.** Two seeded draws covered the instantiate lines, at verb offsets 547 (100 lines) and 647 (8 lines, all drawn). The first draw, at 546, held 99 instantiate lines, which showed that the lines start at 547. I kept that file unread and drew again at 547. Every drawn how agreed with its quotes, so each packet was ruled from its labels, read whole, with quotes read beside them for lines whose side the labels left open.
- **Quotes read.** Instantiate 61, restrict 66, add and link 17, absent 129. Two diary lines carry slips in these counts: the first restrict packet's line says 51 (it was 50), and the absent line says 117 (it was 129).
- **The helper's room count.** `d3_field_entry_counts.py` counts specifications of every op as showing the element, so I report 136 rooms from `d3_c01_sides.py`.
- **Ruling by wording.** The split of the 136 rooms by side reads the reasons' wording ('lower end'), so it is approximate.

### Close-check, D3a-24

`validate.py D3` reports 21,171 of 42,243 ledger lines ruled: the 20,394 before this leg and C01's 777. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 21,886 lines: 777 first rulings from this leg and no re-ruling. Appended re-rulings stay at 715.
- **Pairs.** C01's files hold 8 pairs, none left without its partner (`d3_pair_check.py`). Across the ledger, 1,276 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. The model's hashes are unchanged (elements 4b4e277f…, arrows e0ba1b0b…).
- **Questions.** None is open.

## D3a-25: C02, the tie that names the rival

C02 is a standing claim, untested for order. It is placed in T4-020, T4-021, T4-022 and T4-004, in dimensions D08 and D05. Its statement reads: 'In some rooms, a tie the room had before the canvas (a league or school rivalry, a nation's history, an ideology, lore) names the rival in the same turn that calls for or carries out the attack.' Its range runs from a team's colours turned on a league rival's logo to a war from the nation's history named as the reason to cover a neighbour's flag. F-013 holds it: 10 turns in 7 rooms, with colour factions as a boundary. No arrow touches it. G30 was written before any line was read, and its readings are written under it (above). All 715 lines, in 705 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_shown_rooms.py`, `d3_field_entry_counts.py`, `d3_pair_check.py` and `d3_reason_phrases.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 124 | 87 | 0 | 0 | 0 | 11 | 26 |
| absent (341 `unobserved`, 196 `not-testable`, 2 `observed-absent`, 1 `not-needed`) | 540 | 3 | 0 | 0 | 494 | 18 | 25 |
| restrict | 47 | 46 | 0 | 0 | 1 | 0 | 0 |
| add-condition | 4 | 3 | 0 | 0 | 0 | 1 | 0 |
| all | 715 | 139 | 0 | 0 | 495 | 30 | 51 |

**Where C02 is shown.** Accepted instantiate lines show it in 87 rooms. In 25 more rooms, absent lines were rejected because the concepts show it. No room holds both, so C02 is shown in 112 rooms (`d3_shown_rooms.py`). The helper counts 152 rooms, but it also takes restrict and add specifications, which mostly state limits that C02 never claimed. F-013 read 10 turns in 7 rooms. C02 still speaks of some rooms, and it claims no share and no order. The count is a floor: 29 lines marked NONPORTABLE became particulars by G6, and their markers often name the rival or the target ('lakers', 'france', 'osu', 'quebec').

**What the ties are.** These are rough counts by phrase in the specifications' reasons, and one reason can hold several: a league, division or conference 21, a nation's history 20, a school 11, a creed or ideology 9, and a game 7.

**Restrict lines: no correction.** 46 of the 47 restrict lines are specifications. Each states a limit that C02 never claimed (the tie choosing the target, a cause, execution, a whole room's mandate, every clash), or a case that G30 already leaves out (lore laid on an opponent met on the canvas, defence and blame, taunts and lettering, a tie in another turn, borrowed labels, the room's own work). C02's untested status is named 7 times in these reasons, and F-013's `refuted_by` 7 times. One line is an evidence limit: the_pack-041, whose meme grievance with me_irl the record does not date.

**No elaboration.** One add-condition line is a particular: bostonbruins-031 ('Nah, don't do it. Hockey is family'). A wider old tie holds back an attack and brings repair. No standing statement holds it, and no second C02 line meets it. It goes beside P07's family 'ties to the makers', with overwatch-054's Blizzard kinship and gatech-024's call to Georgia subs to set rivalries aside.

**What the 51 rejects show.**
- **Instantiate, 26.**
  - Lore or history laid on a canvas neighbour or attacker (F-013's `refuted_by`), 9: AMD-036, AmericanFlaginPlace-047, FaroeIslands-024, factorio-038, italy-022, pokemon-021, satania-028, skyrim-028, smite-042.
  - No tie of the room's own, 6: one member's politics (furry-043, mylittlepony-043), a visitor's tie (chicubs-041, greece-043, osugame-038), and a game taste claimed for a national room (sweden-024).
  - A national target with no tie in the words, 1: india-022.
  - No attack, 10: a joke wish (detroitredwings-021), a contest named (australia-027), a joke with no target (polska-040), taunts in lettering (predators-037, minnesotavikings-027, uoft-043), help to another room (neu-043), defence (onepunchman-042), and changes to the room's own work (spain-029, starvstheforcesofevil-039).
- **Absent, 25.** The concepts show C02, so the claim of absence fails. The ties are rival schools or conferences (TheB1G-029, notredame-028, texastech-038, ubc-024, uwaterloo-037), rival games, brands, channels or fandoms (OnePiece-027, achievement_hunter-038, bitcoin-043, cloud9-023, elitedangerous-033, eve-026, leagueoflegends-025, linux-047, morrowind-038, muse-024, nintendo-029, startrek-036), history or faith (catholicism-042, crusaderkings-036, mexico-028, sakartvelo-031, theitalyplace-032, turkey-045, ukraine-028), and an old enmity of the board's (4chan-047).

**Absent lines.** The 494 evidence limits are `unobserved` or `not-testable` lines. Their concepts show attacks on targets the canvas made, defence against old rivals, taunts and lettering, lore laid on neighbours, colour factions' creeds, and national calls whose words carry no tie. I read 60 quotes for candidates. A guard pattern listed 114 limits for a second look, and none moved. The three evidenced lines are specifications (columbia-044 and lost-023, `observed-absent`; paladins-050, `not-needed`).

**Particulars, 30.** 29 are by G6 (NONPORTABLE), 11 of them instantiate lines. One is by G4a (bostonbruins-031).

**No correction, so no §2 re-examination.** C02 stands as served, untested for order. No move was made, and F-013 is not re-examined.

**Repairs (G7).** Lines in repaired rooms were 0.904 accepted (386 lines), and in unrepaired rooms 0.866 (329 lines). No ruling rests on the difference.

**Every standing element is now ruled whole.** `d3_ruled_by_element.py` lists all 24 standing elements as ruled. The candidates (K04, P06, P19, K03, R02), the tentative P21, the arrows, the dimension lines and the `propose` lines remain unruled.

**Carried to later groups.**
- **The count.** C02 is shown in 112 rooms, against F-013's 7. The 11 instantiate particulars would add rooms. The count goes to the verdicts leg and D3c's re-read.
- **Kin ties.** Ties that hold back attacks (bostonbruins, overwatch, gatech) go beside P07's 'ties to the makers'.
- **C02's edges.** Colour factions (F-013's bound; K04, a candidate) and visitors' ties stay outside it. The order test it lacks stays open.

**Disclosed limits and slips.**
- **Draws.** G30 named verb offset 544. The first draw there held 99 instantiate lines, which showed that the lines start at 545. I kept `d3_draw_C02_544.txt` and `d3_draw_C02_644.txt` unread and drew again at 545 (100 lines) and 645 (24 lines). Every drawn how agreed with its quotes, so each packet was ruled from its labels, read whole, with quotes read for lines whose tie or attack the labels left open.
- **A refused command.** At the opening, a `cut -c` after the quote helper was refused by the permission check. I ran the command again without it.
- **Quotes read.** C02's own evidence 7, before G30; instantiate 45; restrict and add-condition 5; absent 60.
- **The helper's room count.** `d3_field_entry_counts.py` counts specifications of every op as showing the element, so I report 112 rooms from `d3_shown_rooms.py`.

### Close-check, D3a-25

`validate.py D3` reports 21,886 of 42,243 ledger lines ruled: the 21,171 before this leg and C02's 715. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 22,601 lines: 715 first rulings from this leg and no re-ruling. Appended re-rulings stay at 715.
- **Pairs.** C02's files hold no pairs (`d3_pair_check.py`). Across the ledger, 1,276 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 139 lines, elements 30, arrows 21, findings 37 and tier history 561, all unchanged. The model's hashes are unchanged (elements 4b4e277f…, arrows e0ba1b0b…).
- **Questions.** None is open.

## D3a-26: P21, who may commit the room

P21 is the field's tentative entry from C4a. It is placed in T3-126 under T4-016 (Negotiated order), in dimension D04. Its statement read: 'Members dispute who may commit the room to an agreement with other rooms: they say that one member's agreement does not bind every placer, deny that a treaty speaks for them, or ask another group for a leader to deal with.' At C4a it rested on one room's two concepts (flyers:c0166, flyers:c0169) and on seven field comments. G31 was written before any line was read, and its readings are written under it (above). All 740 lines, in 705 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_shown_rooms.py`, `d3_field_entry_counts.py`, `d3_pair_check.py` and `d3_reason_phrases.py`.

| op | lines | specification | elaboration (paired) | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 80 | 65 | 0 | 0 | 0 | 1 | 14 |
| absent (534 `unobserved`, 47 `not-testable`, 1 `observed-absent`) | 582 | 1 | 0 | 0 | 484 | 0 | 97 |
| restrict | 66 | 65 | 0 | 0 | 0 | 1 | 0 |
| add-condition | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| add-step | 6 | 4 | 0 | 0 | 0 | 0 | 2 |
| link | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| all | 740 | 141 | 0 | 0 | 484 | 2 | 113 |

**Where P21 is shown.** Accepted instantiate lines show it in 65 rooms. In 97 more rooms, absent lines were rejected because the concepts show it. No room holds both, so P21 is shown in 162 rooms (`d3_shown_rooms.py`). With the restrict lines (64 rooms) and the add and link lines (10) that its statement holds, 211 rooms have a line that shows it (`d3_field_entry_counts.py`). Unlike C02's, P21's restrict lines mostly name P21's own first form, the limit, so here the larger count is a fair one. C4a coded it in one room.

**What the rooms show.** These are rough counts by phrase in the reasons of the 97 rejected absent lines, and one reason can hold several:
- the room's own agreement or decision has not reached every placer, 33 ('there might be some who haven't gotten the memo', ManningPlace; 'it will take some time for everyone to get the news', poland);
- a member states the limit of another room's agreement, 18 ('Some of the people there just don't want to honor it', TheHulk; 'not the rouge ones', stardewvalley);
- a member disclaims or hedges their standing to commit the room, 16 ('I can't speak for the group', lsu; 'I might be wrong but I think I speak for the community', factorio; 'I'm no ambassador, but yeah, go ahead!', xcom);
- a member refuses an agreement already made in the room's name, 10 ('/r/osu has officially teamed up ...' answered 'No'; 'Forget past agreements', TheB1G);
- members ask or dispute who speaks for a group, 6 ('What community are you representing?', VelvetUnderground; 'Not really representative', furry_irl).

**Restrict lines: no correction.** 65 of the 66 restrict lines are specifications. Most say that a member's 'can't control everyone' is a compliance limit and not a dispute over who may represent the room. P21's first form and its range's lower end name that limit, so the statement holds them. spain-022 is a particular by G6. No restriction states a condition that P21 lacks and shows it failing without it.

**Adds and links.** 10 are specifications: the statement holds the conditions and steps, and it sets no order (the order of agreement and dispute is A21's question). europe-022 has P17 beside it, placetardis-029 is held by C01, and texas-054 has P14 beside it. 2 add-step lines are rejected: philippines-025 and thebluecorner-038 carry P21 to the room's own design and priorities, which would loosen it (rule 12). They belong to C01's family.

**What the 14 instantiate rejects show.** Visitors' own forms with no answer from the room's members, 10 (AMD-031, Summit1G-031, belgium-018, ftlgame-020, masseffect-029, pcmasterrace-039, romania-037, skyrim-021, survivor-024, ukraine-023). An agreement reported or assented to with no limit stated, 3 (ChronoTrigger-021, mls-029, monsterhunter-031). A dispute over the room's own design, 1 (darksouls-017). detroitredwings-018 is a particular by G6.

**Absent lines.** The labelers read P21 as an explicit dispute over a mandate. 97 of their 582 claims of absence fail because the rooms' own members state the limit, disclaim their standing, refuse an agreement made in the room's name, or ask whom a visitor speaks for (15, 16, 17, 19, 21 and 9 by packet of 100). The last packet's are tagpro-030, teslamotors-028, thesilphroad-020, trees-038, ufl-034, undertale-033, uva-030, warriors-018 and xcom-022. One line is an observed absence and a specification (ElSalvador-021: a deal revised, with no dispute). The other 484 are evidence limits. A guard listed 39 limits whose labels share words with P21 (control, rogue, speak, represent, memo, official, sanction, authority, diplomat, ambassador). Each was looked at again, and none moved.

**Move 175 (developing working hypotheses), P21.**
- P21 was ruled standing (rule 11, §4), and its statement's frame was rewritten. Two history lines record this: 140 (status) and 141 (statement). The snap is `D3-move-developing-175`.
- The frame now reads 'Members dispute, or state the limits of, who may commit the room to an agreement with other rooms'. The three forms, the range, the level and the tier are unchanged.
- Why: the old frame was narrower than the first form it listed. Readers took the frame. Most restrict lines and 97 absent claims turned on that gap. G31 already read P21 by its forms, so no room enters that the forms did not admit. This is not a loosening (rule 12). It brings the frame into line with the forms, as move 174 brought P22's range into line with its statement.
- No correction was accepted, so §2 was not triggered. No finding touches P21. The elements hash moved from 4b4e277f… to 47ff7a11…; the arrows are unchanged.

**The carried lines, read again under G4a.** G31's last clause asked for this once P21's status was ruled. `_analysis/d3_carried_lines.py` lists 48 lines in 47 ids, outside P21's files, whose reasons name P21. 41 were accepted elaborations carried as 'P21's form, a tentative entry that holds no line'. Each is re-ruled as a specification on P21's statement, with an appended line (`G4aB-P21.jsonl`):
- P07's group, 5: costa_rica-053, portugal-035, twice-028, FloydVsVoid-031, flyers-052;
- P08's group, 30 in 29 rooms: add-condition 19, add-step 10, and the restrict line norway-016;
- P17's group, 6: halo-042, snsd-031, EraseThePlace-022, habs-034, osu-034, turkey-032.

opticgaming-040 stays an elaboration paired with shitredditsays-042. Its content, a simple pattern that draws passers-by over others' work, is not P21's. Five lines of other elements name P21 only beside their own ruling, and they stay (telegram-021, GrowTheTree-021, finland-012, smashbros-059, ScottPilgrim-033). The helper leaves out evidence limits; with them it adds one, smashbros-063, a P18 absent line whose concepts show P21's form but not P18, which stays an evidence limit for P18. Accepted elaborations fall from 1,276 to 1,235. No remaining elaboration lost its partner.

**Repairs (G7).** Lines in repaired rooms were 0.828 accepted (396 lines), and in unrepaired rooms 0.863 (344 lines). No ruling rests on the difference.

**Carried to later groups.**
- **A21** stays tentative. It is P08 → P21: the first agreement comes before the first dispute. Its group tests that order in each room. P21 now stands, so under G4a it holds lines in A21's group and in the candidates' groups.
- **The re-check (§5).** P21's statement was rewritten, so the rooms whose verdicts or local accounts rest on P21 go to the re-check, with those resting on R01, P05 and P22.
- **P21's forms for the clustering at D4:** the limit (own or another room's), the disclaimer, the refusal of a made agreement, and the request for whom a group speaks.
- **Visitors' forms** show P21 in the visitors' rooms. The verdicts leg reads them from either record.

**Disclosed limits and slips.**
- **Draws.** The draw at verb offset 592 held 79 instantiate lines, so the lines start at 593. I kept `d3_draw_P21_592.txt` unread beyond its header and drew again at 593 (80 lines, 10 drawn). Every drawn how agreed with its quotes.
- **One ruling moved within the leg.** asexual-021 was first kept as a limit (a misattribution) and moved to reject when I read norway-023: both answer a visitor's request by saying that their room cannot commit the flag's placers. The diary records the move.
- **Refused commands.** At the opening, a heredoc was refused, so I wrote `d3_notes_mentions.py`. `mem.py contract --section 11` has no such section, since the ruling rules are in section 3. At the absent dry run, a `cut -c` after the batch helper was refused, and I ran the command again without it.
- **Quotes read.** Instantiate 26. Absent about 300 (20, 48, 64, 61, 53 and 40 by packet, with context quotes).
- **Counts by phrase** are over my own reasons, not over the members' words.

### Close-check, D3a-26

`validate.py D3` reports 22,626 of 42,243 ledger lines ruled: the 21,886 before this leg and P21's 740. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 23,382 lines: 740 first rulings and 41 re-rulings from this leg. Appended re-rulings rise from 715 to 756.
- **Pairs.** P21's files hold no pairs (`d3_pair_check.py`). Across the ledger, 1,235 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 141 lines (two from move 175), elements 30, arrows 21, findings 37 and tier history 561. The elements hash is 47ff7a11…; the arrows hash is unchanged (e0ba1b0b…).
- **Questions.** None is open.

## D3a-27: A21, the agreement before the dispute over who commits the room

A21 is the field's tentative arrow from C4a, P08 → P21, of kind order. Its connection read: 'in a room carrying both, the first agreement with another room (a border, a truce or a deal) comes before the first dispute over who may commit the room'. Its mechanism ended: 'and the other side asks who can speak for the group'. No proposition carried it, and the C5 figure did not draw it. G32 was written before any line was ruled, and its readings are written under it (above). All 708 lines, in 705 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a21_census_v2.py`, `c2_arrow_evidence.py` and `d3_pair_check.py`.

| op | lines | specification | correction (paired) | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|
| instantiate | 37 | 22 | 0 | 0 | 0 | 15 |
| absent (259 `unobserved`, 344 `not-testable`, 1 `observed-absent`, 1 `not-needed`) | 605 | 2 | 0 | 536 | 0 | 67 |
| restrict | 65 | 25 | 36 | 4 | 0 | 0 |
| add-step | 1 | 1 | 0 | 0 | 0 | 0 |
| all | 708 | 50 | 36 | 540 | 0 | 82 |

**What the rooms show (the census, `d3_a21_census_v2.py`).**
- **The order, 114 rooms.** An agreement comes first, and a P21 form answers it. Members state that the agreement does not bind every placer ('we did have an agreement. Some of the people there just don't want to honor it', TheHulk; 'someone didn't get the memo', necrodancer), or refuse it ('/r/osu has officially teamed up ...' answered 'No'; '#StopTheAnnexation' four hours after an alliance, counting).
- **At the making, 36 rooms (family F1).** The disclaimer or the request comes while another room's terms are proposed or accepted: 'You do not speak for Purple!' at h+28.06, before 'Deal' at h+29.66 (destiny); 'im just some random guy not the official mediator' two hours before the deal (jerma985); 'We have a deal! I can't speak for every member' (polska).
- **No agreement, 13 rooms (family F2).** A stated limit answers another room's appeal, complaint or accusation, with no agreement in force ('nobody is in charge of the free people drawing', turkey; contributors 'not under direct control', FloydVsVoid).
- One room, detroitredwings, shows both. So 162 rooms show an episode, and the order holds in 114 (0.704).

**The order test.** Its rules were logged before it ran. The model's first-concept test (`c2_arrow_evidence.py`, P08 without T3-126 against T3-126) finds only 11 rooms carrying both. The order holds in 10 (0.909). The null's mean is 0.738 and its 95th percentile 0.909, so the base rate is not beaten. T3-126 holds P21 in only 15 rooms, and P08's concepts come early in most rooms, so this test cannot decide A21. The census of the read lines carries the count, with no null; both are reported.

**Corrections met twice, and the re-examination (§2).** 36 restrict lines are accepted corrections, each paired within its family: F1 in a ring of 26, F2 in a ring of 10. They lift to T3-010 in 20 rooms. The written warrant is the alignment, not the count. The disclaimers of standing and the requests for someone who can speak for a group belong to the making of terms. The stated limit and the refusal answer an agreement already made, or, in 13 rooms, an appeal. The 25 restrict lines whose labelers said 'a compliance limit, not a mandate dispute' are specifications: P21's statement after move 175, and A21's own mechanism ('or that no one can bind every placer'), hold that condition.

**Move 176 (developing working hypotheses), A21.**
- A21 stands with a bound (rule 11, §4). Nine history lines record this (142 to 150), and the snap is `D3-move-developing-176`.
- The connection now reads 'the first dispute over, or stated limit of, who may commit the room', in line with P21. A permission is named beside the border, the truce and the deal.
- The mechanism drops 'and the other side asks who can speak for the group' and adds 'or refuse it'.
- The bound names the forms A21 orders (the stated limit and the refusal) and where it fails (36 rooms at the making, 13 with no agreement). The counts, the grounding, `negative_check` (counterexample), the counterexample response and `in_model` (true) are recorded.
- No finding touches A21. The arrows' hash moved from e0ba1b0b… to ff0b3963…; the elements are unchanged (47ff7a11…).

**What the instantiate rejects show (15).** The maker's own qualification at the making, 10 (AMD-032, Goodboye-066, Peru-029, canada-028, dbz-066, finland-056, polska-064, splatoon-055, theitalyplace-064, ukraine-045). An answer to an appeal or an offer with no agreement, 3 (detroitredwings-043, norge-030, texas-052). No P21 form, 1 (monsterhunter-032). A visitor's room's own forms, 1 (Summit1G-032).

**Absent lines.** 67 claims of absence fail because the concepts show the order (15, 11, 10, 9, 14 and 8 by packet). The two evidenced lines are specifications: ElSalvador-022 (a deal revised with no P21 form) and montenegro-052 (no deal reached). The other 536 are evidence limits. A guard listed 58 of them (refusals of proposals, visitors' forms, qualifications at the making). I had decided each while reading, and none moved.

**One P21 ruling re-ruled.** PinkUnion-029 (a P21 absent line) had been kept as a limit in D3a-26's first packet, before G31's refusal reading was stated. Its codes are those of PinkUnion-030 (an A21 reject here) and of PinkUnion-053, which was re-ruled as a P21 specification. An appended line makes it a reject: 'Mods, end our alliance with r/osugame'; 'it's servitude'. P21 is now shown in 163 rooms. Move 175's history line, which says 162, stays as written.

**Repairs (G7).** Lines in repaired rooms were 0.847 accepted (379 lines), and in unrepaired rooms 0.927 (329 lines). The rejects number 58 in repaired rooms and 24 in unrepaired ones, and 67 of the 82 are claims of absence that the concepts overturn. No ruling rests on the difference.

**Carried to later groups.**
- **The re-check (§5).** A21 was rewritten, so the rooms whose accounts rest on A21 go to the re-check, with those resting on R01, P05, P22 and P21.
- **The making of terms.** P08 holds the proposing and accepting, and P21 holds the disclaimer and the request; no arrow draws the two together in one step. The 36 rooms go to D4's clustering of P21's forms, and to the order tests beside A04 and A14.
- **Limits that answer appeals** (13 rooms) sit beside P07's restraint asked of the room's attackers.
- **The field's entries** are both ruled; none stays tentative.

**Disclosed limits and slips.**
- **Lines seen before G32.** While checking the packet's shape, I printed three instantiate lines (AMD-032, Goodboye-066, Peru-029) before G32 was written. None was ruled then.
- **A stray no-op in a command.** One command carried 'for_none=0;', a shell variable and a word beginning 'for_', against the rules on placeholders and shell variables. The permission check did not refuse it. Both writes in that command were checked (the diary line and the packet's header).
- **A superseded census.** The first census helper (`d3_a21_census.py`) sorted the corrections into families by phrase. It missed dbz-066 and moved two lines between the families. The first revision spec (`d3_revision_A21.json`), written from it, was never run. `d3_a21_census_v2.py` names the families by id, and `d3_revision_A21_v2.json` is the spec written.
- **The themes file** for the order test was first written without the statements the helper prints. `d3_a21_elements_v2.json` supersedes it.
- **Quotes read.** Restrict 22, with 4 more for one speaker's context; instantiate 11 beyond the draw's; absent 24 (9, 5, 5 and 5 in four packets). Many absent lines rest on quotes read for P21 at D3a-26.

### Close-check, D3a-27

`validate.py D3` reports 23,334 of 42,243 ledger lines ruled: the 22,626 before this leg and A21's 708. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 24,091 lines: 708 first rulings and 1 re-ruling from this leg. Appended re-rulings rise from 756 to 757.
- **Pairs.** All 36 pairs in A21's files name a ruled A21 line (`d3_pair_check.py`). Across the ledger, 1,235 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines (nine from move 176), elements 30, arrows 21, findings 37 and tier history 561. The arrows hash is ff0b3963…; the elements hash is unchanged (47ff7a11…).
- **Questions.** None is open.

## D3a-28: A02, the start before the call

A02 is a standing arrow from C2, R01 → P01, of kind order. Its connection reads: 'in a room carrying both, the first proposal or start of a mark comes before the first call for hands'. It is the first link of the account's spine. C2 counted it in 64 of 89 rooms carrying both (0.719; null mean 0.473, p95 0.539), with 25 rooms in the bound's order. G33 was written before any line was read. Its amendment was written before any restrict line was ruled, and its readings are written under it (above). All 646 lines, in 645 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a02_census.py` and `d3_pair_check.py`.

| op | lines | specification | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|
| instantiate | 215 | 140 | 0 | 0 | 0 | 75 |
| absent (252 `not-testable`, 23 `unobserved`) | 275 | 0 | 0 | 211 | 0 | 64 |
| restrict | 134 | 55 | 0 | 77 | 2 | 0 |
| add-condition | 17 | 17 | 0 | 0 | 0 | 0 |
| add-step | 5 | 5 | 0 | 0 | 0 | 0 |
| all | 646 | 217 | 0 | 288 | 2 | 139 |

**What the rooms show (the census, `d3_a02_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision written.
- **The order, 191 rooms.** A member starts or proposes the mark, and a call for that mark comes after it ('I've started the upper rays at 824,913', NewMexico; 'a pineapple construction has begun at (842, 230) ... Come out and help', trees; 'Trying to get a small UVA logo going' at h+47.81, then 'Unfinished, but help is welcome' at h+55.25, uva).
- **A joint opening with a later call, 65 rooms.** The first post proposes the mark and calls for hands, and a later call gathers around the mark (monstercat, timbers, chelseafc). G33 accepts this as the mechanism shown.
- **The bound, 12 rooms.** A bare call that names no mark comes before the proposal ('Hey, do you guys wanna coordinate to create something on r/place?' at h+39.92, then 'I'm getting started right now. Join me' at h+47.31, 49ers). The others are 4chan, androidgaming, chicago, gorillaz, kuwait, nerf, newzealand, stevenuniverse, titanfall, unitedkingdom and yugioh.
- **The falsifier, 1 room.** criticalrole: 'I started that on my own, apparently people understood what I was going for fairly quickly and we managed to get it done' (h+74.42). A start drew helpers by sight, with no call.
- No room shows both the hold and the bound. So 269 rooms show an episode. The hold (the order or a joint opening with a later call) is shown in 256 of them (0.952). The order alone is shown in 191 of the 204 rooms with the order, the bound or the falsifier (0.936). The helper also prints 191 of 269 (0.710), a figure that counts the 65 joint-opening rooms against the order; it is not used.

**The joint opening.** The commonest form the labelers name is the joint opening: one post proposes the mark and calls for hands ('let's draw a monokuma on r/place', danganronpa). 157 rooms show only a lone joint opening. With the 65 rooms where a later call follows, 222 rooms show the start and the call in one post. All 22 add lines name it. A lone joint opening neither holds A02's order nor meets its `mechanism_fails_if`, so the census counts it apart (G33's amendment). The add lines are specifications naming R01 and P01, whose statements one post shows at once.

**Beside C2's count.** C2 compared each room's first coded concepts, and found the bound's order in 25 of 89 rooms. The read lines show the bound in 12 rooms. The two counts differ in kind. The first-concept test counts the order only when the first start concept comes strictly before the first call concept (`c2_arrow_evidence.py`, line 56: `min(hf) < min(ht)`). In a joint opening, both concepts can come from one post at one hour, and the test then counts the room as failing. So C2's 25 rooms can hold joint openings as well as the bound. The census reads what the lines show, and sets the joint opening apart. No ruling rests on the difference.

**No correction (§2).** No restrict line is an accepted correction, so §2 is not triggered. A02 stands as served, with no move. Of the 134 restrict lines, 55 are specifications: the order (31), a joint opening with a later call (20) and the bound (4). 77 are evidence limits, because their concepts show only a joint opening ('Let's start an English flag', england). One restriction meets the falsifier (criticalrole-034). No second room's line meets it, so it is this room's particular (G4 and G5). It sits beside P15's carried family of joins that wait on a visible start. marvel-039 is NONPORTABLE ('shield'), a particular (G6).

**What the instantiate rejects show (75).** A lone joint opening, 60. The bound, 8 (49ers, 4chan, gorillaz, kuwait, newzealand, titanfall, unitedkingdom, yugioh). One end only, 4. Other, 3: a successor canvas (kirby), credits after the close (ireland) and a call to help another room's hearts (wholesomememes).

**Absent lines.** No line is evidenced, and none is NONPORTABLE. 64 claims of absence fail because the concepts show the order, or a joint opening followed by a later call (23, 19 and 22 by packet). Many labelers marked these not-testable because no causal link is stated; G33 asks for the order, which the concepts show. The other 211 are evidence limits. A guard listed four limits whose labels name a start, for a second look. Three stayed limits (EraseThePlace, afip, mylittlepony). One moved: SwissNeutralityZone-041 ('We need more pixels !!!' at h+21.09, a call to defend and repair the zone; 'I put the first pixels' at h+74.48, a credited starter), read as bulgaria-043 was.

**Repairs (G7).** Lines in repaired rooms were 0.783 accepted (355 lines), and in unrepaired rooms 0.780 (291 lines). No ruling rests on the difference.

**Carried to later groups.**
- **The spine line.** The account says 'The room's calls follow the start in 64 of 89 rooms'. D3c's re-read weighs it beside the census and the joint opening, and D4 takes the joint opening as a form.
- **Joins by sight.** criticalrole's start drew helpers with no call. It goes with P15's carried family of joins that wait on a visible start.
- **The bound's 12 rooms** stay under A02's bound, which already names them. D3c's re-read asks how many of C2's 25 failing rooms are joint openings.
- **The re-check (§5).** A02 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **A superseded instantiate build.** A quote check showed that sweden-036's label hid an instruction given with the call. I moved it from the order to a joint opening and rebuilt the rulings as `A02-inst-v2.jsonl`. `A02-inst.jsonl` stays, unused. The same check moved two restrict lines read from labels only (uoft-005, portal-008) to joint openings before they were written.
- **A superseded absent build.** SwissNeutralityZone-041 was kept as a limit in the first absent packet and moved by the guard. The rulings were rebuilt as `A02-absent-v2.jsonl`. `A02-absent.jsonl` stays, unused; the helper ran into it twice with the same arguments, and the second run rewrote the same content.
- **Order of writing.** The absent map was written before the diary note for the last absent packet. The note names every reject.
- **Compaction.** The context was compacted while the absent lines were ruled. The head was read and reconciled with the diary before the next write.
- **Quotes read.** Instantiate about 70 beyond the draws; restrict 29; absent 40 (17, 10 and 6 by packet, and 7 for the guard).

### Close-check, D3a-28

`validate.py D3` reports 23,980 of 42,243 ledger lines ruled: the 23,334 before this leg and A02's 646. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 24,737 lines: 646 first rulings from this leg and no re-ruling. Appended re-rulings stay at 757.
- **Pairs.** A02's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,235 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-29: A01, the call before the build report

A01 is a standing arrow from C2, P01 → P03, of kind order. Its connection reads: 'in a room carrying both, the first call for hands comes before the first build report'. It is the second link of the account's spine. After Stigmergy's recut, C2 counted it in 81 of 126 rooms (0.643; null mean 0.505, p95 0.571). G34 was written before any line was read, and its readings are written under it (above). All 676 lines, in 664 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a01_census.py` and `d3_pair_check.py`.

| op | lines | specification | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|
| instantiate | 276 | 155 | 0 | 0 | 0 | 121 |
| absent (254 `not-testable`, 19 `unobserved`) | 273 | 0 | 0 | 201 | 1 | 71 |
| restrict | 115 | 97 | 0 | 18 | 0 | 0 |
| add-condition | 12 | 12 | 0 | 0 | 0 | 0 |
| all | 676 | 264 | 0 | 219 | 1 | 192 |

**What the rooms show (the census, `d3_a01_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision written.
- **The order, 265 rooms.** A call comes first, and a report of that mark's state follows ('Lets make a sick O to support our boys', then 'Got a green line started', ducks; 'Build a flag on place' at h+42.07, then 'Me and few friends started building one' at h+53.48, montenegro).
- **The bound, 142 rooms with no order line.** The call comes to a mark already started. In 91 of them the call itself reports the start or the progress, or a report comes first ('I've started the "R" at 685,243', donaldglover; 'some of us from /r/houston have started a Texas one right under it!', texas). In the others the call is to finish, keep or improve a placed mark ('This Australian flag on r/place needs some help', australia).
- Two rooms show both. So 407 rooms show an episode, and the order holds in 265 (0.651). C2's share was 0.643 over 126 rooms.
- **The bound is not marginal.** In about a third of the rooms with an episode, the starter places the mark first and the call then reports it. That is the route that A01's bound and A02 already state: a start, then the call. In those 91 rooms, A02's order and A01's bound are one sequence: a placed start, a call that reports it, then building.

**No correction (§2).** No restrict line is an accepted correction. Most restrict lines say that the record cannot show which placings the call caused. A01 claims an order counted inside each room, so that condition does not make it fail. Of the 115 lines, 97 are specifications: the order 39, the bound 54, and 4 held by other statements under G4a. The 4 are chess-031 and tetris-002, calls met by the close (P12's 'the end marked'); hearthstone-003, a call with no plan (P04); and splatoon-035, calls met by design changes and requests for a start (P02, P04). 18 are evidence limits. The 12 add-condition lines are specifications naming P04, K02, P15, R01, A02, P01, P08, P12 or A01's bound. A01 stands as served, with no move.

**What the instantiate rejects show (121).** The call reports a start or progress, or a report comes first, 61. A call for a placed mark, 28. A join, pledge, cheer or advice follows, 23. One end only, 5. Another canvas or a report after the close, 4.

**Absent lines.** No line is evidenced. 71 claims of absence fail because the concepts show the order (14, 31 and 26 by packet). Many labelers marked these not-testable because no answer says the call brought the builder; G34 asks for the order, which the concepts show. One line is NONPORTABLE (marvel-042, 'shield'), a particular by G6. The other 201 are evidence limits. A guard listed 37 limits whose labels name progress or completion; none moved.

**Repairs (G7).** Lines in repaired rooms were 0.715 accepted (369 lines), and in unrepaired rooms 0.713 (307 lines). No ruling rests on the difference.

**Carried to later groups.**
- **The spine.** A02's order and A01's bound describe one sequence in 91 rooms. D3c's re-read weighs the spine's two links together.
- **Joins that wait on a start** (penguins-045: 'once someone sets the anchor') go with P15's carried family and criticalrole's join by sight.
- **Calls at the close** (chess, tetris, worldoftanks) and **lone builders** (flashtv, frankocean, enterthegungeon) sit beside K02 and the canvas clock.
- **A01's counterexample response** still names 53 of 190 rooms from before the recut. It is carried with the fields the prose rule did not read.
- **The re-check (§5).** A01 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quote counts.** Two diary notes gave wrong quote counts (73 for 75 in the first instantiate packet, 51 for 97 in the restrict lines). Later notes corrected both. Quotes read: instantiate 211 beyond the draws, restrict 97, absent 227.
- **One reclassification inside the leg.** gorillaz-005 was first read as the order and moved to BOUND-S before any line was written, to match G33's reading of present-tense starts.
- **The census's start subtype.** For restrict lines, the helper finds the bound's start subtype by phrases in my evidence. A phrase list can miss or catch a line, so the 91 is approximate for restrict lines; instantiate lines are counted by class.
- **New builders.** `d3_arrow_inst_rulings_v2.py` and `d3_arrow_restrict_rulings_v2.py` take their classes from clause files. The A02 builders stay as they were.
- **A stray no-op in a command.** While checking the head script, one command began with `python3 -`, which read no input and did nothing, against the rule on placeholders and no-ops. The permission check did not refuse it. The command's real check ran after it and wrote nothing.

### Close-check, D3a-29

`validate.py D3` reports 24,656 of 42,243 ledger lines ruled: the 23,980 before this leg and A01's 676. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 25,413 lines: 676 first rulings from this leg and no re-ruling. Appended re-rulings stay at 757.
- **Pairs.** A01's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,235 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-30: A03, the build report before upkeep

A03 is a standing arrow from C2, P03 → P05, of kind order. Its connection reads: 'in a room carrying both, the first build report comes before the first act of upkeep or defence'. It is the last link of the account's spine. After Stigmergy's recut, C2 counted it in 148 of 190 rooms (0.779; null mean 0.340, p95 0.389). G35 was written before any line was read, and its readings are written under it (above). All 688 lines, in 672 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a03_census.py` and `d3_pair_check.py`.

| op | lines | specification | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|
| instantiate | 380 | 236 | 0 | 0 | 5 | 139 |
| absent (167 `not-testable`, 16 `unobserved`) | 183 | 0 | 0 | 148 | 2 | 33 |
| restrict | 82 | 55 | 0 | 27 | 0 | 0 |
| add-condition | 42 | 42 | 0 | 0 | 0 | 0 |
| add-step | 1 | 1 | 0 | 0 | 0 | 0 |
| all | 688 | 334 | 0 | 175 | 7 | 172 |

**What the rooms show (the census, `d3_a03_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision written.
- **The order, 308 rooms.** A report of the mark's state comes first, and upkeep or defence of that mark follows ('Completed just a few minutes ago. What it needs now is for us to actively defend it.', bostonceltics; 'EDIT: Done!' at h+39.63, then 'SOME N'WAHS ARE FUCKIN WITH OUR VIVEC. FIX THIS SHIT!' at h+52.31, truestl).
- **The bound, 23 rooms.** Upkeep comes before the line's only report: the mark was already placed, inherited or attacked first ('I've been trying to fight off kU to keep our MU going.' before 'The M is currently in good shape, but the U is F'd', mizzou; r/Megumin's chart kept overnight, konosuba).
- No room shows both. So 331 rooms show an episode, and the order holds in 308 (0.931). 32 rooms show only a first report that is itself damage (J), counted apart; with them, the order holds in 308 of 363 (0.848). C2's share was 0.779 over 190 rooms.
- **The cheer, then upkeep.** 95 lines show one end. Most are a bare cheer followed by upkeep: 'We did it! Now we must defend it' (49ers, MMA, armenia, parahumans, warframe). G15 does not count a bare cheer as a report of the work, so these lines show P11's marking and P05's upkeep, not P03 before P05. In the members' own words, the turn from a cheer to upkeep is the commonest form of the spine's last link.

**No correction (§2).** No restrict line is an accepted correction. Most restrict lines say that upkeep overlaps unfinished building. A03's connection asks for a build report before upkeep, not a completion (G15 counts 'begun' and 'half done'), and its mechanism speaks of 'a finished part', so the condition is held. Of the 82 lines, 55 are specifications: the order 37, the bound 15, and 3 held by other statements under G4a (penguins-047, a move after being overrun, P10 and A10; popheads-026 and wsu-015, no hands to keep the work, K02). 27 are evidence limits. The 43 add lines are specifications: 35 name A03's own connection and mechanism, 4 name P05 (upkeep before growth, defence under attack), 1 names P05 and P02 (monsterhunter-018: a piece dropped from the agreed plan is no longer kept, as move 173 states), 2 name P12 (the close) and 1 names K02. A03 stands as served, with no move.

**What the instantiate rejects show (139).** One end, 95. J, 32. The bound, 8. Another canvas or a report after the close, 4. Five more lines are NONPORTABLE ('lost', 'overwatch') and are particulars by G6.

**Absent lines.** No line is evidenced. 33 claims of absence fail because the concepts show the order (15 and 17 by packet, and one moved by the guard). Many labelers marked these not-testable because no member says the report caused the upkeep; G35 asks for the order, which the concepts show. Two lines are NONPORTABLE particulars (CSUFoCo-041, superman-041). The other 148 are evidence limits. A guard listed 22 limits whose labels name progress or completion. One moved: epublica-058 ('ahora que somos mas quizas podriamos hacerla mas ancha', then 'Deberíamos enfocarnos en proteger lo que tenemos hecho').

**Repairs (G7).** Lines in repaired rooms were 0.760 accepted (379 lines), and in unrepaired rooms 0.715 (309 lines). No ruling rests on the difference.

**Carried to later groups.**
- **The spine.** The cheer followed by upkeep is the commonest form of A03 in the members' words; it joins P11 and P05. D3c's re-read weighs the spine's three links together (A02's joint opening, A01's bound, A03's cheer).
- **Keeping given up.** A room overrun may move rather than keep (P10, A10), and a room without hands may not keep a finished work (K02). Both go with the loss family already carried.
- **A03's counterexample response** still names 109 of 291 rooms from before the recut. It is carried with the fields the prose rule did not read.
- **The re-check (§5).** A03 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quote counts.** One diary note gave a wrong quote count (92 for 68 in the first instantiate packet), and one gave the add counts split wrongly; later notes corrected both from scripts. Quotes read: instantiate 224 beyond the draws, restrict none (every restrict line is accepted either way, so the labels were read without quotes), absent 73.
- **Reclassifications inside the leg.** Four instantiate lines moved from J to the order by the reading on building reported with damage, before any line was written (`d3a30_spec_fix.py`).
- **A superseded absent build.** epublica-058 moved by the guard; the rulings were rebuilt as `A03-absent-v2.jsonl`. `A03-absent.jsonl` stays, unused.
- **Builder change.** `d3_arrow_inst_rulings_v2.py` now also takes 'particular' as a clause decision, for NONPORTABLE instantiate lines. A01's build used only accept and reject, so its output is unchanged.

### Close-check, D3a-30

`validate.py D3` reports 25,344 of 42,243 ledger lines ruled: the 24,656 before this leg and A03's 688. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 26,101 lines: 688 first rulings from this leg and no re-ruling. Appended re-rulings stay at 757.
- **Pairs.** A03's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,235 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-31: A04, upkeep before border talk

A04 is a standing arrow from C2, P05 → P08, of kind order. Its connection reads: 'in a room carrying both, the first act of upkeep or defence comes before the first border talk, truce or deal'. Its bound names the rooms where border talk comes first, and C5's two coders found that such talk mostly offers terms before any damage. C2 counted the order in 235 of 401 rooms (0.586; null mean 0.501, p95 0.539). G36 was written before any line was read, and its readings are written under it (above). All 668 lines, in 662 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a04_census.py` and `d3_pair_check.py`.

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 181 | 58 | 0 | 0 | 0 | 5 | 118 |
| absent (216 `not-testable`, 64 `unobserved`) | 280 | 0 | 0 | 0 | 225 | 3 | 52 |
| restrict | 170 | 151 | 0 | 0 | 19 | 0 | 0 |
| add-condition | 35 | 34 | 1 | 0 | 0 | 0 | 0 |
| add-step | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| contradict | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| all | 668 | 245 | 1 | 0 | 244 | 8 | 170 |

**What the rooms show (the census, `d3_a04_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision written.
- **The order, 141 rooms.** Upkeep or defence of the room's mark comes first, and terms with another room follow ('I will put my pixels to work fighting the grey invaders to the north east', then 'Had a calm talk with them and they agreed to move.', japan; 'To defend it, click here', then a neighbour's 'Maybe we lower the head a bit and you leave some space to the right?', cavestory).
- **The bound, 124 rooms.** The room's first talk comes before any upkeep or damage: space asked while building, terms before damage, or entry through another room's offer ('We'd like to avoid unnecessary fights and wasted pixel placements, so we'd like to propose cooperation.', paydaytheheist; 'WE GOT PERMISSION FROM R/GREENLATTICE', then 'Now let's defend and protect it well.', hongkong).
- Two rooms show both. So 265 rooms show an episode, and the order holds in 141 (0.532). 56 rooms show only J or a proposal to ask; with them, the order holds in 141 of 321 (0.439). C2's share was 0.586 over 401 rooms.
- **The turn that stops at a proposal.** In 33 rooms, upkeep is followed by a member's proposal to talk with no request made ('Could we get a mod to request r/ainbowroad to coexist with our small place?', PUBATTLEGROUNDS; 'Propongo di passare alla diplomazia con l'Inghilterra', italy). G18 does not count these as terms. Both of A04's support transitions are of this kind.

**No correction (§2).** No restrict line is an accepted correction. Of the 170, 151 are specifications and 19 are evidence limits. Most say that border talk can begin while the mark is being built, before any damage, or on entry through another room's offer; A04's bound holds that (90 lines). 31 show the order. 30 are held by other statements under G4a: 22 by A17, since the talk answers the room's own encroachment on a neighbour (croatia, czech, habs, mechanicalkeyboards); 2 by P07 with A05's bound (Summit1G, satania); and one each by P07 with P05's upkeep before growth (funhaus), P05 and P02 (AyyMD, a change the room's own members made), P17 and P21 (TheB1G), P10 (nyjets), A19 and P07 (parrots) and P16 (uiowa). The 36 add lines are 35 specifications, held by A04's bound (19), A17 (9), A04's connection as G36 reads it (4), P16 and A14 (de), P05 and P02 (taiwan) and a counting rule read by its concepts (suomi), and one paired elaboration. That elaboration is AmericanFlaginPlace-026: working out who placed the pixels before treating erosion as a neighbour's conduct is P06's form, a candidate, paired with ucf-016 from P08's group as G18 paired such lines. The contradict line (lithuania-041) states the bound's pattern, a neighbour's terms before any upkeep, so it is a specification. A04 stands as bounded, with no move.

**What the instantiate rejects show (118).** Proposals to ask, 33. Damage inside the talk (J), 23. Not P08's terms, 21: choices inside the room, appeals with no terms, lone placers, help and alliances. The bound, 15. The neighbour's own upkeep or after hour 73, 10. A loss or a move, 8. One end, 8. Five more lines are NONPORTABLE ('quebec', 'halo', 'mexico', 'france', 'sweden') and are particulars by G6.

**Absent lines.** No line is evidenced: 216 are `not-testable` and 64 `unobserved`. 52 claims of absence fail because a concept shows upkeep or defence and, after it, terms with another room. Many labelers marked these not-testable because no member says the upkeep caused the talk; G36 asks for the order, which the concepts show. Three lines are NONPORTABLE particulars (AprilKnights-035, Clannad-024, belgium-038). The other 225 are evidence limits. A guard listed 66 limits whose labels name talk; each was looked at again, and one moved (lost-037, one post naming upkeep and then two treaties).

**Repairs (G7).** Lines in repaired rooms were 0.722 accepted (370 lines), and in unrepaired rooms 0.748 (298 lines). No ruling rests on the difference.

**Carried to later groups.**
- **The near-even split.** The read lines show the order in 141 rooms and talk first in 124. Talk first is mostly space asked while building or terms offered before damage, the pattern A04's bound and C5's coders name. D3c's re-read and D4 weigh it with the spine's three links.
- **The turn that stops at a proposal** (33 rooms) and A04's support transitions, which are proposals. D3c weighs whether the mechanism's 'turns to talk' is shown by proposals or only by terms.
- **The room's own encroachment.** Talk that answers the room's covering of a neighbour (22 restrict lines and 9 adds) belongs with A17 and the contest family.
- **Attribution** (AmericanFlaginPlace-026, paragon-027, SquareSpiral-053) is P06's form, carried to the clustering.
- **The re-check (§5).** A04 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 403 concepts and restrict 529, every cited concept of every line; absent 189, in five batches and one check. Eight threads were read whole for doubtful lines.
- **Counts typed before counting.** Two diary notes gave sub-counts typed before a script counted them (21 for 22 restrict lines held by A17; 20 for 19 add lines held by the bound). Later notes corrected both from scripts. The ledger count in the absent note was computed by adding 280 to the previous count before `wc -l` printed it; the printed count matched.
- **Two Edits in one turn.** Two Edits to `d3_a04_adds.py` ran in one turn, on different lines; both were checked by `grep` before the script ran.
- **A refused check.** A one-line coverage check was refused by the permission check. It was replaced by `d3_spec_cover.py`.
- **Reclassification inside the leg.** harrypotter-022 moved from the order to J by the reading on complaints, before any line was written.
- **A superseded absent build.** lost-037 moved by the guard; the rulings were rebuilt as `A04-absent-v2.jsonl`. `A04-absent.jsonl` stays, unused.

### Close-check, D3a-31

`validate.py D3` reports 26,012 of 42,243 ledger lines ruled: the 25,344 before this leg and A04's 668. It reports 0 errors and the same 2 old warnings on history lines 137 and 138.
- **The ledger** holds 26,769 lines: 668 first rulings from this leg and no re-ruling. Appended re-rulings stay at 757.
- **Pairs.** A04's files hold one pair, AmericanFlaginPlace-026 with ucf-016 (`d3_pair_check.py`). Across the ledger, 1,236 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-32: A05, a settled border before sparing

A05 is a standing arrow from C2, P08 → P07, of kind order and strength thin. Its connection reads: 'in a room carrying both, the first border talk, truce or deal comes before the first act of sparing a neighbour'. Its mechanism says that members spare the neighbour's work by a settled border and remind others of it. At C5c-09 that mechanism was marked theorised: the first sparing names a border, truce, deal, policy or agreement in 17 of 124 rooms (F-020). C2 counted the order in 106 of 158 rooms (0.671; null mean 0.600, p95 0.658). G37 was written before any line was read, and its readings are written under it (above). All 707 lines, in 666 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a05_census.py`, `d3_spec_cover.py` and `d3_pair_check.py`.

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 198 | 154 | 0 | 0 | 0 | 5 | 39 |
| absent (236 `not-testable`, 40 `unobserved`, 1 `not-needed`) | 277 | 1 | 0 | 0 | 249 | 3 | 24 |
| restrict | 170 | 155 | 0 | 0 | 14 | 1 | 0 |
| add-condition | 60 | 60 | 0 | 0 | 0 | 0 | 0 |
| add-step | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| all | 707 | 372 | 0 | 0 | 263 | 9 | 63 |

**What the rooms show (the census, `d3_a05_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision written.
- **The order, 227 rooms.** P08's terms come first, and sparing follows. In 131 of these rooms, a sparing or a reminder names the agreement already made, so the mechanism is in the members' words ('Remember guys we agreed with r/Poland to a 3px wide border. I am rebuilding their flag where we overstep our agreement. Please don't violate it.', AMD; 'No, tenemos definidos bordes.', GranColombia). In the others, the hours show terms first and restraint after ('We had to get a deal with the Bob Ross people.', then 'We moved away from Bob so he could live in peace!', ethereum).
- **The bound, 75 rooms (68 with no order line).** Sparing comes first, on a norm, the cost of a fight, a refused raid or an apology, before any talk or with none ('Let's let /r/doormonster do it's thing to the left of us, let's work around them', then 'We should live and let live.', 49ers; 'it is probably best if we don't piss off another group of people by burninating the Achievement Hunters' logo', HomestarRunner).
- Seven rooms show both. So 295 rooms show an episode, and the order holds in 227 (0.769). Ten rooms show only an unreadable order or an appeal answered by restraint; with them, the order holds in 227 of 305 (0.744). C2's share was 0.671 over 158 rooms.
- **The order named in words, against C5c-09.** It is named in 131 rooms, 0.444 of the episode rooms; C5c-09 found 17 of 124. The two counts measure different things. C5c-09 read each room's first sparing. This census counts a room where any ruled line names the agreement (G37's reading on the order named in words), and the labelers chose the lines for the arrow. So the census does not overturn F-020's read of the first sparing. It shows that, once an agreement is made, members often spare by it and remind others of it in their own words.

**No correction (§2).** No restrict line is an accepted correction. Of the 170, 155 are specifications, 14 are evidence limits and 1 is a NONPORTABLE particular (thepointing-037). By class: the bound's pattern 64; held by another statement 37, of which 31 name P21; the order named in words 34; the order by terms then restraint 20. Most restrictions say that an agreement restrains only the placers it reaches, and P21 holds that. Every line that meets the falsifier, a settled border followed by no sparing, is held by another statement: a breach complained of is P08's holding to terms (rpi, timbers), terms rejected by members are P21's (eve, EraseThePlace, btc), and an attack after terms is P09's (cirkeltrek, ss13). The 62 add lines are all specifications: held by P21 with A05's mechanism (37), by P14 with P21 (5, scripts), by A05's own bound (11: memorials, norms, first makers, apologies, complaints answered), by A05's own connection (5: restraint promised while terms are talked; an offer refused), and one each by A16 (greenbaypackers), P08's conditional terms (uofm), P09 with P17 (texastech) and P12 (torontoraptors). None names a form the model lacks, so none is an elaboration. A05 stands with its bound, with no move.

**What the instantiate rejects show (39).** One end, 16. Alliances as such, 10. Appeals answered by restraint, 7. Order unreadable, 3. After hour 73, 3. Five more lines are NONPORTABLE (Northwestern-045, Russiaclan-037, SquareSpiral-054, ainbowroad-051, czech-059) and are particulars by G6. No instantiate line shows the bound's pattern after the reading on the order named in words moved foxes-046.

**Absent lines.** One line is evidenced: montenegro-039, `not-needed`, where a deal is asked for and refused, talk with no sparing; it is a specification. 24 claims of absence fail, because a concept shows P08's terms and, after them, sparing: 22 by the hours or one post, and 2 by a sparing that names a settled border (GranColombia-034, furry_irl-063). Many labelers marked these not-testable because no member says the agreement caused the restraint; G37 asks for the order, which the concepts show. Three lines are NONPORTABLE particulars (linux-032, planetside-049, russia-046). The other 249 are evidence limits. A guard listed 62 limits whose labels name talk; each was read, and none moved.

**Repairs (G7).** Lines in repaired rooms were 0.908 accepted (391 lines), and in unrepaired rooms 0.886 (316 lines). No ruling rests on the difference.

**Carried to later groups.**
- **The mechanism's mark.** D3c weighs whether A05's mechanism stays theorised, with F-020 re-read beside the 131 rooms whose lines name the agreement in words.
- **The bound.** Sparing comes first in 75 rooms. The account's sentence that sparing rests on the room's own norm is weighed at D3c with the census.
- **Agreements that do not reach every placer.** 31 restrict lines and 37 adds are held by P21. They go with P21 and A21 to the re-check's reading.
- **The host's rules for guests** (warframe-035) are P19's form, a candidate, carried to the clustering.
- **The re-check (§5).** A05 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 416 concepts and restrict 511, every cited concept of every line; absent 164 in five batches, and 4 more for the guard.
- **A first draft that joined two rooms.** G37's first draft paired quotes from two rooms; the pairing was removed before G37 was logged.
- **Quotes in a diary note.** The note on the first draw gives two quotes without the accents and the apostrophe that `cite.py` prints (brasil-032, ireland-033). The rulings files carry them as `cite.py` prints them, and a later note disclosed the slip.
- **A refused command.** The first command to write the absent batch put `cut -c` after a helper, and the permission check refused it. Nothing was written; the command ran again without it.
- **Reclassification inside the leg.** The reading on the order named in words moved danganronpa-026, littlewitchacademia-030 and foxes-046 before any line was written.

### Close-check, D3a-32

`validate.py D3` reports 26,719 of 42,243 ledger lines ruled: the 26,012 before this leg and A05's 707. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 27,476 lines: 707 first rulings from this leg and no re-ruling. Appended re-rulings stay at 757.
- **Pairs.** A05's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,236 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-33: A06, upkeep before machine hands

A06 is a standing arrow from C2, P05 → P14, of kind order and strength strong. Its connection reads: 'in a room carrying both, the first act of upkeep or defence comes before the first script, bot or extra account'. Its mechanism says that upkeep under attack outruns what one pixel per interval can hold, so members turn to scripts and spare accounts. Its bound names rooms that scripted the building from the start, and spare accounts that serve an attack. C2 counted the order in 160 of 203 rooms (0.788; null mean 0.603, p95 0.655), and F-005 states it. G38 was written before any line was read, and its readings are written under it (above). All 708 lines, in 690 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a06_census.py`, `d3_spec_cover.py` and `d3_pair_check.py`. The quotes in the rulings were checked against `cite.py`'s output by `d3_spec_quotes.py`, new at this leg.

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 61 | 32 | 0 | 0 | 0 | 3 | 26 |
| absent (342 `not-testable`, 126 `unobserved`) | 468 | 0 | 0 | 0 | 442 | 0 | 26 |
| restrict | 156 | 124 | 0 | 0 | 31 | 1 | 0 |
| add-condition | 23 | 23 | 0 | 0 | 0 | 0 | 0 |
| all | 708 | 179 | 0 | 0 | 473 | 4 | 52 |

**What the rooms show (the census, `d3_a06_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision written.
- **The order, 87 rooms.** Upkeep or defence comes first, and machine hands put to work follow. In 46 of these rooms, the members name the machine hands as the answer to an attack, a loss or the strain of keeping up ('The Hammer and Sickle is under siege. Need all available comrades to assist in defending', then 'I have *fully automated* my reddit account for constant maintenance of the h&s.', TheFarLeftSide; 'I'm trying, but a 5 minute cool-down can only get you so far.', then 'Hey guys: we have a JavaScript script to reclaim our land', cfb). In the others, the hours show the upkeep first ('I will work to maintain our flag from any would be invaders', then 'I've got two browsers open with a couple of accounts to help maintain.', texas).
- **The bound, 58 rooms (57 with no order line).** Machine hands come before any upkeep: scripts that build the mark, spare accounts during building, and bots that take space or serve an attack ('I'm running a script to create a flag in the blue corner.', england; 'Psst. You can use alt accounts to get 3 or 4 squares every 10 min.', canucks, the room the bound names).
- One room shows both. So 144 rooms show an episode, and the order holds in 87 (0.604). Twelve rooms show only one act holding both ends; with them, the order holds in 87 of 156 (0.558). C2's share was 0.788 over 203 rooms, and its counterexample response counted 43 of 203 rooms in the bound's order.
- **Why the shares differ.** C2 counted the first concept of each element in every room carrying both. This census counts the lines the labelers returned, and 52 of the 156 restrict lines were returned to say that machine hands came first, for building or an attack. The bound states that condition, so those lines are specifications. The census does not overturn C2's count, but in the return's lines the bound's pattern is common: 58 of 144 episode rooms.

**No correction (§2).** No restrict line is an accepted correction. Of the 156, 124 are specifications, 31 are evidence limits and 1 is a NONPORTABLE particular (ice_poseidon-023). By class: the bound's pattern 52; held by another statement 42; the order named in words 18; the order by the hours 12. Of the 42 held lines, 27 name P14's statement, where members argue over scripts, refuse them or shame them under strain ('With scripts? No thanks.', rangers; 'No, we don't write scripts because we believe it is against the spirit of /r/place.', mindcrack). 15 name P05, where the room keeps by hand, covers the night or holds the known form ('Ok So I edited a script to be able to maintain our G without having to sit and watch it.', greenbaypackers). 8 name K02, where members judge their hands or their skill too few, or give up. 3 name P16 with P14's range, for allies' machine hands, and 2 name P09, for bots in an attack. No restriction shows machine hands before upkeep in a room that did not build or attack with them. Every room under strain that never turned to machine hands is held by P05, P14's argument or K02, as G38 reads the falsifier's second clause. The 23 add lines are all specifications: 7 are held by A06's mechanism and 5 by A06's bound; the others are held by P05, P14's argument and adjusting, K02, P10, P09, P04, and A19 with P02, and one counting rule is ruled by its concepts (ethereum-051). A06 stands with its bound, with no move.

**What the instantiate rejects show (26).** One act holding both ends, 9, and the same with the mechanism named later, 4. Machine hands first shown after hour 73, 6. A proposal or a rival's script in place of machine hands, 4. The bound's pattern, 2. One end, 1. Three more lines are NONPORTABLE (TransFlagPlace-041, archlinux-046, day9-047) and are particulars by G6.

**Absent lines.** No line is evidenced: 342 are `not-testable` and 126 `unobserved`. 26 claims of absence fail, because a concept shows upkeep or a warning and, after it, machine hands put to work: 24 by the hours, a reply that answers the call, or one post, and 2 in the members' words (phish-021, satania-044). The other 442 are evidence limits. A guard listed 179 limits whose labels name machine hands. All were read in the packets, four were looked at again with quotes, and none moved.

**Repairs (G7).** Lines in repaired rooms were 0.924 accepted (384 lines), and in unrepaired rooms 0.917 (324 lines). No ruling rests on the difference.

**Carried to later groups.**
- **The bound's share.** In the return's lines, the bound's pattern is in 58 of 144 episode rooms. D3c weighs it with F-005's statement and A06's strength.
- **The mechanism in words.** In 46 rooms, members name the machine hands as the answer to an attack or to strain. D3c reads this beside A05's mechanism and the account's sentence on machine hands.
- **Refusals under strain** (P14's argument, 27 restrict lines) belong with P14's group.
- **Allies' machine hands** (P16 and P14's range: FinalFantasy, uruguay, kingdomhearts) belong with help between rooms.
- **The re-check (§5).** A06 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 133 concepts and restrict 459, every cited concept of every line; absent 132 in four batches, and 10 more for the guard.
- **A background job.** The restrict quote job ran past the two-minute limit and moved to the background. I ruled the add lines while it ran, and read its files only after it finished.
- **A muddled figure in a note.** The census note puts A05's p95 beside A06's in one parenthesis. A06's p95 is 0.655, as the arrow states.
- **Reclassification inside the leg.** The reading on either word order moved muse-042 from J, as the draw note had it, before any line was written.

### Close-check, D3a-33

`validate.py D3` reports 27,427 of 42,243 ledger lines ruled: the 26,719 before this leg and A06's 708. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 28,184 lines: 708 first rulings from this leg and no re-ruling. Appended re-rulings stay at 757.
- **Pairs.** A06's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,236 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-34: A07, the build report before the marking

A07 is a standing arrow from C2, P03 → P11, of kind order and strength strong. Its connection reads: 'in a room carrying both, the first build report comes before the first marking of the finished work'. Its mechanism says that a mark reported done gives the room a finished thing to point at, and the room marks it together. Its bound names a find made by others, celebrated before the room builds, and a work the close cut unfinished, whose attempt the room marks. C2 counted the order in 139 of 182 rooms (0.764; null mean 0.378, p95 0.434). No finding touches A07. G39 was written before any line was read, and its readings are written under it (above). All 673 lines, in 663 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a07_census.py`, `d3_spec_cover.py` and `d3_pair_check.py`. The quotes in the rulings were checked against `cite.py`'s output by `d3_spec_quotes.py`.

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 367 | 74 | 0 | 0 | 0 | 2 | 291 |
| absent (`not-testable` 121 accepted, 32 rejected; `unobserved` 18 and 4; `not-needed` 1) | 176 | 1 | 0 | 0 | 139 | 0 | 36 |
| restrict | 105 | 77 | 5 | 0 | 23 | 0 | 0 |
| add-condition | 23 | 17 | 2 | 0 | 3 | 1 | 0 |
| add-step | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| contradict | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| all | 673 | 170 | 7 | 0 | 166 | 3 | 327 |

**What the rooms show (the census, `d3_a07_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision and kind written.
- **The order, 131 rooms.** A report of the room's build comes first, and a marking of the work follows. In 24 rooms a plain report is answered by a marking, the mechanism in words ('Completado', then 'Lo logramos, quedó inmortalizado. Felicitaciones a todos.', colombia; 'It's complete.', then 'clap clap clap', anime_irl). In the others the hours show the report first ('Working on it! Just placed my third pixel in support.', then 'We did it /r/math!', math).
- **The bound, 26 rooms (25 with no order line).** The close cut the work unfinished and the room marks the attempt ('We almost did it!', ultrahardcore, a room the bound names; 'Although it's unfinished - we successfully made our mark.', skyrim), or the room announces a find made by others ('I'm not sure who was responsible for it.', batman).
- One room shows both. So 156 rooms show an episode, and the order holds in 131 (0.840). C2's share was 0.764 over 182 rooms.
- **One act holding both ends, 189 rooms with no order or bound.** The members' first report is itself the marking ('We did it Reddit! Chatot has been made on /r/place!', twitchplayspokemon; 'Het volkslied is voltooid!! Leve de koning!', thenetherlands). The order cannot be read in these rooms, and G39 counts them apart.
- **An early marking, 15 rooms with no order, bound or joint act.** The room marks the work and then reports it unfinished ('We made it on /r/place!', then 'Not done yet!', starbound). P11 holds this on the room's word.
- With the joint-only and early-only rooms in the denominator, the order holds in 131 of 360 rooms (0.364), below C2's null mean.
- **Why the shares differ.** C2 counted the first concept of each element in each room. A concept that holds both ends counts for both at one hour. The return's lines read such a post as one act, and in 189 rooms that is all they show. Where the lines can place a report before a marking, the order holds more often than C2 counted. But an episode shows in only 156 of the 360 rooms that show an episode, one act holding both ends, or an early marking alone.
- **The family, 7 rooms.** The room marks an attempt that ended before the close with no finished work standing ('most likely bots started to erasing him so I just gave up', then 'Valiant effort!!!', faeria). These are D3a-13's family, paired within itself.

**No correction (§2).** No restrict or contradict line is an accepted correction. Of the 105 restrict lines, 77 are specifications, 23 are evidence limits and 5 are paired elaborations. By class: held by another statement 37; the bound's pattern 20; the order by the hours or in one post 16; the mechanism in words 4. Of the 37 held lines, 29 name P11's statement as G16 reads it. In 13 of them a marking comes before a report that the work is unfinished ('We did it, r/Lakers!', then 'Not quite done in that pic', lakers). The others mark a part, a version, a presence or what the work meant while building goes on. 8 name P05 (repair or upkeep after the marking), 6 name P02 (additions or a design argued after the marking), and 3 name P20, where a member argues the canvas's worth beside the marking ('Where can someone get an actual explanation of what this loser shit is?', chicago). P09 and P12 are named twice each, and P07, P15 and P16 once each. The 23 evidence limits show one act holding both ends, cheers with no report, a cheer for progress or a defence, parts reported and then lost, or records after hour 73 only. The 5 elaborations are D3a-13's family. No restriction shows a marking before any build report, in a room that neither found the work nor was cut by the close, that P11 does not hold on the room's word. The contradict line (warthunder-059) says that credit needs no finished work. There the close cut the plane halfway, which A07's bound holds, so the line is a specification. Of the 24 add-condition and add-step lines, 17 are specifications: 4 name A07's own bound (bulgaria, corridor, qotsa, and sheffield with P05), 1 restates A07's connection (kpop), and 12 name other statements (10 name P11 as G16 reads it, with P02, P05, K02 or A03 where the condition names them; touhou names P02 alone; babymetal names A03 and P05). 4 are counting rules, ruled by their concepts, which show one act (evidence limits). 2 are the family (Thegreatblackhole with mizzou, columbia with foxes), and 1 is a NONPORTABLE particular (fullcommunism-038). A07 stands as served, with no move.

**What the instantiate lines show.** Accepted 74: the order by the hours, a reply or one post, 60; the mechanism in words, 14. Rejected 291: one act holding both ends, 190; one end, 55 (a marking with no build report, a report with no marking, or a cheer for a part or for progress); after hour 73 only, or a visitor's report, 42; an early marking, 3 (re-ruled under reading 1 as corrected); the bound's second sentence, 1 (catholicism-053). Two more lines are NONPORTABLE (btc-037, costa_rica-037) and are particulars by G6.

**Absent lines.** One line is evidenced: pebble-049, `not-needed`, a specification. It shows a build report, then the close cutting the work and a tally mourned, with no marking. 36 claims of absence fail, because a concept shows a report of the room's build and, after it, a marking of the work. In 6 of them a plain report is answered by a marking (Slovakia, colombia, ethereum, malta, anime_irl, russia). The other 139 lines are evidence limits. A guard listed 46 limits whose labels name a finish or 'did it'. Each was read again, and none moved.

**Repairs (G7).** Lines in repaired rooms were 0.493 accepted (373 lines), and in unrepaired rooms 0.530 (300 lines). No ruling rests on the difference.

**Carried to later groups.**
- **A07's reach.** The order holds in 131 of 156 episode rooms, but one act holds both ends in 189 rooms with no order or bound. D3c weighs this with the spine's links, since A07's count and strength rest on concepts that the return reads as one act.
- **The mechanism in words.** In 24 rooms a plain report is answered by a marking. D3c reads this beside A05's and A06's mechanisms in words.
- **The early marking.** 15 rooms mark the work and then report it unfinished. It goes with P15's edge with P11 and P03, carried since D3a-13.
- **The family** (7 rooms, 7 paired elaborations) joins D3a-13's family for the clustering at D4.
- **The canvas's worth argued beside a marking** (P20, 3 restrict lines) goes with P20's forms.
- **The re-check (§5).** A07 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 807 quoted concepts in fifteen windows; restrict 296; absent 120 in three batches; add and contradict 18.
- **Reading 1 corrected.** I first read a build report that comes after the first marking under the bound's first sentence, and three instantiate lines were written on that reading. Before any restrict line was written, I saw that it widened the bound beyond its words (QD3-007). The correction is dated under G39, and three re-rulings are appended.
- **Two refused commands.** Twice the permission check refused a command because `cut -c` sat in a command with a helper or `mem.py`: once at the opening check of G39, and once at a check of earlier add rulings. Nothing ran either time, and each was run again without the clip.
- **A sum made by hand.** The 555 quoted segments of the instantiate spec were first summed by hand from four outputs, then confirmed by one run on the joined spec.
- **A first join.** The first joined restrict spec lacked singapore-047 (104 rows). It is kept as `A07-restrict-spec.txt`, and the full spec is `A07-restrict-spec-105.txt`.
- **A note's wording.** The note that logged the add classes said that the 12 other specifications all name P11. Two do not: touhou-049 names P02 alone, and babymetal-051 names A03 and P05. A later note corrects the wording, and no ruling changed.
- **Reclassifications inside the leg.** Reading 3 moved australia-059 from J to one end and 2007scape-054 from J to the order, before any line was written.

### Close-check, D3a-34

`validate.py D3` reports 28,100 of 42,243 ledger lines ruled: the 27,427 before this leg and A07's 673. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 28,860 lines: 673 first rulings and 3 re-rulings from this leg. Appended re-rulings now stand at 760.
- **Pairs.** A07's files hold 7 pairs, all naming A07 lines (`d3_pair_check.py`). Across the ledger, 1,243 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-35: A08, the marking before the record

A08 is a standing arrow from C2, P11 → P12, of kind order and strength strong. Its connection reads: 'in a room carrying both, the first marking of the finished work comes before the first record of what happened to it'. Its mechanism says that marking the work together turns the room toward keeping it: members ask for the final image, the timelapse, the list of what changed. Its bound names records that come first on the late side, a screenshot of a work found rather than built. Its counterexample response names 64 of 289 rooms that record before they celebrate, as a scope condition. C2 counted the order in 225 of 289 rooms (0.779; null mean 0.565, p95 0.609). No finding touches A08. G40 was written before any line was read, and its readings are written under it (above). All 683 lines, in 679 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a08_census.py`, `d3_spec_cover.py` and `d3_pair_check.py`. The quotes in the rulings were checked against `cite.py`'s output by `d3_spec_quotes.py`.

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 58 | 21 | 0 | 0 | 0 | 2 | 35 |
| absent (322 `not-testable`, 53 `unobserved`) | 375 | 0 | 0 | 0 | 247 | 2 | 126 |
| restrict | 235 | 141 | 4 | 0 | 88 | 2 | 0 |
| add-condition | 12 | 8 | 0 | 0 | 4 | 0 | 0 |
| add-step | 3 | 0 | 0 | 0 | 3 | 0 | 0 |
| all | 683 | 170 | 4 | 0 | 342 | 6 | 161 |

**What the rooms show (the census, `d3_a08_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision and kind written.
- **The order, 232 rooms.** A marking of the room's work comes first, and a record of what happened to it follows ('Place 2017, we did it guys. Good work.', then 'Time-lapse of our logo being built was pretty awesome.', lakers, a room the arrow names). In 28 rooms the record is asked for, saved or given in reply to the marking, the mechanism in words ('Wow nice job guys.', answered by 'Final image:', halo).
- **The bound, 3 rooms.** The first record is a screenshot of a work the room found ('Found on /r/place', then 'I'm happy we managed even a small one. High five guys!', borderlands).
- No room shows both. So 235 rooms show an episode, and the order holds in 232 (0.987). C2's share was 0.779 over 289 rooms.
- **Record first, 5 rooms with no order or bound.** The room's standing work is recorded before the room first marks it ('It's been destroyed', then 'IT'S BACK, NO FLAG WILL PAVE OVER US', neutralmilkhotel). A08's counterexample response states this case. With these rooms, the order holds in 232 of 240 (0.967).
- **One act holding both ends, 30 rooms with no order, bound or record first.** The room's first marking is itself a record of the work's fate ('One brave white bear logo has survived until the end of place', blackmirror). With these rooms too, the order holds in 232 of 270 (0.859). One-act lines among the restrict and absent lines are evidence limits and are not counted here, so 30 is a floor.
- **Other classes.** An early record of an unfinished or another work shows in 36 rooms ('If we can do it fast enough we can maybe get a good screenshot of it at least.', OnePiece). An attempt the close cut is marked in 7 rooms (A07's bound), and D3a-13's family shows in 4.
- **Why the shares differ.** Most of the order rooms come from absent lines. The labelers marked them `not-testable` because the concepts do not show that the marking caused the record. A08 claims an order, not a cause, and in 126 of these lines a marking comes before a record ('My fellow knights, Mission Accomplished!', then 'Screenshot of our logo and The Button in mint condition', AprilKnights). The share is higher than C2's for the same reason as A07's: C2 counted the first concept of each element, and a survival claim counts for both at one hour, while the return reads it as one act.

**No correction (§2).** No restrict line is an accepted correction. Of the 235 restrict lines, 141 are specifications, 88 are evidence limits, 4 are paired elaborations and 2 are NONPORTABLE particulars (dbz-052, formula1-045). By class: the order 65; held by another statement 49; the mechanism in words 19; record first, held by A08's counterexample response, 5; the bound 3. Of the 49 held lines, 41 name P12's statement. 31 of these are early records: records made while the work was built, of the canvas during the event, or of other works lost before the marked one. 8 name A07's bound, an attempt the close cut. Others name P03 (state images during the build, 4), P10 (3), P11 (3, for credit disputes and the room's word), P22 (3, a cleanup asked or an account corrected after hour 73), P05 and P13 (2 each), and P01, P02 and P09 (1 each). The 88 evidence limits mostly show one act holding a marking and a record: a survival claim, or a final image posted as done. The 4 elaborations are D3a-13's family. The record-first lines are held by A08's own counterexample response (reading 7), and five more lines whose concepts showed a record first had an earlier marking in a ruled line (reading 8). Of the 15 add lines, 8 are specifications: 5 early records held by P12 (GrowTheTree, danganronpa, dwarffortress, newzealand, uofm), 2 records of loss and of the close held by P12 (naruto, stardewvalley), and A08's own mechanism in one post (rhythmheaven). 7 are counting rules whose concepts show one act (evidence limits). A08 stands as served, with no move.

**What the instantiate lines show.** Accepted 21: the order by the hours or a reply, 13; the mechanism in words, 8. Rejected 35: one act holding both ends, 11; the same with a record asked for or given later, 19; one end, 4; another room's work, 1 (madokamagica-038). Two more lines are NONPORTABLE (fullcommunism-039, zelda-058) and are particulars by G6.

**Absent lines.** No line is evidenced. 126 claims of absence fail, because a concept shows a marking of the room's work and, after it, a record of what happened to it. In two of them a later edit of the same post adds the record (redpandas, signal), and in one the post gives its image after the cheer (vegan). Two lines are NONPORTABLE (aromantic-045, farmcarrots-046) and are particulars. The other 247 are evidence limits. A guard listed 42 limits whose labels name a timelapse, a screenshot, a final image or an archive. Each was read again, and none moved.

**Repairs (G7).** Lines in repaired rooms were 0.728 accepted (372 lines), and in unrepaired rooms 0.788 (311 lines). No ruling rests on the difference.

**Carried to later groups.**
- **A08's reach.** The order holds where it can be read, but one act at the close holds both ends in at least 30 rooms. D3c weighs this with A07's one-act rooms, since both arrows meet at the same posts.
- **Record first.** 5 rooms record the standing work before they mark it. D3c reads them with A08's counterexample response, one of the fields the prose rule did not read.
- **The mechanism in words.** In 28 rooms a record is asked for or given in reply to a marking. D3c reads this beside A05's, A06's and A07's mechanisms in words.
- **Early records** (36 rooms, records made while the work was built) go with P12's and P03's lines, and with direct information sharing.
- **The family** (4 rooms, 4 paired elaborations) joins D3a-13's family for the clustering at D4. **Attempt markings** (7 rooms) go with A07's bound.
- **The re-check (§5).** A08 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 144 quoted concepts in two windows; restrict 645 in nine windows; absent 309 in four batches; add 9.
- **The draw's offset.** G40 first named verb offset 390. The draw and two windows made there held 57 instantiate lines and one add-step line, because the verb's first line is its header. The sentence was corrected to 391 before any line was read, and the files at 390 are kept as superseded.
- **A no-op in a command.** One check command began with a shell variable assignment (a word beginning 'for_'). It did nothing and the permission check let it run, but it broke the rules against placeholders, no-ops and shell variables in commands.
- **The earlier-marking check.** Reading 8 was applied only to lines whose own concepts showed a record first. Lines that show one act were not checked against earlier markings in other lines, so the joint count is read from each line's own concepts.
- **Reclassification inside the leg.** Reading 9 moved bostonbruins-049 from one act to the mechanism in one post, before any line was written.

### Close-check, D3a-35

`validate.py D3` reports 28,783 of 42,243 ledger lines ruled: the 28,100 before this leg and A08's 683. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 29,543 lines: 683 first rulings from this leg and no re-ruling. Appended re-rulings stay at 760.
- **Pairs.** A08's files hold 4 pairs, all naming A08 lines (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-36: A09, the record before carrying on

A09 is a standing arrow from C2, P12 → P13, of kind order and strength fair. Its connection reads: 'in a room carrying both, the first record of what happened comes before the first act of carrying the work on'. Its mechanism says that a record of the work gives the room something to carry: the image into the banner, the plan into the next canvas. Its bound names rooms that planned their next canvas or emblem while still building. Its counterexample response names texans, which carries the work on at h34.5 and records at h73.2, and 32 of 145 rooms that run this way, as a scope condition. C2 counted the order in 113 of 145 rooms (0.779; null mean 0.563, p95 0.628). No finding names A09. G41 was written before any line was read, and its readings are written under it (above). All 684 lines, in 678 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a09_census.py`, `d3_spec_cover.py` and `d3_pair_check.py`. The quotes in the rulings were checked against `cite.py`'s output by `d3_spec_quotes.py`, and the typed hours by a new helper, `d3_spec_hours.py`.

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 35 | 21 | 0 | 0 | 0 | 1 | 13 |
| absent (325 `not-testable`, 232 `unobserved`) | 557 | 0 | 0 | 0 | 456 | 4 | 97 |
| restrict | 88 | 68 | 0 | 0 | 20 | 0 | 0 |
| add-condition | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| all | 684 | 93 | 0 | 0 | 476 | 5 | 110 |

**What the rooms show (the census, `d3_a09_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision and kind written.
- **The order, 163 rooms.** A record of what happened to the room's work comes first, and an act of carrying the work on follows ('Final Image: https://i.imgur.com/IJf9XLP.png', then 'The design will be the same as in Place. Come join me if you're interested!', titanfall). In 26 rooms the recorded work itself is carried in reply, in its thread or in one post, the mechanism in words ('Place has ended! Here's what we ended with for /r/RotMG', then 'Well anyway here's the sprite (taken from the /r/place thread)', rotmg).
- **The bound, 10 rooms.** A later canvas or the emblem is planned or made while the room builds, before any record ('Flair please: http://imgur.com/a/ivY7G' at h+34.50, texans, the room the counterexample response names).
- No room shows both. So 173 rooms show an episode, and the order holds in 163 (0.942). C2's share was 0.779 over 145 rooms.
- **Carry first, 11 rooms with no order or bound.** An act of carrying on comes before the room's first record. In Temple a member turns the place Discord into the sub's server at h+74.51, and the room's first record comes at h+74.68. A09's counterexample response states this case. With these rooms, the order holds in 163 of 184 (0.886). In 5 carry-first lines the act comes before hour 61: a remake, a profile picture or a tie (D3a-20's forms).
- **One act holding both ends, 4 rooms with no order, bound or carry first** ('if anyone can take the final canvas and fix up ubc I would love a high quality image of everything to make a poster or something', ubc). With these rooms too, the order holds in 163 of 188 (0.867). One-act lines among the restrict and absent lines are evidence limits and are not counted here, so 4 is a floor.
- **One room shows both the order and carry first.** miamidolphins' instantiate line shows a record and then the sidebar at the close. Its add-condition line shows a remake in Minecraft at h+33.29, before any record. Read by first acts, the room carries on first, and the share becomes 162 of 184 (0.880). The priority rule counts it as the order.
- **Why the shares differ.** 97 of the 163 order rooms rest on absent lines alone, and 66 on instantiate or restrict lines. The labelers marked those absent lines `not-testable` or `unobserved` because the concepts do not show that the record caused the carrying on. A09 claims an order, not a cause, and in each of the 97 a record comes before an act of carrying on ('Final Product of the Mona Lisa', then 'Create Mona Lisa at the new Space!', monalisaclan).
- **A one-way check.** Reading 1 checks the lines that show carrying on first against the room's earlier records. No line that shows the order is checked against an earlier act of carrying on in the room's other lines. miamidolphins was found only because its own add line showed the earlier act. So the shares may be high. A08's census has the same asymmetry under G40's reading 8.

**No correction (§2).** No line is an accepted correction. Of the 88 restrict lines, 68 are specifications and 20 are evidence limits. By class: the order 36, 13 of them by the room's earlier record; the mechanism in words 10, 3 of them by the room's earlier record; carry first, held by A09's counterexample response, 11; the bound 9; held by P13 where the record and the carrying on are one act, 2. Most conditions say that the record is not shown to cause the carrying on. A09 orders first acts and claims no cause, so its connection holds them. Others say that carrying on can begin before the close, on a parallel canvas, in an emblem, a tie or a remake. The bound and the counterexample response hold them. The 20 evidence limits show carrying on alone after the close, a record alone, one act, or ties with no record of the room's work. The falsifier's second clause, a recorded work carried nowhere, shows only as one end (vinesauce, stargate). The 4 add lines are specifications: play as a reason to carry on (K01 and P13, esperanto), a work corrected when carried (P05 and P13, furry_irl), a remake before any record (carry first, miamidolphins), and a sidebar promised while building (the bound, reddevils). A09 stands as served, with no move.

**What the instantiate lines show.** Accepted 21: the order by the hours, a reply or one post, 5, two of them by the room's earlier record (2007scape, and pitt after its re-ruling); the mechanism in words, 16. Rejected 13: one act, 6; one end, 7. One line is NONPORTABLE (minecraft-053) and is a particular by G6.

**Absent lines.** No line is evidenced. 97 claims of absence fail, because the line's first record comes before its first act of carrying on. 3 of these are NONPORTABLE lines whose concepts show the order (Moondye7, babymetal, survivor). 4 NONPORTABLE lines show no order and are particulars (nightinthewoods, runescape, southpark, vietnam). The other 456 are evidence limits. A guard listed 82 limits whose labels name a later canvas, a banner, a chat or next time. Six were read again, and two moved to reject (CelticFc-042, ftlgame-058).

**Repairs (G7).** Lines in repaired rooms were 0.813 accepted (374 lines), and in unrepaired rooms 0.855 (310 lines). No ruling rests on the difference.

**Carried to later groups.**
- **A09's reach.** The order holds where it can be read. 21 rooms carry on first: 10 by the bound and 11 by the case the counterexample response states. D3c reads them with that field.
- **A two-way check.** For the order rooms of A07, A08 and A09, D3c checks the room's other lines for an earlier act of the arrow's second end.
- **The mechanism in words** (26 rooms) goes to D3c beside A05's to A08's.
- **D3a-20's forms** (5 carry-first lines before hour 61) join D3a-20's family for the clustering at D4.
- **The re-check (§5).** A09 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 76 quoted concepts in one window; restrict 249 in three windows (83, 95, 71); absent 368 in seven batches; add 10; earlier records 16, from four runs of `d3_a09_cross.py`.
- **Two instantiate lines re-ruled.** pitt-039 was ruled the bound before reading 1's check was applied to it. The check finds pitt-013's retelling at h+54.21 before the emblem at h+56.33, so the line is re-ruled to the order. DestinyTheGame-052 was classed as one end, but its two concepts are one post (cleaned images and flairs), so it is re-ruled as one act. Both re-rulings are appended lines.
- **Counts typed from my tally.** Three sub-counts in log notes came from my tally: 15 order lines by the room's earlier record (13), 5 carry-first acts before the close (6), and 149 absent candidates (151). Each was corrected by a later note before any write.
- **A refused command.** One dry-run command piped its output through `cut -c`, which the permission check refuses after a helper. It ran nothing, and it was run again without the cut.
- **A stopped chain.** At the restrict windows, `grep -c` returned 0 and stopped an `&&` chain before the first window. The window was made by the next command.
- **Superseded files.** Two absent rulings files were rebuilt before any write and kept: one from before the guard's second look, and one whose limit clause said that no record was followed by carrying on. That clause was not true of several carry-first lines (brasil, cirkeltrek, factorio).

### Close-check, D3a-36

`validate.py D3` reports 29,467 of 42,243 ledger lines ruled: the 28,783 before this leg and A09's 684. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 30,229 lines: 684 first rulings from this leg and 2 re-rulings. Appended re-rulings are now 762.
- **Pairs.** A09's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-37: A10, the doubt before the move

A10 is a standing arrow from C2, K02 → P10, of kind order and strength thin. Its connection reads: 'in a room carrying both, the first doubt about the room's numbers or room comes before the first move after a loss'. Its mechanism: 'A room that judges it has too few hands to hold its spot stops fighting for it and moves.' Its bound names early moves by choice, a late room (guatemala) and a room moved by a coalition's plan (MiamiHurricanes). It ends: 'After doubt and a loss, a room moves or gives the work up; the arrow holds for those that move (F-019).' Its counterexample response names anarcho_capitalism, which moves at h9.0 and voices doubt at h32.9, as a scope condition. C2 counted the order in 11 of 21 rooms (0.524; null mean 0.298, p95 0.429), and the C5c read found the judgment first in 10 of 20. G42 was written before any line was read, and its amendment and readings are written under it (above). All 677 lines, in 673 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a10_census.py`, `d3_a10_notes_counts.py`, `d3_spec_cover.py` and `d3_pair_check.py`. Quotes were checked against `cite.py`'s output by `d3_spec_quotes.py`, and typed hours by `d3_spec_hours.py`. The room's earlier doubts and moves were read with a new helper, `d3_a10_cross.py`, in 24 runs, and the rulings of a room's K02 and P10 lines with `d3_a10_room_lines.py`.

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 37 | 23 | 0 | 0 | 0 | 0 | 14 |
| absent (301 `not-testable`, 66 `unobserved`, 5 `not-needed`) | 372 | 5 | 0 | 0 | 333 | 17 | 17 |
| restrict | 252 | 241 | 0 | 0 | 9 | 2 | 0 |
| add-condition | 15 | 15 | 0 | 0 | 0 | 0 | 0 |
| contradict | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| all | 677 | 285 | 0 | 0 | 342 | 19 | 31 |

**What the rooms show (the census, `d3_a10_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision and kind written.
- **The order, 112 rooms.** The room's first doubt about its numbers or room comes first, and its first move after a loss follows ('If we expand too much, we will get overtaken because we are not many.' at h+26.09, then 'our flag got deleted next to the goose, so let's start fresh at this spot that seems empty' at h+67.33, costa_rica). The order lines come from instantiate lines in 22 rooms, restrict lines in 73 and absent lines in 17. In 25 rooms one post or a reply judges first and moves after, the mechanism in words ('I wanted to keep fighting for the spot we've had, but it looks like this is a losing battle. I'll help move it if we can decide on where.', day9).
- **Move first, 46 rooms.** The room's first move after a loss comes before its first doubt ('Void took it over so we're finding a new spot/potentially a new art to do.' at h+38.15, then 'Guess we're a little too small to make this work, couldn't build fast enough.' at h+54.27, paranatural, A10's own support room, as C2's audit found). A10's bound and counterexample response state this case.
- **The bound, 1 room** (MiamiHurricanes, moved by a coalition's plan).
- So 159 rooms order both ends, and the order holds in 112 (0.704). With the 6 rooms whose first doubt and first move are one act, it holds in 112 of 165 (0.679).
- **One room shows both the order and move first.** bangladesh's instantiate line judges first and moves after in one post (c0017, h+58.95). Its restrict line shows a fresh start at h+57.19 (c0016), before that doubt. Read by first acts, the room moves first, and the census counts it so. The instantiate ruling stands, since its post does judge first. The two-way check reads K02's and P10's lines, so it could not see a move cited only in another A10 line.
- **After doubt.** Of 217 rooms whose lines show doubt and then a move, giving up or no move, 165 moved (0.760), 12 gave the work up and 40 did not move. F-019 counted 10 moved of 36 rooms with doubt and a loss. The two counts read different populations. A10's lines were written where the labelers saw the arrow's two elements, so rooms that moved are over-represented. F-019 read every room that voiced doubt and whose record says the work was lost. Neither count replaces the other.
- **Move only, 2 rooms** (indonesia, parrots). They move after a loss with no doubt of their own and no accepted K02 line, so they do not carry both.
- **Why the share is higher than C2's.** C2 read 21 rooms that carry both elements by their codes. This census reads 159 rooms whose ruled lines order both ends, with the two-way check across each room's ruled K02 and P10 lines. At least 22 restrict order lines and at least 21 restrict move-first lines take the room's first act from another line. In 17 rooms the absent line's own concepts show the order, though the labelers marked them `not-testable` or `unobserved`, because the concepts do not show that the doubt caused the move. A10 claims an order, not a cause.

**No correction (§2).** No line is an accepted correction. Of the 252 restrict lines, 241 are specifications, 9 are evidence limits and 2 are particulars by portability. By class: the order 61; the mechanism in words 12; move first 42, held by the bound and the counterexample response; move only 2; the bound 1; gave up 12, held by the bound's last sentence and F-019 ('Sadly though not enough help has come and the project will have to be abundance.', shield); no move 39, the falsifier's second clause, which the arrow records as present and the bound holds ('we don't have enough people to stop them. But we can keep our logo at 170,535.', sixers); held by another statement 72; evidence limits 9. Most conditions say that too few hands do not by themselves make a room move: the room may defend, recruit, shrink the design, negotiate or give up, or a move may need a site, consent or terms. A10 orders first acts and names no sole cause, and its bound holds the rooms that do not move. K02 and P02 hold doubt with no loss, P04 a site chosen before any loss, P07 and P08 moves to spare or by terms, P05 keeping, P16 and P17 help and allies, and P13 and P22 acts after the close. The 16 add and contradict lines are specifications on the same statements. The contradict line (bakchodi-058) says that a room which knows it is outnumbered fights on. A10 already states that as its mechanism's failure, so A10 does not fail. A10 stands as served, with no move.

**What the instantiate lines show.** Accepted 23: the order 9, 6 of them by the room's earlier doubt in a K02 line; the mechanism in words 14. Rejected 14: move first 5, 4 of them by the room's earlier move in a P10 line; one act 6; a move that is not P10's 3, pushes given up as G22 reads them.

**Absent lines.** 17 claims of absence fail, because the line's first doubt comes before its first move after a loss. One of them, uruguay-036, is NONPORTABLE but shows the order, as A09's Moondye7-047 did. The 5 `not-needed` lines are specifications: doubt with no loss (mit), moves to spare or at a neighbour's request (neopets, strangerthings, truestl), and a restart sought after the close (stlouis). 17 NONPORTABLE lines show no order and are particulars. The other 333 are evidence limits. Candidates stayed limits where the room moved first or where P10's rulings found no move after a loss; the log names each. A guard listed 48 limits whose labels name too few hands or being outnumbered. Each had been read in the packet pass, and two were read again (miamidolphins and mysterydungeon, both a planned site changed before any loss).

**Repairs (G7).** Lines in repaired rooms were 0.927 accepted (370 lines), and in unrepaired rooms 0.925 (307 lines). No ruling rests on the difference.

**Carried to later groups.**
- **A10's reach.** The order holds where both ends can be read, in 112 of 159 rooms. 46 rooms move first, the case the bound and the counterexample response state. D3c reads them with those fields.
- **After doubt.** 40 rooms do not move and 12 give up. D3c reads them beside F-019, whose population differs.
- **A two-way check across A10's own lines.** The check reads K02's and P10's ruled lines. A move or doubt cited only in another A10 line was found once (bangladesh), by the census. D3c applies the same check to the order rooms of A07 to A09.
- **The mechanism in words** (25 rooms) goes to D3c beside A05's to A09's.
- **P10's and K02's readings.** The A10 rulings followed P10's rulings on pushes, planned sites and moves by terms, room by room, and found no conflict with them.
- **The re-check (§5).** A10 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 68 quoted segments and 78 hours; restrict 532 segments and 649 hours, in nine windows; add and contradict 42 hours, in paraphrase; absent 48 segments and 52 hours, from four batches of cited candidates.
- **Reading 9 decides one line.** wow-053 shows the order only because a lament that the work is absent counts as K02's judgment. Read as stated hands only, the census would count one order room fewer.
- **A count typed from my tally.** The note on amendment 1 called the order lines with an earlier doubt 'five'. They are eight, and a correction note named them before any write.
- **Spec rows changed before any write.** asexual-040 moved from one act to no move when reading 8 was refined. ice_poseidon-021's evidence was corrected to a move of hands to another work, with its class unchanged. Six rows listed two hours after two concepts, which the hour check reads as one hour for the second concept; each hour was placed after its own concept. 53 quotes typed in double quotes were turned to single quotes, so that the quote check reads them; all were found.
- **Refused or failed commands.** One `grep` piped through `cut -c` was refused by the permission check and ran nothing. Two `grep` commands with a repetition count over 255 failed and ran nothing. Each was run again in another form.
- **A compaction** came after the check for restrict lines 180 to 209 was logged and before their spec part was written. The head and the stage file were read again, and a note logged the reconciliation, before any other write.

### Close-check, D3a-37

`validate.py D3` reports 30,144 of 42,243 ledger lines ruled: the 29,467 before this leg and A10's 677. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 30,906 lines: 677 first rulings from this leg and no re-ruling. Appended re-rulings stay 762.
- **Pairs.** A10's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-38: A11, the template after the talk

A11 is a standing arrow from C2, P02 → P04, of kind transition and strength thin. It is the first arrow of that kind to be ruled. Its mechanism: 'Design talk in a thread is settled by someone posting a template that lays out the agreed design pixel by pixel.' Its failure clause, which the arrow records as present: 'Templates are revised in threads with no design talk before them, or design talk ends with no template'. Its bound keeps it inside reply threads and names template first across rooms (texas). Its counterexample response withdraws the order claim. C2 grounded it on 82 transitions in 36 rooms, and the room-level order was not beaten (111 of 185, 0.600; null mean 0.618, p95 0.670). G43 was written before any line was read, and its four readings are written under it (above). All 678 lines, in 674 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a11_census2.py`, `d3_a11_notes_counts.py`, `d3_spec_cover.py` and `d3_pair_check.py`. Quotes were checked against `cite.py`'s output by `d3_spec_quotes.py`, and typed hours by `d3_spec_hours.py`. The reply structure of every transition line was read with `d3_a11_reply_check4.py` and the forests.

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 18 | 13 | 0 | 0 | 0 | 1 | 4 |
| absent (249 `not-testable`, 73 `unobserved`) | 322 | 0 | 0 | 0 | 295 | 1 | 26 |
| restrict | 331 | 305 | 0 | 0 | 25 | 1 | 0 |
| add-condition | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| add-step | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| all | 678 | 325 | 0 | 0 | 320 | 3 | 30 |

**What the rooms show (the census, `d3_a11_census2.py`).** Its rules were logged before the first run. Each line keeps the class it was ruled under, or the class of its re-ruling, and the helper checks every class against the decision and kind written. Run 2 supersedes run 1, since one line moved (below).
- **The transition, 111 rooms.** Design talk is answered in its thread by a later layout, coordinates, a pointer to the layout or a request for one ('let's build the atomium on the top:' at h+66.18, then 'HERE IS THE ATOMIUM DRAWING' at h+66.19, belgium). The 112 transition lines come from 13 instantiate lines, 72 restrict lines, 1 add line and 26 absent lines. In 64 of the rooms (0.577) a posted layout answers the talk, the mechanism in words. In the others the answer is coordinates, a pointer or a promised layout ('we should build Captain's shield in /r/place' at h+5.61, then 'Location: (300, 625)' at h+5.66, marvel).
- **Template first, 98 more rooms.** A layout comes before any design talk, and the later talk gets no revised layout ('I have made a template of the artwork:' at h+37.96, then 'IT NEEDS TO BE BIGGER' at h+68.19, 4chan). A11's bound and counterexample response state this case. One room shows both the transition and template first. A11 allows this, since it claims no order between rooms.
- **Across threads, 19 more rooms.** The talk stands in one thread and the layout in another ('I really want the border to be red.' at h+15.16; 'If you want to make changes, make sure the reference image is updated.' at h+47.42 in another thread, babymetal). The bound holds them.
- So 228 rooms show both ends, and the transition shows in 111 of them (0.487). With the 21 rooms where one post holds both ends and no other episode shows (Dominican's proposal with its 'Template:' link), it shows in 111 of 249 (0.446).
- **The failure clause's cases, alone.** 31 rooms show talk only ('I'm still trying to figure out what colors to use for his arm. Any ideas?', HomestarRunner, answered by a division of the work and no layout). 86 rooms show a layout only, with no design talk before it ('I keep seeing two templates', AmericanFlaginPlace). The arrow records this failure as present.
- **Beside C2.** C2 counted 82 transitions in 36 rooms. The transition shows here in about three times as many rooms, because the census reads the ruled lines of 674 rooms and the absent lines' own concepts. C2's room-level order was not beaten. Here template first is nearly as common as the transition among rooms that show both ends (98 against 111). The bound and the counterexample response already state that case, so A11's claim stays a transition inside threads. The 111 transition rooms and C2's 111 of 185 ordered rooms count different things, and the numbers match by chance.

**No correction (§2).** No line is an accepted correction. Of the 331 restrict lines, 305 are specifications, 25 are evidence limits (21 one post, 4 told only after the close) and 1 is a particular by portability (giivasunner-041). By class: the transition in words 46, through P04's other forms 26, template first 97, across threads 19, talk only 31, layout only 86. 282 of the 331 lines name settling in their 'how' line (a search for 'settl'). The condition they state is that a template does not settle the design for good: rival templates, polls, later redesigns, and placers who deviate or revert. G43 reading 3 holds it by P02's range, P04's range, P05's statement and pass 7's amendment. The 7 add lines are specifications: one transition (partyparrot-060), one template first (ScottPilgrim), and five held by P04's range, P14, P05, P07 and P08. A11 stands as served, with no move. Whether the mechanism's word 'settled' should be restated is asked of J (QD3-008).

**What the instantiate lines show.** Accepted 13: the mechanism in words 8, P04's other forms 5. Rejected 4: one end 3, where a request for a layout is answered by a layout (Rainbow6, npr, maryland); template first 1 (cfb-048). Particular 1 (superman-009, NONPORTABLE).

**Absent lines.** 26 claims of absence fail, because design talk is answered in its thread by a later P04 concept: 10 by a layout, the mechanism in words, and 16 by P04's other forms. One NONPORTABLE line, whose ends stand in different threads, is a particular (TransFlagPlace-047). The other 295 are evidence limits. No line is `observed-absent` or `not-needed`. Candidates stayed limits where the two ends stand in different threads or in one post, or where a later layout does not answer the talk. A guard listed 60 limits whose labels name a template, blueprint or mock-up, and each had been read in the packet pass.

**Who answers (G43 reading 4).** The first check of the reply structure passed a line when any two of its concepts were reply-linked. So it passed lines whose layout answered another post. Version 4 of the check finds each ruling's answer in the ruling's own words. It lists 37 of the 112 transition lines with no direct reply link. Read in the forests, 24 of them are linked as G43 says: a top-level reply to a submission that holds the talk, a layout by the member who voiced the talk, or a post in the submission's reply chain. 7 more stand by reading 4: two in the same exchange (evex, twitch), two by the member the talk addressed or the template's maker (nerf, Okami), and three by naming the talked design or giving what the talk asked for (chicago, PlaceNL, dallasstars). 6 are re-ruled by appended lines. drugs, raocow, reddevils and japan keep the transition, with the talk and the answer corrected. habs moves to talk only, since its pointer to the template ('If you want to see the template, check out the discord:') answers a charge of vandalism in another branch. foxstevenson's absent line stays a reject, with the submission as the talk answered. No decision or kind changes, and one census class does.

**Repairs (G7).** Lines in repaired rooms were 0.949 accepted (372 lines), and in unrepaired rooms 0.954 (306 lines). No ruling rests on the difference.

**Carried to later groups.**
- **QD3-008.** The word 'settled' in A11's mechanism, with the 282 restrict lines that name settling, goes to J and to D3c.
- **A11's reach.** The transition shows in 111 of 228 rooms that show both ends, and template first in 98. D3c reads them with the bound and the counterexample response.
- **The failure clause.** Talk only (31 rooms) and layout only (86) go to D3c with the failure clause, which the arrow records as present.
- **Reading 4 for later transitions.** A later arrow of kind transition applies reading 4 and the reply check from its first ruling.
- **F-017** is not re-examined, since A11 is not revised.
- **The re-check (§5).** A11 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 37 quoted segments and 44 hours; restrict 548 segments and 1,027 hours, in thirteen windows; add lines 22 hours, in paraphrase; absent 55 segments and 58 hours, from four batches of cited candidates; re-rulings 21 segments and 27 hours.
- **Reading 4 came late.** It was written at the close, from the rulings, and its text first said that every ruling it touches applied it alike. That was false. The check above found six rulings that did not, and the text is amended.
- **The check's own slips.** Its second and third versions misread code labels, and the third once took a quote ('Short answer', cardinals) for the ruling's answer. They flagged lines wrongly and wrote nothing. Version 4 is the one kept.
- **Spec rows changed before any write.** texas-042's c0062 is coded as posting a template, but its quote shows no link, so the line moved from template first to the transition. A check of every other row's code labels then flagged 8 rows, and none changed. Three restrict rows listed two hours after two concepts, and each hour was placed after its own concept.
- **A refused command.** After the compaction, one command piped a hash through `cut -c`. The permission check refused it, and it ran nothing. It was run again without the cut.
- **A compaction** came during the reading-4 check, after its second version ran and before any re-ruling was written. The head and the stage file were read again, and a note logged the reconciliation before any other write.

### Close-check, D3a-38

`validate.py D3` reports 30,822 of 42,243 ledger lines ruled: the 30,144 before this leg and A11's 678. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 31,590 lines: 678 first rulings and 6 re-rulings from this leg. Appended re-rulings are now 768.
- **Pairs.** A11's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** QD3-008 is open. Meanwhile A11's mechanism stays unchanged, and its lines are ruled as specifications held by G43 reading 3. (Added at D3a-39: J chose option 2, as the assumption said, so no ruling here changes; see G43 reading 3.)

## D3a-39: A12, the bare answer to a call

A12 is a standing arrow from C2, P01 → P15, of kind transition and strength thin. It is the second arrow of that kind to be ruled. Its gloss: 'the cheapest answer to a call'. Its mechanism comes from conversation analysis: a call makes an answer due, joining is the preferred answer and comes bare, and declining comes with a reason. It fails if 'The one-line pledges in a room answer no call, or every answer to a call is long and conditional.' It also fails if joins give reasons as often as refusals do, or if refusals come as bare as joins. The arrow marks that failure 'not-addressed', since the reason test ran on attack calls only. Its bound begins 'Never counted as an order.' and holds F-023: acceptances of calls to place were bare in 25 of 31. G44 was written before any line was read, and its eight readings are written under it (above). All 747 lines, in 692 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a12_census2.py`, `d3_a12_class_counts.py`, `d3_spec_cover.py` and `d3_pair_check.py`. Quotes were checked against `cite.py`'s output by `d3_spec_quotes.py`, and typed hours by `d3_spec_hours.py`. Every line was read with its reply context (`d3_reply_context.py`, through `d3_read_window.py`).

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 377 | 333 | 0 | 0 | 0 | 0 | 44 |
| absent (124 `not-testable`, 37 `unobserved`, 1 `observed-absent`) | 162 | 1 | 0 | 0 | 151 | 0 | 10 |
| restrict | 181 | 171 | 0 | 0 | 10 | 0 | 0 |
| add-condition | 21 | 19 | 0 | 0 | 2 | 0 | 0 |
| add-step | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| all | 747 | 530 | 0 | 0 | 163 | 0 | 54 |

**What the rooms show (the census, `d3_a12_census2.py`).** Its rules were logged before the first run. Each line keeps the class it was ruled under, or the class of its re-ruling, and the helper checks every class against the decision and kind written. Run 2 supersedes run 1, since one line moved (below). These are counts of the lines labelers wrote where they saw both ends. They are not rates in the population.
- **The pair, 430 rooms.** A call is answered in its thread by another member's written join, part done or thanks ('Make it happen.' at h+3.60, then 'Got it boss' at h+3.62, 4chan). The 454 pair lines come from 333 instantiate lines, 102 restrict lines, 9 add lines and 10 absent lines. 63 of them name the call from the room's record.
- **The bare join, the mechanism in words.** Among pair lines whose strongest answer is a join, 392 of 411 are bare (0.954). F-023 found 25 of 31. 371 rooms show a bare join (0.863 of the pair rooms). 19 joins give a reason ('ME. I need Isabelle.' at h+41.26, animalcrossing). 37 lines show a part done or thanks, and 6 absent lines show a join that is not graded.
- **The dispreferred answer.** 32 lines show a refusal with a reason ('We don't have enough forces to divert our efforts.' at h+8.79, GreenCorner). 30 lines show a bare refusal or a hostile reply ('Not your personal army.' at h+50.76, anime). 4 lines show both. Each kind shows in 30 rooms.
- **A conditional or asking answer.** 59 lines show a join with a condition or a question back ('Yes but we need numbers.' at h+40.75, 49ers). In 24 lines, in 24 rooms, it is the only answer, and reading 7 does not count it as the pair.
- **Cases held apart from the pair.** Call only shows in 13 rooms ('Help us make the Frog at (990,123) on r/place!' at h+27.85, answered only by 'Wat', FlipnoteStudio3D). A proposal answered shows in 27 ('I suggest we do just a black C and D so we don't need to think about the background.' at h+67.97, then 'sounds good!', corridor). A start joined shows in 20 ('I'm trying to start making BMO to the right of them!' at h+28.89, then 'good luck! I will help', adventuretime). Pledge only shows in 4 rooms, an uncoded first part in 5 and a call after the close in 4. Evidence limits show in 163.
- **Rooms once, by priority.** The pair 430, a conditional answer 19, a refusal 20, call only 11, a proposal answered 26, a start joined 16, pledge only 4, uncoded 4, after the close 3, limit 159.
- So 480 rooms show a call (the pair, a conditional answer, a refusal or call only), and 430 of them show the pair (0.896).
- **Beside C2.** C2 grounded A12 on three exemplars (lebanon, DestinyTheGame, pcmasterrace). Here the pair shows in 430 rooms and the bare join in 371. The census reads written, coded replies only. It does not measure how many calls get no reply, which the bound states.

**The failure clause.** It is not met. Joins give a reason in 19 of 411 graded pair lines. Refusals give one in 32 of the 58 lines that show a refusal (0.55). So joins come bare far more often than refusals do. But here refusals give a reason only about half the time, against 3 of 3 in F-023 and 23 of 38 in F-014. Restrict lines were written to name exceptions, so bare refusals are likely over-represented in them.

**No correction (§2), and the wording.** No line is an accepted correction. The restrict lines state four conditions, and each is held. One visible pair shows no duty on each reader, no silent acceptance by placing and no general preference: the bound and the mechanism's words hold this. Joins can give reasons, ask back or set conditions: G28, the mechanism and the failure clause hold this. Refusals can be bare: the failure clause names this case. A reply can answer a proposal, a start or praise, not a call: P15's range with P02, P04 or P08, R01 and G44's readings hold this. By class the 181 restrict lines show the pair 102 (a bare join 82, a join with a reason 7, a part done 13), a conditional or asking answer only 18, a bare refusal or hostile reply 18, a refusal with a reason 6, call only 8, a proposal answered 12, a start joined 4 and pledge only 3. The other 10 are evidence limits: first parts with no code, and posts after the close. The 21 add-condition lines show the pair 7 (bare 5, with a reason 2), a conditional answer 4, a bare refusal 4, a refusal with a reason 1, a proposal answered 2, call only 1 and evidence limits 2. The 6 add-step lines show the pair 2, a conditional answer 1, call only 1, a start joined 1 and pledge only 1. The closed canvas ('It has ended otherwise id help') is the account's close at hour 73. Offices, pacts and design changes are P15's range with P02 or P08. A12 stands as served, with no move. J's answer to QD3-008 makes a question of wording mine to decide where no correction triggers §2, with a reason logged. I keep A12's words. The asymmetry the mechanism names shows in the census, and F-014 and F-023 already state the measured strength of the refusal side. Whether to record this census in the failure clause's field goes to D3c, since the census is not a seeded read.

**What the instantiate lines show.** Accepted 333: a bare join 301, a join with a reason 10, a part done or thanks 22. Rejected 44: a start joined 15, a proposal answered 13, an uncoded first part 5, after the close 4, call only 3, a refusal only 2, a pledge that answers no call 1, and a conditional answer only 1 (the re-ruling below).

**Absent lines.** 10 claims of absence fail. Each line's own concepts show a call answered in its thread by another member's later written join or part done (AcePlace, Cornwall, DCFU, ElderScrolls, ManningPlace, MiamiHurricanes, ProfessorLayton, Temple, TheB1G, crystalclear). The one `observed-absent` line is a specification (sakartvelo-044): an objection and a counter-proposal meet the call, and no member joins in writing. The other 151 are evidence limits. 24 candidates were read again by their reply trees. They stayed limits where the answer replies to a call that is not among the line's concepts (reading 8), answers a start, a report or a celebration, stands in another thread or after the close, or is the caller's own. A guard listed 81 limits whose labels name help or joining, and each had been read in the packet pass.

**Repairs (G7).** Lines in repaired rooms were 0.920 accepted (401 lines), and in unrepaired rooms 0.936 (346 lines). No ruling rests on the difference.

**Carried to later groups.**
- **The failure clause's field.** A12 marks the reason test 'not-addressed'. This census reads it on calls to place: joins give a reason in 19 of 411 graded lines, refusals in 32 of 58. D3c decides whether to record it, with the likely over-representation of bare refusals stated.
- **Starts joined (20 rooms).** Members join a start told in the present tense, with no call. D3c reads them beside the start before the call (A02) and the start itself (R01).
- **Proposals answered (27 rooms).** Assent to a design choice or a plan's detail shows P15 with no call. D3c reads them beside P02, P04 and A11.
- **Conditional answers** (24 rooms where they are the only answer) go to D3c with the failure clause's 'long and conditional' case.
- **F-023 and F-014** are not re-examined, since A12 is not revised.
- **The re-check (§5).** A12 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 812 quoted segments and 826 hours, in eight windows; restrict 397 segments and 457 hours, in six windows; add-condition 38 and 45; add-step 13 and 17; absent 24 and 24, from two batches of candidates read again; the re-ruling 2 and 2.
- **Every packet was read whole.** The first draw (offset 190) held a join that answers an explanation of the work, not a call (TeamDignitas-048). So that packet was read whole, and so were the others.
- **Two helper slips.** The reading-window wrapper first showed no lines, because its header pattern missed the bracketed index before each line id. Nothing was ruled from that output. The reply-context helper read only the first 80 lines of each forest until it was fixed, before the instantiate write. One line, nbaspurs-057, was affected, and it was read whole again. A11's checks rest only on links found, so none of A11's rulings moved.
- **Spec rows changed before the write.** korea-057 and dmt-004 were reclassed and re-cited when design proposals were separated from calls (reading 1). Rows in the first restrict spec file had a broken clause and were reworded.
- **Reading 7 came late.** It was settled while the restrict lines were ruled, after the instantiate lines were written. One instantiate line, bretagne-032, had only an offer to be there if needed ('Moi je suis la si y'a besoin' at h+49.14). An appended line re-rules it as a reject. The census moves it from the pair to a conditional answer, so run 2 supersedes run 1: the pair rooms fall from 431 to 430, and the bare-join rooms from 372 to 371.
- **A tag added after its ruling.** denmark-058 carries an R tag (the call named from the room's record), written in a tags file of the restrict pass, after its ruling. Its reason cites the call from the line's own concepts and does not name the record. So the count of 63 such pair lines may be one too high. No decision depends on it.
- **A compaction** came after the group's first close and before the re-ruling. The head and the stage file were read again, and a note logged the reconciliation before any other write.

### Close-check, D3a-39

`validate.py D3` reports 31,569 of 42,243 ledger lines ruled: the 30,822 before this leg and A12's 747. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 32,338 lines: 747 first rulings and 1 re-ruling from this leg. Appended re-rulings are now 769.
- **Pairs.** A12's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open. J answered QD3-008 (G43 reading 3).

## D3a-40: A13, upkeep before help between rooms

A13 is a standing arrow from C2, P05 → P16, of kind order and strength fair. Its gloss: 'short of hands, a room turns to other rooms'. Its connection: 'in a room carrying both, the first act of upkeep or defence comes before the first help given, asked for or traded with another room'. Its mechanism: 'A room keeping its work under strain runs short of hands and turns to other rooms for help, and other rooms send it.' Its failure clause, which the arrow records as present, reads 'In a room, help is given, asked for or traded only before any upkeep or defence, or a room under strain never asks for or receives help.' Its bound names rooms that help a neighbour before they have a work of their own, or come to the canvas as another room's helper. Its counterexample response names 'a second path where help is the room's first relation to the canvas'. C2 counted the order in 171 of 240 rooms carrying both (0.713; null mean 0.596, p95 0.642). G45 was written before any line was read, and its twelve readings are written under it (above). All 658 lines, in 652 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a13_census.py`, `d3_spec_cover.py` and `d3_pair_check.py`. Quotes were checked against `cite.py`'s output by `d3_spec_quotes.py`, and typed hours by `d3_spec_hours.py`. Every line was read with its reply context (`d3_read_window.py`).

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 85 | 42 | 0 | 0 | 0 | 1 | 42 |
| absent (268 `not-testable`, 69 `unobserved`) | 337 | 0 | 0 | 0 | 290 | 3 | 44 |
| restrict | 208 | 176 | 0 | 0 | 31 | 1 | 0 |
| add-condition | 24 | 23 | 0 | 0 | 1 | 0 | 0 |
| add-step | 4 | 3 | 0 | 0 | 1 | 0 | 0 |
| all | 658 | 244 | 0 | 0 | 323 | 5 | 86 |

**What the rooms show (the census, `d3_a13_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, or the class of its re-ruling, and the helper checks every class against the decision and kind written. These are counts of the lines labelers wrote where they saw both ends. They are not rates in the population.
- **The order, 155 rooms.** The room keeps its work, and help passes between it and another room after that ('someone is trying to erase the slime at this moment. I can't seem to stop them alone' at h+59.19, then 'I got people from r/tagpro helping out with it.' at h+59.29, dragonquest). The 156 order lines come from 42 instantiate lines, 69 restrict and add lines, 44 absent lines and one particular. 20 of them name the upkeep from the room's record.
- **The mechanism in words, 57 rooms** (0.368 of the order rooms). The help is named as the answer to an attack, a loss or the strain of keeping the work.
- **The direction of the first help.** Among the order lines, the room receives or asks for help in 70, gives help in 24 and trades help in 18. The absent rejects (44) are not graded. The mechanism names only the first direction. In 24 rooms the order shows only through help given once the room's own work is safe ('I've been helping out the LOLI sign when the Taiwan flag and heart don't need maintaining' at h+63.37, taiwan). G17's add-line readings name this help from spare capacity as A13's order.
- **Help first, 42 rooms.** The room's first help comes before any upkeep. In 5 rooms it is the bound's case: the room helps a neighbour before it has a work of its own ('no use we are outnumbered.. better help the french defend their flag' at h+22.33, luxembourg). In 37 it is the counterexample response's second path: help asked for, received or traded to start or build the work ('We at /r/EliteDangerous are trying to create a Star Citizen logo near us. Help us!' at h+50.05, starcitizen).
- **One act or not orderable, 20 rooms.** The room's first upkeep is the helpers' own, or a trade for night cover ('They may help us stay intact when most aussies are asleep if we help them a bit now' at h+19.55, australia), or is reported only as already under way. Three of these lines name the night shortage.
- **Held by another statement, 93 rooms.** The concepts show help refused or limited ('why would we help u if we cant even keep our own logo together' at h+61.07, globaloffensive), help returned, terms before help (A14), restoration by the room that did the damage (P07), or help for an attack (P09).
- **Not help after upkeep, 17 rooms.** The room keeps its work and then only proposes asking ('Maybe we should ask the Danganropa subreddit for support.' at h+38.37, aceattorney). One of A13's own support transitions is such a proposal, as G36 found for A04's.
- One end shows in 36 rooms and other cases in 4. Evidence limits show in 290.
- **Rooms once, by priority.** The order 155, the bound 5, the second path 37, one act 20, held 91, not help 15, one end 35, other 4, limit 290 (652 rooms).
- So 197 rooms show an episode (the order, the bound or the second path), and the order holds in 155 of them (0.787). With the 20 one-act rooms added, it holds in 155 of 217 (0.714). C2 found 171 of 240 (0.713).

**No correction (§2), and the wording.** No line is an accepted correction. The restrict and add conditions say that help comes unasked, from spare capacity, as repayment, by trade or terms, too late, refused or limited, before the room's upkeep, for building, from the room that did the damage, or from a coalition's shared work. A13's bound and counterexample response, P16's statement and range, A14, P07, P08, P09, P10, P12, P17, P21, A19, K02, A10 and G17's readings hold each of them, and no line shows the order failing for want of a condition A13 lacks. By class the 208 restrict lines show the order 58 (in words 21), the second path 33, the bound 5, a held case 80, and evidence limits 31 (one end 18, not help 7, not orderable 6). One restrict line is a particular by portability (flyers-041). The 24 add-condition lines show the order 9, the second path 2, a held case 12 and an evidence limit 1. The 4 add-step lines show the order 2, a held case 1 and an evidence limit 1. A13 stands as served, with no move. Under J's answer to QD3-008, I keep A13's words. The help-first rooms sit mostly in the second path, which only the counterexample response names, not the bound. Help given from spare capacity is A13's order by its connection but not by its mechanism. Whether to name either in A13's fields goes to D3c.

**What the instantiate lines show.** Accepted 42: the mechanism in words 33 (received 29, traded 4) and the order by the hours 9 (received 6, given 3). Rejected 42: one act or not orderable 14 (two of them re-ruled), one end 16, not help after upkeep 10, the second path 2. Particular 1 (detroitredwings-036, NONPORTABLE, which shows the order).

**Absent lines.** 44 claims of absence fail. Each line's own concepts show the room's upkeep and after it help passing between rooms. One NONPORTABLE line among them, thenetherlands-058, shows the order. Three NONPORTABLE lines that do not show it are particulars (buffalowizards-044, hearthstone-043, pitt-043). The other 290 are evidence limits. No line is `observed-absent` or `not-needed`. 72 candidates were read again by their quotes and reply trees. They stayed limits where the help comes first, where the help is reported at an hour that cannot be placed after the upkeep (reading 12), or where what follows the upkeep is terms, a proposal or a greeting. A guard listed 64 limits whose labels name help, and each had been read in the packet pass.

**Repairs (G7).** Lines in repaired rooms were 0.825 accepted (365 lines), and in unrepaired rooms 0.908 (293 lines). The difference comes from rejected instantiate and absent lines. No ruling rests on it.

**Carried to later groups.**
- **A13's wording at D3c.** The second path holds 37 of the 42 help-first rooms and is named only in the counterexample response. Help given from spare capacity shows the order in 24 rooms and is named only by G17's add-line reading.
- **The failure clause's second half.** A room under strain that never asks for or receives help cannot be read in single lines. The held rooms (refusals, too few hands, moves and giving up) go to D3c with it.
- **Reading 11 for earlier groups.** Ends named from a room's record at earlier arrows, A12's 63 pair lines among them, were not checked for edited submissions. D3c checks them.
- **A14** (P08 → P16) shares A13's second end. The lines held by A14 here (terms before help) go to its group.
- **The re-check (§5).** A13 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 195 quoted segments and 203 hours, in three windows; restrict 524 segments and 549 hours, in seven windows; add-condition 61 and 63; add-step 10 and 9; absent 102 and 104, from three batches of candidates read again; re-rulings 6 and 7. The rooms' records gave 32 cited posts.
- **Every packet was read whole.** The first draw (offset 366) held lines whose concepts do not show the order, so every packet was read whole.
- **A packet built at the wrong offset.** The first instantiate packet file used the verb's offset, which counts a header line. It skipped one line and took one restrict line. It is superseded by `d3_pk_A13_inst_365.txt`.
- **Reading 11 came late.** It was settled while ruling the restrict lines. Two instantiate lines are re-ruled by appended lines, and three restrict lines were ruled without the record before the write.
- **Quotes cut short.** In six spec files and one row of a seventh, quotes first stopped at an apostrophe followed by a letter. Each was rewritten with the full quotes and checked before any write. One rewrite and its check ran in the same turn, and the check was run again alone.
- **Counts typed from memory.** Two log notes gave counts typed from memory (cited posts 15 and 23, record-named order lines 9). Later notes correct them from scripts (13, 17 and 11). No ruling rested on them.
- **A stray command.** One check command ended with a no-op that ran nothing.

### Close-check, D3a-40

`validate.py D3` reports 32,227 of 42,243 ledger lines ruled: the 31,569 before this leg and A13's 658. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 32,998 lines: 658 first rulings and 2 re-rulings from this leg. Appended re-rulings are now 771.
- **Pairs.** A13's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-41: A14, border talk before help between rooms

A14 is a standing arrow from C2, P08 → P16, of kind order and strength thin. Its gloss: 'a settled border opens a channel for help'. Its connection: 'in a room carrying both, the first border talk, truce or deal comes before the first help given, asked for or traded with another room'. Its mechanism: 'Talk over a border opens a channel through which the two rooms then trade help: room for upkeep, pixels for protection.' Its failure clause, which the arrow records as present, reads 'In a room, help is traded only before any border talk, or settled borders are never followed by help between the two rooms.' Its bound: 'Where a room's first relation to a neighbour is help, help comes first.' C2 counted the order in 138 of 214 rooms carrying both (0.645; null mean 0.591, p95 0.636). G46 was written before any line was read, and its nine readings are written under it (above). All 666 lines, in 655 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a14_census.py` and `d3_pair_check.py`. Quotes were checked against `cite.py`'s output by `d3_spec_quotes.py`, typed hours by `d3_spec_hours.py`, and quotes cut short by a new helper, `d3_trunc_check.py` (totals by `d3_a14_quote_totals.py`). Every line was read with its reply context (`d3_read_window.py`).

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 216 | 105 | 0 | 0 | 0 | 3 | 108 |
| absent (254 `not-testable`, 68 `unobserved`) | 322 | 0 | 0 | 0 | 283 | 3 | 36 |
| restrict | 109 | 40 | 0 | 0 | 69 | 0 | 0 |
| add-condition | 16 | 5 | 0 | 0 | 11 | 0 | 0 |
| add-step | 3 | 0 | 0 | 0 | 3 | 0 | 0 |
| all | 666 | 150 | 0 | 0 | 366 | 6 | 144 |

**What the rooms show (the census, `d3_a14_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision and kind written. These are counts of the lines labelers wrote where they saw both ends. They are not rates in the population.
- **The order, 179 rooms.** The room and another room talk terms, and help passes between them after that ('I am okay with your proposed border.' at h+37.47, then 'I can help you guys preserve hulk as well.' at h+37.52, TheHulk). The 182 order lines come from 106 instantiate lines (one of them a particular), 40 restrict and add lines, and 36 absent lines. 9 of them take the first terms from the room's record.
- **The channel.** In 138 order rooms the first help after the terms passes with the room the terms were with, the channel the mechanism names. It passes with a third room in 2 and with a room the record does not name in 3. The absent rejects (36 rooms) are not graded.
- **The order in words, 22 rooms** (0.123 of the order rooms). The help names terms already settled as its ground ('That's because we made peace with sweden, they're helping us rebuild.' at h+70.43, overwatch). With help grounded on an alliance, an exchange of help, joint work or the neighbour relation added, as F-020 counted, 38 rooms (0.212). F-020 found 63 of 127 (0.496).
- **One offer, 125 rooms.** The room's first terms and its first help are one offer of help for space or restraint ('If you allow us to build the flag then I'm sure we can work together to restore the beer mug just south of the flag itself?' at h+23.40, israel), or they are reported at hours that cannot be placed against each other. This is the trade the mechanism names, 'room for upkeep, pixels for protection', but the terms do not come before the help. In 124 of these rooms no line shows the order or the bound.
- **Help first, 7 rooms.** The room's first help comes before any terms, the bound's case ('Some of us could help patch you guys, when we spare some tiles, and vise-versa.' at h+26.65, before a request to spare the flag, asexuality).
- **Not terms, 36 rooms.** The talk shown is an appeal with no limit or place, help traded only for help, an alliance, a choice inside the room, or the room undoing its own damage.
- One end shows in 8 rooms, and what follows the terms is not help (restraint, a move, the room's own upkeep or a proposal inside the room) in 7. The close shows in 8, other cases in 5, and evidence limits in 283.
- **Rooms once, by priority.** The order 179, the bound 7, one offer 124, not terms 36, not help 6, one end 7, after the close 8, other 5, limit 283 (655 rooms).
- So 186 rooms show an episode (the order or the bound), and the order holds in 179 of them (0.962). With the 124 one-offer rooms added, it holds in 179 of 310 (0.577). C2 found 138 of 214 (0.645).
- **Beside A13.** A13's 19 lines that named A14 (terms before help) lie in 19 rooms, and 14 of those rooms show A14's order here.

**No correction (§2), and the wording.** No line is an accepted correction. The restrict and add conditions say that the help is only promised or not delivered, that help and space form one offer, that help comes before the terms, that a channel already existed, that the helper is another room, that the record shows no cause, that the help is refused, or that placers break the terms. A14's connection, which counts an order and not a cause, its mechanism, its bound, G17, G18, P16's range, P07, P09, A17 and P21 hold each of them, and no line shows the order failing for want of a condition A14 lacks. By class the 109 restrict lines show the order 35 (in words 2, with a third room 2), the bound 5, and evidence limits 69 (one offer or not orderable 43, not terms 16, after the close 4, one end 3, not help 3). The 16 add-condition lines show the order 5 and evidence limits 11, and the 3 add-step lines are evidence limits. A14 stands as served, with no move. Under J's answer to QD3-008, I keep A14's words. In 125 rooms the terms and the help come as one offer, the trade the mechanism names, so the order the connection names cannot be read there. Whether the connection should name the one offer, and how the order test should count it, goes to D3c.

**What the instantiate lines show.** Accepted 105: the order by the hours, the thread, the reply chain or the post's words 85 (with the same room 83, the helper not named 2) and the order named in words 20 (with the same room 19, not named 1). Rejected 108: one offer or not orderable 76, not terms 18, one end 4, not help 4, after the close 4, help first 2. Particular 3, all NONPORTABLE: cavestory-045 and europe-053 are one offer, and dragonquest-033 shows the order.

**Absent lines.** 36 claims of absence fail. Each line's own concepts show terms between the room and another room and, after them, help passing between rooms, classed by the first act of each. Three NONPORTABLE lines that do not show the order are particulars (Moondye7-052, buffalowizards-045, thenetherlands-059). The other 283 are evidence limits. No line is `observed-absent` or `not-needed`. A guard listed 39 limits whose labels name a deal, truce, treaty or agreement. Each had been read in the window pass, and each shows help first, one offer, a report that cannot be placed (reading 9), the room undoing its own damage, terms only, or the close.

**Repairs (G7).** Lines in repaired rooms were 0.802 accepted (363 lines), and in unrepaired rooms 0.743 (303 lines). The difference comes from rejected and particular lines. No ruling rests on it.

**Carried to later groups.**
- **A14's wording at D3c.** The one offer holds 125 rooms. The connection names an order that the one offer cannot show, while the mechanism names the trade itself.
- **The order in words, beside F-020.** Help named on settled terms shows in 22 order rooms, 38 with F-020's wider grounds, against F-020's 63 of 127. F-020 coded the first help and its ground in each room and likely counted one-offer help as naming a deal, so the two counts measure different things. F-020 is not re-examined, since A14 is not revised. D3c sets the two codings side by side.
- **The failure clause's second half.** Settled borders never followed by help between the two rooms cannot be read in single lines. The lines where restraint, a move or terms alone follow the terms go to D3c with it.
- **The re-check (§5).** A14 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 390 quoted segments and 484 hours, in seven windows; restrict 188 segments and 219 hours, in five windows; add-condition 31 and 37; add-step 6 and 6; absent 76 and 80, from the 39 rows of ten windows. The rooms' records gave 13 cited posts.
- **Every packet was read whole.** The three draws (verb offsets 342, 442 and 542) found 6, 3 and 4 of their 10 lines rejected, most of them one offer, so every packet was read whole.
- **Readings settled while ruling.** Readings 1 to 8 were settled in the instantiate pass and reading 9 in the absent pass. Three spec rows moved under them before any write (archlinux-055, monero-052, acecombat-052). Checked against the written lines, reading 9 changed none.
- **Quotes cut short.** In several spec and row files, quotes first stopped at an apostrophe followed by a letter. Each was fixed before any write. From the restrict pass on, `d3_trunc_check.py` checked every file, and run over all A14 files at the close it finds none.
- **Edits in parallel.** Four fixes to one spec file (`A14-inst-spec-4.txt`) were made by Edits run in parallel, against the rule. The file was then checked alone, and it held all four fixes. One of them mended a garbled clause (neu-024).
- **A shell variable.** One count command used a shell variable, against the standing rule. It ran and changed nothing.

### Close-check, D3a-41

`validate.py D3` reports 32,893 of 42,243 ledger lines ruled: the 32,227 before this leg and A14's 666. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 33,664 lines: 666 first rulings from this leg and no re-ruling. Appended re-rulings stay 771.
- **Pairs.** A14's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-42: A15, the call before the attack

A15 is a standing arrow from C2, P01 → P09, of kind order and strength strong. Its gloss: 'a call's hands can turn on a rival'. Its connection: 'in a room carrying both, the first call to the canvas comes before the room's first call or act against another room's work'. Its mechanism: 'A call brings members to the canvas, and some of them turn its hands against a rival's work instead of, or before, building the room's own.' Its bound: 'Where a room's first canvas act is an attack (edmontonoilers, canucks, anarcho_capitalism among the pass 1 story rooms), the attack call is the first call.' C2 counted the order in 93 of 129 rooms carrying both (0.721; null mean 0.487, p95 0.55), and in 91 of 129 without joining concepts. G47 was written before any line was read, and its 36 readings are written under it (above). All 656 lines, in 653 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a15_census.py` and `d3_pair_check.py`. Quotes were checked against `cite.py`'s output by `d3_spec_quotes.py`, typed hours by `d3_spec_hours.py`, and quotes cut short by `d3_trunc_check.py` (totals by `d3_a15_quote_totals.py`). Every line was read with its reply context (`d3_read_window.py`).

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 78 | 51 | 0 | 0 | 0 | 4 | 23 |
| absent (282 `not-testable`, 125 `unobserved`, 1 `observed-absent`) | 408 | 1 | 0 | 0 | 261 | 0 | 146 |
| restrict | 149 | 79 | 0 | 0 | 70 | 0 | 0 |
| add-condition | 17 | 4 | 0 | 0 | 11 | 2 | 0 |
| add-step | 4 | 2 | 0 | 0 | 2 | 0 | 0 |
| all | 656 | 137 | 0 | 0 | 344 | 6 | 169 |

**What the rooms show (the census, `d3_a15_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision and kind written. These are counts of the lines that labelers wrote where they saw both ends. They are not rates in the population.
- **The order, 277 rooms.** The room calls members to place for its own work, and after that the room calls or acts against another room's work ('Would anyone be willing to start a new spot for 4chan on r/place ?' at h+57.46, then 'Let's remove the asexual pride banner!' at h+62.16, 4chan). The 277 order lines come from 51 instantiate lines, 78 restrict and add lines (74 restrict, 4 add-condition), 146 absent lines, and 2 particulars marked PO. 14 of them take the first call from the room's record.
- **What the first attack is.** In the 129 order rooms with a graded line, the first attack is a call or plan in 109, an act carried out or under way in 15, and encroachment that the room admits or is told of in 5. The absent rejects (146 rooms) are not graded.
- **The order in words, 7 rooms** (0.025 of the order rooms). The attack names the call, the called work or the hands it brought as its ground ('couldn't find the eve logo, decided to vandalize r/ vegan instead' at h+31.87, under a call to defend, eve).
- **One call holding both ends, 58 rooms.** The room's first call is itself a call to place its work over another room's work ('Help us turn the ansoc flag at (40, 450) into an ancap one!', anarchocapitalism), or the first acts cannot be placed against each other. The order the connection names cannot be read there.
- **The bound's pattern, 9 rooms.** The room's first call or act against another work comes before its first call to place ('can we all take a moment to terrorize the Flames logo on /r/place?', with its opening words 'Since we aren't doing our own', canucks). No room shows both the order and the bound.
- Not the room's attack shows in 23 rooms (mostly defence of the room's own place), one end in 18, not a call in 3, and the close in 1. Other cases show in 4, one specification in 1, and evidence limits in 261.
- **Rooms once, by priority.** The order 277, the bound 9, one call 58, not a call 3, not the room's attack 23, one end 16, after the close 1, other 4, the specification 1, limit 261 (653 rooms).
- So 286 rooms show an episode (the order or the bound), and the order holds in 277 of them (0.969). With the 58 one-call rooms added, it holds in 277 of 344 (0.805). C2 found 93 of 129 (0.721).
- **Story rooms and support transitions.** Of the bound's three story rooms, edmontonoilers shows one call, canucks the bound, and anarcho_capitalism the order. Of the three support transitions, Temple and stlouis show the order, and completeanarchy shows defence of the room's flag.

**No correction (§2), and the wording.** No line is an accepted correction. The restrict and add conditions say that the order does not show the call as the cause, that the attack follows the room's finished work, that taking space is the building itself, that the attack is the room's founding work, that scarce space or broken terms gave the reason, that the attack answers erasure, that a visitor's or a member's act is not the room's, or that members deny the room controls an attack. A15's connection, which counts an order and not a cause, its bound, its counterexample response, G20, P05, P08, P18, P21, K01, K02 and A16 hold each of them, and no line shows the order failing for want of a condition A15 lacks. By class the 149 restrict lines show the order 74 (in words 3), the bound 5, and evidence limits 70 (one call or not orderable 38, not the room's attack 16, one end 12, not a call 3, after the close 1). The 17 add-condition lines show the order 4 and evidence limits 11, with 2 particulars, and the 4 add-step lines show the bound 2 and evidence limits 2. A15 stands as served, with no move. Under J's answer to QD3-008, I keep A15's words. Two wording questions go to D3c: the mechanism's 'instead of, or before, building the room's own' does not name an attack after the room's work was complete (11 lines marked AC, 7 of them order lines), and the bound names a separate attack call first, while the commoner form in the rooms is one call that places the room's work over another's (58 rooms against 9).

**What the instantiate lines show.** Accepted 51: the order by the hours, the thread, the reply chain or the post's words 47 (the first attack a call or plan 41, an act 6) and the order named in words 4. Rejected 23: one call or not orderable 13 (two of them by re-ruling), not the room's attack 5, one end 3, the bound 2. Particular 4, all NONPORTABLE: kilian-044 shows the order (PO); brasil-063, europe-054 and onepunchman-055 do not.

**Absent lines.** 146 claims of absence fail. Each line's own concepts show the room's call to place and, after it, the room's call or act against another room's work, classed by the first act of each. One of them is NONPORTABLE (borderlands-057) and is rejected by G45 reading 10. The one `observed-absent` line (mit-045) is a specification: its concepts show calls to place and no attack. The other 261 are evidence limits. A guard listed 60 limits whose labels name an attack. Each had been read in the window pass, and each shows no call to place, defence, a visitor's act, one call holding both ends, or an act reported only before the report (reading 9 and G46 reading 9).

**Repairs (G7).** Lines in repaired rooms were 0.727 accepted (363 lines), and in unrepaired rooms 0.741 (293 lines). No ruling rests on the difference.

**Carried to later groups.**
- **A15's wording at D3c.** The AC lines, beside the mechanism's 'instead of, or before'; and the one call holding both ends (58 rooms), beside the bound and the counterexample response's 36 of 129.
- **The failure clause's second half.** Calls to place never followed by a call or act against another work cannot be read in single lines. The lines where only defence, terms or building follow the call go to D3c with it.
- **The re-check (§5).** A15 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 171 quoted segments and 180 hours, in three windows; re-rulings 6 and 5; restrict 323 segments and 393 hours, in seven windows; add-condition 33 and 35; add-step 7 and 8; absent 311 and 332, from the 147 rows of thirteen windows. The rooms' records gave 31 cited posts, in 8 files.
- **Every packet was read whole.** The draw of ten (verb offset 430) found 6 accepted, 3 rejected and 1 particular, so the packet was read whole, as were all the others.
- **Readings settled while ruling.** Readings 1 to 17 were settled in the instantiate pass, 18 to 35 in the restrict and add passes, and 36 in the absent pass. One spec row (brasil-063) was reworded under readings 7 and 9 before any write.
- **A reading corrected, and two re-rulings.** Reading 4 placed two acts reported as continuing from before at their posts' hours. G46 reading 9 already placed such acts only before the report, so reading 18 corrects reading 4, and buffalobills-059 and floridagators-043 are re-ruled by appended lines.
- **Drafts cut short.** Six spec and row drafts were cut short mid-quote by a Write, each at a quote that began on a word with an apostrophe (A15-restrict-spec-2, -4, -5 and -7, A15-absent-rows-5 and -8). Each was written again whole before any check or write. One draft of A15-restrict-spec-3 held a stray placeholder row, and one row of A15-absent-rows-4 named a concept not in the line. Both were removed before the checks.
- **A shell variable.** One join command began with a stray shell assignment, a word beginning with the refused prefix, against the standing rule. It did nothing, and the join it carried is correct.
- **Counts typed from memory.** One diary note gave two counts from memory (R marks and restrict segments). A second note corrected them from `d3_a15_quote_totals.py`.

### Close-check, D3a-42

`validate.py D3` reports 33,549 of 42,243 ledger lines ruled: the 32,893 before this leg and A15's 656. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 34,322 lines: 656 first rulings and 2 re-rulings from this leg. Appended re-rulings are now 773.
- **Pairs.** A15's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-43: A16, the attack call before the restraint

A16 is a standing arrow from C2, P09 → P07, of kind order and strength strong. Its gloss: 'an attack call is refused inside the room'. Its connection: 'in a room carrying both, the room's first call or act against another room's work comes before its first sparing, refusal, apology or reining in'. Its mechanism begins: 'A call to attack makes an answer from the room due in its thread.' Its bound: 'Partly constitutive: reining in the room's own attackers needs an attack to rein in.' C2 counted the order in 82 of 104 rooms carrying both (0.788; null mean 0.529, p95 0.606). G48 was written before any line was read, and its 111 readings, each logged in the diary, are set out under it by head (above). All 697 lines, in 662 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a16_census.py` and `d3_pair_check.py`. Quotes were checked against `cite.py`'s output by `d3_spec_quotes.py` and `d3_a16_seg_gap.py` (for segments that close before a colon), typed hours by `d3_spec_hours.py`, and quotes cut short by `d3_trunc_check.py` (totals by `d3_a16_quote_totals.py`). Every line was read with its reply context (`d3_read_window.py`), and every restrict and add line with its full how (`d3_add_how.py`).

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 237 | 183 | 0 | 0 | 0 | 7 | 47 |
| absent (213 `not-testable`, 112 `unobserved`, 4 `observed-absent`) | 329 | 4 | 0 | 0 | 247 | 9 | 69 |
| restrict | 104 | 67 | 0 | 0 | 37 | 0 | 0 |
| add-condition | 17 | 13 | 0 | 0 | 4 | 0 | 0 |
| add-step | 10 | 8 | 0 | 0 | 2 | 0 | 0 |
| all | 697 | 275 | 0 | 0 | 290 | 16 | 116 |

**What the rooms show (the census, `d3_a16_census.py`).** Its rules were logged before it ran, and one count was mended after a missing tag was found (below). Each line keeps the class it was ruled under, and the helper checks every class against the decision and kind written. These are counts of the lines that labelers wrote where they saw both ends. They are not rates in the population.
- **The order, 319 rooms.** The room calls or acts against another room's work, and after that the room spares it, refuses the call, reins in its attackers, apologises or restores ('Ohio State has been fucking with us all day.' at h+55.77, then 'No, stop messing with other schools' at h+55.81, Temple). The 346 order lines come from 188 instantiate lines, 85 restrict and add lines (66 restrict, 11 add-condition, 8 add-step), and 73 absent lines (69 rejects and 4 particulars marked PO). 19 of them take an end from a coded post above the line's concepts.
- **The answer in the thread.** 246 order lines answer the attack in its reply chain or thread, and 22 show the order by the hours or in a post's words. The 69 absent rejects are not split. By room, 230 order rooms show an answer in the thread, and 21 show the order only by the hours or in a post's words.
- **The reason.** Of the 255 order lines answered in the thread (the PO lines included), the first answer gives a reason in 208, is bare in 28, and is unmarked in 19: sparing, apology or restoring that answers a neighbour's report. So 208 of 236 marked refusals or reining in give a reason (0.881), beside F-014's 23 of 38 (0.605). By room, 196 of the 211 order rooms with a marked answer give a reason in at least one line, and 15 give only bare ones.
- **The bound's pattern, 3 rooms.** The room's first restraint comes before its first coded attack ('I just want to keep the peace until this whole thing is archived' at h+58.17, then 'I say we capitalise' at h+58.25, criticalrole; also esperanto and hentai). No room shows both the order and the bound.
- **Refused visitors' calls, 9 rooms.** A call from outside the room is refused in the room ('Help us replace the Japanese flag with the Korean one!', kpop). The answer the mechanism names shows, but not the connection's order, and the census counts these apart. One of the nine rooms also shows the order. Seven of the eight instantiate lines refuse with a reason.
- One end shows in 43 rooms, often an attack call met by acceptance, or a target's plea with no answer from the room ('r/ainbowroad rep here. No.', TeamYellowPlace). Not the room's attack shows in 20 rooms, not restraint in 10, after the close in 5 and one act in 1. Other particulars show in 7, absent specifications in 4, and evidence limits in 247.
- **Rooms once, by priority.** The order 319, the bound 3, one act 1, a visitor's call 8, not the room's attack 17, not restraint 9, one end 42, after the close 5, other 7, specification 4, limit 247 (662 rooms).
- So 322 rooms show an episode (the order or the bound), and the order holds in 319 of them (0.991). With the one-act room added, it holds in 319 of 323 (0.988). C2 found 82 of 104 (0.788), and the counterexample response counts 22 of 104 that spare first.
- **Story rooms and support transitions.** The three support-transition rooms (nyjets, leafs, Temple) and the bound's two rooms (touhou, calgaryflames) all show the order on their A16 lines. touhou's line shows it in one post's words: the room's earlier takeover of a neighbour's area, then the help it gave that neighbour in return (reading 43).

**No correction (§2), and the wording.** No line is an accepted correction, and no line is paired. The restrict and add conditions say that a refusal can be bare, that a refusal does not show the attackers complied, that the restraint can answer a neighbour's complaint or an act and not a call, that the answer can come in another branch or by the hours, that the reason can be a cost, an alliance, the room's own work or a joke, that the speaker may be the target or a visitor, and that restraint can come first. A16's mechanism (a refusal usually gives a reason, and the reason may name the cost), its connection (an order, not compliance), its bound, its falsifier's second clause (recorded present), G20's first amendment and G48's readings of the target's and visitors' replies hold each of them. No line shows the order failing for want of a condition A16 lacks. By class the 104 restrict lines show the order 66 (in the thread 54), the bound 1, and evidence limits 37 (one end 17, not the room's attack 9, not restraint 7, after the close 3, a visitor's call 1). The 17 add-condition lines show the order 11 and the bound 2, with evidence limits 4, and the 10 add-step lines show the order 8 and evidence limits 2. A16 stands as served, with no move. Under J's answer to QD3-008, I keep A16's words. Three wording questions go to D3c. The mechanism's reason, the room's norm or the attack's cost, does not name a tie or agreement with the target, the target's prior claim, the room's own work first or a joke, which the 208 marked reasons also give. The bound shows alone in 3 of 322 episode rooms on the return's lines, beside the counterexample response's 22 of 104. The gloss does not say that refused visitors' calls (9 rooms) show the answer but not the order.

**What the instantiate lines show.** Accepted 183: the order answered in the thread 175, and the order by the hours or in a post's words 8. Rejected 47: one end 25, not the room's attack 9, a refused visitor's call 8, not restraint 2, the bound 1 (hentai-050), one act 1 (pcmasterrace-076) and after the close 1 (anaheimducks-044). Particular 7, all NONPORTABLE: five show the order and are marked PO (Russiaclan-048, belgium-050, chile-052, ethereum-061, ireland-038); cirkeltrek-054 and spain-044 do not.

**Absent lines.** 69 claims of absence fail (40 `not-testable`, 29 `unobserved`). Each line's concepts, or the coded posts above them in their reply chain, show the room's call or act against another room's work and, after it, the room's restraint toward another room's work, classed by the first act of each (readings 89 and 95). Nine lines are NONPORTABLE particulars, and four of them show the order and are marked PO (ManningPlace-056, battlecats-024, rit-061, truestl-052). The four `observed-absent` lines are specifications: catholicism-062, k_on-052 and montenegro-048 show an attack call and no restraint of the room's, and transformers-051 shows play between the room's own factions. The other 247 are evidence limits. A guard listed 57 limits whose labels name sparing, apology, stopping or a truce. Each had been read in the window pass, and each shows a visitor's apology for damage to the room's own work, defence of the room's own work, restraint with no attack of the room's, or restraint before the first attack.

**Repairs (G7).** Lines in repaired rooms were 0.800 accepted (385 lines), and in unrepaired rooms 0.824 (312 lines). No ruling rests on the difference.

**Carried to later groups.**
- **A16's wording at D3c.** The reasons beside the mechanism's norm and cost; the bound's 3 of 322 beside the counterexample response's 22 of 104; refused visitors' calls beside the gloss.
- **The failure clause's second half.** Attack calls that draw no refusal can be read in single lines only as one end (43 rooms, many met by acceptance or by a target's plea). They go to D3c with the clause, which A16 records as present.
- **The re-check (§5).** A16 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 481 quoted segments and 586 hours, in ten windows; restrict 213 and 268, in six windows; add-condition 35 and 45; add-step 21 and 26; absent 146 and 188, from the 82 rows of ten windows. Nine further segments and 25 further hours come from coded posts above a line's concepts, and each was checked against `d3_cite_many.py`'s output. No hour mismatched, and no quote was cut short.
- **Every packet was read whole.** The three draws of ten (seeds 20261016+357, +457 and +557) found 21 order lines answered in the thread, 3 one end, 2 refused visitors' calls, 2 particulars, 1 not the room's attack and 1 by the hours, so each packet was read whole, as were all the others.
- **Readings settled while ruling.** Readings 1 to 51 were settled in the instantiate pass, 52 to 88 in the restrict and add passes, and 89 to 111 in the absent pass. The log of reading 99 called indieheads-061 an observed-absent line. A later note corrects it, and the reject stands.
- **Draft fragments.** Four rows, in three drafts, held a stray phrase that quoted part of a post and then called it unquoted or avoided (A16-inst-spec-10 at ucf-055, A16-restrict-spec-1 at 49ers-058 and PurplePixels-052, A16-restrict-spec-6 at winnipegjets-056). One row quoted a word of A16's mechanism as if from a post (A16-restrict-spec-3 at dbz-061), and one closed a quote before a colon (A16-inst-spec-8 at samuraijack-052). Each was mended before the checks. No draft was cut short at an apostrophe.
- **A census tag.** The spec row for ethereum-061 says PO, but no tags file carried the mark, so the first census run counted it among the other particulars. `d3_a16_tag_gaps.py` found it, `A16-tags-amend.txt` adds it, and the counts above are from the second run. The QD3-008 note gave the first run's 207 of 235, which is now 208 of 236. A label in the census script that called an untagged visitor line bare was mended before the first log.
- **A shell variable and a temp file.** One count command began with a no-op assignment whose name has the refused prefix; the permission check refused it, and it ran nothing. At the leg's opening, one command wrote the verb's listing through the TMPDIR shell variable, outside out/, as the opening note disclosed.

### Close-check, D3a-43

`validate.py D3` reports 34,246 of 42,243 ledger lines ruled: the 33,549 before this leg and A16's 697. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 35,019 lines: 697 first rulings from this leg and no re-ruling. Appended re-rulings stay at 773.
- **Pairs.** A16's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-44: A17, the attack call before the talk of terms

A17 is a standing arrow from C2, P09 → P08, of kind order and strength fair. Its gloss: 'an attack call is met with a truce'. Its connection: 'in a room carrying both, the room's first call or act against another room's work comes before its first border talk, truce or deal'. Its mechanism: 'A call to attack is met by the room's relations with its neighbours: the room invokes a truce, or proposes a deal instead.' Its bound: 'Early side only: on the late side border talk comes first (0 of 4 hold), since late rooms meet neighbours before any attack.' C2 counted the order in 95 of 172 rooms carrying both (0.552; null mean 0.423, p95 0.477). G49 was written before any line was read, and its 146 readings, each logged in the diary, are set out under it by head (above). All 650 lines, in 647 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a17_census.py` and `d3_pair_check.py`. Quotes were checked against `cite.py`'s output by `d3_spec_quotes.py` and `d3_a16_seg_gap.py`, typed hours by `d3_spec_hours.py`, and quotes cut short by `d3_trunc_check.py` (totals by `d3_a17_quote_totals.py`). Every line was read with its reply context (`d3_read_window.py`), and every restrict and add line with its full how (`d3_add_how.py`).

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 156 | 81 | 0 | 0 | 0 | 7 | 68 |
| absent (261 `not-testable`, 152 `unobserved`, 9 `observed-absent`) | 422 | 8 | 0 | 0 | 312 | 7 | 95 |
| restrict | 63 | 39 | 0 | 0 | 23 | 1 | 0 |
| add-condition | 7 | 5 | 0 | 0 | 2 | 0 | 0 |
| add-step | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| all | 650 | 133 | 0 | 0 | 339 | 15 | 163 |

**What the rooms show (the census, `d3_a17_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision and kind written. These are counts of the lines that labelers wrote where they saw both ends. They are not rates in the population.
- **The order, 213 rooms.** The room calls or acts against another room's work, and after that the room and another room talk terms ('Declaro guerra ao FLUFFHEAD' at h+67.47, then 'Eles já vieram aqui com um acordo de paz.' at h+68.09, brasil). The 215 order lines come from 85 instantiate lines (81 accepted and 4 particulars marked PO), 33 restrict and add lines (28 restrict, 5 add-condition), and 97 absent lines (95 rejects and 2 particulars marked PO). Five of them take an end from a coded post above the line's concepts.
- **The answer in the thread.** 80 order lines answer the attack in its reply chain or thread, and 34 show the order by the hours or in a post's words. The 95 absent rejects are not split. By room, 83 order rooms show an answer in the thread, 33 show the order only by the hours or in a post's words, 95 only on an absent reject, and 2 only on a NONPORTABLE absent line.
- **The form of the answer.** Of the 84 order lines answered in the thread (the PO lines with a form included), the first answer invokes terms already made (INV) in 41, offers, asks or settles new terms (DEAL) in 39, and reports terms with a third room or contests terms (OTHER) in 4. So the mechanism's two forms, a truce invoked and a deal proposed, appear about equally. By room, 40 order rooms show only INV, 39 only DEAL and 4 only OTHER.
- **The bound's pattern, 17 rooms.** Talk of terms between the room and another room comes before the room's first coded attack ('We have a truce with the tree and therefore RR.' at h+39.00, before the room's first spread at h+40.41, AmericanFlaginPlace). Six of the 17 lines are instantiate lines and 11 restrict lines. No room shows both the order and the bound.
- **Visitors' calls answered by terms, 4 rooms.** A call from outside the room is answered with the room's terms ('Pretty sure we have a treaty with the void.', EraseThePlace). The answer the mechanism names shows, but not the connection's order, and the census counts these apart. None of the four rooms also shows the order.
- Not terms shows in 30 rooms: restraint that names no terms, a proposal inside the room to ask or ally, friendship, or a lone placer's talk ('Los finlandeses son amigos no comida.', argentina). One end or neither shows in 26 rooms, not the room's attack in 17, one act in 6 and after the close in 5. Other particulars show in 9, absent specifications in 8, and evidence limits in 312.
- **Rooms once, by priority.** The order 213, the bound 17, one act 6, a visitor's call 4, not the room's attack 17, not terms 30, one end 26, after the close 5, other 9, specification 8, limit 312 (647 rooms).
- So 230 rooms show an episode (the order or the bound), and the order holds in 213 of them (0.926). With the six one-act rooms added, it holds in 213 of 236 (0.903). C2 found 95 of 172 (0.552), and the counterexample response counts 77 of 172 that talk borders before any attack call.
- **Story rooms and support transitions.** czech shows the order on its support transition ('Texas shall fall', then 'We [already agreed to a truce here]'). thailand shows the order on its return line ('Get over to /r/place, Thailand has been covered up by a frog.', then 'we have an ongoing agreement'), though C2's audit found its first border talk first. PlaceNL's line shows not terms, since its compromise is proposed inside the room. The counterexample response's room, strangerthings, shows only an evidence limit.

**No correction (§2), and the wording.** No line is an accepted correction, and no line is paired. The restrict and add conditions say that the talk can answer a complaint, an accusation or an act and not a call, that an agreement can be invoked and not caused, that talk can come first, that a deal can oblige an attack on a third room, that the talk can answer an alarm or a defence call, that it can come in another branch or by the hours, and that an attack call can be met by assent. A17's connection, which counts a call or an act, its mechanism, its bound and counterexample response, its falsifier's second clause (recorded present), P17 under G4a and G49's readings hold each of them. No line shows the order failing for want of a condition A17 lacks. By class the 63 restrict lines show the order 28 (in the thread 12), the bound 11, and evidence limits 23 (not the room's attack 9, one end 4, not terms 4, one act 3, after the close 3), with one particular. The 7 add-condition lines show the order 5 and evidence limits 2, and the 2 add-step lines are evidence limits. A17 stands as served, with no move. Under J's answer to QD3-008, I keep A17's words. Four wording questions go to D3c. The gloss names a truce, while the answers in the thread split between a truce invoked (41) and a deal proposed (39). The connection's first border talk reads as the room's own, while the return reads terms from either room's record. The bound shows alone in 17 of 230 episode rooms on the return's lines, beside the counterexample response's 77 of 172. The mechanism opens with a call, while many order lines open with the room's act as a neighbour tells of it.

**What the instantiate lines show.** Accepted 81: the order answered in the thread 66, and the order by the hours or in a post's words 15. Rejected 68: not terms 24, one end or neither 21, not the room's attack 8, the bound 6, a visitor's call 4, one act 3 and after the close 2. Particular 7, all NONPORTABLE: four show the order and are marked PO (FaroeIslands-039, ainbowroad-064, belgium-051, czech-058); france-048, germany-064 and roosterteeth-057 do not.

**Absent lines.** 95 claims of absence fail (66 `not-testable`, 28 `unobserved`, 1 `observed-absent`). Each line's concepts, or the coded posts above them in their reply chain, show the room's call or act against another room's work and, after it, talk of terms between the room and another room, classed by the first act of each (reading 105). The observed-absent reject is transformers-052. Seven lines are NONPORTABLE particulars, and two of them show the order and are marked PO (clubpenguin-047, truestl-053). The other eight observed-absent lines are specifications, each showing an attack call with no talk of terms. The other 312 are evidence limits. A guard listed 56 limits whose labels name a truce, a treaty, a deal, a negotiation or an agreement. Each had been read in the window pass, and each shows talk with no coded attack of the room's, talk before the room's first coded attack, an attack or a visit the room suffers, or an act and talk that cannot be placed.

**Repairs (G7).** Lines in repaired rooms were 0.751 accepted (366 lines), and in unrepaired rooms 0.694 (284 lines). No ruling rests on the difference.

**Carried to later groups.**
- **A17's wording at D3c.** The gloss beside the deal; the connection's first border talk beside talk from either room; the bound's 17 of 230 beside the counterexample response's 77 of 172; the mechanism's call beside the room's act as a neighbour tells of it.
- **The failure clause's second half.** Attack calls that draw no talk can be read in single lines only as not terms (30 rooms) or one end (26). They go to D3c with the clause, which A17 records as present.
- **Ungraded absent rejects.** 95 order rooms rest on absent rejects whose form of answer the census does not grade.
- **The re-check (§5).** A17 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 293 quoted segments and 322 hours, in six windows; restrict 124 and 155, in four windows; add-condition 14 and 19; add-step 5 and 4; absent 207 and 233, from the 110 rows of thirteen windows. Seventeen further segments and twenty further hours come from coded posts above a line's concepts or from another window, and each was checked in its own run against `d3_cite_many.py`'s output or that window's quote file. No hour mismatched, and no quote was cut short.
- **Every packet was read whole.** The two draws of ten (seeds 20261016+432 and +532) found 7 order lines answered in the thread, 3 by the hours or in a post's words, 5 not terms, 2 one end, 1 not the room's attack, 1 the bound and 1 after the close, so each packet was read whole, as were all the others.
- **Readings settled while ruling.** Readings 1 to 67 were settled in the instantiate pass, 68 to 99 in the restrict pass, 100 to 104 in the add passes, and 105 to 146 in the absent pass. Three corrections were logged and applied before any row was built: cfb-054 moved to the bound (reading 43), neopets-055 to the order in a post's words (reading 45), and ghibli-057 to a reject (reading 126). The log of readings 56 to 67 gave the second draw's tally in a garbled phrase, and the instantiate pass's note gives the counts by script.
- **Draft slips.** Five quotes, in three absent-row drafts (rows 1, 7 and 11), closed before a colon, and each was reworded before the checks passed. One draft of `A17-absent-rows-13.txt` held an unfinished row ending in a placeholder word; it was overwritten whole before any check or build.
- **Shell slips.** One quote check began with a needless shell assignment, and one listing of the second draw's ids used awk with numbered fields; the rules forbid both. Neither changed a file, and both were disclosed in the diary when they happened. Two commands piped into cut, and the guard refused them; they ran nothing.

### Close-check, D3a-44

`validate.py D3` reports 34,896 of 42,243 ledger lines ruled: the 34,246 before this leg and A17's 650. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 35,669 lines: 650 first rulings from this leg and no re-ruling. Appended re-rulings stay at 773.
- **Pairs.** A17's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-45: A18, the attack before the taunt

A18 is a standing arrow from C2, P09 → P18, of kind order and strength fair. Its gloss: 'an attack is carried on in taunts'. Its connection: 'in a room carrying both, the room's first call or act against another room's work comes before the first taunt, chant, claim of victory or salute with a rival'. Its mechanism: 'An attack makes the rival a named party, and the contest is carried on in talk: taunts, chants, claims of victory, a salute after the fight.' Its bound: 'Early side only: no late-side room carries both.' C2 counted the order in 56 of 68 rooms carrying both (0.824; null mean 0.591, p95 0.676). G50 was written before any line was read, and its amendment 1 before any line was ruled. Its 204 readings, each logged in the diary, are set out under it by head (above). All 647 lines, in 645 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a18_census.py` and `d3_pair_check.py`. Quotes were checked against `cite.py`'s output by `d3_spec_quotes.py` and `d3_a16_seg_gap.py`, typed hours by `d3_spec_hours.py`, and quotes cut short by `d3_trunc_check.py` (totals by `d3_a18_quote_totals.py`). Every line was read with its reply context (`d3_read_window.py`), and every restrict and add line with its full how (`d3_add_how.py`).

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 117 | 50 | 0 | 0 | 0 | 1 | 66 |
| absent (305 `not-testable`, 125 `unobserved`, 1 `observed-absent`) | 431 | 1 | 0 | 0 | 334 | 10 | 86 |
| restrict | 89 | 36 | 0 | 0 | 52 | 1 | 0 |
| add-condition | 10 | 1 | 0 | 0 | 9 | 0 | 0 |
| all | 647 | 88 | 0 | 0 | 395 | 12 | 152 |

**What the rooms show (the census, `d3_a18_census.py`).** Its rules were logged before it ran. Each line keeps the class it was ruled under, and the helper checks every class against the decision and kind written. These are counts of the lines that labelers wrote where they saw both ends. They are not rates in the population.
- **The order, 169 rooms.** The room calls or acts against another room's work, and after that the room taunts, chants, claims victory over or salutes a rival ('We can take out that pineapple too.' at h+49.20, then 'It ended up helping us and backfired on them superbly.' at h+83.21, taiwan). The 169 order lines come from 50 accepted instantiate lines, 30 restrict and add lines (29 restrict, 1 add-condition), and 89 absent lines (86 rejects and 3 particulars marked PO). Four of them take an end from a coded post above the line's concepts.
- **The answer in the thread.** 38 order lines answer the attack in its reply chain or thread, and 42 show the order by the hours or in a post's words. The 86 absent rejects are not split. By room, 38 order rooms show an answer in the thread, 42 show the order only by the hours or in a post's words, 86 only on an absent reject, and 3 only on a NONPORTABLE absent line.
- **The form, the rival and the close.** Of the 80 graded order lines, the first taunt is a taunt, insult, threat, chant or lettering (TAUNT) in 48, a claim of victory or gloating (VICT) in 31, and a salute (SALUTE) in 1. No first taunt is flooding (FLOOD) or blame after the close (BLAME). The first taunt aims at the attack's target (SAME) in 71 lines and at another group (ELSE) in 9. It comes after hour 73 (AC) in 32: 7 of the 38 answered in the thread, and 25 of the 42 shown by the hours or in a post's words. By room, 71 graded order rooms show only SAME and 9 only ELSE.
- **A taunt after an attack the room suffers, 46 rooms.** The room taunts, blames or claims victory over a rival after an attack it suffers, and shows no attack of its own before the taunt (clg, C2's support transition: a visitor's admitted attack on the room's logo, then the room's claim of victory). The mechanism's named party shows here, but not the connection's order, since the attack is not the room's. The census counts these rooms apart. None of the 46 shows the order or the bound.
- **The bound's pattern, 8 rooms.** The room's first taunt comes before its first coded attack, in most lines as an answer to an attack it suffers (skyrim: a chant at h+54.24 under a call to take back the room's home, then the room's attack proposal at h+55.55). One of the 8 lines is an instantiate line and 7 are restrict lines. Three are marked PRE, since they name a rival from outside the canvas: AyyMD, borussiadortmund and uofm. The other five rooms are formula1, funhaus, philippines, skyrim and worldoftanks. No room shows both the order and the bound.
- No line shows a visitor's call answered by the room's taunts. Not a taunt shows in 32 rooms: the target's or a visitor's taunt, a plain justification or report, restraint, terms, or a jab at one individual. One end or neither shows in 20 rooms, not the room's attack in 17, one act in 10 and the first attack after the close in 1. Other particulars show in 9 rooms, an absent specification in 1, and evidence limits in 334.
- **Rooms once, by priority.** The order 169, the bound 8, one act 10, a visitor's call 0, a taunt after an attack suffered 46, not the room's attack 17, not a taunt 32, one end 19, after the close 1, other 9, specification 1, limit 333 (645 rooms).
- So 177 rooms show an episode (the order or the bound), and the order holds in 169 of them (0.955). With the 10 one-act rooms added, it holds in 169 of 187 (0.904). C2 found 56 of 68 (0.824). Its pass 4 count found 2 of 68 with no taunt after the first attack, and the counterexample response counts 12 of 68 that taunt before any attack. 86 of the 169 order rooms rest on absent rejects whose form and rival the census does not grade.
- **Support transitions and C2's sampled rooms.** rpi's line shows the target's taunt and not the room's (reading 45). anarcho_capitalism's line holds its support transition and shows defence first, a call to remove invaders from the room's own place (reading 9). clg's line shows a taunt after an attack it suffered (reading 22), and C2's audit found its first taunt before its first attack. Of C2's sampled rooms, cardinals shows the order, reddevils and portugal show not a taunt, and nbaspurs shows not the room's attack and an evidence limit. Of A18's subs, unitedkingdom shows the order, with a line of the national anthem aimed at the rival (reading 56).

**No correction (§2), and the wording.** No line is an accepted correction, and no line is paired. The restrict and add conditions say that the order of first acts does not prove a cause, that the taunt can aim at another opponent, that it can answer an attack the room suffers, that rivalry talk can come first or come from outside the canvas, that a claim can go unverified, that the contest can be with one individual or with diffuse opponents, that the call and the taunt can be one act, and that visiting celebrants must be kept apart. A18's connection, its mechanism, its bound and counterexample response, G21's readings, C02 under G4a and G50's readings hold each of them. No line shows the order failing for want of a condition A18 lacks. By class the 89 restrict lines show the order 29 (in the thread 5), the bound 7, and evidence limits 52 (a taunt after an attack suffered 23, not the room's attack 8, not a taunt 8, one end 6, one act 6, after the close 1), with one particular. The 10 add-condition lines show the order 1 and evidence limits 9 (a taunt after an attack suffered 3, one end 3, not the room's attack 2, one act 1). A18 has no add-step line. A18 stands as served, with no move. Under J's answer to QD3-008, I keep A18's words. Four wording questions go to D3c. The gloss names taunts, while 31 of the 80 graded first taunts are claims of victory, one is a salute, and 32 come after hour 73. The mechanism says that the attack makes the rival a named party, while in 9 of the 80 the first taunt aims at another group. The named party also shows in 46 rooms that taunt after an attack they suffer, which the connection does not count. The bound shows alone in 8 of 177 episode rooms on the return's lines, beside the counterexample response's 12 of 68.

**What the instantiate lines show.** Accepted 50: the order answered in the thread 33, and the order by the hours or in a post's words 17. Rejected 66: not a taunt 24, a taunt after an attack the room suffers 20, one end or neither 11, not the room's attack 7, one act 3 and the bound 1. Particular 1, NONPORTABLE: factorio-055, whose concepts show a visitor's salute, so it is not marked PO.

**Absent lines.** 86 claims of absence fail (67 `not-testable`, 19 `unobserved`). Each line's concepts, or the coded posts above them in their reply chain, show the room's call or act against another room's work and, after it, the room's taunt, chant, claim of victory or salute with a rival, classed by the first act of each (reading 122). Ten lines are NONPORTABLE particulars, and three of them show the order and are marked PO (OnePiece-056, alberta-050, esperanto-048). The one observed-absent line, anaheimducks-069, is a specification: it shows an attack call after the close and two refusals, with no taunt. The other 334 are evidence limits. A guard listed 42 limits whose labels name a taunt, an insult, a victory, mockery, a gloat, a chant, a curse, a salute, a jab, a boast, blame or a laugh. Each had been read in the window pass. Each shows a taunt after an attack the room suffers or after its defence, a visitor's or the target's taunt, a taunt before the room's first attack, a call and abuse in one post, a jab at one individual or at no rival group, an exchange inside the room, or a plain account, a jest or a remark.

**Repairs (G7).** Lines in repaired rooms were 0.753 accepted (360 lines), and in unrepaired rooms 0.739 (287 lines). No ruling rests on the difference.

**Carried to later groups.**
- **A18's wording at D3c.** The gloss beside the claims of victory and the taunts after the close; the mechanism's named party beside the 9 ELSE lines and the 46 rooms that taunt after an attack they suffer; the bound's 8 of 177 beside the counterexample response's 12 of 68.
- **The failure clause's second half.** Attacks that draw no taunt can be read in single lines only as one end (20 rooms) or not a taunt (32). They go to D3c with the clause, which A18 records as present.
- **Rivalries from before the canvas.** Three bound lines are marked PRE, and one call cites an old rivalry (purdue-058, reading 95). They go with the carried question of what picks the attack's target (C02).
- **Ungraded absent rejects.** 86 order rooms rest on absent rejects whose form and rival the census does not grade.
- **The re-check (§5).** A18 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 210 quoted segments and 260 hours, in five windows; restrict 160 and 234, in six windows; add-condition 23 and 27; absent 182 and 204, from the 97 rows of thirteen windows. Every segment and hour was found in its own window's quote file. No hour mismatched, and no quote was cut short.
- **Every packet was read whole.** The two draws of ten (seeds 20261016+442 and +542) found 7 order lines answered in the thread, 4 by the hours or in a post's words, 4 not a taunt, 3 a taunt after an attack suffered, 1 not the room's attack and 1 one end. So each packet was read whole, as were all the others.
- **Readings settled while ruling.** Readings 1 to 62 were settled in the instantiate pass, 63 to 115 in the restrict pass, 116 to 121 in the add-condition pass, and 122 to 204 in the absent pass. Amendment 1 was written while the first instantiate window was read, before any line was ruled. After reading 59, the row for sweden-055 was reworded before any build, and its file was checked again with no miss. The log of readings 122 to 128 gave window ab001_000 five rejects and 28 limits; a later note corrects this to four and 29, as the rows give.
- **Draft slips.** One draft instantiate row (drugs-059) closed a quote before a colon, and it was reworded before the checks passed.
- **Shell slips.** Before the opening note, one command was a no-op holding a shell assignment whose name begins with a refused prefix; the guard refused it, and it ran nothing. One later command was a no-op shell assignment of a file path, which ran and changed nothing. One check piped a `mem.py` read into cut; the guard refused it, and it ran nothing. Each was disclosed in the diary when it happened.

### Close-check, D3a-45

`validate.py D3` reports 35,543 of 42,243 ledger lines ruled: the 34,896 before this leg and A18's 647. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 36,316 lines: 647 first rulings from this leg and no re-ruling. Appended re-rulings stay at 773.
- **Pairs.** A18's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-46: A19, upkeep before the coalition

A19 is a standing arrow from C2, P05 → P17, of kind order and strength thin. Its gloss: 'under attack, works defend each other'. Its connection: 'in a room carrying both, the first act of upkeep or defence comes before the first alliance, shared chat, joint mark or request to host'. Its mechanism: 'A room keeping its work against attack joins other rooms whose works face the same threat, and they defend each other's works together.' Its bound: 'Late side: no late room of 4 holds; late rooms enter the canvas through other rooms (bretagne, MiamiHurricanes, yuyuyu).' Pass 4 counted the order in 87 of 121 rooms carrying both (0.719; null mean 0.614, p95 0.678). G51 was written before any line was read, and it has no amendment. Its 112 readings, each logged in the diary, are set out under it by head (above). All 646 lines, in 644 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a19_census.py` and `d3_pair_check.py`. Quotes were checked against `cite.py`'s output by `d3_spec_quotes.py` and `d3_a16_seg_gap.py`, typed hours by `d3_spec_hours.py`, and quotes cut short by `d3_trunc_check.py` (totals by `d3_a19_quote_totals.py`). The writers of the rejected absent lines were checked against their posts in other rooms by `d3_a19_crossauthors.py` and `d3_a19_rej_crosscheck.py`. Every line was read with its reply context (`d3_read_window.py`), and every restrict and add line with its full how (`d3_add_how.py`).

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 69 | 14 | 0 | 0 | 0 | 0 | 55 |
| absent (334 `not-testable`, 143 `unobserved`) | 477 | 0 | 0 | 0 | 456 | 1 | 20 |
| restrict | 91 | 28 | 0 | 0 | 63 | 0 | 0 |
| add-condition | 9 | 3 | 0 | 0 | 6 | 0 | 0 |
| all | 646 | 45 | 0 | 0 | 525 | 1 | 75 |

**What the rooms show (the census, `d3_a19_census.py`).** Its rules were logged before it ran. Each line keeps the class of its latest ruling, and the helper checks every class against the decision and kind written. These are counts of the lines that labelers wrote where they saw both ends. They are not rates in the population.
- **The order, 49 rooms.** The room keeps or defends its own work, and after that it joins, proposes, takes up or acts on a coalition with a named room. In vegan, a member calls 'Defend the homeland in /r/place!' at h+54.47. A reply in its chain at h+57.98 agrees a deal with a neighbour: 'In return for help defending our sign I have agreed to help keep the cube free from rogue pixels' (reading 109). The 49 order lines come from 14 accepted instantiate lines, 15 restrict lines and 20 absent rejects. Ten of them take the first end from a coded post above the line's concepts (R).
- **In the thread, or by the hours.** 18 order lines show the order in the reply chain or thread, and 11 by the hours or in a post's words. The 20 absent rejects are not split. By room, 18 order rooms show it in the thread or chain, 11 only by the hours or in a post's words, and 20 only on an absent reject.
- **The form and the mechanism.** Of the 29 graded order lines, the first coalition act is an alliance (ALLY) in 23, a joint mark (JOINT) in 3, a shared chat (CHAT) in 2 and a hub of kindred rooms (HUB) in 1. None is a tally. 15 of the 29 name an attack, a shared threat or defence given both ways (MW). C2 grounded the arrow on 52 transitions in 28 rooms where an alliance is proposed in reply to a call to defend.
- **The bound's pattern, 18 rooms.** The room's first coalition comes before its first upkeep. In Slovakia, joint flags and a shared chat with a kindred room come before the first call to fight for the flag (reading 28). Of the 18 lines, 2 are instantiate lines, 13 are restrict lines and 3 are add-condition lines. Two are marked ENTRY, since the room enters the canvas through the coalition (purdue, uiowa). The forms tagged on the bound lines are ALLY 7, JOINT 4, HUB 3 and CHAT 1. The other bound rooms are ChronoTrigger, Slovakia, colombia, completeanarchy, daftpunk, greenlattice, lithuania, megaman, nin, parrots, placeportalpattern, placesnek, samuraijack, texas, theitalyplace and yogscast. No room shows both the order and the bound.
- **Other classes.** One act shows in 28 rooms (29 lines). In these, one post holds the defence and the coalition, an ally keeps the work before the members do, or the two are reported at hours that cannot be placed. Hosting is the only second end in 5 rooms (clubpenguin, lego, paladins, rocketbeans, yumenikki). What follows the upkeep is not a coalition in 15 rooms: help one way or traded, a truce, a visitor's offer that no member takes up, or a proposal that names no partner. One end shows in 72 rooms (73 lines). In 12 of them a coalition answers a warning of a coming threat with no upkeep before it (TH), and 7 of the lines are marked ENTRY. One line is a NONPORTABLE particular (hearthstone), and 456 are evidence limits. No line shows a first end that is not the room's upkeep, and none shows a first coalition after the close.
- **Rooms once, by priority.** The order 49, the bound 18, one act 28, hosting only 5, not a coalition 15, not the room's upkeep 0, one end 72, after the close 0, other 1, limit 456 (644 rooms).
- So 67 rooms show an episode (the order or the bound), and the order holds in 49 of them (0.731). With the 28 one-act rooms added, it holds in 49 of 95 (0.516). Pass 4 found 87 of 121 (0.719), and 7 of 121 with no coalition after the first upkeep. The counterexample response counts 51 of 157 rooms that join a coalition before any upkeep (0.325). Here the bound shows alone in 18 of 67 (0.269). 20 of the 49 order rooms rest on absent rejects whose form the census does not grade.
- **Support transitions and C2's sampled rooms.** The criticalrole line shows the order. A member reports that the room was invited into a communal alliance chat, after its upkeep, and its support transition passes the audit (reading 29). naruto, the arrow's lead instance, lists its alliances with no upkeep in its line, so it shows one end (reading 15). The yugioh line is an evidence limit: its work is kept under a host's region and terms (reading 112). lakers and bretagne, the two rooms that failed C2's sample, hold evidence limits. The lakers line holds the r/nbaplace hub with no upkeep shown (reading 93), and the bretagne line holds a visitor's offer or the room's own chat (reading 79). Of the bound's named late rooms, bretagne and MiamiHurricanes hold evidence limits, and yuyuyu has no A19 line.
- **Contrary facts from other rooms.** Two acts in other rooms' records come before halo's first call to protect its work, at h+30.62. A pact naming r/halo was sealed in r/mylittlepony at h+18.62 (reading 96). In r/cowchop, a halo member wrote 'From us at /r/halo, we request peace with your inevitable overlap of our art.' at h+28.83, and offered to restore that room's logo at h+28.99. By the visitor rule these acts stay in those records, so halo-061 stays a reject. They are noted beside the census and not counted.

**No correction (§2), and the wording.** No line is an accepted correction, and no line is paired. The restrict and add conditions say these things: the order of first acts does not prove a cause; no common enemy or threat is shown as the reason; the coalition can come first, let a room enter its spot, or rest on affinity or shared building; an existing alliance can be called on; a room can withdraw from shared defence or stay neutral; hosting and traded help can stand where a coalition is expected; and a coalition can answer a shortage of users or honour a treaty with no threat named. A19's connection, its mechanism, its bound and counterexample response, the falsifier's second clause (recorded present), K02, P07, P08, P16, G27's readings and G51's readings hold each of them. No line shows the order failing for want of a condition A19 lacks. By class, the 91 restrict lines show the order 15 (in the thread 9), the bound 13, and evidence limits 63 (one end 39, one act 11, not a coalition 9, hosting 4). The 9 add-condition lines show the bound 3 and evidence limits 6 (one act 3, not a coalition 1, hosting 1, one end 1). A19 has no add-step or contradict line. A19 stands as served, with no move. Under J's answer to QD3-008, I keep A19's words, and three wording questions go to D3c. First, the connection names a request to host, while pass 4, F-008 and this census count without hosting, and 5 rooms show hosting as the only second end. Second, 12 rooms join a coalition on a warning of a coming threat, with no upkeep before it (TH), while the mechanism names an attack. Third, the bound names late rooms that enter the canvas through other rooms. ENTRY marks 9 rooms, of which 2 show the bound, and the bound's named late rooms show no order. The bound shows alone in 18 of 67 episode rooms, beside the counterexample response's 51 of 157. A fourth matter is a limit of the record, not of the words: statements of existing alliances, and reports after the close, cannot be placed against an earlier upkeep.

**What the instantiate lines show.** Accepted 14: the order in the thread or chain 9, and by the hours or in a post's words 5. Rejected 55: one end 33 (8 marked TH and 1 ENTRY), one act 15, not a coalition 5 and the bound 2. No line is a particular.

**Absent lines.** 20 claims of absence fail (16 `not-testable`, 4 `unobserved`). Each line's concepts, or the coded posts above them in their reply chain, show the room's upkeep or defence of its own work and, after it, the room's coalition, classed by the first act of each (readings 64 and 109). One line is a NONPORTABLE particular, hearthstone-035, and it is not marked PO (reading 88). No line is observed-absent or not-needed. The other 456 are evidence limits. One reject, canada-035, was withdrawn before any build. The same alliance invitation by the same writer stands in r/france, so the writer's side is not shown (reading 83). The writers of the 20 rejects were checked against their posts in other rooms. Five cited concepts are by writers who post elsewhere. In each, the row reads the post as the neighbour's, or the words show the room's side, as in 'From us at /r/halo' (stryking, halo) and 'Russian here' (Outlanov, russia). A guard listed 189 limits whose labels name a tie (alliance, ally, coalition, treaty, pact, joint or together). Each had been read in its window. Each shows the bound's pattern, one act, a statement that cannot be placed, a visitor's or a cross-poster's post, a truce, help one way or traded, hosting, the room's own chat, or one end.

**Repairs (G7).** Lines in repaired rooms were 0.872 accepted (358 lines), and in unrepaired rooms 0.896 (288 lines). The repaired rooms hold more rejects (45 against 30). No ruling rests on the difference.

**Carried to later groups.**
- **A19's wording at D3c.** The request to host in the connection, beside the 5 hosting-only rooms; TH's 12 rooms, beside the mechanism's attack; the bound's late side, beside ENTRY's 9 rooms; and the bound's 18 of 67, beside the counterexample response's 51 of 157.
- **The failure clause's second half.** In single lines, a room under attack that never joins with another can be read only as one end (72 rooms) or not a coalition (15). These go to D3c with the clause, which A19 records as present.
- **Hubs announced across rooms.** Hub makers announced r/nbaplace, r/phillyplace and r/716Place in several team or city subs. By G50 reading 108, such an announcement is not the room's act (readings 93, 103 and 111). These go with P17's carried question of prior ties and colour faiths that choose allies (C02).
- **Contrary facts.** The two acts in other rooms' records before halo's own call go to the verdicts leg with halo.
- **Ungraded absent rejects.** 20 order rooms rest on absent rejects whose form the census does not grade.
- **The re-check (§5).** A19 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 122 quoted segments and 149 hours, in three windows; restrict 213 and 243, in six windows; add-condition 24 and 26; absent 42 and 48, from the 21 rows of fifteen windows. Every segment and hour was found in its windows' quote files or in the 13 cites files. No hour mismatched, and no quote was cut short.
- **Every packet was read whole.** The draw of ten (seed 20261016+487) found 4 lines with one end, 3 with the order by the hours or in a post's words, 1 one act, 1 the bound and 1 not a coalition. So the packet was read whole, as were all the others.
- **Readings settled while ruling.** Readings 1 to 23 were settled in the instantiate pass, 24 to 59 in the restrict pass, 60 to 63 in the add-condition pass, and 64 to 112 in the absent pass. Two logs gave wrong closing tallies, and later notes correct them: window i487_000 holds O-A 4 and O-H 4, and the absent pass holds 20 rejects and 456 limits. The second tally was typed before a script counted it. Reading 69, applied backwards, re-ruled three written lines. The author check made after reading 93 found the warriors-049 and gatech-049 rulings resting on a cross-poster, and both were re-ruled by appended lines. A check under reading 83 withdrew canada-035's reject before any build.
- **Build slips.** The restrict packet was first written from the verb offset with `--op restrict`, which counts within the op, and it held no line. It was overwritten from op offset 0 before any read. The add-condition build first omitted `--op add-condition`, and the script refused it. One draft add row (suomi-049) closed a quote before a colon, and it was reworded before the checks. `d3_a19_quote_totals.py` first passed several quote files to `d3_a16_seg_gap.py`, which takes one, so it was edited and rerun.
- **Shell slips.** One command held a heredoc and a no-op, and the guard refused it. One check piped a helper's output into cut. The guard refused it, and the rerun had no cut. Four commands ran with a needless shell assignment or a no-op and changed nothing. The first set a variable before an echo, and the second set one before a quote check. The third listed files, changed the working directory, and ended with an assignment whose name begins with a refused prefix. The fourth was a placeholder of the same form. The working directory was set back at once. Each slip was disclosed in the diary when it happened.

### Close-check, D3a-46

`validate.py D3` reports 36,189 of 42,243 ledger lines ruled: the 35,543 before this leg and A19's 646. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 36,967 lines: 646 first rulings and 5 re-rulings from this leg. Appended re-rulings now number 778.
- **Pairs.** A19's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.

## D3a-47: A20, the call before the host sub's line

A20 is a standing arrow from C2, P01 → P20, of kind order and strength strong. Its gloss: 'calls flood the host sub, and the host draws a line'. Its connection says that the room's first call to the canvas comes before the first line the host sub draws around canvas talk. Its mechanism says that the calls flood the host sub, and that its moderators or members answer with one thread, removals or a canvas sub. Its failure clause names a line drawn before any call, or a line whose words name no flood, and the arrow records this failure as present. C2 counted the order in 132 of 155 rooms carrying both (0.852; null mean 0.538, p95 0.594). G52 was written before any line was read. Its one amendment was written before any line was ruled, and it applies to every line. Its 105 readings, each logged in the diary, are set out under it by head (above). All 700 lines, in 690 rooms, are ruled, and none is pending. Counts are from `_analysis/d3_group_close.py`, `d3_opkind.py`, `d3_a20_census.py` and `d3_pair_check.py`. Quotes were checked against `cite.py`'s output by `d3_spec_quotes.py` and `d3_a16_seg_gap.py`, typed hours by `d3_spec_hours.py`, and quotes cut short by `d3_trunc_check.py` (totals by `d3_a20_quote_totals.py`). The order each absent reject states was checked by `d3_a20_absent_order_check.py`. Every line was read with its reply context (`d3_read_window.py`), and every restrict and add line with its full how (`d3_add_how.py`).

| op | lines | specification | elaboration | correction | evidence limit (kind none) | particular | reject |
|---|---|---|---|---|---|---|---|
| instantiate | 120 | 39 | 0 | 0 | 0 | 1 | 80 |
| absent (241 `not-testable`, 193 `unobserved`) | 434 | 0 | 0 | 0 | 376 | 1 | 57 |
| restrict | 134 | 53 | 0 | 0 | 81 | 0 | 0 |
| add-condition | 12 | 3 | 0 | 0 | 9 | 0 | 0 |
| all | 700 | 95 | 0 | 0 | 466 | 2 | 137 |

**What the rooms show (the census, `d3_a20_census.py`).** Its rules were logged before it ran. Each line keeps the class of its latest ruling, and the helper checks every class against the decision and kind written. These are counts of the lines that labelers wrote where they saw both ends. They are not rates in the population.
- **The order, 148 rooms.** A call to place is posted in the room, and after it the host sub draws a line around canvas talk. In iceland, a member writes at h+20.11 to those who want to lend a hand on the canvas. At h+69.13, a new thread says: 'Please keep all /r/place related discussions here. Individual threads will be deleted.' (reading 85). The 149 order lines come from 40 instantiate lines (one of them math-034's particular, marked PO), 49 restrict lines, 3 add-condition lines and 57 absent rejects. 51 of them take the first end from a coded post above the line's concepts (R).
- **In the chain, or by the hours.** 82 order lines show the order in the reply chain or thread, 66 by the hours or in a post's words, and one is the PO particular. By room, 81 order rooms show it in the chain or thread, and 67 only by the hours or in a post's words.
- **The flood in words.** In 97 order lines, in 97 rooms, the first line answers canvas posts (MW): it routes, removes, gathers or objects to them, or names their number. In 52 lines, in 51 rooms, it answers no flood (NF): a sticky asked for or made so that members can see the work, a pinned call, a paused thread, or a judgment of the canvas's worth. In scotland, a member asks at h+23.68 to pin the room's own call, posted at h+23.01, so that the troops rally (reading 19). 51 of the 148 order rooms have NF order lines only (0.345). The mechanism names a flood, and it does not reach these rooms.
- **The close.** In 11 order rooms the first line comes after hour 73, after a call made while the canvas ran (AC). In transformers, a member calls the canvas a matter of bragging rights at h+80.40, after the room's calls (reading 100). Before hour 73, the order holds in 137 of 153 episode rooms (0.895). Pass 4 counted the calls before the whole line in 122 of 144 rooms before hour 73.
- **Visitors.** In 3 order rooms the first call is a visitor's or a kindred group's (VC: chicago, msu, thenetherlands).
- **The bound's pattern, 16 rooms.** The host sub's first line comes before the room's first coded call. In sweden, a member dismisses the canvas at h+23.12, and the first call comes at h+67.93 (reading 25). Of the 16 lines, 12 are instantiate lines and 4 are restrict lines. The bound rooms are argentina, babymetal, chicubs, czech, finland, fireemblem, lebanon, masseffect, monero, monsterhunter, pitt, pokemon, smite, sweden, switzerland and trees. No room shows both the order and the bound.
- **Other classes.** One act shows in 16 rooms (17 lines). In these, one post holds the call and the line, a removal notice is the only record of the call (RM, magictcg), or a reply points the call to a sticky or megathread made at an hour the record does not show. What follows the call is not the host sub's line in 25 rooms (26 lines): moderation as such, coordination with no line stated, or another sub's line. One end shows in 106 rooms (110 lines). In 5 rooms the only call comes after the close (AFTER). One line is a NONPORTABLE particular (counting-034), and 376 are evidence limits. No line shows a first end that is not a call.
- **Rooms once, by priority.** The order 148, the bound 16, one act 15, not a call 0, not the host sub's line 25, one end 105, after the close 5, other 1, limit 375 (690 rooms).
- So 164 rooms show an episode (the order or the bound), and the order holds in 148 of them (0.902). With the 15 one-act rooms added, it holds in 148 of 179 (0.827). C2 counted 132 of 155 (0.852), and pass 4 found 5 of 155 with no line after the first call. The counterexample response counts 23 of 155 rooms that draw the line first (0.148). Here the bound shows alone in 16 of 164 (0.098).
- **Support transitions and C2's sampled rooms.** The rocketleague line shows the order in the thread, and its support transition passes (reading 22). nintendo's two lines are one act. In nintendo-063, a reply points a visitor's call to a megathread already made, and the line was re-ruled to J after the scan. nintendo-064 holds C2's audited transition, c0120 to c0121, which points a call to the room's existing megathread (reading 63). The france line shows one end (reading 12). Of C2's sampled rooms, transformers, darksouls and crusaderkings show the order. The transformers line is marked NF and AC, as C2 read the room as a failure of the mechanism. The rotmg line shows one end: objections and a removal rule with no call coded (reading 58).

**No correction (§2), and the wording.** No line is an accepted correction, and no line is paired. The restrict and add conditions say these things: the order of first acts does not prove a cause; no flood of calls is shown as the reason; the line can come before any call; the line can answer no flood, as a sticky for visibility or a judgment of worth; the line can be the sub's standing policy or its own norms; a removal can follow a format rule; and a pointer to a sticky already made cannot be placed against the call. A20's connection, its bound and counterexample response, the falsifier's second clause (recorded present), G26's readings and G52's readings hold each of them. No line shows the order failing for want of a condition A20 lacks. By class, the 134 restrict lines show the order 49 (in the thread 32), the bound 4, and evidence limits 81 (one end 46, not the host sub's line 23, one act 10, after the close 2). The 12 add-condition lines show the order 3, and evidence limits 9 (one end 6, one act 2, not the host sub's line 1). A20 has no add-step or contradict line. A20 stands as served, with no move. Under J's answer to QD3-008, I keep A20's words, and three wording questions go to D3c. First, the mechanism names a flood, while 51 of the 148 order rooms show only first lines that answer no flood. Second, the connection counts a dismissal of the canvas, and the census reads worth remarks as the host's line, including remarks by members who join in the same post (uofm, kurdistan) and judgments after the close. Third, the bound shows alone in 16 of 164 episode rooms, beside the counterexample response's 23 of 155. A fourth matter is a limit of the record, not of the words: a reply that points a call to a sticky already made cannot be dated against the call, so 17 lines are one act, and nintendo's audited transition is one of them.

**What the instantiate lines show.** Accepted 39: the order in the chain or thread 28, and by the hours or in a post's words 11. Rejected 80: one end 58, the bound 12, one act 5, a first call only after the close 3, and not the host sub's line 2. One line is a particular, math-034, marked PO.

**Absent lines.** 57 claims of absence fail (40 `not-testable`, 17 `unobserved`). Each line's concepts, or the coded posts above them in their reply chain, show a call posted in the room and, after it, the host sub's line, classed by the first act of each (reading 67). By the census tags, 31 of these first lines answer canvas posts (MW) and 26 answer no flood (NF); 15 take the first end from a post above (R), and 6 come after the close (AC). All 57 state the call before the line (`d3_a20_absent_order_check.py`). One line is a NONPORTABLE particular, counting-034, and it is not marked PO (reading 80). No line is observed-absent or not-needed. The other 376 are evidence limits. A guard listed 89 limits whose labels name a megathread, a sticky, a pin, a removal, a deletion, a ban, a rule, spam, a flood or moderators. Each had been read in its window, and `d3_guard_named.py` finds every one of them named in a logged reading. Each shows moderation as such, coordination, the sub's own April Fools joke, a canvas-born room's venue, another sub's line, a line with no coded call, a line before the first call, or a pointer to a sticky made at an hour the record does not show.

**Repairs (G7).** Lines in repaired rooms were 0.795 accepted (381 lines), and in unrepaired rooms 0.809 (319 lines). The repaired rooms hold more rejects (77 against 60). No ruling rests on the difference.

**Carried to later groups.**
- **A20's wording at D3c.** The mechanism's flood, beside NF's 51 rooms; worth remarks by members who take part, as the host's line; and the bound's 16 of 164, beside the counterexample response's 23 of 155.
- **The dating of stickies.** A pointer to a sticky or megathread already made reports a line at an hour the record does not show. This holds 17 one-act lines and nintendo's audited transition (reading 23).
- **P20's carried questions.** Canvas-born rooms, whose own venues draw no line; removals that send talk elsewhere; and the clock, with 11 AC rooms. These go with G26's readings.
- **The re-check (§5).** A20 is not rewritten, so it adds no room to the re-check.

**Disclosed limits and slips.**
- **Quotes read.** Instantiate 210 quoted segments and 245 hours, in five windows; restrict 254 and 290, in nine windows; add-condition 18 and 24; absent 114 and 123, from the 58 rows of thirteen windows. Every segment and hour was found in its windows' quote files or in the 26 cites files. No hour mismatched, and no quote was cut short.
- **Every packet was read whole.** The draw of ten from the 100-line instantiate packet (seed 20261016+447) found 4 lines with one end, 3 with the order in the thread, 1 by the hours, 1 the bound and 1 one act. The draw from the 20-line packet (seed 20261016+547) found 6 with one end, 2 the bound, 1 the order in the thread and 1 one act. So both packets were read whole, as were all the others.
- **Readings settled while ruling.** Readings 1 to 26 were settled in the instantiate pass, 27 to 62 in the restrict pass, 63 to 66 in the add-condition pass, and 67 to 105 in the absent pass. Two logs gave window r567_000's counts as typed, and both were wrong. A later note corrects them by script, and from then on every logged count came from a script. Reading 23 moved pokemon-046 and singapore-044 to J before the build, by superseding files. A scan after reading 66 read the 92 written order rows for the same kind of reply. 45 had a concept that names a megathread, a sticky or a pinned or existing thread, and one of them, nintendo-063, was re-ruled by an appended line.
- **Build slips.** The absent windows' build ran past the foreground limit and finished in the background, with exit code 0, while the first window was read. Nothing was written to the windows meanwhile. One absent row (coldplay-059) ended a quote next to a word with an apostrophe, and it was reworded before the counts were logged. Two edits to the census script were sent in parallel. Both applied, and the census was run again before its counts were logged. `d3_spec_counts.py` now counts reject rows among the rows that need a tag.
- **Shell slips.** Two commands held a needless shell assignment and changed nothing. The first was a placeholder whose name begins with a refused prefix. The second set a variable before a quote check. Each slip was disclosed in the diary when it happened.

### Close-check, D3a-47

`validate.py D3` reports 36,889 of 42,243 ledger lines ruled: the 36,189 before this leg and A20's 700. It reports 0 errors and the same 2 old warnings on the move name 'stabilizing' (the first on history line 137).
- **The ledger** holds 37,668 lines: 700 first rulings and 1 re-ruling from this leg. Appended re-rulings now number 779.
- **Pairs.** A20's files hold no pair (`d3_pair_check.py`). Across the ledger, 1,247 accepted elaborations are checked, and the same 7 older ones pair with a line of another kind (`d3_pair_kind_check.py`).
- **The other ledgers.** History holds 150 lines, elements 30, arrows 21, findings 37 and tier history 561. Both hashes are unchanged (elements 47ff7a11…, arrows ff0b3963…).
- **Questions.** None is open.
