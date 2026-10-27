# Audit, section 4: the reconstruction sample (E1c, E1d)

Written at E1d, 28 October 2026. The figures come from `audit-E1/reconstruction_validate.py`, `audit-E1/reconstruction_causes.py` and `audit-E1/reconstruction_tables.py`, each with its rule in its docstring and its output beside it. The return, one line per room, is `reconstruction-E1.jsonl`.

## 1. The build and the dispatch

- **The sample (E1c).** Thirty rooms were drawn by seed from the ledgers before any was opened (`audit-E1/reconstruction_draw.py`; `reconstruction-sample-E1.jsonl`). By the first return's ruled verdict: does-not-compose 1, cannot-tell 2, composes 8, composes-with-residue 19. They fall in 20 branches, one room each, and 10 rooms sit in no branch. `notes-E1.md` names them.
- **The packets.** Each holds the skeleton from `rebuild.py` at the frozen model 46384686…, the coder's `case.md` and the room's second-order themes. They run from 29,610 to 47,848 bytes. `RETURN-E1.md` asks the reader to score each claim of `case.md` as accounted yes, partly, no or unresolved, with the element or arrow id.
- **The dispatch**, outside my session, ran from 22:29Z to 22:40Z on 27 October. One reader per room, deepseek/deepseek-v4.1-flash called directly, cost 1.728235 USD for 916,006 input and 2,267,673 output tokens (`_fleet_raw/E1/DONE`).
- **The defect that stopped it.** fleet.py judged 0 returns valid and all 30 rooms exhausted after three attempts each. Every packet ends by asking the reader to return its lines "and then the end marker the return specification names". `RETURN-E1.md`, which I wrote at E1c, names no marker. So each reader ended with a marker of its own: END OF PACKET in 22 rooms, END OF RETURN in 6, and two other forms in 1 room each. That last line is not JSON, and fleet.py rejected the whole return (`defects.jsonl` line 121). At the PI's instruction there was no re-dispatch.

## 2. The returns validated

- **The rule**, written before the run: for each room, the newest raw file; one final line that is not JSON is dropped and recorded; any other line that is not JSON makes the return invalid; the claim lines carry the room and one of the four values; the summary's counts equal the claim lines.
- **The result.** In all 30 rooms the newest raw file is the third attempt, by modification time and by attempt number alike. Its one final line is a marker, and it was dropped. Every other line parses. The summary's counts equal the claim lines in all 30, and every summary states the model 46384686d617.
- **25 rooms are valid under the rule as first written.** The readers of picturegame, python, ReBoot, tagpro and Madeon wrote the room as "r/" with its name on every line. The packets name each room that way, and `RETURN-E1.md` does not say which form it wants (`defects.jsonl` line 122). An amendment made after the first run, and dated in the script, reads that form as the room. Under it, all 30 are valid. The first output is kept (`reconstruction_validate.superseded-1.json`), and both counts are reported.

## 3. Fidelity, by verdict and by branch

Fidelity, as `RETURN-E1.md` defines it, is yes plus half of partly, over yes, partly and no. Unresolved claims are reported apart and are never failures. A no whose reason begins "contradicts" is counted as contradicted.

**Fidelity by verdict** (the first return's ruled fixed-global verdict, model e15f9647…)

| verdict | rooms | mean fidelity | claims | yes | partly | no | unresolved | contradicted |
|---|---|---|---|---|---|---|---|---|
| composes | 8 | 0.911 | 537 | 474 | 29 | 31 | 3 | 0 |
| composes-with-residue | 19 | 0.875 | 1,161 | 965 | 112 | 73 | 11 | 0 |
| cannot-tell | 2 | 0.770 | 40 | 25 | 10 | 4 | 1 | 0 |
| does-not-compose | 1 | 0.680 | 50 | 26 | 16 | 8 | 0 | 0 |
| all | 30 | 0.871 | 1,788 | 1,490 | 167 | 116 | 15 | 0 |

- The mean is 0.871 over the 30 rooms, and 0.884 over the 25 valid under the first rule. The range is 0.637 (simonfraser) to 0.975 (ReBoot), and the median is 0.910.
- **No claim is contradicted.** 15 of 1,788 claims are unresolved, 8 of them in mls.
- By the first return's verdict, mean fidelity falls in the verdicts' own order, from 0.911 (composes) to 0.680 (does-not-compose). The two lower strata hold 2 rooms and 1, so this is an observation, not a test.

**Fidelity by branch** (the room's most specific branch; each sampled branch holds one room)

| branch | room | verdict | fidelity | claims | yes | partly | no | unresolved |
|---|---|---|---|---|---|---|---|---|
| F01 | ethoslab | composes | 0.932 | 81 | 74 | 3 | 4 | 0 |
| F02 | thenetherlands | composes-with-residue | 0.971 | 70 | 67 | 2 | 1 | 0 |
| F03 | hunterxhunter | composes | 0.911 | 45 | 38 | 6 | 1 | 0 |
| F06 | mls | composes-with-residue | 0.891 | 86 | 68 | 3 | 7 | 8 |
| F07 | puzzleanddragons | composes-with-residue | 0.959 | 62 | 57 | 3 | 1 | 1 |
| F08 | slovenia | composes-with-residue | 0.735 | 49 | 25 | 22 | 2 | 0 |
| F10 | seolhyun | composes-with-residue | 0.925 | 40 | 35 | 4 | 1 | 0 |
| F15 | ucf | composes | 0.896 | 74 | 64 | 1 | 7 | 2 |
| F16 | dwarffortress | composes-with-residue | 0.910 | 78 | 70 | 2 | 6 | 0 |
| F18 | kirby | composes | 0.939 | 107 | 98 | 5 | 4 | 0 |
| F23 | physical_removal | composes-with-residue | 0.930 | 72 | 64 | 4 | 3 | 1 |
| F24 | hyperlightdrifter | composes-with-residue | 0.940 | 92 | 86 | 1 | 5 | 0 |
| F25 | picturegame | does-not-compose | 0.680 | 50 | 26 | 16 | 8 | 0 |
| F26 | python | composes | 0.822 | 46 | 33 | 8 | 4 | 1 |
| F28 | necrodancer | composes-with-residue | 0.917 | 42 | 36 | 5 | 1 | 0 |
| F29 | tagpro | composes-with-residue | 0.906 | 53 | 45 | 6 | 2 | 0 |
| F30 | simonfraser | composes-with-residue | 0.637 | 51 | 19 | 27 | 5 | 0 |
| F33 | superman | composes-with-residue | 0.927 | 55 | 51 | 0 | 4 | 0 |
| F34 | penguins | composes | 0.862 | 58 | 48 | 4 | 6 | 0 |
| F35 | mamamoo | composes-with-residue | 0.843 | 51 | 42 | 2 | 7 | 0 |
| none | gameboy | composes-with-residue | 0.797 | 37 | 27 | 5 | 5 | 0 |
| none | Goodboye | composes-with-residue | 0.910 | 78 | 69 | 4 | 5 | 0 |
| none | Madeon | composes-with-residue | 0.662 | 40 | 25 | 3 | 12 | 0 |
| none | pansexual | composes-with-residue | 0.942 | 77 | 72 | 1 | 4 | 0 |
| none | PinkUnion | composes-with-residue | 0.921 | 64 | 55 | 6 | 2 | 1 |
| none | quq | cannot-tell | 0.750 | 21 | 12 | 6 | 2 | 1 |
| none | ReBoot | composes | 0.975 | 20 | 19 | 1 | 0 | 0 |
| none | sakartvelo | cannot-tell | 0.789 | 19 | 13 | 4 | 2 | 0 |
| none | sonicthehedgehog | composes | 0.948 | 106 | 100 | 1 | 5 | 0 |
| none | TeamYellowPlace | composes-with-residue | 0.906 | 64 | 52 | 12 | 0 | 0 |
| none, together | 10 rooms | | 0.860 (mean) | 526 | 444 | 43 | 37 | 2 |

- Each sampled branch holds one room, so a branch's figure is one room's. F30 (simonfraser) is the lowest and F02 (thenetherlands) the highest. The 10 rooms in no branch average 0.860.

**What the figure licenses.** Like the fleet figures of FLEET.md section 2, fidelity bounds whether the written skeleton decides a reader's scoring, not whether the skeleton is right. Each room had one reader, an instance of one model. The test is in-sample: the skeleton was built from the room's own return lines, and the packet held the room's own themes. SCHEMA-adaptations.md section 8 calls it "an in-sample preservation and composition check, not independent truth estimation".

## 4. The causes of a low score, separated

- **The rule**, written before any line was read (`audit-E1/reconstruction_causes.py`). A low score is fidelity below 0.8. That takes 7 rooms: simonfraser, Madeon, picturegame, slovenia, quq, sakartvelo and gameboy. I read every no, partly and unresolved line in them (120), and every no line in the other 23 rooms (80), so that a cause found in the low rooms can be set beside the rest. I gave each line one cause, from the claim, the reader's reason, the packet's skeleton and the room's themes (`audit-E1/reconstruction_causes.tsv`). After the first page, and before any cause was written, I wrote down how two of the causes would be read; the script's docstring holds it.
- **The causes.** *Unsupported*: the coder's claim goes past the room's record. *Evidence*: the record cannot show it, or the skeleton's line on it is absent or not testable. *Particular*: a fact of the room that the coder's account states and no skeleton line carries. *Shared*: the model's element does not hold what the room did, or the model has no element for a kind of act that is not one room's alone. *Reader*: the reader's no or partly is mistaken, or the line is not a claim of the account.

| cause | the 7 rooms below 0.8 (no, partly, unresolved) | the other 23 rooms (no lines) | all |
|---|---|---|---|
| particular | 102 | 65 | 167 |
| evidence | 7 | 6 | 13 |
| reader | 10 | 2 | 12 |
| shared | 0 | 7 | 7 |
| unresolved | 1 | 0 | 1 |
| unsupported | 0 | 0 | 0 |
| all | 120 | 80 | 200 |

Inside particular: detail 44; off the canvas 42; a room named 23; an interval 19; an order 15; a layer 12; the coder's synthesis 6; a line the room proposed 6.

**Fidelity lost in each room below 0.8, by cause** (a no line costs 1 and a partly line 0.5, over yes, partly and no)

| room | fidelity | particular | evidence | reader | unresolved |
|---|---|---|---|---|---|
| simonfraser | 0.637 | 0.353 | 0.010 | 0.000 | 0.000 |
| Madeon | 0.662 | 0.225 | 0.000 | 0.112 | 0.000 |
| picturegame | 0.680 | 0.280 | 0.000 | 0.040 | 0.000 |
| slovenia | 0.735 | 0.265 | 0.000 | 0.000 | 0.000 |
| quq | 0.750 | 0.200 | 0.025 | 0.025 | 0.000 |
| sakartvelo | 0.789 | 0.079 | 0.105 | 0.026 | 0.000 |
| gameboy | 0.797 | 0.176 | 0.027 | 0.000 | 0.000 |

**What each cause holds.**
- **Particulars, 167 of the 200 lines.** The skeleton carries acts by element. It does not carry the room's other business, its counterparts by name, its clock, or the layer that carried an act.
  - *Off the canvas* (42): the room's ordinary traffic before, beside and after the event. Examples are picturegame's numbered game relay, ucf's campus questions, Madeon's trade in concert recordings and gameboy's hardware talk. The coder's account covers the room's whole window; the model covers its organizing for the canvas.
  - *Details, rooms named, intervals, orders and layers*: a counterpart named, a gap the coder measured to the second, which of two threads came first, and whether posts or comments carried an act. simonfraser and slovenia lose most of their fidelity here.
  - *Synthesis and proposed lines*: the coder's reading of the room as a whole, and lines the room proposed at the return that the model did not take, such as Madeon's real concert recordings.
- **Evidence, 13 lines.** The skeleton's line on the act is absent or not testable in the room (P04, P10, P12, P23, P27, P28, P32 and P33, and the arrow A17). In sakartvelo, a room with 5 concepts, evidence carries 0.105 of the 0.211 the room lost.
- **Reader, 12 lines.** None is a fault of the skeleton. The readers of Madeon and quq scored the room's theme list as claims (5 lines). Other readers scored sentences about the coder's evidence, which `RETURN-E1.md` says are not claims (7 lines).
- **Shared, 7 lines: two facts in two rooms.** In mamamoo, members placed pixels at random, without a plan (4 lines of one fact), and the model has no element for placing that organizes nothing. In hyperlightdrifter, a member warned that a rival might attack (3 lines of one fact); P05 holds watching and defence under attack, not the warning. Each is a kind of act, not one room's alone, and so a candidate for a shared change. Neither was tested beyond its room.
- **Unsupported, none found.** I took the coder's claims as the packet gives them and did not test them against the raw record. That test is section 1's: the handler's check found 0.6573 of the case accounts' quoted strings in the room's corpus. Three of the thirty were in its sample (ethoslab, PinkUnion and tagpro), and every quoted string of their accounts was found (15, 13 and 7).

**So no low score here is a failure of the global model.** The low scores come from what the skeleton is not built to carry, from particulars the return did not record, from evidence the record lacks, and from readers who scored lines that are not claims. 7 of the 200 lines point at the shared account, and no line contradicts it.

## 5. What this part cannot say

- Whether a second reader, or a reader of another model, would score the same. Each room had one reader.
- Anything out of sample.
- The causes of the 84 partly lines in the 23 rooms at or above 0.8. I did not read them.
- A branch's fidelity beyond its one sampled room.
- Whether anyone else would give the same causes. They are one analyst's reading, and nobody checked it.
