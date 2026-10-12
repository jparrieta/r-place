#!/usr/bin/env python3
"""assemble.py: stage B3's check leg reads the fleet's returns into the files stage B4 inherits.

    python3 tools/assemble.py B3 [--root .] [--out out] [--families F] [--dry-run] [--supersede]
                                 [--accept-sub-label]

Written from stages/STAGE-B3-coding-fleet.md (sections 1.5, 1.6, 2, 3 and 3.1: "assemble assign_raw.jsonl,
assign_pass2.jsonl and multiplacement_log.jsonl from the returns, keyed on packet heading and cell number, with
the typed theme id as a label"), and from the orchestrator's note of 2026-10-12T19:00Z carrying J's rulings of
12 October on stage B4 (the three placements, the five classes). The analyst runs it; it lives in the analyst's
tools, imports vlib and never fleet.py, which the analyst's copy lacks (fleet.counted's rule is copied below,
word for word, as checks/stage_B3.py copies it).

What it reads, and only that:
  - the ACCEPTED returns: out/_fleet_raw/B3/<batch>/r<k>.jsonl (also under a dispatch group folder,
    out/_fleet_raw/B3/batch-k/<batch>/), never <reader>.failed.txt or <reader>.raw.txt; each with its
    r<k>.meta.json (the reissue number, the reader id the dispatch gave, the packet's elapsed seconds). A packet
    with more than one accepted r*.jsonl is refused by name: which reading is the batch's is not this tool's
    call. A batch with no accepted return is named, as exhausted (EXHAUSTED.tsv) or as missing;
  - out/batches-B3.jsonl: the authority on a batch's agent, replicate, items by position, gold copies and
    duplicate;
  - out/fleet_ids.jsonl through vlib.fleet_table: the fleet's ids (T2-nnnnn, C+7 digits) back to room ids;
  - out/_packets-B3/MANIFEST.json for each packet's count rule (count_key, count_exclude);
  - package/store/themes.jsonl (through vlib's recut overlay, out/recut/WITHDRAWN.json honoured) and
    out/scheme/scheme_current.jsonl for the B1 grouping; the families file for families_opened.

What it writes (nothing with --dry-run):
  out/assign_raw.jsonl              the pass-1 item lines, in batch then position order
  out/assign_pass2.jsonl            the lines carrying "revises", position set to the pass-1 cell they revise
  out/multiplacement_log.jsonl      every multiplacement record, riding on its item line as
                                    "multiplacement_log" (kept there as well) or sent as a line of its own
  out/predicted_confusion-B3.jsonl  the prediction lines
  out/b3_classes.jsonl              one line per item of the analysed set: its class, 1 to 5
Every line carries batch, agent, replicate, position, copy_kind, reissue and reader. agent and replicate are
batches-B3.jsonl's (the batch's agent id, a0001): the dispatch's reader ids (r1, r6 ...) are reused across
packets by one dispatch run, each packet a fresh context, so r6 is not one reader, and "no reader in two
replicates of an item" can only be checked on the batch's agent. The id the dispatch gave is kept as
`reader`, the agent the reader typed as `fleet_agent`, and a replicate typed otherwise than the batch's as
`replicate_typed`. An existing output is never overwritten: the tool refuses unless --supersede, which first
renames each old file to <name>.superseded-<utc> (never deleted).

The ids (the handler's brief, 2026-10-12). theme_id T2-nnnnn becomes tNN and sub the theme's room; every concept
C+7 digits in support, also_present, support_primary and support_additional becomes cNNNN; a multiplacement
record's sub, theme_id and key likewise. The fleet's ids stay beside them: fleet_sub, fleet_theme_id,
fleet_support, fleet_also_present, fleet_support_primary, fleet_support_additional, fleet_key. A leading "r/"
is stripped from sub. Refused, naming the line, with a non-zero exit and nothing written:
  - an id the table cannot resolve (a theme or a concept);
  - a typed sub that is not the room of the theme the id names (unless --accept-sub-label, below);
  - a concept of another room;
  - a theme id that is not the item batches-B3.jsonl holds at that cell (the cell is the key, the id a label);
  - a multiplacement record naming another item than its line.
--accept-sub-label lets a typed sub that disagrees with the theme's room through, only where the theme id
and the cell both name the same item, so the item's identity rests on two keys that agree; each such line
keeps the typed room as `sub_typed`, and the tool lists them. It is off by default, and using it is a choice
to report.
The readers' t_start and t are dropped: readers invent them (on the 2026-10-12 run every line read
2026-05-09T00:00:00Z). The measured time is the dispatch's, the packet's elapsed seconds from its meta, carried
on every line as `packet_elapsed_s` (per packet, not per item).

copy_kind, from batches-B3.jsonl (J's ruling via the orchestrator, 2026-10-12: "no seeded copy counts as a
corpus reading"). Walking a batch's items by position: an item's live occurrences come first, the first of
them "corpus" and the second, for the batch's declared duplicate only, "duplicate"; occurrences beyond the
live count are the batch's gold copies, "gold". Where a batch holds an item both live and as a gold copy, the
position of the gold copy is not recorded anywhere, so the first occurrence is taken as the live one; the
tool says how many such batches it met.

The B1 grouping (the note, "The three placements"): the set of third-order themes in scheme_current.jsonl
whose members include the item, matched by (sub, second-order label) through package/store/themes.jsonl. The
sha256 of scheme_current.jsonl is recorded on every class line (expected prefix 8b67360b8d0dfefc; another is
warned). Members that match by label but whose theme_id disagrees with the store, members that match no
label, and labels that name more than one theme of a room are counted and the first named.

The classes (J, 12 October; the orchestrator's note, "The rule, replacing section 1's ..."). For each item of
the analysed set, the corpus copies only, pass 1, replicate 1 against replicate 2; a list is third_order in
its order, a set is its themes:
  5  the item has no B1 grouping (checked first: it is the item's own attribute, whatever the readers did;
     "58 at B1" counts these);
  3  a replicate is missing (its packet in EXHAUSTED.tsv or with no return): it cannot be agreed, so it goes to
     B4, flagged missing_replicate and counted apart;
  1  the two lists are equal, order included, and the set equals the B1 grouping: the readers' list stands;
  2  the two lists are equal and the set is a proper subset of the B1 grouping: the B1 grouping stands, the
     readers' list first, then B1's other themes in ascending id order (T3-nnn), source "b1_grouping_kept";
  3  the lists differ, including the same themes in another order;
  4  the lists are equal and the set is not inside the B1 grouping.
An agreed empty list (no placement) is class 3, flagged. Classes 1 and 2 stand without adjudication; 3, 4
and 5 go to stage B4. The unopened-family flag is set whatever the class (section 1's other rule stands): a
placement by either reader whose family is in neither reader's families_opened. The family of a theme is read
from --families, else out/families.jsonl, out/scheme/families.jsonl, else a "family" field on the scheme's
rows; with none, the flag is null and the tool says it was not computed.
"""
import argparse, collections, datetime, glob, hashlib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vlib
from vlib import E, W, err, warn, jsonl, fold

B1_SHA_EXPECTED = "8b67360b8d0dfefc"           # the note, "The three placements"
COUNT_DEFAULT = {"count_key": "position", "count_exclude": ["primary", "revises", "predicted_confusion"]}
ACCEPTED = re.compile(r"^r\d+\.jsonl$")
FLEET_T = re.compile(r"^T2-\d+$")
FLEET_C = re.compile(r"^C\d{7}$")
OUTPUTS = ("assign_raw.jsonl", "assign_pass2.jsonl", "multiplacement_log.jsonl", "predicted_confusion-B3.jsonl",
           "b3_classes.jsonl")
DROP = ("t_start", "t")


def counted(o, rule):
    """fleet.counted, word for word (the analyst's tools have no fleet.py)."""
    key = rule.get("count_key")
    if not key:
        return True
    if key not in o or any(k in o for k in rule.get("count_exclude", [])):
        return False
    return o.get("pass", 1) in (1, "1", None)


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def split_key(k):
    if isinstance(k, dict):
        return (k.get("sub"), k.get("theme_id"))
    if isinstance(k, str) and "/" in k:
        a, b = k.split("/", 1)
        return (a, b)
    return (None, None)


def strip_r(s):
    return s[2:] if isinstance(s, str) and s.startswith("r/") else s


def path_in(base, p):
    return p if os.path.isabs(p) or os.path.exists(p) else os.path.join(base, p)


# ---- the returns -----------------------------------------------------------------------------------------------

def packet_folders(raw, batches):
    """{batch: [folder, ...]}: every folder under out/_fleet_raw/B3/ named after a batch, at any depth (a dispatch
    group folder batch-k/ holds its packets one level down)."""
    out = collections.defaultdict(list)
    for d, subdirs, _files in os.walk(raw):
        subdirs.sort()
        name = os.path.basename(d)
        if name in batches and d != raw:
            out[name].append(d)
    return out


def exhausted(raw):
    """Packets EXHAUSTED.tsv lists (anywhere under the raw folder), {packet: why}."""
    out = {}
    for p in glob.glob(os.path.join(raw, "**", "EXHAUSTED.tsv"), recursive=True):
        for i, ln in enumerate(open(p, encoding="utf-8")):
            f = ln.rstrip("\n").split("\t")
            if i == 0 and f and f[0] == "packet":
                continue
            if f and f[0]:
                out[f[0]] = f[2] if len(f) > 2 else ""
    return out


def copy_kinds(b):
    """[copy_kind by position] for a batch line (positions 1..n are indexes 0..n-1)."""
    items = [split_key(x) for x in as_list(b.get("items"))]
    gold = collections.Counter(split_key(g) for g in as_list(b.get("gold_items")))
    live = collections.Counter(items)
    live.subtract(gold)
    dups = {split_key(x) for x in as_list(b.get("duplicate_items"))}
    seen = collections.Counter()
    kinds = []
    for k in items:
        if seen[k] < max(live[k], 0):
            kinds.append("corpus" if seen[k] == 0 else ("duplicate" if k in dups else "corpus-repeated"))
        else:
            kinds.append("gold")
        seen[k] += 1
    return kinds, items, any(gold[k] and live[k] > 0 for k in gold)


class Translator:
    def __init__(self, by_fleet, accept_sub_label):
        self.t = by_fleet
        self.accept = accept_sub_label
        self.sub_label = []          # (where, typed, room)

    def theme(self, fid, where, what="theme_id"):
        e = self.t.get(fid) if isinstance(fid, str) else None
        if not e or e.get("kind") != "t":
            err("%s: %s %r does not resolve in out/fleet_ids.jsonl; an id the table cannot resolve is refused, not "
                "carried" % (where, what, fid), shape="assemble: a theme id the fleet table cannot resolve", where=where)
            return None
        return e

    def concepts(self, ids, sub, where, field):
        out = []
        for x in as_list(ids):
            e = self.t.get(x) if isinstance(x, str) else None
            if not e or e.get("kind") != "c":
                err("%s: %s holds %r, which does not resolve in out/fleet_ids.jsonl as a concept"
                    % (where, field, x), shape="assemble: a concept id the fleet table cannot resolve", where=where)
                out.append(x)
            elif sub is not None and e["sub"] != sub:
                err("%s: %s holds %s, a concept of r/%s, not of r/%s, the item's room"
                    % (where, field, x, e["sub"], sub), shape="assemble: a concept of another room", where=where)
                out.append("%s:%s" % (e["sub"], e["id"]))
            else:
                out.append(e["id"])
        return out

    def sub_check(self, typed, room, where, cell_ok):
        if typed == room:
            return True
        if self.accept and cell_ok:
            self.sub_label.append((where, typed, room))
            return True
        err("%s: the line types sub %r and its theme id names a theme of r/%s; a mismatch is refused%s"
            % (where, typed, room, " (the cell and the id agree on the item; --accept-sub-label would carry it with "
               "sub_typed)" if cell_ok else ""), shape="assemble: a typed sub off the theme's room", where=where)
        return False


def translate_record(m, line, tr, where):
    """A multiplacement record, read into room ids against its item line (already translated)."""
    m = dict(m)
    fid = m.get("theme_id")
    if fid is not None and fid != line["fleet_theme_id"]:
        e = tr.theme(fid, where, "multiplacement record theme_id")
        if e and (e["sub"], e["id"]) != (line["sub"], line["theme_id"]):
            err("%s: a multiplacement record names %s/%s and rides on the line of %s/%s"
                % (where, e["sub"], e["id"], line["sub"], line["theme_id"]),
                shape="assemble: a multiplacement record off its line", where=where)
    for f in ("sub", "theme_id", "key"):
        if f in m:
            m["fleet_" + f] = m[f]
    m["sub"], m["theme_id"] = line["sub"], line["theme_id"]
    m["key"] = "%s/%s" % (line["sub"], line["theme_id"])
    for f in ("support_primary", "support_additional"):
        if f in m:
            m["fleet_" + f] = m[f]
            m[f] = tr.concepts(m[f], line["sub"], where, f)
    for f in ("batch", "agent", "replicate", "position"):
        if f in m and m[f] != line[f]:
            m["fleet_" + f if f != "replicate" else "replicate_typed"] = m[f]
    for f in ("batch", "agent", "replicate", "position", "copy_kind", "reissue", "reader"):
        m[f] = line[f]
    return m


def read_returns(out, raw, by_batch, manifest, tr):
    """(pass-1 lines, pass-2 lines, multiplacement records, prediction lines, stats)."""
    folders = packet_folders(raw, by_batch)
    ex = exhausted(raw)
    p1, p2, mp, pc = [], [], [], []
    st = collections.Counter()
    st["mixed_batches"] = 0
    missing = []
    for bid in sorted(by_batch):
        b = by_batch[bid]
        files = [os.path.join(d, f) for d in folders.get(bid, []) for f in sorted(os.listdir(d)) if ACCEPTED.match(f)]
        if len(files) > 1:
            err("packet %s has %d accepted returns (%s); one accepted return per packet, and which is the batch's "
                "reading is not the assembler's call" % (bid, len(files), ", ".join(os.path.relpath(f, out) for f in files)),
                shape="assemble: a packet with more than one accepted return", where=bid)
            continue
        if not files:
            (st.__setitem__("exhausted", st["exhausted"] + 1) if bid in ex else missing.append(bid))
            continue
        f = files[0]
        rel = os.path.relpath(f, out)
        reader = os.path.basename(f)[:-6]
        meta = {}
        mpath = f[:-6] + ".meta.json"
        try:
            meta = json.load(open(mpath, encoding="utf-8"))
        except (OSError, ValueError):
            warn("%s has no readable meta (%s); its reissue and elapsed seconds are null"
                 % (rel, os.path.basename(mpath)), shape="assemble: a return without its meta", where=rel)
        if meta and meta.get("valid") is False:
            err("%s: its meta says valid false; an accepted return is one the dispatch validated" % rel,
                shape="assemble: a return its meta marks invalid", where=rel)
        kinds, items, mixed = copy_kinds(b)
        st["mixed_batches"] += int(mixed)
        rule = dict(COUNT_DEFAULT)
        rule.update({k: v for k, v in (manifest.get(bid) or {}).items() if k in ("count_key", "count_exclude")})
        base = {"batch": bid, "agent": b.get("agent"), "replicate": b.get("replicate"),
                "reissue": meta.get("reissue"), "reader": meta.get("reader", reader)}
        rows = jsonl(f) or []
        st["returns"] += 1
        by_pos = {}
        held = []
        for i, r in enumerate(rows, 1):
            where = "%s line %d" % (rel, i)
            if "predicted_confusion" in r:
                pc.append(dict(dict(base, position=None, fleet_agent=r.get("agent")),
                               **{k: v for k, v in r.items() if k not in ("agent", "batch", "replicate")}))
                continue
            if "revises" in r:
                held.append((where, r))
                continue
            if "primary" in r and "third_order" not in r:      # a multiplacement record as a line of its own
                held.append((where, r))
                continue
            if not counted(r, rule):
                err("%s: a line that is no prediction, item, pass-2 line or multiplacement record (keys %s)"
                    % (where, sorted(r)[:8]), shape="assemble: a return line of no known kind", where=where)
                continue
            pos = r.get("position")
            pos = int(pos) if isinstance(pos, str) and pos.isdigit() else pos
            cell = items[pos - 1] if isinstance(pos, int) and 1 <= pos <= len(items) else None
            if cell is None:
                err("%s: position %r is no cell of batch %s (1..%d)" % (where, r.get("position"), bid, len(items)),
                    shape="assemble: a position outside its batch", where=where)
                continue
            if pos in by_pos:
                err("%s: position %d is returned twice in one return" % (where, pos),
                    shape="assemble: a position returned twice", where=where)
                continue
            e = tr.theme(r.get("theme_id"), where)
            if e is None:
                continue
            room, tid = e["sub"], e["id"]
            cell_ok = cell == (room, tid)
            if not cell_ok:
                err("%s: theme id %s names %s/%s, and batch %s holds %s/%s at cell %d; the cell is the key and the id "
                    "a label, and the two disagree" % (where, r.get("theme_id"), room, tid, bid, cell[0], cell[1], pos),
                    shape="assemble: a theme id off its cell", where=where)
            typed = strip_r(r.get("sub"))
            sub_ok = tr.sub_check(typed, room, where, cell_ok)
            line = dict(base, position=pos, copy_kind=kinds[pos - 1])
            line["sub"], line["theme_id"] = room, tid
            line["fleet_sub"], line["fleet_theme_id"] = r.get("sub"), r.get("theme_id")
            if typed != room and sub_ok:
                line["sub_typed"] = typed
            line["fleet_agent"] = r.get("agent")
            if r.get("replicate") != b.get("replicate"):
                line["replicate_typed"] = r.get("replicate")
                st["replicate_typed"] += 1
            if r.get("batch") not in (None, bid):
                line["batch_typed"] = r.get("batch")
                st["batch_typed"] += 1
            for k, v in r.items():
                if k in DROP or k in ("sub", "theme_id", "batch", "agent", "replicate", "position"):
                    continue
                line[k] = v
            line["packet_elapsed_s"] = meta.get("elapsed_s")
            if "support" in r:
                line["fleet_support"] = r["support"]
                line["support"] = tr.concepts(r["support"], room, where, "support")
            if isinstance(r.get("also_present"), dict):
                line["fleet_also_present"] = r["also_present"]
                line["also_present"] = {t: tr.concepts(cs, room, where, "also_present[%s]" % t)
                                        for t, cs in r["also_present"].items()}
            ml = r.get("multiplacement_log")
            recs = ml if isinstance(ml, list) else [ml] if isinstance(ml, dict) and ml else []
            tl = [translate_record(m, line, tr, where) for m in recs if isinstance(m, dict)]
            if isinstance(ml, (list, dict)):
                line["multiplacement_log"] = tl if isinstance(ml, list) else (tl[0] if tl else ml)
            mp.extend(tl)
            by_pos[pos] = line
            p1.append(line)
        for where, r in held:
            if "revises" in r:
                v = r.get("revises")
                v = v.get("position") if isinstance(v, dict) else v
                v = int(v) if isinstance(v, str) and v.isdigit() else v
                one = by_pos.get(v)
                if one is None:
                    warn("%s: a pass-2 line revises %r, no pass-1 line of this return; carried, and the check names it"
                         % (where, r.get("revises")), shape="assemble: a pass-2 line naming no pass-1 line", where=where)
                line = dict(base, position=v, copy_kind=one["copy_kind"] if one else None)
                line["sub"], line["theme_id"] = (one["sub"], one["theme_id"]) if one else (None, None)
                line["fleet_agent"] = r.get("agent")
                if r.get("theme_id") is not None:
                    e = tr.theme(r.get("theme_id"), where)
                    if e and one and (e["sub"], e["id"]) != (one["sub"], one["theme_id"]):
                        err("%s: a pass-2 line names %s/%s and revises the line of %s/%s"
                            % (where, e["sub"], e["id"], one["sub"], one["theme_id"]),
                            shape="assemble: a pass-2 line off the line it revises", where=where)
                    line["fleet_theme_id"], line["fleet_sub"] = r.get("theme_id"), r.get("sub")
                for k, v2 in r.items():
                    if k in DROP or k in ("sub", "theme_id", "batch", "agent", "replicate", "position"):
                        continue
                    line[k] = v2
                if "support" in r:
                    line["fleet_support"] = r["support"]
                    line["support"] = tr.concepts(r["support"], line["sub"], where, "support")
                p2.append(line)
            else:                                   # a multiplacement record sent as a line of its own
                pos = r.get("position")
                one = by_pos.get(int(pos) if isinstance(pos, str) and pos.isdigit() else pos)
                if one is None:
                    err("%s: a multiplacement record at position %r, where this return has no item line"
                        % (where, pos), shape="assemble: a multiplacement record with no item line", where=where)
                    continue
                mp.append(translate_record(r, one, tr, where))
        if not any("predicted_confusion" in r for r in rows):
            st["no_prediction"] += 1
    return p1, p2, mp, pc, st, missing, ex


# ---- the B1 grouping and the families ----------------------------------------------------------------------------

def b1_grouping(out, theme_rows):
    """({(sub, tid): {T3 ids}}, sha256, report Counter, examples). Members are matched by (sub, label)."""
    p = next((x for x in (os.path.join(out, "scheme", "scheme_current.jsonl"), os.path.join(out, "scheme_current.jsonl"))
              if os.path.exists(x)), None)
    if p is None:
        err("scheme_current.jsonl is in neither out/scheme/ nor out/; the B1 grouping cannot be joined, and every item "
            "would read as class 5")
        return {}, None, collections.Counter(), {}
    digest = vlib.sha(p)
    if not digest.startswith(B1_SHA_EXPECTED):
        warn("%s has sha256 %s, not the %s the orchestrator's note of 2026-10-12 names; the classes rest on this file, "
             "say which in notes-B3.md" % (os.path.relpath(p, out), digest[:16], B1_SHA_EXPECTED))
    by_label = collections.defaultdict(set)
    for t in theme_rows:
        by_label[(t.get("sub"), t.get("second_order"))].add(t.get("theme_id"))
    groups = collections.defaultdict(set)
    rep, ex = collections.Counter(), collections.defaultdict(list)
    for s in jsonl(p) or []:
        tid3 = s.get("theme") or s.get("id")
        for m in s.get("members") or []:
            rep["members"] += 1
            ids = by_label.get((strip_r(m.get("sub")), m.get("second_order")))
            if not ids:
                rep["no_match"] += 1
                ex["no_match"].append("%s: %s/%s %r" % (tid3, m.get("sub"), m.get("theme_id"), m.get("second_order")))
                continue
            if len(ids) > 1:
                rep["label_ambiguous"] += 1
                ex["label_ambiguous"].append("%s: %s %r -> %s" % (tid3, m.get("sub"), m.get("second_order"), sorted(ids)))
            if m.get("theme_id") not in ids:
                rep["id_disagrees"] += 1
                ex["id_disagrees"].append("%s: %s/%s, the label is %s" % (tid3, m.get("sub"), m.get("theme_id"), sorted(ids)))
            else:
                rep["matched"] += 1
            for i in ids:
                groups[(strip_r(m.get("sub")), i)].add(tid3)
    return groups, digest, rep, ex


def families(out, given):
    """({T3 id: family}, where it came from) or ({}, None)."""
    cands = [given] if given else [os.path.join(out, "families.jsonl"), os.path.join(out, "scheme", "families.jsonl")]
    for p in cands:
        p = path_in(out, p) if p else p
        if p and os.path.exists(p):
            fam = {t: f.get("family") for f in (jsonl(p) or []) for t in as_list(f.get("themes"))}
            if fam:
                return fam, p
        elif given:
            err("--families %s does not exist" % given)
            return {}, None
    for name in ("scheme_final.jsonl", os.path.join("scheme", "scheme_final.jsonl"), os.path.join("scheme", "scheme_current.jsonl"),
                 "scheme_current.jsonl", "scheme.jsonl"):
        p = os.path.join(out, name)
        fam = {(r.get("id") or r.get("theme")): r.get("family") for r in (jsonl(p) or []) if r.get("family")}
        if fam:
            return fam, p
    return {}, None


# ---- the classes ------------------------------------------------------------------------------------------------

def classify(items, p1, groups, fam, digest):
    """One class line per item of the analysed set. Returns (rows, stats)."""
    reads = collections.defaultdict(dict)
    for r in p1:
        if r.get("copy_kind") != "corpus":
            continue
        k = (r["sub"], r["theme_id"])
        if r["replicate"] in reads[k]:
            err("%s/%s has two corpus lines in replicate %s (%s and %s); one corpus reading per replicate"
                % (k[0], k[1], r["replicate"], reads[k][r["replicate"]]["batch"], r["batch"]),
                shape="assemble: two corpus readings of one item in one replicate", where="%s/%s" % k)
        reads[k][r["replicate"]] = r
    rows, st = [], collections.Counter()
    for k in sorted(items):
        got = reads.get(k, {})
        r1, r2 = got.get(1), got.get(2)
        l1 = list(as_list(r1.get("third_order"))) if r1 else None
        l2 = list(as_list(r2.get("third_order"))) if r2 else None
        b1 = groups.get(k, set())
        flags = {"missing_replicate": r1 is None or r2 is None}
        if flags["missing_replicate"]:
            flags["replicates_present"] = sorted(got)
        placed = set(l1 or []) | set(l2 or [])
        if fam:
            opened = set(as_list(r1.get("families_opened") if r1 else None)) | set(as_list(r2.get("families_opened") if r2 else None))
            un = sorted(t for t in placed if fam.get(t) not in opened)
            flags["unopened_family"] = bool(un)
            if un:
                flags["unopened_themes"] = un
        else:
            flags["unopened_family"] = None
        for f in ("multi", "bag"):
            flags[f] = any((x or {}).get(f) for x in (r1, r2))
        final, source = None, None
        if not b1:
            cls = 5
        elif flags["missing_replicate"]:
            cls = 3
        elif l1 != l2:
            cls = 3
        elif not l1:
            cls, flags["empty_placement"] = 3, True
        elif set(l1) == b1:
            cls, final, source = 1, l1, "readers_agree"
        elif set(l1) < b1:
            cls, final, source = 2, l1 + sorted(b1 - set(l1)), "b1_grouping_kept"
        else:
            cls = 4
        if final and len(final) > 3:
            flags["over_three"] = True
            st["over_three"] += 1
        row = {"sub": k[0], "theme_id": k[1], "class": cls, "r1": l1, "r2": l2, "b1": sorted(b1), "flags": flags,
               "final": final, "source": source, "b1_scheme_sha256": digest[:16] if digest else None}
        rows.append(row)
        st["class%d" % cls] += 1
        st["missing_replicate"] += int(flags["missing_replicate"])
        st["missing_replicate_class5"] += int(flags["missing_replicate"] and cls == 5)
        st["unopened"] += int(bool(flags["unopened_family"]))
        st["rep1"] += int(r1 is not None)
        st["rep2"] += int(r2 is not None)
    return rows, st


# ---- writing ---------------------------------------------------------------------------------------------------

def write_jsonl(path, rows):
    tmp = path + ".tmp-assemble"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def main(argv):
    ap = argparse.ArgumentParser(prog="assemble.py", description="stage B3's returns into the files stage B4 inherits")
    ap.add_argument("stage", choices=["B3"])
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="out")
    ap.add_argument("--families", help="families.jsonl ({family, themes}); found under out/ when not given")
    ap.add_argument("--dry-run", action="store_true", help="read, check and count; write nothing")
    ap.add_argument("--supersede", action="store_true", help="rename existing outputs to <name>.superseded-<utc> first")
    ap.add_argument("--accept-sub-label", action="store_true",
                    help="carry a typed sub off the theme's room where the theme id and the cell agree (kept as sub_typed)")
    a = ap.parse_args(argv)
    root = a.root
    out = a.out if os.path.isabs(a.out) else os.path.join(root, a.out)
    ctx = {"package": os.path.join(root, "package"), "root": root, "outdir": out, "stage": "B3"}
    E.clear(); W.clear()

    batches = jsonl(os.path.join(out, "batches-B3.jsonl"))
    if not batches:
        sys.exit("assemble.py: out/batches-B3.jsonl is absent or empty; the batches are the key every return is read on")
    by_batch = {b.get("batch"): b for b in batches}
    by_fleet, _ = vlib.fleet_table(out)
    if not by_fleet:
        sys.exit("assemble.py: out/fleet_ids.jsonl is absent or empty; the returns are in fleet ids and cannot be read "
                 "back without it")
    raw = os.path.join(out, "_fleet_raw", "B3")
    if not os.path.isdir(raw):
        sys.exit("assemble.py: out/_fleet_raw/B3/ does not exist; there are no returns to assemble")
    try:
        manifest = json.load(open(os.path.join(out, "_packets-B3", "MANIFEST.json"), encoding="utf-8"))
    except (OSError, ValueError):
        manifest = {}
        warn("out/_packets-B3/MANIFEST.json is not readable; the default count rule (position, less primary, revises "
             "and predicted_confusion) is used for every packet")

    # the analysed set: the store as it stands now (out/recut/ laid over it, WITHDRAWN.json honoured)
    current = vlib.current_themes(ctx)
    if os.path.exists(os.path.join(ctx["package"], "store", "rooms.jsonl")) and \
            os.path.exists(os.path.join(out, "dropped.jsonl")):
        sets = vlib.analysed_set("B3", "the analysed set", out, ctx)
        analysed = sets[0] if sets else {k[0] for k in current}
    else:
        analysed = {k[0] for k in current}
        warn("package/store/rooms.jsonl or out/dropped.jsonl is absent, so the analysed set is every second-order theme "
             "that stands now (%d), no room dropped" % len(current))
    items = {k for k in current if k[0] in analysed}
    theme_rows = vlib.recut_overlay("themes", jsonl(os.path.join(ctx["package"], "store", "themes.jsonl")) or [], out)

    tr = Translator(by_fleet, a.accept_sub_label)
    p1, p2, mp, pc, st, missing, ex = read_returns(out, raw, by_batch, manifest, tr)
    groups, digest, rep, rex = b1_grouping(out, theme_rows)
    fam, fam_src = families(out, a.families)
    if not fam:
        warn("no families file was found (--families, out/families.jsonl, out/scheme/families.jsonl, or a family field "
             "on the scheme's rows); the unopened-family flag was NOT computed and is null on every class line")
    rows, cs = classify(items, p1, groups, fam, digest)
    stray = sorted({(r["sub"], r["theme_id"]) for r in p1 if r.get("copy_kind") != "gold"} - items)
    if stray:
        err("%d items read as corpus are not in the analysed set (%s)" % (len(stray), ["%s/%s" % k for k in stray[:3]]),
            shape="assemble: a corpus reading outside the analysed set")
    if missing:
        err("%d batches have no accepted return and are not in EXHAUSTED.tsv (%s); a batch is returned, exhausted or "
            "named" % (len(missing), missing[:5]))

    kinds = collections.Counter(r.get("copy_kind") for r in p1)
    print("assemble B3: %d returns read (%d batches exhausted, %d missing); %d returns without a prediction line"
          % (st["returns"], st["exhausted"], len(missing), st["no_prediction"]))
    print("  lines: pass 1 %d (corpus %d, gold %d, duplicate %d%s), pass 2 %d, multiplacement records %d, predictions %d"
          % (len(p1), kinds["corpus"], kinds["gold"], kinds["duplicate"],
             ", repeated beyond the declared duplicate %d" % kinds["corpus-repeated"] if kinds["corpus-repeated"] else "",
             len(p2), len(mp), len(pc)))
    if st["mixed_batches"]:
        print("  %d batches hold an item both live and as a gold copy; the first occurrence was taken as live"
              % st["mixed_batches"])
    print("  typed off the batch: replicate %d, batch %d; typed sub off the theme's room carried as sub_typed: %d"
          % (st["replicate_typed"], st["batch_typed"], len(tr.sub_label)))
    for w_, t_, r_ in tr.sub_label:
        print("    sub_typed %s: typed %r, the theme's room %r" % (w_, t_, r_))
    print("  B1 grouping: scheme_current.jsonl sha256 %s; members %d, matched %d, theme_id disagreeing with the label %d, "
          "no label match %d, label naming several themes %d; items with a grouping %d of %d"
          % (digest[:16] if digest else None, rep["members"], rep["matched"], rep["id_disagrees"], rep["no_match"],
             rep["label_ambiguous"], sum(1 for k in items if groups.get(k)), len(items)))
    for kind in ("id_disagrees", "no_match", "label_ambiguous"):
        for x in rex.get(kind, [])[:5]:
            print("    %s: %s" % (kind, x))
    print("  families: %s" % (fam_src or "none found, unopened-family flag not computed"))
    n = len(items)
    print("  analysed set %d items; coverage replicate 1 %d (%.1f%%), replicate 2 %d (%.1f%%)"
          % (n, cs["rep1"], 100.0 * cs["rep1"] / max(n, 1), cs["rep2"], 100.0 * cs["rep2"] / max(n, 1)))
    print("  classes: " + ", ".join("%d: %d" % (c, cs["class%d" % c]) for c in range(1, 6)) +
          "; standing (1, 2) %d, to B4 (3, 4, 5) %d" % (cs["class1"] + cs["class2"], cs["class3"] + cs["class4"] + cs["class5"]))
    print("  missing_replicate %d (in class 3: %d; in class 5, no grouping: %d); unopened-family flags %s; class-2 "
          "lines over three themes %d" % (cs["missing_replicate"], cs["missing_replicate"] - cs["missing_replicate_class5"],
                                          cs["missing_replicate_class5"], cs["unopened"] if fam else "not computed",
                                          cs["over_three"]))

    ef, wf = fold(E), fold(W)
    for m in wf:
        print("WARN  " + m)
    for m in ef:
        print("ERROR " + m)
    if E:
        lines = collections.defaultdict(list)
        for _m, shape, where in E:
            if shape and where:
                lines[shape].append(where)
        for shape, ws in lines.items():
            if len(ws) > 1:
                print("  %s, every line: %s" % (shape, "; ".join(ws)))
        print("REFUSING: %d errors; nothing written" % len(ef))
        return 1
    files = {"assign_raw.jsonl": p1, "assign_pass2.jsonl": p2, "multiplacement_log.jsonl": mp,
             "predicted_confusion-B3.jsonl": pc, "b3_classes.jsonl": rows}
    there = [n_ for n_ in OUTPUTS if os.path.exists(os.path.join(out, n_))]
    if a.dry_run:
        print("dry run: nothing written%s" % ("; %s exist and would need --supersede" % ", ".join(there) if there else ""))
        return 0
    if there and not a.supersede:
        print("REFUSING: %s already exist in %s; an output is never overwritten silently (pass --supersede to rename the "
              "old files to <name>.superseded-<utc> first)" % (", ".join(there), out))
        return 1
    utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for n_ in there:
        old = os.path.join(out, n_)
        os.replace(old, "%s.superseded-%s" % (old, utc))
        print("  superseded %s -> %s.superseded-%s" % (n_, n_, utc))
    for n_ in OUTPUTS:
        write_jsonl(os.path.join(out, n_), files[n_])
        print("  wrote %s: %d lines" % (n_, len(files[n_])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
