#!/usr/bin/env python3
"""C2c, read-only: how much of P01 (the call) is a one-line enrolment. The reviewer found the A02 instance's answer
"I'm in." cited as a call. This counts, among the concepts cited under T3-002 (calling members in to place), those
whose coder label reads as joining rather than calling, by a pattern written here before the count:

  ENROL: the label begins with joining, volunteering, agreeing, offering, committing, signing up, pledging, promising
  to help, accepting, answering (a call) with, counting (oneself) in, saying (one) is in / on it / will help, or
  heading over, or the passage is at most five words and contains in, on it, game, help, coming, sword (an answer).

It then reads A02 (R01 -> P01) and A01 (P01 -> P03) in their holding rooms: in how many is the first P01 concept an
ENROL concept. Labels are the coders'; the pattern is a reading aid, not a recut, and its counts are approximate.

    python3 out/_analysis/c2c_t3002_enrolments.py
"""
import collections, json, os, random, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
LAB = re.compile(r"^(joining|volunteering|agreeing|offering|committing|signing up|pledging|promising to help|accepting|"
                 r"answering .* with|counting (themself|themselves|oneself|himself|herself) in|saying (they|he|she) "
                 r"(is|are|am|will) (in|on it|help)|heading over|coming to help|enlisting|reporting joining)", re.I)
SHORT = re.compile(r"\b(in|on it|game|help|coming|sword|down|count me)\b", re.I)
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json", "--limit",
                    "10000000"], cwd=ROOT, capture_output=True, text=True)
codes = dict(((c["sub"], c["code_id"]), c) for c in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))
els = dict((e["id"], e) for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p3.json"), encoding="utf-8"))["elements"])
cited = collections.defaultdict(lambda: collections.defaultdict(list))
for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    for t, cs in (r.get("support_by_theme") or {}).items():
        for c in cs:
            k = (r["sub"], c)
            if k in codes:
                for eid in ("P01", "R01", "P03"):
                    if t in els[eid]["themes"]:
                        cited[eid][r["sub"]].append(k)
                if t == "T3-002":
                    cited["T3-002"][r["sub"]].append(k)


def enrol(k):
    c = codes[k]
    lab = str(c.get("first_order") or "")
    txt = " ".join(str(c.get("text") or "").split())
    return bool(LAB.search(lab)) or (len(txt.split()) <= 5 and bool(SHORT.search(txt)))


t3 = sorted(set(k for s in cited["T3-002"].values() for k in s))
en = [k for k in t3 if enrol(k)]
print("concepts cited under T3-002: %d in %d rooms; reading as enrolment: %d (%.3f)" % (
    len(t3), len(cited["T3-002"]), len(en), len(en) / max(len(t3), 1)))
rnd = random.Random(20261014)
print("ten enrolment readings, by seed:")
print("\n".join("  %s/%s %s | %s" % (k[0], k[1], codes[k].get("first_order"), " ".join(str(codes[k].get("text"))[:90].split()))
                for k in rnd.sample(en, min(10, len(en)))))
print("ten other T3-002 readings, by seed:")
rest = [k for k in t3 if k not in set(en)]
print("\n".join("  %s/%s %s | %s" % (k[0], k[1], codes[k].get("first_order"), " ".join(str(codes[k].get("text"))[:90].split()))
                for k in rnd.sample(rest, min(10, len(rest)))))


def first(eid, sub):
    ks = [k for k in cited[eid].get(sub, []) if codes[k].get("hour") is not None]
    return min(ks, key=lambda k: codes[k]["hour"]) if ks else None


def read(fr, to):
    both = [s for s in cited[fr] if s in cited[to]]
    hold = [s for s in both if codes[first(fr, s)]["hour"] < codes[first(to, s)]["hour"]]
    side = to if to == "P01" else fr
    e = [s for s in hold if enrol(first(side, s))]
    print("%s -> %s: holds in %d of %d rooms; in %d of the holding rooms the first P01 concept reads as an enrolment"
          % (fr, to, len(hold), len(both), len(e)))


read("R01", "P01")
read("P01", "P03")
