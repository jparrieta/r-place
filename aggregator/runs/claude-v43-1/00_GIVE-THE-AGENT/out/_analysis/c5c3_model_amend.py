#!/usr/bin/env python3
"""C5c-03, pass 7: bring element statements and arrow mechanisms into line with the declaration amendments and findings
they repeat (c5c3_model_spec.json; the rule logged before, diary C5c-03). For each element, then each arrow: every `old`
must occur exactly once in its field; the replacements are applied, the file rewritten, one model/history.jsonl line
appended (move developing or dropping working hypotheses, the old line as `was`), then one diary line (mem.py log --kind
move) and one snap (snap.py C5 move-developing-<n>, from 131). Stops at the first failure.

    python3 out/_analysis/c5c3_model_amend.py            check, write nothing
    python3 out/_analysis/c5c3_model_amend.py --write    apply, log and snap
"""
import copy, datetime, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
spec = json.load(open(os.path.join(OUT, "_analysis", "c5c3_model_spec.json"), encoding="utf-8"))
WRITE = "--write" in sys.argv
n = 131


def run(args):
    p = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit("failed: %s\n%s" % (" ".join(args), p.stderr[-800:]))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""


for kind, fname in (("elements", "elements.jsonl"), ("arrows", "arrows.jsonl")):
    for xid, s in spec[kind].items():
        path = os.path.join(OUT, "model", fname)
        rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
        hit = [r for r in rows if r["id"] == xid]
        if len(hit) != 1:
            sys.exit("%s not found once in %s" % (xid, fname))
        was = copy.deepcopy(hit[0])
        for r in s["replace"]:
            t = hit[0][r["field"]]
            c = t.count(r["old"])
            if c != 1:
                sys.exit("%s %s: old text found %d times: %r" % (xid, r["field"], c, r["old"][:70]))
            hit[0][r["field"]] = t.replace(r["old"], r["new"])
        print("%s: %d replacements check" % (xid, len(s["replace"])))
        if not WRITE:
            continue
        open(path, "w", encoding="utf-8").write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        line = {"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": "C5",
                "leg": LEG, "id": xid, "event": "%s amended (pass 7)" % ", ".join(sorted({r["field"] for r in s["replace"]})),
                "move": "developing or dropping working hypotheses", "why": s["why"], "was": was}
        with open(os.path.join(OUT, "model", "history.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
        run([os.path.join("tools", "mem.py"), "log",
             "%s Move (developing or dropping working hypotheses), pass 7: %s brought into line with what it repeats. %s. "
             "Findings touched: none changed." % (xid, line["event"].split(" amended")[0], s["why"]), "--kind", "move"])
        print("   " + run([os.path.join("tools", "snap.py"), "C5", "move-developing-%d" % n]))
        n += 1
print("done" if WRITE else "all replacements check; nothing written")
