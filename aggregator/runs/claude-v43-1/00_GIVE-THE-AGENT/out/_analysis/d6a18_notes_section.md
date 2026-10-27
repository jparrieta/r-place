
## D6a-18: the Dutch telling

**The close-check report of D6a-17** (`_analysis/d6a17_validate_D6.txt`): 0 errors, 0 warnings; fractal lines 50, branches placed 35 of 35.

**J's instruction** (27 October, 06:54 and 06:58 Berlin, through the handler). For each of J's fourteen rooms of the Dutch area, show how the global model is instantiated in that room, as in the form telling. Draw one figure per room as in round 2, and write a short note across the fourteen. All of it is in `out/dutch-telling-D6/`, with a `README.md`. The fourteen were not too many for one leg: two were already told (r/norway and r/PlaceNL, round 2, pointed to), and four of the twelve new rooms are thin.

**What was written.** Twelve room tellings: r/cirkeltrek, r/indonesia, r/placehearts, r/mindcrack, r/Goodboye, r/norge, r/czech, r/armenia, r/sweden, r/blackmirror, r/greece and r/thenetherlands. Each has `.md`, `.png`, `.svg` and `.dot`, and the README sets the fourteen side by side.

**What the fourteen show** (`_analysis/d6a18_dutch_info.json`, `d6a18_dutch_matrix.json`).
- **Forms:** six of the rooms are in A, five in B, and one each in C, D and E.
- **Typicality:**
  - only r/PlaceNL shows more than half of its form's changed cells;
  - four rooms show none;
  - several lie on their form's edge or nearer another form's centre.
- **Held as stated:** all fourteen carry the starter, explaining the canvas and jokes.
- **Changed:** of the 130 selected changes, 60 are restricts. Keeping (8 rooms), scripts (7) and sparing (6) are changed most.
- **The neighbourhood:** in most of the records, a neighbour's border lines answer the Dutch rooms' expansion. Three relations read differently here:
  - border talk comes from expansion, not from keeping;
  - sparing gets reasons the model does not name;
  - agreements reach only some placers.

**Checks.**
- Every quotation and item id in the twelve tellings was found in the room's A1 telling, apart from my labels "robust" and "restrict, not sorted".
- All r/ names are analysed rooms in exact case, prose_check found 0 hits, and there are 0 dashes in all thirteen files.
- Every changed unit and form cell is drawn in each figure (`_analysis/d6a18_fig_check.txt`).

**Licences exercised at D6a-18.**
- `d6a11_form_telling.py` now reads thin rooms' lines as well as defining rooms', so that the thin rooms can be told. The form's cells use defining rooms only, and a defining room's figure and a form figure re-generate byte-identical.
- Thin rooms' restrict lines on arrows were not in the D5 sort, and they are drawn as "restrict, not sorted".
- A thin room's distance to its form's centre is computed in the same space as the defining rooms' (the embedding's thin block) and given as the rank it would have.
- The A1 tellings were read through their Chronology and Relations sections, whole, through `mem.py case`.

**Slips at D6a-18.**
- The first diary read piped `mem.py diary` through `cut`, which the harness refused; it was re-run whole.
- Drafts went beyond their sources in seven places, all corrected before the checks:
  - r/cirkeltrek: "the most units carried", which was false;
  - r/indonesia: "war command" in quotation marks, which was my translation;
  - r/mindcrack: "the organised Dutch builders", which the record's own apology contradicts;
  - r/Goodboye: a gloss for the quoted "blep";
  - r/blackmirror: "the first answer", and a claim not limited to the sections read;
  - the README: "a vote" as a reason for sparing, which no sparing line gives.
