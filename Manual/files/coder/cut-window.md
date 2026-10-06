# cut_window_v32.py

Cuts a community's record to the 97-hour window.

**What it holds**

`python3 cut_window_v32.py IN.jsonl OUT.jsonl`. The window runs from 2017-03-31 16:00 UTC (the canvas opens) through 2017-04-03 17:00 (placement disabled) to 2017-04-04 17:00. A thread with any item in the window is kept whole, and items outside it are marked `_context`. A thread with no item in the window is dropped.

**Who writes it, and when**

The instrument's author. The sources do not say which script ran it for the yard's rooms; the yard README says rooms were made from raw24 files by `build_room.py`, which is not among these sources.

**Why it exists**

The docstring says the window was tested: "748 of 748 codes fall inside END, the last one at +39h", and a coder who read seventy threads beyond it coded none. Threads stay whole "so that every parent resolves and cite() can reach anything quotable". There is no pre-period, because the ordinary week is "the brief's job".

**Where**

[cut_window_v32.py](../../../coder/instrument/v32/cut_window_v32.py). Its output is `record/coder_corpus.jsonl.gz` in each room.

Checked against: cut_window_v32.py, yard/README.md
