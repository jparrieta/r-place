# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-18, 2026-10-07.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-18 read blocks 01 to 18 whole (53, 48, 62, 44, 34, 37, 36, 30, 52, 50, 21, 35, 1, 32, 37, 46, 35 and 35 rooms). 687 of 705 rooms have a note in `out/rooms/`. 18 rooms remain, all in block 19. The next leg is A1b-19. At this close `mem.py next` names r/ainbowroad, the first room of block 19. Always take the next room from `mem.py next`, never from this file.

Block 19 is the last block. In its leg, before the close, write `coordinating-rule-A1.md` and `organizing_end-A1.jsonl` (stage file §5): the rule with ten concept ids on each side in the lexicon's words, then one line per room of the analysed set, all 705, under that rule and from the forest, with each note's `ended` line reconciled and every disagreement logged. That is a large piece of work; begin it as soon as the last note is logged.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count.

`validate.py A1` at this close: 0 errors, 0 warnings. 687 notes over 705.

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
- r/yogscast's first coded turn is not about the canvas (h-18.58, streaming keys; first canvas call h5.03, confirmed this leg).

Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh defect, not yet filed: linked artworks with region placements before hour 0. Twenty-one rooms now carry such a case:
- through block 14: FloydVsVoid, ProfessorLayton, SwissNeutralityZone (shared with switzerland), monalisaclan, radiohead, aoe2, thebluecorner, globaloffensive, GrowTheTree, nin, npr, starcitizen;
- block 15: rainbowgrid, AmericanFlaginPlace;
- block 16: trees, afip, PlaceNL, scotland;
- block 17: Thegreatblackhole (The First Void, h-14.52);
- block 18: 2007scape (RuneScape disconnected message, h-15.07), androidgaming (h-0.64).

The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it; decide at A1c.

## The principal investigator's answer QA1-001

The concept-reach threshold stays at 0 items. No substitute measure is to be invented. Every room is read at concept level in the later model-building stages, and unplaced concepts are read at the end too. `notes-A1.md` says that the measure gives no cut in this store.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- concept_reach_threshold: 0 items, kept by QA1-001.
- `n_off_platform`: median 4, max 88 (dankmemes: its canvas concepts name one Discord).
- `px_window_share`: median 0.111, max 0.547; null for tenma.
- Concentration is null in 3 rooms (nonbinary, oltp, wario).
- 79 rooms have their last coded turn before hour 73.

## The onset contrast

`out/contrast.md`. Early: first coded turn after hour 0 and before hour 3, 131 rooms. Late: first coded turn after hour 48, 61 rooms. The confound is size (median items 5067 against 33). A held-size comparison (items 156 to 2770, 41 against 12) travels with it. Expectation: late rooms organize around finding space on a full canvas; early rooms around claiming and holding it.

Block 18 early rooms: 2007scape (758 coded authors), prequelmemes (467), europe (443), uofm, lakers, ElderScrolls (its first turn an April Fools restyle). The large ones built in several places at once before settling (2007scape's many memes, europe's four flags) and named restraint as a rule (prequelmemes made attacks a standing no-go).

Block 18 late rooms, three:
- r/bigbang (h62.85): three members one after another (the sixth kind); the canvas links a 30-px text placed from h4.11 by others that the room never reports finding.
- r/TheID (h61.31): one member calling a Rainbow Road spot ours (the fifth kind, find the mark already there).
- r/parabola (h52.91): arrived with its word already on the canvas, then moved it by request and made border deals (near the third kind).

The kinds so far:
- ask and move: COSI, UPenn, sheffield, corridor, MiamiHurricanes, mysterydungeon, CSUFoCo, latin, guatemala;
- take, refuse once, shuffle: Cornwall;
- arrive to defend work others built: cgpgrey, OrderOfTheKoi, VelvetUnderground, ibo; near it, parabola;
- take by script over objections: udub;
- talk about a site and find the mark already there: sakartvelo, UNLincoln, vietnam, TheID; aeskwadraat and bigbang (mark never found);
- one member alone or with friends: CelticFc, azerbaijan, tetris, DevonUK, Produce101, Villanova, bigbang;
- possibly a seventh, a sub formed late around a pattern already there: rainbowgrid.

In every late room so far, the linked work was placed from the first hours. No size test yet.

## The three sentences written before reading, against eighteen blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke. Block 18: the linked region predates the room's first call in Goodboye (h39.6), denverbroncos (canvas work from h48.1), catalunya, aromantic, pusheen, apocalypserising, neutralmilkhotel; borussiadortmund built its crest from a BVB 09 already on the canvas; blackmirror began in a black void others made. The canvas links works the room credits to another sub: Okami (THE_PACK's wolf), ElderScrolls (r/truestl's Vivec), marvel (Wolverine, Hydra by the marvelstudios Discord), neutralmilkhotel (shared with indieheads).
2. Coordinating turns end mostly between hours 68 and 73. Block 18's earlier ends: aromantic h47.08, Summit1G h57.14, ElderScrolls h59.81, TheID h61.48, blackmirror h61.87, RelientK h62.47, planetside h62.94, daftpunk h65.40, lithuania h66.48.
3. Fights are with neighbours, and rivals often become partners. Block 18:
   - uofm repaired Ohio State's O and spent spare pixels on it;
   - crusaderkings made its crown with r/norge after a day of dispute;
   - 2007scape called r/runescape allies and brothers in arms;
   - Goodboye met a Dutch demand by giving a dog clogs;
   - Summit1G was moved by Canada, who helped rebuild it.
4. Deals often do not bind the crowd. Block 18: catalunya's Factorio deal denied as talk with one guy (c0039); crusaderkings told other Discords not to decide for an artwork it started (c0051); 2007scape's unorganised members bulldozed neighbours while others apologised (c0503, c0646); uofm's OSU partners blamed casuals (c0181).
5. Leaders outside the thread: streamers led or raided (destiny's work stopped when the streamer stopped, c0090 c0092; forsen recruited on streams; 82 of Summit1G's 140 coded turns are a raiding chat's chant). One organiser carried several small rooms (RelientK top author 0.515, parrots 0.365, TheID 1.0).
6. April Fools filled the first day of most early rooms: 2007scape, europe (no English), ElderScrolls, lakers, borussiadortmund (a Red Bull takeover).
7. Moderators funnelled canvas posts into one thread or a second sub: europe (r/EuropePlace), borussiadortmund, daftpunk, Okami's moderator ruled on expansion.
8. Scripts: refused for a script-free work (prequelmemes c0439); a remote template (uofm c0183); a neighbour's bots offered to rebuild what its old scripts overran (RelientK c0026, c0032).

Seen three or more times and logged, blocks 10 to 18:
- Green Lattice and Rainbow Road as host, permit office and border authority. Block 18: daftpunk (building permit, figures moved by Green Lattice), planetside (application area closed), blackmirror and TheID (Rainbow Road feared or used).
- The Blue Corner as unworkable host or invader: europe gave up on it; notredame's first site morphed by it; yogscast's second head lost there.
- r/placestart pressing neighbours: borussiadortmund (gray lines), with r/uofu negotiating.
- A room that wrecked a work helps rebuild it, or repays those who moved: 2007scape (PuzzleAndDragons, N7), uofm (Ohio State's O).
- A representative who cannot bind the crowd: catalunya, crusaderkings, apocalypserising, uofm, Summit1G (a Chatot member disowned).
- A room relocates or trims its work when a neighbour asks: Northwestern, stardewvalley, RelientK, yogscast (the Texas shimmy), parabola.
- Restraint named as the room's rule: prequelmemes, yogscast, Goodboye, notredame, stardewvalley, parrots, europe; before: cavestory, wholesomememes, tf2, purdue, unturned, rwby.
- A work made by another sub celebrated by the room: Okami, ElderScrolls, marvel, neutralmilkhotel; before: araragi, HomestarRunner, bdsm, starryknights.
- A second sub or Discord taking the canvas work: europe, crusaderkings (r/CKCrusaders), uofm (r/theB1G), denverbroncos (r/ManningPlace), lithuania (a Baltic Discord of 125).
- A national room spending its pixels on neighbours: lithuania (Latvia, Belarus, Estonia).
- Colour factions as hosts: parrots joined PurplePixels' alliance.

Paired lead checks for block 18 are in the diary, one line per room. Most leads agree on both sides. Where they agree only in part, the missing half is a deal or request absent from one room's coded concepts, mostly in large rooms with many threads out of scope (2007scape 2,466, prequelmemes 1,508, europe 982).

## Contrary rooms

Blocks 01 to 16: see `notes-A1.md` and earlier heads; kept here by name only.
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
- Block 17: placestart, starryknights, tf2, brasil, wholesomememes, Thegreatblackhole, GreenCorner, ibo, wario.

Block 18:
- destiny: a room whose work followed one streamer on stream and stopped when he did.
- Summit1G: most of its coded turns are a raiding rival chat's chant.
- Okami: celebrated a wolf another sub made, and forbade expansion through that sub's logo.
- 2007scape: no single goal; members bulldozed neighbours while others rebuilt them.
- lithuania: a nation that spent its pixels on neighbours' flags.
- stardewvalley: a popular sub that chose small figures over a logo.
- planetside: a small room refused by Green Lattice's closed application area; the canvas names its work an attempted invasion.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to carry into A1c and B1:
- Who started the work: joining or finding work begun elsewhere, against starting it; a linked region placed from the first hours, against the room's late first call; a work the room credits to another sub; a work the room mourned as lost that the canvas keeps.
- Where organizing happened: in the thread, against in Discord, a second sub, a forum, or a stream; a Discord that decides for the room, against a meeting place.
- Deals: binding, against not kept; truce against alliance; living on an ally's land by permission; repair after taking space.
- A sub made for the canvas that governs others, keeps a single work, asks leave, polices purity, migrates, forms late around a pattern, or claims a colour.
- A national flag run as a permission office, a front line, an alliance office, a restitution office, a joint work with a rival, or a helper of neighbours' flags.
- Scripts: self-defence, refused, repairing a rival, joint, restrained, fighting the room's own plan, copied, offered by a neighbour, running past their owners.
- The moderator as organiser, obstacle, gatekeeper, funnel, enforcer, or elected chief.
- A leader outside the room: a streamer, a chat, a single organiser.
- Restraint named as the room's rule, against expansion.
- The late-room kinds listed above.

## The last rooms read

Block 18, in reading order: 2007scape, prequelmemes, yogscast, Goodboye, denverbroncos, lakers, bigbang, destiny, planetside, marvel, androidgaming, forsen, catalunya, Okami, notredame, TheID, ElderScrolls, Northwestern, parabola, uofm, borussiadortmund, apocalypserising, crusaderkings, aromantic, pusheen, blackmirror, Summit1G, AcePlace, daftpunk, lithuania, neutralmilkhotel, stardewvalley, parrots, europe, RelientK.

## Ledgers at this close

- `lexicon-A1.md`: 1,261 lines. `running-A1.md`: 522 lines. `leads-A1.jsonl`: 2,429 lines. Every lead's `other` is in `order-A1.txt`, letter case aside; this was checked at this close with grep, sort and comm.
- Corrections this leg:
  - r/apocalypserising's noted line was logged in the same call that wrote the note, before the hook reported 353 words; the note was trimmed and a correction line logged.
  - The lakers lexicon line "Celtics sand castle" capitalised a word the item writes in lower case; a superseding line gives the exact words.
  - androidgaming's coder-unsure line was corrected to the first call's deleted body.
- Rule, kept:
  - Fetch every id with `cite.py`. Check every lead's room with grep against the frame. Append through a grep filter on the item id. Never type an id from memory.
  - Copy lexicon words from the item text, never from the coder's labels; check case and spelling with `cite.py` before appending.
  - Check struck-by lines against `cite.py` before writing.
  - Never log "noted" in the same call that writes the note; wait for the hook's answer.
  - A room with one or two concepts repeats an id on the carrying line.
- The hook rejects notes of 350 words or more by its own count, which runs 4 to 13 words above `wc -w`; keep `wc -w` at 340 or below.
- The permission check refuses "=w=", for and while loops, shell functions, some heredoc forms and awk. The command guard reads a bare "rm" inside quoted text as a delete. Use grep, cut, tr and plain echo appends.
- `read_room.sh` concept lines: use `cut -c1-20,38-110` for large rooms and grep themes with "  tNN  "; a call over 30 KB is saved to a file the sandbox will not let me read. Write large theme reads to `$TMPDIR` and page them with head and grep.
- `mem.py diary --last 5` returns lines from an older file; read the current leg's diary with `mem.py diary --grep <room>`.

## The next comparison

Block 19 holds 18 rooms, beginning with r/ainbowroad: ainbowroad, dota2, Braveryjerk, WisconsinBadgers, FederationPlace, seventeen, rpi, traaaaaaannnnnnnnnns, rotmg, dofus, snsd, clg, reddevils, gameboy, fxKorea, winnipegjets, Russiaclan, predators. Many leads point at r/ainbowroad, dota2, rpi, rotmg and predators; read the lead lines first.

For every room, ask:
- Did the artwork exist before the room's first call, and who built it?
- Do the canvas fields link the work the room describes, and where?
- Was the deal struck in the thread, in Discord or in a second sub, and did both sides' participants keep it?
- Did the room's own members or tools work against its plan?
- Which side of the onset contrast is the room on, and is it a sub made for the canvas?

Then write the coordinating-turn rule and the organizing-end file for all 705 rooms before the close.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
