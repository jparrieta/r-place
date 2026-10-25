#!/usr/bin/env python3
"""D4a-02: for each key named, run d4_key_lines_bynode.py and write its output to
out/_analysis/d4a02_keys/<op>_<element>_<node>.txt (never overwriting), then print each file's size. The keys are the
element change keys at level 4 that D4a-01 left unread (tree-D4.md, "Where the pass stopped"), passed on the command
line in the order read.

    python3 out/_analysis/d4a02_dump_keys.py restrict:P05:T4-006 add-step:P14:T4-009 ...
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, "out", "_analysis", "d4a02_keys")
os.makedirs(D, exist_ok=True)
for k in sys.argv[1:]:
    p = os.path.join(D, k.replace(":", "_") + ".txt")
    if os.path.exists(p):
        print("exists, kept: %s" % os.path.basename(p))
        continue
    r = subprocess.run([sys.executable, os.path.join(ROOT, "out", "_analysis", "d4_key_lines_bynode.py"), "--key", k],
                       capture_output=True, text=True, cwd=ROOT)
    open(p, "w", encoding="utf-8").write(r.stdout + (("\n[stderr]\n" + r.stderr) if r.returncode else ""))
    print("%s: %d bytes%s" % (os.path.basename(p), os.path.getsize(p), " (error)" if r.returncode else ""))
