# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-01, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Leg A1b-01 read block 01 whole: 53 of 53 rooms have a note in `out/rooms/`. 652 rooms remain, in blocks 02 to 19. The next leg is A1b-02. The next room is the one `mem.py next` names; at this close it names r/placecanada, the first room of block 02. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count. Block 13 is r/counting alone, at 11.17 MB.

`validate.py A1` at this close: 0 errors, 0 warnings. 53 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed at B3.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh, not yet filed: two rooms' linked artworks show region placements before hour 0 (r/FloydVsVoid from h-14.47, r/ProfessorLayton from h-13.49, with a burst there). The canvas window runs from -16, so this may be by design. Check `package/DATA-manifest-canvas.md` through the verbs before filing it.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- concept_reach_threshold: 0 items. QA1-001 is still open with the principal investigator (checked at this close; no answer).
- `n_off_platform`: median 4, max 88 (dankmemes).
- `px_window_share`: median 0.111, max 0.547; null for tenma.
- Concentration is null in 3 rooms (nonbinary, oltp, wario).
- 79 rooms have their last coded turn before hour 73.

## The onset contrast

`out/contrast.md`. Early: first coded turn before hour 3, 131 rooms. Late: first coded turn after hour 48, 61 rooms. The confound is size (median items 5067 against 33). A held-size comparison (items 156 to 2770, 41 against 12) travels with it. Expectation: late rooms organize around finding space on a full canvas; early rooms around claiming and holding it.

Block 01 gave a first look. Late-onset rooms in block 01 (mamamoo h62, TheAdventuresofTintin h68, uva h47.8, auburn h29 then h61, drumcorps h51, qotsa h54, httyd h41, littlewitchacademia h49) all talk about space: negotiated corners, moves on request, resizing to the gap, refused spots. Early-onset rooms (tagpro h0.3, drugs h1.5, babymetal h3.7, cfb h4, the_pack h3.8) talk about holding, defence, shifts and scripts. This fits the expectation. It is not yet tested against size.

## What the first block showed against the three sentences

The three sentences written before reading: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The burst is often late, and the artwork was often there before the room spoke. In most block-01 rooms the linked artwork shows placements from hour 1 or 2, while the room's first canvas talk comes hours or days later (madokamagica, PinkVomitMonster, watchmen, TheAdventuresofTintin, mamamoo, buffalowizards, tokyo and others). The room joins, adopts or only notices work begun elsewhere. The canvas fields do not say who placed the early pixels.
2. Coordinating turns mostly end between hours 59 and 73, not exactly at 73. Several rooms keep organizing on successor canvases after 73 (greyblob, megaman, homestuck, terraria, calgaryflames). Small late rooms end when their build is done (Dustforce h62, uvic h59, buffalowizards h50).
3. Fights are with canvas neighbours, but rivals from outside the canvas also come in: school against school (cfb, uva, uvic), club against club (liverpoolfc and reddevils, later a truce). Deals about space are the most common coordinating act.
4. Deals are struck off the thread and reported back as done. Discord or chat treaties appear in madokamagica, babymetal, PinkVomitMonster, mamamoo, drugs, wales, cfb, FloydVsVoid. The public record holds the report, not the bargaining.
5. The goal is often set late, by one member, and changed by neighbours: moves on request (jerma985, necrodancer, qotsa), resizing to fit (httyd, drumcorps, littlewitchacademia), shrinking to a tiny mark (auburn).
6. Not predicted: in many rooms the room's own April Fools joke fills more coded turns than the canvas (monstercat, cfb, drumcorps, bahrain, strangerthings, babymetal, liverpoolfc's blue prank). The coders coded it. B1 must decide how it bears on organizing.
7. Not predicted: moderators herd canvas talk into one thread or remove it (liverpoolfc, madokamagica, babymetal, anime, drugs). In some rooms the moderators were the organisers (strangerthings, babymetal, cfb); in others they resisted.

## Contrary rooms

- morrowind and megaman: members said they were not organized.
- heyyea: a late keeper of art it did not make.
- egypt: the surviving flag was a stranger's gift.
- duckgame: mourned art that the atlas lists as surviving.
- AprilKnights: an existing order with elections.
- flashtv: the moderators' prank ran apart from the canvas work.
- PinkVomitMonster: a sub made for a figure already on the canvas; members called its lack of coordination its beauty.
- FloydVsVoid: the founder said he was wrong not to compromise with the Void; the prism survived through deals.
- anime: a huge room that mostly refused, routed or argued credit; its one sustained effort ran in a side thread with a crypto sub's script.
- watchmen and TheAdventuresofTintin: rooms that noticed art they did not visibly build.
- tagpro: the stated aim from the first hour was advertising, and members counted subscribers.
- the canvas fields and the room disagree: anime (Emilia not linked), qotsa (atlas keeps the first attempt, not the relocated icon), cfb (room said the logo was lost; atlas keeps a College Football entry), drugs (BOOF IT lost, list kept).
- Earlier, from the screen: UNLincoln, yerbamate, Redox, azores, archlinux.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 02:
- joining work begun elsewhere, against starting it;
- organizing in the thread, against organizing elsewhere and reporting back;
- a room's own rivals, against canvas neighbours;
- the room's April Fools practice, against its canvas practice.

## The last rooms read

Block 01, in order of reading after the last compaction: liverpoolfc, monstercat, madokamagica, bahrain, mamamoo, strangerthings, babymetal, auburn, PinkVomitMonster, the_pack, anime, FloydVsVoid, wales, cfb, watchmen, ProfessorLayton, TheAdventuresofTintin, buffalowizards, lofihiphop, drugs, uva, qotsa, drumcorps, Dustforce, tagpro, uvic.

## Ledgers at this close

- `lexicon-A1.md`: about 190 entries. `running-A1.md`: about 100 entries. `leads-A1.jsonl`: 75 lines, all naming rooms of the frame. Four ties to groups outside the frame (exmormon, the_fack, unc, nerdfighters) were removed from leads and stay in the room notes.
- Diary third-time notes logged: art placed before the room's call; organizing after h73 on successor canvases; treaties reported back from Discord; moderators herding canvas talk; April Fools outweighing canvas talk; the atlas naming a different work.

## The next comparison

In block 02, for every room: did the artwork exist before the room's first call, and did the room build, adopt or only notice it? Did the deals happen in the thread or elsewhere? Test the onset contrast on block 02's late rooms against early rooms of similar size. The first paired check is when r/denmark and r/sweden are both read, in block 07.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
