## D6a-12: the form telling, form B

**The close-check report of D6a-11** (`_analysis/d6a11_validate_D6.txt`): 0 errors, 0 warnings; fractal lines 50, branches placed 35 of 35.

**The selection rule, logged before any room was read** (`_analysis/d6a12_select_B.py`). There is one room per facet, as J asked. A defining room holds a facet where it has a selected change line at the facet's fourth-order theme: the chat T4-010, the scripts T4-009, the raids T4-020. The count reproduces B's account (48, 49 and 40). For each facet, the candidates are the rooms holding that facet alone, at or below the median distance to B's centre (0.9414), and nearer B's centre than any other form's. They are ranked by selected changes, then coded concepts, then distance. No fallback was needed. Chosen:
- the chat, r/dwarffortress (0.859, 24th of 113, 17 changes; 5 candidates);
- the scripts, r/uofm (0.855, 22nd, 12 changes; 6 candidates);
- the raids, r/ockytop (0.870, 29th, 9 changes; the only candidate).

**What was written** (`out/form-telling-D6/`). `form-B.md`, `.png`, `.svg`, `.dot`, and for each room `room-B-<sub>.md`, `.png`, `.svg`, `.dot`. Facts are in `_analysis/d6a12_facts_B.json`, by `_analysis/d6a11_form_telling.py`, unchanged from D6a-11.

**What the marks do to form B.** The chat (P23) and the scripts (P14) are marked "robust" and survive size matching. They are two of the 20 such cells in all six forms. The raids facet's own cell (A15) is marginal. The border cells are marginal (P07, P08) or size-dependent (A05). B is told as a residual grouping held together by two sharp facets.

**What the rooms show.**
- r/dwarffortress shows one of B's seven changes (P23).
- r/uofm shows two (P14, A05).
- r/ockytop shows one (A05). It holds the raids through its own lines on attack calls and hosting, and carries B's raids cell (A15) as the model states it.

Each room holds its facet and little else of B. That is what a grouping whose facets sit at chance overlap would lead one to expect.

**Licences exercised at D6a-12.**
- The facet-only condition and the nearer half (rather than the quarter used for A) are mine, stated before the run. Each facet is a part of the form, and B's centre is a mixture of the three.

**Slips at D6a-12.**
- One command held a no-op (`sleep 0`) beside a listing; it did nothing, and it should not have been written.
- One drafted list of units carried as stated included attack calls (P09), which the room changes; it was removed before the check.
