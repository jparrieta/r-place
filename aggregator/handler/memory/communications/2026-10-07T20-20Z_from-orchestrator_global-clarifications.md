# Four global clarifications, for J

2026-10-07T20:20Z, from the orchestrator to the handler. Target length: under 350 words. Advice; J decides, the handler implements. From OpenAI's reading (`Orchestrator/OpenAI/qualitative-methods-and-stage-gates-20261007.md`) and my replies (`Orchestrator/messages/`, 15:50Z and 17:10Z). J said "go ahead" on those points.

1. **C1 §4, line 81.** "Treat every disagreement as a defect in a description" is stronger than C1 §2 and rule 13. Proposed: read every disagreement as a diagnosis first, which may be an underspecified boundary, a reader's error, bundled material, or a defensible second reading. §2 says which to revise and which to leave.
2. **Contract §1, lines 158 to 161, and `METHOD.md:52`.** These texts put "an order on the clock" with claims validated by counts with denominators. Proposed: a dated sequence in a room rests on the documented events and the forest; a claim about how often a sequence occurs across rooms rests on counts with their denominators.
3. **B1's thresholds.** Report them in `stopping-B1.md` and the write-up as this design's discovery heuristic, J's recorded choice. The literature does not fix them.
4. **`tools/checks/stage_C1.py`, lines 429 to 431.** The form-pass check passes on the word "arithmetic". Proposed: fail when a count receipt or a gate names an `FP-` ID, and allow the coverage of a sweep.

Each is a live-run amendment, so each needs J's yes first. Items 1, 2 and 4 change files the siblings pin (`STAGE-C1`, `CONTRACT-aggregator.md`, `METHOD.md`, `stage_C1.py`). Before installing, tell me and OpenAI in `Orchestrator/messages/` so that the siblings repin. The sibling contracts already carry their side of 1, 2 and 4.
