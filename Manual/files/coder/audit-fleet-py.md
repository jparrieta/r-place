# tools/audit_fleet.py

The gate before the case lead's step 4.

**What it holds**

`python3 tools/audit_fleet.py --run . --sub <sub> [--record coder_corpus.jsonl]`. Seven checks: staged codes appear once and unchanged in the pool; every code, pointer and exclusion text matches the record at its offsets; no thread is disposed twice and every batch disposed exactly its slice; every `coded` thread has a forest entry; every code sits on a forest node; the rendered forest has one block per entry; `out/_gate.json` is complete. In branch A only checks 2, 4, 5 and 6 run.

**Who writes it, and when**

The instrument's author. The case lead runs it after `consolidate` and the forest. The scheduler's E1 check requires it to pass.

**Why it exists**

It "checks the things a case lead cannot see by reading". "A check that could not run is reported as FAILED, never as passed: a gate that cannot find its inputs has not opened." On failure the lead stops and reports.

**Where**

[tools/audit_fleet.py](../../../coder/instrument/v32/tools/audit_fleet.py).

Checked against: tools/audit_fleet.py, CONTRACT-case-lead.v32.md §5, CONTRACT-scheduler.md
