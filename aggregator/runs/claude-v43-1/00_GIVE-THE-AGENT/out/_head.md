# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-04, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-04 read blocks 01 (53 rooms), 02 (48), 03 (62) and 04 (44) whole. 207 of 705 rooms have a note in `out/rooms/`. 498 rooms remain, in blocks 05 to 19. The next leg is A1b-05. At this close `mem.py next` names r/osu, the first room of block 05. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count. Block 13 is r/counting alone, at 11.17 MB.

`validate.py A1` at this close: 0 errors, 0 warnings. 207 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh, not yet filed: linked artworks with region placements before hour 0. Cases so far: r/FloydVsVoid h-14.47, r/ProfessorLayton h-13.49, r/SwissNeutralityZone h-14.52, and in block 04 r/monalisaclan h-15.23, r/radiohead h-11.54, r/aoe2 h-0.66. The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it. The diary records each case.

## The principal investigator's answer QA1-001

The concept-reach threshold stays at 0 items. No substitute measure is to be invented. Every room is read at concept level in the later model-building stages, and unplaced concepts are read at the end too. `notes-A1.md` says that the measure gives no cut in this store.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- concept_reach_threshold: 0 items, kept by QA1-001.
- `n_off_platform`: median 4, max 88 (dankmemes).
- `px_window_share`: median 0.111, max 0.547; null for tenma.
- Concentration is null in 3 rooms (nonbinary, oltp, wario).
- 79 rooms have their last coded turn before hour 73.

## The onset contrast

`out/contrast.md`. Early: first coded turn before hour 3, 131 rooms. Late: first coded turn after hour 48, 61 rooms. The confound is size (median items 5067 against 33). A held-size comparison (items 156 to 2770, 41 against 12) travels with it. Expectation: late rooms organize around finding space on a full canvas; early rooms around claiming and holding it.

Block 03 checks are in the diary and the last head. Block 04 early rooms, ten: r/smite (h0.05), r/hearthstone (h0.17), r/spacexmasterrace (h0.55), r/ice_poseidon (h1.13), r/giivasunner (h1.16), r/frankocean (h1.63), r/catholicism (h1.78), r/radiohead (h1.92), r/haskell (h2.09), r/rickandmorty (h2.64). In the seven I read after the mid-leg compaction, the first coded turn is April Fools talk or a call to build. Most then claimed a spot and moved at least once (smite, hearthstone, giivasunner, ice_poseidon's second TriHard). Block 04 late rooms, four: r/vermont (h49.05), r/bees (h55.3), r/Clannad (h58.3), r/ElSalvador (h60.24). r/vermont asked where to fit without interfering; r/bees took over another sub's text in its first turn; r/Clannad opened by announcing its work finished. r/bees and r/Clannad found their art already placed (from h2.57 and h1.43). The late side keeps showing first coded turns that date the room's talk, not its pixels. No size test yet.

## The three sentences written before reading, against four blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke, and other subs often made it. Block 04 adds many more. In 16 of 44 notes the `made` line says outright that placements began before the room's first coded turn. Most other block-04 artworks were also placed from h1 to h3, and only ten block-04 rooms spoke before h3. r/drawhelix kept and redrew Helix, which others had placed; r/Clannad, r/genderfluid and r/bees opened by announcing finished work; r/chess's knight was built by Norway; r/theitalyplace organised the Italian flag but the canvas fields link it only to Malta's flag; r/spacexmasterrace built a SpaceX logo and rockets but the fields link it only to a YES. The canvas fields do not say who placed the early pixels.
2. Coordinating turns end mostly between hours 62 and 73. Block 04: r/hearthstone h72.90, r/radiohead h72.96, r/mexico h72.96, r/4chan h72.81, r/physical_removal h72.81, r/spacexmasterrace h72.76, r/aoe2 h72.62. Earlier ends: r/drawhelix h66.26, r/compsoc h66.81, r/thepointing h58.14, r/bees h63.29. After the close r/giivasunner and r/spacexmasterrace moved to replacement canvases.
3. Fights are with canvas neighbours, and inside rooms. Block 04: r/smite's members accused each other and their own sub of damaging the logo; r/utahjazz turned CUBERS into GOBERT and the cubers said they were there first; r/ice_poseidon lost its top-left TriHard and blamed the Void, then r/2007scape.
4. Deals are struck in the thread, in Discord, or both, and their reach is disputed. Block 04: r/giivasunner made its deal with r/mexico into a room rule against attacking without consultation; r/aoe2's Good Sunday Agreement with Ireland was tested when Ireland threatened to withdraw support over the American wall, and the organiser refused to choose; r/radiohead held its TagPro agreement against a nicer line; r/tampabaylightning's neighbour r/cavestory erased part of its own art so the logo was not covered; r/thepointing's member approached PlaceStart while disclaiming authority to speak for the room.
5. The goal is often set by one member and changed by neighbours. Block 04: r/vermont's one edited post carried the room; r/bees was one member; r/rush scaled the Starman down to 2112 and the Canadian team took it into their flag; r/ssbpm cut its plan to just the M.
6. The room's own April Fools makeover filled more coded turns than the canvas in many rooms. Block 04: r/smite (all-Loki flairs), r/hearthstone (PirateStone), r/ssbpm (Project Melee), r/rickandmorty (the surprise premiere), r/rush (the Purge), r/catholicism, r/ethereum, r/factorio, r/thesimpsons, r/kamenrider.
7. Moderators were organisers, obstacles or attackers. Block 04: r/4chan's moderator sent members to the canvas and later posted a script tutorial; r/rickandmorty's moderator stickied coordinates once; r/rush's moderator ran the Purge and let it play out; r/smite's megathread was refused and then granted.
8. The atlas sometimes names a different, covered or former work: r/compsoc (CompSoc covered), r/giivasunner (Former place of Fred Flinstone). r/mexico and r/ice_poseidon mourned work the canvas still keeps under that name.

New in block 04, seen in three or more rooms and logged in the diary:
- Raids proposed again and again and refused in the thread: r/mexico on Italy, r/4chan ("not your personal army", Rule 8), r/korea on Japan, r/Temple on Ohio State.
- A room gives up expansion or moves when a neighbour asks: r/haskell, r/vermont, r/iastate, r/thepointing, r/rush.
- Members ask where their own work is: r/hearthstone, r/borderlands, r/rickandmorty.

## Contrary rooms

Block 01: morrowind and megaman said they were not organized; heyyea kept art it did not make; egypt's flag was a stranger's gift; duckgame mourned art the atlas lists as surviving; AprilKnights had an order with elections; flashtv's prank ran apart from canvas work; PinkVomitMonster called its lack of coordination its beauty; FloydVsVoid's founder regretted not compromising; anime mostly refused and argued credit; watchmen and TheAdventuresofTintin noticed art they did not visibly build; tagpro aimed at advertising; anime, qotsa, cfb and drugs disagree with the canvas fields. From the screen: UNLincoln, yerbamate, Redox, azores, archlinux.

Block 02: homelab, a moderator-led takeover; hentai, a moderator retaliating; kpop and ubc, members refusing an attack; norge, expansion argued as destroying others; cirkeltrek; loltyler1, attack first and then build; bobross and nonbinary, one post speaking for unseen work; zelda, a large room whose canvas work ran elsewhere.

Block 03: ukplace (late onset, expansion by script); SwissNeutralityZone (named for neutrality, attacked a Savoyard flag); GuardiansOfDatBoi (founder made peace while members bent a beam); minecraft and GuildWars2 (asked at the close why they were not on the canvas); bardmains (offered a neighbour's laser a hole); placeDE (official Discord, members saying Discord had nothing to decide).

Block 04:
- theitalyplace: organised the Italian flag; the canvas fields link it only to Malta's flag. A pact with TheFarLeftSide was said to be broken and then said never to have existed.
- spacexmasterrace: built a SpaceX logo, rockets and a barge; the canvas fields link only a YES.
- tampabaylightning: won space because a neighbour, r/cavestory, chose to erase part of its own art.
- aoe2: an ally, Ireland, repaired the helmet more than the room did; the organiser refused to choose between Ireland and America.
- 4chan: a room named for raiding whose members refused many raid calls in the thread.
- ice_poseidon: answered a streamer's call to black out osu; members asked what osu had done.
- korea: k-pop fan subs added to the national flag, and members argued who may label it and who counts as Korean.
- drawhelix: kept and redrew a work others placed.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 05:
- joining or finding work begun elsewhere, against starting it;
- organizing in the thread, against organizing in Discord and reporting back;
- deals that bind a room, against deals made by a few that others reject;
- a deal turned into a room rule (giivasunner), against a deal held only by the organiser (aoe2);
- a sub made for the canvas, against an existing community turning to it;
- one organiser with alts or friends, against a room-wide effort;
- attacking first and building later, against building first and defending;
- the room's April Fools practice, against its canvas practice;
- the moderator as organiser, as obstacle, and as attacker;
- the canvas fields linking the room's work, against linking a neighbour's or nothing it describes.

## The last rooms read

Block 04, in reading order: anime_irl, iastate, chess, day9, wildhockey, monalisaclan, ElSalvador, partyparrot, catholicism, thesimpsons, SydneyFC, kamenrider, diablo, haskell, frankocean, ethereum, vermont, theitalyplace, factorio, placetardis, rush, rickandmorty, smite, hearthstone, drawhelix, ice_poseidon, compsoc, mexico, giivasunner, thepointing, 4chan, genderfluid, utahjazz, ssbpm, borderlands, physical_removal, Temple, radiohead, korea, tampabaylightning, spacexmasterrace, Clannad, aoe2, bees.

## Ledgers at this close

- `lexicon-A1.md`: 455 lines. `running-A1.md`: 209 lines. `leads-A1.jsonl`: 614 lines; every `other` checked against `order-A1.txt` before appending.
- In this leg one lead line was written with a wrong item id (rickandmorty to AcePlace, dfr3tho). A corrected line with dfs2915 was appended and the diary records it. The rule stands: run `lex.py` or `cite.py` first, append second.
- The hook rejects notes of 350 words or more. First drafts in this leg often ran 370 to 410 words; aim for 300 in the first draft.
- Diary third-time notes logged so far: art placed before the room's call; organizing after h73 on successor canvases; treaties reported back from Discord; moderators herding canvas talk; April Fools outweighing canvas talk; the atlas naming a different work; rooms joining upkeep of art already there; rooms helping a displaced neighbour rebuild; canvas work coordinated in another sub; a room asking at the close why it is not on the canvas; a room learning another sub or Discord built its art; raids refused in the thread; rooms giving up expansion when asked; members asking where their own work is.

## The next comparison

In block 05, for every room: did the artwork exist before the room's first call, and who built it? Do the canvas fields link the work the room describes? Was the deal struck in the thread or in Discord, and did members accept that it bound them? Which side of the onset contrast is the room on, and is it a sub made for the canvas? Block 05 holds many rooms that earlier rooms named: r/osu and r/osugame (ice_poseidon, loltyler1), r/greenlattice (spacexmasterrace, giivasunner, ssbpm, hearthstone), r/bostonceltics (Clannad), r/france (mexico), r/uiuc (Temple), r/indieheads (aoe2, radiohead), r/heroesofthestorm. Read each against the leads that name it. r/thebluecorner follows in block 06. The first paired check of a deal from both sides is r/denmark and r/sweden in block 07; r/maryland, r/survivor and r/tampabaylightning named that pact.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
