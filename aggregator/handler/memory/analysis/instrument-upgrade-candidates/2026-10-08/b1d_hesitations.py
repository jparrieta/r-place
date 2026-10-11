"""B1d: count each room's hesitations in the B1 log, for the second pass's chosen list.

usage: python3 out/_analysis/b1d_hesitations.py [--top 20]

Three signals, read from the log of every `mem.py` call (out/_mem_reads-B1.jsonl, which holds the
text of each `log` call) and from the idea and discovery ledgers:
  for_b1d   kinds (T3 ids) named after "For B1d" in the room's notes: kinds left unplaced or unsure;
  doubt     words of doubt in the room's notes: hesitat, unsure, not sure, doubt, could also,
            either kind, a lead;
  ideas     ideas triggered in the room (ideas-B1.jsonl) whose label never became a mint.
A note is the room's when it begins with the room's name, or with "room end", "room boundary",
"room" and then the name. Score = for_b1d + doubt + 2 x ideas. Prints the rooms ranked.
"""
import json
import re
import subprocess
import sys

top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 20

listing = subprocess.run(["python3", "tools/saturation.py", "order", "--stage", "B1"],
                         capture_output=True, text=True).stdout
rooms = [ln.split("\t")[1] for ln in listing.splitlines() if "\t" in ln]
low = {r.lower(): r for r in rooms}

lead = re.compile(r"^\s*(?:room end |room boundary |room |B1c room \d+ )?([A-Za-z0-9_]+)", re.I)
doubt = re.compile(r"hesitat|unsure|not sure|doubt|could also|either kind|a lead\b", re.I)
forb = re.compile(r"For B1d[:,]?(.*)", re.S)

score = {}


def add(room, key, n):
    if n:
        d = score.setdefault(room, {"for_b1d": 0, "doubt": 0, "ideas": 0})
        d[key] += n


with open("out/_mem_reads-B1.jsonl", encoding="utf-8") as f:
    for line in f:
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get("verb") != "log" or not r.get("args"):
            continue
        text = str(r["args"][0])
        if text.startswith("B1c "):
            continue
        m = lead.match(text)
        if not m or m.group(1).lower() not in low:
            continue
        room = low[m.group(1).lower()]
        fm = forb.search(text)
        if fm:
            add(room, "for_b1d", len(set(re.findall(r"T3-\d{3}", fm.group(1)))))
        add(room, "doubt", len(doubt.findall(text)))

minted = set()
with open("out/theme_discovery.jsonl", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            minted.add(json.loads(line)["label"].strip().lower())
with open("out/ideas-B1.jsonl", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        i = json.loads(line)
        if i.get("leg") == "B1c" or i["label"].strip().lower() in minted:
            continue
        room = str(i.get("trigger", "")).split(":")[0]
        if room.lower() in low:
            add(low[room.lower()], "ideas", 1)

ranked = sorted(score.items(), key=lambda kv: (-(kv[1]["for_b1d"] + kv[1]["doubt"] + 2 * kv[1]["ideas"]), kv[0]))
print("rank\troom\tscore\tfor_b1d\tdoubt\tideas_not_minted")
for n, (room, d) in enumerate(ranked, 1):
    if n > top:
        break
    print("%d\t%s\t%d\t%d\t%d\t%d" % (n, room, d["for_b1d"] + d["doubt"] + 2 * d["ideas"], d["for_b1d"], d["doubt"], d["ideas"]))
print("rooms with any signal: %d" % len(score))
