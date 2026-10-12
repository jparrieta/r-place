#!/usr/bin/env python3
"""B3a: the stage B3 packets in fleet ids (J, 2026-10-12: every concept and second-order theme only as its fleet
id, never a room id, headings included), from out/batches-B3.jsonl. packets.py B3 writes room ids, so this
builder renders the same structure (stage B3 sections 1.1 and 1.2) with b2_packets_fleet.py's item renderer:

  _packets-B3/index.md, G01.md ... G21.md   packets.py's scheme_pages on scheme_final.jsonl, no exemplars
  _packets-B3/B017.md                       a batch: title (batch and replicate), the brief, a sibling block per
                                            room (labels of all its second-order themes under fleet ids, labels
                                            only), the items in the batch's order, numbered by position, the end
  _packets-B3/B017-p1.md, -p2.md ...        a batch over the 50 KB ceiling, in parts for one reader in one
                                            conversation, each part with every sibling block, positions running on
Every file is held under 50 KB (FLEET.md). An item larger than a part (leagueoflegends t02) runs over two
consecutive parts of the same reader, its heading repeated with "continued", its line due after the part it ends
in (QB3-001). A gold copy is rendered as any other item and its room gets a sibling block like the batch's rooms,
so no reader can tell it apart; the gold key never reaches the folder. A bag flag is one line under the item.
MANIFEST.json: per file, the items whose lines it is due ("items"), bytes, sha256, count key and excludes,
codes_by_item {fleet theme id: [fleet code ids]}, and for parts group, part and parts. The build stops if any
room id stands anywhere in a file, and if any file is over the ceiling.

    python3 out/_analysis/b3_packets_fleet.py [--write]
"""
import argparse, hashlib, importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)
pk = bpf.pk

CEILING = 50 * 1024
ROOM_ID = re.compile(r"\b(?:c\d{4}|t\d{2,3})\b")
BRIEF = ("Each room is introduced once by the labels of all its second-order themes (the sibling block). Then the "
         "items, interleaved across rooms, numbered by position. Place each item and return one line per item in the "
         "form the return specification gives, the prediction line first. Copy ids exactly as written here.")
BAGLINE = "flagged as a bag: place from the concepts, not from the coder's grouping."


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def sibling(store, tmap, sub):
    ts = sorted(store.by_sub.get(sub, []), key=lambda t: tmap[(sub, t["theme_id"])])
    return (["## r/%s" % sub, "", "sibling block, the labels of all %d second-order themes of this room (labels only):"
             % len(ts)] + ["- %s %s" % (tmap[(sub, t["theme_id"])], t.get("second_order") or "") for t in ts] + [""])


def item_lines(store, cmap, tmap, key, pos, bag):
    s, t = key.split("/")
    L = bpf.render(store, cmap, tmap, s, t, pos)
    if bag:
        L = L[:2] + [BAGLINE, ""] + L[2:]
    return L


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    cmap, tmap = bpf.load_ids()
    store = pk.Store(ROOT, OUT)
    # a room id the coder wrote into a label or a note (one in the store: nyjets t11's note names c0104) is served
    # as its fleet id, the words unchanged; participants' words are never touched
    translated = []
    for (s, t), th in store.themes.items():
        for f in ("second_order", "theme_note"):
            v = str(th.get(f) or "")
            nv = re.sub(r"\b(c\d{4}|t\d{2,3})\b",
                        lambda m: cmap.get((s, m.group(1))) or tmap.get((s, m.group(1))) or m.group(1), v)
            if nv != v:
                th[f] = nv
                translated.append("%s/%s %s" % (s, t, f))
    real = {s: {c for (r, c) in cmap if r == s} | {x for (r, x) in tmap if r == s} for s in store.by_sub}
    batches = jl(os.path.join(OUT, "batches-B3.jsonl"))
    files, man, parted, cont = [], {}, 0, []
    for b in batches:
        name, rep, items = b["batch"], b["replicate"], b["items"]
        bags = set(b.get("bag_flags") or [])
        rooms = list(dict.fromkeys([x.split("/")[0] for x in items]))       # batch rooms and gold copies' rooms
        sib = []
        for r in sorted(rooms):
            sib += sibling(store, tmap, r)
        title = "# Batch %s, replicate %d" % (name, rep)
        blocks = [item_lines(store, cmap, tmap, k, p, k in bags) for p, k in enumerate(items, 1)]
        whole = "\n".join([title, "", BRIEF + " It holds %d items; return %d lines." % (len(items), len(items)), ""]
                          + sib + ["## The items", ""] + [ln for bl in blocks for ln in bl] + ["", pk.END, ""])
        if len(whole.encode("utf-8")) <= CEILING:
            files.append((name, whole, items, {}))
            continue
        # parts: fill each part with whole items under the ceiling; an item larger than a part runs on
        parted += 1
        def head(k, n):
            first = "Write the prediction line first, before any placement. " if k == 1 else "Do not repeat the prediction line. "
            return ["# Batch %s, replicate %d, part %d of %d" % (name, rep, k, n), "",
                    "Batch %s, part %d of %d. You read every part in this one conversation; the parts are one batch. %s%s"
                    % (name, k, n, first, BRIEF.replace(", the prediction line first", "")), ""] + sib + [
                    "## The items, part %d of %d" % (k, n), ""]
        tail_len = 600
        base = len("\n".join(head(9, 9)).encode("utf-8")) + tail_len
        parts, cur, cur_b, due = [], [], base, []
        for p, (k, bl) in enumerate(zip(items, blocks), 1):
            z = len("\n".join(bl).encode("utf-8")) + 1
            if cur and cur_b + z > CEILING:
                parts.append((cur, due)); cur, cur_b, due = [], base, []
            if base + z <= CEILING:
                cur += bl; cur_b += z; due.append(k)
                continue
            # an item larger than a part: its concept lines run over consecutive parts
            hd, body = bl[:6], bl[6:]
            chunk = list(hd)
            cb = base + len("\n".join(chunk).encode("utf-8"))
            for i in range(0, len(body), 2):
                pair = body[i:i + 2]
                pz = len("\n".join(pair).encode("utf-8")) + 1
                if cb + pz > CEILING:
                    parts.append((cur + chunk + ["(item %d continues in the next part; return its line after it)" % p, ""], due))
                    cur, due = [], []
                    chunk = ["### %d. (continued) %s" % (p, bl[0][4:].split(". ", 1)[1]), ""]
                    cb = base + len("\n".join(chunk).encode("utf-8"))
                chunk += pair; cb += pz
            cur = chunk; cur_b = cb; due.append(k)
            cont.append("%s position %d (%s)" % (name, p, k))
        if cur:
            parts.append((cur, due))
        n = len(parts)
        for i, (lines, due) in enumerate(parts, 1):
            last = ("After this part, make your second pass over the whole batch as the return specification says. "
                    if i == n else "Return the lines for this part's items and the end marker; part %d follows. " % (i + 1))
            txt = "\n".join(head(i, n) + lines + ["", last + pk.END, ""])
            files.append(("%s-p%d" % (name, i), txt, due, {"group": name, "part": i, "parts": n}))
    # checks: the ceiling; no actual room id of a room in the file anywhere in it; strings shaped like a room id
    # that are no id of those rooms (participants' own words, such as tank names) are reported, not stopped on
    bad, shaped = [], []
    for name, txt, due, extra in files:
        z = len(txt.encode("utf-8"))
        if z > CEILING:
            bad.append("%s is %d bytes" % (name, z))
        rooms_here = set(re.findall(r"^## r/(\S+)$", txt, re.M))
        ids_here = set().union(*(real.get(r, set()) for r in rooms_here)) if rooms_here else set()
        m = set(ROOM_ID.findall(txt))
        if m & ids_here:
            bad.append("%s carries room ids of its rooms %s" % (name, sorted(m & ids_here)[:5]))
        elif m:
            shaped.append("%s: %s" % (name, sorted(m)))
        if pk.CANVAS.search(txt):
            bad.append("%s carries a canvas field" % name)
    print("coder labels and notes with a room id served as its fleet id: %s" % (translated or "none"))
    print("files with strings shaped like a room id that are no id of their rooms: %s" % (shaped or "none"))
    print("batches %d; files %d; batches in parts %d; items running over two parts: %s" % (
        len(batches), len(files), parted, cont or "none"))
    print("largest file %d bytes" % max(len(t.encode("utf-8")) for _, t, _, _ in files))
    for x in bad[:20]:
        print("  STOP: " + x)
    if bad:
        sys.exit("%d files fail a check" % len(bad))
    if not a.write:
        return
    to = os.path.join(OUT, "_packets-B3")
    if os.path.exists(to) and os.listdir(to):
        sys.exit("%s exists and is not empty" % to)
    rows, sname = pk.load_scheme(OUT, ["scheme_final.jsonl"])
    pk.scheme_pages(ROOT, OUT, to, rows, pk.jl(os.path.join(OUT, "families.jsonl")), False)
    for name, txt, due, extra in files:
        open(os.path.join(to, name + ".md"), "w", encoding="utf-8").write(txt)
        cbi = {}
        for k in due:
            s, t = k.split("/")
            cbi[tmap[(s, t)]] = [cmap[(s, c)] for c in store.themes[(s, t)].get("code_ids") or [] if (s, c) in store.codes]
        e = {"items": len(due), "bytes": len(txt.encode("utf-8")), "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest(),
             "count_key": "position", "count_exclude": pk.COUNT_04["count_exclude"], "codes_by_item": cbi}
        e.update(extra)
        man[name] = e
    json.dump(man, open(os.path.join(to, "MANIFEST.json"), "w", encoding="utf-8"), indent=1)
    shared = [f for f in os.listdir(to) if re.fullmatch(r"(index|G\d\d)\.md", f)]
    print("wrote %s: %d shared pages (largest %d bytes), %d batch files, MANIFEST.json" % (
        to, len(shared), max(os.path.getsize(os.path.join(to, f)) for f in shared), len(files)))


if __name__ == "__main__":
    main()
