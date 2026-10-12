"""The split layer (J, 2026-10-12): split is withdrawn; a split written before is laid over the store until
out/recut/WITHDRAWN.json exists, and then the parents stand again while records made under the split resolve."""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(HERE)
sys.path.insert(0, T)
import vlib
d = tempfile.mkdtemp(); S = os.path.join(d, "package", "store"); O = os.path.join(d, "out"); C = os.path.join(O, "recut")
for x in (S, C): os.makedirs(x)
w = lambda p, rows: open(p, "w").write("".join(json.dumps(r) + "\n" for r in rows))
codes = [{"sub": "sweden", "code_id": "c%04d" % i, "theme_id": "t01", "hour": i} for i in range(1, 8)]
w(os.path.join(S, "codes.jsonl"), codes)
w(os.path.join(S, "themes.jsonl"), [{"sub": "sweden", "theme_id": "t01", "second_order": "big", "code_ids": ["c%04d" % i for i in range(1, 8)]}])
w(os.path.join(S, "rooms.jsonl"), [{"sub": "sweden"}])
w(os.path.join(C, "themes.jsonl"), [{"sub": "sweden", "theme_id": "t02", "parent": "t01", "code_ids": ["c0001", "c0002", "c0003"]},
                                     {"sub": "sweden", "theme_id": "t03", "parent": "t01", "code_ids": ["c0004", "c0005", "c0006", "c0007"]}])
w(os.path.join(C, "codes.jsonl"), [{"sub": "sweden", "code_id": "c%04d" % i, "theme_id": "t02" if i < 4 else "t03", "parent": "t01"} for i in range(1, 8)])
fails = []
def ok(name, cond):
    print(("ok   " if cond else "FAIL ") + name); cond or fails.append(name)
rd = lambda n: [json.loads(l) for l in open(os.path.join(S, n + ".jsonl"))]
r = subprocess.run([sys.executable, os.path.join(T, "mem.py"), "split", "sweden:t01", "--child", "a|x|c0001,c0002,c0003",
                    "--child", "b|y|c0004,c0005,c0006,c0007", "--reason", "r", "--root", d, "--out", O, "--stage", "B2"],
                   capture_output=True, text=True)
ok("split is refused", r.returncode != 0 and "withdrawn" in (r.stdout + r.stderr))
th = {t["theme_id"] for t in vlib.recut_overlay("themes", rd("themes"), O)}
ok("while the split stands, the children replace the parent", th == {"t02", "t03"})
open(os.path.join(C, "WITHDRAWN.json"), "w").write(json.dumps({"ruled_by": "J 2026-10-12", "reason": "coders' layer"}))
th = {t["theme_id"] for t in vlib.recut_overlay("themes", rd("themes"), O)}
ok("withdrawn, the parent stands again", th == {"t01"})
ct = vlib.code_themes(vlib.recut_overlay("codes", rd("codes"), O))
ok("withdrawn, a concept is the parent's", str(ct[("sweden", "c0001")]) == "t01")
ok("a record about the parent resolves", vlib.support_problems({"T3-001": ["c0001"]}, ["T3-001"], "sweden", "t01", ct) == [])
ok("a record made about a child still resolves", vlib.support_problems({"T3-001": ["c0001"]}, ["T3-001"], "sweden", "t02", ct) == [])
ok("but not under the other child", vlib.support_problems({"T3-001": ["c0001"]}, ["T3-001"], "sweden", "t03", ct) != [])
ctx = {"package": os.path.join(d, "package"), "outdir": O}
ok("the validator still knows the children for old records", ("sweden", "t02") in vlib.store_themes(ctx))
print("\nsplit: %d failed" % len(fails)); sys.exit(1 if fails else 0)
