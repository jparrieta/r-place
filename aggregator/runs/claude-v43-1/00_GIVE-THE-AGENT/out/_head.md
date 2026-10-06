# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-17, 2026-10-07.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-17 read blocks 01 to 17 whole (53, 48, 62, 44, 34, 37, 36, 30, 52, 50, 21, 35, 1, 32, 37, 46 and 35 rooms). 652 of 705 rooms have a note in `out/rooms/`. 53 rooms remain, in blocks 18 and 19 (35 and 18 rooms). The next leg is A1b-18. At this close `mem.py next` names r/2007scape, the first room of block 18. Always take the next room from `mem.py next`, never from this file.

Block 19 is the last block. In its leg, before the close, write `coordinating-rule-A1.md` and `organizing_end-A1.jsonl` (stage file §5).

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count.

`validate.py A1` at this close: 0 errors, 0 warnings. 652 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading:
- r/tenma has no canvas line;
- r/archlinux has a coded turn at hour 100.9;
- `n_codes_coder` has two meanings;
- `items.jsonl` has an undocumented state `collapsed`;
- concept reach is 1.0 everywhere;
- r/yogscast's first coded turn is not about the canvas.

Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh defect, not yet filed: linked artworks with region placements before hour 0. Nineteen rooms now carry such a case:
- through block 14: FloydVsVoid, ProfessorLayton, SwissNeutralityZone (shared with switzerland), monalisaclan, radiohead, aoe2, thebluecorner, globaloffensive, GrowTheTree, nin, npr, starcitizen;
- block 15: rainbowgrid, AmericanFlaginPlace;
- block 16: trees, afip, PlaceNL, scotland;
- block 17: Thegreatblackhole (The First Void, 9,343 px, from h-14.52).

The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it.

## The principal investigator's answer QA1-001

The concept-reach threshold stays at 0 items. No substitute measure is to be invented. Every room is read at concept level in the later model-building stages, and unplaced concepts are read at the end too. `notes-A1.md` says that the measure gives no cut in this store.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- concept_reach_threshold: 0 items, kept by QA1-001.
- `n_off_platform`: median 4, max 88 (dankmemes: its canvas concepts name one Discord).
- `px_window_share`: median 0.111, max 0.547; null for tenma.
- Concentration is null in 3 rooms (nonbinary, oltp, wario). r/wario has 0 coded authors.
- 79 rooms have their last coded turn before hour 73.

## The onset contrast

`out/contrast.md`. Early: first coded turn after hour 0 and before hour 3, 131 rooms. Late: first coded turn after hour 48, 61 rooms. The confound is size (median items 5067 against 33). A held-size comparison (items 156 to 2770, 41 against 12) travels with it. Expectation: late rooms organize around finding space on a full canvas; early rooms around claiming and holding it.

Block 17 early rooms, six: tf2, brasil, wholesomememes, rwby, kirby, portugal. The first day of four of them was the sub's own April Fools joke (rwby's restyle, wholesomememes' no-swearing rule, kirby's Jack Kirby room, brasil's Argentina takeover). tf2 and brasil are large rooms (270 and 277 coded authors) whose own members worked against their plan.

Block 17 late rooms, three:
- r/Villanova (h56.66): one member, then friends (the sixth kind).
- r/guatemala (h49.38): ask and move, ending with a heart others had placed from the first hours.
- r/ibo (h58.56): joined and defended an IB logo placed from h1.14, then called it a failed mission; the canvas keeps it (third kind, arrive to defend work others built).

The kinds so far:
- ask and move: COSI, UPenn, sheffield, corridor, MiamiHurricanes, mysterydungeon, CSUFoCo, latin, guatemala;
- take, refuse once, shuffle: Cornwall;
- arrive to defend work others built: cgpgrey, OrderOfTheKoi, VelvetUnderground, ibo;
- take by script over objections: udub;
- talk about a site and find the mark already there: sakartvelo, UNLincoln, vietnam; aeskwadraat (mark never found);
- one member alone or with friends: CelticFc, azerbaijan, tetris, DevonUK, Produce101, Villanova;
- possibly a seventh, a sub formed late around a pattern already there: rainbowgrid.

In every late room so far, the linked work was placed from the first hours. No size test yet.

## The three sentences written before reading, against seventeen blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke. Block 17: the linked region predates the room's first call in ibo, purdue (h16.1), montenegro (h42.1), unturned (h26.6), cowchop (h23.2), edboxes (h27), starryknights (painting done at its first turn) and placestart. The canvas links works a room never names: r/wario (Ashley), r/kirby (three Kirbys, the largest with 18,566 placers against 33 coded authors).
2. Coordinating turns end mostly between hours 68 and 73. Block 17's earlier ends:
   - r/Thegreatblackhole h34.51 (it migrated to r/theblackvoid at h18.1);
   - r/wario h46.97 (one post);
   - r/GreenCorner h48.41 (corner lost to Blue by h17);
   - r/guatemala h58.93;
   - r/starryknights h65.85.
3. Fights are with neighbours, and rivals often become partners. Block 17:
   - r/turkey made a heart with Greek users from h43 and members disputed it after the close;
   - an Argentine repaired r/brasil's flag "more than my own" (c0470);
   - r/purdue refused to attack Illinois, which had helped it;
   - r/cowchop maintained the logos of Funhaus, Naruto and One Piece.
4. Deals often do not bind the crowd. Block 17:
   - r/turkey: a member answered McGill that no one could stop free people (c0055);
   - r/cowchop: a Funhaus emissary apologised for pixels it could not control (c0024);
   - r/rwby: its Discord chose to ram through neighbours (c0256), then the room repaid those who moved;
   - r/placestart: treaties did not stop its own builders and scripts.
5. A room's own members worked against its plan: r/tf2 members undid the sub's logo redesign believing it vandalism (c0311); r/brasil members named Brazilians as most of the flag's vandals (c0210); r/twentyonepilots ran several threads with no shared plan.
6. April Fools filled the first day of most early rooms: rwby, wholesomememes, kirby, brasil, unturned, tf2.
7. Moderators: r/wholesomememes' moderators removed canvas posts as reposts or not memes; r/turkey and r/unturned funnelled canvas posts into one sticky or megathread; r/russia banned canvas posts.
8. Scripts: one script chosen so members do not work against each other (purdue c0272); bare hands claimed while a script ran (tf2 c0363, c0364); bots blamed for spoiling the end (brasil, GabrielDropout, Thegreatblackhole).

Seen three or more times and logged, blocks 10 to 17:
- Green Lattice and Rainbow Road as host, border authority and permission office. Block 17: kirby (Green Lattice's diplomacy list), cowchop (peace on condition of building upward), geometrydash, portugal, sips.
- The Blue Corner as a host under truce, and as an invader: GreenCorner lost its corner to Blue.
- r/placestart governing others' space; block 17: placestart itself, whose own builders and scripts overran its treaties.
- A room that covered or wrecked a work helps rebuild it, or repays those who moved: rwby (BikiniBottomTwitter), tf2 (EVE, RotMG), cowchop; before: PlaceNL restitution, philippines.
- A representative who cannot bind the crowd; members disclaiming the room's voice: turkey, cowchop, rwby, tf2 (an extremist few c0142); before: PlaceNL, poland, stlouisblues.
- A room relocates or shrinks its work when a neighbour asks: unturned (shrinking against MSU), edboxes (moved between Quebec and Iceland), tf2.
- Restraint named as the room's rule: cavestory, wholesomememes (borders kept c0166), tf2, purdue (neighbourly as the survival rule c0200), unturned (c0093), rwby (no greed c0265).
- Bots and scripts: held works while organisers restrained them; refused on principle; a room's own bots fighting each other (Linux's in cowchop's record c0095); copied between rooms (Temple's script in purdue); bots said to have taken over at the end (brasil, Thegreatblackhole).
- A Discord that controls who may edit, or a layer above rooms: rwby's Discord deciding to ram through; brasil's Discord of over 120 against 7-1 raids.
- The Dutch as pressing neighbours: turkey (the first site over the Dutch flag; a Dutch Discord of 400).
- A national sub sends canvas work to a second sub or Discord: brasil (r/placebr), turkey (r/GreecePlace).
- Living on an ally's land by permission: purdue (inside Police State's white space by compromise).
- The canvas keeping a work the room called lost: raocow, futanari, CSUFoCo, ibo.
- Colour factions: PinkUnion, purplecorner, GreenCorner (elections and polls during attack).

Paired lead checks for block 17 are in the diary, one line per room. Most leads agree on both sides. Where they agree only in part, the missing half is a deal or request absent from one room's coded concepts, mostly in large rooms with many threads out of scope (rwby 329, tf2 583, brasil 518).

## Contrary rooms

Blocks 01 to 15: see `notes-A1.md` and earlier heads; kept here by name only.
- Block 01: morrowind, megaman, heyyea, egypt, duckgame, AprilKnights, flashtv, PinkVomitMonster, FloydVsVoid, anime, watchmen, TheAdventuresofTintin, tagpro, qotsa, cfb, drugs; from the screen UNLincoln, yerbamate, Redox, azores, archlinux.
- Block 02: homelab, hentai, kpop and ubc, norge, cirkeltrek, loltyler1, bobross and nonbinary, zelda.
- Block 03: ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft and GuildWars2, bardmains, placeDE.
- Block 04: theitalyplace and spacexmasterrace; tampabaylightning; aoe2; 4chan; ice_poseidon; korea; drawhelix.
- Block 05: greenlattice, norway, utaustin, france, masseffect, ducks and mariokart, natsume.
- Block 06: thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit.
- Block 07: falcons, formula1, slovenia, sweden, wine, btc, nin, uoft.
- Block 08: ReBoot, nVade, epublica, lego, foxes, math, popheads, ockytop.
- Block 09: sadboys, spacex, Fez, warthunder, nascar, israel, magictcg, tenma, ManningPlace.
- Block 10: cgpgrey, EraseThePlace, dankmemes, anarcho_capitalism, twice, TeamYellowPlace, mcgill, PokemonSage.
- Block 11: UNLincoln, totallynotrobots, finland, udub, GreenEmpire, danganronpa, india.
- Block 12: ontario, orderofthebluecorner, CelticFc, enterthegungeon, eve, anarchocapitalism, teamcube.
- Block 13: counting.
- Block 14: polandball, ubreddit, canucks, rust, fivenightsatfreddys, kanye, azerbaijan.
- Block 15: theblackvoid, rainbowgrid, raocow, Slovakia, taiwan, oltp, asexual.
- Block 16: PlaceNL, pcmasterrace, PinkUnion, streetfighter, aeskwadraat, Mario, wallstreetbets.

Block 17:
- placestart: a sub made for the canvas that ran treaties while its own builders and scripts overran them.
- starryknights: its first turn shows the painting already done; it credits the starters.
- tf2: members undid their own sub's redesign as vandalism; scripts refused while one ran.
- brasil: its members named Brazilians as most of the flag's vandals; a rival nation's member repaired it.
- wholesomememes: its moderators removed most canvas posts; LOVE was one member's doodle kept by a few.
- Thegreatblackhole: a void that argued to spare art and migrated to another sub after 13 hours.
- GreenCorner: a colour faction that held elections during attack and lost its corner by h17.
- ibo: a late room that defended a logo placed from h1.14 and called it a failure.
- wario: one post; the canvas links a character it never names.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in blocks 18 and 19:
- Who started the work:
  - joining or finding work begun elsewhere, against starting it;
  - a linked region placed from the first hours, against the room's late first call;
  - a linked region far from where the room built, or never named;
  - a work the room mourned as lost that the canvas keeps.
- Where organizing happened: in the thread, against in Discord, a second sub or a forum; a Discord that decides for the room, against a meeting place; layers above rooms.
- Deals:
  - deals that bind a room, against deals its own participants do not keep;
  - a truce against an alliance;
  - living on an ally's land by permission;
  - restitution or repayment after taking space.
- A sub made for the canvas that governs others, keeps a single work, asks leave, erases, fades, polices purity, migrates (Thegreatblackhole), forms late around a pattern, spreads, or claims a colour.
- A national flag run as a permission office, a watcher, a front line, an alliance office, a restitution office, or a joint work with a rival (turkey's heart).
- Scripts: self-defence, refused, repairing a rival, joint, restrained, fighting the room's own plan, copied, taking over, one script to stop members working against each other.
- The moderator as organiser, obstacle, gatekeeper, prankster, enforcer, funnel, hacked account, or elected chief.
- A large room with a large mark, against a large room whose mark stayed small.
- Restraint named as the room's rule, against expansion; restraint for maintainability (unturned).
- The late-room kinds listed above.
- The canvas fields linking the room's work, a neighbour's, a covered or lost work, or a work the room never names.

## The last rooms read

Block 17, in reading order: detroitlions, portugal, Villanova, russia, FinalFantasy, pathofexile, adventuretime, araragi, HomestarRunner, sips, bdsm, purplecorner, spain, cavestory, placestart, geometrydash, guatemala, GabrielDropout, starryknights, ibo, rwby, wholesomememes, kirby, tf2, wario, twentyonepilots, brasil, purdue, montenegro, GreenCorner, unturned, Thegreatblackhole, cowchop, edboxes, turkey.

## Ledgers at this close

- `lexicon-A1.md`: 1,207 lines. `running-A1.md`: 507 lines. `leads-A1.jsonl`: 2,332 lines. Every lead's `other` is in `order-A1.txt`, letter case aside; this was checked at this close with grep, sort and comm.
- Corrections this leg:
  - geometrydash's "noted" line was logged before the hook passed; the note was trimmed and a correction line logged.
  - placestart's paired-check line overstated agreement; a correction line was logged.
  - spain's ended turn was changed to c0066.
  - The HomestarRunner struck-by line lost stray backslashes.
  - The twentyonepilots lexicon line "the clique" was the coder's label; a superseding line gives the item's words.
  - The edboxes struck-by line was corrected to the item's exact words before logging.
- Rule, kept:
  - Fetch every id with `cite.py`. Check every lead's room with grep against the frame. Append through a grep filter on the item id. Never type an id from memory.
  - Copy lexicon words from the item text, never from the coder's labels; check with `cite.py` before appending.
  - Check struck-by lines against `cite.py` before writing.
  - A room with one or two concepts repeats an id on the carrying line (nonbinary, yerbamate, oltp, austriahungary, wario).
- The hook rejects notes of 350 words or more by its own count, which runs about 4 to 12 words above `wc -w`; keep `wc -w` at 340 or below. Draft the `doing` line at about 120 words. Log "noted" only after the hook passes.
- The permission check refuses "=w=", for and while loops, shell functions, some heredoc forms and awk. The command guard reads a bare "rm" inside quoted text as a delete. Use grep, cut, tr and plain echo appends.
- `read_room.sh` concept lines: use `cut -c1-20,38-150` and grep themes with "  tNN  ". For rooms over about 400 concepts, read by theme in two calls; one call over 30 KB is saved to a file the sandbox will not let me read.
- `mem.py diary --last 5` returns lines from an older file; read the current leg's diary with `mem.py diary --grep <room>`.

## The next comparison

Block 18 holds 35 rooms, beginning with r/2007scape. For every room, ask:
- Did the artwork exist before the room's first call, and who built it?
- Do the canvas fields link the work the room describes, and where?
- Does the canvas keep a work the room called lost, or link one it never names?
- Was the deal struck in the thread, in Discord or in a second sub, and did both sides' participants keep it?
- Did the room's own members or tools work against its plan?
- Which side of the onset contrast is the room on, and is it a sub made for the canvas?

When later blocks bring rooms named in leads, read the lead lines first. These include:
- block 18: prequelmemes, notredame, Northwestern, RelientK, europe, catalunya, aromantic, AcePlace, uofm, forsen, 2007scape, Goodboye, lakers, borussiadortmund, parabola, marvel;
- block 19: rpi, rotmg, ainbowroad, dota2, predators.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
