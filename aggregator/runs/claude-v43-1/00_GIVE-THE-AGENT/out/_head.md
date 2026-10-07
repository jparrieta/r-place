# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-37, 2026-10-07, the eighteenth leg of the catch-up pass.

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

The catch-up pass is declared in `out/order-A1.txt` as comment lines `#<block><TAB><sub>` after the A1 order (the checker refuses a room named twice; comment lines are skipped). 702 rooms, blocks 20 to 48, 25 rooms each (block 48 has 2), listed with tiers and byte sizes in `out/_analysis/catchup-A1.tsv`. Tiers: 40 rooms whose concepts were partly served, then 187 with more than 170 concepts, then 158 whose ended line differs from the rule by more than an hour, then 317 others. `mem.py next` does not serve this pass; take the next block from the `#NN` lines (`grep "^#36" out/order-A1.txt`) and the diary (`mem.py diary --grep "amended" --limit 500`).

Blocks 20 to 37 are done: 450 of 702 rooms. The next leg reads block 38, starting with the first `#38` line in `order-A1.txt` (Lugarix, line 1159).
The reading route for the pass: `bash out/_analysis/catchup_read.sh <sub> case` (logs the room opened, prints case.md whole), then `... brief`, then `... check` (prints lines served against the total from `_mem_reads-A1.jsonl`). In the same turn, Read the note with the Read tool (the Edit tool needs it). Amend it, count with `wc -w`, and log `<sub> amended (catch-up): ...` with `--ids <sub>`. One bash call can log the last room, check `ls .pause`, and print the next case.md; print brief.md and the check in a second call. The shell shows at most 30 KB per call, and the overflow goes under CONTROL, which is read-denied.

Note length (J, 7 October 2026, in the stage file and in a message answered during A1b-35): about 350 words is a guide, not a limit. Length and wording are my judgement; the pass/fail rules stand (the fixed lines, concept ids, case and brief read before the note). Do not cut earlier lines to fit new ones; cut only what I would not miss later, and log it. Keep the new lines short: coder unsure about 25 words, later about 45. The hook now reports a note over the guide as advice and lets it stand; `validate.py` counts these as warnings (21 in block 35, 19 in block 36, 18 in block 37). If unsure about writing, ask J (`mem.py ask`). When cutting the last doing clause, keep a full stop; removing it removes the line break before `week:`, and the hook refuses the note (yogscast, AcePlace). A coder unsure line that says none, cites a concept id, or gives the brief's coverage ("N threads out of scope") is not case.md's word: replace it with case.md's limits and thread ids. Remove any gendered pronoun for a member when a line is cut.

After a compaction, do not trust edits made from the summary. Serve the room's case.md and brief.md again and check every id before logging (block 33 polandball).

`mem.py diary --grep` pages its output; pass `--limit 500` before counting lines. A grep pattern with parentheses matches nothing; grep on a plain word. macOS grep has no `-P`. A shell variable set from `$(...)` was refused by the permission check; run `wc -w` alone and type the count.

The harness's brief is empty for event-made subs (among them theblackvoid, placeDE, greenlattice, thebluecorner, placehearts, PlaceNL, placestart, ainbowroad; blocks 30 to 33 eighteen more; block 34 hoodr, aeskwadraat, purplecorner, starryknights, GreenCorner, Thegreatblackhole; block 35 AcePlace, PinkVomitMonster; block 37 GuardiansOfDatBoi, CryptoFR, ukplace); it is still served and checked, and the later line says so.

`validate.py A1` before this close: 0 errors, 58 warnings (notes over the 350-word guide). A coder unsure line already drawn from case.md in an earlier read is kept and extended, not replaced (3 rooms in block 36, 9 in block 37). When case.md shows an earlier line is wrong, correct it through the later line or a small logged edit (block 36: wales, buffalowizards, lofihiphop; block 37: bobross, linux, glasgow, ukplace).

## Section 5, done in A1b-19

- `out/coordinating-rule-A1.md`: the coordinating-turn rule. A turn counts when its label's leading act calls, assigns, plans, reports placement before hour 73, defends, makes or breaks a deal, or corrects another's placement; not when it recounts, jokes, mourns, thanks, praises, apologizes, blames, or is a moderator's removal. After hour 73 only calls or plans for canvas work count. Stage B1 copies it into `prior.md` §5; a change needs a departure line and a diary line, and figures under both rules.
- `out/organizing_end-A1.jsonl`: 705 lines, nine fields, recomputed by the close-check from the store (scripts `a1_ends.py` and `a1_codes_dump.py`, logged departures).
- Figures: 44,116 of 115,388 concepts coordinate (0.382). Nine rooms have no coordinating turn: watchmen, Redox, yerbamate, Lugarix, azores, ReBoot, PokemonSage, UNLincoln, tetris. 146 rooms have their last coordinating turn after hour 73. work_remained: kept 347, lost 218, silent 140.
- Measured error (ruling 5): agreement 79 of 100; precision 0.92, recall 0.66. Median end h72.02 with calls after hour 73, h71.69 without (ruling 4).

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed later in the run.

## What the checks found

Seven defects are in `defects.jsonl`, plus an eighth line answering the seventh. None blocks the reading. The first six: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas.

The seventh, answered by J (ruling 2): 25 rooms' linked artworks show placements before hour 0, earliest h-15.92 (AmericanFlaginPlace); they are Reddit's tests while the canvas was closed. Notes that say "placed from h-..." keep their words; catch-up later lines say tests (GrowTheTree, npr, rainbowgrid, Thegreatblackhole).

## The principal investigator's answer QA1-001

The concept-reach threshold stays at 0 items. No substitute measure is to be invented. Every room is read at concept level in the later model-building stages, and unplaced concepts are read at the end too.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- `n_off_platform`: median 4, max 88 (dankmemes).
- `px_window_share`: median 0.111, max 0.547; null for tenma.
- Concentration is null in 3 rooms (nonbinary, oltp, wario).
- 79 rooms have their last coded turn before hour 73.

## The onset contrast

`out/contrast.md`. Onset = first coded turn at hour 0 or later: early 132, late 61, neither 512. Early: hours 0 to before 3. Late: after hour 48. The confound is size (median items 5067 against 33); a held-size comparison (items 156 to 2770, 41 against 12) travels with it. Expectation: late rooms organize around finding space on a full canvas; early rooms around claiming and holding it. In every late room read, the linked work was placed from the first hours.

## The three sentences written before reading

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

What the reading found against them (`notes-A1.md` §6): the artwork was often on the canvas before the room spoke; coordinating turns do not all end near hour 73; rivals often became partners; deals often did not bind the crowd.

Seen three or more times and logged, blocks 10 to 37 (each block's rooms are in `running-A1.md`):
- The brief shows words or habits the canvas work reused (twelve rooms in block 35, eight in block 36, thirteen in block 37); a shared project ran the week before (five in block 35).
- Members outside the Discord missed the plan or refused the venue (block 36 dwarffortress, vocaloid); a venue or command could not bind every placer (block 37 polska, sixers).
- Green Lattice and Rainbow Road as host, permit office and border authority (blocks 19, 26 to 28; block 34 latin, planetside, esperanto).
- A representative, Discord or deal that cannot bind the crowd; restraint or deals not accepted by every member (blocks 19 to 31, 33, 34).
- A room relocates or trims its work when a neighbour asks (blocks 19, 28).
- Restraint named as the room's rule (blocks 10 to 24), qualified by the room's own conquest talk (blocks 25 to 28); attack talk beside restraint (blocks 32 to 37).
- A neighbour protects the room's work, or a room that wrecked one helps it after (blocks 19, 24 to 30, 33).
- Decisions made in Discord, IRC, Telegram or a second sub, seen only as returned (blocks 19, 24, 28, 30 to 37).
- One or two members carrying the work; credit as one member's claim; a remake or last mark by one member (blocks 19, 27 to 29, 31 to 33).
- Members joining work already under way, or a room credited with work another group started (blocks 31, 32; block 34 araragi).
- A canvas mark, call or label grown from something already running that week (blocks 20, 22 to 34).
- Misread edits, and the room's own defenders, scripts or bots undoing its work (blocks 22 to 31, 33).
- Bots or scripts deciding what stays, or named as makers (blocks 21, 24, 25, 29, 32).
- Members' own accounts of the same act disagreeing; blame never settled (blocks 23, 24, 29, 32, 33, 37).
- The work called pointless, spam or tiring, too small or thinly staffed; the result recounted as partial (blocks 24 to 28, 30, 31, 33, 34).
- Moderators gathering, routing or turning the canvas work (blocks 25 to 28, 30, 31, 34).
- The room's own April Fools switch or fake rules running beside the canvas (blocks 33, 34).
- The event recruiting into the sub, or to the product (blocks 25 to 33).
- The work carried elsewhere after the close (blocks 25 to 30, 32 to 34, 36, 37).

## Contrary rooms

Blocks 01 to 18 by name only (details in `notes-A1.md` and earlier heads): morrowind, megaman, heyyea, egypt, duckgame, AprilKnights, flashtv, PinkVomitMonster, FloydVsVoid, anime, watchmen, TheAdventuresofTintin, tagpro, qotsa, cfb, drugs, UNLincoln, yerbamate, Redox, azores, archlinux; homelab, hentai, kpop, ubc, norge, cirkeltrek, loltyler1, bobross, nonbinary, zelda; ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft, GuildWars2, bardmains, placeDE; theitalyplace, spacexmasterrace, tampabaylightning, aoe2, 4chan, ice_poseidon, korea, drawhelix; greenlattice, norway, utaustin, france, masseffect, ducks, mariokart, natsume; thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit; falcons, formula1, slovenia, sweden, wine, btc, nin, uoft; ReBoot, nVade, epublica, lego, foxes, math, popheads, ockytop; sadboys, spacex, Fez, warthunder, nascar, israel, magictcg, tenma, ManningPlace; cgpgrey, EraseThePlace, dankmemes, anarcho_capitalism, twice, TeamYellowPlace, mcgill, PokemonSage; totallynotrobots, finland, udub, GreenEmpire, danganronpa, india; ontario, orderofthebluecorner, CelticFc, enterthegungeon, eve, anarchocapitalism, teamcube; counting; polandball, ubreddit, canucks, rust, fivenightsatfreddys, kanye, azerbaijan; theblackvoid, rainbowgrid, raocow, Slovakia, taiwan, oltp, asexual; PlaceNL, pcmasterrace, PinkUnion, streetfighter, aeskwadraat, Mario, wallstreetbets; placestart, starryknights, tf2, brasil, wholesomememes, Thegreatblackhole, GreenCorner, ibo, wario; destiny, Summit1G, Okami, 2007scape, lithuania, stardewvalley, planetside.

Block 19 (details in `notes-A1.md`): ainbowroad, dota2, Braveryjerk, dofus, Russiaclan, rotmg.

Catch-up notes whose not-this line the account qualified: utaustin (block 23); miamidolphins, placehearts, chicubs (block 24); lego, lebanon, israel, vegan, touhou, magictcg (block 25); straya, farmcarrots, TransFlagPlace, titanfall (block 26); rust, funhaus, AmericanFlaginPlace (block 27); trees, starvstheforcesofevil, brasil, prequelmemes (block 28); phish (block 29); bardmains, osu (block 30); vim, TreePlace, bih, japan (block 31); PORTUGALCARALHO, npr (block 32); GreenEmpire, armenia, satania, nyjets (block 33); hoodr, muse, esperanto, araragi, twentyonepilots, GreenCorner, Thegreatblackhole, yogscast (block 34); forsen, AcePlace, lithuania, terraria, PinkVomitMonster (block 35); DatBoi, WPI, ubc (block 36); texastech, linux, dallasstars, oman, sixers (block 37). The later lines say how.

The one room that fits nothing else, chosen at A1c: r/Summit1G. 82 of its 140 coded turns are a raiding rival chat's chant.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to carry into B1:
- Who started the work: joining or finding work begun elsewhere, against starting it; a linked region placed from the first hours, against the room's late first call; a work credited to another sub or its Discord; a work the room mourned as lost that the canvas keeps.
- Where organizing happened: in the thread, against in Discord, IRC, Telegram, a second sub, a private sub (ockytop), a forum, or a stream; venues interleaved rather than replaced (esperanto); plans brought back for members outside the venue.
- Deals: binding, against not kept; truce against alliance; living on an ally's land by permission; hosting others' works in exchange for upkeep (TeamYellowPlace); leaders' deals against members' fights; a room kept by the stronger side's terms (Slovakia).
- A sub made for the canvas that governs others, polices purity, migrates, or claims a colour; or forms late around a pattern others repeated (rainbowgrid).
- Scripts: self-defence, refused, repairing a rival, joint, fighting the room's own plan, a neighbour's bot erasing an unregistered addition (yumenikki); hand defence against scripts (GabrielDropout).
- The moderator as organiser, obstacle, funnel, enforcer or permit office; a moderator who is also the main defender (oneplus).
- The end of organizing: before hour 73, at the close, or in calls to rebuild after it; the work kept elsewhere after the close.

## What the catch-up pass found so far (blocks 20 to 37)

Every block's findings are in `running-A1.md` under "catch-up block NN" (block 37: entries 679 to 686) and in the list of patterns seen three times above.

## The last rooms read

Catch-up block 37, in order: bobross, texastech, spelunky, ghibli, polska, linux, yerbamate, dallasstars, ravens, iceland, GuardiansOfDatBoi, CryptoFR, oman, columbia, ftlgame, Bravenewbies, ohio, lovelive, Madeon, freedomplanet, xcom, glasgow, uruguay, ukplace, sixers.

## Ledgers at this close

- `lexicon-A1.md`: 1,289 lines. `running-A1.md`: 686 lines (this leg 8 entries). `leads-A1.jsonl`: 2,478 lines. `departures.jsonl`: 9 lines. `defects.jsonl`: 8 lines.
- Rule, kept:
  - Fetch every id with `cite.py`. Check every lead's room with grep against the frame before appending. Append through a grep filter on the item id. Never type an id from memory; check an id carried through a compaction against the notes or the diary before using it.
  - Copy lexicon words from the item text, never from the coder's labels.
  - Never log "noted" or "passed" in the same call that writes the note; wait for the hook's answer.
  - Count a ledger's lines after appending, before logging the count; count the diary's trim lines before writing the closing line.
  - There is no `--kind close`; log the closing line as a note.
- The permission check refuses "=w=", for and while loops, shell functions, heredocs, awk and a variable set from `$(...)`. The command guard reads a bare "rm" inside quoted text as a delete. Use the Write and Edit tools for file content; an Edit whose old text spans non-adjacent lines fails, so edit lines one at a time.
- The diary rolls into a new part as it grows; during A1b-37 it moved into part A1-38. After a compaction the guard requires the exact line "compacted; head reconciled" through `mem.py log --kind note`.

## The next comparison

Catch-up block 38 (25 rooms), from the `#38` lines in `order-A1.txt`. For each room ask: does the coder's account change who started the work, where it was decided, what became of it, or whether the room's members kept their deals? Does the brief show a joke, ritual or shared project the canvas work grew from? Record only what changes the note.

When the pass ends (block 48), compare the `later:` lines across rooms, by the patterns listed above.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
