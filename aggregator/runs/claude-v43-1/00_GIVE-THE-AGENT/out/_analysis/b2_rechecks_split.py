#!/usr/bin/env python3
"""B2b-r2-p2: the rechecks the scheme edits owe the split's children (QB2-010), from `mem.py rechecks --owed`
(read page by page with --offset; mem.py pages at 80 lines).

The children were placed after every edit, against the scheme as it stands. Each owing edit's changed
sentence is read against the children it owes (--show); the reason per edit names what the sentence decides
and why the child stays. Placement and concepts are the child's own line in author_items.jsonl or
gold_items.jsonl. Items owed that are not children are reported and not recorded here. Dry run unless
--write; --max N slices (about 4.5 seconds a record).
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
MEM = [sys.executable, os.path.join(ROOT, "tools", "mem.py")]
WHY_FILE = os.path.join(OUT, "_analysis", "b2_rechecks_split_why.json")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def owed_lines():
    lines, off = [], 0
    while True:
        p = subprocess.run(MEM + ["rechecks", "--owed", "--offset", str(off)], capture_output=True, text=True)
        out = [l for l in p.stdout.splitlines()]
        lines += out
        m = re.search(r"\[lines \d+-(\d+) of (\d+)", "\n".join(out))
        if not m or int(m.group(1)) >= int(m.group(2)):
            return lines
        off = int(m.group(1))


def main():
    placed = {r["item"]: r for n in ("author_items.jsonl", "gold_items.jsonl") for r in jl(os.path.join(OUT, n))}
    edits = jl(os.path.join(OUT, "scheme_edits.jsonl"))
    owed, edit = [], None
    for line in owed_lines():
        m = re.match(r"^(edit:\d+)\s", line)
        if m:
            edit = m.group(1)
        m = re.match(r"^\s+owed: ([^:]+):(t\d+)\s+on (\S+)", line)
        if m:
            owed.append((edit, "%s/%s" % (m.group(1), m.group(2)), m.group(3).split(",")))
    owed = list(dict.fromkeys((e, it, tuple(th)) for e, it, th in owed))
    kids = [o for o in owed if placed.get(o[1], {}).get("source") == "split"]
    other = [o for o in owed if o not in kids]
    print("owed %d: %d to split children, %d to other items%s" % (len(owed), len(kids), len(other),
          (" (%s)" % ", ".join(sorted({"%s %s" % (e, it) for e, it, _ in other}))[:400]) if other else ""))
    if "--show" in sys.argv:
        for e in dict.fromkeys(e for e, _, _ in kids):
            x = edits[int(e.split(":")[1]) - 1]
            now, was = x.get("now"), x.get("was")
            if isinstance(now, list) and isinstance(was, list):
                now = [d for d in now if d not in was]
            its = sorted({"%s on %s" % (it, ",".join(th)) for ee, it, th in kids if ee == e})
            print("%s %s %s\n  changed: %s\n  owes: %s\n" % (e, x.get("theme"), x.get("field"),
                  json.dumps(now, ensure_ascii=False)[:700], "; ".join(its)))
        return
    why = json.load(open(WHY_FILE, encoding="utf-8")) if os.path.exists(WHY_FILE) else {}
    calls, nowhy = [], set()
    for e, it, th in kids:
        if e not in why:
            nowhy.add(e); continue
        r = placed[it]
        codes = ";".join("%s=%s" % (t, ",".join(r["support_by_theme"][t])) for t in th)
        reason = "unchanged: placed at B2b-r2-p2 after %s, against the scheme as it stands; read against its sentence: %s" % (e, why[e])
        calls.append(MEM + ["recheck", it.replace("/", ":"), "--change", e, "--theme", ",".join(th), "--codes", codes,
                            "--reason", reason, "--stage", "B2"])
    print("to record %d; edits without a reason: %s" % (len(calls), sorted(nowhy) or "none"))
    if nowhy or "--write" not in sys.argv:
        return
    if "--max" in sys.argv:
        calls = calls[:int(sys.argv[sys.argv.index("--max") + 1])]
    bad = 0
    for c in calls:
        p = subprocess.run(c, capture_output=True, text=True)
        if p.returncode != 0:
            bad += 1
            print("FAILED %s %s: %s" % (c[3], c[5], (p.stdout + p.stderr).strip()[-300:]))
    print("recorded %d, failed %d" % (len(calls) - bad, bad))


if __name__ == "__main__":
    main()
