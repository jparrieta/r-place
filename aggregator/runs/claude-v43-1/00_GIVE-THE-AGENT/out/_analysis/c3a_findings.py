#!/usr/bin/env python3
"""C3a: write the bound the abductive read prompted by O'Mahony and Ferraro (2007) found.

  findings.jsonl     a line superseding F-006 (decided order is rare), status bounded, with the condition: decided
                     order gathers in rooms placed on a colour-faction theme or on vetting guests' requests, held to
                     room size, and only in the smaller rooms. Numbers are read from c3a_decided_order_split.txt.
  model/history.jsonl  a line for C01 (the claim that cites F-006), event bounded, move relating or contrasting,
                     abductive true, prompted_by the work; elements.jsonl is not changed (an element carries no bound
                     field; the condition is written into the finding, stage C3 section 3).

Refuses to run if F-006 already has a C3a line.

    python3 out/_analysis/c3a_findings.py
"""
import datetime, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
WORK = "O'Mahony and Ferraro 2007"
FP = os.path.join(OUT, "findings.jsonl")
HP = os.path.join(OUT, "model", "history.jsonl")
rows = [json.loads(l) for l in open(FP, encoding="utf-8") if l.strip()]
if any(r["id"] == "F-006" and r.get("leg") == LEG for r in rows):
    sys.exit("F-006 already has a %s line; not written again" % LEG)
cur = [r for r in rows if r["id"] == "F-006"][-1]
txt = open(os.path.join(OUT, "_analysis", "c3a_decided_order_split.txt"), encoding="utf-8").read()
ruling = re.search(r"ruling set\s+(\d+) rooms,\s+(\d+) with decided order \(([\d.]+)\)", txt)
other = re.search(r"all other rooms\s+(\d+) rooms,\s+(\d+) with decided order \(([\d.]+)\)", txt)
guests = re.search(r"guests asking a host\s+(\d+) rooms,\s+(\d+) with", txt)
null = re.search(r"in the ruling set: (\d+); null mean ([\d.]+), 95th percentile (\d+), p \(one-sided\) ([\d.]+)", txt)
qs = re.findall(r"quartile (\d) \((\d+) to (\d+) items\): (\d+) of (\d+) \([\d.]+\) against (\d+) of (\d+)", txt)
if not (ruling and other and guests and null and len(qs) == 4):
    sys.exit("could not read c3a_decided_order_split.txt")
q = [tuple(int(x) for x in t[3:]) for t in qs]
small = (q[0][0] + q[1][0], q[0][1] + q[1][1], q[0][2] + q[1][2], q[0][3] + q[1][3])
large = (q[2][0] + q[3][0], q[2][1] + q[3][1], q[2][2] + q[3][2], q[2][3] + q[3][3])
cond = ("Bounded at C3a by an abductive read prompted by %s, who hold that a production community establishes a shared "
        "basis of authority before it can govern itself (p. 1081). Decided order gathers where a room governs a territory "
        "for a colour or rules on guests' requests to build: %s of the %s rooms placed on a colour-faction theme "
        "(Neo-tribes) or on vetting others' requests carry it (%s), against %s of the %s other rooms (%s). Held to room "
        "size, %s against a null mean of %s (95th percentile %s, p %s; decided-order rooms shuffled within "
        "items_in_window quartiles, 2000 shuffles, seed 20261014). The gap lies in the two smaller quartiles (%d of %d "
        "against %d of %d); in the two larger it vanishes (%d of %d against %d of %d). None of the %s rooms whose "
        "members asked a host for space carries it. The factions appoint overseers and lay down rules (PurplePixels "
        "c0057, c0137), name a temporary leader (TheGreatGreenBox c0051) and call for bans (orderofthebluecorner c0009)."
        % (WORK, ruling.group(2), ruling.group(1), ruling.group(3), other.group(2), other.group(1), other.group(3),
           null.group(1), null.group(2), null.group(3), null.group(4), small[0], small[1], small[2], small[3],
           large[0], large[1], large[2], large[3], guests.group(1)))
f = dict(cur)
f.update({"stage": "C3", "leg": LEG, "supersedes": "F-006@%s" % cur["leg"], "status": "bounded", "t": T,
          "bound": cur.get("bound", "") + " " + cond,
          "evidence": list(cur.get("evidence") or []) + ["out/_analysis/c3a_decided_order_split.txt",
                                                         "PurplePixels:c0057", "PurplePixels:c0137",
                                                         "TheGreatGreenBox:c0051", "orderofthebluecorner:c0009"],
          "literature": [WORK], "abductive": True, "prompted_by": WORK,
          "why": "stage C3a, contradicting work: %s; the disagreement is about the setting and bounds the claim to rooms "
                 "whose work is their own picture" % WORK})
els = [json.loads(l) for l in open(os.path.join(OUT, "model", "elements.jsonl"), encoding="utf-8") if l.strip()]
c01 = [e for e in els if e["id"] == "C01"][0]
h = {"t": T, "stage": "C3", "leg": LEG, "id": "C01", "event": "bounded", "move": "relating or contrasting",
     "why": "its finding F-006 bounded at C3a: decided order gathers in rooms that govern a territory for a colour or "
            "rule on guests, held to size and in the smaller rooms; the element's statement and range are unchanged "
            "(the range already ends at canvas-born factions holding elections)",
     "was": c01, "abductive": True, "prompted_by": WORK,
     "stamp": {"leg": LEG, "prompted_by": {"work": WORK, "theme": "T4-011"}}}
with open(FP, "a", encoding="utf-8") as out:
    out.write(json.dumps(f, ensure_ascii=False) + "\n")
with open(HP, "a", encoding="utf-8") as out:
    out.write(json.dumps(h, ensure_ascii=False) + "\n")
print(cond)
print("F-006 superseded (status bounded); C01 history line written")
