# The raw record for the quote check at E1

Built 2026-09-30 by `aggregator-handler/build_raw_record.py` (J: build the raw record for the quote check; do not touch the data). For every room of the frame, the record its coder read, `coder_corpus.jsonl`, gzipped in `<sub>/coder_corpus.jsonl.gz`: yard rooms from `Layer A/50_coding_runs/yard_v30/rooms/<sub>/run/` or its `run.tar.zst`; earlier rooms from their batch in `Layer A/50_coding_runs/` (`40_analysis/coder_version/coder_version.csv`). The sources were read only.

`MANIFEST.tsv`: per room, where it was coded, the source, lines, bytes and the sha256 of the uncompressed file. All 705 rooms of the frame, every one coded in the yard (since 2026-09-30, when the 299 rooms coded before the yard were recoded there under v32 and this record rebuilt for them from their yard runs). The earlier records of those 299, including the raw24 stand-ins for the four v16 rooms, are set aside in rplace-set-aside-2026-09-26/v38-earlier-coded-rooms-before-recode-0930/raw/.

The analyst never reads this folder (INPUT is denied to it). `check_quotes.py` reads it first. The room folders are not committed (gitignored); this file and the manifest are.

On 2026-09-30 the 23 rooms recoded at medium in yard_v30_medium_v2 were rebuilt from that yard (MANIFEST.tsv says `yard:` for both yards); their corpora are byte-identical to the ones they replace.

On 2026-10-04 (the frame of 705) the seven rooms that finished in the yard (r/anime, r/DestinyTheGame, r/hearthstone, r/masseffect, r/pcmasterrace, r/rickandmorty, r/wow) were added from their `run.tar.zst`, and r/lehigh and r/upvote, which left the frame, were set aside with their manifest rows (`Jail/_to_delete/2026-10-04-set-aside/r-place/frame-before-705-20261004/`, beside the repository). Earlier entries in the manifest are unchanged.
