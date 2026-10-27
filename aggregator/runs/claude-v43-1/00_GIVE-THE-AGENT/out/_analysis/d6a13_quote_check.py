#!/usr/bin/env python3
"""D6a-13 onward, the form tellings: check a room telling against its A1 telling. Every straight-quoted string in the
room file must appear in package/<sub>/case.md (curly quotes and apostrophes folded), every backticked item id must
appear there, and every r/ name in the given files must be an analysed room in exact case (r/place allowed). Prints
one line per problem and a summary; reads no other file.

    python3 out/_analysis/d6a13_quote_check.py --sub suomi --room out/form-telling-D6/room-C-suomi.md \
        --names out/form-telling-D6/form-C.md out/form-telling-D6/room-C-suomi.md
"""
import argparse, os, re

ap = argparse.ArgumentParser()
ap.add_argument("--sub", required=True)
ap.add_argument("--room", required=True)
ap.add_argument("--names", nargs="*", default=[])
a = ap.parse_args()
AN = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(AN))
PKG = os.path.join(ROOT, "package")


def fold(s):
    return (s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
            .replace("…", "...").replace("–", "-").replace("—", "-"))


case = fold(open(os.path.join(PKG, a.sub, "case.md"), encoding="utf-8").read())
room = open(a.room, encoding="utf-8").read()
problems = 0
quotes = re.findall(r'"([^"\n]+)"', fold(room))
for q in quotes:
    if q not in case:
        problems += 1
        print("QUOTE NOT IN CASE:", q)
ids = [i for i in re.findall(r"`([0-9a-z]{6,7})`", room)]
for i in ids:
    if ("`" + i + "`") not in case:
        problems += 1
        print("ID NOT IN CASE:", i)
rooms = set(d for d in os.listdir(PKG) if os.path.isdir(os.path.join(PKG, d)))
names = 0
for fn in a.names:
    for n in re.findall(r"(?<![A-Za-z0-9_])/?r/([A-Za-z0-9_]+)", open(fn, encoding="utf-8").read()):
        names += 1
        if n != "place" and n not in rooms:
            problems += 1
            print("R/ NAME NOT AN ANALYSED ROOM:", fn, n)
print("%s: %d quotations, %d item ids, %d r/ names checked; %d problems" % (a.sub, len(quotes), len(ids), names,
                                                                            problems))
