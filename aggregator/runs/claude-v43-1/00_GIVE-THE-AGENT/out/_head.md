# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-14, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-14 read blocks 01 to 14 whole (53, 48, 62, 44, 34, 37, 36, 30, 52, 50, 21, 35, 1 and 32 rooms). 534 of 705 rooms have a note in `out/rooms/`. 171 rooms remain, in blocks 15 to 19 (37, 46, 35, 35 and 18 rooms). The next leg is A1b-15. At this close `mem.py next` names r/theblackvoid, the first room of block 15. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count.

`validate.py A1` at this close: 0 errors, 0 warnings. 534 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh defect, not yet filed: linked artworks with region placements before hour 0. Twelve cases: r/FloydVsVoid h-14.47, r/ProfessorLayton h-13.49, r/SwissNeutralityZone h-14.52, r/monalisaclan h-15.23, r/radiohead h-11.54, r/aoe2 h-0.66, r/thebluecorner h-12.34, r/globaloffensive h-13.62, r/GrowTheTree h-0.24, r/nin h-11.52, r/npr h-11.19, r/starcitizen h-0.24. r/leagueoflegends and r/orderofthebluecorner link works already counted. Block 14 added none. The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it.

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

Block 14 early rooms, nine: r/bitcoin, r/splatoon, r/kingdomhearts, r/undertale, r/smashbros, r/fivenightsatfreddys, r/kanye, r/runescape, r/floridagators. As before the first turns are mostly April Fools. Most of these held large or multiple works by Discord, scripts, or both; r/kanye grew one work to 11,680 px and hosted neighbours.

Block 14 late rooms, two: r/vietnam (first coded turn h49.47) fits the fifth kind: it talked about a flag, eight members wrote, one said not to bother, and at h69.3 a member found a heart-shaped flag placed from h2.8. r/azerbaijan (h72.60) fits the possible sixth kind first seen in r/CelticFc: a visitor from r/turkey called in the last half hour and one member drew a small flag alone. The kinds so far: ask and move (COSI, UPenn, sheffield, corridor, MiamiHurricanes); take, refuse once, shuffle (Cornwall); arrive to defend work others built (cgpgrey); take by script over objections (udub); talk about a site and find the mark already there (sakartvelo, UNLincoln, vietnam); one member alone finds a spot (CelticFc, azerbaijan). In every late room so far the linked work was placed from the first hours. No size test yet.

## The three sentences written before reading, against fourteen blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke. Block 14: r/cuboulder found its logo there at h53.3 ("don't we already have one?"), r/polandball asked who planned its polandball, r/vietnam found a heart flag, r/shishamo, r/onepunchman and r/armok's linked regions predate their first calls by a day or more. Twice the canvas links a region far from where the room built (r/ubreddit at 114, 226 against its brick at 845, 189; r/paranatural's 15 px Eightfold the room called dead).
2. Coordinating turns end mostly between hours 68 and 73. Block 14: most rooms end h70 to h72.9. Earlier ends: r/nerf h50.28, r/rust h60.26, r/canucks h59.01, r/paranatural h57.10, r/polandball h58.08, r/archlinux h63.05, r/satania h64.74.
3. Fights are with neighbours, and rivals often become partners or hosts. Block 14: r/croatia took a Dutch flag and then twice helped r/TheHulk relocate and rebuild; r/rutgers gave its first spot to Purdue and later traded protection with it; r/starcraft and Chelsea agreed after a refusal; r/runescape and r/2007scape allied and then fought.
4. Deals often do not bind the crowd. Block 14: r/TheHulk said some Croatians would not honour the agreement (c0086); r/undertale said its r/lost treaty was not honoured (c0032); members disclaimed speaking for the room in r/splatoon (c0093), r/canucks (c0107) and r/rutgers (c0147).
5. The goal is often set by one member: r/satania's sign, r/paranatural's post, r/azerbaijan's flag, r/kanye's Wave at h1.9.
6. April Fools makeovers filled early turns in most block 14 rooms (kingdomhearts as Final Fantasy, smashbros as Amazing Crash Family, polandball's paragraph day, runescape's Get Pizza).
7. Moderators: r/polandball's switch ran 27 hours; r/PUBATTLEGROUNDS lost a moderator account to a hack; r/clashroyale-style moderator diplomacy recurs in r/splatoon ("only willing to talk to mods").
8. The canvas fields link works the room did not make or barely placed: r/vietnam (writers 0.009), r/paranatural (0), r/polandball (made by a small uncoordinated group), r/ubreddit (0.029).

Seen three or more times and logged, blocks 10 to 14:
- Green Lattice as host and border authority (many rooms; block 14: kingdomhearts, canucks, croatia, TheHulk, floridagators), and whose members sometimes disrupt work its Discord allowed (warframe, yugioh).
- The Blue Corner as host rooms ask or ally with (enterthegungeon, clashroyale, argentina; block 14: starcraft, smashbros, kingdomhearts, floridagators, PUBATTLEGROUNDS); its own sub r/orderofthebluecorner refused every non-blue request.
- r/placestart governing others' space (liquicity, hatsune, cgpgrey, clubpenguin; splatoon's orange squid, starcraft's overlap).
- A room that covered or wrecked a work helps rebuild it (animalcrossing, puzzleanddragons, liquicity; croatia with Hulk, runescape, smashbros, rust).
- Deals struck by ambassadors that the sub's own participants break or do not know of (twice, bakchodi, TsundereSharks, stevenuniverse, weezer, yugioh, TheHulk, undertale).
- A member accepting or rejecting a deal while disclaiming the room's voice (weezer, argentina, splatoon, canucks, rutgers).
- A room yields or holds because one side was there first (titanfall, danganronpa, malaysia, neu, clashroyale, starcraft).
- A room relocates or shrinks its work when a neighbour asks (many; block 14: croatia, TheHulk, undertale, lifeisstrange, mindcrack, kingdomhearts).
- Members refuse to attack a rival's work (anaheimducks, armenia, ucf, clashroyale).
- Bots held the work while organisers restrained the bots for neighbours (rust, archlinux, runescape, bitcoin); against scripts refused on principle (mindcrack, floridagators, aggies, pakistan, dragonquest).
- A Discord that controls who may edit (smashbros, fivenightsatfreddys, starcraft; argentina's foreign-policy group earlier).
- The Dutch and r/placeNL as pressing neighbours with diplomats (Dominican, mindcrack, croatia, belgium).
- A national sub sends canvas work to a second sub or Discord (de, NovaScotia, newzealand, argentina; finland and suomi).
- Large rooms whose canvas calls were scattered and whose mark came from a Discord group (dankmemes, leagueoflegends, DestinyTheGame, clashroyale, eve).

Paired lead checks, both sides read, block 14 (full lines in the diary): agree for croatia and TheHulk; croatia and undertale (corrected after a first misreading); splatoon and fivenightsatfreddys; weezer and smashbros; Temple with rutgers; sweden and vim with archlinux; chelseafc with starcraft; drumcorps, wow and Redox with rust; czech with mindcrack; titanfall with ubreddit; ockytop with floridagators; hunterxhunter with lifeisstrange; aceattorney and sheffield with onepunchman; iceland with splatoon; sixers, frankocean, TransFlagPlace and TheFarLeftSide with kanye. Not found in the concepts read: ubc, uoft, stevenuniverse with polandball; buffalo with nerf; edmontonoilers with canucks; costa_rica with runescape; ethereum with archlinux and bitcoin; several with kanye.

## Contrary rooms

Blocks 01 to 11: see `notes-A1.md` and earlier heads; kept here by name only. Block 01: morrowind, megaman, heyyea, egypt, duckgame, AprilKnights, flashtv, PinkVomitMonster, FloydVsVoid, anime, watchmen, TheAdventuresofTintin, tagpro, qotsa, cfb, drugs; from the screen UNLincoln, yerbamate, Redox, azores, archlinux. Block 02: homelab, hentai, kpop and ubc, norge, cirkeltrek, loltyler1, bobross and nonbinary, zelda. Block 03: ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft and GuildWars2, bardmains, placeDE. Block 04: theitalyplace and spacexmasterrace; tampabaylightning; aoe2; 4chan; ice_poseidon; korea; drawhelix. Block 05: greenlattice, norway, utaustin, france, masseffect, ducks and mariokart, natsume. Block 06: thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit. Block 07: falcons, formula1, slovenia, sweden, wine, btc, nin, uoft. Block 08: ReBoot, nVade, epublica, lego, foxes, math, popheads, ockytop. Block 09: sadboys, spacex, Fez, warthunder, nascar, israel, magictcg, tenma, ManningPlace. Block 10: cgpgrey, EraseThePlace, dankmemes, anarcho_capitalism, twice, TeamYellowPlace, mcgill, PokemonSage. Block 11: UNLincoln, totallynotrobots, finland, udub, GreenEmpire, danganronpa, india. Block 12: ontario, orderofthebluecorner, CelticFc, enterthegungeon, eve, anarchocapitalism, teamcube. Block 13: counting.

Block 14:
- polandball: a sub with a 1,310 px polandball on the canvas whose own record shows an April Fools switch and members asking who planned it.
- ubreddit: the canvas links a SUNY at Buffalo region far from the room's conceded brick.
- canucks: began by attacking the Flames logo and built its own later; its thread carried antisemitic jokes about a rumoured r/Israel plan.
- rust: a botnet whose organisers cut their own target and called land-grabbing bad citizenship.
- fivenightsatfreddys: lost and rebuilt its monument several times while its Discord and its sub fought over which character to draw.
- kanye: painted over others early "to spread the wavy word", then hosted and defended many neighbours.
- azerbaijan: one member's flag in the last half hour, called for by a visitor from r/turkey.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 15 and after:
- joining or finding work begun elsewhere, against starting it; finding it only after the close; a linked region placed from the first hours, against the room's late first call; a linked region far from where the room built;
- organizing in the thread, against organizing in Discord or a second sub; a Discord that controls who may edit, against one that is a voluntary meeting place;
- deals that bind a room, against deals its own participants or the other side's do not know or keep; deals accepted by one member who disclaims the room's voice;
- a treaty kept against the room's own wish, against one broken by its own rogues;
- a sub made for the canvas that governs others, keeps a single work, asks leave, erases, fades, or polices purity;
- a national flag run as a permission office, a watcher, a front line, or an alliance office;
- scripts written in self-defence, scripts refused on principle, scripts that repair a rival, joint scripts with a former rival, bots restrained by their own organisers;
- the moderator as organiser, obstacle, gatekeeper, prankster, enforcer, or hacked account;
- a large room with a large mark, against a large room whose mark came from a Discord group or stayed small;
- the late-room kinds listed above, including the sixth (CelticFc, azerbaijan);
- the canvas fields linking the room's work, a neighbour's, a covered or lost work, or a work the room never names.

## The last rooms read

Block 14, in reading order: rutgers, shishamo, belgium, croatia, onepunchman, paranatural, fivenightsatfreddys, kingdomhearts, archlinux, TheHulk, polandball, runescape, splatoon, armok, starcraft, satania, cuboulder, nerf, bitcoin, kanye, smashbros, ubreddit, vietnam, undertale, floridagators, Dominican, lifeisstrange, rust, canucks, PUBATTLEGROUNDS, mindcrack, azerbaijan.

## Ledgers at this close

- `lexicon-A1.md`: 938 lines. `running-A1.md`: 435 lines. `leads-A1.jsonl`: 1,844 lines. Every lead's `other` is in `order-A1.txt`, letter case aside; checked at this close with grep, sort and comm.
- Corrections appended this leg: a belgium lexicon line truncated to "terro" was superseded by the full words; a polandball lexicon line that used the coder's label "Polandparagraphs" was superseded by the room's words "poland paragraph day". Two diary lines were corrected by later lines (armok is not a first-builder-script case; croatia's record does hold the three-pixel request undertale names).
- Rule, kept: fetch every id with `cite.py` and check every lead's room with grep against the frame; append through a grep filter on the item id; never type an id from memory. Lexicon words are copied as written from the item text, never from the coder's labels. Struck-by lines are checked against `cite.py` before writing.
- The hook rejects notes of 350 words or more by its own count, which sometimes runs up to 20 words above `wc -w`; keep `wc -w` at 340 or below. Drafts still run 375 to 420; draft the `doing` line at about 130 words.
- The permission check refuses shell commands holding the string "=w=" and some loop and heredoc forms; awk is denied. Use grep, cut, tr and plain echo appends.

## The next comparison

Block 15 holds 37 rooms, beginning with r/theblackvoid, a void group named as attacker by r/runescape and r/canucks this leg; read the lead lines first. For every room: did the artwork exist before the room's first call, and who built it? Do the canvas fields link the work the room describes, and where? Was the deal struck in the thread, in Discord or in a second sub, and did both sides' participants keep it? Which side of the onset contrast is the room on, and is it a sub made for the canvas? When later blocks bring rooms named in block 14's leads (thenetherlands and PlaceNL, quebec, scotland, livecounting, mylittlepony, philippines, msu, cavestory, unturned, purdue, tf2, rwby, GabrielDropout, FaroeIslands, turkey, edboxes, placestart, 2007scape, lakers, borussiadortmund, dota2, ainbowroad, snsd, parabola, marvel), read the lead lines first.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
