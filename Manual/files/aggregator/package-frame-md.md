# `package/FRAME.md`

The frame: which rooms the run holds, dated and hashed.

## What it holds

A short paragraph with three facts: the copy date, the room count, and a sha256 "over each room's six files and forest, rooms in sorted order". Then one line: the rooms are those whose coding had finished by the copy date, of a population of 708, and the list is `store/rooms.jsonl`.

## Who writes it, and when

`build_store.py` at stage 00. The date is the day of the build unless `--frame-date` gives one.

## Why it exists

Contract §5: "The frame you hold is a dated, hashed copy of every room whose coding had finished when the copy was taken", and "No room was chosen on anything but having been coded by the copy date." A1's first check reconciles the count against `rooms.jsonl`, the room folders and the distinct rooms in the codes and themes; A1's `run_manifest.json` takes the package hash from here.

## Where

[package/FRAME.md](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/FRAME.md).

Checked against: tools/build_store.py, CONTRACT-aggregator.md §5, stages/STAGE-A1-reading-room-notes.md.
