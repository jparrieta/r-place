# render_openings_v32.py

Writes the openings file, the room's table of contents for the case lead.

**What it holds**

`python3 render_openings_v32.py coder_corpus.jsonl <sub> [--out-dir DIR]`. One block per thread in time order: a metadata line, a line of counts (comments in the window and in all, branches, depth, authors, the sum of scores), the title, and the opening post cut at 500 words. Above a size threshold it also writes `openings_titles.md` and `openings_digest.md` (counts per hour, stickied and moderator posts, the ten highest-scored titles per hour).

**Who writes it, and when**

The instrument's author. `newrun.py` calls it for the case lead only; fleet batches get no openings file.

**Why it exists**

"So that a lead who never reads the raw threads still knows what was posted when and how big each thread grew." It is "orientation, not material": the lead codes nothing from it (CONTRACT-case-lead §1a).

**Where**

[render_openings_v32.py](../../../coder/instrument/v32/render_openings_v32.py). Output: `record/openings.md` in the materials archive and `run/openings.md` in the run archive.

Checked against: render_openings_v32.py, newrun.py, CONTRACT-case-lead.v32.md
