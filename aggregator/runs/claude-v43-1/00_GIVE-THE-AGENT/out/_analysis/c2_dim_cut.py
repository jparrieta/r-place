#!/usr/bin/env python3
"""C2 section 2: cut one aggregate dimension from its spec in out/_analysis/c2_dim_specs.json, when it is cut.

Checks the spec (D id unused; label, members (two or more, each a fourth-order theme in fourth/fourth.jsonl and in no
dimension already cut), construct block with status, gloss, mistaken_for, disconfirm_elsewhere, a source for a
borrowed or adapted one and `changed` for an adapted one; question; confidence clear|arguable; move). With --write it
appends, in order: the line to out/dimensions.jsonl; its event line to out/tier_history.jsonl (tier dimension, event
created, was null); a move line in the diary through `mem.py log --kind move`; and the snap `tools/snap.py C2
move-<move>-<n>`, n the next after the stage's earlier move snaps. Each step runs only if the one before it answered.

    python3 out/_analysis/c2_dim_cut.py D01 [--write]
"""
import datetime, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DIMS = os.path.join(OUT, "dimensions.jsonl")


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
    did = args[0]
    specs = json.load(open(os.path.join(OUT, "_analysis", "c2_dim_specs.json"), encoding="utf-8"))
    sp = dict((s["id"], s) for s in specs["dimensions"]).get(did)
    if sp is None:
        sys.exit("no spec %s" % did)
    t4 = set(r["id"] for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl")))
    cut = jl(DIMS)
    taken = dict((m, r["id"]) for r in cut for m in r.get("members") or [])
    cb = sp.get("construct") or {}
    probs = []
    if not re.match(r"^D\d{2}$", did):
        probs.append("id is not D01")
    if did in set(r["id"] for r in cut):
        probs.append("%s already cut" % did)
    for f in ("label", "question", "move", "why", "predicate"):
        if not sp.get(f):
            probs.append("no %s" % f)
    if len(sp.get("members") or []) < 2:
        probs.append("fewer than two members")
    for m in sp.get("members") or []:
        if m not in t4:
            probs.append("%s not in fourth/fourth.jsonl" % m)
        if m in taken:
            probs.append("%s already in %s" % (m, taken[m]))
    if cb.get("status") not in ("borrowed", "adapted", "coined"):
        probs.append("construct.status %r" % cb.get("status"))
    for f in ("gloss", "mistaken_for", "disconfirm_elsewhere"):
        if not cb.get(f):
            probs.append("construct.%s empty" % f)
    if cb.get("status") in ("borrowed", "adapted") and not cb.get("source"):
        probs.append("no source")
    if cb.get("status") == "adapted" and not cb.get("changed"):
        probs.append("adapted with no changed")
    if sp.get("confidence") not in ("clear", "arguable"):
        probs.append("confidence %r" % sp.get("confidence"))
    if sp.get("move") not in ("merging", "relating"):
        probs.append("move %r" % sp.get("move"))
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    leg = open(os.path.join(ROOT, ".leg")).read().strip()
    construct = dict(cb)
    if construct.get("status") in ("borrowed", "adapted"):
        construct["recalled"] = True
    line = {"id": did, "label": sp["label"], "members": sp["members"], "construct": construct,
            "question": sp["question"], "predicate": sp["predicate"], "confidence": sp["confidence"],
            "pass": 1, "leg": leg, "t": t}
    hist = {"t": t, "stage": "C2", "leg": leg, "tier": "dimension", "id": did, "move": sp["move"], "event": "created",
            "was": None, "now": [{"id": did, "members": sp["members"]}], "prompted_by": specs.get("prompted_by", ""),
            "why": sp["why"]}
    if probs or not write:
        print(json.dumps(line, ensure_ascii=False))
    if probs:
        sys.exit("refused: " + "; ".join(probs))
    print("checks: 0 problems; %d members" % len(sp["members"]))
    if not write:
        return
    with open(DIMS, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    with open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(hist, ensure_ascii=False) + "\n")
    print("wrote dimensions.jsonl (%d lines) and tier_history.jsonl (%d lines)" % (
        len(jl(DIMS)), len(jl(os.path.join(OUT, "tier_history.jsonl")))))
    msg = ("Dimension cut (section 2), move %s (Grodal, Anteby and Holm): %s %s, construct %s%s; members %s. Question: %s "
           "Why: %s" % (sp["move"], did, sp["label"], cb["status"], (" (%s; recalled)" % cb["source"]) if cb.get("source") else "",
                        ", ".join(sp["members"]), sp["question"], sp["why"]))
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "log", msg, "--kind", "move"],
                       cwd=ROOT, capture_output=True, text=True)
    print((r.stdout or "").strip())
    if r.returncode:
        sys.exit("mem.py log failed: %s" % r.stderr[-300:])
    n = 1 + max([int(m.group(1)) for m in (re.search(r"C2-move-[a-z]+-(\d+)\.sha256$", p)
                                            for p in glob.glob(os.path.join(OUT, "_snap", "C2-move-*.sha256"))) if m] or [0])
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "snap.py"), "C2", "move-%s-%d" % (sp["move"], n)],
                       cwd=ROOT, capture_output=True, text=True)
    print((r.stdout or "").strip())
    if r.returncode:
        sys.exit("snap failed: %s" % (r.stderr or r.stdout)[-300:])


if __name__ == "__main__":
    main()
