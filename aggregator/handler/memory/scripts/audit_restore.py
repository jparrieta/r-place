"""audit_restore.py: the handler's check of a restore leg (J, 2026-10-07: put back what the 350-word cap cut, from the
record, never from memory). For each room of the leg's batch (pretrim-A1/BATCHES.tsv): the note at the checkpoint
before the leg against the note now; every line added or changed must be made of words the analyst had written,
in the cut versions (pretrim-A1/<sub>__<leg>.md) or in the note before the leg: at least 90% of its word 3-grams
found there. And each room of the batch has a diary note line in the leg (the decision recorded, put back or not).

    python3 audit_restore.py RUN_DIR LEG [EXTRA_SUB ...]
"""
import difflib, glob, json, os, re, sys, tarfile
RUN, LEG = sys.argv[1], sys.argv[2]
AG = os.path.join(RUN, "00_GIVE-THE-AGENT"); OUT = os.path.join(AG, "out"); P = os.path.join(OUT, "_handling", "pretrim-A1")
SNAP = os.path.join(RUN, "CONTROL", "snapshots")
batch = [l.split("\t")[1] for l in open(os.path.join(P, "BATCHES.tsv"), encoding="utf-8").read().splitlines()[1:] if l.split("\t")[0] == LEG]
batch += [x for x in sys.argv[3:] if x not in batch]   # rooms the leg changed outside its batch (2026-10-07, A1b-55)
idx = [l.split("\t") for l in open(os.path.join(SNAP, "INDEX.tsv"), encoding="utf-8").read().splitlines()[1:] if l.strip()]
order = [r[0] for r in sorted(idx, key=lambda r: r[2])]
label = "A1." + LEG
prev = order[order.index(label) - 1] if label in order else order[-1]
want = {"00_GIVE-THE-AGENT/out/rooms/%s.md" % s: s for s in batch}; before = {}
with tarfile.open(os.path.join(SNAP, prev, "fs.tar.gz"), "r:gz") as t:
    for m in t:
        if m.name in want:
            before[want[m.name]] = t.extractfile(m).read().decode("utf-8")
            if len(before) == len(want):
                break
NEUTRAL = {"he": "P", "she": "P", "they": "P", "his": "PP", "her": "PP", "hers": "PP", "their": "PP", "theirs": "PP",
           "him": "PO", "them": "PO", "himself": "PR", "herself": "PR", "themselves": "PR", "themself": "PR",
           "was": "BE", "were": "BE", "is": "BE2", "are": "BE2", "has": "HV", "have": "HV"}
# a gendered pronoun made neutral (the analyst's own policy, logged) is not new wording (2026-10-07, after A1b-50)
grams = lambda s: [tuple(w) for w in zip(*([NEUTRAL.get(x, x) for x in re.findall(r"\w+", s.lower())][i:] for i in range(3)))]
noted = set()
for f in glob.glob(os.path.join(OUT, "diary", "A1-*.jsonl")):
    for l in open(f, encoding="utf-8"):
        try:
            o = json.loads(l)
        except ValueError:
            continue
        if str(o.get("leg") or "").startswith(LEG) and o.get("kind") == "note":
            noted |= {str(i).lower() for i in o.get("ids") or []}
probs, changed, put = [], 0, 0
for sub in batch:
    src = before.get(sub, "")
    for f in glob.glob(os.path.join(P, "%s__A1b-*.md" % sub)):
        m = re.search(r"## Before the cut\n\n```\n(.*?)```", open(f, encoding="utf-8").read(), re.S)
        src += "\n" + (m.group(1) if m else "")
    have = set(grams(src))
    now = open(os.path.join(OUT, "rooms", sub + ".md"), encoding="utf-8").read()
    if now != before.get(sub):
        changed += 1
        added = [l[1:] for l in difflib.unified_diff(before.get(sub, "").splitlines(), now.splitlines(), lineterm="")
                 if l.startswith("+") and not l.startswith("+++")]
        for line in added:
            g = grams(line)
            if g:
                share = sum(x in have for x in g) / len(g)
                if share < 0.9:
                    probs.append("%s: a line %.0f%% from the record: %s" % (sub, 100 * share, line[:120]))
        put += 1
    if sub.lower() not in noted:
        probs.append("%s: no note line in %s (the decision is not recorded)" % (sub, LEG))
print("%s: %d rooms in the batch, %d notes changed, %d problem(s)" % (LEG, len(batch), changed, len(probs)))
for p in probs[:30]:
    print("  " + p)
print("problems %d" % len(probs))
