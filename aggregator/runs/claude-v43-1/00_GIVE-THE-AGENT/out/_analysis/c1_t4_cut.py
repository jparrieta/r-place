#!/usr/bin/env python3
"""C1 section 8: cut one fourth-order theme from its spec in out/_analysis/c1_t4_specs.json, when it is cut.

Checks the spec (T4 id unused; name, gloss, declared, disconfirm, prose and members present; a source for a borrowed or
adapted one; every member a theme of scheme_v2.jsonl and in no fourth-order theme already cut; move merging|relating).
With --write it appends, in order: the line to out/fourth/fourth.jsonl; its event line to out/tier_history.jsonl
(tier fourth, event created, the move); a move line in the diary through `mem.py log --kind move`; and the snap
`tools/snap.py C1 move-<move>-<n>`, n the next number after the stage's earlier move snaps. Each step runs only if the
one before it answered. Without --write it prints the line and the checks only.

    python3 out/_analysis/c1_t4_cut.py T4-001 [--write]
"""
import datetime, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
FOURTH = os.path.join(OUT, "fourth", "fourth.jsonl")
FIELDS = ("id", "name", "gloss", "gloss_from", "declared", "source", "recalled", "adaptation", "mistaken_for",
          "disconfirm", "members", "prose", "move")


def jl(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    write = "--write" in sys.argv
    if len(args) != 1:
        sys.exit(__doc__)
    tid = args[0]
    specs = json.load(open(os.path.join(OUT, "_analysis", "c1_t4_specs.json"), encoding="utf-8"))
    sp = dict((s["id"], s) for s in specs["themes"]).get(tid)
    if sp is None:
        sys.exit("no spec %s" % tid)
    scheme = set(t["id"] for t in jl(os.path.join(OUT, "scheme_v2.jsonl")))
    cut = jl(FOURTH)
    taken = dict((m, r["id"]) for r in cut for m in r.get("members") or [])
    probs = []
    if not re.match(r"^T4-\d{3}$", tid):
        probs.append("id is not T4-nnn")
    if tid in set(r["id"] for r in cut):
        probs.append("%s is already cut; an id is never reused" % tid)
    for f in ("name", "gloss", "gloss_from", "declared", "disconfirm", "prose", "members", "move", "why"):
        if not sp.get(f):
            probs.append("no %s" % f)
    if sp.get("declared") not in ("borrowed", "adapted", "coined"):
        probs.append("declared is %r" % sp.get("declared"))
    if sp.get("declared") in ("borrowed", "adapted") and not sp.get("source"):
        probs.append("a borrowed or adapted theme names its source")
    if sp.get("declared") == "adapted" and not sp.get("adaptation"):
        probs.append("an adapted theme says what changed and why")
    if sp.get("declared") == "coined" and not sp.get("mistaken_for"):
        probs.append("a coined theme names the construct a reader will mistake it for")
    if sp.get("move") not in ("merging", "relating"):
        probs.append("move is %r" % sp.get("move"))
    mem = sp.get("members") or []
    if len(set(mem)) != len(mem):
        probs.append("a member listed twice")
    for m in mem:
        if m not in scheme:
            probs.append("%s is not a theme of scheme_v2.jsonl" % m)
        if m in taken:
            probs.append("%s already sits in %s" % (m, taken[m]))
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    leg = open(os.path.join(ROOT, ".leg")).read().strip()
    line = dict((k, sp[k]) for k in FIELDS if k in sp)
    if line.get("declared") in ("borrowed", "adapted"):
        line["recalled"] = True
    line.update({"leg": leg, "t": t})
    hist = {"t": t, "stage": "C1", "leg": leg, "tier": "fourth", "id": tid, "move": sp.get("move"), "event": "created",
            "was": None, "now": [{"id": tid, "members": mem}],
            "prompted_by": specs.get("prompted_by", ""), "why": sp.get("why")}
    if not write or probs:
        print(json.dumps(line, ensure_ascii=False))
        print(json.dumps(hist, ensure_ascii=False))
    if probs:
        sys.exit("refused: " + "; ".join(probs))
    print("checks: 0 problems; %d members" % len(mem))
    if not write:
        return
    os.makedirs(os.path.dirname(FOURTH), exist_ok=True)
    with open(FOURTH, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    with open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(hist, ensure_ascii=False) + "\n")
    print("wrote fourth/fourth.jsonl (%d lines) and tier_history.jsonl (%d lines)" % (
        len(jl(FOURTH)), len(jl(os.path.join(OUT, "tier_history.jsonl")))))
    msg = ("Fourth-order theme cut (section 8), move %s (Grodal, Anteby and Holm): %s %s, declared %s%s; %d third-order "
           "themes: %s. Why: %s" % (sp["move"], tid, sp["name"], sp["declared"],
                                    (" (%s; recalled)" % sp["source"]) if sp.get("source") else "", len(mem), ", ".join(mem),
                                    sp["why"]))
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "log", msg, "--kind", "move"],
                       cwd=ROOT, capture_output=True, text=True)
    print((r.stdout or "").strip())
    if r.returncode:
        sys.exit("mem.py log failed: %s" % r.stderr[-300:])
    n = 1 + max([int(m.group(1)) for m in (re.search(r"C1-move-[a-z]+-(\d+)\.sha256$", p)
                                            for p in glob.glob(os.path.join(OUT, "_snap", "C1-move-*.sha256"))) if m] or [0])
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "snap.py"), "C1", "move-%s-%d" % (sp["move"], n)],
                       cwd=ROOT, capture_output=True, text=True)
    print((r.stdout or "").strip() or ("snap C1 move-%s-%d" % (sp["move"], n)))
    if r.returncode:
        sys.exit("snap failed: %s" % (r.stderr or r.stdout)[-300:])


if __name__ == "__main__":
    main()
