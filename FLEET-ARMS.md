# Two reader arms

Target length: under 600 words.

Choose an arm when preparing a study. Separate studies can run both arms at once. Each study has its own files, actors, returns and locks. Each defaults to three simultaneous readers, so two studies can use six readers in total.

```bash
cd "$HOME/Jail"
python3 r-place/aggregator/handler/codex/run.py arms
python3 r-place/aggregator/handler/codex/run.py build study-codex --fleet-arm codex
python3 r-place/aggregator/handler/codex/run.py build study-router --fleet-arm openrouter
```

The live panel has the same selector beside **Prepare study**. These commands prepare studies; they do not start research. Use the usual stage and leg controls afterward. A running controller owns dispatch.

| Arm | Packet readers | Continuation |
|---|---|---|
| `codex` | GPT-6 Sol medium | Native Codex history and checkpoint fork |
| `openrouter` | Model/provider selected by `@preset/cheap` | Saved API messages and matching files replayed to the pinned model/provider |

The OpenRouter arm replaces readers at B2, B3, B4, D2/D3 verdicts and E1, matching the former gateway stages. Handler, aggregator, C2/C5 reviewers, D labelers and subreddit case coders keep their existing Codex settings. Both arms use three independent readers in B2, two in B3/B4, and the existing counts elsewhere. Replication and concurrency are separate settings.

## Configuration and routing

`aggregator/handler/claude/fleet-arms.json` defines the two choices. Set the OpenRouter preset or explicit model there before building a study. Build copies and hashes the resolved settings. Changing an existing study's arm is refused. A separate study is required for a different arm.

OpenRouter uses its API directly. No Claude CLI or Codex provider override is needed. At first dispatch, one small routing probe resolves the preset to a model and provider. Both are pinned for that study. The preset selects routing only: subsequent requests use the frozen local settings, including medium reasoning effort and a 16,000-token ceiling. They do not inherit later preset changes. Parameters unsupported by the provider cause a visible failure.

Credentials come from `OPENROUTER_API_KEY`, legacy `OPENROUTER_KEY`, or macOS Keychain service `openrouter` with your login name as account. Set an environment key before starting the controller. Keys are never placed in commands, archives or run files. OpenRouter calls use its separate account balance, not the ChatGPT subscription.

## Checks and recovery

Both arms use the same packets, schemas, counts, end markers and bounded reissues. Multipart packets retain one reader conversation. Each part records routing evidence, usage and an archive. The aggregator resolves substantive disagreement; schema checks do not prove coding quality.

Service errors block the dispatch without consuming a coding reissue. `recover DISPATCH_ID` retains valid returns and resumes the saved phase plan. `recover-plan STUDY` resumes remaining phases. `stop-run STUDY` prevents pending readers from starting until explicit recovery. Unknown request outcomes may already have incurred charges. There is no automatic cross-provider fallback.

Click **Resume as interview**, or use `resume CHECKPOINT --actor NAME` and `chat NAME`. API archives contain transcripts, supplied reasoning blocks, packet files, controller source, hashes and lineage. They do not contain hidden provider state or a process image. Stop cancels local transport; it cannot guarantee cancellation or refund upstream. OpenRouter chat accepts a new message after the current turn settles. Save an interview to archive it again.

Offline tests cover both arms. Before OpenRouter research, run `python3 r-place/aggregator/handler/codex/run.py acceptance --fleet-arm openrouter --live`. This makes one routing probe and three small paid turns, tests two interview restores, and retains the receipts. Native acceptance uses `--fleet-arm codex` and passed on 2026-10-02. OpenRouter live acceptance remains untested.

Sources: [OpenRouter presets](https://openrouter.ai/docs/guides/features/presets), [API](https://openrouter.ai/docs/api/reference/overview), [reasoning continuity](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens), [Codex app-server](https://learn.chatgpt.com/docs/app-server).
