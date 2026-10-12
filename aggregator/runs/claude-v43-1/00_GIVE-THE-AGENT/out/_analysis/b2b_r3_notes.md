
## Leg B2b-r3, check round 3, 2026-10-12

### J's ruling of 12:24 Berlin, applied

No one cuts the bags, neither this run nor the coders. The second-order themes stand as the coders made them. A bag stays one item through B2 and B3: one theme placed, and its other themes under `also_present`, each with three concepts of its own at least. The line under "The B1 bags" that waited for a coder recut is struck, and the head's line with it.

### The dispatch, as the handler rescued it

The dispatch log (`_fleet_raw/B2/round-3/DONE`) reported 7 valid returns and 8 exhausted packets. That was the handler's defect, not the readers': `fleet.py`'s new check counted the third-order ids in `multiplacement_log.additional` as concept codes. The handler fixed it, re-validated every saved reply with the fixed check, and kept per packet the first three valid replies in reader order (`_fleet_raw/B2/round-3/RESCUE-2026-10-12.json`). The other valid replies are in each packet's `_beyond_three/` and are not scored. **`EXHAUSTED.tsv` is superseded by the rescue record.**

`fleet.py`'s counts (`_fleet_raw/B2/round-3/log.jsonl`, read by `out/_analysis/b2_r3_look.py`): 36 calls on deepseek/deepseek-v4.1-flash, medium effort; 15 first issues, 12 first reissues and 9 second reissues; 1.4904 USD; 7,431 seconds of calls in all. Of the 29 calls refused at dispatch, 27 were refused by the faulty check; two had faults of their own (P03-r3-2 r1 cited C0286150, a code not under its item; P03-r3-2 r5 lacked the end marker). The next table lists the kept replies.

| packet | items | kept replies | their durations (s) | their output tokens |
|---|---|---|---|---|
| P03-r3-1 | 12 | r1, r2, r3 | 141, 156, 410 | 38,319; 26,513; 33,862 |
| P03-r3-2 | 13 | r2, r3, r6 | 151, 188, 392 | 27,741; 38,694; 34,939 |
| P03-r3-3 | 8 | r2, r3, r10 | 199, 389, 387 | 38,176; 33,973; 54,632 |
| P03-r3-4 | 7 | r1, r2, r3 | 188, 203, 922 | 34,136; 44,211; 92,036 |
| P03-r3-5 | 10 | r1, r2, r3 | 55, 170, 276 | 13,826; 29,731; 24,440 |

**Translation.** Round 3 is in fleet ids. `out/_analysis/b2_translate_fleet.py --round 3` read only the kept replies and wrote room-id copies to `out/_analysis/b2_r3_returns/`: 150 lines, 0 id problems. The readers wrote the room as "r/name"; the translator drops the "r/" before the lookup in `out/fleet_ids.jsonl`. Every line's heading matches its packet position.

### The three numbers

`out/_analysis/b2_score_r3.py` scored round 3 by the declared definitions (per-item table `out/_analysis/b2_r3_items.tsv`; `pilot_rounds.jsonl` line 3). The readers are round 2's, so the change from round 2 is the scheme's edits 287 to 295 and the readers' own variation (QB2-007). The next table lists rounds 2 and 3.

| figure | round 2 | round 3 |
|---|---|---|
| fidelity, all 50 | 0.639 | 0.682 |
| fidelity against the rechecked placements | 0.701 | 0.760 |
| primary match | 0.747 | 0.780 |
| pairwise agreement, all 50 | 0.718 | 0.728 |
| primary pairwise | 0.833 | 0.793 |
| alpha | 0.710 | 0.721 |
| items with two readers differing | 27 | 23 |
| round-1 items (40): fidelity / pairwise / alpha | 0.572 / 0.685 / 0.676 | 0.611 / 0.676 / 0.668 |
| ten biggest bags: fidelity / pairwise | 0.911 / 0.850 | 0.967 / 0.933 |
| lines with two or more themes, of 150 | 47 | 27 |

Item by item against round 2, pairwise rose on 17 items, fell on 12 and held on 21. By source, pairwise is 0.731 on the pair items, 0.671 on the random items, 0.556 on the round-1 bags and 0.933 on the ten biggest bags.

**Bags.** 22 lines set `item_is_a_bag`; 18 lines name 145 themes under `also_present`, none under the three-concept floor. The themes readers name (placed plus `also_present`) score Jaccard 0.283 against mine on the ten biggest bags, as at round 2. One reader named 24 on ainbowroad t03. Four lines flag a bag and name no `also_present` (QB2-013, below).

### What round 3 showed

**The round-2 edits.**
- Edit 287, the T3-065 gloss (guatemala t02). At round 2 all three readers placed T3-002, T3-167 and T3-026, missing whose flag it is. At round 3 two readers place T3-065 and T3-167, my placement, and cite the gloss ("a flag built in r/guatemala being Guatemala's"). The third places T3-038 and T3-002. Pairwise fell from 1.00 to 0.33 while fidelity rose: the edit doing its work on two of three readers.
- The T3-195/T3-005 and T3-195/T3-011 questions (nVade t04). Round 2: two readers on T3-195, one on T3-005. Round 3: two on T3-005, one on T3-195. I placed T3-011 and T3-005.
- The T3-033/T3-038 question (n64 t02, dofus t01). No reader now places n64 t02 on T3-033; they divide T3-002 (two) and T3-038 (one). dofus t01's pairwise rose.

**The cluster that still divides.** T3-002 (a call for hands), T3-033 (proposing the room's mark) and T3-038 (building and reporting a mark). signal t01 gets three readers on three themes; n64 t02 divides T3-002 and T3-038; on 2007scape t04 one reader leads with T3-070 (directions for placers) where the other two place T3-038. All three items were steady at round 2 except n64 t02. The readers' reasons turn on which act leads: the call, the offer of an idea, or the build and its reports. The scheme's questions in this cluster do not decide that when one item holds all three.

**Single-reader departures on items unanimous at round 2.** ice_poseidon t16 (one reader on T3-192, joking about damage, against T3-031), WisconsinBadgers t04 (one reader on T3-042 alone, the other two adding T3-042 or T3-006 to T3-076), donaldglover t04 (one reader adds T3-032), kpop t04 (the readers' additions vary between T3-136 and T3-066). None touches an edited theme.

**Divisions that persist from round 2.** AyyMD t08 (two of three on T3-023, as at round 2; my author-error), flashtv t13 (T3-073 against T3-009), acecombat t05 (two on T3-014), simonfraser t08 and Goodboye t03 (bags), floridagators t09, furry t10, parabola t02, harrypotter t08, nyu t01, cubers t12, Slovakia t07, anarcho_capitalism t12, farmcarrots t15.

**Base rates of the edited themes**, per reader against my count over the 50: T3-065 2.7 against 3; T3-195 0.3 against 0 (round 2 more); T3-033 2.3 against 2; T3-038 1.7 against 3; T3-002 1.3 against 0; T3-026 0 against 0. No edited theme's rate fell to rare.

**Section 4.** The packets hold 7 to 13 items, too few for a first-ten against last-ten curve. Within packets, agreement with the other two falls from first half to last in 9 of 15 readers and rises in 6 (all six in the two shortest packets). The B3 cap stays at 40 with a 10-item warm-up. 23 dividing items are appended to `exemplar_candidates.jsonl` (68 lines).

### The decision

Round 3's pairwise agreement on the hard set, 0.728, clears the declared threshold of 0.70. By section 5 the rounds stop, and no round 4 opens. This leg writes no scheme edit. The freeze needs, first, the 443 unconfirmed gate pairs read and confirmed and every cluster read for a decide_when_both that names a theme with no discriminator; the T3-002/T3-033/T3-038 cluster is the first to read. That work and the freeze are the next leg's; I asked J whether a fix to the cluster waits for the gold round or gets a round 4 (QB2-012, assumed: rounds stop).

The figure licenses this claim, in FLEET.md's terms: readers holding only the scheme reproduce what I would have produced at a scale one analyst cannot reach, on hard items, at 0.682 fidelity. It does not license the claim that any competent reader would have produced it.

### QB2-013: four bag flags with no also_present

`validate.py B2` reports 4 errors. Four kept lines set `item_is_a_bag` true and leave `also_present` empty: P03-r3-2/r3.jsonl lines 6, 10 and 11 (acecombat t05, n64 t02, Goodboye t03) and P03-r3-2/r6.jsonl line 6 (acecombat t05). Each places one theme validly. Reader r6 says why: the item is a bag, but no other theme has three concepts of its own. The flag and the three-concept floor collide. `fleet.py` accepted the lines. I asked J to waive them by name, as at QB2-009, and whether the return spec should say that a bag with no other theme at the floor is not flagged. Meanwhile round 3 is scored with the four lines as given; the flag enters no figure.
