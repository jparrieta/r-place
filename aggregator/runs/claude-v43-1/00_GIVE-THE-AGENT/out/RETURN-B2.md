# RETURN-B2: the return specification for the stage B2 pilot

Frozen with the stage file. The packet builder serves it, the brief cites it, and the validator's schema is read from it.

## Rule 0, in the contract's words

Rule 0. **Single placement, exception on the record.** A second-order theme carries one third-order theme: the one whose gate its material satisfies best; where more than one gate is satisfied, the theme's `decide_when_both` field decides. A second placement only where one cannot carry the material, and never silently: it needs its own distinct supporting concept, a written `why_not_one` in terms of what the single placement would fail to carry, a named dispensable one, and a line in `multiplacement_log.jsonl`. Three at most; beyond three, place one and record `item-is-a-bag`. An unjustified extra is a defect. The log is a measurement: recurring `(primary, additional)` pairs are boundaries the scheme has not drawn, and stage C1 reads that table first.

## What you return

One JSON line per item in the packet, in packet order, and nothing else between the lines. Read the index page whole first. Open a family's page before you place anything into it, and list the families you opened in `families_opened`.

- `sub`, `theme_id`: the item's heading, `<sub>/<theme_id>`.
- `batch`: the packet name (for round 2, `P03-r2`; a packet served in parts keeps the one name). `agent`: your reader id as given to you. `replicate`: 1. `position`: the item's number in the packet.
- `third_order`: the theme ids you place the item on, primary first. One id, unless rule 0's exception holds; never more than three.
- `multi`: true when `third_order` holds more than one id.
- `why`: for each id in `third_order`, what about THIS item put it there rather than its nearest neighbour.
- `confidence`: `clear` or `arguable`.
- `read`: `whole` (you read the label, the note and every concept) or `theme-block` (the label and note, and the concepts in part).
- `exemplar_read`: null. No exemplar is served at this stage.
- `families_opened`: the family ids whose pages you opened for this item.
- `t_start`, `t`: when you began and finished the item (ISO time, as you can tell it).
- `support`: the concept ids (`c0013`) your placement rests on.
- `multiplacement_log`: null when `multi` is false. When `multi` is true, this is the line rule 0 owes to `multiplacement_log.jsonl`: `{"primary": "T3-…", "additional": ["T3-…"], "codes": ["c…"], "why_not_one": "what the single placement would fail to carry", "dispensable": "T3-…"}`. The check leg copies it into the pilot's record. It never enters the run's own `multiplacement_log.jsonl` from stage B1.
- `item_is_a_bag`: true only when more than three themes would be needed. Then `third_order` holds one id and `why` names the others.
- `also_present`: `{}` unless `item_is_a_bag` is true. For a bag, every theme beyond the one placed, each with its own concept ids: `{"T3-…": ["c…", "c…"], "T3-…": ["c…"]}`. `support` holds the concepts behind the placed theme; a theme in `also_present` never repeats the placed one.

```json
{"sub": "...", "theme_id": "...", "batch": "P03-r2", "agent": "...", "replicate": 1, "position": 23, "third_order": ["T3-007"], "multi": false, "why": {"T3-007": "what about THIS theme put it here rather than its nearest neighbour"}, "confidence": "clear|arguable", "read": "whole|theme-block", "exemplar_read": null, "families_opened": ["G03", "G09"], "t_start": "...", "t": "...", "support": ["c0013"], "multiplacement_log": null, "item_is_a_bag": false, "also_present": {}}
END-OF-RETURN
```

A packet too large for one file is served in parts (`P03-r2-p1`, `P03-r2-p2`, ...). Read every part before you answer. On every part but the last, reply with the end marker alone. On the last part, write one line per item of the whole packet, in packet order, then the end marker. An item may begin in one part and end in the next; its concepts continue under the same heading.

After your last line, write the end marker `END-OF-RETURN` on a line of its own. Confirm that you reached the end of the packet by writing that marker; a return without it is a partial return and is reissued.
