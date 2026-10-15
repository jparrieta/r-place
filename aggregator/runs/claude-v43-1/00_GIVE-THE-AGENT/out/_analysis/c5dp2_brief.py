#!/usr/bin/env python3
"""C5d-p2: point the interview brief written at C5c-13 at this leg. Writes out/interview/C5d-p2.md from
out/interview/C5c-13.md (kept as written): the title names C5d-p2 and says where the brief was written, and the doubt
about the model freeze says the freeze is recorded at this leg's close. Each passage must occur once. Refuses if the
target exists.

    python3 out/_analysis/c5dp2_brief.py
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "out", "interview", "C5c-13.md")
DST = os.path.join(ROOT, "out", "interview", "C5d-p2.md")
if os.path.exists(DST):
    sys.exit("%s exists" % DST)
t = open(SRC, encoding="utf-8").read()
CH = [("# Interview brief, C5c-13: the model finished again, after the serial work",
       "# Interview brief, C5d-p2: the model finished again, after the serial work\n\nWritten at C5c-13, which redid C5d's "
       "work; pointed at C5d-p2, the leg that records the model freeze and carries the interview point."),
      ("- **The model freeze.** The hash recorded at C5d is the pre-serial model's. I asked how it is to be re-recorded "
       "(QC5-003).",
       "- **The model freeze.** The hash recorded at C5d was the pre-serial model's. C5d-p2 records the model as pass 15 "
       "left it (QC5-003). What stage D reads is that version, and I have changed nothing since.")]
for old, new in CH:
    if t.count(old) != 1:
        sys.exit("found %d times: %r" % (t.count(old), old[:60]))
    t = t.replace(old, new)
open(DST, "w", encoding="utf-8").write(t)
print("wrote %s (%d words)" % (DST, len(t.split())))
