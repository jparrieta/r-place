# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1a, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive? I have not changed it.

## Where the run stands

Stage A1, the reading. Leg A1a is done: the checks, the screen and what is written before reading. No room has been read whole yet and no room note exists. The next leg is A1b-01, block 01 of 19. The next room is the one `mem.py next` names: r/anarchism, the first of block 01. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) of all 705 rooms cut into blocks of about 3 MB by `mem.py`'s byte count. The blocks with their rooms and bytes are listed in `notes-A1.md`. Block 13 is r/counting alone, at 11.17 MB. One leg may not finish it, and its note waits for the room's end.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: the 46 rooms with one coded thread all wrote about the canvas while it was open. None has zero threads and none starts after hour 73. Dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed at B3. 29 rooms carry one or two second-order themes.

## What the checks found

Six defects are in `defects.jsonl`, and none blocks the reading:

1. r/tenma has no canvas line: area 0, no artwork, no pixels row.
2. r/archlinux has a coded turn at hour 100.9, past the window.
3. `n_codes_coder` excludes retractions in 32 rooms and includes them elsewhere.
4. `items.jsonl` has an undocumented state, `collapsed` (21,011 items). The forests count 531,851 items against the store's 158,227.
5. The concept reach share is 1.0 in every room, so the stage file's measure cannot yield a threshold.
6. r/yogscast's first coded turn (h -18.58) is not about the canvas.

The tools all work, and `validate.py --self-test` passes 137 of 137.

Two departures are in `departures.jsonl`. Both are saved scripts in `out/_analysis/` that read the store directly: one for the section 1 checks the verbs do not serve, one for the reading order.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231. Themes on concepts: 0.429. The second-order tier is close to fixed width, so large rooms are compressed most.
- **concept_reach_threshold: 0 items.** Every room is read at concept level from stage C2 until the return is adjudicated. This rests on QA1-001, asked of the principal investigator: did the stage file mean another measure? Read `mem.py asks QA1-001` at the next leg's start.
- `n_off_platform`: median 4, q3 10, max 88 (dankmemes). 66 rooms have none.
- `px_window_share` (the share of a room's own artwork placed by its writers): median 0.111, max 0.547. It is null for tenma.
- Concentration is null in 3 rooms (nonbinary, oltp, wario), so its denominator is 702.
- 79 rooms have their last coded turn before hour 73.

## The onset contrast

`out/contrast.md`. Early: first coded turn after hour 0 and before hour 3, 131 rooms. Late: first coded turn after hour 48, 61 rooms. r/italy and r/yogscast stand on neither side. The confound is written first: room size differs a hundredfold (median items 5067 against 33). A held-size comparison on rooms with 156 to 2770 items, 41 against 12, travels with the contrast. My expectation: late rooms organize around finding space on a full canvas, early rooms around claiming and holding it. If the held-size comparison erases the space-finding difference, onset on this clock measures size and nothing else. Stage C2 tests it against the model's arrows.

## What I expect, before reading

Most rooms will show one burst of calls, coordinates and reports in the first day or two, then defence and looking back, with coordinating turns ending near hour 73. The fights will be with canvas neighbours, and the deals about borders and space, struck in the thread or sent to Discord. The goal will be set in the first hours by one person's call and changed only under a neighbour's pressure or a loss of ground. The room notes test these sentences. Each later leg says what the notes showed that these did not predict.

## Contrary rooms already seen

- r/UNLincoln's one thread defends a logo that a reply says is Northeastern's, not theirs.
- r/watchmen and r/yerbamate only noticed their art on the canvas. These may be rooms that did not organize.
- r/Redox and r/azores report work done in another room (r/rust) or on a Discord. The organizing crossed the room's boundary.
- r/archlinux: a member says the organizing was "almost completely on Discord". The public record may be the smaller part of the work.

## Open distinctions

None is filed in `_questions/` yet. One question is pending with the principal investigator: QA1-001, the concept reach measure.

## The last rooms opened

At the screen, through their forests: r/signal, r/vermont, r/watchmen, r/wsu, r/yerbamate. Then r/yogscast (codes), r/archlinux (codes) and r/UNLincoln (canvas). These were screen reads, not readings for a note.

## The next comparison

The first block's rooms against the three sentences above. In particular: does organizing end near hour 73, or does it go on into the aftermath? Do the fights run with canvas neighbours or with rivals named from elsewhere? The first contrast check is when r/denmark and r/sweden are both read, in block 07.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
