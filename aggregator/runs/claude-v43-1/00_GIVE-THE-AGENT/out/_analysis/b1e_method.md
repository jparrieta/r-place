# B1e working method (claude-v43-1), written at the leg's start, 2026-10-11

This file is a working record (rule 18). It says how the scheme's fields are written, so that the work
can continue after a compaction.

1. Families: `out/_analysis/b1e_families.tsv`, 21 families over the 197 themes, each a group a reader would
   confuse. A theme's discriminators name its near neighbours, inside its family first.
2. Per family, in order G01 to G21:
   - `python3 out/_analysis/b1e_digest.py <its T3 ids> --k 40 > $TMPDIR/dg_GNN.txt`, printed in parts: label,
     trigger, members, rooms, rule 0 partners, tier_history events, a seeded sample of member labels.
   - `python3 out/_analysis/b1e_cands.py <T3> --n 30 > $TMPDIR/cd_<T3>.txt` per theme: the concepts the rule 0
     lines name for the theme as an added kind, then a seeded sample of its quotes (`cite.py --tier 3rd`,
     seed 20261011). Where these hold fewer than three passing quotes, a second sample with seed 20261012.
   - Each exemplar is a quote copied from cite.py's output, a participant's words. Rivals are other passing
     quotes from the same room (the check reads rivals as concepts of the exemplar's room).
   - The family's lines are written to `out/_analysis/b1e_draft_GNN.jsonl`: every field of section 4, with
     `tier` and `floor` filled at assembly, and one extra field `two_or_half` (section 7's strongest argument
     that the theme is two or half of another), moved to `notes-B1.md` at assembly.
   - A diary note after each family names the file and its themes.
3. Names: the head's "Names to change at B1e" are applied in the drafts; each change gets a
   `tier_history.jsonl` line (event relabelled) at assembly.
4. Floors: `out/_analysis/b1e_floor.py` proposes for each theme with members in two or more rooms a pair
   unlike in size (one room's items in the window at least twice the other's), the pair not joined in an
   episode that names the theme; a theme in one room, or whose rooms are one episode, is rare.
5. Assembly: `out/_analysis/b1e_assemble.py` writes `scheme.jsonl`, `families.jsonl` and `scheme.md`
   (by family, with an index page), and prints the token sizes.
