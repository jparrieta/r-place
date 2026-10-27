
## D6a-17: the form telling, round 2

**The close-check report of D6a-16** (`_analysis/d6a16_validate_D6.txt`): 0 errors, 0 warnings; fractal lines 50, branches placed 35 of 35.

**J's instructions** (27 October, 14:03 and 15:23 Berlin, through the handler, after the form-telling interview). There were three tasks:
- a second round of room choices by the rule I gave in the interview, for all six forms, with what changed and why, and only the new rooms told;
- one good-old room per form, the plain typical case;
- the figures redrawn with a hollow border for a form cell the room lacks, and restricts split into "the arrow fails here" and "the record cannot show it".

Everything is in `out/form-telling-D6-r2/`, with a `README.md`. Round 1 in `out/form-telling-D6/` is unchanged. The interview transcript is not in my folder, and I worked from J's summary of my answers.

**The rules, logged before they ran** (`_analysis/d6a17_select_r2.py`).
- **Round 2:** a room shows a form cell where one of its selected lines has the cell's unit and a deciding op. There is one room per part where the form has parts (B's three facets; D's three kept leaves). The triple chosen shows the most of the form's cells jointly; ties go to cells shown in sum, then selected changes, then coded concepts. There is no distance limit.
- **Good old:** the candidates hold every column of the form's change signature and lie nearer the form's centre than any other. They are ranked by cells shown, then distance, then selected changes.

**What the rules chose.** Joint coverage, round 1 against round 2: A 8 and 11 of 11; B 3 and 7 of 7; C 8 and 10 of 10; D 12 and 15 of 17; E 9 and 13 of 13; F 11 and 13 of 14. That is 51 against 69 of the 72 cells.

| form | round-2 rooms | good-old room |
|---|---|---|
| A | r/monalisaclan, r/norway, r/ripcity | r/FloydVsVoid (round 1) |
| B | r/AmericanFlaginPlace (chat), r/evex (scripts), r/PlaceNL (raids) | r/mexico (new) |
| C | r/bisexual, r/gatech (kept), r/spacexmasterrace | r/gatech |
| D | r/Temple (D.1), r/bindingofisaac (kept, D.2.1), r/kirby (D.2.2) | r/gamindustri (new) |
| E | r/4chan, r/paladins, r/stevenuniverse (kept) | r/warframe (round 1) |
| F | r/dbz, r/nbaspurs (kept), r/wildhockey | r/nbaspurs |

Sixteen rooms are new and told, and six are pointed to round 1. Covering the cells reaches rooms between forms: r/norway lies nearer B's centre, and r/evex, r/bisexual and r/Temple nearer A's.

**The figures** (`_analysis/d6a17_figures_r2.py`; six form figures and 22 room figures, each `.dot`, `.png` and `.svg`).
- A form cell a room lacks has a hollow double blue border, and every cell of the form is drawn.
- Restricts on arrows follow the D5 sort of each line: fails here, record cannot show, a condition or an overlap.
- A form figure draws each restricted arrow cell as two parallel arrows with the form's counts.
- `d6a11_form_telling.py`'s room facts now carry each change line's id, an added field, so that the sort can be looked up. Its drawings are unchanged.
- Every changed unit and every form cell is drawn in each room figure (checked by script, `_analysis/d6a17_fig_check.txt`).

**Checks.** Every quotation and item id in the 16 new tellings was found in the room's A1 telling, apart from the quoted label "robust". All r/ names are analysed rooms in exact case. prose_check found 0 hits and there are 0 dashes in all 17 files.

**Licences exercised at D6a-17.**
- The rules' tie-breaks are mine, stated before the run. So is the good-old rule's reading of "the form as a whole" as holding every column of its signature, near its centre.
- The A1 tellings were read through `_analysis/d6a17_case_sections.py`: their Chronology and Relations sections, whole, through `mem.py case`. Their other sections were not read.

**Slips at D6a-17.**
- The first check of the room figures matched arrows by the wrong pattern and reported false misses; it was rewritten before any figure was changed. The second check found one real miss: r/4chan restricts a dimension (D02) as the element of a change, which had no box. The script now draws such a unit, and r/4chan's figure was re-rendered.
- The first version of the room-summary script held a no-op line, which was removed before it ran. It also failed once on a change with no fourth-order theme, which was fixed.
- Drafts went beyond their sources in four places, all corrected before the checks:
  - r/ripcity: "each by its only line";
  - r/mexico: a garbled sentence, and a tie stated as a lead;
  - r/4chan: what "Rule 8" says and what the raided work was;
  - the README: a filename written as a pattern.
