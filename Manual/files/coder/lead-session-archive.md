# The lead session archive

A case lead's whole checkpoint store, compressed: its saved conversation, the managed room, and every checkpoint.

**What it holds**

`<sub>-gpt56-calibration-v1/` with, as found on disk: `ARCHIVE.json` (marker: version, subreddit, store name, date, format, restore tool), `HEAD.json` (the last committed checkpoint), `STORE.json` (paths, model, effort, Codex binary, runtime fingerprint, lifecycle text), `native/` (the lead's Codex home: sessions, configuration, databases), `workspace/` (the managed copy of the room), `.lock`. `lead_archive.py` also requires `state/lead.json`, and CHECKPOINTS.md names `objects`, `checkpoints`, `refs` and `audit`.

**Who writes it, and when**

`codex_lead.py` builds the store at every completed lead turn; `lead_archive.py archive` packs it after work ends. Archives over 95 MB are split into `.part00`, `.part01` and so on; join them with `cat` first. The armenia archive is 76,643,642 bytes.

**Why it exists**

"Only the case lead receives native conversation checkpoints", kept "for continuation and forks". See [how the case lead remembers](../../memory/coder-lead.md) for what resuming needs.

**Where**

[coder/lead-sessions/](../../../coder/lead-sessions/): twelve, for the example rooms of the Armenia and Dutch conflict (all but Goodboye and norway). The rest of the census's saved sessions are not in this repository.

Checked against: _tools/lead_archive.py, _tools/codex_lead.py, CHECKPOINTS.md, rooms/armenia/STATE.json
