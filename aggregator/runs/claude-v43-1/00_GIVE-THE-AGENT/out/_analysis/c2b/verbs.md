# The read verbs

If your session has the run's tools, you may check a quote, hour or order against the record (`metroid/c0001` is room metroid, concept c0001):

- `python3 tools/cite.py --room <sub> --code <cNNNN>`: a concept's words.
- `python3 tools/mem.py after <sub>/<cNNNN>`: what answered a concept, with intervals.
- `python3 tools/mem.py forest <sub>`: a room's threads with each coded turn's hour (`--offset`, `--limit`).
- `python3 tools/mem.py room <sub> --no-canvas`: a room on one page, always `--no-canvas`.

Without them, the packet is complete in itself.
