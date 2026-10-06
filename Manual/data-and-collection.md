# Data and collection

*Kind of page: how-to: getting each data store.*

Where the data is, how to get all of it, which scripts built each store, and on what terms it is shared. The instructions and scripts are in [`data/`](../data/README.md), one folder per store; the folder holds no data: each script downloads or builds its store in place.

## The stores

| Store | Folder | Size in the study | Used for |
|---|---|---|---|
| the pixel record | [data/pixels](../data/pixels/README.md) | 16,559,897 placements | canvas facts at aggregation; never given to a coder |
| the atlas | [data/atlas](../data/atlas/README.md) | 1,473 artworks | pointers and neighbours only; its descriptions never enter coding |
| the placer accounts | [data/users](../data/users/README.md) | 1,101,801 accounts, about 14 GB | building the venues from placer writing; placer counts |
| venues, placers only | [data/venues-placers](../data/venues-placers/README.md) | 50,936 venues, 13.6 GB | screening: which venues carried r/place action |
| venues in full (raw24) | [data/raw24](../data/raw24/README.md) | 24,093 venues, about 51 GB | coding: every room is cut from its raw24 file |
| pixels per artwork | [data/pixels-per-artwork](../data/pixels-per-artwork/README.md) | 23,058,857 rows, 1.1 GB with the panel | who built where, and when; the aggregator's `artworks.jsonl` |
| hourly pixels per community | [data/pixels-hourly](../data/pixels-hourly/README.md) | 67,907 rows | the aggregator's `pixels.csv` and stage D4's activity table |

**raw24 or venues from placers?** They answer different questions. raw24 holds the whole community, so it is what a coder reads and what a replication of the coding needs. The placer-only store holds what the canvas's participants wrote, wherever they wrote it, so its denominator is right for any placer-side count, and it reaches venues no community sweep touched.

## Getting it

[data/README.md](../data/README.md) gives the order, seven steps from the public sources to every store, with the command for each. Each store's folder says how the study's own copy was made where it differs, and `LINK.md` says where that copy is: the atlas venues' raw24 is on the [Drive](https://drive.google.com/drive/folders/1itd-IZsAhBq9lMzCnrQERlO2vfxdT9g6); the other stores are to be added. Every step was run end to end on a small sample on 2026-09-26, with the results in each README; the full collections, which take days, and the tile dump's download were not.

## How it was collected

Every text record came through one archive, arctic-shift (`arctic-shift.photon-reddit.com/api`), which serves Reddit's record as it was ingested at the time, not Reddit's current record with years of deletions applied. Venues were walked uncapped over the 24-day span; placer accounts were walked by author. The event window is fixed in one module, [rplace_window.py](../data/_lib/rplace_window.py): the canvas opened 2017-03-31 16:00 UTC and froze 2017-04-03 17:00 UTC; the coders' window adds one day after.

## Earlier instrument versions

[archive/instrument-history.tar.gz](../archive/instrument-history.tar.gz): one file, 11.3 MB, 622 files: Layer A's `10_instrument` (the coder contract's earlier versions) and `60_aggregator` (the aggregator's), instruments only. [HISTORY-MANIFEST.tsv](../archive/HISTORY-MANIFEST.tsv) lists every file and why any was skipped. Built once on 2026-09-25 by [bundle_history.py](../aggregator/handler/bundle_history.py) and frozen. Earlier aggregator runs are not shipped.

## Terms of use

Everything here is open, and using it requires citing the study (see [CITATION.cff](../CITATION.cff)).

- **Code** (every `.py` and `.sh`): the [MIT licence](../LICENSE). It asks that the copyright notice travel with the code.
- **Documents and the instrument's text** (contracts, stage files, the Manual, codes, themes and cases the agents wrote): [CC BY 4.0](../LICENSE-docs.md). Use and adapt them freely; attribution, meaning a citation, is a condition of the licence.
- **Third-party material is not ours to license.** Reddit posts and comments belong to their authors and fall under Reddit's terms; the pixel record is Reddit's public release; the atlas is placeAtlas's. The licences above cover the study's own work on them, not the material itself.

Please, as a matter of research ethics rather than licence:

- no attempt to re-identify a placer from the pixel record beyond the study's own join;
- no username in a published table, figure or quote without the scrubbing the paper describes;
- honour deletions: a post deleted since collection should not be republished.

This page is not legal advice.
