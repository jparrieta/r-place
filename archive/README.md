# Archive

Target length: under 220 words.

| file | what |
|---|---|
| `instrument-history.tar.gz` | every earlier instrument version, packed by `aggregator/handler/bundle_history.py` on 2026-10-02: coder v30; aggregator v28, v35, v37; the v37 run kit and v41. `HISTORY-MANIFEST.tsv` lists every file and why any was left out. |
| `instrument-v42-2026-10-03.tar.gz` | instrument v42 as the run claude-v42-1 used it, packed when this folder was made from `rplace` (2026-10-04; `rplace` at commit 61f11eab): `aggregator/instrument` (without `_versions`), `aggregator/handler/claude` (without the test stand-in link), the handler scripts and their notes, `coder/census`, `verify.sh`. sha256 8daa4e3fe335c469817dc4a0653e96f1288548719204fc5e205868f96e7bfb37. |
| `instrument-v43-2026-10-04T13Z-before-misq.tar.gz` | instrument v43 as built into claude-v43-1 (fingerprint 094d34f13f720d57), packed on 2026-10-04 at 13:32 UTC before the changes that followed Günther, Joshi and Constantinides (2026) and the audits of that day: `aggregator/instrument` (without `_versions`), `aggregator/handler/claude`, `aggregator/handler/claude-adapter`, the handler scripts and notes, `coder/census`, `verify.sh`, `OWNERSHIP.tsv`. sha256 b632af2c3a5213592e3934ef0ce7619ac7386ab2e384a192219fbdb5ac8d9153. |

The live instrument in this folder is v43 (see `aggregator/instrument/VERSIONS.tsv`).
