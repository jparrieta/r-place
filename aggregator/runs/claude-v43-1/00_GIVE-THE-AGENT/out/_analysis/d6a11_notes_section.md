## D6a-11: the form telling, form A (J, 27 October, 06:41 to 06:58 Berlin)

**The close-check report of D6a-10** (`_analysis/d6a10_validate_D6.txt`): 0 errors, 0 warnings; fractal lines 50, branches placed 35 of 35.

**J's instruction, through the handler (the PI's message of 09:25 UTC).** Six legs follow D6b, one per form, A to F (D6a-11 to D6a-16). Each writes the form's telling with a figure of its changes against the global model, with its changes drawn apart by mark. It then picks three representative and rich rooms by a rule stated before any room is read, and shows how the model is instantiated in each, with a figure. The cut (D4a-08c) does not change, and no data file changes.

**The selection rule, logged before any room was read.** The candidates are the form's defining rooms in the nearest quarter of distances to the form's centre (the allocation's columns, as D5 measured it) that lie nearer this form's centre than any other. They are ranked by selected changes, then coded concepts, then distance, and the first three are taken (`_analysis/d6a11_select_rooms.py`). For form A: r/FloydVsVoid (distance 0.690, rank 1 of 135, 26 changes), r/prequelmemes (0.777, rank 13, 25 changes) and r/theexpanse (0.737, rank 5, 24 changes). The rule chose D5's best fit again.

**What was written** (`out/form-telling-D6/`):
- `form-A.md`, `form-A.png`, `form-A.svg` and the graphviz source `form-A.dot`;
- for each room, `room-A-<sub>.md`, `.png`, `.svg` and `.dot`.

Facts are in `_analysis/d6a11_facts_A.json`, from `_analysis/d6a11_form_telling.py`.

**Reading rules used in the telling.**
- **The changes.** Each change is written as op:element at the T3, T4 and dimension of the line's placement; that is where the room's own theme sits, not always the element's dimension.
- **A room's instantiation.** It is read from `_views/rooms-x-elements.tsv`. A unit is carried as stated where the room instantiates it with no change. It is changed where the room has a selected change on it, the current shared lines with a full lift that the forms were cut from. A change line in the ledger view that is not selected is drawn apart and not counted.
- **The signature.** The form's change signature is the allocation's (`room-forms-D4a08c.jsonl`); a count from the lines does not reproduce its columns.
- **The A1 tellings.** Each room's A1 telling (`package/<sub>/case.md`) is cited for moments, not redone. Every quotation was checked against it by script.

**What the marks do to form A.** None of its 11 changed cells survives the stricter thresholds. Four are size-dependent (C01, P23, P07, P12), and seven are marginal and survive size matching. The form is a lean of the population toward the terms and the plan kept current, not a set-apart type. Each of the three rooms shows four or five of the form's eleven changes. r/prequelmemes and r/theexpanse carry the form's border terms as stated.

**Licences exercised at D6a-11.**
- The selection rule's quarter and its ranking are mine, stated before the run.
- The ledger view's changes outside the selected set are drawn apart rather than dropped.
- The figures add, to the C5 drawing, only the elements a form or room changes.

**Slips at D6a-11.**
- The first signature, counted from the lines, did not reproduce the allocation's and was replaced by the allocation's own.
- The first list of units carried as stated required an exact match and missed units with other ledger marks; it was corrected to match the figures.
- A diary line said the prose check read 0 before it was rerun on the corrected file; the rerun read 0.
