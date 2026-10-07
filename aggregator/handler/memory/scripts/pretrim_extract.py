"""pretrim_extract.py: the A1 catch-up notes as the analyst wrote them before the 350-word hook made it cut them
(J, 2026-10-07, 10:10 Berlin: "go ahead"). Nothing is reconstructed from memory: each note is replayed from the
checkpoint before the leg (CONTROL/snapshots/<prev>/fs.tar.gz) through the leg's own Write/Edit/MultiEdit calls in
its transcript (out/_transcripts/leg-A1.<leg>-*.jsonl); the replay must end on the note the leg's checkpoint holds,
or the room is marked unverified. The fullest state the hook refused for length is the pre-trim note.

    python3 pretrim_extract.py RUN_DIR LEG [LEG ...]      e.g. A1b-20 A1b-21 ...   (writes out/_handling/pretrim-A1/<sub>__<leg>.md and INDEX.tsv)
"""
import difflib, glob, io, json, os, re, sys, tarfile

RUN = sys.argv[1]; LEGS = sys.argv[2:]
AG = os.path.join(RUN, "00_GIVE-THE-AGENT"); OUT = os.path.join(AG, "out", "_handling", "pretrim-A1")
SNAP = os.path.join(RUN, "CONTROL", "snapshots")
LONG = re.compile(r"rooms/([^/\s]+)\.md, fix it now:.*?is (\d+) words; the form is under 350", re.S)
os.makedirs(OUT, exist_ok=True)
idx = [l.split("\t") for l in open(os.path.join(SNAP, "INDEX.tsv"), encoding="utf-8").read().splitlines()[1:] if l.strip()]
order = [r[0] for r in sorted(idx, key=lambda r: r[2])]


def notes_at(label, subs):
    want = {"00_GIVE-THE-AGENT/out/rooms/%s.md" % s: s for s in subs}
    got = {}
    with tarfile.open(os.path.join(SNAP, label, "fs.tar.gz"), "r:gz") as t:
        for m in t:
            if m.name in want:
                got[want[m.name]] = t.extractfile(m).read().decode("utf-8")
                if len(got) == len(want):
                    break
    return got


def events(path, t0, t1):
    """(tool_use_id, sub, kind, input) for note writes in order; results by id; length refusals by id. Only entries
    stamped inside the leg (after the previous close, up to this close): a resumed session carries earlier legs."""
    uses, results, refused = [], {}, {}
    for l in open(path, encoding="utf-8"):
        try:
            o = json.loads(l)
        except ValueError:
            continue
        ts = str(o.get("timestamp") or "")[:19]
        if not ts or ts <= t0 or ts > t1:
            continue
        a = o.get("attachment") or {}
        if a.get("type") == "hook_blocking_error":
            m = LONG.search(json.dumps(a.get("blockingError") or {}).replace("\\n", "\n"))
            if m:
                refused[a.get("toolUseID")] = int(m.group(2))
        msg = o.get("message") or {}
        c = msg.get("content") if isinstance(msg, dict) else None
        if not isinstance(c, list):
            continue
        for x in c:
            if x.get("type") == "tool_use" and x.get("name") in ("Write", "Edit", "MultiEdit"):
                fp = str((x.get("input") or {}).get("file_path") or "")
                m = re.search(r"out/rooms/([^/]+)\.md$", fp)
                if m:
                    uses.append((x["id"], m.group(1), x["name"], x["input"]))
            elif x.get("type") == "tool_result":
                body = json.dumps(x.get("content"))
                results[x.get("tool_use_id")] = not (x.get("is_error") or "tool_use_error" in body)
    return uses, results, refused


def apply(text, name, inp):
    if name == "Write":
        return inp.get("content", "")
    edits = inp.get("edits") if name == "MultiEdit" else [inp]
    for e in edits:
        old, new = e.get("old_string", ""), e.get("new_string", "")
        if old not in text:
            raise ValueError("old_string not found")
        text = text.replace(old, new) if e.get("replace_all") else text.replace(old, new, 1)
    return text


rows = []
for leg in LEGS:
    label = "A1." + leg
    tr = sorted(glob.glob(os.path.join(AG, "out", "_transcripts", "leg-%s-*.jsonl" % label)))
    if label not in order or not tr:
        print("%s: no checkpoint or transcript" % leg); continue
    prev = order[order.index(label) - 1]
    closed = {r[0]: r[2][:19] for r in idx}
    uses, results, refused = [], {}, {}
    for p in tr:
        u, r, f = events(p, closed[prev], closed[label]); uses += u; results.update(r); refused.update(f)
    subs = sorted({s for _, s, _, _ in uses})
    start, end = notes_at(prev, subs), notes_at(label, subs)
    n_room = 0
    for sub in subs:
        if not any(i in refused for i, s, _, _ in uses if s == sub):
            continue
        n_room += 1
        state, ok, fullest, fullest_w = start.get(sub, ""), True, None, -1
        for i, s, name, inp in uses:
            if s != sub or results.get(i) is False:
                continue
            try:
                state = apply(state, name, inp)
            except ValueError:
                ok = False; break
            if i in refused and len(state.split()) > fullest_w:
                fullest, fullest_w = state, len(state.split())
        verified = ok and state == end.get(sub)
        now = end.get(sub, "")
        diff = "".join(difflib.unified_diff(now.splitlines(True), (fullest or "").splitlines(True),
                                            "rooms/%s.md (now)" % sub, "rooms/%s.md (before the cut, %s)" % (sub, leg)))
        with open(os.path.join(OUT, "%s__%s.md" % (sub, leg)), "w", encoding="utf-8") as f:
            f.write("# r/%s: the note before the 350-word cut\n\n" % sub)
            f.write("Leg %s. Replayed from the checkpoint before the leg (%s) through the leg's own edits; %s.\n"
                    "Before the cut %d words; now %d. The note before the cut, then the change from now to it.\n\n"
                    % (leg, prev, "the replay ends on the note the leg's checkpoint holds (verified)" if verified
                       else "UNVERIFIED: the replay does not end on the checkpoint's note, so trust only the diff's lines you can confirm",
                       fullest_w, len(now.split())))
            f.write("## Before the cut\n\n```\n%s```\n\n## From now to before the cut\n\n```diff\n%s```\n" % (fullest or "", diff))
        rows.append((sub, leg, fullest_w, len(now.split()), "yes" if verified else "no"))
    print("%s: %d note(s) cut by the hook" % (leg, n_room))
ip = os.path.join(OUT, "INDEX.tsv")
old = [l for l in (open(ip).read().splitlines()[1:] if os.path.exists(ip) else []) if l.split("\t")[1] not in LEGS]  # rows of other legs kept
with open(ip, "w", encoding="utf-8") as f:
    f.write("sub\tleg\twords_before_cut\twords_now\treplay_verified\n")
    for l in old:
        f.write(l + "\n")
    for r in rows:
        f.write("\t".join(map(str, r)) + "\n")
print("rows %d, verified %d" % (len(rows), sum(r[4] == "yes" for r in rows)))
