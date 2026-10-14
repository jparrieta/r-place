#!/usr/bin/env python3
"""C2 section 2, pass 2: split Contention out of Order without law (move: splitting), by the rule written in
out/_questions/contention-dimension.md before pass 2 counted (Reading 2 is preferred if pass 2 grounds an arrow into or
out of attack whose mechanism does not run through border talk; A15 and A18 are such arrows).

With --write, in order, each step only if the one before it answered:
1. dimensions.jsonl rewritten in place: D04 loses Repertoire of contention and Rivalry, with its question, predicate and
   construct block revised; D08 Contention appended. tier_history.jsonl: one line for D04 (event recut, was = the old
   line) and one for D08 (event created, was null).
2. fourth/fourth.jsonl rewritten in place: the two fourth-order themes' dimension set to D08 and pass to 2;
   tier_history.jsonl: one line each with the old line as was.
3. model/elements.jsonl rewritten in place: P09 and P18 move to D08; P09 also cites F-007; model/history.jsonl: one line
   each with the old element as was.
4. One move line in the diary (mem.py log --kind move) and the snap tools/snap.py C2 move-splitting-<n>.

    python3 out/_analysis/c2_dim_recut_p2.py [--write]
"""
import datetime, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
write = "--write" in sys.argv


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def wl(p, rows):
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def al(p, rows):
    with open(p, "a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
leg = open(os.path.join(ROOT, ".leg")).read().strip()
DP, FP, EP = os.path.join(OUT, "dimensions.jsonl"), os.path.join(OUT, "fourth", "fourth.jsonl"), os.path.join(OUT, "model", "elements.jsonl")
dims, t4, els = jl(DP), jl(FP), jl(EP)
name = dict((r["id"], r["name"]) for r in t4)
moved = [k for k, v in name.items() if v in ("Repertoire of contention", "Rivalry")]
if len(moved) != 2 or "D08" in set(d["id"] for d in dims):
    sys.exit("refused: the two themes not found, or D08 already cut")
d04 = [d for d in dims if d["id"] == "D04"][0]
if not set(moved) <= set(d04["members"]):
    sys.exit("refused: the themes are not in D04")
was_d04 = json.loads(json.dumps(d04))
d04["members"] = [m for m in d04["members"] if m not in moved]
d04["question"] = ("How rooms that share one surface, with no authority over any of them, come to hold, spare, trade, settle "
                   "and federate over space and help.")
d04["predicate"] = ("A fourth-order theme belongs when its acts are directed at another room as a party to an order: a claim "
                    "against it, restraint toward it, a deal, help, or a body of rooms. Moves against a rival and talk with a "
                    "rival belong to Contention.")
d04["construct"]["disconfirm_elsewhere"] = ("In another surface shared by groups with no authority over them, neighbouring "
                                            "groups neither claim, spare, bargain, trade help nor federate in recurring forms, "
                                            "and order between them arises by chance.")
d04["pass"], d04["leg"], d04["t"] = 2, leg, t
d08 = {"id": "D08", "label": "Contention", "members": sorted(moved),
       "construct": {"status": "adapted", "source": "Tilly, C. and Tarrow, S. (2007) Contentious Politics (recalled)",
                     "changed": "Tilly and Tarrow's contention is claim-making against or through authorities, with a "
                                "repertoire learned over years. Here no claim is made on any authority, the stakes are pixels "
                                "and honour, the repertoire is learned in hours, and the contest is often played for sport.",
                     "mistaken_for": "Conflict as the breakdown of order between rooms. Here the contest and its settlement "
                                     "run together: an attack call is refused or met with a truce inside the same room "
                                     "(A16, A17).",
                     "disconfirm_elsewhere": "On another surface shared by groups, attacks are never answered inside the "
                                             "attacking group by refusal or talk, and are never carried on in talk with "
                                             "the rival.",
                     "gloss": "It's been a well fought war today : ) I've been trying to fuck up your CLG all day",
                     "gloss_from": "clg/c0040", "recalled": True},
       "question": "How a room wages a contest with another room and carries it on: the moves against the rival's work, and "
                   "the talk that makes the rival a party.",
       "predicate": "A fourth-order theme belongs when its acts are directed against another room as a rival: moves against "
                    "its work, or talk that names it as an opponent.",
       "confidence": "arguable", "pass": 2, "leg": leg, "t": t}
th = [{"t": t, "stage": "C2", "leg": leg, "tier": "dimension", "id": "D04", "move": "splitting", "event": "recut",
       "was": was_d04, "now": [{"id": "D04", "members": d04["members"]}, {"id": "D08", "members": d08["members"]}],
       "prompted_by": "out/_questions/contention-dimension.md; arrows A15 to A18 (pass 2)",
       "why": "Contention split out: two pass 2 arrows run into and out of attack without border talk (A15 call then attack, "
              "A18 attack then rivalry talk), and two run from the contest into the order between rooms (A16 restraint, "
              "A17 truce); with the split the dimension level shows the contest and its settlement as two things."},
      {"t": t, "stage": "C2", "leg": leg, "tier": "dimension", "id": "D08", "move": "splitting", "event": "created",
       "was": None, "now": [{"id": "D08", "members": d08["members"]}], "prompted_by": "out/_questions/contention-dimension.md",
       "why": "split from D04 (see the D04 line)"}]
for r in t4:
    if r["id"] in moved:
        w = json.loads(json.dumps(r))
        r["dimension"], r["pass"] = ["D08"], 2
        th.append({"t": t, "stage": "C2", "leg": leg, "tier": "fourth", "id": r["id"], "move": "splitting",
                   "event": "dimension changed", "was": w, "why": "moved from D04 Order without law to D08 Contention"})
eh = []
for e in els:
    if e["id"] in ("P09", "P18"):
        w = json.loads(json.dumps(e))
        e["dimension"] = ["D08"]
        if e["id"] == "P09":
            e["evidence"]["findings"] = sorted(set((e["evidence"].get("findings") or []) + ["F-007"]))
        eh.append({"t": t, "stage": "C2", "leg": leg, "id": e["id"], "event": "dimension changed", "move": "splitting",
                   "why": "its fourth-order theme moved from D04 to D08 Contention%s" % ("; cites F-007" if e["id"] == "P09" else ""),
                   "was": w})
print("D04 members now: %s" % ", ".join(d04["members"]))
print("D08: %s" % json.dumps(d08, ensure_ascii=False)[:400])
print("tier_history lines: %d; element history lines: %d" % (len(th), len(eh)))
if not write:
    sys.exit(0)
wl(DP, [d04 if d["id"] == "D04" else d for d in dims] + [d08])
wl(FP, t4)
al(os.path.join(OUT, "tier_history.jsonl"), th)
wl(EP, els)
al(os.path.join(OUT, "model", "history.jsonl"), eh)
print("written: dimensions.jsonl %d lines, fourth.jsonl %d, tier_history.jsonl %d, elements.jsonl %d" % (
    len(jl(DP)), len(jl(FP)), len(jl(os.path.join(OUT, "tier_history.jsonl"))), len(jl(EP))))
msg = ("Dimension recut (section 2, pass 2), move splitting (Grodal, Anteby and Holm): D08 Contention split from D04 Order "
       "without law, members %s (Repertoire of contention, Rivalry); construct adapted (Tilly and Tarrow, contentious "
       "politics; recalled), confidence arguable. Question: %s D04 keeps %s; its question, predicate and disconfirmation "
       "clause revised. fourth.jsonl: the two themes' dimension set to D08 (tier_history lines with was). Elements P09 and P18 "
       "move to D08 (history lines with was); P09 cites F-007. Why: by the rule in _questions/contention-dimension.md, A15 and "
       "A18 run into and out of attack without border talk; A16 and A17 run from the contest into the order between rooms, "
       "which the split makes visible at the dimension level." % (", ".join(d08["members"]), d08["question"],
                                                                 ", ".join(d04["members"])))
r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "log", msg, "--kind", "move"], cwd=ROOT,
                   capture_output=True, text=True)
print((r.stdout or "").strip())
if r.returncode:
    sys.exit("mem.py log failed")
n = 1 + max([int(m.group(1)) for m in (re.search(r"C2-move-[a-z]+-(\d+)\.sha256$", p)
                                        for p in glob.glob(os.path.join(OUT, "_snap", "C2-move-*.sha256"))) if m] or [0])
r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "snap.py"), "C2", "move-splitting-%d" % n], cwd=ROOT,
                   capture_output=True, text=True)
print((r.stdout or r.stderr).strip())
