# Coder documents copied from the yard, 2026-09-24

Source: `rPlace/Layer A/50_coding_runs/yard_v30/rooms/<sub>/run/out/` for every room with a
`codes.jsonl` at copy time (327 rooms). Copied whole except `_transcript.jsonl` and
`_journal.jsonl` (harness records, 951 MB and 85 MB; they stay in the yard). The yard was read
only. `yard-meta/` holds STATUS.tsv, CODING-PROGRESS, the case-lead prompt, the scheduler
contract, the change log and the frozen v30 instrument text.

`ROOMS.tsv`: per room, codes, themes, retracted codes. `MANIFEST.sha256`: every file's hash.
This copy is a snapshot; rooms coded after 2026-09-24 are not in it. The frame for the v38 run is
a later dated copy taken when coding closes (design note §11, decision 3).

Retracted codes (`retracted: true`, 84 of 63,832) are the coder's own withdrawals. They stay in this
snapshot as the yard wrote them and are dropped at the store build: the store never holds them
(J, 2026-09-24).

## Added 2026-09-24, later: the forests and the briefs

For every room in `ROOMS.tsv`, `rooms/<sub>/forest/` now holds the yard's own rendering of the
coded threads: `forest.jsonl` (each coded thread as a reply tree, one line per thread, coded
turns carrying their code ids and the coder's labels, states coded, bridge, removed, dropped),
`tree_index.json` (coordinate to item per thread, with the header counts), and `<sub>.md` (the
forest as the coder's tools printed it). Re-rendered on 2026-09-24 from the yard's `run/coder_corpus.jsonl` (read only) with the room's
final `codes.jsonl`, by the room's own `run/tools/tree_builder.py` (two versions in the yard, the
v30 and the v32 rooms; each room used its own). The yard's pre-rendered forest in `run/package/`
predated the counter step (step 5) in 137 rooms and lacked 611 coded items; after the re-render
every non-retracted code sits on a forest item. `rooms/<sub>/brief.md` is the pre-event brief from `brief/out/brief.md`, written
before the coder read the window. No item body is copied: the record's text stays in the yard;
the participant's words the store carries are the coded passages in `codes.jsonl` (`text`,
`start`, `end`). Hashes: `MANIFEST-forests.sha256`.

## Re-cut 2026-09-26

The frame held 658 rooms after the re-cut: the 638 of the first copy, less r/britishcolumbia, r/connery and r/realgirls (outside the census population, J 2026-09-26), plus 23 rooms verified in the yard since 24 September, imported with `import_rooms.py verified`, which takes only rooms of the population. r/counting, verified too, was held outside at first, then added the same day (J: keep it, cut the long trees): its forest nests up to 1,004 deep, more than Python 3.11's JSON reader opens, so `import_rooms.py` cuts every forest below depth 490 (`CUT_DEPTH`) in `forest.jsonl` only. Counting loses 1,564 items there, 38 coded, whose codes the store lists as unjoined; `tree_index.json` and `counting.md` stay whole, and the whole forest is kept as `rooms/counting/forest/forest.uncut.jsonl`, which no tool reads. It is the only room the cut touches. The frame is 659 rooms. `ROOMS.tsv` is rewritten by `import_rooms.py rooms_tsv`; `yard-meta/` holds the yard's status as of the re-cut; `MANIFEST-2026-09-26.sha256` hashes every file of every room; the two older manifests record the first copy. `CODERS.tsv` says, per room, where it was coded, the instrument and the model records.

## The population, 26 September 2026

The census was rebuilt on 26 and 27 September: 777 communities, 708 of them the population (r/place left it on 27 September as the field) (`yard-handler/census/MASTER-census.csv`, `handable = 1`; [the census page](../../../Manual/census.md) gives the narrowing). The frame's rooms are all in it.

## Update 2026-09-27

35 rooms verified in the yard since the re-cut were imported with `import_rooms.py verified`: the frame holds 694 rooms. On 28 September r/2007scape and r/europe followed: 696 rooms, 12 of the population still in the yard's queue. `MANIFEST-2026-09-28.sha256` hashes every file of every room and replaces the earlier dated manifests; `CODERS.tsv` has a row per room; `yard-meta/` holds the yard's status of 27 September, 18:39. Twelve of the 35 entered the census from the canvas or an atlas description, so no atlas link names their artworks: their canvas fields and hourly pixel series come from the artworks credited in `data/atlas/credits_beyond_links.csv`. r/tenma has no artwork, so no pixel series and an empty outcome line. The week-before activity of the 13 comes from their raw24 in `Layer A/raw24_additions`, by the study's rule.

## Update 2026-09-30: the earlier rooms recoded

The 299 rooms coded before the yard (instruments v16 to v27, batches in Layer A) were recoded in the yard under v32 (gpt-5.6-sol) and replace their earlier coding here, imported with `import_rooms.py room`. All 696 rooms are now coded in the yard (`CODERS.tsv`: 571 v32, 125 v30). The earlier folders, with the CODERS.tsv, ROOMS.tsv, yard-meta and MANIFEST of before, are in `rplace-set-aside-2026-09-26/v38-earlier-coded-rooms-before-recode-0930/`. The 299 rooms hold 15,329 codes now against 27,921 before. `MANIFEST-2026-09-30.sha256` hashes every file of every room; yard-meta is the yard's status of 30 September.

## Update 2026-09-30, later: one model, one effort

The 23 rooms the yard had coded at xhigh effort (Dorset by gpt-6-astra) were coded again at medium in `Layer A/50_coding_runs/yard_v30_medium_v2` and replace their earlier coding here (`import_rooms.py room` with `RPLACE_YARD_ROOMS` pointing at that yard). Every room is now coded by gpt-5.6-sol at medium (`CODERS.tsv`; the effort is in the yards' STATUS.tsv, `run_agent_specs`). Instruments: 594 rooms v32, 102 v30. `yard-meta/medium-v2/` holds the second yard's status. The earlier coding is in `rplace-set-aside-2026-09-26/v38-xhigh-rooms-before-medium-v2-0930/`. `MANIFEST-2026-09-30b.sha256` replaces `MANIFEST-2026-09-30.sha256`, moved there.

## Update 2026-10-02: the frame is 700

r/leagueoflegends and r/overwatch, finished in the yard (v32, gpt-5.6-sol medium), imported with `import_rooms.py room` (J). With r/dota2 and r/globaloffensive (1 October) the frame holds 700 of the 708; the eight largest are still in the queue. `MANIFEST-2026-10-02.sha256` replaces the 1 October manifest, which is in `Jail 3/_to_delete/frame-before-700-1002/` with the earlier CODERS.tsv, ROOMS.tsv and canvas.

## Update 2026-10-04: the frame is 705

Built for instrument v43 in `r-place` (J). Seven rooms finished in the yard on 3 and 4 October 2026 (v32, gpt-5.6-sol at medium, verdict full), imported with `import_rooms.py room`: r/anime, r/DestinyTheGame, r/hearthstone, r/masseffect, r/pcmasterrace, r/rickandmorty, r/wow. Their codes and themes match the yard's STATUS.tsv (retracted codes kept here, dropped at the store build). Two rooms left: r/lehigh, which wrote nothing about the event while the canvas was open (first coded turn at hour 78.98), and r/upvote, which wrote nothing about the event at all (J, 2026-10-04: "we need only communities in which there was some writing"; the census rule is on [the census page](../../../Manual/census.md)). r/the_donald, the last room of the population, is not coded: the yard holds it at "brief awaiting validation" since 30 September. The frame is 705 of a population of 706.

`CODERS.tsv` has the seven rows and not the two; `yard-meta/` holds the yard's status of 4 October 2026, 01:02 UTC; `MANIFEST-2026-10-04.sha256` (13,711 lines) replaces `MANIFEST-2026-10-02.sha256`. The 698 rooms kept are byte-identical to the frame of 700. The earlier files and the two rooms are in `Jail/_to_delete/2026-10-04-set-aside/r-place/frame-before-705-20261004/`, beside the repository.
