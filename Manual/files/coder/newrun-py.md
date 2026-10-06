# newrun.py

Builds a case lead's run directory, and through `build_fleet()`, each fleet batch.

**What it holds**

`python3 newrun.py RUNDIR SUB CORPUS_JSONL BRIEF_MD MODEL`. It copies the instrument in, fills the placeholders in `CONTRACT.md`, `AGENT.md` and `CONTRACT-case-lead.md`, renders `corpus.txt`, writes `openings.md`, creates `out/` with an empty `_transcript.jsonl`, and writes `corpus_manifest.json` (the counts the gate uses) and `_manifest.json` (a sha256 of every instrument file, the model, and a fingerprint). `INSTRUMENT_FILES` lists the files the fingerprint covers.

**Who writes it, and when**

The instrument's author. `room.py run` calls it once per room; `codex_lead.py init` calls `room.py run` inside the managed copy.

**Why it exists**

So `close_run.py` "can tell afterwards whether anything moved underneath the run". The empty transcript is "deliberate": C2 fails until the dispatcher fills it. "The model is a condition of the reading", so a missing model is an error.

**Where**

[newrun.py](../../../coder/instrument/v32/newrun.py).

Checked against: newrun.py, yard/_tools/room.py, yard/_tools/codex_lead.py
