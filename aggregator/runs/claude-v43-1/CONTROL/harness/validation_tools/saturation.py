#!/usr/bin/env python3
"""saturation.py: when to stop reading (J, 2026-09-29), for a stage whose units are read one at a time.

    python3 tools/saturation.py order  --stage B1          B1's seeded order printed, each room read or unread (B1d)
    python3 tools/saturation.py status --stage B1          the loop replayed: estimates, rounds, markers, next unit
    python3 tools/saturation.py report --stage B1          out/stopping-B1.md, the report for the PI
    python3 tools/saturation.py decide --stage B1 continue|finish|stop --why "..."   the PI's decision, after a report

The rule, for stage B1 only (A1 reads every room and counts no kinds: J, 2026-09-29). A unit is a room;
a kind is a third-order theme as met, from out/kinds-B1.jsonl, which mem.py mint and place
append with the room being read (`at`, which says when a kind is new) and the room whose theme was placed
(`sub`, the room that holds it, where the estimates count it, as Chao et al. 2014 assume: J, 2026-09-29),
and where a merge or a split, logged by mem.py log, is a new kind;
the ledger is never rewritten, so a later regrouping leaves the past as it was read). Material is counted in words (a room's
concepts' quoted text plus its second-order themes), in units of the average room of the analysed set.
No estimate is made before 50 average rooms, and 25 rooms, are read. No round is longer than 25
average rooms. If 60% of the words are read before marker 3, stage B1 reports and pauses for the PI
(the check-in): continue under the rule, finish the list, or stop. While a new kind has come in the
last 10 average rooms (and the last 10 rooms, so one large room cannot fill the gap), reading goes on.
After 10 without one, a round starts: the estimate predicts how far the next kind is, and the round reads that far (never more than
the rooms already read, the doubling limit of Chao et al. 2014). A round that brings a new kind resets
everything, and so does a new kind in the draw (J, 2026-09-29). Three empty rounds in a row are marker 1 (where the literature would stop); three more are
marker 2; then a draw: units taken at random from those not yet read, as many words as the three rounds
between the markers. When the draw is read, marker 3 is set, the report is written and the stage pauses
for the PI, who decides whether to finish the list or stop. Stage B1 reads in a seeded
random order (tag B1), drawn at every call; no list is written.

The estimates, for units read T, room-kind pairs U, kinds seen once Q1 and twice Q2 (Chao et al. 2014,
incidence data): coverage C = 1 - (Q1/U)(T-1)Q1/((T-1)Q1 + 2Q2); unseen kinds Q0 = (T-1)/T Q1^2/(2Q2)
(Q1(Q1-1)/2 (T-1)/T when Q2 = 0); new kinds expected in the next room r = Q0 Q1/(T Q0 + Q1), the first
step of their extrapolation; the next kind is expected 1/r rooms on, and a round reads that far,
converted to average rooms at the mean size of the rooms read so far. When no
kind has been seen once (or one kind once and none twice, where Chao2's Q0 is 0) the estimate expects nothing more; the round is then as long as the one before,
and at least 10 average rooms (the handler's choice, 2026-09-29, for the PI to confirm). The draw's bound: among N unread
units, n drawn and k bringing a new kind, the smallest K with P(X <= k) < 0.05, X ~ Hypergeometric(N, K, n)
(Callaghan and Müller-Hansen 2020): K or more unread units carrying an unseen kind are ruled out.

Everything is replayed from the files on disk at every call, in the order the units were meant to be
read; nothing depends on the analyst's memory. The seed is the sha256 of the store's rooms.jsonl, so no
one chooses the order.
"""
import argparse, collections, datetime, hashlib, json, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vlib

ROUND_GAP = 10          # average rooms, and rooms, without a new kind before a round starts
BURN_IN = 50            # average rooms read before any estimate is made (J, 2026-09-29)
BURN_IN_ROOMS = 25      # and rooms read
ROUND_MAX = 25          # no round is longer than this, in average rooms (J, 2026-09-29)
CHECK_IN = 0.60         # at this share of the words, before marker 3, the stage reports and pauses (B1)
ROUNDS_TO_MARKER1 = 3
ROUNDS_TO_MARKER2 = 6
ALPHA = 0.05


def _jl(p):
    try:
        return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    except (OSError, ValueError):
        return []


def _jl_lines(p):
    """One line at a time: a bad line is skipped, never the file."""
    out = []
    try:
        for l in open(p, encoding="utf-8"):
            if l.strip():
                try:
                    r = json.loads(l)
                except ValueError:
                    continue
                if isinstance(r, dict):
                    out.append(r)
    except OSError:
        pass
    return out


def _stamp():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


# ---- the frame and its material ------------------------------------------------------------------

def store(root):
    s = os.path.join(root, "package", "store")
    return {n: _jl(os.path.join(s, n + ".jsonl")) for n in ("rooms", "codes", "themes")}


def analysed(root, out, st=None):
    st = st or store(root)
    dropped = {vlib.canon(d.get("sub")).lower() for d in _jl(os.path.join(out, "dropped.jsonl"))}
    return [r["sub"] for r in st["rooms"] if r.get("sub") and r["sub"].lower() not in dropped]


def words(st):
    w = collections.Counter()
    for c in st["codes"]:
        w[c.get("sub")] += len(str(c.get("text") or "").split())
    for t in st["themes"]:
        w[t.get("sub")] += len(str(t.get("second_order") or "").split()) + len(str(t.get("theme_note") or "").split())
    return w


def seed(root):
    """The seed: the sha256 of package/store/rooms.jsonl, frozen in out/seed.txt at B1's first draw, so a later
    rebuild of the store cannot reshuffle B1's walk."""
    f = os.path.join(root, "out", "seed.txt")
    if os.path.exists(f):
        s = open(f, encoding="utf-8").read().strip()
        if s:
            return s
    p = os.path.join(root, "package", "store", "rooms.jsonl")
    try:
        return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    except OSError:
        return "0"


def shuffled(units, sd, tag):
    u = sorted(units)
    random.Random("%s:%s" % (sd, tag)).shuffle(u)
    return u


# ---- the estimates ---------------------------------------------------------------------------------

def estimates(sets):
    T = len(sets)
    freq = collections.Counter(k for s in sets for k in s)
    S, U = len(freq), sum(len(s) for s in sets)
    Q1 = sum(1 for v in freq.values() if v == 1)
    Q2 = sum(1 for v in freq.values() if v == 2)
    e = {"T": T, "U": U, "S": S, "Q1": Q1, "Q2": Q2, "C": None, "Q0": None, "next_in": None}
    if T < 2 or not S:
        return e
    Q0 = (T - 1) / T * (Q1 * Q1 / (2 * Q2) if Q2 else Q1 * (Q1 - 1) / 2)
    C = 1.0 if not Q1 else 1 - (Q1 / U) * ((T - 1) * Q1 / ((T - 1) * Q1 + 2 * Q2))
    r = Q0 * Q1 / (T * Q0 + Q1) if Q0 > 0 and Q1 > 0 else 0.0
    e.update(C=round(C, 4), Q0=round(Q0, 2), next_in=(round(1 / r, 1) if r > 0 else None))
    return e


def bound(N, n, k):
    """The smallest K (unread units carrying an unseen kind) rejected at ALPHA; None when none is."""
    if n <= 0 or N <= 0:
        return None
    for K in range(k + 1, N + 1):
        p = sum(math.comb(K, j) * math.comb(N - K, n - j) for j in range(0, min(k, n) + 1)) / math.comb(N, n)
        if p < ALPHA:
            return K
    return None


# ---- the stages ------------------------------------------------------------------------------------

def data(root, out, stage, st=None):
    """(order, done, incidence) for a stage. order: the units in the order they are meant to be read;
    done: the units read whole; incidence: unit -> the kinds it shows."""
    st = st or store(root)
    an = set(analysed(root, out, st))
    inc = {}
    if stage == "B1":
        f = os.path.join(out, "seed.txt")
        if not os.path.exists(f) and os.path.isdir(out):     # frozen at the first draw
            open(f, "w", encoding="utf-8").write(seed(root) + "\n")
        order = shuffled(sorted(an), seed(root), "B1")
        order, done, _ = vlib.b1_progress(out, st["themes"], an, order)
        order = order or []
        led = os.path.join(out, "kinds-B1.jsonl")
        if os.path.exists(led):          # the kinds as met, append only (mem.py mint, place, log merged|split)
            for r in _jl_lines(led):
                if r.get("at") and r.get("kind"):
                    inc.setdefault(vlib.canon(r["at"], an), set()).add(r["kind"])
        else:                            # no ledger (a run from before 2026-09-29): the current grouping
            cur = os.path.join(out, "scheme", "scheme_current.jsonl")
            if not os.path.exists(cur):
                cur = os.path.join(out, "scheme_current.jsonl")
            for r in _jl_lines(cur):
                for m in r.get("members") or []:
                    inc.setdefault(vlib.canon(m.get("sub"), an), set()).add(r.get("theme"))
        return order, done, {s: inc.get(s, set()) for s in order}
    raise SystemExit("the stopping rule covers stage B1 only; A1 reads every room and counts no kinds (J, 2026-09-29)")


def holdings(root, out, an):
    """B1's ledger as (at, sub, kind): a kind is met while `at` is read, and held by `sub`, the room whose
    second-order theme was placed. The estimates count a kind in the room that holds it, as Chao et al. 2014
    assume of incidence data (J, 2026-09-29); what is new, and when, is still read from `at`."""
    led = os.path.join(out, "kinds-B1.jsonl")
    if not os.path.exists(led):
        return None
    return [(vlib.canon(r["at"], an), vlib.canon(r.get("sub") or r["at"], an), r["kind"])
            for r in _jl_lines(led) if r.get("at") and r.get("kind")]


def replay(root, out, stage, st=None):
    st = st or store(root)
    order, done, inc = data(root, out, stage, st)
    held_lines = holdings(root, out, set(analysed(root, out, st))) if stage == "B1" else None
    if held_lines is None:               # no ledger: a kind is held where it is met
        held_lines = [(u, u, k) for u, ks in inc.items() for k in ks]
    by_at = collections.defaultdict(list)
    for at, sub, k in held_lines:
        by_at[at].append((sub, k))
    held, waiting = collections.defaultdict(set), collections.defaultdict(set)
    w = words(st)
    an = analysed(root, out, st)
    avg = (sum(w[s] for s in an) / len(an)) if an else 1.0
    avg = avg or 1.0
    total_words = sum(w[s] for s in an)
    sd = seed(root)
    decisions = {}
    for d in _jl_lines(os.path.join(out, "stopping-%s-decision.jsonl" % stage)):
        decisions[d.get("point") or "marker 3"] = d.get("decision")
    decision = decisions.get("marker 3")
    R = {"stage": stage, "avg_words": round(avg, 1), "units": len(order), "total_words": total_words,
         "rounds": [], "markers": {}, "draw": None, "state": "reading", "next": None, "resets": 0,
         "seq": [], "decision": decision, "decisions": decisions, "checkin": None}
    if not order:
        R.update(state="no order yet (the analysed set is empty)",
                 now={"rooms_read": 0, "x": 0.0, "words_share": 0.0, "S": 0, "C": None, "Q0": None, "T": 0},
                 new_kinds=[], left={"rooms": 0, "words": total_words, "avg_rooms": round(total_words / avg, 1)},
                 out_of_turn=sorted(done))
        return R
    used, seen = set(), set()
    sets_now = lambda: [held[r] for r in R["seq"]]
    x, last_new, rcount, last_new_n = 0.0, 0.0, 0, 0
    state, draw_q = "run", []
    first_new = {}

    def snap():
        e = estimates(sets_now())
        return dict(e, rooms_read=len(R["seq"]), x=round(x, 1),
                    words_share=round(sum(w[s] for s in R["seq"]) / total_words, 4) if total_words else None)

    def start_round():
        e = estimates(sets_now())
        if e["next_in"] is not None:
            per = x / len(R["seq"]) if R["seq"] else 1.0     # average rooms per room read so far: the estimate
            H = max(1.0, min(e["next_in"] * per, x, ROUND_MAX))  # is in rooms, the round in average rooms; never
                                                               # past double what is read (Chao et al. 2014), nor 25
        else:                                          # no kind seen once: the estimate expects none; the
            prev = R["rounds"][-1]["length"] if R["rounds"] else 0.0   # round is as long as the last one, at least 10
            H = min(max(float(ROUND_GAP), prev), float(ROUND_MAX))
        R["rounds"].append({"n": len(R["rounds"]) + 1, "in_row": rcount + 1, "start_rooms": len(R["seq"]), "start_x": round(x, 1),
                            "predicted": e["next_in"], "length": round(H, 1), "end_x": round(x + H, 1),
                            "C": e["C"], "Q0": e["Q0"], "S": e["S"], "long": H > 10, "result": "open"})

    while True:
        if state == "drawn":                 # the draw is read: marker 3, then the PI decides (B1)
            R["draw"]["bound"] = bound(R["draw"]["N"], R["draw"]["n"], R["draw"]["k"])
            R["markers"][3] = dict(snap(), draw_n=R["draw"]["n"], draw_k=R["draw"]["k"])
            if stage == "B1" and decision != "finish":
                R["state"] = "report" if decision is None else "stopped"
                break
            state = "after"
            continue
        if (R["checkin"] is None and 3 not in R["markers"] and state not in ("after",) and total_words
                and x >= BURN_IN and len(R["seq"]) >= BURN_IN_ROOMS
                and sum(w[s] for s in R["seq"]) >= CHECK_IN * total_words):
            R["checkin"] = snap()
            dci = decisions.get("check-in")
            if stage == "B1" and dci is None:
                R["state"] = "check-in"
                break
            if stage == "B1" and dci == "stop":
                R["state"] = "stopped"
                break
            if stage == "B1" and dci == "finish":
                state = "after"
                continue
        if state == "draw":
            u = next((s for s in draw_q if s not in used), None)
        else:
            u = next((s for s in order if s not in used), None)
        if u is None:
            if state == "draw":            # the unread units ran out inside the draw
                state = "drawn"
                continue
            R["state"] = "end"
            break
        if u not in done:
            R["next"] = u
            R["state"] = {"run": "reading", "round": "round %d" % (rcount + 1), "draw": "draw",
                          "after": "reading on after marker 3"}.get(state, state)
            break
        used.add(u)
        R["seq"].append(u)
        new = inc.get(u, set()) - seen
        seen |= inc.get(u, set())
        held[u] |= waiting.pop(u, set())             # kinds placed into this room's themes before it was read
        for sub, k in by_at.get(u, []):
            (held[sub] if sub in used else waiting[sub]).add(k)
        x += (w[u] or 1) / avg
        for k in new:
            first_new[k] = {"kind": k, "unit": u, "rooms_read": len(R["seq"]), "x": round(x, 1)}
        if state == "draw":
            R["draw"]["n"] += 1
            R["draw"]["k"] += 1 if new else 0
            R["draw"]["words"] += w[u]
            R["draw"]["units"].append(u)
            if new:                          # a new kind in the draw restarts the count (J, 2026-09-29)
                R.setdefault("draws_reset", []).append(dict(R["draw"], at=u))
                R["draw"] = None
                R["resets"] += 1
                R["markers"].pop(1, None)
                R["markers"].pop(2, None)
                last_new, last_new_n = x, len(R["seq"])
                state, rcount = "run", 0
                continue
            if R["draw"]["words"] >= R["draw"]["target_words"]:
                state = "drawn"
            continue
        if state == "after":
            continue
        if new:
            last_new, last_new_n = x, len(R["seq"])
            if state == "round":
                R["rounds"][-1]["result"] = "new"
                R["resets"] += 1
                R["markers"].pop(1, None)
                R["markers"].pop(2, None)
            state, rcount = "run", 0
            continue
        n = len(R["seq"])
        if (state == "run" and x - last_new >= ROUND_GAP and n - last_new_n >= ROUND_GAP
                and x >= BURN_IN and n >= BURN_IN_ROOMS):
            state = "round"
            start_round()
        elif state == "round" and x >= R["rounds"][-1]["end_x"]:
            R["rounds"][-1]["result"] = "empty"
            rcount += 1
            if rcount == ROUNDS_TO_MARKER1:
                R["markers"][1] = snap()
            if rcount == ROUNDS_TO_MARKER2:
                R["markers"][2] = snap()
                m1 = R["markers"][1]
                target = sum(w[s] for s in R["seq"][m1["rooms_read"]:])
                rest = [s for s in order if s not in used]
                draw_q = shuffled(rest, sd, "draw-%d" % len(R["seq"])) if stage == "B1" else rest
                R["draw"] = {"N": len(rest), "n": 0, "k": 0, "words": 0, "target_words": target, "units": [],
                             "target_rooms": round(target / avg, 1), "bound": None}
                state = "draw"
            else:
                start_round()
    if R["state"] in ("check-in", "stopped"):
        R["next"] = None
    R["now"] = snap()
    R["new_kinds"] = sorted(first_new.values(), key=lambda d: d["rooms_read"])
    read_words = sum(w[s] for s in R["seq"])
    R["left"] = {"rooms": len([s for s in order if s not in used]),
                 "words": total_words - read_words,
                 "avg_rooms": round((total_words - read_words) / avg, 1)}
    R["out_of_turn"] = sorted(done - used)
    return R


# ---- the report ------------------------------------------------------------------------------------

def report_md(R):
    L = ["# When to stop, stage %s" % R["stage"], "",
         "Written by `tools/saturation.py report` at %s. The rule: `saturation.py` docstring; J, 2026-09-29." % _stamp(), ""]
    now, left = R["now"], R["left"]
    L += ["## Where the reading stands", "",
          "| | |", "|---|---:|",
          "| rooms read | %d of %d |" % (now["rooms_read"], R["units"]),
          "| share of the words read | %s |" % ("%.1f%%" % (100 * now["words_share"]) if now["words_share"] is not None else "n/a"),
          "| rooms left | %d |" % left["rooms"],
          "| words left, in average rooms (%s words each) | %s |" % (R["avg_words"], left["avg_rooms"]),
          "| kinds seen | %s |" % now["S"],
          "| coverage now | %s |" % now["C"],
          "| unseen kinds estimated now | %s |" % now["Q0"],
          "| state | %s |" % R["state"], ""]
    L += ["## The markers", "", "| marker | rooms read | average rooms read | coverage | unseen kinds | share of words |",
          "|---|---:|---:|---:|---:|---:|"]
    names = {1: "1: three empty rounds (the literature's stop)", 2: "2: three more empty rounds", 3: "3: the draw read"}
    for k in (1, 2, 3):
        m = R["markers"].get(k)
        L.append("| %s | %s | %s | %s | %s | %s |" % (names[k], *(("-",) * 5 if not m else
                 (m["rooms_read"], m["x"], m["C"], m["Q0"], "%.1f%%" % (100 * m["words_share"]) if m["words_share"] is not None else "n/a"))))
    c = R.get("checkin")
    L.append("| check-in: %d%% of the words read before marker 3 | %s |" % (round(100 * CHECK_IN), "-" if not c else
             "%s | %s | %s | %s | %s" % (c["rooms_read"], c["x"], c["C"], c["Q0"], "%.1f%%" % (100 * c["words_share"]))))
    L.append("")
    if R["draw"]:
        d = R["draw"]
        L += ["## The draw", "",
              "%d rooms drawn at random from the %d unread at marker 2, %d words (the three rounds between the markers read %d); "
              "%d brought a new kind. %s" % (
                  d["n"], d["N"], d["words"], d["target_words"], d["k"],
                  ("With 95%% confidence, %d or more unread rooms carrying an unseen kind are ruled out." % d["bound"])
                  if d["bound"] else ("The draw is still being read." if R["state"] == "draw" or 3 not in R["markers"]
                                      else "The draw is too small to rule anything out at 95%.")), ""]
        if left["avg_rooms"] <= d["target_rooms"]:
            L += ["What is left (%s average rooms) is no larger than the draw was (%s): reading everything costs no "
                  "more than the draw did." % (left["avg_rooms"], d["target_rooms"]), ""]
    L += ["## The rounds", "", "| round | began at room | predicted next kind in | length (average rooms) | coverage | unseen | result |",
          "|---:|---:|---:|---:|---:|---:|---|"]
    for r in R["rounds"]:
        L.append("| %d | %d | %s | %s%s | %s | %s | %s |" % (r["n"], r["start_rooms"], r["predicted"], r["length"],
                                                             " (over 10)" if r["long"] else "", r["C"], r["Q0"], r["result"]))
    L += ["", "Resets (a new kind inside a round or the draw): %d." % R["resets"], ""]
    for d in R.get("draws_reset") or []:
        L += ["A draw was cut short at r/%s (room %d of the draw), which brought a new kind; the count started again." % (d["at"], d["n"]), ""]
    L += ["## When each kind first came", "",
          "| kind | room | rooms read | average rooms read |", "|---|---|---:|---:|"]
    L += ["| %s | %s | %d | %s |" % (d["kind"], d["unit"], d["rooms_read"], d["x"]) for d in R["new_kinds"]]
    if R["stage"] == "B1" and R["state"] == "check-in":
        L += ["", "**The check-in: %d%% of the words are read and marker 3 is not reached. The stage pauses here: the PI "
              "decides to continue under the rule (`saturation.py decide --stage B1 continue`), finish the list "
              "(`... finish`) or stop (`... stop`).**" % round(100 * CHECK_IN)]
    if R["stage"] == "B1" and R["state"] == "report":
        L += ["", "**The three markers are reached. The stage pauses here: the PI decides whether to finish the list "
              "(`saturation.py decide --stage B1 finish`) or stop (`... stop`).**"]
    return "\n".join(L) + "\n"


def status_lines(R):
    now = R["now"]
    L = ["saturation %s: %s; %d of %d rooms read (%s of the words); kinds %s, coverage %s, unseen %s; rounds %d, "
         "markers %s" % (R["stage"], R["state"], now["rooms_read"], R["units"],
                         "%.1f%%" % (100 * now["words_share"]) if now["words_share"] is not None else "n/a",
                         now["S"], now["C"], now["Q0"], len(R["rounds"]), ",".join(map(str, sorted(R["markers"]))) or "none")]
    if R["rounds"] and R["rounds"][-1]["result"] == "open":
        r = R["rounds"][-1]
        L.append("round %d open: predicted next kind in %s rooms; reads to %s average rooms (now %s)%s"
                 % (r["n"], r["predicted"], r["end_x"], now["x"], "; this round is over 10 rooms: log it" if r["long"] else ""))
    if R["next"]:
        L.append("next: %s" % R["next"])
    elif R["state"] == "check-in":
        L.append("the check-in: %d%% of the words are read before marker 3; write the report (saturation.py report "
                 "--stage %s), log it, and close with done.sh %s --pause for the PI's decision (continue, finish or stop)"
                 % (round(100 * CHECK_IN), R["stage"], R["stage"]))
    elif R["state"] == "report":
        L.append("the three markers are reached: write the report (saturation.py report --stage %s), log it, and "
                 "close with done.sh %s --pause for the PI's decision" % (R["stage"], R["stage"]))
    if R["out_of_turn"]:
        L.append("read out of turn: %s" % ", ".join(R["out_of_turn"][:10]))
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("verb", choices=("order", "status", "report", "decide"))
    ap.add_argument("what", nargs="?")
    ap.add_argument("--stage", required=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--why", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    out = os.path.abspath(a.out or os.path.join(root, "out"))
    stage = a.stage.upper()
    if a.verb == "order":   # print only: the second pass (B1d) walks this order again
        if stage != "B1":
            raise SystemExit("order is B1's; A1's order is the analyst's, in out/order-A1.txt")
        order, done, _ = data(root, out, "B1")
        for i, s in enumerate(order, 1):
            print("%d\t%s\t%s" % (i, s, "read" if s in done else "unread"))
        return 0
    if a.verb == "decide":
        R = replay(root, out, stage)
        point = {"check-in": "check-in", "report": "marker 3"}.get(R["state"])
        allowed = {"check-in": ("continue", "finish", "stop"), "marker 3": ("finish", "stop")}.get(point, ())
        if not point:
            raise SystemExit("nothing waits for a decision (state: %s)" % R["state"])
        if a.what not in allowed or not a.why.strip():
            raise SystemExit('at the %s: decide %s --why "the PI\'s words"' % (point, "|".join(allowed)))
        with open(os.path.join(out, "stopping-%s-decision.jsonl" % stage), "a", encoding="utf-8") as f:
            f.write(json.dumps({"t": _stamp(), "stage": stage, "point": point, "decision": a.what, "why": a.why}) + "\n")
        print("decision logged at the %s: %s" % (point, a.what))
        return 0
    R = replay(root, out, stage)
    if a.verb == "report":
        p = os.path.join(out, "stopping-%s.md" % stage)
        open(p, "w", encoding="utf-8").write(report_md(R))
        print("written %s" % os.path.relpath(p, root))
        return 0
    if a.json:
        print(json.dumps({k: v for k, v in R.items() if k != "seq"}, ensure_ascii=False, indent=1))
    else:
        print("\n".join(status_lines(R)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
