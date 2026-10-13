#!/usr/bin/env python3
"""C1 section 6, the empties: every line of assignments_final.jsonl with third_order [].

Items are ordered by B1's reading order (tools/saturation.py order --stage B1), the order in which the scheme
first met each room, so that the first appearance of each kind of empty can be read off (saturation by kind).

    python3 out/_analysis/c1_empties.py --summary
    python3 out/_analysis/c1_empties.py --pack --from 1 --to 40     writes c1_empties_packs/empties-001-040.md
    python3 out/_analysis/c1_empties.py --list                      one line per item, in B1 order

Read-only on every ledger; --pack refuses to overwrite.
"""
import argparse, collections, importlib.util, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def b1_order():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "saturation.py"), "order", "--stage", "B1"],
                       cwd=ROOT, capture_output=True, text=True, check=True)
    pos = {}
    for line in r.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0].strip().isdigit():
            pos[parts[1].strip()] = int(parts[0])
    return pos


def load():
    rows = jl(os.path.join(OUT, "assignments_final.jsonl"))
    empties = [r for r in rows if not r.get("third_order")]
    b3 = {(r["sub"], r["theme_id"]): r for r in jl(os.path.join(OUT, "b3_classes.jsonl"))}
    dis = {(r["sub"], r["theme_id"]): r for r in jl(os.path.join(OUT, "disagreements.jsonl"))}
    rev = collections.defaultdict(list)
    for r in jl(os.path.join(OUT, "assign_revisions_only.jsonl")):
        rev[(r["sub"], r["theme_id"])].append(r)
    pos = b1_order()
    empties.sort(key=lambda r: (pos.get(r["sub"], 10 ** 6), r["theme_id"]))
    return empties, b3, dis, rev, pos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--pack", action="store_true")
    ap.add_argument("--from", dest="a", type=int)
    ap.add_argument("--to", dest="b", type=int)
    a = ap.parse_args()
    empties, b3, dis, rev, pos = load()

    if a.summary:
        print("empties: %d of %d lines; rooms holding one: %d" % (
            len(empties), sum(1 for _ in open(os.path.join(OUT, "assignments_final.jsonl"))),
            len(set(r["sub"] for r in empties))))
        keyset = ("source", "taxonomy", "class", "unresolved", "confidence", "leg")
        for k in keyset:
            c = collections.Counter(str(r.get(k)) for r in empties)
            print("%s: %s" % (k, json.dumps(dict(c.most_common()))))
        rd = collections.Counter()
        for r in empties:
            c = b3.get((r["sub"], r["theme_id"])) or {}
            rd[("r1 empty" if not c.get("r1") else "r1 placed", "r2 empty" if not c.get("r2") else "r2 placed",
                "b1 empty" if not c.get("b1") else "b1 placed")] += 1
        print("readers and B1 at B3: " + json.dumps({" / ".join(k): v for k, v in rd.most_common()}))
        print("in disagreements.jsonl: %d" % sum(1 for r in empties if (r["sub"], r["theme_id"]) in dis))
        print("with a C1 revision line: %d" % sum(1 for r in empties if (r["sub"], r["theme_id"]) in rev))
        return

    if a.list:
        for i, r in enumerate(empties, 1):
            c = b3.get((r["sub"], r["theme_id"])) or {}
            print("%3d b1#%3s %s:%s class %s %s %s r1 %s r2 %s b1 %s" % (
                i, pos.get(r["sub"]), r["sub"], r["theme_id"], r.get("class"), r.get("source"), r.get("taxonomy"),
                c.get("r1"), c.get("r2"), c.get("b1")))
        return

    if a.pack:
        spec = importlib.util.spec_from_file_location("bpf", os.path.join(AN, "b2_packets_fleet.py"))
        bpf = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bpf)
        store = bpf.pk.Store(ROOT, OUT)
        L = ["# The empties, items %d to %d of %d, in B1's reading order" % (a.a, a.b, len(empties)), ""]
        for i in range(a.a, min(a.b, len(empties)) + 1):
            r = empties[i - 1]
            key = (r["sub"], r["theme_id"])
            c = b3.get(key) or {}
            L.append("## E%03d  %s/%s  (B1 order %s; class %s; source %s; taxonomy %s; leg %s)" % (
                i, r["sub"], r["theme_id"], pos.get(r["sub"]), r.get("class"), r.get("source"), r.get("taxonomy"), r.get("leg")))
            L.append("readers at B3: r1 %s; r2 %s; my B1 %s" % (c.get("r1"), c.get("r2"), c.get("b1")))
            d = dis.get(key)
            if d:
                L.append("B4: ruling %s; field %s of %s; why: %s" % (d.get("ruling"), d.get("field"), d.get("theme"),
                                                                   " ".join(str(d.get("why") or "").split())))
            for v in rev.get(key, []):
                L.append("C1 revision (%s): %s" % (v.get("leg"), " ".join(str(v.get("reason") or v.get("why") or "").split())))
            L += store.item(r["sub"], r["theme_id"])[2:]
        os.makedirs(os.path.join(AN, "c1_empties_packs"), exist_ok=True)
        pth = os.path.join(AN, "c1_empties_packs", "empties-%03d-%03d.md" % (a.a, a.b))
        if os.path.exists(pth):
            sys.exit("%s exists" % pth)
        open(pth, "w", encoding="utf-8").write("\n".join(L) + "\n")
        print("wrote %s: %d bytes, %d lines" % (os.path.relpath(pth, ROOT), os.path.getsize(pth), len(L)))


if __name__ == "__main__":
    main()
