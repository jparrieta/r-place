# Automatic leg blocks

Target length: under 400 words.

Approve a finite range once. The controller runs its legs in order without further clicks. Each leg retains its own conversation, files, validation, recall probe and native checkpoint. Published analysis branches retain their Git checks. Closing the page does not stop work. The Mac and controller must remain running.

In the panel, choose the study, open **Run a block of legs**, enter the first and last leg, then **Approve and run block**. The operational handler can make the same request after your instruction. It takes the last leg from the declared plan, never guesses it.

Terminal example, using an illustrative three-leg range:

```bash
python3 r-place/aggregator/handler/codex/run.py run-block STUDY --first A1b-01 --last A1b-03
python3 r-place/aggregator/handler/codex/run.py block-status STUDY
python3 r-place/aggregator/handler/codex/run.py stop-block STUDY
```

`stop-block` prevents further starts and lets the current leg finish. Normal pause and stop controls remain available. A direct message or card to the analyst also stops further automatic starts, so it cannot race your intervention. After resolving the issue, `resume-block STUDY` renews permission for the remaining original range. Uncertain starts are never replayed automatically. A paused scientific leg needs its explicit continuation before a new remaining range is approved.

| Repeated steps | Work unit |
|---|---|
| A1b | Declared reading block |
| B1b, B1d | Coding or second-pass stretch |
| B4a | Adjudication packet, at most 500 items |
| C1a, C2a/d, C5a/c | Revision or review pass |
| D3a | Element group and remaining adjudication |
| D4a | Pass over the adaptation ledger |
| D5a, D6a | Branch or dimension |
| E1b | Audit section |

A block stays within one repeated step. It stops at its limit, actual interview cut, stage completion, failed validation, unresolved publication/fleet, or a request for judgment. Interviews remain optional conversations; saving their cut does not require attendance.

B1b also checks the pinned stopping-rule tool before admission. Its 60% check-in, marker 3 and PI stop override block permission. The analyst can write `out/NEEDS-JUDGMENT.md` to hold advancement. A turn ending without a close also blocks, without retrying it.

Controller restart suspends blocks for inspection. New analysis branches do not inherit permission to run. Activation requires the updated controller; an older server disables these controls. Offline tests do not establish live model acceptance.
