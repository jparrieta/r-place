# The case-lead prompt (CASE-LEAD-PROMPT.md)

An extra message added to the case lead's opening message, version `lead-calibration-v2`.

**What it holds**

Scheduler notes and, between two markers, the exact block sent to the lead. The block asks the lead to apply five existing requirements more fully: consolidation (§7), within-case findings (§8), the counter-reading (§8), checkable citations with each ID in backticks, and a complete-record check that ends with `close_run.py . --role lead --preflight`. It names the model for the wave, `gpt-5.6-sol` at `medium` effort, and says fleet coders get only their normal message.

**Who writes it, and when**

Written 2026-09-08 after review of the Dorset demonstration. `start_yard_lead.py` cuts the block out between `<!-- BEGIN LEAD PROMPT -->` and `<!-- END LEAD PROMPT -->`, adds it to the output of `room.py message lead`, and saves the result and its hashes in the store's `state/`.

**Why it exists**

"The research contract is unchanged." The block "introduces no target number of themes, searches or codes", adds "no case evidence or interpretive categories", and any conflict is resolved "in favour of the supplied research contract".

**Where**

[CASE-LEAD-PROMPT.md](../../../coder/handler/CASE-LEAD-PROMPT.md); a copy sits in each room's `validation/`.

Checked against: CASE-LEAD-PROMPT.md, _tools/start_yard_lead.py
