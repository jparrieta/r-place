
## D6a-14: the form telling, form D

**The close-check report of D6a-13** (`_analysis/d6a13_validate_D6.txt`): 0 errors, 0 warnings; fractal lines 50, branches placed 35 of 35.

**The selection rule, logged before any room was read** (`_analysis/d6a14_select_D.py`). D keeps splits below it, and its three leaves partition its 96 defining rooms: D.1, keeping with the call (54); D.2.1, the play, carried on (27); D.2.2, the play, kept (15). One room is taken per leaf. The candidates in each leaf are its defining rooms at or below the median distance to D's centre (0.9042), and nearer D's centre than any other form's. They are ranked by selected changes, then coded concepts, then distance. No fallback was needed. Chosen:
- D.1, r/rotmg (0.8231, 8th of 96, 20 changes; 18 candidates);
- D.2.1, r/bindingofisaac (0.8037, 4th, 23 changes; 14 candidates);
- D.2.2, r/romania (0.8987, 45th, 15 changes; 2 candidates).

Each is among the three rooms the form's account names as nearest its own part's centre.

**What was written** (`out/form-telling-D6/`). `form-D.md`, `.png`, `.svg`, `.dot`, and for each room `room-D-<sub>.md`, `.png`, `.svg`, `.dot`. Facts are in `_analysis/d6a14_facts_D.json`, by `_analysis/d6a11_form_telling.py`. Quotations and item ids were checked against the A1 tellings by `_analysis/d6a13_quote_check.py`.

**What the marks do to form D.** Six of its 17 changes are marked "robust":
- the call returning from carrying on and loss (P01);
- keeping shared and checked (P05);
- scripts offered and not shown run (P14);
- the host's room for canvas talk (P20);
- carrying on begun before the close (P13), and the record not waited for (A09).

None is size-dependent, and D is the only form so. The help in the form's name is marginal: A13 is held by 33 rooms but leans only 1.32 times the population. D is told as keeping shared and checked, with help and carrying on as two further patterns held by different rooms.

**What the rooms show.**
- r/rotmg shows six of D's changes (P01, A01, P05, A13, P13, A09). Its keeping runs through loss and moving, which is form F's ground.
- r/bindingofisaac shows eight (P01, A02, A05, A13, K01, A20, P13, A09), the most. It carries keeping as stated.
- r/romania shows four (P14, P19, K01, P13). Six of its 15 changes sit at mistaking friendly work for vandalism, which is form C's ground.

Of the three, only r/rotmg shows form D's sharp keeping change (P05). The rooms of D.2 carry the sub's play (K01) and the rooms of D.1 do not, as the parts would lead one to expect.

**Licences exercised at D6a-14.**
- One room per leaf of D's kept splits, and the nearer half rather than the quarter, are mine, stated before the run, as for form B's facets.

**Slips at D6a-14.**
- One check command used `cut -c` after a helper and was refused by the harness. It was re-run without it.
- Two wordings in r/bindingofisaac's draft went beyond the A1 telling (an order for one quotation, and "no answer" where the telling says neither acceptance nor refusal). They were corrected before the check.
