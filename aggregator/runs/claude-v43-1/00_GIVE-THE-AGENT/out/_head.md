# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-05, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-05 read blocks 01 (53 rooms), 02 (48), 03 (62), 04 (44) and 05 (34) whole. 241 of 705 rooms have a note in `out/rooms/`. 464 rooms remain, in blocks 06 to 19. The next leg is A1b-06. At this close `mem.py next` names r/wow, the first room of block 06. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count. Block 13 is r/counting alone, at 11.17 MB.

`validate.py A1` at this close: 0 errors, 0 warnings. 241 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh, not yet filed: linked artworks with region placements before hour 0. Six cases: r/FloydVsVoid h-14.47, r/ProfessorLayton h-13.49, r/SwissNeutralityZone h-14.52, r/monalisaclan h-15.23, r/radiohead h-11.54, r/aoe2 h-0.66. None new in block 05. The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it.

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

Earlier blocks are in the diary and earlier heads. Block 05 early rooms, three: r/rit (h1.01, April Fools posts first), r/TheGreatGreenBox (h1.23, a sub made in the first hours whose coordination ended near h15), r/france (h2.32, a flag chosen in the first minutes). Block 05 late rooms, two: r/natsume (h54.1) found Nyanko-sensei already on the canvas and never learned who made it; r/Dorset (h60.1) found its flag under way, with Devon's help, on a Cornish flag. Both late rooms found art, not space. That matches the earlier late rooms: the first coded turn dates the room's talk, not its pixels. No size test yet.

## The three sentences written before reading, against five blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke, and other subs often made it. In block 05, 10 of 34 `made` lines say outright that placements began before the room's first call. r/natsume, r/Dorset and r/FlipnoteStudio3D found or named art placed long before. In r/ducks and r/mariokart the room's writers placed none of the linked artwork. The canvas fields link only a heart for r/colombia and only Kvikk Lunsj and a cheese slicer for r/norway, not the flags they discussed.
2. Coordinating turns end mostly between hours 62 and 73. Block 05: r/osu h72.99, r/france h72.96, r/kcroyals h72.96, r/osugame h72.91, r/samuraijack h72.91, r/greenlattice h72.31. Earlier ends: r/TheGreatGreenBox h25.4, r/mariokart h31.4, r/redpandas h47.1, r/mit h64.0. After the close r/greenlattice, r/nightinthewoods, r/uiuc and r/TheGreatGreenBox moved to clone canvases.
3. Fights are with neighbours, and rivals often turn into partners. Block 05: sport rivals building together (r/utaustin with r/aggies, r/osu with Michigan under a Big Ten truce, r/uiuc with Purdue, r/hawks with the Blues); r/osugame's Tyler1 raid ending in an alliance; r/neopets apologising to the mango makers, who then helped build its Jubjub.
4. Deals are struck in the thread, in Discord, or both. Block 05 shows a sub made for the canvas running a permit office: r/greenlattice's Art Application Form and approved-projects document from h51.4, with diplomacy sent to Discord. r/france agreed a border at row 771 with r/placehearts on Discord. r/osugame met in a "world congress" Discord of representatives. r/masseffect's deal with the taskbar was one member's negotiation.
5. The goal is often set by one member. Block 05: r/mit's member set the corner because nobody replied; r/kcroyals ran on one edited post; r/FlipnoteStudio3D was one call and one confused reply.
6. April Fools makeovers filled more coded turns than the canvas in many rooms: r/paydaytheheist, r/heroesofthestorm, r/hawks (Breadman), r/NieR (swapped with r/nioh), r/samuraijack (the premiere swap), r/indieheads, r/rit.
7. Moderators: r/france's moderators funnelled every canvas post into a megathread; r/bostonceltics' moderators later refused a sticky; r/hawks removed canvas posts at h70; r/greenlattice's moderators were called traitors.
8. The atlas names former works: r/nightinthewoods ("(Former) Night in the Woods Logo"), r/TheGreatGreenBox ("Former location of the Green Corner").

New in block 05, seen in three or more rooms and logged in the diary:
- Sport rivals build together on the canvas.
- A room backs off an attack, apologises, and the target helps it.

Paired lead checks, both sides read: most agree (Temple and osu; darksouls and paydaytheheist; morrowind, truestl and natsume; kamenrider and kcroyals; wildhockey and hawks; loltyler1 and osugame; Clannad and bostonceltics; several rooms and greenlattice). One mismatch: r/ghibli says Virginia Tech took the Totoro spot, and r/virginiatech's record does not name it.

## Contrary rooms

Block 01: morrowind and megaman said they were not organized; heyyea kept art it did not make; egypt's flag was a stranger's gift; duckgame mourned art the atlas lists as surviving; AprilKnights had an order with elections; flashtv's prank ran apart from canvas work; PinkVomitMonster called its lack of coordination its beauty; FloydVsVoid's founder regretted not compromising; anime mostly refused and argued credit; watchmen and TheAdventuresofTintin noticed art they did not visibly build; tagpro aimed at advertising; anime, qotsa, cfb and drugs disagree with the canvas fields. From the screen: UNLincoln, yerbamate, Redox, azores, archlinux.

Block 02: homelab, hentai, kpop and ubc, norge, cirkeltrek, loltyler1, bobross and nonbinary, zelda.

Block 03: ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft and GuildWars2, bardmains, placeDE.

Block 04: theitalyplace and spacexmasterrace (canvas fields link a neighbour's work or a YES); tampabaylightning (a neighbour erased its own art); aoe2 (an ally repaired the helmet more than the room); 4chan (raid calls refused); ice_poseidon; korea; drawhelix.

Block 05:
- greenlattice: a sub made for the canvas that governed other rooms' art through forms and an approved list.
- norway: the English-language sub forwarded canvas requests to r/Norge, where the action was.
- utaustin: won its spot with a disguised script that turned GiantBomb's defence against itself.
- france: an outside forum, the 18-25 of jeuxvideo.com, arrived late and was blamed for purifying the flag.
- masseffect: moved three times and accepted its attacker's help to rebuild.
- ducks and mariokart: the linked artwork has no placements by the room's writers.
- natsume: found its work, never learned who made it.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 06:
- joining or finding work begun elsewhere, against starting it;
- organizing in the thread, against organizing in Discord and reporting back;
- deals that bind a room, against deals made by a few that others reject;
- a deal turned into a room rule, against a deal held only by the organiser;
- a sub made for the canvas that governs others (greenlattice), against one that only builds;
- one organiser with alts or friends, against a room-wide effort;
- attacking first and building later, against building first and defending;
- rivals who stay rivals, against rivals who build together;
- the room's April Fools practice, against its canvas practice;
- the moderator as organiser, as obstacle, and as attacker;
- the canvas fields linking the room's work, against linking a neighbour's or nothing it describes.

## The last rooms read

Block 05, in reading order: osu, samuraijack, Dorset, virginiatech, nightinthewoods, norway, chicago, ss13, greenlattice, paydaytheheist, uiuc, NieR, masseffect, ducks, colombia, albania, rit, mit, truestl, bostonceltics, roosterteeth, france, utaustin, mariokart, kcroyals, redpandas, natsume, osugame, hawks, TheGreatGreenBox, FlipnoteStudio3D, heroesofthestorm, indieheads, neopets.

## Ledgers at this close

- `lexicon-A1.md`: 542 lines. `running-A1.md`: 226 lines. `leads-A1.jsonl`: 774 lines; every `other` is in `order-A1.txt`, checked by a one-line python check over the whole file at this close.
- In this leg two lead lines named rooms outside the frame (roosterteeth to evangelion, kcroyals to mariners). Validate caught them; they were removed and their content kept in the diary. Two lead lines had wrong item ids (rit to COSI, and rickandmorty to AcePlace in the last leg); corrected lines were appended. Rule: check the frame with grep or the python check, and the id with `cite.py`, before appending.
- r/FlipnoteStudio3D has two concepts; its carrying line repeats c0001 because the form requires three ids. The diary records why.
- The hook rejects notes of 350 words or more. First drafts still run 360 to 410; aim for 300.
- Diary third-time notes so far: art placed before the room's call; organizing after h73 on successor canvases; treaties reported back from Discord; moderators herding canvas talk; April Fools outweighing canvas talk; the atlas naming a different work; rooms joining upkeep of art already there; rooms helping a displaced neighbour rebuild; canvas work coordinated in another sub; a room asking at the close why it is not on the canvas; a room learning another sub or Discord built its art; raids refused in the thread; rooms giving up expansion when asked; members asking where their own work is; sport rivals building together; a room backing off and its target helping.

## The next comparison

In block 06, for every room: did the artwork exist before the room's first call, and who built it? Do the canvas fields link the work the room describes? Was the deal struck in the thread or in Discord, and did members accept that it bound them? Which side of the onset contrast is the room on, and is it a sub made for the canvas? Block 06 holds r/thebluecorner, named in the leads by 17 earlier rooms (osu, osugame, ice_poseidon, rush, masseffect, 4chan and others); only r/greenlattice and r/ainbowroad are named by more, 22 each. Read it against every lead that names it, as r/greenlattice was read in block 05. r/ainbowroad comes in block 19. Block 06 also holds r/wow, r/placesnek, r/germany, r/gorillaz, r/habs and r/bih. The first paired check of a national pact is r/denmark and r/sweden in block 07, with r/placehearts and r/japan.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
