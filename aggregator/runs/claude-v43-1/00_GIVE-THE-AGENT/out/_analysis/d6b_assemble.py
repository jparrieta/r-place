#!/usr/bin/env python3
"""D6b: assemble retelling-D6.md from the parts (QD6-001's answer, the PI's message for D6a-02): the frame and D01
(retelling-D6-parts/D01.md), D02 to D08, then part 2, the telling (D6b-telling.md). The parts stay in place. Prints the
whole file; write it with >.

    python3 out/_analysis/d6b_assemble.py > out/retelling-D6.md
"""
import os

PARTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "retelling-D6-parts")
# D6a-09 (J's ruling 1b): the sensitivity section, written by _analysis/d6a09_sensitivity.py --md, follows part 2
ORDER = ["D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D6b-telling", "D6a09-sensitivity"]
chunks = []
for p in ORDER:
    chunks.append(open(os.path.join(PARTS, p + ".md"), encoding="utf-8").read().strip("\n"))
print("\n\n".join(chunks))
