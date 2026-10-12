
### The rebuild in B2's packet shape

- **Packets** (`out/_analysis/b3_packets_fleet2.py`, in `out/_packets-B3/`). `index.md` and `G01.md` to `G21.md` come from `scheme_final.jsonl`, with no exemplars and every page under 50 KB. There are 1,210 self-contained packets, one per batch. Each carries a title naming the batch and its replicate, the brief with its own item count, the sibling block of every room in the batch's `rooms`, the items in position order and the end line.
- **Sizes.** At most 15 items and 178,758 bytes of item text a packet.
- **MANIFEST.json.** It gives each packet its items, bytes, `item_bytes`, sha256, count key and excludes, and `codes_by_item`, with no group, part or parts. It lists 17,653 lines due.
- **Fleet ids only.** nyjets t11's coder note serves c0104 as its fleet id. The tank names "t34" and "t90" in a warthunder participant's words stand in B0075 and B0819; `fleet.py`'s guard now reads id positions only (QB3-002).
- **`RETURN-B3.md`.** It no longer speaks of parts. The second pass comes after the last first line and before the end marker. J's two rulings stand word for word.
- **`run_manifest.json`.** A B3 entry of this shape supersedes the first (11 entries).

### The close-check, B3a

`validate.py B3` reported:

```
stage B3:
  batches 1210, R 2, rooms 705, items 7844, graph one component
  leg: build (0 dispatch folders with DONE)


0 errors (0 distinct shapes), 0 warnings
```

The leg closes with `done.sh B3 --cut packets-out`. J runs the dispatch in two groups, the first 100 batches and then the other 1,110, with the gold check of section 3.2 between them.
