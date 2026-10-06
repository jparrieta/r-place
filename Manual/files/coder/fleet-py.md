# tools/fleet.py

The case lead's harness for branch B: plan, dispatch, collect, consolidate.

**What it holds**

`plan [--threshold 500] [--budget 500] [--floor 25]` decides the branch and cuts slices of whole threads, writing `out/_gate.json`, `out/timeline.md` and `out/lexicon.md`. `dispatch --batch NN --model ID` builds `fleet/batch_NN/` with the slice, context openings and continuing IDs. `collect --batch NN` brings the facts files back and appends a ledger entry to `out/ledger.md`. `redispatch` sets a failed batch aside under `fleet/_failed/`. `consolidate` closes each batch, fills `staging/`, pools `package/codes.jsonl`, `threads.jsonl` and `pointers.jsonl`, writes `package/codes_by_thread.md` and the lead's journal. `status` reports.

**Who writes it, and when**

The instrument's author. The case lead runs it at the points its contract names.

**Why it exists**

"Nothing here reads a coder's case or notes, and nothing here interprets anything." The ledger is "the lead's memory of the fleet, kept by the harness".

**Where**

[tools/fleet.py](../../../coder/instrument/v32/tools/fleet.py).

Checked against: tools/fleet.py, CONTRACT-case-lead.v32.md
