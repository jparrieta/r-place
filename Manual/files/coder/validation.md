# validation/

The receipts that say how a room's lead was prompted and what the checks found.

**What it holds**

As found on disk: `CASE-LEAD-PROMPT.md` (the prompting document), `prompting.json` (version, model, effort, the document's and message's sha256, the source brief's sha256), `lead-opening.txt` (the whole opening message the lead received), `RUN-RECEIPT.json`, `run-check.txt` and `checkpoint-check.txt`.

**Who writes it, and when**

`start_yard_lead.py` writes `prompting.json` and `lead-opening.txt` into the store's `state/` before the first turn. CASE-LEAD-PROMPT.md says "a copy of the prompting receipt accompanies the room's validation documents" under `rooms/<community>/validation/`. The script that copies them there and writes `RUN-RECEIPT.json`, `run-check.txt` and `checkpoint-check.txt` is not among these sources; `coding_queue.py` reads `RUN-RECEIPT.json` (including `reported_total_tokens`) to decide a room is finished.

**Why it exists**

So a calibrated run "is distinguishable from the earlier uncalibrated demonstration", and so the mechanical checks travel with the reading. "Mechanical success does not certify the qualitative reading."

**Where**

`validation/` in each sample room, for example [armenia](../../../coder/rooms/armenia/).

Checked against: CASE-LEAD-PROMPT.md, _tools/start_yard_lead.py, _tools/coding_queue.py
