# Audit, section 5: versioned judgments, side by side (E1d)

Written at E1d, 28 October 2026. The figures come from `audit-E1/versioned_judgments.py`, with its rule in its docstring and its output beside it. `audit-E1/reconstruction_tables.py` prints the table.

## 1. The four judgments and their versions

- **The original fixed-global verdict**, from `verdicts-D.jsonl`: the first return, served at pass 15 (model e15f9647…), ruled where the readers split. Over the population: composes 201, composes with residue 489, cannot tell 14, does not compose 1 (section 3).
- **The fixed-global verdict at the re-check**, at the frozen model 46384686…: 630, 56, 19 and 0.
- **The current adapted-local status**, from the effective return manifest (`adaptation-returns.jsonl`, read through `tools/adaptation_ledger.py`). Every one of the 705 rooms has phase recheck, model 46384686…, local status unresolved and grade composes-with-residue. The status is the same in every room, so it cannot set one room against another. Local validation is not established.
- **Shared-branch adequacy**, from `branches-D5.jsonl`: 33 of the 35 branches have shared status unresolved, and F09 and F32 have supported. Every branch line names the global model e15f9647… and the local model 46384686…. Neither supported branch is in the sample.
- **The reconstruction**: fidelity and unresolved claims (section 4), at 46384686…, the version every reader's summary states.

| room | branch | fixed-global, first return | fixed-global, re-check | adapted-local status / grade | shared-branch status | fidelity | unresolved claims |
|---|---|---|---|---|---|---|---|
| picturegame | F25 | does-not-compose | composes-with-residue | unresolved / composes-with-residue | unresolved | 0.680 | 0 |
| sakartvelo | none | cannot-tell | composes | unresolved / composes-with-residue | no branch | 0.789 | 0 |
| quq | none | cannot-tell | composes | unresolved / composes-with-residue | no branch | 0.750 | 1 |
| hunterxhunter | F03 | composes | composes | unresolved / composes-with-residue | unresolved | 0.911 | 0 |
| ethoslab | F01 | composes | composes | unresolved / composes-with-residue | unresolved | 0.932 | 0 |
| python | F26 | composes | composes-with-residue | unresolved / composes-with-residue | unresolved | 0.822 | 1 |
| kirby | F18 | composes | composes | unresolved / composes-with-residue | unresolved | 0.939 | 0 |
| ucf | F15 | composes | composes | unresolved / composes-with-residue | unresolved | 0.896 | 2 |
| penguins | F34 | composes | composes | unresolved / composes-with-residue | unresolved | 0.862 | 0 |
| ReBoot | none | composes | cannot-tell | unresolved / composes-with-residue | no branch | 0.975 | 0 |
| sonicthehedgehog | none | composes | composes | unresolved / composes-with-residue | no branch | 0.948 | 0 |
| mamamoo | F35 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.843 | 0 |
| superman | F33 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.927 | 0 |
| physical_removal | F23 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.930 | 1 |
| thenetherlands | F02 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.971 | 0 |
| tagpro | F29 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.906 | 0 |
| gameboy | none | composes-with-residue | composes | unresolved / composes-with-residue | no branch | 0.797 | 0 |
| necrodancer | F28 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.917 | 0 |
| simonfraser | F30 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.637 | 0 |
| Goodboye | none | composes-with-residue | composes | unresolved / composes-with-residue | no branch | 0.910 | 0 |
| Madeon | none | composes-with-residue | composes-with-residue | unresolved / composes-with-residue | no branch | 0.662 | 0 |
| dwarffortress | F16 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.910 | 0 |
| TeamYellowPlace | none | composes-with-residue | composes | unresolved / composes-with-residue | no branch | 0.906 | 0 |
| hyperlightdrifter | F24 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.940 | 0 |
| puzzleanddragons | F07 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.959 | 1 |
| seolhyun | F10 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.925 | 0 |
| pansexual | none | composes-with-residue | composes | unresolved / composes-with-residue | no branch | 0.942 | 0 |
| PinkUnion | none | composes-with-residue | composes | unresolved / composes-with-residue | no branch | 0.921 | 1 |
| mls | F06 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.891 | 8 |
| slovenia | F08 | composes-with-residue | composes | unresolved / composes-with-residue | unresolved | 0.735 | 0 |

## 2. Where the judgments disagree

- **The rule**, written before the run: a room disagrees where its first-return and re-check verdicts differ, or where it composes at the first return with fidelity below the thirty's median (0.910), or cannot be told or does not compose with fidelity at or above it. The manifest and the branch status mark no room, since they are the same across the sample, and the rule does not use them.
- **25 of the 30 disagree.** 23 changed verdict at the re-check: 18 from composes-with-residue to composes, 2 from cannot-tell to composes, and one each from does-not-compose to composes-with-residue (picturegame), from composes to composes-with-residue (python) and from composes to cannot-tell (ReBoot). ucf and penguins compose with fidelity below the median, and so does python.
- ReBoot, which the re-check could not tell, has the highest fidelity of the thirty, 0.975 over 20 claims. It is outside the seeded sample and was not examined.

## 3. The seeded sample, examined with the case evidence

The seeded five are sakartvelo, picturegame, Goodboye, dwarffortress and necrodancer. In all five the verdict changed at the re-check. For each I read the verdict lines at both returns, and the case account and the skeleton in its packet.

- **sakartvelo** (no branch; cannot-tell, then composes; 0.789). Both first readers could not tell: the room holds 5 concepts, below the floor of 10. At the re-check, one reader found it composing under P27 and P31, the candidates for choosing where to start and for arguing over an occupied spot, and one still could not tell; I ruled that it composes. The case account describes a late, small exchange over where to start a Georgian flag. The skeleton accounts for 13 of its 19 claims, and half the fidelity lost is evidence: P04 and P12 are not testable in the room. **Both judgments hold.** The revised model states what the room did, and the record shows little. The verdict moved with the model, which gained two candidates, not with new evidence about the room. The concept count explains why the first return could not tell. It does not say whether the model fits.
- **picturegame** (F25; does-not-compose, then composes-with-residue; 0.680). Both first readers found a room whose themes are a game of sound rounds, picture hints and emoji proposals, not a canvas mark. Both re-check readers found it composing with residue under K01, P23 and P24, with the sound round and the emoji proposals as the residue. The case account says that the room's sustained conduct was its own April Fools round and its ordinary numbered relay, and that the canvas appears in one emoji proposal. Of its 24 lines read, 8 are the relay and 4 are which layer carried the proposal. **The reconstruction agrees with the first return in substance**: the skeleton holds the room's few canvas acts and not its main business. The change of verdict follows the model's wider frame and its candidates, not more organizing for the canvas.
- **Goodboye** (no branch; composes-with-residue, then composes; 0.910). Both first readers named residue: a guest asking the host's permission to build above its mark, and the mark bringing newcomers back; one added a leader's commands. Both re-check readers found it composing, and named no element for that residue. The skeleton accounts for 69 of 78 claims. Its 5 no lines are two gaps, two orders and ordinary dog sharing, all particulars. **The re-check and the reconstruction agree.**
- **dwarffortress** (F16; composes-with-residue, then composes; 0.910). The readers split at both returns. At the first, I ruled residue: decisions taken in a chat, and canvas events turned into the game's stories. At the re-check, one reader kept the chat as residue because P23 is a candidate with no arrows, and I ruled that it composes, since P23 states the chat. The reconstruction reader scored all 6 claims it placed on P23 as accounted. Its 6 no lines are ordinary game talk (3), P10 not testable (2) and a visitor from another room (1). **The reconstruction agrees with the ruling.** The readers' split is over whether a candidate without arrows composes.
- **necrodancer** (F28; composes-with-residue, then composes; 0.917). The readers split at both returns. At the re-check I ruled that the residue of my first ruling, a visitor answered and editing sent to a chat, is now P25 and P23, and that the move ahead of a neighbour's announced taskbar is P27. The one no line of the reconstruction is the answer to a visitor's criticism of the game's music (claim 26). The room's line on P25 holds a member explaining the game's genre to a passer-by [necrodancer/c0069], not that answer. **The judgments differ in grain.** My ruling read the theme t08 as P25 and named c0067. The reconstruction reads the claim, and the room's line on P25 cites another concept.

**What the five show.** In all five the verdict moved with the model at D3, as candidates entered, and not with new evidence about the room. The reconstruction agrees with the re-check where the room's record is mostly its work for the canvas (Goodboye, dwarffortress and necrodancer, 0.910 to 0.917). It agrees with the first return's doubt where the record is small or lies mostly off the canvas (sakartvelo and picturegame).

## 4. What this part cannot say

- Room by room, whether the local adaptations hold. The adapted-local status is the same in all 705 rooms, so it says nothing about any one of them.
- Whether a shared branch is adequate for its sampled room. Every sampled branch is unresolved.
- Why the 20 disagreeing rooms outside the seeded five disagree. I did not examine them.
