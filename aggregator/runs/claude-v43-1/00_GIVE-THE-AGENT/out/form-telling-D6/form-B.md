# Form B, Behind the thread: chat, scripts, raids: the form's telling

Written at D6a-12, on J's instruction (27 October, 06:41 to 06:58 Berlin, through the handler). The form is form B of the D4a-08c cut, which does not change. It has 141 rooms, 113 of them defining. The figure is `form-B.png` (and `form-B.svg`). The counts come from `fractal-forms-D6.jsonl`, `form-cells-sensitivity-D6.tsv`, `form-cells-size-D6.tsv`, the allocation file `room-forms-D4a08c.jsonl`, the D5 lines of the form's defining rooms and `_analysis/d6a09_b_facets.json`; `_analysis/d6a11_form_telling.py` reads them. Local validation is not established: each room shows a pattern in its ruled lines, not in a validated account of the room.

**How a change is written here.** A change is an op on a unit of the model: an element or an arrow. The op is add-step, add-condition, link or restrict. The change is placed at the third-order theme (T3) where the room's own theme sits, and so at a fourth-order theme (T4) and a dimension. The T3 and T4 given for each change are the most common placements of the form's lines for it.

## What B is: a residual grouping with three facets

B is not one shared change. Its account and the correction of D6a-09 call it a residual grouping. Its defining rooms change one or more of three fourth-order themes, the three facets:
- **the scripts:** Workarounds (T4-009, Coordination without command), held by 49 of the 113;
- **the chat:** Backstage decision-making (T4-010, Coordination without command), held by 48;
- **the raids:** Repertoire of contention (T4-020, Contention), held by 40.

Different rooms hold them at about chance overlap:
- 19 rooms hold only the scripts, 22 only the chat and 15 only the raids;
- 30 hold two facets;
- 7 hold all three, against 7.4 if the facets were independent;
- 20 hold none.

43 of its 113 defining rooms lie nearer another form's centre, the most of any form.

**The change signature.** The allocation's columns give the same three themes:
- Workarounds, changed by 43 per cent of the defining rooms, 2.06 times the population;
- Backstage decision-making, 43 per cent, 2.29 times;
- Repertoire of contention, 35 per cent, 2.35 times.

## The changed cells, along the model's course

Read against the 66 elements and arrows by the rule of D6a-01, the form changes seven units.

- **The call turned on a rival.** A15, P01 to P09 (a call's hands can turn on a rival), is restricted in 18 defining rooms (1.39 times the share), most often at T3-006, calling to deface rivals' work (T4-020 Repertoire of contention, D08). The record does not show a call's builders turning on a rival. In some rooms the attack call is the first call or shares the opening turn with recruiting; in others the lines show the order of calls but not that the same hands attacked.
- **The chat.** P23 is specified by add-step and add-condition in 20 rooms (1.83), at T3-014, moving planning into a chat (T4-010 Backstage decision-making, D02). The chat works on conditions: invitations that work, and a current plan that members outside the chat can find.
- **The scripts.** P14 is specified by add-step in 33 rooms (2.09), at T3-028, running scripts for the work (T4-009 Workarounds, D02). Scripts are run as shared tools, and their targets and versions are kept in step.
- **The neighbours.**
  - P07, sparing, is specified by add-condition and link in 15 rooms (1.35), at T3-024 (refusing to cover others' work) and T3-006 (T4-015 Live and let live, D04). Sparing passes through the room's tools: an instruction to spare agreed space must reach script users as an update to their target.
  - P08, border terms, is specified by add-step in 18 rooms (1.31), at T3-010 (settling borders) and T3-149 (agreeing truces with rival rooms) (T4-016 Negotiated order, D04). Members ask for a treaty before any damage, seek consensus before a proposal and relay a negotiated move to builders.
  - A05, P08 to P07 (a settled border is a line members keep), is specified by add-condition in 16 rooms (1.39), mostly at T3-149 (T4-016, D04). A settled border is kept where its terms reach the placers and the scripts' targets.
- **Stepping away.** P32, members stepping away under strain, is restricted in 12 rooms (2.04), at T3-087 (tracing who changed the work) and T3-190 (splitting a faction over doctrine). Where a member left, the reason given was the room's scripts or a doctrine, not strain.

**How the changes follow one another.** B's rooms start, call and build as the model says. They leave R01, P01, P03, A01, A02 and A03 untouched at the form level. The changes come where the work runs behind the thread. A call may already be a call to attack (A15). The plan and the terms go to the placers through the chat (P23) and to the machines through the scripts (P14). The terms with neighbours then hold only where they reach both (P07, A05), with the treaty prepared and relayed (P08). Members who leave give the tools or a doctrine as their reason (P32). Each facet's rooms do their part apart from the others'. So the form is three courses through the same model, not one course with three steps.

## What the marks do to the form's claim

- **Marked "robust": 2.** The chat (P23) and the scripts (P14) keep their relation at ratio 1.5 and floor 15 per cent, and both survive the size-held test.
- **Marginal: 4.** P32, P07, P08 and A15 lean only at the rule's thresholds and survive size matching.
- **Size-dependent: 1.** A05 fails when matched on canvas-work concepts (1.14).

So B's claim rests on two facets. The chat and the scripts are among the sharpest changes of any form: of the 20 cells that survive the stricter rule, these are two. The raids facet's own cell, the call turned on a rival (A15), is marginal, and the restrictions behind it mostly say what the record cannot show. The border cells (P07, P08, A05) are where the chat and the scripts meet the neighbours, and they are marginal or size-dependent. B is best read as a residual grouping held together by two sharp facets, the chat and the scripts, with a third, the raids, that leans only weakly. Its lead after the close is a property of its chat and script rooms: 26 of the 35 rooms that coordinated after hour 73 hold the chat or the scripts.

## The figure

`form-B.png` draws the stage C5 model with form B's changes, its added units (P23 and P32) among the mediators:
- "robust": solid border, dark orange (P14, P23);
- "marginal": dashed border, light orange (P07, P08, P32, and the arrow A15);
- "size-dependent": dotted, grey-blue (the arrow A05).

The legend gives the change signature.

## Three rooms, one per facet

**The selection rule, logged in the diary before any room was read** (`_analysis/d6a12_select_B.py`).
- A defining room holds a facet where it has a selected change line at the facet's fourth-order theme.
- For each facet, the candidates are the rooms that hold that facet alone, within the nearer half of B's defining distances to its centre (at or below 0.9414, the median), and nearer B's centre than any other form's.
- They are ranked by selected changes, then coded concepts, then distance, and the first is taken.
- No fallback was needed.

The three rooms:
- **The chat: r/dwarffortress** (`room-B-dwarffortress.md`): distance 0.859, 24th nearest of 113; 17 selected changes; 5 candidates.
- **The scripts: r/uofm** (`room-B-uofm.md`): distance 0.855, 22nd nearest; 12 selected changes; 6 candidates.
- **The raids: r/ockytop** (`room-B-ockytop.md`): distance 0.870, 29th nearest; 9 selected changes; the only candidate.

The form's defining median is 10 changes. The raids facet's room is the poorest of the three, because few rooms hold the raids alone near the centre.
