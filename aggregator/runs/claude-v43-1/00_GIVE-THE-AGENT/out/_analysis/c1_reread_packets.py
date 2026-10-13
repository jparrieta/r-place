#!/usr/bin/env python3
"""C1a-01: read packets for the class 4 rulings that rest on "the earlier reading" (notes-C1.md, "The re-reads"), the
five J named first (chicago t01, armok t04, dmt t03, germany t08, smashbros t01), then the others in room order.

Each item shows: its label, the coder's note and each concept (id | label | the participant's words); both B3
readings with their why; my B1 grouping; the B4a-06 ruling's why; the fresh readings of B4c with their sets and why
(b4c_readings.jsonl); and the frozen scheme's name, must_show and must_not_show for every theme named, with the
discriminators between two named themes. Writes out/_analysis/c1_reread/chunk-NN.md (at most 60,000 bytes a chunk)
and index.tsv. Dry run (sizes) without --write.

    python3 out/_analysis/c1_reread_packets.py [--write]
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
FIRST = [("chicago", "t01"), ("armok", "t04"), ("dmt", "t03"), ("germany", "t08"), ("smashbros", "t01")]


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    dis = [d for d in jl("disagreements.jsonl") if "earlier reading" in str(d.get("why") or "")]
    keys = [(d["sub"], d["theme_id"]) for d in dis]
    if not set(FIRST) <= set(keys):
        sys.exit("the five are not all among the rulings resting on the earlier reading")
    order = FIRST + sorted((k for k in keys if k not in FIRST), key=lambda k: (k[0].lower(), k[1]))
    dk = {(d["sub"], d["theme_id"]): d for d in dis}
    cls = {(c["sub"], c["theme_id"]): c for c in jl("b3_classes.jsonl")}
    S = {r["id"]: r for r in jl("scheme_final.jsonl")}
    raw = collections.defaultdict(dict)
    for x in jl("assign_raw.jsonl"):
        if x["copy_kind"] == "corpus":
            raw[(x["sub"], x["theme_id"])][x["replicate"]] = x
    fresh = collections.defaultdict(list)
    for x in jl(os.path.join("_analysis", "b4c_readings.jsonl")):
        fresh[(x["sub"], x["theme_id"])].append(x)
    store = bpf.pk.Store(ROOT, OUT)

    def nm(t):
        return "%s %s" % (t, S[t]["name"]) if t in S else t

    blocks = []
    for i, k in enumerate(order, 1):
        s, t = k
        th = store.themes[k]
        c, d = cls[k], dk[k]
        L = ["### %d. %s/%s, class %d%s" % (i, s, t, c["class"], " (one of the five J named)" if k in FIRST else ""), "",
             "**%s** | note: %s" % (th.get("second_order"), th.get("theme_note")), ""]
        for cid in th.get("code_ids") or []:
            cd = store.codes.get((s, cid))
            if cd:
                L.append("- %s | %s | %s" % (cid, cd.get("first_order"), " ".join(str(cd.get("text") or "").split())))
        L.append("")
        named = set(c.get("r1") or []) | set(c.get("r2") or []) | set(c.get("b1") or [])
        for rep in (1, 2):
            x = raw[k].get(rep) or {}
            why = x.get("why") if isinstance(x.get("why"), dict) else {}
            L.append("**B3 reader %d:** %s; %s; support %s; also_present %s" % (
                rep, "; ".join(nm(y) for y in x.get("third_order") or []) or "(none)", x.get("confidence"),
                " ".join(x.get("support") or []), ", ".join((x.get("also_present") or {}).keys()) or "-"))
            for y, w in why.items():
                L.append("- why %s: %s" % (y, w))
        L.append("**My B1 grouping:** %s" % ("; ".join(nm(y) for y in c.get("b1") or []) or "unplaced"))
        L.append("**The B4a-06 ruling:** unresolved; taxonomy %s. Why: %s" % (d.get("taxonomy"), d.get("why")))
        L.append("")
        for x in sorted(fresh.get(k, []), key=lambda x: (x["arm"], x["stratum"], x["replicate"])):
            arm = "arm 1" if x["arm"].startswith("deepseek") else "arm 2"
            named |= set(x["third_order"])
            why = x.get("why") if isinstance(x.get("why"), dict) else {}
            L.append("**Fresh, %s, %s packet, reading %d:** %s; %s" % (
                arm, "an R" if x["stratum"] == "R" else "a %s" % x["stratum"], x["replicate"],
                "; ".join(nm(y) for y in x["third_order"]) or "(none)", x.get("confidence")))
            for y, w in why.items():
                L.append("- why %s: %s" % (y, " ".join(str(w).split())))
        L.append("")
        L.append("**Scheme, for the themes named above:**")
        for y in sorted(named):
            r = S.get(y)
            if not r:
                continue
            L.append("- %s %s (%s). must_show: %s | must_not_show: %s" % (y, r["name"], r["family"], r.get("must_show"), r.get("must_not_show")))
            if r.get("decide_when_both"):
                L.append("  - decide_when_both: %s" % r.get("decide_when_both"))
            for dd in r.get("discriminators") or []:
                if isinstance(dd, dict) and dd.get("vs") in named:
                    L.append("  - vs %s: %s" % (dd.get("vs"), dd.get("question")))
        L.append("")
        blocks.append((k, "\n".join(L) + "\n"))
    chunks, cur, size = [], [], 0
    for b in blocks:
        z = len(b[1].encode("utf-8"))
        if cur and (size + z > CAP or (len(cur) == len(FIRST) and cur[-1][0] in FIRST and b[0] not in FIRST)):
            chunks.append(cur); cur, size = [], 0
        cur.append(b); size += z
    if cur:
        chunks.append(cur)
    for n, ch in enumerate(chunks, 1):
        print("chunk %02d: items %d, bytes %d" % (n, len(ch), sum(len(b[1].encode("utf-8")) for b in ch)))
    if "--write" not in sys.argv:
        return
    dd = os.path.join(AN, "c1_reread")
    if os.path.exists(dd):
        sys.exit("%s exists" % dd)
    os.makedirs(dd)
    idx = ["n\titem\tchunk"]
    n = 0
    for c, ch in enumerate(chunks, 1):
        open(os.path.join(dd, "chunk-%02d.md" % c), "w", encoding="utf-8").write(
            "# C1a-01 re-reads, chunk %d\n\n" % c + "".join(b[1] for b in ch))
        for b in ch:
            n += 1
            idx.append("%d\t%s/%s\t%d" % (n, b[0][0], b[0][1], c))
    open(os.path.join(dd, "index.tsv"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print("wrote %d chunks into %s" % (len(chunks), dd))


if __name__ == "__main__":
    main()
