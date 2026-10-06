# `tools/links.py`

Checks that every id named in the head and the questions exists.

## What it holds

It resolves third- and fourth-order themes, dimensions, elements, arrows, findings, families, branches, adaptation ids and question slugs against `out/`; a room (`r/<sub>` or `<sub>/`) against `rooms.jsonl`, where a room the rooms named and r/place also resolve; a first-order concept (`<sub>/cNNNN` or `<sub>:cNNNN`) against the store's codes; a second-order theme (`<sub>/tNN`) against its themes. It exits 1 and lists what does not resolve.

## Who writes it, and when

Shipped in the analyst's `tools/`. `validate.py --open` runs it at every leg's open, and `done.sh` runs it at every close.

## Why it exists

An unresolved id in the head fails the launch at every stage; at close it keeps the leg open, except at a pause, where it is carried to the next leg. The head must point at real things because the next leg starts from it.

## Where

[tools/links.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/links.py).

Checked against: tools/links.py, tools/validate.py, tools/done.sh.
