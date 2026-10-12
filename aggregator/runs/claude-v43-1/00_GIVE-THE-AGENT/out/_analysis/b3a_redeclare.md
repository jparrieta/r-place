
### Declarations revised under J's ruling (QB3-001, QB3-002; 16:37 Berlin), before the new packets

**J's ruling.**
- **Packet shape.** B3 uses B2's packet shape. Every packet is self-contained: at most 15 items and 180,000 bytes of item text, no MANIFEST group, part or parts, and its own item count. No item is split across packets.
- **Rooms.** A room may be spread over several packets; each packet carries the sibling block of every room it holds items from.
- **Gold copies.** They are listed in `items` and in `gold_items`, exempt from room membership and left out of coverage.
- **Returns.** Multiplacement records ride on the item line. Pass-2 lines carry `revises` after the pass-1 lines in the same return.
- **Warm-up and exemplars.** The warm-up stays in reserve, and no exemplars are served.
- **The handler's fixes.** The check now expects 7,844 items and ignores the withdrawn split. `fleet.py`'s room-id guard reads id positions only. A packet with 0 lines due is accepted.

**What changed in the build.**
- **Superseded, kept under new names.** The first build's whole-room batches served in parts: `out/_analysis/batches-B3_parts_superseded.jsonl`, `packets-B3_parts_superseded/`, `b3_dispatch_order_parts_superseded.json` and `RETURN-B3_parts_superseded.md`. The split of leagueoflegends t02 over two parts goes with them.
- **Stand as declared above:** R = 2; the seed 20261015; the gold rate and policy; one duplicate a batch; no exemplars; the warm-up in reserve; the reissue policy; the bag flags.

**The item cap: 15 positions a batch** (corpus items, gold copies and the duplicate's second copy) **and 180,000 bytes of item text** (J). The allocator (`out/_analysis/b3_allocate2.py`) works as follows:
- **Order.** For each replicate it shuffles the 705 rooms under the seed and pours their items in that order. A room's items stay together and run on into the next batch when one is full.
- **Room left in each batch.** It holds back one position for the duplicate's second copy and one for an expected gold copy. It also holds back 40,000 bytes of the byte cap.
- **The largest item fits.** leagueoflegends t02 (89,161 bytes) fits whole in one packet. No item is over 180,000 bytes.

**The allocation** (seed 20261015, under the suffix `20261015:redraw2`: the connectivity gate forced 2 redraws).
- **Batches.** 1,210 batches (605 a replicate), one reader each: 1,210 readers.
- **Positions.** 17,653 in all: 15,688 readings at items × R, 1,210 duplicates and 755 gold copies. Each gold item is seeded 18 or 19 times.
- **Batch size.** Batches hold 5 to 15 positions, median 15, and at most 178,588 bytes of item text.
- **Rooms.** 996 of the 1,410 room-replicates are spread over more than one batch; one room is spread over 22.
- **Coverage, from the batches.** Each replicate places each of the 7,844 items exactly once.
- **Gate 1, per item.** An item's two replicates sit in different batches, on different readers.
- **Gate 2.** The room-batch graph over the corpus items is one component.

**The gold positions.** Each gold item is seeded 18 or 19 times, more often than a batch has positions, so no rule can keep every reader of a gold item on a different position. Each copy instead takes a position at which its gold item has been seeded least often so far, which spreads each gold item over the positions.

**The duplicate.** One item a batch, from its own corpus items, presented twice. The two copies sit at least a third of the batch apart, or as far apart as a small batch allows.

**The rooms on a packet.** A batch's `rooms` are the sibling blocks its packet carries: the rooms of its corpus items, and the rooms of its gold copies, so that a gold copy looks like any other item.

**The order of batches.** A seeded shuffle of the 1,210 batch ids (`out/_analysis/b3_dispatch_order.json`), in two groups: the first 100 batches, then the other 1,110. The gold check of stage B3 section 3.2 runs between them.

**The cost.** 1,210 readers, each reading the index and the families it opens (about 28,000 input tokens, as at B2's gold round), about 34 million input tokens. The item text over the whole fleet is about 11 million more. Output runs about 1,800 tokens a position for 17,653 positions, about 32 million, and more for the second pass. By B2's gold round's prices the fleet costs about 40 to 55 USD.
