"""pretrim_review.py: one short review file per room from pretrim_extract.py's output, and the rooms cut into batches,
one batch per restore leg (J, 2026-10-07, 11:05: all 562 cut notes, option b). A review file holds, for each leg that
cut the room's note, only the lines the cut changed (unified diff, one line of context), so the analyst reads the cut,
not the whole note twice.

    python3 pretrim_review.py RUN_DIR FIRST_LEG_NUMBER BATCHES      e.g. runs/claude-v43-1 49 5
"""
import collections, difflib, os, re, sys
RUN, first, nb = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
P = os.path.join(RUN, "00_GIVE-THE-AGENT", "out", "_handling", "pretrim-A1")
R = os.path.join(P, "review"); os.makedirs(R, exist_ok=True)
rows = [l.split("\t") for l in open(os.path.join(P, "INDEX.tsv"), encoding="utf-8").read().splitlines()[1:] if l.strip()]
by = collections.defaultdict(list)
for sub, leg, before, now, ok in rows:
    by[sub].append((leg, int(before), int(now), ok))
def block(path, name):
    t = open(path, encoding="utf-8").read()
    m = re.search(r"## Before the cut\n\n```\n(.*?)```", t, re.S)
    return m.group(1) if m else ""
subs = sorted(by, key=str.lower)
size = {}
for sub in subs:
    cur = open(os.path.join(RUN, "00_GIVE-THE-AGENT", "out", "rooms", sub + ".md"), encoding="utf-8").read()
    L = ["# r/%s: what the 350-word cap cut" % sub, "",
         "Read with your note as it stands now (`out/rooms/%s.md`). Each section is one leg's cut, recovered from the record "
         "(the checkpoint before the leg and the leg's own edits; verified against the leg's checkpoint). Lines marked `-` "
         "are in the note as it stood after that leg; lines marked `+` are what you wrote before the hook made you cut. "
         "Since then the note may have changed again." % sub, ""]
    for leg, before, now, ok in sorted(by[sub], key=lambda x: int(x[0][4:])):
        full = block(os.path.join(P, "%s__%s.md" % (sub, leg)), sub)
        after = None
        t = open(os.path.join(P, "%s__%s.md" % (sub, leg)), encoding="utf-8").read()
        m = re.search(r"```diff\n(.*?)```", t, re.S)
        d = m.group(1) if m else ""
        # rebuild the note after the leg from the diff is not needed: the extract wrote now-vs-before; recompute tight context
        L += ["## %s: %d words before the cut, %d after%s" % (leg, before, now, "" if ok == "yes" else " (UNVERIFIED)"), ""]
        hunks = [l for l in d.splitlines() if not l.startswith(("---", "+++"))]
        L += ["```diff"] + hunks + ["```", ""]
    open(os.path.join(R, sub + ".md"), "w", encoding="utf-8").write("\n".join(L))
    size[sub] = os.path.getsize(os.path.join(R, sub + ".md")) + len(cur.encode())
# batches: rooms in name order, cut by size into nb batches of about equal bytes
total = sum(size.values()); target = total / nb; b, acc, out = first, 0, []
for sub in subs:
    if acc >= target and b < first + nb - 1:
        b, acc = b + 1, 0
    out.append((b, sub)); acc += size[sub]
with open(os.path.join(P, "BATCHES.tsv"), "w", encoding="utf-8") as f:
    f.write("leg\tsub\tcuts\n")
    for b, sub in out:
        f.write("A1b-%02d\t%s\t%s\n" % (b, sub, ",".join(x[0] for x in sorted(by[sub], key=lambda x: int(x[0][4:])))))
c = collections.Counter(b for b, _ in out); kb = collections.Counter()
for b, sub in out: kb[b] += size[sub]
print("rooms %d, review+note bytes %d kB" % (len(subs), total // 1000))
for b in sorted(c): print("A1b-%02d: %d rooms, %d kB" % (b, c[b], kb[b] // 1000))
