#!/usr/bin/env python3
"""B4a: the adjudication packets of stage B4 (sections 1, 6 and 7), from out/_analysis/b4_prepare.json's packet plan,
out/b3_classes.jsonl, the corpus lines of out/assign_raw.jsonl and out/multiplacement_log.jsonl, and the store.

Blindness (section 6), by this script since no v38 tool strips: agent, batch, replicate, position, the timestamps and
the dispatch's reader ids never reach the packet. The two readings are shown as A and B in an order seeded per item
(sha256 of "20261016:" + item), so the replicate cannot be read off the order. Each reading keeps its set, confidence,
read, families_opened, bag, also_present, its `why` per theme and, for an added theme, the record's why_not_one.
My B1 grouping is shown as the third placement (J's three placements), labelled as mine.

The item is rendered as `mem.py theme` gives it: label, the coder's theme_note, and each concept as id | label |
the participant's words (member, hour and thread dropped).

Writes out/_adjudication-B4/packet-NN/chunk-KK.md (25 items each), packet-NN/index.tsv (n, item, class, chunk, A is
replicate) and packet-NN/notes.md (the conflicts pass: the theme_notes alone, grouped by the readings' primaries).
index.tsv's last column is the unblinding key; I do not read it while I rule (the append script reads it).
"""
import collections, hashlib, importlib.util, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(AN, "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)
CHUNK = 25


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    plan = json.load(open(os.path.join(AN, "b4_prepare.json"), encoding="utf-8"))["packets"]
    cls = {"%s/%s" % (c["sub"], c["theme_id"]): c for c in jl(os.path.join(OUT, "b3_classes.jsonl"))}
    S = {r["id"]: r for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}
    lines = collections.defaultdict(dict)
    for x in jl(os.path.join(OUT, "assign_raw.jsonl")):
        if x["copy_kind"] == "corpus":
            lines["%s/%s" % (x["sub"], x["theme_id"])][x["replicate"]] = x
    recs = collections.defaultdict(list)
    for m in jl(os.path.join(OUT, "multiplacement_log.jsonl")):
        if m.get("copy_kind") == "corpus":
            recs[(m["batch"], m["position"])].append(m)
    store = bpf.pk.Store(ROOT, OUT)
    base = os.path.join(OUT, "_adjudication-B4")
    if os.path.exists(base) and "--write" in sys.argv:
        sys.exit("%s exists" % base)

    def name(t):
        return "%s %s" % (t, S[t]["name"]) if t in S else t

    def reading(tag, x):
        s = x.get("third_order") or []
        out = ["**Reading %s:** %s (confidence %s; read %s; families opened %s%s)" % (
            tag, "; ".join(name(t) for t in s) or "(none)", x.get("confidence"), x.get("read"),
            ",".join(x.get("families_opened") or []) or "-", "; flagged a bag" if x.get("bag") else "")]
        why = x.get("why") if isinstance(x.get("why"), dict) else {}
        for t in s:
            out.append("- why %s: %s" % (t, why.get(t, "-")))
        # the line's support list is left out: the append script takes each placed theme's concepts from the line
        for m in recs.get((x["batch"], x["position"]), []):
            out.append("- added %s, own concepts %s; why_not_one: %s" % (
                m.get("additional"), " ".join(m.get("support_additional") or []), m.get("why_not_one")))
        ap = x.get("also_present") or {}
        if ap:
            out.append("- also_present: %s" % "; ".join("%s %s" % (t, " ".join(v or [])) for t, v in ap.items()))
        return out

    for p in plan:
        n = p["packet"]
        pdir = os.path.join(base, "packet-%02d" % n)
        chunks, index, notes = collections.defaultdict(list), [], collections.defaultdict(list)
        for i, key in enumerate(p["items"], 1):
            c = cls[key]
            s, t = key.split("/")
            th = store.themes[(s, t)]
            ab = hashlib.sha256(("20261016:" + key).encode()).digest()[0] % 2
            first, second = (1, 2) if ab == 0 else (2, 1)
            L = ["### %d. %s/%s, class %d%s" % (i, s, t, c["class"], ", a placement from a family neither reader opened" if c["flags"].get("unopened_family") else ""),
                 "", "**%s** | note: %s" % (th.get("second_order"), th.get("theme_note")), ""]
            for cid in th.get("code_ids") or []:
                cd = store.codes.get((s, cid))
                if cd:
                    L.append("- %s | %s | %s" % (cid, cd.get("first_order"), " ".join(str(cd.get("text") or "").split())))
            L.append("")
            L += reading("A", lines[key][first]) + [""] + reading("B", lines[key][second]) + [""]
            L.append("**B1 grouping (mine, at B1):** %s" % ("; ".join(name(x) for x in c["b1"]) or "unplaced"))
            L.append("")
            k = (i - 1) // CHUNK + 1
            chunks[k] += L
            index.append("%d\t%s\t%d\t%d\t%d" % (i, key, c["class"], k, first))
            prims = sorted({(c["r1"] or ["-"])[0], (c["r2"] or ["-"])[0]})
            notes[" / ".join(prims)].append("- %s/%s (%s): %s" % (s, t, th.get("second_order"), th.get("theme_note")))
        sizes = [len("\n".join(v).encode()) for v in chunks.values()]
        print("packet %d: %d items, %d chunks, chunk bytes min %d max %d, total %d" % (n, len(p["items"]), len(chunks), min(sizes), max(sizes), sum(sizes)))
        if "--write" in sys.argv:
            os.makedirs(pdir)
            for k, v in chunks.items():
                open(os.path.join(pdir, "chunk-%02d.md" % k), "w", encoding="utf-8").write(
                    "# Adjudication packet %d, chunk %d\n\n" % (n, k) + "\n".join(v) + "\n")
            open(os.path.join(pdir, "index.tsv"), "w", encoding="utf-8").write("n\titem\tclass\tchunk\tA_is_replicate\n" + "\n".join(index) + "\n")
            nl = ["# Packet %d: the coders' theme notes alone, grouped by the readings' primaries (the conflicts pass)" % n, ""]
            for g in sorted(notes, key=lambda g: (-len(notes[g]), g)):
                nl += ["## %s (%d)" % (g, len(notes[g])), ""] + notes[g] + [""]
            open(os.path.join(pdir, "notes.md"), "w", encoding="utf-8").write("\n".join(nl))


if __name__ == "__main__":
    main()
