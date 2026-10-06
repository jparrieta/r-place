# `tools/projections.py`

Stage D4 §6, projected on afterwards: the verdicts and the canvas per branch and per cluster.

## What it holds

One line per branch (`branches.jsonl`) and per cluster (`chunk-share-D4.jsonl`) into `out/projections-D4.jsonl`: the D2 verdicts counted, the share of rooms that do not compose with its percentile against a permutation null (random groups of the same size from the analysed set), and the canvas fields summarised (median area, rooms with an artwork, the percentile of the median area) with the contract's sentence on what the canvas measures. A room's verdict is the analyst's D3 ruling where there is one, else the readers' verdict where they agree, else split.

## Who writes it, and when

The analyst runs it at D4 after the cuts are snapped and the comparison is built. Nothing it writes is read back into a cut (rule 7).

## Links

[distance.py](tool-distance-py.md), [stage D4](../../stages/D4.md).
