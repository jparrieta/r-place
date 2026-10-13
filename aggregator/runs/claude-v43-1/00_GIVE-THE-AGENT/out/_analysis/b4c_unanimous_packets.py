#!/usr/bin/env python3
"""B4c: read packets for the items unanimous in the fleet that a fresh reader placed elsewhere (section 12; notes-B4.md,
"The check (B4c)"): every item with a disagrees-unanimous reading in either arm, from out/_analysis/b4c_figures.json.

Each item shows: its label, the coder's note and each concept (id | label | the participant's words), as `mem.py
theme` gives them; the two B3 readers' agreed list with their why; my B1 grouping; the settled line (third_order, the
themes it places with concepts, its also_present themes, its source); the four fresh readings (two per arm) with their
sets, confidence, why and also_present; and, for every theme any of these names, the frozen scheme's name, must_show
and must_not_show, and the discriminators between two of the named themes.

A summary line says, per fresh reading, whether its set equals the fleet's list, equals the settled set, or neither.
Writes out/_analysis/b4c_unanimous/chunk-NN.md (items in class then room order, at most 60,000 bytes a chunk) and
index.tsv. Dry run (sizes only) without --write.

    python3 out/_analysis/b4c_unanimous_packets.py [--write]
"""
import collections, importlib.util, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(AN, "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)
CAP = 60000
A1, A2 = "deepseek-v4.1-flash", "openai-gpt-6-astra"


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    figs = json.load(open(os.path.join(AN, "b4c_figures.json"), encoding="utf-8"))
    items = figs["unanimous_either_arm"]
    fin = {"%s/%s" % (x["sub"], x["theme_id"]): x for x in jl(os.path.join(OUT, "assign_final.jsonl"))}
    cls = {"%s/%s" % (c["sub"], c["theme_id"]): c for c in jl(os.path.join(OUT, "b3_classes.jsonl"))}
    S = {r["id"]: r for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}
    raw = collections.defaultdict(dict)
    for x in jl(os.path.join(OUT, "assign_raw.jsonl")):
        if x["copy_kind"] == "corpus":
            raw["%s/%s" % (x["sub"], x["theme_id"])][x["replicate"]] = x
    fresh = collections.defaultdict(list)
    for name in ("reassign.jsonl", "reassign-openai-astra.jsonl"):
        for x in jl(os.path.join(OUT, name)):
            fresh[x["item"]].append(x)
    store = bpf.pk.Store(ROOT, OUT)
    items = sorted(items, key=lambda k: (fin[k]["class"], k.lower()))

    def nm(t):
        return "%s %s" % (t, S[t]["name"]) if t in S else t

    blocks = []
    for i, key in enumerate(items, 1):
        s, t = key.split("/")
        th = store.themes[(s, t)]
        c, f = cls[key], fin[key]
        fleet = c["r1"]
        L = ["### %d. %s/%s, class %d, settled source %s" % (i, s, t, c["class"], f.get("source")), "",
             "**%s** | note: %s" % (th.get("second_order"), th.get("theme_note")), ""]
        for cid in th.get("code_ids") or []:
            cd = store.codes.get((s, cid))
            if cd:
                L.append("- %s | %s | %s" % (cid, cd.get("first_order"), " ".join(str(cd.get("text") or "").split())))
        L.append("")
        L.append("**Fleet (both B3 readers):** %s" % ("; ".join(nm(x) for x in fleet) or "(none)"))
        for rep in (1, 2):
            x = raw[key].get(rep) or {}
            why = x.get("why") if isinstance(x.get("why"), dict) else {}
            L.append("- B3 reader %d why: %s" % (rep, " | ".join("%s: %s" % (k, v) for k, v in why.items()) or "-"))
        L.append("**My B1 grouping:** %s" % ("; ".join(nm(x) for x in c.get("b1") or []) or "unplaced"))
        L.append("**Settled line:** %s; placed with concepts: %s; also_present: %s" % (
            "; ".join(nm(x) for x in f.get("third_order") or []) or "(none)",
            ", ".join("%s %s" % (k, " ".join(v)) for k, v in (f.get("support_by_theme") or {}).items()) or "-",
            ", ".join("%s %s" % (k, " ".join(v)) for k, v in (f.get("also_present") or {}).items()) or "-"))
        L.append("")
        named = set(fleet or []) | set(c.get("b1") or []) | set(f.get("third_order") or [])
        summ = []
        for x in sorted(fresh[key], key=lambda x: (x["arm"], x["replicate"])):
            arm = "arm 1" if x["arm"] == A1 else "arm 2"
            F = x["third_order"]
            named |= set(F)
            rel = "= fleet" if set(F) == set(fleet or []) else "= settled" if set(F) == set(f.get("third_order") or []) else "other"
            summ.append("%s r%d %s (%s)" % (arm, x["replicate"], ",".join(F) or "-", rel))
            why = x.get("why") if isinstance(x.get("why"), dict) else {}
            L.append("**Fresh, %s reading %d (%s):** %s; confidence %s%s" % (
                arm, x["replicate"], x["outcome"], "; ".join(nm(y) for y in F) or "(none)", x.get("confidence"),
                "; also_present %s" % ", ".join(x["also_present"]) if x.get("also_present") else ""))
            for y in F:
                L.append("- why %s: %s" % (y, why.get(y, "-")))
        L.append("")
        L.append("**Summary:** " + "; ".join(summ))
        L.append("")
        L.append("**Scheme, for the themes named above:**")
        for y in sorted(named):
            r = S.get(y)
            if not r:
                continue
            L.append("- %s %s (%s). must_show: %s | must_not_show: %s" % (y, r["name"], r["family"], r.get("must_show"), r.get("must_not_show")))
            for d in r.get("discriminators") or []:
                if isinstance(d, dict) and d.get("vs") in named:
                    L.append("  - vs %s: %s" % (d.get("vs"), d.get("question")))
        L.append("")
        blocks.append((key, c["class"], "\n".join(L) + "\n"))
    chunks, cur, size = [], [], 0
    for b in blocks:
        z = len(b[2].encode("utf-8"))
        if cur and size + z > CAP:
            chunks.append(cur); cur, size = [], 0
        cur.append(b); size += z
    if cur:
        chunks.append(cur)
    for k, ch in enumerate(chunks, 1):
        print("chunk %02d: items %d, bytes %d, classes %s" % (k, len(ch), sum(len(b[2].encode("utf-8")) for b in ch),
                                                              dict(collections.Counter(b[1] for b in ch))))
    if "--write" not in sys.argv:
        return
    d = os.path.join(AN, "b4c_unanimous")
    if os.path.exists(d):
        sys.exit("%s exists" % d)
    os.makedirs(d)
    idx = ["n\titem\tclass\tchunk"]
    n = 0
    for k, ch in enumerate(chunks, 1):
        open(os.path.join(d, "chunk-%02d.md" % k), "w", encoding="utf-8").write(
            "# Unanimous items a fresh reader placed elsewhere, chunk %d\n\n" % k + "".join(b[2] for b in ch))
        for b in ch:
            n += 1
            idx.append("%d\t%s\t%d\t%d" % (n, b[0], b[1], k))
    open(os.path.join(d, "index.tsv"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print("wrote %d chunks into %s" % (len(chunks), d))


if __name__ == "__main__":
    main()
