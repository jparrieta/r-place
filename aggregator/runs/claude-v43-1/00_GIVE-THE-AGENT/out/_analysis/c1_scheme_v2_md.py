#!/usr/bin/env python3
"""C1 section 9: write out/scheme_v2.md, the whole scheme and not a diff, from the ledgers.

Every theme of scheme_v2.jsonl with every field, by family; the gate block (each of the 35 gate sentences amended at
C1 with its old and new sentence, its reason, its rechecks and the placements it moved); the tier change; the
placements moved at C1 by cause; the reading rules; the watch items; the fourth-order theme each third-order theme
sits in. Refuses to overwrite; supersede with a new name.

    python3 out/_analysis/c1_scheme_v2_md.py [--out scheme_v2.md]
"""
import argparse, collections, json, os, re, sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


ap = argparse.ArgumentParser()
ap.add_argument("--out", default="scheme_v2.md")
ap.add_argument("--causes", action="store_true", help="print the moves-by-cause table only; write nothing")
a = ap.parse_args()
dest = os.path.join(OUT, a.out)
if os.path.exists(dest) and not a.causes:
    sys.exit("%s exists; supersede it with a new name" % a.out)

scheme = jl("scheme_v2.jsonl")
final = dict((t["id"], t) for t in jl("scheme_final.jsonl"))
names = dict((t["id"], t["name"]) for t in scheme)
fams = dict((f["family"], f["name"]) for f in jl("families.jsonl"))
gh = jl("gate_history.jsonl")
rc = jl("rechecks-C1.jsonl")
th = [r for r in jl("tier_history.jsonl") if r.get("stage") == "C1" and r.get("tier") == "third"]
t4 = jl(os.path.join("fourth", "fourth.jsonl"))
owner = dict((m, r) for r in t4 for m in r["members"])
rows = jl("assignments_final.jsonl")

lines_of, rooms_of = collections.Counter(), collections.defaultdict(set)
for r in rows:
    for t in r.get("third_order") or []:
        lines_of[t] += 1
        rooms_of[t].add(r["sub"])
done = collections.Counter(r.get("change") for r in rc)
changed = collections.Counter(r.get("change") for r in rc if r.get("changed"))
gate_moves = collections.Counter()
cause = collections.Counter()
cause_lines = collections.defaultdict(set)
revised = set()


def classify(why):
    w = why or ""
    if w.startswith("J, 13 October 2026, 20:16 Berlin"):
        return "the class 2 ruling (J, 13 October, 20:16 Berlin): the readers' list stands"
    if "C1a-01 re-read" in w:
        return "pass 1 re-reads under the class 2 ruling"
    if "empties pass" in w:
        return "the empties pass (pass 8): B4 rulings re-read"
    if "revision rate" in w:
        return "the revision rate's errors (pass 5)"
    if "doubt decided" in w:
        return "a pass 1 doubt decided (pass 5)"
    if re.search(r"gate:(\d+)\b", w):
        return "rechecks after an amended gate"
    if "flagged class 2 record" in w:
        return "a flagged class 2 record promoted (pass 4)"
    if "Review of a line listed" in w:
        return "lines listed for review at gates 15 to 21 (pass 4)"
    if "lone-B1 floor" in w:
        return "the lone-B1 floor revised (pass 4)"
    if "QC1-002" in w:
        return "J's floor for a second theme (QC1-002)"
    return "other: " + w[:60]


for r in rows:
    for m in r.get("moves") or []:
        k = (r["sub"], r["theme_id"])
        revised.add(k)
        c = classify(m.get("why"))
        cause[c] += 1
        cause_lines[c].add(k)
        for g in set(re.findall(r"gate:(\d+)\b", m.get("why") or "")):
            gate_moves["gate:" + g] += 1
if a.causes:
    print("| cause | move entries | lines |\n|---|---|---|")
    print("\n".join("| %s | %d | %d |" % (c, n, len(cause_lines[c])) for c, n in cause.most_common()))
    print("| all | %d | %d |" % (sum(cause.values()), len(revised)))
    sys.exit(0)

by_theme_gates = collections.defaultdict(list)
for g in gh:
    by_theme_gates[g["theme"]].append(g)
amended_themes = sorted(set(g["theme"] for g in gh))
amended_fams = sorted(set((dict((t["id"], t["family"]) for t in scheme)).get(t) for t in amended_themes))
rare = [t for t in scheme if t.get("tier") == "rare"]


def floor_line(t):
    if t.get("tier") == "rare":
        return "Rare tier."
    f = t.get("floor") or {}
    if not f:
        return ""
    rooms = f.get("rooms") or []
    return "Floor: %s, unlike in %s (%s)." % (" and ".join(rooms), f.get("unlike", ""), f.get("why", ""))


def ex_line(e):
    riv = e.get("rivals") or []
    return "\"%s\" (%s %s%s)" % (e.get("quote", ""), e.get("sub", ""), e.get("code_id", ""),
                                (", rivals " + ", ".join(riv)) if riv else "")


def disc_diff(was, now):
    w = dict((d.get("vs"), d.get("question")) for d in (was or []))
    n = dict((d.get("vs"), d.get("question")) for d in (now or []))
    out = []
    for vs in sorted(set(w) | set(n)):
        if w.get(vs) == n.get(vs):
            continue
        if vs not in w:
            out.append("- Added, against %s: %s" % (vs, n[vs]))
        elif vs not in n:
            out.append("- Removed, against %s: %s" % (vs, w[vs]))
        else:
            out.append("- Against %s, was: %s" % (vs, w[vs]))
            out.append("- Against %s, now: %s" % (vs, n[vs]))
    return out or ["- (no question changed)"]


FIELD = {"must_show": "must show", "must_not_show": "must not show", "decide_when_both": "decide when both",
         "discriminators": "discriminators", "gloss": "gloss"}
L = []
P = L.append
P("# The third-order scheme, version 2 (stage C1)")
P("")
P("Written at stage C1, leg C1a-11, 2026-10-14 (UTC), from `scheme_v2.jsonl` and the C1 ledgers by "
  "`out/_analysis/c1_scheme_v2_md.py`. This is the whole scheme, every theme with every field, and not a diff. After "
  "stage C1 it is the frozen instrument: every later stage keys its theme ids to it, and the validator resolves them "
  "against it. `scheme_v2.jsonl` mirrors `scheme_final.jsonl` field for field; `scheme_final.md` is the scheme as it "
  "was frozen at stage B2.")
P("")
P("%d themes in %d families; %d are on the rare tier. At C1 no theme was added, split, merged or retired. %d gate "
  "sentences were amended in %d themes (%s), one theme moved to the rare tier, and %d of %d placement lines were "
  "revised. The fourth-order themes cut at C1 are in `fourth/fourth.md`; each third-order theme below names the one it "
  "sits in." % (len(scheme), len(fams), len(rare), len(gh), len(amended_themes), ", ".join(amended_fams), len(revised),
                len(rows)))
P("")
P("## How to read a theme")
P("")
P("Place each second-order theme on the theme whose gate its concepts meet: must show, must not show, and decide when "
  "both. A discriminator is the question that separates a theme from a near neighbour. Rule 0 orders the placed themes "
  "by the concepts each takes, ties by placements; at most three are placed, and a second or third theme needs three "
  "concepts of its own (J's floor, QC1-002). Other themes with three concepts of their own, named by a reader or by my "
  "B1, go under `also_present`; four themes with three concepts each make a bag, and no one cuts a bag. A theme on the "
  "rare tier is placed like any other; it marks a kind the corpus carries below stage B1's floor of two rooms unlike "
  "each other.")
P("")
P("## Reading rules declared at C1")
P("")
P("These rules say how the fields below are read. They were declared in `notes-C1.md` and applied in every C1 recheck.")
P("")
for s in [
    "**The visitor rule.** A theme names an act in the record of the room whose threads hold the words. Another room's act spoken there is placed by what it is for this room.",
    "**\"The work\"** in a field is the room's own work unless the field names another's.",
    "**A bare mention of the event** holds no act; it stays unplaced.",
    "**How a recheck is read.** The item moves when the old and amended sentences give different answers, J's floor applied to both, and the line follows the old one; a line that differs from both is listed for review.",
    "**J's floor in every pairing sentence.** \"When it has concepts of its own\" is read as three concepts or more.",
    "**The named words of T3-010 | T3-149** (and since gates 33 and 34, of T3-149 | T3-025). Attack, war, fight, battle, invasion, raid and conquest name an attack. Verbs acting on a work without them are a work asked to be spared (T3-010). A pledge to leave each other alone that names no lines or space is a non-aggression pact (T3-149). A greeting \"in peace\", or an adverb or adjective on border talk, names no pact.",
    "**Help between rooms is read from either room's record** (gate:5 for T3-084, gate:27 for T3-011).",
    "**Credit and own part (gates 30 to 32).** A member's own part, during the work or after, is T3-003; T3-043 is credit to others and disputes over who made it. A plural claim of who made it stays T3-043. A mixed concept goes by the act its label leads with."]:
    P("- " + s)
P("")
P("## The gate block: every gate amended at C1")
P("")
P("Each amendment was recorded with `mem.py gate` in `gate_history.jsonl` and written into `scheme_v2.jsonl`. It owed "
  "a recheck of the placements it could move: every one up to thirty, else a seeded sample of thirty, and every one "
  "once more than one in ten of the sample moved. The rechecks are in `rechecks-C1.jsonl`. \"Moved\" counts the moves "
  "on `assignments_final.jsonl` lines whose reason names the gate, including moves made later on review. The full "
  "gate of every theme, amended or not, is in its block under Themes.")
P("")
P("The next table lists the 35 amendments with the theme, the field, the placements the change could move, the "
  "rechecks done, the rechecks that changed the line, and the moves that name the gate.")
P("")
P("| gate | leg | theme | field | could move | rechecked | changed | moved |")
P("|---|---|---|---|---|---|---|---|")
for g in gh:
    P("| %s | %s | %s %s | %s | %d | %d | %d | %d |" % (g["ref"], g["leg"], g["theme"], names.get(g["theme"], ""),
                                                      FIELD.get(g["field"], g["field"]), g.get("candidates") or 0,
                                                      done[g["ref"]], changed[g["ref"]], gate_moves[g["ref"]]))
P("")
for g in gh:
    P("### %s: %s %s, %s (%s)" % (g["ref"], g["theme"], names.get(g["theme"], ""), FIELD.get(g["field"], g["field"]),
                                  g["leg"]))
    P("")
    if g["field"] == "discriminators":
        L.extend(disc_diff(g.get("was"), g.get("now")))
    else:
        P("- Was: %s" % (g.get("was") or "(empty)"))
        P("- Now: %s" % g.get("now"))
    P("- Why: %s" % g.get("why"))
    P("- Rechecks: %d placements could move; %d rechecked%s; %d changed; %d %s this gate." % (
        g.get("candidates") or 0, done[g["ref"]], " (all, the sample having moved more than one in ten)"
        if done[g["ref"]] > 30 else " (the seeded sample)" if done[g["ref"]] == 30 else "", changed[g["ref"]],
        gate_moves[g["ref"]], "move names" if gate_moves[g["ref"]] == 1 else "moves name"))
    P("")
P("## The tier change")
P("")
for r in th:
    was = r.get("was") or {}
    fl = was.get("floor") or {}
    P("- **%s %s: %s** (%s, move %s). It was %s, its floor %s, unlike in %s. Why: %s Prompted by: %s." % (
        r["id"], names.get(r["id"], ""), r.get("event"), r.get("leg"), r.get("move"), was.get("tier"),
        " and ".join(fl.get("rooms") or []), fl.get("unlike", ""), r.get("why"), r.get("prompted_by")))
P("")
P("## Placements moved at C1, by cause")
P("")
P("Every move is recorded on its line of `assignments_final.jsonl` (`moves`, with the concepts behind each theme) and "
  "in `assign_revisions_only.jsonl`. The next table counts the move entries and the lines they touch, by cause. A line "
  "moved twice counts under each cause.")
P("")
P("| cause | move entries | lines |")
P("|---|---|---|")
for c, n in cause.most_common():
    P("| %s | %d | %d |" % (c, n, len(cause_lines[c])))
P("| all | %d | %d |" % (sum(cause.values()), len(revised)))
P("")
P("## Watch items")
P("")
P("These are known weak points of the wording, carried to `handback-C1.md`. None amended a gate at C1.")
P("")
for s in [
    "**osugame t04.** Removals pointing to a canvas sub meet both T3-063's decide when both (gate:23, \"removing under any other rule\") and T3-090's must show (\"canvas posts redirected to it\"). The two sentences overlap on a sub that removes canvas posts and sends them to its own canvas sub.",
    "**The named words and the common speech of war.** The named words of T3-010 | T3-149 read attack, war, fight, battle, invasion, raid and conquest as naming an attack. The form pass (`form_pass-C1.md`, the finding on the vocabulary of state and war) finds such words across 571 rooms and 145 line themes, even for builders. The rule decides only between those themes; a reader applying it should ask whether the word names an act on the work or is the room's ordinary register.",
    "**T3-010 | T3-149, the one unresolved pair.** The pair test at pass 7 could not call it joint or lump (`c1_pair_calls-*.json`).",
    "**Two boundaries barred from a third sentence.** T3-033 | T3-041 (the call, offer and build cluster moved at B2 and split the readers again) and T3-002 | T3-005 (calls to defend). Twenty placements read against them were kept as found (`out/_analysis/c1_pair_carried_decisions.json`).",
    "**Four kinds the scheme lacks** (pass 8's empties): April Fools play that stages no fake; another sub's April Fools change seen from this room; the sub's own moderation outside the canvas; disputes over the room's own jokes. Their lines stay empty.",
    "**Five errors no C1 verb applies** (`out/_analysis/c1_unapplied.jsonl`, QC1-003): two lines to be emptied and three bags whose placed theme and `also_present` should swap."]:
    P("- " + s)
P("")
P("## Index")
P("")
by = collections.OrderedDict()
for t in scheme:
    by.setdefault(t["family"], []).append(t)
for fam in sorted(by):
    P("**%s %s**" % (fam, fams.get(fam, "")))
    P("")
    for t in by[fam]:
        P("- %s %s%s: %s" % (t["id"], t["name"], " (rare)" if t.get("tier") == "rare" else "", t.get("gloss", "")))
    P("")
P("## Themes")
P("")
for fam in sorted(by):
    P("## %s %s" % (fam, fams.get(fam, "")))
    P("")
    for t in by[fam]:
        i = t["id"]
        P("### %s %s" % (i, t["name"]))
        P("")
        P(("%s %s" % (t.get("gloss", ""), floor_line(t))).strip())
        P("")
        P("- Must show: %s" % t.get("must_show", ""))
        P("- Must not show: %s" % t.get("must_not_show", ""))
        P("- Decide when both: %s" % t.get("decide_when_both", ""))
        for d in t.get("discriminators") or []:
            P("- Against %s: %s" % (d.get("vs"), d.get("question")))
        P("- Varies: %s" % t.get("varies", ""))
        P("- Is not: %s" % t.get("is_not", ""))
        if t.get("gate_parts"):
            P("- Gate parts: %s" % json.dumps(t["gate_parts"], ensure_ascii=False))
        P("- Exemplars: %s" % "; ".join(ex_line(e) for e in t.get("exemplars") or []))
        o = owner.get(i)
        P("- At C1's close: placed on %d lines in %d rooms; fourth-order theme %s." % (
            lines_of[i], len(rooms_of[i]), ("%s %s" % (o["id"], o["name"])) if o else "none (unpicked; see `fourth/fourth.md`)"))
        gs = by_theme_gates.get(i)
        tier_note = [r for r in th if r["id"] == i]
        notes = []
        if gs:
            notes.append("amended by %s" % ", ".join("%s (%s)" % (g["ref"], FIELD.get(g["field"], g["field"])) for g in gs))
        if tier_note:
            notes.append("moved to the rare tier (%s)" % tier_note[0].get("leg"))
        if not notes and final.get(i) is not None:
            same = all(final[i].get(k) == t.get(k) for k in t)
            notes.append("unchanged at C1" if same else "differs from scheme_final.jsonl outside the gate ledger")
        P("- C1: %s." % "; ".join(notes))
        P("")
os.makedirs(os.path.dirname(dest) or OUT, exist_ok=True)
open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("wrote %s: %d themes, %d gates, %d tier changes, %d lines revised, %d words" % (
    a.out, len(scheme), len(gh), len(th), len(revised), len(" ".join(L).split())))
