#!/usr/bin/env python3
"""C2b: append stage C2's reviewer entry to out/run_manifest.json (stage C2 section 6: the reader's model, seed,
decoding and count), with the packet, the return specification and the model served pinned by sha256. Refuses if a
stage C2 entry is already there. Keeps the file's own formatting (a list, indent 1).

    python3 out/_analysis/c2b_manifest_entry.py [--write]
"""
import datetime, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
MP = os.path.join(OUT, "run_manifest.json")


def sha(p):
    return hashlib.sha256(open(os.path.join(OUT, p), "rb").read()).hexdigest()


raw = open(MP, encoding="utf-8").read()
man = json.loads(raw)
if not isinstance(man, list):
    sys.exit("run_manifest.json is not a list")
if any(isinstance(e, dict) and str(e.get("stage")) == "C2" for e in man):
    sys.exit("a stage C2 entry is already in run_manifest.json; not appended again")
pk = os.path.join("_packets-C2", "C2-reviewer.md")
entry = {
    "stage": "C2",
    "leg": "C2b",
    "step": "the reviewer's build (stage C2 section 6): one hostile reader, once, before the final passes",
    "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "model": "claude-opus-5-5 x1 via cli, the reviewer route PLATFORM-claude.md sets for C2 (Opus through the Claude "
             "CLI, a session of its own, sent by the operator's fleet.py); the model that served is recorded by the "
             "dispatch in arm.json",
    "decoding": {"temperature": None, "top_p": None,
                 "note": "set by the dispatch (fleet.py) and the CLI, which this session cannot read; the dispatch "
                         "records what served"},
    "seeds": {"draw": None, "note": "no draw: one packet, one reader; the packet's contents are fixed by "
                                    "out/_analysis/c2b_reviewer_sources.py with the options in `build`"},
    "n_agents": 1,
    "pass_served": 3,
    "packet": {"name": "C2-reviewer", "path": "out/" + pk, "bytes": os.path.getsize(os.path.join(OUT, pk)),
               "sha256": sha(pk), "ceiling": 51200},
    "return_spec": {"path": "out/RETURN-C2.md", "sha256": sha("RETURN-C2.md")},
    "model_served": {"file": "out/model-p3.md", "sha256": sha("model-p3.md"),
                     "sections_served_verbatim": ["the title line", "What the model says, in prose", "The elements",
                                                  "The arrows"],
                     "not_served": ["the opening above the first section", "Theorised arrows, and the model with and "
                                    "without them", "The model on the dimensions", "Dynamics",
                                    "Ungrounded relationships", "Looked for and not found",
                                    "The tiers the arrows run between, and what the model does not use",
                                    "Where the model should break, in its own terms",
                                    "The three strongest arrows, read as artefacts", "Two tests"],
                     "why": "model-p3.md alone is 51,723 bytes, over the 50 KB packet ceiling (FLEET.md); the "
                            "return's served names this file's sha256 as the model the sections were drawn from"},
    "pages": ["0-instruction.md (the instruction verbatim, what is served, the served sha256)",
              "model-p3-sections.md (the sections above, verbatim)", "story-p3.md (out/model/story-p3.md, whole, "
              "sha256 %s)" % sha(os.path.join("model", "story-p3.md")),
              "criterion.md (notes-C2.md's criterion paragraph, verbatim)",
              "tiers.md (fourth.jsonl, dimensions.jsonl and scheme_v2.jsonl rendered: every third-order theme by "
              "name; dimension questions not served)", "verbs.md (cite.py and mem.py read verbs, room --no-canvas)"],
    "not_served_at_all": "structure.md and structure-p2.md (about 1 MB each), the model ledgers as files "
                         "(the elements and arrows reach the reader through model-p3.md's tables and arrow entries; "
                         "history.jsonl and the arrows' full sampled_against fields do not), "
                         "room notes, findings, the prior, the notes body (stage C2 section 6)",
    "build": "python3 out/_analysis/c2b_reviewer_sources.py --no-opening --no-questions --omit \"Theorised arrows;"
             "The model on the dimensions;Dynamics;Ungrounded relationships;Looked for and not found;The tiers the "
             "arrows run between;Where the model should break;The three strongest arrows;Two tests\" --write; then "
             "python3 tools/packets.py files --stage C2 --name C2-reviewer out/_analysis/c2b/0-instruction.md "
             "out/_analysis/c2b/model-p3-sections.md out/model/story-p3.md out/_analysis/c2b/criterion.md "
             "out/_analysis/c2b/tiers.md out/_analysis/c2b/verbs.md",
    "ids": "room names and concept ids as the model cites them; no second-order theme ids; no canvas field",
    "notes": "The return lands in out/_fleet_raw/C2/; the check leg (C2c) copies it into review-C2.md under the "
             "instruction and answers every item in notes-C2.md under rule 13.",
}
print(json.dumps(entry, indent=1, ensure_ascii=False))
if "--write" in sys.argv:
    man.append(entry)
    ascii_only = "\\u" in raw
    open(MP, "w", encoding="utf-8").write(json.dumps(man, indent=1, ensure_ascii=ascii_only))
    print("appended; run_manifest.json now holds %d entries" % len(man))
