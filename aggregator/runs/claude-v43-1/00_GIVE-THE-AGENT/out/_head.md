# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-02, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Leg A1b-01 read block 01 whole (53 rooms). Leg A1b-02 read block 02 whole (48 rooms). 101 of 705 rooms have a note in `out/rooms/`. 604 rooms remain, in blocks 03 to 19. The next leg is A1b-03. At this close `mem.py next` names r/texastech, the first room of block 03. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count. Block 13 is r/counting alone, at 11.17 MB.

`validate.py A1` at this close: 0 errors, 0 warnings. 101 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh, not yet filed: two rooms' linked artworks show region placements before hour 0 (r/FloydVsVoid from h-14.47, r/ProfessorLayton from h-13.49, with a burst there). The canvas window runs from -16, so this may be by design. Check `package/DATA-manifest-canvas.md` through the verbs before filing it.

## The principal investigator's answer QA1-001

The concept-reach threshold stays at 0 items. No substitute measure is to be invented. Every room is read at concept level in the later model-building stages, and unplaced concepts are read at the end too. `notes-A1.md` says that the measure gives no cut in this store. Nothing else in the reading rested on the assumption.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- concept_reach_threshold: 0 items, kept by QA1-001.
- `n_off_platform`: median 4, max 88 (dankmemes).
- `px_window_share`: median 0.111, max 0.547; null for tenma.
- Concentration is null in 3 rooms (nonbinary, oltp, wario).
- 79 rooms have their last coded turn before hour 73.

## The onset contrast

`out/contrast.md`. Early: first coded turn before hour 3, 131 rooms. Late: first coded turn after hour 48, 61 rooms. The confound is size (median items 5067 against 33). A held-size comparison (items 156 to 2770, 41 against 12) travels with it. Expectation: late rooms organize around finding space on a full canvas; early rooms around claiming and holding it.

Block 01 fitted the expectation without a size test. Block 02 was not checked against the contrast lists room by room. Block 03 should do it: for each room, look up its side in `contrast.md` before writing the note.

## The three sentences written before reading, against two blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke. In both blocks the linked artwork usually shows placements from hour 1 or 2, while the room's first canvas talk comes hours or days later. In block 02 the rooms adopted work begun elsewhere: r/konosuba took art planned by r/Megumin; r/shield had a HYDRA logo from the MCU Discord; r/stlouis kept the Blues note; r/DatBoi was run by GuardiansOfDatBoi; r/Redox and r/signal only reported work; r/batman and r/earthbound found their logos and repaired them; r/alberta worked through r/placecanada; r/zelda's Link builders coordinated in r/PlaceLink; r/bobross had one post speaking as "we" for a finished chibi. The canvas fields do not say who placed the early pixels.
2. Coordinating turns end mostly between hours 62 and 73. Block 02 examples: r/loltyler1 h72.67, r/seahawks h72.91, r/phish h72.50, r/ubc h72.75, r/norge h72.79, r/zelda h66.98, r/homelab h69.30. Several rooms tried again on successor canvases after 73 (r/phish on PlaceTwo; r/loltyler1 called the room onto another canvas).
3. Fights are with canvas neighbours, and some rooms brought outside rivals in. r/loltyler1 griefed the OSU logo for two days, then built #FreeTyler1 and offered r/osugame an alliance. r/seahawks fought r/49ers fans over a border and made a one-pixel truce.
4. Deals were struck in two places. In block 01 most were struck in Discord and reported back. In block 02 several were struck in the thread itself: r/seahawks with a 49ers fan, r/phish with a Brazil member who moved Fluffhead for them, r/carletonu offering a newcomer a spot beside its work. The r/phish deal broke a day later, by the room's account. Small rooms joined the placestart taskbar to survive (r/vocaloid, r/monsterhunter, r/earthbound).
5. The goal is often set by one member, often late, and changed by neighbours. r/seahawks chose a little 12 because a small area is easier to defend, then told defenders to let it decay so it could move. r/phish moved from letters to a logo to the word Fluffhead, and moved once more at Brazil's request.
6. The room's own April Fools makeover filled more coded turns than the canvas in many rooms: r/teslamotors, r/mechanicalkeyboards, r/giantbomb, r/seahawks (everyone a moderator), r/zelda (the swap with r/horizon and posts removed under a Horizon-only rule), r/loltyler1 (the unban joke). This adds to block 01's list. A later stage must decide how this bears on organizing.
7. Moderators were organisers, obstacles or attackers. r/homelab's moderator led a takeover. r/hentai's moderator retaliated against members who objected. r/zelda's moderators removed posts all day for the joke. r/seahawks' moderator opened one thread to gather the place talk at h70.
8. The atlas sometimes names a different or minor work than the threads describe: r/completeanarchy (Bread), r/vocaloid (Vocaloid Soft), r/australia (a small flag), r/giantbomb (the room mourned the bomb; the atlas keeps it).

## Contrary rooms

Block 01:
- morrowind and megaman: members said they were not organized.
- heyyea: a late keeper of art it did not make.
- egypt: the surviving flag was a stranger's gift.
- duckgame: mourned art that the atlas lists as surviving.
- AprilKnights: an existing order with elections.
- flashtv: the moderators' prank ran apart from the canvas work.
- PinkVomitMonster: a sub made for a figure already on the canvas; members called its lack of coordination its beauty.
- FloydVsVoid: the founder said he was wrong not to compromise with the Void; the prism survived through deals.
- anime: a huge room that mostly refused, routed or argued credit.
- watchmen and TheAdventuresofTintin: rooms that noticed art they did not visibly build.
- tagpro: the stated aim from the first hour was advertising.
- the canvas fields and the room disagree: anime, qotsa, cfb, drugs.
- Earlier, from the screen: UNLincoln, yerbamate, Redox, azores, archlinux.

Block 02:
- homelab: a moderator-led takeover of other work.
- hentai: the moderator retaliated against members' objections.
- kpop and ubc: members refused an attack or refused to deface.
- norge: members argued that expansion meant destroying others.
- cirkeltrek: a neighbour said of another group that it had no control over its people.
- loltyler1: a room that attacked first and then built, with a streamer's relayed wish turning it toward building.
- bobross and nonbinary: one post each, speaking for work no thread shows being built.
- zelda: a very large room whose canvas work ran in other subs; the room praised and credited.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 03:
- joining work begun elsewhere, against starting it;
- organizing in the thread, against organizing elsewhere and reporting back;
- deals struck in the thread, against deals struck in Discord;
- a room's own rivals, against canvas neighbours;
- attacking first and building later, against building first and defending;
- the room's April Fools practice, against its canvas practice;
- the moderator as organiser, as obstacle, and as attacker.

## The last rooms read

Block 02, in reading order: placecanada, konosuba, shield, minnesotavikings, completeanarchy, hellointernet, cloud9, Rainbow6, cirkeltrek, faeria, alberta, monsterhunter, DatBoi, stlouis, uwaterloo, OKState, homelab, monero, Redox, vocaloid, australia, hentai, DCFU, dwarffortress, signal, nuclearthrone, luciomains, czech, WPI, colorado, ubc, giantbomb, serbia, kpop, norge, ScottPilgrim, teslamotors, carletonu, earthbound, batman, kindafunny, nonbinary, mechanicalkeyboards, loltyler1, seahawks, zelda, bobross, phish.

## Ledgers at this close

- `lexicon-A1.md`: 277 lines. `running-A1.md`: 145 lines. `leads-A1.jsonl`: 170 lines; every `other` checked against `order-A1.txt`.
- Diary third-time notes logged so far: art placed before the room's call; organizing after h73 on successor canvases; treaties reported back from Discord; moderators herding canvas talk; April Fools outweighing canvas talk; the atlas naming a different work; rooms first speaking of art already on the canvas and joining its upkeep; rooms helping a displaced neighbour rebuild; canvas work coordinated in another sub made for it.

## The next comparison

In block 03, for every room: did the artwork exist before the room's first call, and did the room build, adopt or only notice it? Were the deals struck in the thread or elsewhere? Which side of the onset contrast is the room on, and does its talk fit the expectation once size is held? The first paired check is when r/denmark and r/sweden are both read, in block 07. The leads to r/osugame and r/greenlattice fall in block 05; r/thebluecorner is in block 06.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
