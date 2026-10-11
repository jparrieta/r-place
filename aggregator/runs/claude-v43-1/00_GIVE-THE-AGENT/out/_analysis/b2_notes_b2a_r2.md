
## Leg B2a-r2, build round 2, 2026-10-11

### QB2-003, revisited

The PI's answer to QB2-003 arrived during B2b-r1, and that leg applied it in full. Every repair is a `scheme_edits.jsonl` line with `caused_by` `gates:T3-a|T3-b`; mirrors are kind gate-check, with no recheck and no tier_history line; new sentences are scheme-ambiguous and owe both. My assumption, to repair only the pairs round 1's edited themes belong to, was dropped in that leg. No work of this leg rested on it. `mem.py gates` on the scheme served this round finds 0 one-way discriminators, 0 `must_not_show` lines without a discriminator and 0 unknown ids. 28 pairs are confirmed and 464 are not. The answer asks me to confirm each pair I read; the 464 are read and confirmed before the freeze.

### The ten biggest bags, placed

I read all ten second-order themes whole, paged with `--limit` and `--offset` and never cut. Then I placed them, before any round-2 packet existed. `out/_analysis/b2_author_r2.py` appended them to `author_items.jsonl`. It checked every theme id against `scheme.jsonl`, and every concept against the item's own concepts with `vlib.support_problems` and `vlib.also_present_problems`. It also checked that no item was already in the hard or gold set, and it took each item's rank from `notes-B1.md`'s list. Each line carries `source` "biggest-bag", `support_by_theme`, `item_is_a_bag` and `also_present`. All ten are arguable. The hard set is now 50 items.

Rule 0, as amended, decides the form. Round 1 showed that my second kinds were author-errors whenever one theme carried the material. So no line places more than one theme. A bag, an item that needs more than three themes, places one and names the rest under `also_present`, each with its own concepts.

The next table lists the ten items: the theme placed, the themes named under `also_present`, and the B1 working kinds.

| rank | item | concepts | placed | also_present | B1 working kinds |
|---|---|---|---|---|---|
| 1 | leagueoflegends t02 | 798 | T3-023 | none | T3-023 |
| 2 | theblackvoid t09 | 389 | T3-006 | none | T3-006, T3-080, T3-085 |
| 3 | ainbowroad t11 | 361 | T3-035 | none | T3-035, T3-084, T3-139 |
| 4 | 2007scape t04 | 349 | T3-038 | T3-005, T3-123, T3-010, T3-179, T3-157 | T3-038 |
| 5 | theblackvoid t12 | 335 | T3-174 | T3-006, T3-163, T3-190, T3-005 | T3-031, T3-163, T3-174 |
| 6 | ainbowroad t04 | 327 | T3-021 | T3-139, T3-024, T3-011, T3-084 | T3-021 |
| 7 | ainbowroad t03 | 326 | T3-005 | T3-084, T3-149, T3-050, T3-124 | T3-005 |
| 8 | dota2 t05 | 314 | T3-023 | none | T3-023, T3-032 |
| 9 | ainbowroad t07 | 311 | T3-041 | T3-035, T3-160, T3-033, T3-061 | T3-038, T3-041, T3-160 |
| 10 | sweden t01 | 310 | T3-065 | T3-035, T3-012, T3-061, T3-113, T3-151 | T3-065 |

Six are bags and four take one theme. Points from the reads:
- leagueoflegends t02 and dota2 t05 are the two moderator makeovers (Marc Merrill, and Arteezy as r/tz). Objections to the joke, reactions to Riot's own jokes and asks to keep the theme are present, but the takeover carries them.
- theblackvoid t09 calls attacks on named targets: national flags, the EU flag, the trans ribbon, "the slimy swedes". The B1 working kinds added T3-080 and T3-085. I found the calls to attack carry the material and placed T3-006 alone.
- ainbowroad t11 is outside rooms addressing Rainbow Road as host. Requests for space, pleas for help and pleas not to be run over sit on one host relation, and T3-035 carries them.
- theblackvoid t12: I placed T3-174 (loyalty to the Void's colour: hails, the oath, anthems) over the B1 working T3-031. The creeds are professions of loyalty, not in-jokes played inside the room.
- ainbowroad t07: I placed T3-041 (extending strands, adding features) over T3-038. The road was already built; these concepts extend it.
- ainbowroad t03 holds the line "KILL THE GAYS" (c1395), posted to the room. It is served to readers as it stands.

### What was built

**`RETURN-B2.md`.** It gains the `also_present` clause in J's words of section 1. A bag places one theme and names every other with its own concept ids; otherwise the field is `{}`. It also gains a paragraph on parts: read every part, reply with the end marker alone on every part but the last, and answer for all items on the last. The batch name is now `P03-r2`. The round-1 text is kept as `out/_analysis/RETURN-B2_round1.md`; round 1 is scored as it was sent.

**The packets, in parts (QB2-001).** `packets.py B2` writes one packet and exits when it is over 50 KB. Round 2 renders to about 513 KB, and leagueoflegends t02 alone is about 87 KB. So the splitter `out/_analysis/b2_parts_r2.py` imports `packets.py` and uses its own `Store.item` and `scheme_pages`. It shuffles the 50 items as `packets.py` does, with seed 20261012. Then it cuts the rendered lines into parts. An item that does not fit runs on into the next part under its heading marked "(continued)". A concept line always travels with its quote line, and positions run on across parts. The helper checks that every concept of every item is served exactly once. It wrote `out/_packets-B2/round-2/`:
- `index.md` (33,542 bytes) and 21 family pages (7,839 to 19,772 bytes), from the edited `scheme.jsonl`, with no exemplars;
- `P03-r2-p1` to `P03-r2-p11`. Ten parts are 50,254 to 50,394 bytes and the last is 9,799; each is under 51,200 bytes with its end line, 513,096 bytes in all;
- `MANIFEST.json`.

The next table lists the positions each part holds.

| part | positions | part | positions |
|---|---|---|---|
| p1 | 1-8 | p7 | 37 |
| p2 | 8-19 | p8 | 37-39 |
| p3 | 19-27 | p9 | 39-43 |
| p4 | 27-28 | p10 | 43-47 |
| p5 | 28-36 | p11 | 47-50 |
| p6 | 36-37 | | |

Position 37 runs over four parts (p5 to p8); it is leagueoflegends t02. The seeded order and the positions per part are in `out/_analysis/b2_order_r2.json`, outside the readers' folder. Round 1's packets are where they were: flat in `out/_packets-B2/`, and J's copy in `round-1/`. No gold item and no room note is in the folder.

**MANIFEST.json, on QB2-004's assumption.** QB2-004 is open. It asks what form `fleet.py` expects when one item is larger than a part. Until it is answered, each part carries `count_key` position, the B3 exclusions, `group` P03-r2, `part` k and `parts` 11. Parts 1 to 10 carry `items` 0, since their reply is the end marker alone, and part 11 carries all 50. Each entry also records its positions and the seed. If J answers otherwise, the next build leg rebuilds from the same helper.

**Manifest.** `run_manifest.json` has a B2 round-2 entry (`out/_analysis/b2_manifest_r2.py`). It records the model, deepseek/deepseek-v4-flash-0731, and J's reader settings: one provider (Relace) and medium reasoning effort. Round 1 ran at high effort on mixed providers. A change in agreement between the rounds is therefore partly the settings and not only the edits. The entry also records the seed, 3 agents, 50 items, and every part's bytes and sha256.

**The PI's round-2 rule.** No round may meet a stopping rule before the ten biggest bags have been read once. Round 2 serves all ten, so its check leg may apply the stopping rules.

**Questions open:** QB2-004.
