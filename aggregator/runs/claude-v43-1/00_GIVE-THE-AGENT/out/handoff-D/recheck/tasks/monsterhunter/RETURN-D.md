# RETURN-D. What a labeler returns, and how it is checked.

You are resuming your case-lead conversation and reading its matching coded record (the coder documents in this task) against a
global model of how communities organized during the event (`MODEL.md`, with its id vocabulary
in `VOCABULARY.json` and the coding ladder in `LADDER.md`). You return two files into the return
folder the handler names (`DROPS/D/<sub>/`), never into the task folder, and nothing else. Every claim you write names a node id from the vocabulary or from this
room's own themes and concepts, and cites a concept id from this room's `codes.jsonl`. Free
text is allowed only in the `how` field of a ledger line and in the prose of the room model.

## 1. `model-D.md`: the room model

Rewrite this room's `case.md` in the model's vocabulary. Its sections follow the model's aggregate dimensions, or its elements if no dimensions are warranted, in `MODEL.md`'s order. Inside a section, write prose; every claim carries either an
element id in brackets (`[P07]`) where the model applies, or `[new: <your words>]` where no
element covers what the room did, and a concept citation (`[c0117]`) from this room's codes.
Where an element of the model did not occur in this room and the room did not need it, say so
with the id (`[absent P03]`). An element or arrow marked `tentative` in `VOCABULARY.json` is on
trial like every other: answer it for this room as you answer any element, with `instantiate`,
`restrict`, `contradict` or `absent`. For `absent`, set `observation` to `observed-absent`,
`not-needed`, `unobserved` or `not-testable`. Silence is `unobserved`, never evidence of absence. End the file with one grade line, `grade: composes |
composes-with-residue | does-not-compose`, and one sentence of why. The grade is yours and is
reported beside the independent fixed-global verdict; it does not replace it. Your grade
assesses the adapted local explanation. Add `local_status: validated | unresolved | insufficient-evidence`
and a section `## Local exceptions` listing each supported discrepancy, its adaptation and
evidence, plus any unresolved claim. Write `none` with a reason if there are no exceptions.
Do not assert exact fit when evidence remains unresolved. A local particular can be valid
without becoming a shared construct.

## 2. `adaptations.jsonl`: what the model must change to explain this room

One line per adaptation, JSON, one object per line. The operations, with their required
fields (`SCHEMA` §2 and §3, reproduced here):

| op | required | meaning |
|---|---|---|
| `instantiate` | `element`, `source` (a theme id of this room), `how`, `evidence.codes` | the element operates here in this way |
| `absent` | `element`, `why`, `observation`, plus `evidence.codes` for observed-absent or not-needed | Distinguish evidenced nonoccurrence, evidenced lack of need, an unobserved element and one that this record cannot test. Only the first two support a negative claim. |
| `add-condition` | `element`, `source` (the theme that is the condition), `how`, `evidence.codes` | the element operates here only under a condition the model leaves open |
| `add-step` | `element`, `source` (the theme that is the finer step), `how`, `evidence.codes` | a finer process inside the element the model does not name |
| `link` | `from` (a theme id of this room), `to` (an element or dimension id), `kind`, `how`, `evidence.codes` | a sequence or dependence the room needs and the model lacks |
| `restrict` | `element`, `source` (the condition), `how`, `evidence.codes` | the element fails here unless the condition holds, and the model says otherwise |
| `contradict` | `element`, `statement`, `how`, `evidence.codes` | the room's record contradicts the element as stated |
| `propose` | `statement`, `source` (a theme id), `how`, `evidence.codes` | something the room needed that no element covers |

Required on every line: `model_version`, the contents of `VERSION` in this folder, copied
exactly; a line written against another version is rejected whole. Optional on any line:
`relation` (another community's name, where the adaptation is about a named other),
`evidence.transitions`, a list of transitions read off `forest.md`, each written
`<thread id>:<coordinate>><coordinate>` (for example `62yv7y:2>2.1`, the turn at 2.1 answering
the turn at 2). `how` is one sentence, under forty words, saying what the
adaptation explains about this room. State shared conditions without case names where possible. A necessary case-specific name
is retained and marked nonportable by ingest; it remains available for local validation,
although it cannot by itself warrant a shared claim. A room with
nothing to adapt returns one line with `"op": "none"` and evidence for the fit.

```json
{"op": "add-condition", "element": "P07", "source": "t07",
 "how": "explains why the room recruited outside placers on night two and not before",
 "evidence": {"codes": ["c0117", "c0118"], "transitions": ["62yv7y:2>2.1"]}, "relation": null,
 "model_version": "<the contents of VERSION>"}
```

## 3. The end marker and the check

The last line of `adaptations.jsonl` is `{"end": true, "lines": <count>}`; the last line of
`model-D.md` is `<!-- end -->`. Confirm both before you finish. Your return is checked by
script: an unknown id, a concept id not in this room, a retracted concept, a `how` longer than
one sentence, a missing marker, or a line without evidence is
returned to the handler with the failing rule named, and the handler will ask you to repair it.
