#!/usr/bin/env python3
"""C5b: stage C5's readers' entry in out/run_manifest.json (stage C5 section 8: the readers' model, seed, decoding and
count), with account.md, figure-C5.md, propositions.jsonl, author_claims.jsonl and RETURN-C5.md pinned by sha256.
Keeps the file's own formatting (a list, indent 1).

    python3 out/_analysis/c5b_manifest_entry.py --write      append the entry; refuses if a C5 entry is there
    python3 out/_analysis/c5b_manifest_entry.py --packets    add the three packets (path, bytes, sha256) to that
                                                             entry, once packets.py has written them
"""
import datetime, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
MP = os.path.join(OUT, "run_manifest.json")


def sha(p):
    return hashlib.sha256(open(os.path.join(OUT, p), "rb").read()).hexdigest()


raw = open(MP, encoding="utf-8").read()
man = json.loads(raw)
ascii_only = "\\u" in raw
c5 = [e for e in man if isinstance(e, dict) and str(e.get("stage")) == "C5"]
if "--write" in sys.argv:
    if c5:
        sys.exit("a stage C5 entry is already in run_manifest.json; not appended again")
    entry = {
        "stage": "C5",
        "leg": "C5b",
        "step": "the readers' build (stage C5 section 8): three readers, once, after the passes stopped at pass 4",
        "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "model": "claude-opus-5-5 x1 per packet via cli, the reviewer route PLATFORM-claude.md sets for C5 (Opus "
                 "through the Claude CLI, each reader in a session of its own, sent by the operator's fleet.py); the "
                 "model that served is recorded by the dispatch in arm.json",
        "decoding": {"temperature": None, "top_p": None,
                     "note": "set by the dispatch (fleet.py) and the CLI, which this session cannot read; the dispatch "
                             "records what served"},
        "seeds": {"rooms_draw": 20261015, "room_passages": 20261015,
                  "note": "one room per pool by random.Random(20261015) (c5b_rooms_draw2.py); each room's 7 passages "
                          "by cite.py's own seeded draw (--grep . --n 7 --seed 20261015); the Stigmergy records are "
                          "the 72 drawn at C5a-01 with seed 20261015 (c5_stigmergy_sample.py), 24 to each reader"},
        "n_agents": 3,
        "pass_served": 4,
        "account_sha256": sha("account.md"),
        "served": {"account.md": sha("account.md"), "figure-C5.md": sha("figure-C5.md"),
                   "propositions.jsonl": sha("propositions.jsonl")},
        "author_claims": {"path": "out/author_claims.jsonl", "sha256": sha("author_claims.jsonl"), "n": 9},
        "return_spec": {"path": "out/RETURN-C5.md", "sha256": sha("RETURN-C5.md"),
                        "keys": ["reader", "served", "claims", "relations", "could_not_follow", "unsupported", "rooms",
                                 "declarations", "codes"],
                        "note": "the stage's return line, with two keys added for the second reading J's ruling 4 of "
                                "15 October asks of the C5 readers: declarations and codes"},
        "rooms": {"drawn": {"reached easily (told, pass 5 story)": "cardinals",
                            "the last story could not tell (told with a residue)": "luciomains",
                            "the late side of the onset contrast": "mysterydungeon"},
                  "served": "facts lines of room --no-canvas (all above the thread list but the forest summary) and "
                            "7 coded passages by cite.py's seeded draw; the forest is not served",
                  "why": "a drawn room's forest runs to 10 KB or more, and each packet must hold account.md, "
                         "figure-C5.md and propositions.jsonl (35,073 bytes) under the 51,200-byte ceiling"},
        "second_reading": {"ruling": "J, 15 October 01:29 Berlin, ruling 4: the C5 readers are the second reader for "
                                     "the declaration prose pass; the PI's C5b message adds the Stigmergy codes",
                           "served": "the rule (its reading parts and the C5a-02 scope paragraph); the 40 sentences of "
                                     "the 36 amended declarations that the rule's word lists put in question "
                                     "(c5b_in_question.py), whole declarations split across the three readers by "
                                     "bytes; the Stigmergy code definitions and the 24 records of one member theme "
                                     "per reader, through cite.py, with no code of mine and no coder's label",
                           "not_served": "the whole amended declarations; their sentences outside the rule's word "
                                         "lists, with the quotes those carry; the forests of the rooms",
                           "split": {"1": "T3-038", "2": "T3-041", "3": "T3-060"}},
        "pages": "out/_analysis/c5b/r1..r3/0-read-me-first.md and second-reading.md (c5b_pages.py); "
                 "out/_analysis/c5b/shared/rooms.md (c5b_rooms_draw2.py)",
        "build": "python3 tools/packets.py files --stage C5 --name C5-reader-k out/_analysis/c5b/rk/0-read-me-first.md "
                 "out/account.md out/figure-C5.md out/propositions.jsonl out/_analysis/c5b/shared/rooms.md "
                 "out/_analysis/c5b/rk/second-reading.md, for k = 1, 2, 3",
        "ids": "room names and concept ids as the account cites them; element, arrow, proposition, finding and "
               "declaration ids; no canvas field",
        "notes": "The returns land in out/_fleet_raw/C5/; the check leg copies them into readers-C5/ and scores "
                 "fidelity both ways, the readers' sentence verdicts and their codes against mine.",
    }
    man.append(entry)
    open(MP, "w", encoding="utf-8").write(json.dumps(man, indent=1, ensure_ascii=ascii_only))
    print("appended; run_manifest.json now holds %d entries" % len(man))
elif "--packets" in sys.argv:
    if len(c5) != 1:
        sys.exit("expected one stage C5 entry, found %d" % len(c5))
    pk = []
    for k in (1, 2, 3):
        p = os.path.join("_packets-C5", "C5-reader-%d.md" % k)
        pk.append({"name": "C5-reader-%d" % k, "path": "out/" + p, "bytes": os.path.getsize(os.path.join(OUT, p)),
                   "sha256": sha(p), "ceiling": 51200})
    c5[0]["packets"] = pk
    # the served files' digests, read again, in case a served file was rewritten before the packets
    c5[0]["served"] = {f: sha(f) for f in ("account.md", "figure-C5.md", "propositions.jsonl")}
    c5[0]["account_sha256"] = sha("account.md")
    open(MP, "w", encoding="utf-8").write(json.dumps(man, indent=1, ensure_ascii=ascii_only))
    print("packets added to the C5 entry: %s" % ", ".join("%s %d bytes" % (x["name"], x["bytes"]) for x in pk))
else:
    print(__doc__)
