#!/usr/bin/env python3
"""B2b-r1: the round-1 scheme edits, applied to the drafts (out/_analysis/b1e_draft_G*.jsonl), then reassembled.

Three parts (QB2-003 asks how to record gate repairs no item caused; this leg repairs only the pairs
round 1's edited themes belong to):
  EXPLICIT  gate sentences changed because readers split or all differed from me on round-1 items
  MIRROR    a one-way discriminator touching an edited theme: its question copied into the other gate
            (each question names both sides), from out/_analysis/b2_gates_r1_before.txt
  NEWPAIR   a must_not_show that sends material to a theme with no discriminator: one question, in both gates
Writes, with --write: the drafts; out/scheme_edits.jsonl (one line per theme and field changed, with
caused_by, kind, was, now, why); tier_history.jsonl lines (event rescoped, move asking questions); then
runs b1e_assemble.py --write. Dry run by default.
"""
import collections, datetime, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")

ITEMS = {
    "T3-005": ["GreenCorner/t03", "nVade/t04"], "T3-021": ["GreenCorner/t03"],
    "T3-009": ["stardustcrusaders/t19", "redhotchilipeppers/t09"], "T3-043": ["stardustcrusaders/t19", "redhotchilipeppers/t09"],
    "T3-087": ["orderofthebluecorner/t08"], "T3-121": ["orderofthebluecorner/t08"], "T3-011": ["nVade/t04"],
    "T3-065": ["guatemala/t02", "catalunya/t01"], "T3-026": ["guatemala/t02"],
    "T3-002": ["guatemala/t02", "catalunya/t01", "cubers/t12"], "T3-169": ["cubers/t12"],
    "T3-042": ["WisconsinBadgers/t04"], "T3-076": ["WisconsinBadgers/t04"],
    "T3-033": ["dofus/t01"], "T3-092": ["dofus/t01"], "T3-004": ["nyu/t01", "furry/t10"], "T3-070": ["nyu/t01", "furry/t10"],
    "T3-031": ["farmcarrots/t15"], "T3-050": ["farmcarrots/t15"],
}
KIND = {"T3-009": "author-error", "T3-043": "author-error", "T3-087": "author-error", "T3-121": "author-error",
        "T3-004": "author-error"}

EXPLICIT = [
    ("T3-005", "must_not_show", "replace", "Watching and repairing with no attacker in view (T3-021)",
     "Watching for damage and repairing it, with or without an attacker in view, where no fight is called (T3-021)",
     "the must_not_show said repair belongs to T3-021 only with no attacker in view, while the discriminator said with or without; the two sentences contradicted each other (the PI, from the B1e interview), and on GreenCorner t03 all three readers placed T3-005 alone"),
    ("T3-021", "must_show", "append", None,
     " Repair during a raid counts here when the fixing leads and no fight is called.",
     "states on T3-021's side what T3-005's corrected must_not_show sends to it"),
    ("T3-009", "decide_when_both", "set", None,
     "Celebration with thanks or credit: the side with more concepts is primary. T3-043, T3-072 or T3-157 is primary when the thanks, the allies or the reflection hold more concepts than the celebrating, and is added only where its part has concepts of its own.",
     "on stardustcrusaders t19, a thread mostly of thanks, all three readers placed T3-043 alone while the gate made T3-009 primary by default; the readers were right and the default was not"),
    ("T3-043", "decide_when_both", "set", None,
     "Credit and celebration together: the side with more concepts is primary, the other added only where its part has concepts of its own; a thread whose concepts are mostly thanks to the makers is T3-043.",
     "the same default, on T3-043's side"),
    ("T3-065", "must_show", "append", None,
     " Announcements that the flag has begun or is up, and calls for hands to it, go here too.",
     "on guatemala t02, a national flag started and announced, two readers placed T3-026 and one T3-002, none T3-065; on catalunya t01 one reader placed T3-002; the gate did not say that every step of the room's own flag stays here"),
    ("T3-092", "decide_when_both", "append", None,
     " A piece begun alone and then offered to the room for others to join: T3-033 when the offer leads, T3-092 when the lone making is reported with no call.",
     "on dofus t01, a member who began alone and then invited the room, the readers placed T3-092, T3-038 and T3-002; the gate did not say which way the invitation tips it"),
]
ADD = [  # (theme, vs, question)
    ("T3-087", "T3-121", "Do members find out or name who is damaging the work (T3-087), or exclude a member who did, by a ban, a kick or a call to moderators to throw them out (T3-121)?"),
    ("T3-121", "T3-087", "Do members find out or name who is damaging the work (T3-087), or exclude a member who did, by a ban, a kick or a call to moderators to throw them out (T3-121)?"),
    ("T3-005", "T3-011", "Is the room's own work defended (T3-005), or another room's work helped or defended by the room's members, a pledge to protect it included (T3-011)?"),
    ("T3-011", "T3-005", "Is the room's own work defended (T3-005), or another room's work helped or defended by the room's members, a pledge to protect it included (T3-011)?"),
    ("T3-065", "T3-026", "Is the room's mark announced as up (T3-026), or is the work the flag of the room's own land, announced, called for or built (T3-065)?"),
    ("T3-026", "T3-065", "Is the room's mark announced as up (T3-026), or is the work the flag of the room's own land, announced, called for or built (T3-065)?"),
    ("T3-002", "T3-169", "Is the work the sub's name written on the canvas (T3-169), whatever the call or report about it, or any other picture called for (T3-002)?"),
    ("T3-169", "T3-002", "Is the work the sub's name written on the canvas (T3-169), whatever the call or report about it, or any other picture called for (T3-002)?"),
]
NEWPAIR = [  # must_not_show defects touching the edited themes, not covered by a mirror
    ("T3-002", "T3-044", "Are the room's own members called to come and place (T3-002), or outsiders brought to the sub by its mark and welcomed (T3-044)?"),
    ("T3-002", "T3-084", "Are the room's own members called to place (T3-002), or another canvas room asked, as a group, for help (T3-084)?"),
    ("T3-009", "T3-072", "Is the room's own finished work celebrated (T3-009), or other rooms thanked for their help (T3-072)?"),
    ("T3-038", "T3-004", "Is the mark being placed and its progress reported (T3-038), or its look argued and corrected against the plan (T3-004)?"),
    ("T3-073", "T3-009", "Is what happened to the work told (T3-073), or the finished work celebrated (T3-009)?"),
    ("T3-144", "T3-002", "Are hands called for in the open (T3-002), or recruited only inside friendly communities so the work draws no attackers (T3-144)?"),
    ("T3-115", "T3-011", "Is another room's request refused (T3-115), or its work helped (T3-011)?"),
]


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    write = "--write" in sys.argv
    drafts = {}
    files = {}
    for p in sorted(glob.glob(os.path.join(AN, "b1e_draft_G*.jsonl"))):
        rows = jl(p)
        files[p] = rows
        for r in rows:
            drafts[r["id"]] = r
    before = {t: json.loads(json.dumps(r)) for t, r in drafts.items()}
    why = collections.defaultdict(list)
    cause = collections.defaultdict(set)
    for t, field, op, old, new, w in EXPLICIT:
        r = drafts[t]
        if op == "replace":
            if old not in r[field]:
                sys.exit("not found in %s %s: %r" % (t, field, old))
            r[field] = r[field].replace(old, new)
        elif op == "append":
            r[field] = r[field].rstrip() + new
        else:
            r[field] = new
        why[(t, field)].append(w)
        cause[(t, field)] |= set(ITEMS[t])
    edited = set(ITEMS)

    def add_disc(t, vs, q, w, items):
        r = drafts[t]
        if vs in {d["vs"] for d in r["discriminators"]}:
            return False
        r["discriminators"].append({"vs": vs, "question": q})
        why[(t, "discriminators")].append(w)
        cause[(t, "discriminators")] |= set(items)
        return True

    for t, vs, q in ADD:
        add_disc(t, vs, q, "a discriminator added because round 1's readers split on the pair (%s/%s)" % (t, vs), ITEMS.get(t) or ITEMS[vs])
    # mirrors
    one = re.compile(r"^\s+(T3-\d+) has one against (T3-\d+); (T3-\d+) none against")
    n_mirror = 0
    for line in open(os.path.join(AN, "b2_gates_r1_before.txt"), encoding="utf-8"):
        m = one.match(line)
        if not m:
            continue
        x, y = m.group(1), m.group(2)
        if x not in edited and y not in edited:
            continue
        q = next(d["question"] for d in drafts[x]["discriminators"] if d["vs"] == y)
        items = ITEMS.get(y) or ITEMS.get(x)
        if add_disc(y, x, q, "one-way discriminator mirrored: %s's question against %s copied into %s's gate (mem.py gates)" % (x, y, y), items):
            n_mirror += 1
    n_new = 0
    for a, b, q in NEWPAIR:
        items = ITEMS.get(a) or ITEMS.get(b)
        n_new += add_disc(a, b, q, "%s's must_not_show sends material to %s with no discriminator (mem.py gates)" % (a, b), items)
        n_new += add_disc(b, a, q, "%s's must_not_show sends material to %s with no discriminator (mem.py gates)" % (a, b), items)
    changed = sorted(why)
    print("explicit field edits %d; discriminators added: %d from round-1 splits, %d mirrored, %d new-pair; theme-fields changed %d; themes changed %d" % (
        len(EXPLICIT), len(ADD), n_mirror, n_new, len(changed), len({t for t, _ in changed})))
    if not write:
        for t, f in changed:
            print("  %s %s: %s" % (t, f, "; ".join(sorted(cause[(t, f)]))))
        return
    for p, rows in files.items():
        with open(p, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ep = os.path.join(OUT, "scheme_edits.jsonl")
    n0 = len(jl(ep)) if os.path.exists(ep) else 0
    with open(ep, "a", encoding="utf-8") as fh, open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as th:
        for i, (t, f) in enumerate(changed, n0 + 1):
            was, nw = before[t][f], drafts[t][f]
            kind = KIND.get(t, "scheme-ambiguous") if f != "discriminators" or any("split" in w for w in why[(t, f)]) else "scheme-ambiguous"
            fh.write(json.dumps({"n": i, "edit": "edit:%d" % i, "round": 1, "leg": "B2b-r1", "t": now, "theme": t, "field": f,
                                 "caused_by": sorted(cause[(t, f)]), "kind": kind, "was": was, "now": nw,
                                 "why": "; ".join(why[(t, f)]), "asks": ["QB2-003"] if f == "discriminators" else []},
                                ensure_ascii=False) + "\n")
            th.write(json.dumps({"t": now, "stage": "B2", "leg": "B2b-r1", "tier": "third", "id": t, "move": "asking questions",
                                 "event": "rescoped", "was": {"field": f, "text": was}, "now": [{"id": t, "field": f, "text": nw}],
                                 "prompted_by": "B2 round 1: readers' placements on %s" % ", ".join(sorted(cause[(t, f)])),
                                 "why": "; ".join(why[(t, f)]) + "; the theme's members are unchanged (no narrowing)",
                                 "edit": "edit:%d" % i}, ensure_ascii=False) + "\n")
    print("scheme_edits.jsonl lines %d to %d" % (n0 + 1, n0 + len(changed)))
    subprocess.run([sys.executable, os.path.join(AN, "b1e_assemble.py"), "--write"], check=True)


if __name__ == "__main__":
    main()
