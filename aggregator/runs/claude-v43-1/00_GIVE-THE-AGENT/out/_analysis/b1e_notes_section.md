

## Leg B1e, the scheme standing, 2026-10-11

The leg wrote the shipped scheme from the working grouping. It wrote a gate, discriminators, varies, is_not and exemplars for each of the 197 themes, set every theme in one of 21 families, read the floor, and ran the hand-over checks of section 7. No theme was merged, split or dropped. The leg ran across one compaction.

**What was written.**
- `scheme.jsonl`: 197 themes, 183 main and 14 rare, each with every field of section 4. 578 exemplars through `cite.py`: 187 themes have three, 7 have two and 3 have one.
- `families.jsonl`: 21 families. `scheme.md`: an index page listing every family with its themes' names and glosses, then every family's themes in full.
- `confusions.md`: 17 ranked pairs, an exposing second-order theme for each, a family boundary to test, and an estimate on the hardest pair.
- `findings.jsonl`: opened with F-001, the scheme's claim in rule 14's form.
- `tier_history.jsonl`: 129 lines added (124 to 252), 115 `relabelled` and 14 `moved_to_rare`.
- `saturation-B1.md`: a closing section on how the second pass stopped.
- `handback-B1.md` and `out/interview/B1e.md`.
- Working files in `out/_analysis/`: `b1e_method.md`, the 21 drafts `b1e_draft_G01.jsonl` to `b1e_draft_G21.jsonl`, `b1e_families.tsv`, `b1e_floor.tsv`, `b1e_relabels.tsv`, `b1e_two_or_half.md`, `b1e_running_dropped.tsv`, the packet pages in `b1e_packets/` (before the last reassembly) and `b1e_packets2/` (after it), and the scripts named below.

**How the gates were written.** One family at a time. For each theme, `b1e_digest.py` printed its trigger, its rooms, its rule 0 partners, its tier history and a seeded sample of members. `b1e_cands.py` printed seeded candidate concepts, filtered by the gate's own words where that helped. Every quote was confirmed as a substring of the concept's words through `cite.py` (`b1e_cite.py`). `b1e_check_draft.py` checked each draft's fields, name length, problem words, family, discriminator ids and quotes. Families were revised during drafting for what a reader would confuse; each move is in the diary.

**The gate questions the second pass left, as settled.**
- T3-188 takes an outside room's denial when it separates its organised members from placers acting in its name. A bare "it was not us" that points to another room is tracing (T3-087). Members doubting that damage was their room's own are also tracing.
- T3-146 takes hate symbols and slurs. Obscene drawings and ordinary insults that are covered are repair (T3-021).
- Glitches: explaining one is T3-016, placing beyond the limit with one is T3-088, coping with one is T3-074.
- T3-099 keeps the protected side only. A host-side kind for protection given was weighed and set aside: in every case met, protection given reads as help sent (T3-011) or an alliance (T3-150).
- T3-027 takes bot rumours and claims that a defence was scripts when fairness is in question.
- T3-081 excludes game-fandom wars with no national history.
- T3-054 takes either answer to a successor canvas. T3-117 takes registering the end and hoping the event returns. T3-073 takes live reports.
- T3-002 takes calls to placers who are not yet a group. T3-126 takes saying that no one can speak for the placers.
- The discriminators the head owed are written into both gates of each pair, as `b1e_disc_pairs.py` checked: T3-068/T3-061/T3-006, T3-010/T3-149/T3-151, T3-024/T3-010, T3-046/T3-076, T3-003/T3-038, T3-044/T3-082, T3-074/T3-136, T3-037/T3-098, T3-073/T3-038, T3-188/T3-076/T3-195, T3-188/T3-087, T3-016/T3-074, T3-070/T3-091, T3-120/T3-088, T3-050/T3-017 and T3-168/T3-024. Six of them were missing in one or both directions after drafting, and `b1e_add_disc.py` added 10 questions before the last reassembly.
- 115 names changed; each change has a `relabelled` line. The head's listed changes are among them.

Before assembly, 42 gate fields named legs, room theme ids, concept ids or the notes. Strangers are given none of these, so each field was rewritten in words (`b1e_fix_fields.py`). `b1e_assemble.py` cut rule 0 and bag line counts from 32 fields. Counts stay in the working files and in `confusions.md`.

**The floor and the tiers.** `b1e_floor.py` read the floor for all 197 themes against `episodes-B1.jsonl`, counting rooms that tell one episode as one, and the store's items in the window.
- 181 themes rest on a pair of rooms at least twice apart in size and not joined by an episode. Pairs with exemplar rooms came first.
- T3-173 rests on form: GreenCorner is a sub made on the canvas for a colour faction; AprilKnights is an order carried over from the 2015 Button event. T3-189 rests on form: scp is a sub whose members write the fiction together; parahumans is the fan sub of one author's web serial. No pair of their rooms is twice apart in size.
- 14 rare. Thirteen were seen in one room: T3-007, T3-025, T3-067, T3-077, T3-093, T3-106, T3-133, T3-144, T3-161, T3-166, T3-186, T3-191, T3-197. T3-128 was seen in three rooms (PurplePixels, destiny, ice_poseidon) that tell one episode, E1132. The validator warns that it is rare on three rooms; this is the reason.
- T3-007 and T3-077 each have a second room's concept, named in the head (parahumans c0007, in a bag; PlaceNL c0087), but scheme_current.jsonl does not place those second-order themes on them. They ship rare by the file.

**Moves.** Two moves were logged with `--kind move` and snapped: asking questions (115 relabels, `B1-move-asking-questions-1`) and relating or contrasting (the floor and 14 rare, `B1-move-relating-or-contrasting-1`).

**What the second-order themes showed that the notes did not predict.**
- `prior.md` expected 250 to 450 kinds. The walk made 197, below the low end. The notes' families were each one kind or a few, not the many the prior expected once split by how a thing was done; kinds were not split by degree.
- The prior named deals between rooms as one family. It did not predict that one second-order theme about a neighbour would so often hold four or more kinds at once. Themes touching G13, G14 or G15 sit on one kind in 36.0% of cases, against 54.1% for the rest (`b1e_kinds_per_theme.py`).
- How many kinds a second-order theme needs follows its grain. At five concepts or fewer, 70.4% sit on one kind; at six to twenty, 35 to 38% do. Above forty concepts the share rises again (61.8%), because bags keep one kind and name the rest. canucks (40 themes, about 5 concepts each) has every theme on one kind; turkey (14 themes, about 19 concepts each) has 13 of 14 on two or three.
- The three kinds the prior said the material would refuse held as predicted. Deliberation off the record appears only as a decision brought back (T3-152). Reward and motive are thin (T3-159, T3-110). The canvas as outcome is absent: canvas facts were dropped from the running file and no kind rests on the atlas.

**Themes rejected, and why.** 17 of the 214 ideas were never minted (`b1e_ideas_unminted.py`). Each trigger's doing is held by existing kinds:
- hijacking a rival's script (detroitlions t10): T3-006, with T3-028 named in its bag;
- calling from comments when the sub's posts are closed (ontario t01): T3-020, T3-033, T3-070; the venue varies, the call does not;
- making a mark because rivals have one (baylor t03): T3-033;
- reusing another room's script (wildhockey t02): T3-028;
- answering an insult with goodwill (bulgaria t06): T3-050;
- guarding an ally's flag while it sleeps (argentina t06): T3-150, with T3-141 and T3-011 in its bag;
- watching the canvas on a livestream (twitch t08): T3-016;
- redirecting requests to specialist rooms (anime t12): T3-062, T3-137;
- closing the canvas sub after the end (heyyea t11): T3-117, and now T3-111's gate;
- declining to start again after the end (aoe2 t11): T3-054, which now takes either answer;
- performing state offices in the room's canvas war (indonesia t07): T3-081;
- striking where the defence is weak (theblackvoid t08): T3-006 and T3-020;
- posting slurs and taboo material on the joke day (ultrahardcore t07): T3-031 and T3-182; offensive joking stays in T3-031, and arguing over it is T3-143;
- reporting the live canvas (france t09): T3-073, which now takes live reports;
- conceding placers ignore the plan (PlaceNL t11): T3-188;
- gathering lone placers together (rainbowgrid t02): T3-002, T3-090, T3-126; a kind would split T3-002 by degree (B1d-07);
- planning the room's pixel operations (france t05): T3-070.

Weighed at B1e and set aside: a host-side kind for protection given (T3-011 or T3-150 hold it); political slogans as a kind (T3-033 holds them); veiled fascist emblems as a kind (T3-113 holds them, named plainly in its gate).

### Before handing over (section 7)

**The stranger test.** I read only the gates and discriminators of T3-005, T3-021 and T3-087. `b1e_stranger_draw.py` drew five second-order themes, seeded, from the 689 members of the three. The draw left out rooms of the second pass and the three themes' exemplar rooms. Placed from the gates:
- thesimpsons t11 (asking allies to fight red and celebrating together): T3-005. The request to an ally to call off aligned placers is a kind none of the three gates holds (T3-084 or T3-139).
- littlewitchacademia t08 (keeping the witches around): T3-021, with no hesitation. Handing upkeep over at bedtime looks like T3-141, which I did not hold.
- vegan t08 (defending vegan signs from repeated overwriting): T3-005. I hesitated over whether its repair concepts (c0177, c0181) earn T3-021. The working grouping did not add it.
- palestine t04 (defending, repairing and holding the flag): T3-005 with T3-021 (c0073). I hesitated over c0074, a member messaging the placers laying blue dots, which none of the three gates holds.
- WPI t05 (stopping others from taking the logo): T3-005 with T3-087. I hesitated over whether a warning that a named room wants the logo is tracing when the source is already known.

All five primaries match the working placements. The test was not blind: `mem.py theme` prints the working placements above the concepts, and they were in view.

**The ten biggest bags** (second-order themes ranked by the concepts under them; stage B3 flags them so readers place them from the concepts):
1. leagueoflegends t02, 798 concepts, T3-023: Turning Marc Merrill into the room's lord and savior
2. theblackvoid t09, 389 concepts, T3-006, T3-080, T3-085: Calling attacks on named targets
3. ainbowroad t11, 361 concepts, T3-035, T3-084, T3-139: Petitioning the road for room, help, or protection
4. 2007scape t04, 349 concepts, T3-038: Building from coordinates, grids, and progress calls
5. theblackvoid t12, 335 concepts, T3-031, T3-163, T3-174: Hailing and embodying the Void
6. ainbowroad t04, 327 concepts, T3-021: Repairing and defending the road and nearby art
7. ainbowroad t03, 326 concepts, T3-005: Warning about and fighting attacks
8. dota2 t05, 314 concepts, T3-023, T3-032: Turning the subreddit into r/tz and playing along
9. ainbowroad t07, 311 concepts, T3-038, T3-041, T3-160: Extending strands and building road projects
10. sweden t01, 310 concepts, T3-065: Building, repairing, and decorating the shared canvas

**Running-file entries dropped.** All 769 entries of `running-A1.md` were read. 601 name a doing, and the kinds whose gates take it carry it. 168 are dropped; each is listed with its reason in `out/_analysis/b1e_running_dropped.tsv`:
- canvas, 51: facts from the canvas record (linked artworks, writers' shares, placements before hour 0, the atlas). They are measured from pixels, not told in the rooms' words, and the canvas fields carry them.
- record, 61: remarks about the A1 reading itself (block markers, sides of a block, corrections, notes an account weakened, accounts that disagree). The doings they mention, such as attack talk in a room read as restrained, are carried by their kinds.
- share, 15: a share of a room's coded record (April Fools filling most turns, one member writing most). The store's facts and stage C1's counts carry them.
- brief, 33: the room's week before the canvas as the source of a word, mark or habit. This is outside the window B1 places; T3-031 and T3-033 carry the canvas talk that uses it.
- sequence, 8: an order of events over the week. This is sequencing, for stage C.

**Token sizes, and what was cut.** Tokens are estimated as bytes over four; no tokenizer was run.
- `scheme.md`: 341,571 bytes and 57,990 words, about 85,400 tokens. Its 197 exemplar lines are 56,510 bytes and 8,991 words, about 14,100 tokens. Its index section (lines 1 to 268) is 31,904 bytes and 5,418 words, about 8,000 tokens.
- The index page the harness serves (`packets.py scheme`, built to `out/_analysis/b1e_packets2/index.md` after the last reassembly): 33,148 bytes and 5,455 words, about 8,300 tokens.
- One family page: 6,566 bytes (G12) to 16,448 bytes (G21), about 1,600 to 4,100 tokens. A reader holding the index and one family page holds about 10,000 to 12,400 tokens.
- Cut to get there: the working labels and the two-or-half arguments moved to the notes; rule 0 and bag line counts cut from 32 fields; leg names, room theme ids and concept ids rewritten out of 42 fields; exemplars withheld from the packet pages, which is `packets.py`'s default.
- Not cut: `scheme.md` keeps every exemplar for a human reader.

**Size distribution** (second-order themes per theme, `b1e_rooms_fit.py`): minimum 1, quartiles 7, 26 and 91, maximum 532, mean 68.2. By band: 1 member, 11 themes; 2 to 9, 49; 10 to 24, 37; 25 to 49, 23; 50 to 99, 36; 100 to 199, 25; 200 to 399, 13; 400 or more, 3. The largest themes are T3-009 (532), T3-010 (444), T3-005 (429), T3-031 (390), T3-002 (385), T3-001 (380), T3-021 (357) and T3-004 (347). None holds one in ten of the 7,786 placed second-order themes; T3-009 holds 6.8%. T3-009 was read member by member at B1b-06, four kinds were split out of it, and the PI kept the rest whole at B1b-20. Its gate now writes out its variation, from a one-line "we did it" to long posts with the final image, pride and thanks.

**Families.** 21. The largest is G21, after the canvas closed (15 themes); then G15, pacts and envoys between rooms (13); then G02 and G14 (12 each). The smallest are G09 and G12 (6 each).

**The one second-order theme the scheme handles badly.** argentina t06, "making and contesting pixel alliances". It holds T3-150, and its bag names seven more kinds: T3-149, T3-011, T3-079, T3-078, T3-141, T3-126 and T3-081. One stretch of talk about allies does eight things the scheme keeps apart: a truce, help, a joint flag, help to kin nations' flags, a night watch for an ally, who speaks for the room, and the fight cast as national history. A reader holding one family's tests cannot place it whole.

**Faults and slips this leg.**
- After the compaction, the G19 draft was written and checked once before the head and the stage file were read again. The reconciliation line followed, and the G19 labels were then checked against `scheme_current.jsonl`.
- The G20 draft's write and its check ran in one turn. The check read the written file and passed.
- A first draft of the `saturation-B1.md` closing paragraph named stretches 6 and 7 with a room count typed from memory. It was checked against the stretch table and corrected (stretches 1 and 2, 21 and 24 rooms) before it was logged.
- The guard refused two jq commands (one with chained `or` selects and a field print; one with a jq variable and a redirect), a python heredoc and a jq `test()` filter. Each was redone with grep or a script file.
- After `scheme.jsonl` was written, `mem.py scheme <T3>` serves the shipped scheme without members, so `b1e_digest.py` printed members 0. Member lists after that point were read from `scheme_current.jsonl` with jq.
- Left from B1d and not taken up at B1e: the 107 episode lines whose kinds none of their rooms holds; seven pairs of lines telling one event; E989; the cfb and finland records; shared-member counts that may include AutoModerator; the 76 T3-005/T3-021 themes; T3-149 and T3-150 members that may hold T3-195; and the kinds left out of bags. B1e wrote gates and did not re-place members. These go to stage B2 in the handback.

