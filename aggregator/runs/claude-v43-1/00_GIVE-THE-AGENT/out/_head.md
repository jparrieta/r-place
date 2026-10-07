# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-29, 2026-10-07, the tenth leg of the catch-up pass.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Legs A1a, A1b-01 to A1b-19 and A1c are closed; A1c closed at the interview cut. All 705 rooms have a note.

J's rulings of 7 October 2026 (after the A1c handback) opened a catch-up pass, legs A1b-20 onward:
1. For every room whose case.md or brief.md was not served whole in A1, read both whole, then amend the note: replace the `coder unsure:` line with what case.md says, with thread ids, and add a dated `later:` line wherever the account or the brief changes the note. Forests and concepts are not part of the pass. Read each file whole, with no head, cut or limit below its total; before amending, check in the read log that lines served equal the total. If a block does not fit in a leg, stop at a safe stop and pause; never shorten the route. Log any departure the moment it is made.
2. Hour 0 is the canvas opening; Reddit's tests appear from about hour -16. Defect 7 is answered (a line appended to `defects.jsonl`).
3. The onset is the first coded turn at hour 0 or later. Done: only r/italy moves (to the early side); early 132, late 61, held size unchanged (appended to `contrast.md`).
4. The organizing end reported with and without calls after hour 73. Done: `out/organizing_end-to73-A1.jsonl`.
5. The rule is kept; its measured error is in `coordinating-rule-A1.md`.
6. `leads-outside-frame-A1.jsonl` is a ledger B1 may read.
7. `mem.py diary --last` now reads the newest part.

The catch-up pass is declared in `out/order-A1.txt` as comment lines `#<block><TAB><sub>` after the A1 order (the checker refuses a room named twice; comment lines are skipped). 702 rooms, blocks 20 to 48, 25 rooms each (block 48 has 2), listed with tiers and byte sizes in `out/_analysis/catchup-A1.tsv`. Tiers: 40 rooms whose concepts were partly served, then 187 with more than 170 concepts, then 158 whose ended line differs from the rule by more than an hour, then 317 others. `mem.py next` does not serve this pass; take the next block from the `#NN` lines (`grep "^#30" out/order-A1.txt`) and the diary (`mem.py diary --grep "amended" --limit 500`).

Blocks 20 to 29 are done: 250 of 702 rooms. The next leg reads block 30, starting with the first `#30` line in `order-A1.txt` (pepe, line 959).
The reading route for the pass: `bash out/_analysis/catchup_read.sh <sub> case` (logs the room opened, prints case.md whole), then `... brief`, then `... check` (prints lines served against the total from `_mem_reads-A1.jsonl`). Each file is under 30 KB, so the output is shown whole. Then Read the note, amend it, and log `<sub> amended (catch-up): ...` with `--ids <sub>`. One bash call can log the last room, check `ls .pause`, and open the next.

Note length: the hook refuses a note at 350 words or more by its own count, which runs close to `wc -w`. Concept ids, hours and coordinates each count as words, so a doing line full of ids runs long. Rewrite or edit doing and week first, to about 60 words with one or two ids per clause; coder unsure about 20, later about 50; drop the placer count from made. Aim for `wc -w` of 340 or less; at 347 or more, trim even without a refusal and log it. A coder unsure line that cites a concept id or the brief's coverage is not case.md's word: replace it with thread ids. Block 29: 11 notes refused by the hook and 2 trims by `wc -w`, each logged. In block 29 the egypt note was logged as passing before the hook's refusal was seen; a correction line followed.

`mem.py diary --grep` pages its output; pass `--limit 500` before counting lines. A grep pattern with parentheses matches nothing; grep on a plain word.

The harness's brief is empty for event-made subs (theblackvoid, FloydVsVoid, placecanada, placeDE, monalisaclan, theitalyplace, greenlattice, thebluecorner, placehearts, TheFarLeftSide, EraseThePlace, farmcarrots, TransFlagPlace, PurplePixels, SquareSpiral, AmericanFlaginPlace, AvoArmy, PlaceNL, placestart, ainbowroad); it is still served and checked, and the later line says so. Where a coder unsure line said none and the account names limits, the line is replaced with the limits.

`validate.py A1` before this close: 0 errors, 0 warnings.

## Section 5, done in A1b-19

- `out/coordinating-rule-A1.md`: the coordinating-turn rule. A turn counts when its label's leading act calls, assigns, plans, reports placement before hour 73, defends, makes or breaks a deal, or corrects another's placement; not when it recounts, jokes, mourns, thanks, praises, apologizes, blames, or is a moderator's removal. After hour 73 only calls or plans for canvas work count. Stage B1 copies it into `prior.md` §5; a change needs a departure line and a diary line, and figures under both rules.
- `out/organizing_end-A1.jsonl`: 705 lines, nine fields, recomputed by the close-check from the store (scripts `a1_ends.py` and `a1_codes_dump.py`, logged departures).
- Figures: 44,116 of 115,388 concepts coordinate (0.382). Nine rooms have no coordinating turn: watchmen, Redox, yerbamate, Lugarix, azores, ReBoot, PokemonSage, UNLincoln, tetris. 146 rooms have their last coordinating turn after hour 73, mostly calls to rebuild on later canvases. work_remained: kept 347, lost 218, silent 140.
- Reconciliation with the notes' `ended` lines: same 268, within an hour 156, differs 281; the notes stand.
- Measured error (ruling 5): agreement 79 of 100; precision 0.92, recall 0.66. Median end h72.02 with calls after hour 73, h71.69 without (ruling 4).

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed later in the run.

## What the checks found

Seven defects are in `defects.jsonl`, plus an eighth line answering the seventh. None blocks the reading. The first six: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas.

The seventh, answered by J (ruling 2): 25 rooms' linked artworks show placements before hour 0, earliest h-15.92 (AmericanFlaginPlace); they are Reddit's tests while the canvas was closed. Notes that say "placed from h-..." keep their words; catch-up later lines say tests (blocks 26 to 28: leagueoflegends, AmericanFlaginPlace, trees, PlaceNL, scotland, 2007scape, ainbowroad).

## The principal investigator's answer QA1-001

The concept-reach threshold stays at 0 items. No substitute measure is to be invented. Every room is read at concept level in the later model-building stages, and unplaced concepts are read at the end too.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- concept_reach_threshold: 0 items, kept by QA1-001.
- `n_off_platform`: median 4, max 88 (dankmemes).
- `px_window_share`: median 0.111, max 0.547; null for tenma.
- Concentration is null in 3 rooms (nonbinary, oltp, wario).
- 79 rooms have their last coded turn before hour 73.
- Coordinating turns 0.382 of concepts; organizing_end_hour null in 9 rooms, above 73 in 146.

## The onset contrast

`out/contrast.md`. Onset = first coded turn at hour 0 or later: early 132, late 61, neither 512. Early: hours 0 to before 3. Late: after hour 48. The confound is size (median items 5067 against 33); a held-size comparison (items 156 to 2770, 41 against 12) travels with it. Expectation: late rooms organize around finding space on a full canvas; early rooms around claiming and holding it.

The kinds of late room found in the reading are listed in `notes-A1.md` and the A1b-26 head. In every late room read, the linked work was placed from the first hours.

## The three sentences written before reading, against nineteen blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

What the reading found against them (`notes-A1.md` §6): the artwork was often on the canvas before the room spoke; coordinating turns do not all end near hour 73; rivals often became partners; deals often did not bind the crowd.

Seen three or more times and logged, blocks 10 to 29:
- Green Lattice and Rainbow Road as host, permit office and border authority (block 19: ainbowroad, gameboy, rpi; blocks 26 to 28).
- A representative, Discord or deal that cannot bind the crowd: catalunya, crusaderkings, apocalypserising, uofm, Summit1G, reddevils, rpi; blocks 22 to 28; block 29 ukraine, phish, rotmg, ScottPilgrim, megaman.
- A room relocates or trims its work when a neighbour asks: Northwestern, stardewvalley, RelientK, yogscast, parabola, predators, fxKorea, Russiaclan; block 28 dota2.
- Restraint named as the room's rule: prequelmemes, yogscast, Goodboye, notredame, stardewvalley, parrots, europe, traaaaaaannnnnnnnnns, WisconsinBadgers, predators; block 24 ireland, greenbaypackers, formula1. Blocks 25 to 28 qualify it: the account showed the room's own encroachment or conquest talk beside a note that stressed restraint (six, six, eight and seven rooms).
- A room that crowded or wrecked a neighbour helps it after, or a neighbour protects the room's work: 2007scape, uofm, rotmg, clg, winnipegjets, monsterhunter; blocks 24 to 28; block 29 monero's snowman, rotmg, batman, nuclearthrone, reddevils.
- A second sub or Discord taking or deciding the canvas work: europe, crusaderkings, uofm, denverbroncos, lithuania, winnipegjets; block 24 eight rooms; block 28 AvoArmy.
- One or two members carrying the work, or too few builders: dofus, fxKorea, gameboy, plus the late-room list; blocks 27, 28; block 29 six small rooms (tokyo, TheAdventuresofTintin, signal, mamamoo, riskofrain, bahrain).
- A canvas mark, call or label grown from something already running that week (blocks 20, 22 to 29; block 29 five rooms, among them austria's Monday complaining thread and batman's monthly vote).
- Misread edits: a neighbour's work taken for an attack (block 22), the room's own planned change, people or repairers taken for an attack (blocks 23, 24, 26 to 29; block 29 ScottPilgrim, monero, littlewitchacademia, seahawks).
- An accused attacker defended, the real culprit named, or blame never settled (blocks 23, 24; block 29 frc, seahawks, austria, nuclearthrone, ukraine).
- Bots, scripts or alts named as the makers, or scripts fighting the room's own plan (blocks 21, 24, 25); credit after the close disputed between hands, scripts and other subs (blocks 26 to 28); bots making people feel powerless (block 29 littlewitchacademia, egypt, frc).
- Celebration disputed after the close (blocks 24, 25); the work called pointless, spam or tiring (blocks 27, 28).
- Promised help not shown carried out, or an approved build missing (block 28: rwby, ainbowroad, PlaceNL).
- Moderators meeting, routing or turning the canvas work (blocks 25 to 28).
- The event recruiting into the sub (blocks 25 to 28; block 29 monero, ScottPilgrim).
- The room fighting itself over its design (block 26: india, leagueoflegends, titanfall).
- The work carried elsewhere after the close, or the call refused: successor canvases, flairs, atlases, beads, a museum print, a kept Discord (blocks 25 to 29; block 29 seven rooms).

## Contrary rooms

Blocks 01 to 18 by name only (details in `notes-A1.md` and earlier heads): morrowind, megaman, heyyea, egypt, duckgame, AprilKnights, flashtv, PinkVomitMonster, FloydVsVoid, anime, watchmen, TheAdventuresofTintin, tagpro, qotsa, cfb, drugs, UNLincoln, yerbamate, Redox, azores, archlinux; homelab, hentai, kpop, ubc, norge, cirkeltrek, loltyler1, bobross, nonbinary, zelda; ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft, GuildWars2, bardmains, placeDE; theitalyplace, spacexmasterrace, tampabaylightning, aoe2, 4chan, ice_poseidon, korea, drawhelix; greenlattice, norway, utaustin, france, masseffect, ducks, mariokart, natsume; thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit; falcons, formula1, slovenia, sweden, wine, btc, nin, uoft; ReBoot, nVade, epublica, lego, foxes, math, popheads, ockytop; sadboys, spacex, Fez, warthunder, nascar, israel, magictcg, tenma, ManningPlace; cgpgrey, EraseThePlace, dankmemes, anarcho_capitalism, twice, TeamYellowPlace, mcgill, PokemonSage; totallynotrobots, finland, udub, GreenEmpire, danganronpa, india; ontario, orderofthebluecorner, CelticFc, enterthegungeon, eve, anarchocapitalism, teamcube; counting; polandball, ubreddit, canucks, rust, fivenightsatfreddys, kanye, azerbaijan; theblackvoid, rainbowgrid, raocow, Slovakia, taiwan, oltp, asexual; PlaceNL, pcmasterrace, PinkUnion, streetfighter, aeskwadraat, Mario, wallstreetbets; placestart, starryknights, tf2, brasil, wholesomememes, Thegreatblackhole, GreenCorner, ibo, wario; destiny, Summit1G, Okami, 2007scape, lithuania, stardewvalley, planetside.

Block 19: ainbowroad (a permit office for other subs), dota2 (its own scripts fought each other), Braveryjerk (one call, no placement), dofus (one member alone), Russiaclan (every border by alliance), rotmg (sprites made, lost, remade).

Catch-up notes whose not-this line the account qualified: utaustin (block 23); miamidolphins, placehearts, chicubs (block 24); lego, lebanon, israel, vegan, touhou, magictcg (block 25); straya, farmcarrots, TransFlagPlace, titanfall (block 26); rust, funhaus, AmericanFlaginPlace (block 27); trees, starvstheforcesofevil, brasil, prequelmemes (block 28); phish (block 29, the later lines say how).

The one room that fits nothing else, chosen at A1c: r/Summit1G. 82 of its 140 coded turns are a raiding rival chat's chant.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to carry into B1:
- Who started the work: joining or finding work begun elsewhere, against starting it; a linked region placed from the first hours, against the room's late first call; a work credited to another sub (texas to r/houston), a private group's joke (AvoArmy), or another sub's Discord (shield's HYDRA); a work the room mourned as lost that the canvas keeps (serbia's crest).
- Where organizing happened: in the thread, against in Discord, a second sub, a forum, or a stream; a Discord that decides for the room, against a meeting place; a sub that moved canvas talk to a side sub (osugame, sweden, parahumans, suomi, greece, texas, mylittlepony, europe).
- Deals: binding, against not kept; truce against alliance; living on an ally's land by permission (nuclearthrone's Y.V. in Ireland's flag); repair after taking space; leaders' deals against members' fights; protection called a mafia (paladins); a contact the other side says does not represent it (placestart).
- A sub made for the canvas that governs others, keeps a single work, asks leave, polices purity, migrates, or claims a colour.
- A national flag as permission office, front line, alliance office, or joint work with a rival.
- Scripts: self-defence, refused, repairing a rival, joint, fighting the room's own plan, running past their owners, keeping an obsolete design.
- The moderator as organiser, obstacle, funnel, enforcer, permit office, or newcomer to the canvas (nascar).
- A leader outside the room: a streamer, a chat, a single organiser, a national Discord, an outside forum; a chief voted in by the thread (quebec).
- Restraint named as the room's rule, against expansion; purity against art on blue.
- The end of organizing: before hour 73, at the close, or in calls to rebuild after it; the work kept elsewhere after the close.

## What the catch-up pass found so far (blocks 20 to 29)

Every block's findings are in `running-A1.md` under "catch-up block NN" (block 29: entries 614 to 622) and in the list of patterns seen three times above.

## The last rooms read

Catch-up block 29, in order: rotmg, reddevils, tokyo, megaman, egypt, riskofrain, ukraine, austria, littlewitchacademia, bahrain, mamamoo, strangerthings, TheAdventuresofTintin, shield, cloud9, alberta, monero, signal, nuclearthrone, ScottPilgrim, batman, kindafunny, seahawks, phish, frc.

## Ledgers at this close

- `lexicon-A1.md`: 1,289 lines. `running-A1.md`: 622 lines (this leg 9 entries). `leads-A1.jsonl`: 2,478 lines. `departures.jsonl`: 9 lines. `defects.jsonl`: 8 lines.
- `out/leads-outside-frame-A1.jsonl`: two lead lines (FederationPlace to harvard, clg to teamsolomid), a ledger B1 may read (ruling 6).
- Rule, kept:
  - Fetch every id with `cite.py`. Check every lead's room with grep against the frame before appending. Append through a grep filter on the item id. Never type an id from memory.
  - Copy lexicon words from the item text, never from the coder's labels.
  - Never log "noted" or "passed" in the same call that writes the note; wait for the hook's answer.
  - Count a ledger's lines after appending, before logging the count; count the diary's trim lines before writing the closing line.
  - `mem.py log --kind` accepts note, opened, pause and the stage kinds; there is no kind "close". Log the closing line as a note.
- The permission check refuses "=w=", for and while loops, shell functions, heredocs and awk. The command guard reads a bare "rm" inside quoted text as a delete. Use the Write and Edit tools for file content; an Edit whose old text spans non-adjacent lines fails, so edit lines one at a time.
- The diary rolls into a new part as it grows; it moved from part A1-23 to A1-25 during this leg. After a compaction the guard requires the exact line "compacted; head reconciled" through `mem.py log --kind note`.

## The next comparison

Catch-up block 30 (25 rooms), from the `#30` lines in `order-A1.txt`. For each room ask: does the coder's account change who started the work, where it was decided, what became of it, or whether the room's members kept their deals? Does the brief show a joke, ritual or shared project the canvas work grew from? Record only what changes the note.

When the pass ends (block 48), compare the `later:` lines across rooms, by the patterns listed above.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
