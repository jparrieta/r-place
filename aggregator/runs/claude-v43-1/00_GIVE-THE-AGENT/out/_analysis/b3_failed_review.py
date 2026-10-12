#!/usr/bin/env python3
"""B3b: the failed replies read as one set, and the accepted replies screened for the same fault (J, ruling 3 of
the B3b leg message). Reads only; writes out/_analysis/b3_failed_review.json.

Failed replies: out/_fleet_raw/B3/<packet>/<reader>.failed.txt (first line the dispatch's reason, then the reply).
Each is classed by its reason (a concept outside its item; a line not JSON; a count; other), and every concept
it cites, in support, also_present and the multiplacement records, is classed against the item batches-B3 holds
at the line's cell (the batch record the reply was served: the superseded file for B0192 and B0927):
  own        a concept of the item
  packet     a concept of another item of the same packet (and whether that item sits at an adjacent position)
  room       a concept of another item of the same room, not in the packet
  other      a concept of another room
  unknown    not in out/fleet_ids.jsonl
Accepted replies (r*.jsonl with a valid meta): the same classes over pass-1 and pass-2 lines, by field, and the
concept ids written inside the `why` texts, which no check reads.
"""
import collections, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RAW = os.path.join(OUT, "_fleet_raw", "B3")
CID = re.compile(r"C\d{7}")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def fields(x):
    out = [("support", c) for c in x.get("support") or []]
    ap = x.get("also_present")
    if isinstance(ap, dict):
        for v in ap.values():
            out += [("also_present", c) for c in (v if isinstance(v, list) else [v])]
    for r in x.get("multiplacement_log") or []:
        if isinstance(r, dict):
            out += [("multiplacement", c) for c in list(r.get("support_primary") or []) + list(r.get("support_additional") or [])]
    return [(f, c) for f, c in out if isinstance(c, str)]


def main():
    fc, ft = {}, {}
    for r in jl(os.path.join(OUT, "fleet_ids.jsonl")):
        if r["kind"] == "c":
            fc[r["fleet"]] = "%s/%s" % (r["sub"], r["theme"])
        else:
            ft[r["fleet"]] = "%s/%s" % (r["sub"], r["id"])
    batches = {b["batch"]: b for b in jl(os.path.join(OUT, "batches-B3.jsonl"))}
    for old in sorted(glob.glob(os.path.join(OUT, "batches-B3.superseded-*.jsonl")), reverse=True):
        for b in jl(old):
            batches.setdefault(b["batch"], b)

    def classify(c, item, b, pos):
        o = fc.get(c)
        if o is None:
            return "unknown", None
        if o == item:
            return "own", None
        if o in b["items"]:
            ps = [i + 1 for i, x in enumerate(b["items"]) if x == o]
            return "packet", min(abs(p - pos) for p in ps)
        return ("room" if o.split("/")[0] == item.split("/")[0] else "other"), None

    # ---- failed replies
    reasons, cls, dist, per_reply, by_field = collections.Counter(), collections.Counter(), collections.Counter(), [], collections.Counter()
    nonjson_lines, typed_off = 0, 0
    files = sorted(glob.glob(os.path.join(RAW, "*", "*.failed.txt")))
    for f in files:
        pk = os.path.basename(os.path.dirname(f))
        b = batches[pk]
        lines = open(f, encoding="utf-8").read().splitlines()
        why = lines[0]
        kind = ("concept outside the item" if "not among the codes" in why else "not JSON" if "JSON" in why
                else "count" if re.search(r"count|lines|short|expected", why) else "other")
        reasons[kind] += 1
        rec = {"file": os.path.relpath(f, OUT), "why": why, "kind": kind, "bad": collections.Counter()}
        for ln in lines[1:]:
            if not ln.strip():
                continue
            try:
                x = json.loads(ln)
            except ValueError:
                nonjson_lines += 1; continue
            if not isinstance(x, dict) or "position" not in x or "revises" in x:
                continue
            p = x["position"]
            if not isinstance(p, int) or not 1 <= p <= len(b["items"]):
                continue
            item = b["items"][p - 1]
            if ft.get(x.get("theme_id")) != item:
                typed_off += 1
            for fld, c in fields(x):
                k, d = classify(c, item, b, p)
                cls[k] += 1
                if k != "own":
                    rec["bad"][k] += 1; by_field[(fld, k)] += 1
                if k == "packet":
                    dist[d] += 1
        per_reply.append(rec)
    # ---- accepted replies
    acc = collections.Counter()
    acc_lines = acc_lines_bad = why_ids = why_bad = 0
    examples = []
    for d in sorted(os.listdir(RAW)):
        pd = os.path.join(RAW, d)
        if not os.path.isdir(pd) or d not in batches:
            continue
        b = batches[d]
        for f in sorted(os.listdir(pd)):
            if not re.fullmatch(r"r\d+\.jsonl", f):
                continue
            if not json.load(open(os.path.join(pd, f[:-6] + ".meta.json"), encoding="utf-8")).get("valid"):
                continue
            for x in jl(os.path.join(pd, f)):
                if "position" not in x and "revises" not in x:
                    continue
                p = x.get("revises") or x["position"]
                if not isinstance(p, int) or not 1 <= p <= len(b["items"]):
                    continue
                item = b["items"][p - 1]
                pas = "pass2" if "revises" in x else "pass1"
                acc_lines += 1
                bad = False
                for fld, c in fields(x):
                    k, _ = classify(c, item, b, p)
                    acc[(pas, fld, k)] += 1
                    if k not in ("own", "unknown") or (k == "unknown" and FLEET_LIKE(c)):
                        bad = True
                        if len(examples) < 12:
                            examples.append("%s/%s %s position %d: %s %s is %s" % (d, f, pas, p, fld, c, k))
                acc_lines_bad += bad
                for v in (x.get("why") or {}).values():
                    for c in CID.findall(str(v)):
                        why_ids += 1
                        k, _ = classify(c, item, b, p)
                        why_bad += k != "own"
    print("failed replies %d over %d packets; by the dispatch's reason: %s" % (
        len(files), len({r["file"].split("/")[2] for r in per_reply}), dict(reasons)))
    print("lines not JSON inside failed replies: %d; item lines typed off their cell: %d" % (nonjson_lines, typed_off))
    print("concepts cited in failed replies, by class: %s" % dict(cls))
    print("off-item concepts by field and class: %s" % {"%s/%s" % k: v for k, v in sorted(by_field.items())})
    print("packet-neighbour citations by distance in positions from the citing line: %s" % dict(sorted(dist.items())))
    rk = collections.Counter(tuple(sorted(r["bad"])) for r in per_reply)
    print("failed replies by the classes of their off-item concepts: %s" % {"+".join(k) or "none": v for k, v in rk.items()})
    print("accepted replies: %d item lines; lines with an off-item concept %d" % (acc_lines, acc_lines_bad))
    print("accepted, concepts by (pass, field, class): %s" % {"/".join(k): v for k, v in sorted(acc.items())})
    print("concept ids inside why texts: %d, not the item's own %d" % (why_ids, why_bad))
    for e in examples:
        print("  " + e)
    for r in per_reply:
        if r["kind"] != "concept outside the item" or "unknown" in r["bad"] or "other" in r["bad"]:
            print("  %s [%s] %s; off-item %s" % (r["file"], r["kind"], r["why"][:160], dict(r["bad"])))
    json.dump({"failed": len(files), "reasons": reasons, "classes": cls, "packet_distance": dist,
               "by_field": {"%s/%s" % k: v for k, v in by_field.items()},
               "replies": [dict(r, bad=dict(r["bad"])) for r in per_reply],
               "accepted": {"/".join(k): v for k, v in acc.items()}, "accepted_lines": acc_lines,
               "accepted_lines_off_item": acc_lines_bad, "why_ids": why_ids, "why_ids_off_item": why_bad},
              open(os.path.join(OUT, "_analysis", "b3_failed_review.json"), "w", encoding="utf-8"), indent=1)


def FLEET_LIKE(c):
    return bool(re.fullmatch(r"C\d{7}", c))


if __name__ == "__main__":
    main()
