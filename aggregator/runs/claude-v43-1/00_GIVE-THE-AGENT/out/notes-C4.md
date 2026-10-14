# Notes, stage C4 (the field)

## Order kept

I opened with `AGENT.md`, the head, the stage file, the last five diary lines and `validate.py --open C4` (0 errors, 0 warnings). Then I looked for `field/`.

## The field's arrival

The field did not arrive.
- The leg opened at 16:11:58Z.
- At 16:12:52Z there was no `field/` in the run folder and none in `out/`. The stage check looks in `out/field`.
- No shelf holds a field work, and `RUN.json` does not name one.
- I asked J (QC4-001), and checked again at 16:13:04Z. Still no field and no answer.

The principal investigator's message says this leg is C4, the field, and gives no reason for an absence. As the stage file says, `field-C4.md` records that the field was not held and why. Nothing of section 2 runs.

## What the leg did

- **`field-C4.md`.** It says the field was not held, with the reason as far as I have one, and names QC4-001. It also sets down the three claims of my model that a view of the whole event could most easily overturn. I wrote them before seeing any field material, so they can stand as a prior if the field arrives at a later leg:
  - relations between rooms grow out of keeping the work;
  - most attack calls are refused inside the room, with a reason;
  - decided order is rare, and gathers in the small factions the canvas grew.
- **`manifest-C4.txt`.** No file has a stage C4 successor, and the stage C3 files stand.
- **Nothing in the model, the tier, the mapping or `findings.jsonl` changed.** No element or arrow entered from the field. No move was made, so nothing was snapped.

## The principal investigator's relay from the C3c interview fork

The PI's message relays ten answers I gave on a fork of the C3c close, which I did not see. It says I may use or set them aside as the stage file allows. Here the stage file allows only the confrontation with the field, which did not run, so I set them aside at this leg. They change no file.

Three of them bear on work already closed, and I carry them as open:
- **Felin and Zenger.** By their own definition (2017, p. 262), contrarian belief makes a theory valuable, not what makes it a theory. If so, my C3a ruling that the accounts are "about different things" may not hold, and the difference is one of setting. I have not checked the page at this leg.
- **The goal and the first loop.** Widening P02 into setting and revising the goal, with an arrow from the move back to the goal, would close the model's first loop. It needs a connection statement that can see a second occurrence.
- **The recalled source under Stigmergy.** If the field of stigmergy holds it to be coordination through the trace without talk, building and reporting the mark would join what that field keeps apart, and the cut would need a recut.

## Slips, C4a

None that I know of. Each write and its check ran in separate turns.

## The close-check, C4a

`python3 tools/validate.py C4`, run after the notes body and before the handback and the head; `field/` and `out/field` were checked again in the same call and were still absent, and QC4-001 was still open:

```
stage C4:
  field-C4.md: the field was not held
  entries from the field: 0; successors: none


0 errors (0 distinct shapes), 0 warnings
```

**How the leg closes.** The stage file says that when the field has not arrived, the leg closes once `field-C4.md` says so, and nothing below that point applies. The interview point concerns the model read against the field, and no such reading took place. So I close with `done.sh C4`, not with the interview cut. Its report is in the leg's closing diary line.
