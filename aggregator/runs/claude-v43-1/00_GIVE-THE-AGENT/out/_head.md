# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-16, 2026-10-07.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-16 read blocks 01 to 16 whole (53, 48, 62, 44, 34, 37, 36, 30, 52, 50, 21, 35, 1, 32, 37 and 46 rooms). 617 of 705 rooms have a note in `out/rooms/`. 88 rooms remain, in blocks 17 to 19 (35, 35 and 18 rooms). The next leg is A1b-17. At this close `mem.py next` names r/detroitlions, the first room of block 17. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count.

`validate.py A1` at this close: 0 errors, 0 warnings. 617 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short:
- r/tenma has no canvas line;
- r/archlinux has a coded turn at hour 100.9;
- `n_codes_coder` has two meanings;
- `items.jsonl` has an undocumented state `collapsed`;
- concept reach is 1.0 everywhere;
- r/yogscast's first coded turn is not about the canvas.

Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh defect, not yet filed: linked artworks with region placements before hour 0. Eighteen rooms now carry such a case:
- through block 14: FloydVsVoid, ProfessorLayton, SwissNeutralityZone (shared with switzerland), monalisaclan, radiohead, aoe2, thebluecorner, globaloffensive, GrowTheTree, nin, npr, starcitizen;
- block 15: rainbowgrid (h-12.27), AmericanFlaginPlace (h-15.92, h-14.51);
- block 16: trees (h-12.51), afip (American Flag Banner h-14.34, the same flag as AmericanFlaginPlace), PlaceNL (Entire Dutch Area and The Dutch Border, h-8.01), scotland (The Royal Banner of Scotland, h-12.94).

The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it. r/OrderOfTheKoi has no linked artwork; its region is "derived from the pixel record".

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

Block 16 early rooms, ten: pcmasterrace, streetfighter, oneplus, philippines, mylittlepony, paladins, stlouisblues, wallstreetbets, nlsscirclejerk, trees. Their first turns are mostly April Fools. Several turned to the canvas only a day later (streetfighter, oneplus, paladins). pcmasterrace's mark stayed small for a top-100 sub.

Block 16 late rooms, six:
- r/latin (h49.48): ask and move, on Green Lattice's terms.
- r/OrderOfTheKoi (h53.57) and r/VelvetUnderground (h58.64): arrived to defend work others built (the third kind).
- r/DevonUK (h54.10) and r/Produce101 (h70.94): one member, then friends (the sixth kind). Produce101 took a spot another group wanted.
- r/aeskwadraat (h69.13): designs only, and the stop came first. The canvas links a region the room never mentions; a variant of the fifth kind in which the mark is never found.

The kinds so far:
- ask and move: COSI, UPenn, sheffield, corridor, MiamiHurricanes, mysterydungeon, CSUFoCo, latin;
- take, refuse once, shuffle: Cornwall;
- arrive to defend work others built: cgpgrey, OrderOfTheKoi, VelvetUnderground;
- take by script over objections: udub;
- talk about a site and find the mark already there: sakartvelo, UNLincoln, vietnam; aeskwadraat (mark never found);
- one member alone or with friends: CelticFc, azerbaijan, tetris, DevonUK, Produce101;
- possibly a seventh, a sub formed late around a pattern already there: rainbowgrid.

In every late room so far, the linked work was placed from the first hours. No size test yet.

## The three sentences written before reading, against sixteen blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke. Block 16:
   - r/OneTrueEmilia found its sign at h57.1;
   - r/oneplus found its logo at h29.1;
   - r/nlsscirclejerk found an outline already made;
   - in r/Mario a couple built the toadstool from the start and told of it only after the close.

   The canvas often links a work the room never names or did not make: r/streetfighter (Brazil's Blanka), r/aeskwadraat, r/ultrahardcore (far from its planned heart), r/poland (a heart, not its flag), r/sbu (writers 0.004).
2. Coordinating turns end mostly between hours 68 and 73. Block 16's earlier ends:
   - r/thetreesnetwork h17.61;
   - r/austriahungary h43.08;
   - r/hoodr h53.33;
   - r/latin h57.92;
   - r/shrooms h54.59;
   - r/gamindustri h64.05;
   - r/livecounting h66.07.
3. Fights are with neighbours, and rivals often become partners or hosts. Block 16:
   - r/philippines lost its spot to r/osugame, then signed a treaty to move and called it "a truce not an alliance";
   - r/PlaceNL ran a restitution office for groups it had overrun ("the Poldermodel at work");
   - r/quebec moved after talks with Canada;
   - r/scotland settled a border with r/israel instead of attrition.
4. Deals often do not bind the crowd. Block 16:
   - r/PlaceNL said its organised members could not control the Dutch masses (c0097, c0168);
   - r/stlouisblues found its own and allies' fans the hardest to stop (c0118);
   - r/poland disowned attacks on AMD as randoms (c0079);
   - a room's own scripts fought each other: r/mylittlepony, r/wallstreetbets, r/quebec.
5. The goal is often set by one member: r/hoodr (top author 0.469), r/sbu's script (about 20 runners), r/DevonUK, r/Produce101, r/Mario's couple.
6. April Fools makeovers filled the first day of most early rooms: pcmasterrace's Comic Sans, paragon's Iggy, oneplus's Dash Energy, starvstheforcesofevil's redesign, trees, paladins.
7. Moderators: r/mylittlepony's and r/scotland's moderators funnelled canvas posts into one thread; r/quebec elected a chief by vote (c0058).
8. The canvas fields link works the room did not make or barely placed: r/PinkUnion (20 coded authors, 60,303 placers, writers 0.003), r/sbu, r/streetfighter, r/aeskwadraat.

Seen three or more times and logged, blocks 10 to 16:
- Green Lattice as host, border authority and approval office. Block 16: gamindustri (Google Docs approval list), latin (no new applications), paladins (protection on terms, "a mafia"), esperanto (a whole flag refused as too big), mylittlepony, OnePiece.
- The Blue Corner as a host under truce: pcmasterrace moved in (c0715); stlouisblues made a formal request; TeamDignitas, starbound and pitt in block 15.
- r/placestart governing others' space: liquicity, hatsune, cgpgrey, clubpenguin, splatoon, starcraft, transformers; block 16: sbu (the start button), thetreesnetwork (the task bar).
- A room that covered or wrecked a work helps rebuild it: animalcrossing, liquicity, croatia, runescape, pitt's penguins; block 16: philippines (FNaF, the smiley), PlaceNL (restitution).
- Deals that the sub's own participants break or do not know of; members disclaiming the room's voice: bakchodi, weezer, undertale, transformers; block 16: PlaceNL, poland, stlouisblues.
- A room relocates or shrinks its work when a neighbour asks. Many rooms; block 16: portal, latin, muse, catalonia, gamindustri.
- Members refuse to attack a rival or keep a let-alone; restraint named as greed or fair share. Block 16: gratefuldead ("we don't fight here"), starvstheforcesofevil ("fair share"), catalonia ("we are not Germany"), msu (the all-Big Ten plan), portal.
- Bots and scripts:
  - held works while organisers restrained them: rust, archlinux;
  - refused on principle: mindcrack, floridagators;
  - a room's own bots or scripts fighting each other: taiwan, criticalrole, mylittlepony, wallstreetbets, quebec;
  - copied between rooms: singapore, livecounting, catalonia;
  - bots said to have taken over at the end: pcmasterrace (c0958).
- A Discord that controls who may edit, or a layer above rooms: smashbros, starcraft; block 16: sbu (a 2,000-member mods-only Discord), stlouisblues (a diplomat across 12 servers).
- The Dutch and r/placeNL as pressing neighbours with diplomats: Dominican, mindcrack, croatia, belgium, Slovakia, singapore; block 16: PlaceNL itself.
- A national sub sends canvas work to a second sub or Discord: switzerland, thenetherlands, asexual, poland (r/Polska as headquarters).
- Living on an ally's land by permission (new): swordartonline, miraculousladybug, yuyuyu.
- The canvas keeping a work the room called lost: raocow, futanari, CSUFoCo.

Paired lead checks for block 16 are in the diary, one line per room. Most leads agree on both sides. Where they agree only in part, the missing half is a deal or request absent from one room's concepts. One partial disagreement: r/runescape says it refused to help r/msu; r/msu's record shows r/runescape offering help (c0048). Both may be true of different members.

## Contrary rooms

Blocks 01 to 14: see `notes-A1.md` and earlier heads; kept here by name only.
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

Block 16:
- PlaceNL: a conquering sub that ran an application office to give space back, and said it could not control its own masses.
- pcmasterrace: a top-100 sub whose logo stayed small; members say bots took over at the end.
- PinkUnion: a colour faction of 20 coded authors claiming a region placed by 60,303 people.
- streetfighter: its own Ryu never stood; the canvas links Brazil's Blanka, which it thanked.
- aeskwadraat: designs only; the canvas links a work it never mentions.
- Mario: no shared goal; a couple built the toadstool from the start and said so only after the close.
- wallstreetbets: open botting set the terms for its neighbours ("our bots would fight eachother all day").

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 17 and after:
- Who started the work:
  - joining or finding work begun elsewhere, against starting it;
  - a linked region placed from the first hours, against the room's late first call;
  - a linked region far from where the room built, or never named;
  - a work the room mourned as lost that the canvas keeps.
- Where organizing happened: in the thread, against in Discord, Telegram, teamspeak or a second sub; a Discord that controls who may edit, against a voluntary meeting place; layers above rooms (mods-only Discords, World Congress).
- Deals:
  - deals that bind a room, against deals its own participants do not keep;
  - a truce against an alliance;
  - living on an ally's land by permission;
  - restitution after conquest.
- A sub made for the canvas that governs others, keeps a single work, asks leave, erases, fades, polices purity, forms late around a pattern, spreads and gives its work away (AvoArmy), or claims a colour (PinkUnion).
- A national flag run as a permission office, a watcher, a front line, an alliance office, or a restitution office.
- Scripts: self-defence, refused, repairing a rival, joint, restrained, fighting the room's own plan, copied, taking over.
- The moderator as organiser, obstacle, gatekeeper, prankster, enforcer, funnel, hacked account, or elected chief.
- A large room with a large mark, against a large room whose mark stayed small (pcmasterrace, twitch).
- Restraint named as the room's rule, against expansion.
- The late-room kinds listed above.
- The canvas fields linking the room's work, a neighbour's, a covered or lost work, or a work the room never names.

## The last rooms read

Block 16, in reading order: mylittlepony, gamindustri, Mario, latin, paladins, sbu, quebec, poland, msu, stlouisblues, shrooms, ultrahardcore, portal, hoodr, trees, nlsscirclejerk, OneTrueEmilia, philippines, afip, livecounting, yuyuyu, paragon, AvoArmy, miraculousladybug, DevonUK, catalonia, muse, Produce101, starvstheforcesofevil, re_zero, VelvetUnderground, esperanto, wallstreetbets, calvinandhobbes, pcmasterrace, aeskwadraat, swordartonline, streetfighter, oneplus, OrderOfTheKoi, PlaceNL, PinkUnion, scotland, austriahungary, gratefuldead, thetreesnetwork.

## Ledgers at this close

- `lexicon-A1.md`: 1,117 lines. `running-A1.md`: 480 lines. `leads-A1.jsonl`: 2,174 lines. Every lead's `other` is in `order-A1.txt`, letter case aside; this was checked at this close with grep, sort and comm. Two leads from block 01 (liverpoolfc) carry item ids with a path suffix.
- Corrections this leg: the OrderOfTheKoi struck-by line was corrected to the item's exact words before logging; the swordartonline coordinates were completed; r/Mario's note was softened where the room does not place the toadstool.
- Rule, kept:
  - Fetch every id with `cite.py`. Check every lead's room with grep against the frame. Append through a grep filter on the item id. Never type an id from memory.
  - Copy lexicon words as written from the item text, never from the coder's labels.
  - Check struck-by lines against `cite.py` before writing.
  - A room with one or two concepts repeats an id on the carrying line (nonbinary, yerbamate, oltp, austriahungary).
- The hook rejects notes of 350 words or more by its own count, which runs up to about 20 words above `wc -w`; keep `wc -w` at 340 or below. Drafts still run 350 to 410; draft the `doing` line at about 120 words.
- The permission check refuses "=w=", for loops, some heredoc forms and awk. The command guard reads a bare "rm" inside quoted text as a delete. Use grep, cut, tr and plain echo appends.
- `read_room.sh` concept lines differ by page: use `cut -c1-20,38-150` and grep themes with "  tNN  ".

## The next comparison

Block 17 holds 35 rooms, beginning with r/detroitlions. For every room, ask:
- Did the artwork exist before the room's first call, and who built it?
- Do the canvas fields link the work the room describes, and where?
- Does the canvas keep a work the room called lost, or link one it never names?
- Was the deal struck in the thread, in Discord or in a second sub, and did both sides' participants keep it?
- Did the room's own tools work against its plan?
- Which side of the onset contrast is the room on, and is it a sub made for the canvas?

When later blocks bring rooms named in leads, read the lead lines first. These include:
- from blocks 15 and 16: catalunya, aromantic, AcePlace, europe, prequelmemes, rwby, uofm, unturned, forsen, pathofexile, 2007scape, snsd, brasil, placestart, Goodboye, dota2, ainbowroad;
- from earlier: purdue, tf2, GabrielDropout, edboxes, lakers, borussiadortmund, parabola, marvel, clg, turkey.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
