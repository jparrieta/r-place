# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-06, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-06 read blocks 01 (53 rooms), 02 (48), 03 (62), 04 (44), 05 (34) and 06 (37) whole. 278 of 705 rooms have a note in `out/rooms/`. 427 rooms remain, in blocks 07 to 19. The next leg is A1b-07. At this close `mem.py next` names r/porterrobinson, the first room of block 07. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count. Block 13 is r/counting alone, at 11.17 MB.

`validate.py A1` at this close: 0 errors, 0 warnings. 278 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh defect, not yet filed: linked artworks with region placements before hour 0. Nine cases now. Earlier blocks: r/FloydVsVoid h-14.47, r/ProfessorLayton h-13.49, r/SwissNeutralityZone h-14.52, r/monalisaclan h-15.23, r/radiohead h-11.54, r/aoe2 h-0.66. Block 06: r/thebluecorner h-12.34, r/globaloffensive h-13.62, r/GrowTheTree h-0.24. The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it.

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

`out/contrast.md`. Early: first coded turn after hour 0 and before hour 3, 131 rooms. Late: first coded turn after hour 48, 61 rooms. The confound is size (median items 5067 against 33). A held-size comparison (items 156 to 2770, 41 against 12) travels with it. Expectation: late rooms organize around finding space on a full canvas; early rooms around claiming and holding it.

Block 06 early rooms, five: r/wow, r/globaloffensive (h0.20, April Fools first, a 1G found already on the canvas), r/pokemon (h0.34, Team Skull first, then many single-sprite calls), r/asktransgender (h1.46, a trans flag on the Day of Visibility, routed under neighbours' art), r/chicubs (h2.68, a call with no spot for a day). Block 06 late rooms, three: r/azores and r/k_on, and r/DiamondClub (h55.5, one member placed a <> beside He-Man; the linked artwork has placements from h1.24). The late rooms again found art or placed small marks in gaps. Each late room's first coded turn comes long after its region's first placements. No size test yet.

## The three sentences written before reading, against six blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke, and other subs often made it. In block 06 nearly every `made` line has placements hours or days before the room's first call. r/vim credits its logo to r/ArchLinux. r/furry_irl adopted a sign another person made. r/gravityfalls and r/globaloffensive found their art under way. In eight block 06 rooms the room's writers placed under 0.03 of the linked artwork: Pigifs, evedreddit, bih, spongebob, pokemon, vim, germany, placehfarts.
2. Coordinating turns end mostly between hours 62 and 73. Block 06: r/naruto h72.70, r/thebluecorner h72.75, r/gorillaz h72.86, r/chicubs h72.80, r/miamidolphins h72.03. Earlier ends: r/soylent h59.67, r/TreePlace h55.12, r/evedreddit h53.46, r/Pigifs h52.57. After the close r/naruto, r/gravityfalls, r/gorillaz, r/furry_irl and r/thebluecorner moved to clone canvases (pxls.space, PlaceTwo).
3. Fights are with neighbours, and rivals often turn into partners. Block 06: r/chicubs and r/miamidolphins traded mutual protection; r/globaloffensive destroyed the Oilers logo, then helped move it; r/straya overran r/parahumans' beetle, then helped redraw it and the two called themselves mates; r/GrowTheTree's tree was consumed by the American flag, whose builders apologised and later offered to help rebuild.
4. Deals are struck in the thread, in Discord, or both. Block 06: r/miamidolphins honoured a two-pixel border agreed by representatives in r/placestart's Discord; r/furry_irl voted in Discord to abandon its first spot and used Green Lattice's diplomacy Discord; r/bangtan's K-pop groups defended one area through a group Discord. Some deals did not bind: r/GrowTheTree said r/Straya's crowd ignored its Discord deal; a r/germany member refused orders from a small group deciding in Discord; r/hunterxhunter members called their own last-minute removal of a neighbour's triangle a broken promise.
5. The goal is often set by one member. Block 06: r/bih's flag was one member's work; r/DiamondClub's <> was one member's call; r/Pigifs's sign was one member's call with pig gifs as a reward; r/spongebob had separate members calling for separate characters.
6. April Fools makeovers filled more coded turns than the canvas in many rooms: r/naruto, r/globaloffensive (an Overwatch makeover), r/hunterxhunter (Wagon Quest), r/pokemon (Team Skull), r/furry_irl (real animals), r/miamidolphins (fake trades).
7. Moderators: r/chicubs' moderators refused to ban canvas posts from the game thread; r/naruto's moderator set the spot; r/furry_irl's moderators set a four-pixel rule after April Fools; r/globaloffensive's automoderator removed canvas calls for their link form.
8. The atlas names former or covered works: r/gravityfalls ("(Covered) Bill Cipher") matches the room's account of loss to the void.

New in block 06, seen in three or more rooms and logged in the diary:
- A sub made for the canvas, sometimes around one small piece and what it stands for (TreePlace, GrowTheTree, loliconsunite, placehfarts), sometimes governing others (thebluecorner's rules for artists).
- Canvas work moved to a second sub made for it, to keep the main sub clear (parahumans, gorillaz, asktransgender).
- A neighbour asks permission before overlapping and gets it (bangtan, gravityfalls, hunterxhunter).
- A deal struck by a few said not to bind the crowd (GrowTheTree, hunterxhunter, germany).
- The void treated as a faction to fight or negotiate with (bangtan, gravityfalls, gorillaz, GrowTheTree, parahumans, asktransgender).

Paired lead checks, both sides read, block 06: agree for chicubs and miamidolphins, france and bih (an apology and a French forum outside Reddit), wales and furry_irl, polska and soylent, gorillaz and evedreddit, wow with heroesofthestorm and hearthstone, landry and madokamagica. Disagree: r/ftlgame says Etho asked protection and FTL honoured it; r/ethoslab's record shows only a black border kept against FTL and a shift to avoid a fight. Not comparable: r/thebluecorner, r/colombia and r/bangtan name deals with Germany that r/germany's record does not hold, because r/germany sends canvas work to r/placeDE.

## Contrary rooms

Block 01: morrowind and megaman said they were not organized; heyyea kept art it did not make; egypt's flag was a stranger's gift; duckgame mourned art the atlas lists as surviving; AprilKnights had an order with elections; flashtv's prank ran apart from canvas work; PinkVomitMonster called its lack of coordination its beauty; FloydVsVoid's founder regretted not compromising; anime mostly refused and argued credit; watchmen and TheAdventuresofTintin noticed art they did not visibly build; tagpro aimed at advertising; anime, qotsa, cfb and drugs disagree with the canvas fields. From the screen: UNLincoln, yerbamate, Redox, azores, archlinux.

Block 02: homelab, hentai, kpop and ubc, norge, cirkeltrek, loltyler1, bobross and nonbinary, zelda.

Block 03: ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft and GuildWars2, bardmains, placeDE.

Block 04: theitalyplace and spacexmasterrace; tampabaylightning; aoe2; 4chan; ice_poseidon; korea; drawhelix.

Block 05: greenlattice, norway, utaustin, france, masseffect, ducks and mariokart, natsume.

Block 06:
- thebluecorner: a sub made for the canvas that set rules for artists and claimed the right to curate; members argued all week whether the corner was pure blue or a backdrop for art.
- germany: the English-language sub was where neighbours came to ask; the flag was run in r/placeDE. The canvas fields link a TV tower, not the flag.
- vim: the logo is credited to r/ArchLinux.
- furry_irl: adopted a sign another person made, and gave its first spot to Wales.
- placehfarts: the room's work was one letter of another room's text; the linked artwork is larger.
- Pigifs: the war with r/babyelephantgifs was a joke in comments; the linked mark sits far from the coordinates the call named.
- TreePlace: a member refused to move the tree because moving would undo its meaning.
- evedreddit: answered a neighbour's envoy only with mock war; the sign later drew a lapsed player back.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 07:
- joining or finding work begun elsewhere, against starting it;
- organizing in the thread, against organizing in Discord or a second sub and reporting back;
- deals that bind a room, against deals made by a few that the crowd ignores;
- a deal turned into a room rule, against a deal held only by the organiser;
- a sub made for the canvas that governs others (greenlattice, thebluecorner), against one that only keeps a small piece (TreePlace, GrowTheTree);
- one organiser with alts or friends, against a room-wide effort;
- attacking first and building later, against building first and defending;
- rivals who stay rivals, against rivals who build together;
- the room's April Fools practice, against its canvas practice;
- the moderator as organiser, as obstacle, and as attacker;
- the canvas fields linking the room's work, against linking a neighbour's or nothing it describes;
- a national sub that runs its flag, against one that forwards the work to another sub (norway, germany).

## The last rooms read

Block 06, in reading order: wow, habs, MMA, placesnek, azores, k_on, eder, landry, polyamory, berkeley, katawashoujo, thebluecorner, naruto, parahumans, loliconsunite, ethoslab, Pigifs, globaloffensive, miamidolphins, chicubs, bangtan, gorillaz, germany, DiamondClub, pokemon, vim, TreePlace, evedreddit, gravityfalls, hunterxhunter, GrowTheTree, bih, placehfarts, furry_irl, spongebob, asktransgender, soylent.

## Ledgers at this close

- `lexicon-A1.md`: 619 lines. `running-A1.md`: 254 lines. `leads-A1.jsonl`: 955 lines. Every lead's `other` is in `order-A1.txt`; checked at this close with grep, sort and comm over the whole file. Five names differ only in letter case (Landry, LoveLive, MLS, Monero, RocketLeague, all from block 01); the validator accepts them.
- In this leg ten lexicon or lead lines carried a wrong item id (globaloffensive 2, miamidolphins 2, pokemon 2, bangtan, GrowTheTree, gravityfalls, asktransgender): the id came from a different code, or a placeholder was typed before the id was fetched. Each was corrected by an appended line; the wrong lines stay, superseded, and the diary names each one. Rule now: fetch every id with `cite.py` in one call, and append in a later call. Never type an id from memory.
- The gorillaz lead to r/eve named the wrong room for the Dreddit sign; a gorillaz-to-evedreddit lead is appended.
- The miamidolphins note's `named` line was corrected after reading r/chicubs: the Cues are the Cubs logo misspelt at the freeze, not a separate group.
- The hook rejects notes of 350 words or more, and quotes of four words or more outside `struck by`. First drafts still run 360 to 400; aim for 300.
- The diary rolled to `diary/A1-3.jsonl` in this leg.

## The next comparison

In block 07, for every room: did the artwork exist before the room's first call, and who built it? Do the canvas fields link the work the room describes? Was the deal struck in the thread, in Discord or in a second sub, and did the crowd accept that it bound them? Which side of the onset contrast is the room on, and is it a sub made for the canvas? Block 07 holds the first paired check of a national pact: r/denmark and r/sweden, with r/placehearts and r/japan. Read r/sweden against the leads that name Sweddit as a refusing owner (hunterxhunter), a permission-giver (berkeley) and an ally (germany). Read r/placehearts against r/placehfarts and r/asktransgender. Read r/texans against r/miamidolphins and r/katawashoujo.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
