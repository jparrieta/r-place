"""build_prototypes.py: for each room the 350-word cap cut, the note as it stands now with the cut lines put back
wherever the line the cut left still stands word for word (J, 2026-10-07, 11:18: "make a folder with the changed
version ... they can choose if they want it"). Nothing is written by a model: each change group of a cut's diff
(pretrim-A1/<sub>__<leg>.md) is applied only if its after-cut lines are in the note now, contiguous and unchanged;
cuts are applied latest leg first. The analyst's notes are not touched: the prototypes go to pretrim-A1/restored/.

    python3 build_prototypes.py RUN_DIR [OUT_DIR]
"""
import collections, os, re, sys
RUN = sys.argv[1]
AG = os.path.join(RUN, "00_GIVE-THE-AGENT", "out"); P = os.path.join(AG, "_handling", "pretrim-A1")
OUTD = sys.argv[2] if len(sys.argv) > 2 else os.path.join(P, "restored"); os.makedirs(OUTD, exist_ok=True)
rows = [l.split("\t") for l in open(os.path.join(P, "INDEX.tsv"), encoding="utf-8").read().splitlines()[1:] if l.strip()]
by = collections.defaultdict(list)
for sub, leg, *_ in rows:
    by[sub].append(leg)

def groups(diff):
    """change groups of a unified diff: (context line before or None, minus lines, plus lines)."""
    out, prev, mi, pl = [], None, [], []
    for l in diff.splitlines():
        if l.startswith(("---", "+++", "@@")):
            if mi or pl:
                out.append((prev, mi, pl)); mi, pl = [], []
            prev = None if l.startswith("@@") else prev
            continue
        if l.startswith("-"):
            mi.append(l[1:])
        elif l.startswith("+"):
            pl.append(l[1:])
        else:
            if mi or pl:
                out.append((prev, mi, pl)); mi, pl = [], []
            prev = l[1:] if l.startswith(" ") else l
    if mi or pl:
        out.append((prev, mi, pl))
    return out

def find(lines, block):
    for i in range(len(lines) - len(block) + 1):
        if lines[i:i + len(block)] == block:
            return i
    return -1

stats = []
for sub in sorted(by, key=str.lower):
    note = open(os.path.join(AG, "rooms", sub + ".md"), encoding="utf-8").read()
    lines = note.split("\n"); applied, conflict = [], []
    for leg in sorted(by[sub], key=lambda x: -int(x[4:])):
        t = open(os.path.join(P, "%s__%s.md" % (sub, leg)), encoding="utf-8").read()
        m = re.search(r"```diff\n(.*?)```", t, re.S)
        for prev, mi, pl in groups(m.group(1) if m else ""):
            if mi:
                i = find(lines, mi)
                if i >= 0 and lines[i:i + len(mi)] != pl:
                    lines[i:i + len(mi)] = pl; applied.append(leg)
                elif i < 0:
                    conflict.append(leg)
            elif prev is not None and prev in lines and not any(p in lines for p in pl):
                i = lines.index(prev); lines[i + 1:i + 1] = pl; applied.append(leg)
            else:
                conflict.append(leg)
    proto = "\n".join(lines)
    if applied:
        open(os.path.join(OUTD, sub + ".md"), "w", encoding="utf-8").write(proto)
    stats.append((sub, len(applied), len(conflict), len(note.split()), len(proto.split())))
with open(os.path.join(OUTD, "PROTOTYPES.tsv"), "w", encoding="utf-8") as f:
    f.write("sub\tgroups_put_back\tgroups_left_to_you\twords_now\twords_prototype\n")
    for s in stats:
        f.write("\t".join(map(str, s)) + "\n")
full = sum(1 for s in stats if s[1] and not s[2]); part = sum(1 for s in stats if s[1] and s[2]); none = sum(1 for s in stats if not s[1])
print("rooms %d: prototype complete %d, prototype partial %d, no prototype %d; groups put back %d, left %d; words added %d"
      % (len(stats), full, part, none, sum(s[1] for s in stats), sum(s[2] for s in stats), sum(s[4] - s[3] for s in stats)))
