# The census: from 1,473 artworks to 706 communities

*Kind of page: explanation: the judgements behind the population.*

Every room the study codes is a subreddit that the 2017 atlas credits with an artwork. This page shows each step from the atlas to the 706 communities the study counts as its population, and names the steps that took a judgement. Those steps cannot be regenerated from downloads; their results ship as files in [coder/census/](../coder/census/README.md), and each is linked below.

## The narrowing

One line per cut, from every artwork on the atlas to the communities one could code. Each line says how many leave and why.

| | Artworks | Communities | Leave or join | Why | Kind |
|---|---:|---:|---:|---|---|
| the 2017 atlas | 1,473 | | | | download |
| name no subreddit | 1,236 | | 237 leave | the entry links no subreddit ([what they are](artworks-outside-the-population.md)) | download |
| name only links that are no community | 1,227 | 763 | 9 leave | user pages, r/all, a private sub, a Discord group, names with no archive, a subreddit founded in 2022 | **judgement** |
| named on the canvas, not by the atlas | 1,227 | 767 | 4 join | the community's name is written on the final canvas and it organised there in its own threads | **judgement** |
| named in an atlas description as maker, not linked | 1,227 | 776 | 9 join | an artwork's description credits it, and it took part in its own threads | **judgement** |
| a redirect kept as a row | 1,227 | 777 | 1 | r/TFLS points to r/TheFarLeftSide, which now carries its three artworks; its row stays, read `none` | **judgement** |
| silent in the 73 hours the canvas was open | 1,200 | 748 | 29 leave | nothing posted while the canvas was open | count |
| active only after the freeze | 1,193 | 741 | 7 leave | talk about a frozen canvas is not organising on a live one | count, then **judgement** |
| text takes no part in the event | 1,164 | 709 | 32 leave | a coder read `none` (29, r/TFLS among them), or a check read no event talk (3) | **judgement** |
| no writing about the event while the canvas was open | 1,162 | 707 | 2 leave | r/lehigh wrote about it only after the freeze; r/upvote never did, by two aggregator readings (J, 4 October 2026) | **judgement** |
| the field, not a case | 1,161 | **706** | 1 leaves | r/place, where the rooms met; coded and modelled apart, it enters the aggregator at stage C4 ([the stage](stages/C4.md)) | **judgement** |

The 706 are `handable = 1` in [MASTER-census.csv](../coder/census/MASTER-census.csv): 298 `case` rows (coded, and the event is in their text) and 408 `candidate` rows (not yet coded when the sheet was built). A candidate coded `none` later leaves as well, so 706 is the most one could code. The artworks column counts the artworks that still credit at least one community on the line; an artwork shared by several communities stays while any of them does.

The 763 communities the atlas links come from its links: 759 are named as typed (case-folded, `r/` removed), four through a link corrected by hand (below), and 20 of the 760 were collected only when the links were checked. The four from the canvas and the nine from descriptions have 0 in `atlas_artworks`; `validations.jsonl` gives each one's reason and evidence. The link files are [census_740_mapping.csv](../coder/census/census_740_mapping.csv), [atlas_35_resolution_worksheet.csv](../coder/census/atlas_35_resolution_worksheet.csv) and [atlas_link_unresolved.csv](../coder/census/atlas_link_unresolved.csv).

### From the population to the aggregator

The 706 are what the yard codes; the aggregator reads a frame, a dated copy of the rooms whose coding had finished. On 4 October 2026:

| | Communities | Why |
|---|---:|---|
| the population | 706 | the table above |
| in the yard | 706 | every one has a room (the yard also keeps 34 rooms the census screens out, r/lehigh and r/upvote among them) |
| in the v43 frame | 705 | coded when the frame was taken (4 October 2026), all in the yard by gpt-5.6-sol at medium; 700 on 2 October 2026, 696 on 28 September 2026 |
| not yet coded | 1 | r/the_donald, held in the yard at "brief awaiting validation" since 30 September 2026; 7.0 per cent of the population's text in the coders' window |

**The run reads 705** (J, 4 October 2026; 700 from 2 October, then r/anime, r/DestinyTheGame, r/hearthstone, r/masseffect, r/pcmasterrace, r/rickandmorty and r/wow as the yard finished them on 3 and 4 October, less r/lehigh and r/upvote). r/the_donald, the largest room by text, is not in this snapshot; every count says it is of 705. Slices where a single thread of 500 to 5,200 items filled the coder's budget came back uncoded; they are not recoded, and contract §5 names the seven rooms whose canvas talk they hold. A room a coder closes `none` leaves the population. `import_rooms.py verified` imports the verified rooms of the population and refuses any other.

## Checked again, 26 September 2026

Every line of the table was recounted from the pinned atlas, the text record of each community was counted again in the archive, and the final canvas was read for written names. The census was then rebuilt with its own builders, which reproduce the earlier sheet exactly from the same inputs. What changed:

- **Two short records replaced.** 759 of the 763 communities were counted again (four giants timed out: r/argentina, r/place, r/thepointing, r/the_donald). 730 match the census exactly, and 27 are short by one to five items that Reddit or the archive has dropped since August. r/chelseafc (655 items in the 73 hours, against 3,400) and r/hyperlightdrifter (93, against 152) had been collected short; both were collected again in full and their rows rebuilt. Neither changes membership.
- **Two links resolved.** Artwork 467 (ANZAC Monument) links the multireddit `newzealand+australia` and now counts for both; artwork 1883 (Danish Avocado) links `avocodoarmy`, a misspelling of r/AvoArmy, whose name is written on the canvas beside its avocados. r/2007scape's artwork count was one short and is corrected. No community is added.
- **Four communities join from the canvas** (J, 26 September 2026). 112 `r/` names can be read on the final canvas; four belong to communities no atlas entry credits that organised on the canvas in their own threads: r/catalunya (the Senyera, credited to r/catalonia), r/morrowind (Vivec, credited to r/truestl), r/satania (beside the Gabriel Dropout art) and r/tenma. Each is recorded in `validations.jsonl` with its evidence. The reading covers the final canvas only; a name painted over before the end is not seen.
- **The links left hold up, but one.** Each was looked up again in the archive, under every case. The Robin link is a truncated name: r/ccKufiPrFaShleWoliGtM exists, and it is now a census row; its one post in the 24 days comes after the freeze and is a joke about Robin, so it leaves with the post-freeze rooms. r/transgenderplace was created in 2022. r/clanicahn, r/RatHub and r/centuryclub have no records (the last is private, and private subreddits are not archived). The three user pages lead to two individual makers and to u/Zequez's bot; he also coordinated r/totallynotrobots, already a row.
- **The names on the canvas hold up.** Of the 112 names read, the ones with no row are short forms of rows (r/KSP, CFC, NZ, RBTV, DTG), misreadings (r/Kilian, r/heyyea), the four added, or names with no records at all (r/arhok, r/eubers, and one partly covered).
- **Nine communities join from atlas descriptions** (J, 27 September 2026). Every description of the 1,473 was searched for subreddits named as makers but not linked. Nine took part in their own threads: r/FinalFantasy (the French FF Mage), r/AyyMD (the AMD logo), r/CKCrusaders (Crusader Kings), r/dankmemes (Gnome Child), r/ElderScrolls (Vivec), r/glasgow (the Scottish thistle), r/purplecorner (the purple corner), r/ukplace (the UK flag) and r/OrderOfTheKoi (the koi on the Italian flag, organised without once naming r/place). Their records come from Layer B's venue collection. Three more were named as makers, r/brazil, r/PICT and r/spacefarts, and checked on 27 September at 11:55 UTC, once the archive answered: none adds a community. r/Brazil and r/Pict exist but hold no post or comment from 24 March to 17 April 2017; r/spacefarts holds nothing at all. Blanka (#708) is already credited to r/brasil, a population member, so 'r/brazil' in its description is a misspelling. #1174 and #1177 stay outside the population.
- **The field** (J, 27 September 2026). r/place, the subreddit the event was named after, leaves the population. It is not one community acting on the canvas but the square where the communities met, and a room of 207,342 items that narrates every other room is not a case beside them. It is coded apart and modelled by a sealed analyst; the aggregator receives that model after the literature and before its account, at stage C4, and returns whatever the field adds to every room.
- **A redirect.** r/TFLS, read `none` by its coder, holds one item: a link to r/TheFarLeftSide. Its three artworks, the largest "The Far Left Side", now count for r/TheFarLeftSide, already in the population; r/TFLS keeps its row.
- **Descriptions checked too.** 29 of the 237 unlinked artworks name a subreddit in their text. Apart from r/place, each is a census row already, except r/czechoslovakia, which posted nothing from 24 March to 10 April 2017.

The earlier sheet is kept in `rplace-set-aside-2026-09-26/census-before-regen/`, outside the repository.

## The judgements

**1. Which community an atlas link means.** The atlas names subreddits as annotators typed them. Case-folding the 1,236 artworks' links gives about 775 names. Each was resolved by hand, and 35 did not match a downloaded community at first. Nineteen were real rooms nobody had collected; they were collected, and none had anything in the window. Four were wrong rather than missing, and each was assigned to the community the artwork belongs to:

- `hyperlightdrifer` is a typo for r/hyperlightdrifter;
- `r2007Scape` is r/2007scape with the `r/` folded into the name;
- `ProtectTheT` was founded in 2019; the artwork's title names r/ockytop;
- `Chelsea` is a real but dormant sub; the artwork belongs to r/chelseafc.

The eight links left are not communities or cannot be collected: r/all, three user pages, a private sub, a Discord group, a name with no archive, and a subreddit founded in 2022 on an artwork credited to other communities as well. Three more, a multireddit, a misspelling and a truncated Robin room name, were resolved on 26 September 2026 (below). `atlas_link_unresolved.csv` lists all fifteen with their resolution. Two subreddits collected while settling these, r/Chelsea and r/rockytop, are not census rows, since the artwork each was a candidate for belongs to another community.

**2. What counts as being there.** The rule is writing about the event during the 73 hours the canvas was open (2017-03-31 16:00 to 2017-04-03 17:00 UTC), not the 97-hour window the coders read (J, 4 October 2026: "we need only communities in which there was some writing"). Until then any post in the 73 hours counted, which let in r/lehigh: 12 posts while the canvas was open, none about it, and its writing about the event beginning at hour 78.98. It and r/upvote, whose one coded thread asks for upvotes and names no canvas, drawing or placement, left on 4 October; each carries its reason in `validation_note` and in `validations.jsonl` (`event_talk_after_freeze`, `no_event_talk`). Twenty-nine communities have nothing in the window at all. Six have nothing while the canvas was open and something in the 24 hours after it froze; four of those six were read by a coder as talking about the canvas (`full` or `trace`). They are out all the same: talking about a frozen canvas is a different act from organising to place pixels on a live one. Each of the six carries its reason in `validation_note`.

**3. Whether the text takes part in the event.** A lexical screen (`screen_class` and the `hit_*` columns) counts marker words over the 97-hour window. It never drops a community, because its markers are English and it misses rooms that name the artwork and not the event. A reading decides:

- a coder's verdict of `none` screens a room out (29 rooms);
- four rooms the screen flagged were read one by one by a Claude session on 27 August 2026, and each reading is in `validations.jsonl` with its evidence. r/britishcolumbia, r/connery and r/realgirls hold no event talk and are screened out. r/PokemonSage names the Foliat sprite and never the event, and it stays in.

The coder's verdict and the post-freeze rule answer different questions, what the text says and whether the room belongs, which is why the verdict is not the count. The count is the `positive` and `handable` columns.

## How the sheet was built

The counts in MASTER-census.csv come from raw24 and could be rebuilt. The judgements cannot; they are inputs. The study's builders, made on 27 August 2026, are in [coder/census/builders/](../coder/census/builders/README.md), unchanged, and run in this order:

    build_venue_activity.py  raw24 census_740_mapping.csv    the venue counts per community
    emit_tables.py                                           venue_summary.csv
    screen_event_talk.py     raw24 census_740_mapping.csv    the lexical screen
    build_master_census.py                                   MASTER-census.csv, applying the coder
                                                             verdicts and validations.jsonl

They keep the study's folder layout, and the coder verdicts they read come from an earlier run's output that is not shipped as a file; the sheet carries them. The builders' README says what a rerun needs.

## What the coders and the aggregator took from it

**The yard.** The scheduler codes the rooms of `STATUS.tsv` from the bottom up, smallest first. On 27 September 2026 the yard held 741 rooms: all 708, r/place (the field, coded apart), and 32 rooms outside it, which were built before the screen closed them (29 stopped at the brief, 3 coded and closed `none`). r/chelseafc and r/ockytop, two of the resolved links, and the four communities from the canvas were added that day from a fresh collection; by the evening all but r/chelseafc were coded and verified. r/PokemonSage and r/hyperlightdrifter, coded before the yard existed, were added for recoding.

**The aggregator.** The v38 frame (`package/FRAME.md`) is every room of the population whose coding had finished when the copy was taken. A room outside the population never enters it: `import_rooms.py` refuses it, so r/britishcolumbia, r/connery and r/realgirls, coded in the yard and closed `none`, are not in the frame. On 26 September 2026 the frame held 659 rooms ([the numbers](numbers.md) give the current count). One of them, r/counting, has reply chains up to 1,004 deep, more than the store's reader can open; its forest is cut at depth 490, and [the forest page](files/aggregator/package-forest-jsonl.md#the-depth-cut) says what the cut removes.

## Two cautions

The census is a census of claimed artworks that survived. A community that organised and was painted over before the freeze has no atlas entry and no row, and the 237 artworks that name no subreddit, work with no room behind it, are outside it by construction. [The artworks outside the population](artworks-outside-the-population.md) says what they are and who made them.

The numbers moved while the study ran. Documents written before 27 August 2026 say 740 (downloaded, not cases) and some say 219 or 287 positive (a filter on the coder's verdict that let the post-freeze rooms back in). The sheet is the count.
