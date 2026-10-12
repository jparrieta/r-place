
## Leg B2b-r3-p3, the freeze, 2026-10-12

J ruled at QB2-012 (13:47 Berlin) that no round 4 runs. The handler made this leg the freeze leg itself (12:25Z). It has four tasks: read the T3-002/T3-033/T3-038 cluster, make any sentence fix the reading calls for, confirm the gate pairs on edited themes, and freeze. A fix made here is tested only by the gold round in B2c.

### The cluster read

Round 3's readers split on three items. On signal t01 the three readers chose T3-033, T3-038 and T3-002. On n64 t02 they chose T3-002 with T3-070, T3-002 alone, and T3-038. On 2007scape t04 one reader chose T3-070 and two chose T3-038. I read each item whole:
- **signal t01** holds one opening question (c0001, "Anyone else interested in getting /r/signal onto /r/place?") and two concepts that place and report the work (c0002 drawing at a location, c0003 "We did it!").
- **n64 t02** holds one opening call to unite (c0010) and three concepts that build and report the logo (c0011 the image imitated, c0012 started at stated coordinates, c0014 the finished logo).

The readers who left T3-038 took the opening post as "the lead". The three pairs of the cluster used three different measures. T3-002 against T3-033 used "the lead". T3-038's decide_when_both used "the larger part". T3-033 against T3-038 used "the side with more concepts". None covered an item holding all three acts.

**The fix** (`out/_analysis/b2_edits_freeze.py`, scheme_edits 296 to 302, scheme-ambiguous, caused_by signal t01, n64 t02, 2007scape t04):
- **One measure.** The decide_when_both of T3-002, T3-033 and T3-038 now carry one rule. Count the concepts of each act. The act with the most concepts of its own is primary. The opening post does not lead because it comes first. On a tie, T3-038 wins when the work was placed. Otherwise T3-002 wins when the mark was already chosen, and T3-033 when it was not.
- **The three pair questions** are now set word for word the same in both gates, with this count.
- **A new T3-038/T3-070 question.** T3-038 and T3-070 had no question between them. On 2007scape t04 one reader placed T3-070 where two placed T3-038. On n64 t02 one reader added T3-070 for the link to the finished logo.

No theme was narrowed. Each theme keeps its members, and the edits only order the cluster.

**Rechecks** (`b2_rechecks_freeze.py`): 129 records over 44 items, and none moves. I read whole every item that holds two of the cluster's acts, or coordinates beside a report. The next table lists their counts.

| item | file | concepts by act | placement |
|---|---|---|---|
| 2007scape t04 | author | 349 concepts: about 44 build or report, 35 call, 23 give directions, 13 propose | T3-038 stays |
| signal t01 | author | 2 build or report, 1 opening question | T3-038 stays |
| n64 t02 | author | 2 build (c0011, c0012), 1 call (c0010) | T3-038 stays |
| Villanova t01 | gold | 3 build or report, 2 calls | T3-038 stays |
| roosterteeth t03 | gold | 7 build or report, no call | T3-038 stays |
| cloud9 t12 | gold | 1 call, 1 failed attempt; a tie, nothing placed | T3-002 stays |
| edboxes t02, mindcrack t03 | gold | calls lead | T3-002 stays |
| dankmemes t10, dofus t01, kpop t04 | gold, author, author | proposals lead | T3-033 stays |
| GabrielDropout t03 | gold | 4 directions, 2 reports; the closest | T3-070 stays |
| predators t04, england t03, furry t10 | gold, author, author | directions lead | T3-070 stays |

On furry t10, c0034 ("working on it at (965, 759)") is now a report of where the work stands, and it leaves T3-070's support.

### The gate pairs read

`out/_analysis/b2_pairs_dump.py` wrote each unconfirmed pair on an edited theme side by side to `out/_analysis/b2_pairs_read_first.txt`. There were 449 pairs:
- 253 carry one question, the same in both gates;
- 169 carry two wordings of a question;
- 27 carry no question, and one gate's decide_when_both or is_not settles them.

I read all 449, to the end marker. Two faults were found.
- **T3-009 against T3-072 and T3-157.** T3-009's decide_when_both makes the thanks to allies (T3-072) or the reflection on working together (T3-157) primary when it holds more concepts than the celebrating, as T3-043's does. T3-072 and T3-157 each said "T3-009 primary" with no condition, so the gates of each pair contradicted each other.
- **T3-038 against T3-070.** My new question sent "where to see it" and a link to the finished work to T3-038. T3-026's must_show already takes "others pointed to where it is". I found this reading the T3-026/T3-038 pair.

**The fixes** (`out/_analysis/b2_edits_freeze2.py`, scheme_edits 303 to 306):
- T3-072 and T3-157 now say what T3-009 says: the side with more concepts is primary.
- The T3-038/T3-070 question now keeps T3-038 for work in progress, and points a link that only shows the finished work at T3-026.
- **Rechecks:** 52 records (`b2_rechecks_freeze2.py`), and none moves. The five items on T3-009 were read whole: mcgillrobotics t02, montenegro t04, mordhau t05, redhotchilipeppers t09 and ukraine t07. Each holds more celebrating concepts than thanks to allies or reflection. On redhotchilipeppers t09 the count is six celebrating concepts against one thanking allies. On n64 t02, c0014 and c0015 now point to the finished logo, so T3-038's support is c0011 and c0012.
- `rechecks-B2.jsonl` holds 1,594 records, none missing.

**Confirmed.** The fixes changed six themes from the round-3 scheme (kept as `out/_analysis/scheme_round3.jsonl` and `.md`): T3-002, T3-033, T3-038, T3-070, T3-072 and T3-157. After them, 450 pairs touched an edited theme.
- I read again the 11 pairs the second fixes touched, and read the one new pair (T3-157/T3-164) for the first time (`b2_pairs_new.py`).
- I confirmed all 450 (`b2_confirm_freeze.py`). Each reason quotes the question or clause that decides the pair, and the cluster's pairs and the fixed pairs have reasons of their own.
- I read the 20 pairs on unedited themes (`b2_pairs_read_rest.txt`), and confirmed them too.

`mem.py gates` reports 496 pairs, all 496 confirmed and 0 stale. It finds no one-way question, no must_not_show with no question against its target, and no undefined id.

### The freeze

`out/_analysis/b2_freeze.py` wrote two files. `families.jsonl` (21 families) stands beside them.
- **`scheme_final.jsonl`:** 197 themes, with every field as in `scheme.jsonl`.
- **`scheme_final.md`:** `scheme.md` with a frozen header.

The sentences are those after the 306 lines of `scheme_edits.jsonl`. The sha256 of `scheme_final.jsonl` is fb8b543a98982d36df299d0494773f1bf9ee481b3966331bffc4d299127be595.

**The tier word (QB2-014, open).** The rare tier is marked "tier": "rare" (14 themes). The main tier is marked "tier": "common" (183 themes). The B2 close-check accepts only none, rare, common or core, so "main" would fail it 183 times. The C1 check expects main or rare, and it finds moves to rare by looking for "main" in the frozen file. I asked J which word stands, and whether the handler will make the two checks agree. If J rules "main", I supersede `scheme_final.jsonl` under a new name once the B2 check accepts that word.

**Base rates.** No theme was narrowed at the freeze, so no theme's base rate falls from these edits. The edits change only which act of the cluster is primary when an item holds several. The gold round shows whether T3-002's and T3-033's rates fall against T3-038's.

**The sentence I am least sure a stranger reads as I meant.** It is the cluster's new rule, "count the concepts of each: the act with the most concepts of its own is primary". A reader must sort each concept into one act before counting. On 2007scape t04 that sorting is itself a judgement over 349 concepts.

### The close-check, B2b-r3-p3

`validate.py B2` reported:

```
stage B2:
  leg: check (3 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  _fleet_raw/B2/round-2: 15 readers, 150 return lines, 16 waived by J (return_waivers.jsonl)
  _fleet_raw/B2/round-3: 15 readers, 150 return lines, 4 waived by J (return_waivers.jsonl)
  author items 50, gold items 40, rounds scored 3, edits 306 (author-error 4), scheme ids 197 (scheme_final.jsonl), frozen


0 errors (0 distinct shapes), 0 warnings
```

The leg closes with `done.sh B2`. B2c builds the gold round and the two stability rounds on the frozen scheme.
