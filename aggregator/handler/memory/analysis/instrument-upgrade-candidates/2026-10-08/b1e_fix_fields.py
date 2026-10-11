#!/usr/bin/env python3
"""B1e: rewrite draft gate fields that name legs, theme or concept ids, notes or working counts.

The stranger holds fifty second-order themes and one family's tests (section 3); a gate that says
"B1d-06", "rainbowgrid t02", "c0422" or "69 bag lines" refers to what the reader is not given.
Each entry below replaces one whole field in its draft line; the case it described stays, in
words. Dry run by default; --write rewrites the draft files in place.
"""
import glob, json, os, sys

AN = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "out", "_analysis")

FIX = {
    ("T3-001", "is_not"): "Members proposing pranks to play on friends away from the site: nothing is staged in the room, so it is the sub's usual talk (T3-017).",
    ("T3-023", "varies"): "From a one-day styling swap to a full change of subject with removals enforced; from the moderators alone to a whole sub raiding another sub as a joke.",
    ("T3-032", "decide_when_both"): "A theme that stages or plays the jokes and objects to them keeps the staging kind as primary and adds T3-032 when the objecting has three or more concepts.",
    ("T3-017", "is_not"): "Members trading outside creators' April Fools releases as examples of the day done well: that is reacting to official April Fools (T3-048).",
    ("T3-014", "decide_when_both"): "Moving into a chat and relaying its decisions: T3-014 primary, T3-152 added when the relay has concepts of its own; meeting other rooms there adds T3-153.",
    ("T3-152", "decide_when_both"): "The move into the chat is T3-014, the relay of its decisions T3-152; when both have concepts of their own, the larger is primary.",
    ("T3-002", "varies"): "From one 'come help me out' that draws no reply to repeated rallies through a long build; calls to start, to finish, to repair; calls to placers repeating a pattern before any group exists.",
    ("T3-002", "is_not"): "Calls to build the room's national flag (T3-065).",
    ("T3-044", "decide_when_both"): "Whose eyes find the mark: outsiders led to the sub go to T3-044; the room's own members finding work they did not know of go to T3-082.",
    ("T3-125", "is_not"): "A room drawing the line between its coordinated members and placers it does not control (T3-188).",
    ("T3-074", "decide_when_both"): "Doubting whether the room can manage a work at all, even during the work, goes to T3-136; working around the timer and too few hands while building goes to T3-074. Glitches: explaining how the canvas or a glitch works is T3-016; using a glitch to place beyond the limit is T3-088; coping with a glitch that stops or delays placing is T3-074.",
    ("T3-136", "decide_when_both"): "Doubting whether the room can manage a work at all, even mid-work, goes to T3-136; working around the timer and too few hands while building goes to T3-074.",
    ("T3-020", "varies"): "From a quick 'top right corner!' to long searches across a full canvas; spots beside kindred works; striking where the defence is weak.",
    ("T3-033", "varies"): "From one member's wish to put a symbol on the canvas to a series of picture proposals; political slogans proposed as such sit here.",
    ("T3-033", "decide_when_both"): "A theme whose lead is recruiting hands to a picture is T3-002; one whose lead is offering the room an idea of what to make is T3-033.",
    ("T3-169", "decide_when_both"): "Writing the sub's name is T3-169's doing; a call to write it is its form, and one concept carries one placement.",
    ("T3-082", "decide_when_both"): "Whose eyes find the mark: the room's own members finding work they did not know of go to T3-082; outsiders led to the sub go to T3-044.",
    ("T3-087", "decide_when_both"): "Tracing with defence: T3-005 primary when the fight leads, T3-087 added when the tracing has concepts of its own. Members doubting that a damage was the room's own are tracing it (T3-087); an organised room telling others its plan does not cover such placers is T3-188.",
    ("T3-121", "varies"): "From shunning a single traitor to a three-day cooling-off; a ban from the room's Discord challenged and reversed.",
    ("T3-126", "varies"): "From a false moderator claim exposed to a random member denying they are the official mediator; a room telling other Discords not to decide for its art; a pattern's repeaters with no one to speak for them.",
    ("T3-126", "decide_when_both"): "Separating the organised plan from placers it does not control is T3-188; who may speak for the room is T3-126.",
    ("T3-188", "decide_when_both"): "An outside room's denial counts when it separates its organised members from placers acting in its name (a fandom room's Danish members, a crusader room's Norwegian ally); a bare 'it was not us' that points to another room is tracing (T3-087). Separating the plan from such placers is T3-188; who may speak for the room is T3-126.",
    ("T3-027", "decide_when_both"): "Running and arguing: T3-028 primary when the scripts are run, T3-027 added when the argument has concepts of its own. A bot rumour, or saying a defence was scripts rather than people, goes here when fairness is in question.",
    ("T3-006", "decide_when_both"): "Replacing or attacking another room's mark, another nation's flag included: destroying or blacking it out is T3-006; turning it into the room's sign is T3-068; growing the room's work over the neighbour's space is T3-061. A theme with more than one: the larger part primary, the others under rule 0.",
    ("T3-024", "decide_when_both"): "Restraint inside a border deal: T3-010 primary when the deal leads, T3-024 added when the restraint has concepts of its own. Sparing others' work by the room's own choice is T3-024; agreeing lines with a neighbour is T3-010.",
    ("T3-046", "decide_when_both"): "An argument that ends in restraint: T3-046 when the argument leads, T3-024 when the restraint does. Stopping the room's own attack is T3-076; arguing whether such covering is fair is T3-046.",
    ("T3-010", "decide_when_both"): "A pact ending or forestalling a fight between rooms already in contact goes to T3-149; an agreement drawing borders or sharing space where no fight began goes to T3-010. A theme that holds several kinds of deal keeps the leading one as primary.",
    ("T3-011", "decide_when_both"): "Help given in return is T3-151; help given with nothing asked is T3-011.",
    ("T3-099", "decide_when_both"): "Protection given by the bigger room, told from its side, is not here: it sits with the help it is (T3-011) or the alliance (T3-150).",
    ("T3-149", "decide_when_both"): "A pact ending or forestalling a fight between rooms already in contact goes to T3-149; an agreement drawing borders or sharing space where no fight began goes to T3-010. A truce invoked against a breach is T3-195 when the invoking leads.",
    ("T3-151", "decide_when_both"): "Help given in return is T3-151, help with nothing asked T3-011.",
    ("T3-194", "decide_when_both"): "The envoy's errand is T3-194, the deal it carries T3-010 or its kin; when both have concepts of their own, the larger is primary.",
    ("T3-195", "decide_when_both"): "A theme that makes a deal and later invokes it keeps the larger part as primary and adds the other under rule 0.",
    ("T3-193", "varies"): "From a nation's members refusing to submit to hearts and neighbours to a rival fandom's room defending a joint logo.",
    ("T3-065", "decide_when_both"): "The flag of the room's land as its mark is T3-065, calls for hands to any other picture T3-002. A flag with emblems drawn into it: T3-065 for the flag, T3-113 when the emblems have concepts of their own.",
    ("T3-065", "must_not_show"): "Calls for hands to any other picture (T3-002); emblems and pictures drawn beside or inside the flag (T3-113); helping another nation's flag (T3-078).",
    ("T3-113", "decide_when_both"): "A flag with emblems: see T3-065. A political emblem argued over: T3-080 when the argument leads. Veiled fascist emblems drawn into a national room's work sit here.",
    ("T3-081", "is_not"): "A streamer's fans calling a raid on a rival logo a war: a game-fandom war has no national history.",
    ("T3-081", "must_not_show"): "War language for fights between game fandoms or teams with no national history (T3-050, T3-005); national politics read into the canvas outside a fight (T3-130).",
    ("T3-130", "decide_when_both"): "A target chosen for national political reasons and converted, as when a national room puts its own flag over another nation's: T3-068 for the converting, T3-130 for the national reason when it has concepts of its own.",
    ("T3-146", "decide_when_both"): "Hate symbols and slurs covered are T3-146; obscene drawings and ordinary insults covered are repair (T3-021). A theme that covers swastikas and refuses requests to draw them keeps T3-146 primary, with T3-177 added when the calls have concepts of their own.",
    ("T3-177", "varies"): "From a proposal to turn a rival channel's logo into a swastika to members drawing one on their own room's logo.",
}


def main():
    write = "--write" in sys.argv
    done = set()
    for p in sorted(glob.glob(os.path.join(AN, "b1e_draft_G*.jsonl"))):
        with open(p, encoding="utf-8") as f:
            rows = [json.loads(x) for x in f if x.strip()]
        changed = 0
        for r in rows:
            for (tid, k), v in FIX.items():
                if r["id"] == tid:
                    if r[k] != v:
                        r[k] = v
                        changed += 1
                    done.add((tid, k))
        if changed:
            print("%s: %d field(s)" % (os.path.basename(p), changed))
            if write:
                with open(p, "w", encoding="utf-8") as f:
                    for r in rows:
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
    left = sorted(set(FIX) - done)
    print("fixes %d, applied to %d fields; not found: %s; %s" % (len(FIX), len(done), left, "written" if write else "dry run"))


if __name__ == "__main__":
    main()
