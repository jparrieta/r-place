# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-15, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-15 read blocks 01 to 15 whole (53, 48, 62, 44, 34, 37, 36, 30, 52, 50, 21, 35, 1, 32 and 37 rooms). 571 of 705 rooms have a note in `out/rooms/`. 134 rooms remain, in blocks 16 to 19 (46, 35, 35 and 18 rooms). The next leg is A1b-16. At this close `mem.py next` names r/mylittlepony, the first room of block 16. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count.

`validate.py A1` at this close: 0 errors, 0 warnings. 571 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh defect, not yet filed: linked artworks with region placements before hour 0. Fourteen cases: r/FloydVsVoid h-14.47, r/ProfessorLayton h-13.49, r/SwissNeutralityZone h-14.52 (shared with r/switzerland), r/monalisaclan h-15.23, r/radiohead h-11.54, r/aoe2 h-0.66, r/thebluecorner h-12.34, r/globaloffensive h-13.62, r/GrowTheTree h-0.24, r/nin h-11.52, r/npr h-11.19, r/starcitizen h-0.24, r/rainbowgrid h-12.27, r/AmericanFlaginPlace h-15.92 (USA / Canvas Center) and h-14.51 (E pluribus unum). The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it.

## The principal investigator's answer QA1-001

The concept-reach threshold stays at 0 items. No substitute measure is to be invented. Every room is read at concept level in the later model-building stages, and unplaced concepts are read at the end too. `notes-A1.md` says that the measure gives no cut in this store.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- concept_reach_threshold: 0 items, kept by QA1-001.
- `n_off_platform`: median 4, max 88 (dankmemes: its canvas concepts name one Discord).
- `px_window_share`: median 0.111, max 0.547; null for tenma.
- Concentration is null in 3 rooms (nonbinary, oltp, wario). oltp was read this leg: one coded turn by a deleted author.
- 79 rooms have their last coded turn before hour 73.

## The onset contrast

`out/contrast.md`. Early: first coded turn after hour 0 and before hour 3, 131 rooms. Late: first coded turn after hour 48, 61 rooms. The confound is size (median items 5067 against 33). A held-size comparison (items 156 to 2770, 41 against 12) travels with it. Expectation: late rooms organize around finding space on a full canvas; early rooms around claiming and holding it.

Block 15 early rooms, five: r/thenetherlands, r/zootopia, r/eagles, r/nintendo, r/starlightstage. All held their works to the end. thenetherlands planned in r/cirkeltrek and Discord; zootopia kept its work by a bot.

Block 15 late rooms, four:
- r/rainbowgrid is a new shape. The sub formed at h64 around a pattern already on the canvas, placed from h-12.27.
- r/mysterydungeon is ask and move. It built its own gear in under three hours.
- r/CSUFoCo (first coded turn h57.46) is nearest ask and move. A member showed a small logo already made, then asked for a Colorado colleges area worked out with CU Boulder. The linked region sits in the centre ring, placed from h1.05. The room put its logo on the far right side.
- r/tetris (h71.31) fits the sixth kind, one member alone. Its calls came minutes before and after the close, and one member placed pieces beside the rubik's cube. The linked region was placed from h2.57, writers 0.055.

The kinds so far:
- ask and move: COSI, UPenn, sheffield, corridor, MiamiHurricanes, mysterydungeon, CSUFoCo;
- take, refuse once, shuffle: Cornwall;
- arrive to defend work others built: cgpgrey;
- take by script over objections: udub;
- talk about a site and find the mark already there: sakartvelo, UNLincoln, vietnam;
- one member alone finds a spot: CelticFc, azerbaijan, tetris;
- possibly a seventh, a sub formed late around a pattern already there: rainbowgrid.

In every late room so far, the linked work was placed from the first hours. No size test yet.

## The three sentences written before reading, against fifteen blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke. Block 15: r/starbound's linked regions were placed from h1.7, while its first call came at h27.7. r/TeamDignitas found someone already making its logo under the Lattice at h8.8. r/CSUFoCo and r/tetris, as above. r/uiowa's first call was h33.8 and r/tinytardis's first post h35.0, both on regions placed from the first hours. Twice the canvas links a region far from where the room built: r/asexual (a heart at 545, 727 against its banner near 150, 600) and r/CSUFoCo.
2. Coordinating turns end mostly between hours 68 and 73. Block 15: most rooms end h70 to h72.9. Earlier ends: r/oltp h12.31 (one turn), r/twitch h46.15, r/nyjets h58.62, r/futanari h59.08, r/uiowa h64.10, r/rainbowgrid h68.38, r/kuwait h69.16. r/tetris and r/criticalrole have coordinating turns just after h73.
3. Fights are with neighbours, and rivals often become partners or hosts. Block 15: r/Slovakia's flag was kept by a Norwegian vote to rebuild it, on terms it accepted (c0047, c0048). In r/taiwan, one of r/morocco's own members cancelled its raid (c0066), and sabotage calls turned into help (c0075). r/pitt kept a mutual let-alone with Penn State (c0091). r/zootopia yielded its spot to r/indieheads, calling it "intersub diplomacy".
4. Deals often do not bind the crowd. Block 15: r/transformers' member accepted a deal without speaking for everyone (c0075). r/taiwan's own scripts fought its own TW#1 text (c0062). r/criticalrole fought itself over two template links (c0056).
5. The goal is often set by one member: r/futanari's place thing, r/tetris's pieces, r/raocow's Demo (top author 0.485), r/mizzou's MIZ (top author 0.364).
6. April Fools makeovers filled early turns in many block 15 rooms (OnePiece as Foxy's place, zootopia as r/kubo, taiwan's Thaiwan).
7. Moderators: r/nintendo's funnelled calls into one megathread; r/pitt's removed a Penn State attack post.
8. The canvas fields link works the room did not make, barely placed or mourned as lost: r/raocow's Demo (the room said Sweden obliterated it; writers 0.022), r/futanari's "Original Location" (writers 0.001), r/asexual's heart (writers 0.003), r/oltp's Oceanic League work, r/mizzou's "The Great Kansas Massacre".

Seen three or more times and logged, blocks 10 to 15:
- Green Lattice as host and border authority. Many rooms; block 15: starbound (refuses newcomers c0063; latticed over the flag to defend it c0074), OnePiece (refused Luffy a spot, then allied), TeamDignitas, raocow, zootopia.
- The Blue Corner as a host that rooms ask or ally with. Block 15: TeamDignitas surrounded its logo in blue so the blue corner would ignore it (c0025); starbound got leave (c0067); pitt's first logo sat in the Blue Corner. Its own sub r/orderofthebluecorner refused every non-blue request.
- r/placestart governing others' space: liquicity, hatsune, cgpgrey, clubpenguin, splatoon, starcraft, transformers.
- A room that covered or wrecked a work helps rebuild it: animalcrossing, puzzleanddragons, liquicity, croatia, runescape, smashbros, rust; block 15: r/penguins with pitt.
- Deals struck by ambassadors that the sub's own participants break or do not know of (bakchodi, weezer, yugioh, TheHulk, undertale); a member disclaiming the room's voice in a deal (weezer, splatoon, canucks, rutgers, transformers).
- A room yields or holds because one side was there first: titanfall, danganronpa, malaysia, neu, clashroyale, starcraft.
- A room relocates or shrinks its work when a neighbour asks. Many rooms; block 15: zootopia, starbound, criticalrole, taiwan (the West wall for r/danganronpa), pitt.
- Members refuse to attack a rival's work or keep a mutual let-alone: anaheimducks, armenia, ucf, clashroyale; block 15: pitt, nyjets, palestine, switzerland, OnePiece.
- Restraint against greed named as such (new, block 15): criticalrole, funhaus, fireemblem, starbound, OnePiece.
- Bots held the work while organisers restrained the bots for neighbours: rust, archlinux, runescape, bitcoin. Scripts refused on principle: mindcrack, floridagators, aggies, pakistan, dragonquest. A room's own tools fighting its own plan (new, block 15): taiwan, criticalrole, AmericanFlaginPlace. Repair scripts copied between rooms: singapore from AmericanFlaginPlace.
- A Discord that controls who may edit: smashbros, fivenightsatfreddys, starcraft, argentina.
- The Dutch and r/placeNL as pressing neighbours with diplomats: Dominican, mindcrack, croatia, belgium; block 15: Slovakia (the Dutch offered a place), singapore ("Your flag is on Dutch ground").
- A national sub sends canvas work to a second sub or Discord: de, NovaScotia, newzealand, argentina, finland and suomi; block 15: switzerland (r/SwissNeutralityZone), thenetherlands (r/cirkeltrek), asexual (r/AcePlace).
- Large rooms whose canvas calls were scattered and whose mark came from a Discord group: dankmemes, leagueoflegends, DestinyTheGame, clashroyale, eve; block 15: twitch, nintendo, starbound.
- The canvas keeping a work the room called lost (new, block 15): raocow, futanari, CSUFoCo.

Paired lead checks for block 15 are in the diary, one line per room. Most leads agree on both sides. Where they agree only in part, the missing half is a deal or request absent from one room's concepts.

## Contrary rooms

Blocks 01 to 13: see `notes-A1.md` and earlier heads; kept here by name only.
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

Block 15:
- theblackvoid: no single command. Its Discord leaders, moderators and members gave rival orders and split into unofficial Discords.
- rainbowgrid: a sub formed at h64 around a pattern the crowd had been repeating; the pattern was placed from h-12.27.
- raocow: mourned Demo as obliterated by Sweden. The canvas links a Demo region placed from the first hours.
- Slovakia: its flag was kept by a Norwegian vote to rebuild it and by terms it accepted. Force did not keep it.
- taiwan: its own scripts fought its own TW#1 text. An attacker's member cancelled the attacker's raid.
- oltp: one coded turn, which asks oceanic players to keep up a sign built by others.
- asexual: the canvas links a heart the room never names, far from its banner.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 16 and after:
- Who started the work:
  - joining or finding work begun elsewhere, against starting it;
  - finding it only after the close;
  - a linked region placed from the first hours, against the room's late first call;
  - a linked region far from where the room built;
  - a work the room mourned as lost that the canvas keeps.
- Where organizing happened: in the thread, against in Discord or a second sub. A Discord that controls who may edit, against one that is a voluntary meeting place.
- Deals:
  - deals that bind a room, against deals its own participants or the other side's do not know or keep;
  - deals accepted by one member who disclaims the room's voice;
  - a flag kept by a stronger side's vote and terms, against a flag held by force.
- A treaty kept against the room's own wish, against one broken by its own rogues.
- A sub made for the canvas that:
  - governs others;
  - keeps a single work;
  - asks leave;
  - erases;
  - fades;
  - polices purity;
  - forms late around a pattern already there.
- A national flag run as a permission office, a watcher, a front line, or an alliance office.
- Scripts:
  - written in self-defence;
  - refused on principle;
  - that repair a rival;
  - joint scripts with a former rival;
  - bots restrained by their own organisers;
  - a room's own scripts or templates working against its own plan;
  - scripts copied between rooms.
- The moderator as organiser, obstacle, gatekeeper, prankster, enforcer, funnel, or hacked account.
- A large room with a large mark, against a large room whose mark came from a Discord group or stayed small.
- Restraint named as the room's rule (greed, neutrality, let-alone), against expansion.
- The late-room kinds listed above, including the sixth and a possible seventh.
- The canvas fields linking the room's work, a neighbour's, a covered or lost work, or a work the room never names.

## The last rooms read

Block 15, in reading order: theblackvoid, eagles, rainbowgrid, starlightstage, funhaus, fireemblem, FaroeIslands, nintendo, uiowa, mysterydungeon, CKCrusaders, tinytardis, berserk, twitch, kuwait, transformers, nyjets, thenetherlands, palestine, AmericanFlaginPlace, zootopia, CSUFoCo, tetris, asexual, oltp, switzerland, starbound, pitt, futanari, mizzou, Slovakia, raocow, singapore, TeamDignitas, taiwan, criticalrole, OnePiece.

## Ledgers at this close

- `lexicon-A1.md`: 1,010 lines. `running-A1.md`: 463 lines. `leads-A1.jsonl`: 1,984 lines. Every lead's `other` is in `order-A1.txt`, letter case aside; this was checked at this close with grep, sort and comm. Two leads from block 01 (liverpoolfc) carry item ids with a path suffix; they are older than this leg.
- Corrections appended this leg: three lexicon lines superseded (funhaus, nintendo, TeamDignitas; two used the coder's labels), rainbowgrid's early "noted" logged in the diary, and nyjets' ended line corrected to c0144.
- Rule, kept:
  - Fetch every id with `cite.py`. Check every lead's room with grep against the frame. Append through a grep filter on the item id. Never type an id from memory.
  - Copy lexicon words as written from the item text, never from the coder's labels.
  - Check struck-by lines against `cite.py` before writing.
  - A room with one concept carries that id three times (nonbinary, yerbamate, oltp).
- The hook rejects notes of 350 words or more by its own count, which runs up to about 20 words above `wc -w`. Keep `wc -w` at 340 or below. Drafts still run 355 to 385; draft the `doing` line at about 130 words.
- The permission check refuses "=w=", for loops, some heredoc forms and awk. The command guard reads a bare "rm" inside quoted text as a delete. Use grep, cut, tr and plain echo appends.

## The next comparison

Block 16 holds 46 rooms, beginning with r/mylittlepony, named in block 14's leads; read its lead lines first. For every room, ask:
- Did the artwork exist before the room's first call, and who built it?
- Do the canvas fields link the work the room describes, and where?
- Does the canvas keep a work the room called lost?
- Was the deal struck in the thread, in Discord or in a second sub, and did both sides' participants keep it?
- Did the room's own tools work against its plan?
- Which side of the onset contrast is the room on, and is it a sub made for the canvas?

When later blocks bring rooms named in leads, read the lead lines first. These include:
- from block 15: AcePlace, aromantic, catalunya, europe, ainbowroad, dota2, wallstreetbets, rwby, forsen, pathofexile, turkey;
- from earlier: quebec, scotland, livecounting, philippines, msu, cavestory, unturned, purdue, tf2, GabrielDropout, edboxes, placestart, 2007scape, lakers, borussiadortmund, snsd, parabola, marvel, clg.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
