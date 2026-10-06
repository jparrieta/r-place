# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-03, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01, A1b-02 and A1b-03 read blocks 01 (53 rooms), 02 (48 rooms) and 03 (62 rooms) whole. 163 of 705 rooms have a note in `out/rooms/`. 542 rooms remain, in blocks 04 to 19. The next leg is A1b-04. At this close `mem.py next` names r/anime_irl, the first room of block 04. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count. Block 13 is r/counting alone, at 11.17 MB.

`validate.py A1` at this close: 0 errors, 0 warnings. 163 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh, not yet filed: some linked artworks show region placements before hour 0. r/FloydVsVoid's prism from h-14.47, r/ProfessorLayton's from h-13.49, and in block 03 r/SwissNeutralityZone's Void Prism and Swiss Cheese and Mountains from h-14.52. The canvas window runs from -16, so this may be by design. Check `package/DATA-manifest-canvas.md` through the verbs before filing it.

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

Block 03 was checked room by room from each room's first coded hour. Two early rooms: r/twitchplayspokemon (h0.6) held Helix through alliances and told land claims as lore; r/evex (h2.8) claimed a compact spot with r/ainbowroad's permission and later moved four pixels for r/eve. Four late rooms: r/aeon (h71) took a script from r/monero two hours before the close; r/mcgillrobotics (h54.9) placed beside the Canadian flag in one post; r/quq (h57.9) only announced and later located its mark; r/ukplace (h53.4) did not look for space but expanded by script over others. r/ukplace is a sub made for the canvas, with pre-event members at 0, so its late first coded turn may date the sub, not the effort. No size test yet.

## The three sentences written before reading, against three blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke, and other subs often made it. Block 02 examples are in the diary. In block 03: r/Homura's members asked who built their work and were told the r/MadokaMagica Discord did; r/lovelive's Honoka came from a user on the SIF subreddit; r/sakuragakuin's banner was done before its first coded turn, beside r/babymetal's mural; r/spelunky, r/Madeon, r/yerbamate, r/Lugarix and r/quq only found or announced their art; r/glasgow pointed to r/scotland's work; r/aeon's plan came from r/monero. The canvas fields do not say who placed the early pixels.
2. Coordinating turns end mostly between hours 62 and 73. Block 03 examples: r/texastech h73.21, r/frc h72.88, r/maryland h72.89, r/placeDE h72.98, r/xcom h72.78, r/survivor h72.32. Several rooms moved to pxls.space or another canvas after the close (r/frc, r/futurama, r/placeportalpattern, r/bardmains).
3. Fights are with canvas neighbours. Block 03 adds fights inside rooms: r/AyyMD fought over red or green among its own members; r/frc's members blamed their own team 4611 for invading Poland first; r/futurama changed Bender's colour and material several times.
4. Deals are struck in Discord more often than in threads, and their reach is disputed. In block 03 members asked who speaks for a group when a deal is cited: r/harrypotter and r/buffalobills, r/polska and AMD ("I can't speak for every member"), r/dallasstars and Green Lattice, r/survivor and Denmark. Rooms reported rogue members breaking deals their Discord had made (r/costa_rica and Green Lattice, r/sixers and r/Kanye, r/columbia and the blue corner). r/darksouls' members learned of a Discord decision after it was made and asked who decided.
5. The goal is often set by one member, often late, and changed by neighbours. Block 03 has many rooms whose one organiser did most of the work with alts or friends (r/nyu, r/oman, r/sixers, r/freedomplanet, r/ravens), and rooms that moved again and again with apologies (r/dallasstars at least four times, r/lsu at least five, r/ftlgame, r/xcom).
6. The room's own April Fools makeover filled more coded turns than the canvas in many rooms. Block 03: r/battlecats (joke flairs, about five to one), r/kerbalspaceprogram (meme day), r/survivor (Facebook parody), r/GuildWars2, r/zelda earlier, r/twitchplayspokemon (an election), r/sixers, r/glasgow.
7. Moderators were organisers, obstacles or attackers. Block 03: r/linux's moderator removed script posts as off-topic; r/darksouls' and r/bardmains' moderators gathered posts into one megathread and removed others; r/kerbalspaceprogram's moderator removed a call for help as low effort.
8. The atlas sometimes names a different, covered or destroyed work: r/survivor (covered), r/battlecats (used to be here), r/quq (destroyed), r/frc's logo the room mourned as broken, r/GuardiansOfDatBoi linked to the beam and not to Dat Boi.

## Contrary rooms

Block 01: morrowind and megaman said they were not organized; heyyea kept art it did not make; egypt's flag was a stranger's gift; duckgame mourned art the atlas lists as surviving; AprilKnights had an order with elections; flashtv's prank ran apart from canvas work; PinkVomitMonster called its lack of coordination its beauty; FloydVsVoid's founder regretted not compromising; anime mostly refused and argued credit; watchmen and TheAdventuresofTintin noticed art they did not visibly build; tagpro aimed at advertising; anime, qotsa, cfb and drugs disagree with the canvas fields. From the screen: UNLincoln, yerbamate, Redox, azores, archlinux.

Block 02: homelab, a moderator-led takeover; hentai, a moderator retaliating; kpop and ubc, members refusing an attack; norge, expansion argued as destroying others; cirkeltrek; loltyler1, attack first and then build; bobross and nonbinary, one post speaking for unseen work; zelda, a large room whose canvas work ran elsewhere.

Block 03:
- ukplace: a late-onset sub that expanded by script over others and defended it as fair use of Reddit's API.
- SwissNeutralityZone: a room named for neutrality that attacked a Savoyard flag and argued whether helping America was neutral.
- GuardiansOfDatBoi: a sub whose founder negotiated peace while its members kept bending a beam at OSU.
- minecraft and GuildWars2: large rooms whose members asked at the close why their room was not on the canvas.
- bardmains: offered a neighbour's laser a hole through its own mask.
- placeDE: a sub that ran on an official Discord while members said Discord had nothing to decide, and argued against both expansion and nationalist symbols.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 04:
- joining or finding work begun elsewhere, against starting it;
- organizing in the thread, against organizing in Discord and reporting back;
- deals that bind a room, against deals made by a few that others reject;
- a sub made for the canvas, against an existing community turning to it;
- one organiser with alts or friends, against a room-wide effort;
- attacking first and building later, against building first and defending;
- the room's April Fools practice, against its canvas practice;
- the moderator as organiser, as obstacle, and as attacker.

## The last rooms read

Block 03, in reading order: texastech, frc, spelunky, ghibli, pepe, polska, linux, yerbamate, skyrim, dallasstars, ravens, iceland, GuardiansOfDatBoi, CryptoFR, GuildWars2, oman, columbia, ftlgame, twitchplayspokemon, Bravenewbies, ohio, darksouls, lovelive, Madeon, minecraft, battlecats, freedomplanet, Honduras, xcom, harrypotter, glasgow, uruguay, survivor, ukplace, sixers, Lugarix, aceattorney, hongkong, costa_rica, SwissNeutralityZone, maryland, aeon, sakuragakuin, mcgillrobotics, futurama, england, nyu, kerbalspaceprogram, evex, n64, latvia, placeportalpattern, MonkeyIsland, Homura, quq, toolband, peterdraws, placeDE, bardmains, lsu, AyyMD, malta.

## Ledgers at this close

- `lexicon-A1.md`: 370 lines. `running-A1.md`: 185 lines. `leads-A1.jsonl`: 419 lines; every `other` checked against `order-A1.txt`.
- In this leg, item ids written before checking were found and corrected (polska, linux, skyrim, ftlgame, frc, peterdraws). The rule from here: run `lex.py` or `cite.py` first, append second. The diary records it.
- Diary third-time notes logged so far: art placed before the room's call; organizing after h73 on successor canvases; treaties reported back from Discord; moderators herding canvas talk; April Fools outweighing canvas talk; the atlas naming a different work; rooms joining upkeep of art already there; rooms helping a displaced neighbour rebuild; canvas work coordinated in another sub; a room asking at the close why it is not on the canvas; a room learning another sub or Discord built its art.

## The next comparison

In block 04, for every room: did the artwork exist before the room's first call, and who built it? Was the deal struck in the thread or in Discord, and did members accept that it bound them? Which side of the onset contrast is the room on, and is it a sub made for the canvas? Many leads point into block 04 (r/anime_irl, r/osugame later in 05) and many earlier rooms named r/greenlattice and r/thebluecorner (blocks 05 and 06). The first paired check is when r/denmark and r/sweden are both read, in block 07; block 03 adds r/maryland and r/survivor as rooms that dealt with them.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
