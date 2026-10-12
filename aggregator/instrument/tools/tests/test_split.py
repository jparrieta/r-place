"""split: a second-order theme cut into children in out/recut/, read back through the store (J, 2026-10-12)."""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(HERE)
sys.path.insert(0, T)
import vlib
d = tempfile.mkdtemp(); S = os.path.join(d, "package", "store"); O = os.path.join(d, "out"); os.makedirs(S); os.makedirs(O)
w = lambda p, rows: open(p, "w").write("".join(json.dumps(r) + "\n" for r in rows))
codes = [{"sub": "sweden", "code_id": "c%04d" % i, "theme_id": "t01", "first_order": "x%d" % i, "hour": i, "item_id": "i%d" % i,
          "thread_id": "th%d" % (i % 2), "second_order": "big"} for i in range(1, 8)] + \
        [{"sub": "sweden", "code_id": "c0008", "theme_id": "t02", "first_order": "y", "hour": 1, "second_order": "small"}]
w(os.path.join(S, "codes.jsonl"), codes)
w(os.path.join(S, "themes.jsonl"), [{"sub": "sweden", "theme_id": "t01", "second_order": "big", "code_ids": ["c%04d" % i for i in range(1, 8)]},
                                     {"sub": "sweden", "theme_id": "t02", "second_order": "small", "code_ids": ["c0008"]}])
w(os.path.join(S, "rooms.jsonl"), [{"sub": "sweden"}])
w(os.path.join(O, "fleet_ids.jsonl"), [{"kind": "t", "fleet": "T2-00001", "sub": "sweden", "id": "t01"}])
fails = []
def run(*args):
    return subprocess.run([sys.executable, os.path.join(T, "mem.py")] + list(args) + ["--root", d, "--out", O, "--stage", "B2"],
                          capture_output=True, text=True)
def ok(name, cond):
    print(("ok   " if cond else "FAIL ") + name); cond or fails.append(name)
r = run("split", "sweden:t01", "--child", "a|does a|c0001,c0002", "--child", "b|does b|c0003,c0004,c0005,c0006,c0007", "--reason", "t")
ok("a child of two concepts is refused", r.returncode != 0 and "three at least" in (r.stdout + r.stderr))
r = run("split", "sweden:t01", "--child", "a|does a|c0001,c0002,c0003", "--child", "b|does b|c0004,c0005,c0006", "--reason", "t")
ok("a concept left out is refused", r.returncode != 0 and "in no child" in (r.stdout + r.stderr))
r = run("split", "sweden:t01", "--child", "a|does a|c0001,c0002,c0003,c0008", "--child", "b|does b|c0004,c0005,c0006,c0007", "--reason", "t")
ok("a concept of another theme is refused", r.returncode != 0 and "not a concept of" in (r.stdout + r.stderr))
r = run("split", "sweden:t01", "--child", "a|does a|c0001,c0002,c0003", "--child", "b|does b|c0004,c0005,c0006,c0007", "--reason", "too coarse")
ok("a good split is written", r.returncode == 0 and "into 2 children" in r.stdout)
th = vlib.recut_overlay("themes", [json.loads(l) for l in open(os.path.join(S, "themes.jsonl"))], O)
ok("the parent is gone from the themes read", ("sweden", "t01") not in {(t["sub"], t["theme_id"]) for t in th})
ok("the children stand as t03 and t04", {"t03", "t04"} <= {t["theme_id"] for t in th})
cs = {c["code_id"]: c["theme_id"] for c in vlib.recut_overlay("codes", [json.loads(l) for l in open(os.path.join(S, "codes.jsonl"))], O)}
ok("the concepts follow their child", cs["c0001"] == "t03" and cs["c0007"] == "t04" and cs["c0008"] == "t02")
fl = [json.loads(l) for l in open(os.path.join(O, "fleet_ids.jsonl"))]
ok("each child has a fleet id", {("sweden", "t03"), ("sweden", "t04")} <= {(x["sub"], x["id"]) for x in fl if x["kind"] == "t"})
ok("fleet ids stay unique", len({x["fleet"] for x in fl}) == len(fl))
ct = vlib.code_themes(vlib.recut_overlay("codes", [json.loads(l) for l in open(os.path.join(S, "codes.jsonl"))], O))
ok("a record made before the split, about the parent, still resolves", vlib.support_problems({"T3-001": ["c0001"]}, ["T3-001"], "sweden", "t01", ct) == [])
ok("a record about the child resolves", vlib.support_problems({"T3-001": ["c0001"]}, ["T3-001"], "sweden", "t03", ct) == [])
ok("a concept of the other child does not", vlib.support_problems({"T3-001": ["c0007"]}, ["T3-001"], "sweden", "t03", ct) != [])
ctx = {"package": os.path.join(d, "package"), "outdir": O}
ok("the children count as second-order themes", ("sweden", "t03") in vlib.store_themes(ctx) and ("sweden", "t01") in vlib.store_themes(ctx))
r = run("theme", "sweden/t03")
ok("mem.py theme reads a child", r.returncode == 0 and "does a" in r.stdout)
r = run("split", "sweden:t01", "--child", "a|x|c0001,c0002,c0003", "--child", "b|y|c0004,c0005,c0006,c0007", "--reason", "again")
ok("a superseded parent cannot be split again", r.returncode != 0)
print("\nsplit: %d failed" % len(fails)); sys.exit(1 if fails else 0)
