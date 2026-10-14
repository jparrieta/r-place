#!/usr/bin/env python3
"""C2c: fix in out/model/arrows.jsonl the errors the reviewer found that the ledger carries (contract rule 13: an
error is fixed), each with a model/history.jsonl line carrying the old line as `was`. Quotes, items, threads and hours
are read from the store through mem.py, never typed.

  A02  its instances answered a start with an enrolment ("I'm in.", "I'm on my way!"), not a call (reviewer error 2):
       replaced by two starts answered by a call (opticgaming c0191 -> c0192; kerbalspaceprogram c0026 -> c0028).
  A04  its first instance invokes a treaty made before the upkeep call, and its second room (DestinyTheGame) fails
       the order (reviewer error 3): replaced by two upkeep calls answered by a first approach to the neighbour, in
       rooms where the order holds (unturned c0059 -> c0060; adventuretime c0064 -> c0065).
  A05  its printed instance (ubc c0084) is one turn, cited under no third-order theme, and shows no order (reviewer
       error 4): the support leads with the asktransgender transition (c0003 -> c0004), keeps roosterteeth c0097, and
       drops ubc c0084 and the roosterteeth remark c0098.
  A20  transformers holds on the order but its first line names no flood, so the mechanism fails there (reviewer
       error 5): its sampled_against entry records the mechanism as failing; the bound and the counterexample
       response gain the post-close judgment of the canvas's worth as a scope condition.

    python3 out/_analysis/c2c_fix_arrows.py [--write]
"""
import datetime, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AP = os.path.join(OUT, "model", "arrows.jsonl")
HP = os.path.join(OUT, "model", "history.jsonl")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def codes_of(sub):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--sub", sub, "--json",
                        "--limit", "100000"], cwd=ROOT, capture_output=True, text=True)
    return dict((c["code_id"], c) for c in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))


C = {}


def code(sub, cid):
    if sub not in C:
        C[sub] = codes_of(sub)
    c = C[sub].get(cid)
    if c is None:
        sys.exit("%s/%s is not in the store" % (sub, cid))
    return c


def quote(sub, cid):
    return {"sub": sub, "code": cid, "quote": " ".join(str(code(sub, cid)["text"]).split())}


def trans(sub, a, b):
    x, y = code(sub, a), code(sub, b)
    if x["thread_id"] != y["thread_id"]:
        sys.exit("%s %s and %s are not in one thread" % (sub, a, b))
    if not x["hour"] < y["hour"]:
        sys.exit("%s %s is not before %s" % (sub, a, b))
    return {"sub": sub, "thread": x["thread_id"], "items": [x["item_id"], y["item_id"]], "codes": [a, b],
            "hours": [x["hour"], y["hour"]], "interval_min": int(round((y["hour"] - x["hour"]) * 60))}


rows = [json.loads(l) for l in open(AP, encoding="utf-8") if l.strip()]
A = dict((r["id"], r) for r in rows)
was = dict((k, json.loads(json.dumps(A[k]))) for k in ("A02", "A04", "A05", "A20"))
hist = []

a = A["A02"]
a["support"] = [quote("opticgaming", "c0191"), quote("opticgaming", "c0192"), quote("kerbalspaceprogram", "c0026"),
                quote("kerbalspaceprogram", "c0028")]
a["support_transition"] = [trans("opticgaming", "c0191", "c0192"), trans("kerbalspaceprogram", "c0026", "c0028")]
a["instance_note"] = ("C2c, reviewer error 2: the earlier instances (sips c0026 to c0027, habs c0047 to c0048) answer a "
                      "start with a one-line enrolment cited under T3-002, not a call; replaced by two starts answered by "
                      "a call, in rooms where the order holds. Most in-thread answers to a start are enrolments; at room "
                      "level the first P01 concept reads as an enrolment in at most 10 of the 64 holding rooms "
                      "(c2c_t3002_enrolments.txt), so the count stands.")
hist.append(("A02", "instances corrected", "reviewer error 2 (quote): the instances showed a start answered by an "
             "enrolment, not a call; replaced by opticgaming c0191 -> c0192 and kerbalspaceprogram c0026 -> c0028"))

a = A["A04"]
a["support"] = [quote("unturned", "c0059"), quote("unturned", "c0060"), quote("adventuretime", "c0064"),
                quote("adventuretime", "c0065")]
a["support_transition"] = [trans("unturned", "c0059", "c0060"), trans("adventuretime", "c0064", "c0065")]
a["instance_note"] = ("C2c, reviewer error 3: switzerland c0044 -> c0045 answers an upkeep call by invoking a treaty "
                      "made earlier, so it does not show upkeep bringing the room to talk (switzerland's room-level "
                      "order still holds: first upkeep h5.38, first treaty talk h18.62); DestinyTheGame's room fails the "
                      "order (first border talk h18.74, first upkeep h27.89). Replaced by upkeep calls answered by a "
                      "first approach to the neighbour, in rooms where the order holds.")
hist.append(("A04", "instances corrected", "reviewer error 3 (order): the switzerland instance invokes an earlier "
             "treaty and DestinyTheGame's room fails the order; replaced by unturned c0059 -> c0060 and adventuretime "
             "c0064 -> c0065"))

a = A["A05"]
a["support"] = [quote("asktransgender", "c0003"), quote("asktransgender", "c0004"), quote("roosterteeth", "c0097")]
old = a.get("support_transition") or []
ask = [t for t in old if t["sub"] == "asktransgender"]
rest = [t for t in old if t["sub"] != "asktransgender"]
a["support_transition"] = ask or [trans("asktransgender", "c0003", "c0004")]
a["instance_note"] = ("C2c, reviewer error 4: the printed instance, ubc c0084, is one turn cited under no third-order "
                      "theme and shows no order; the support now rests on the asktransgender transition (a request "
                      "over the border answered by a policy of not harming artwork, c0003 -> c0004), with roosterteeth "
                      "c0097 as a quote; ubc c0084 and the roosterteeth transition to the remark c0098 (praise for the "
                      "border, not a sparing) are dropped.")
hist.append(("A05", "instances corrected", "reviewer error 4 (order): the printed instance was one uncited turn; the "
             "support leads with asktransgender c0003 -> c0004"))

a = A["A20"]
n = 0
for s in a["sampled_against"]:
    if s["sub"] == "transformers":
        s["mechanism"] = "fails"
        s["note"] = (s.get("note") or "") + ("; C2c (reviewer error 5): the order holds, the mechanism fails here: "
                                             "a line that names no flood is A20's failure clause")
        n += 1
if n != 1:
    sys.exit("transformers is not once in A20's sampled_against")
a["bound"] = a["bound"] + (" A member's judgment of the canvas's worth after the close answers no flood "
                           "(transformers, h80.40): the mechanism does not reach it.")
a["counterexample_response"] = a["counterexample_response"] + (" C2c: the reviewer read transformers as a failure of "
                                                               "the mechanism, which it is; it is recorded so (order "
                                                               "holds, mechanism fails), the post-close judgment is a "
                                                               "scope condition in the bound, and transformers joins "
                                                               "the next story draw as a sampled failure. A20 stays "
                                                               "strong: 132 of 155 rooms, 29 transitions.")
hist.append(("A20", "bounded", "reviewer error 5 (contradiction): transformers' first line names no flood, so A20's "
             "mechanism fails there though the order holds; recorded as a mechanism failure, with the post-close "
             "judgment of the canvas's worth as a scope condition"))

print(json.dumps(dict((k, {"support": A[k]["support"], "support_transition": A[k].get("support_transition")})
                      for k in ("A02", "A04", "A05")), ensure_ascii=False, indent=1)[:4000])
print(A["A20"]["bound"][-200:])
if "--write" in sys.argv:
    with open(AP, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(HP, "a", encoding="utf-8") as f:
        for k, ev, why in hist:
            f.write(json.dumps({"t": T, "stage": "C2", "leg": LEG, "id": k, "event": ev, "move": "relating or contrasting",
                                "why": why, "was": was[k]}, ensure_ascii=False) + "\n")
    print("arrows.jsonl rewritten (%d lines); %d history lines appended" % (len(rows), len(hist)))
