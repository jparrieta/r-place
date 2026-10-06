# How we check v43

Target length: under 520 words. Run from ~/Jail/r-place. These are the checks both orchestrators run; this file changes only with the instrument.

1. `python3 orchestrator/OpenAI/checks/check_state.py --corpus --fingerprint FP`, FP from `aggregator/runs/claude-v43-1/CONTROL/RUN.json`: source ownership/hashes and Claude prepared corpus, 705 rooms, 115388 codes, 7844 themes. The fingerprint is Claude's build of the run, not Codex live acceptance.
2. `python3 orchestrator/OpenAI/checks/prepare_v43.py`: verify the pristine Codex corpus input and its original receipt. Its earlier build fingerprint is input provenance; fresh study builds install the current cards, tools and stage shelves. `--build` is used once and refuses overwrite. It makes no model calls.
3. `python3 orchestrator/OpenAI/checks/offline.py`: Python 3.11.17, NumPy and SciPy from the existing private tool environment, real 8 GiB reserve. Expect 215 tests, including 33 backend-dispatch regressions and seven new order tests with 17 targets compared directly with Claude. No inference or research. Private logs stay outside the repository.
4. `NODE_PATH=<installed Playwright modules> node aggregator/handler/codex/runtime/tests/panel_browser.cjs`: 56 fake-controller scenarios, phone layouts, dark/light modes, live and durable questions. No research API calls. Current Mac Chrome 154.0.8037.93.
5. `cd aggregator/instrument && bash tools/tests/run.sh` with the same Python 3.11 bin on PATH. Expect self-test 137 checks, zero verbs/stage-D failures, additional suites 14, 14 and 3.
6. `python3 aggregator/handler/claude/gen_platform.py --check`: platform schedules current.
7. Only after separate login and authorization: v43 `run.py acceptance --live`, then `python3 orchestrator/OpenAI/checks/platform_reading.py --live`. Use synthetic material; never use a research leg as a probe. Historical v42 results do not substitute.

Tests must retain actual reserve checks. Claude's adapter tests also run under OpenAI's Python: `PYTHONDONTWRITEBYTECODE=1 ../.rplace-runtime/tools/python311/venv/bin/python3 -B -m unittest discover -s aggregator/handler/claude-adapter/tests -p 'test_*.py'` (synthetic stores, a stand-in CLI); their success does not establish controller integration. Logs, screenshots, login and checkpoint files stay in `.rplace-runtime-v43` outside Git. Read the exact run source before a corpus check; no notes-only reconstruction. Results go to the orchestrators' record outside the repository, never here.

## Claude's checks

8. `bash orchestrator/Claude/scripts/harness_test_copy.sh .` in the Cowork VM (80 checks, on a small store it makes in its home), or on the Mac `bash aggregator/handler/claude/tests/run.sh aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT`. Then `python3 aggregator/handler/claude-adapter/tests/test_adapter.py` (20) and `tests/test_legs.py` (15). Synthetic stores and a stand-in CLI only.
9. On the Mac, after any build: `bash aggregator/runs/claude-v43-1/CONTROL/harness/acceptance.sh` (22) and `acceptance_v41.sh` (23), each ending ALL CLEAR; after a Claude CLI update, `python3 aggregator/handler/claude-adapter/probe_lifecycle.py --model claude-sonnet-5-5 --effort low` (14, a synthetic run outside the repository).
