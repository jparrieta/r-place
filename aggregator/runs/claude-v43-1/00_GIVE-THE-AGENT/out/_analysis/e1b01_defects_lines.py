#!/usr/bin/env python3
"""E1b-01: the defects the quotes audit found, as defects.jsonl lines (appended by a stdout redirect, once).

    python3 out/_analysis/e1b01_defects_lines.py >> out/defects.jsonl

Each line names its file and line, and the audit-E1 output that shows it. Nothing earlier is changed (rule 18).
"""
import json

L = [
    {"where": "account-p1.md line 23",
     "what": "The instrument's: my English translation of a Finnish post is set in quotation marks beside the original (suomi/c0098, which resolves), with no word saying it is a translation. Found by audit-E1/quotes_resolve.py, read at E1b-01.",
     "sure": True},
    {"where": "dutch-telling-D6/greece.md line 36; form-telling-D6-r2/room-E-paladins.md line 26",
     "what": "The instrument's: two quotes in my D6 tellings are the coder's wording, given as members' words. greece: \"the heart was placed cooperatively later\" is the coder's English for a Greek post (greece/c0126, item dfrvs5t), with no original. paladins: \"April Fools' shenanigans\" is the coder's wording; the post says \"April Fools' Day, so expect shenanigans\" (paladins/c0001, item 62mzfo). Both were carried from case.md, against which my D6 quote check tested them, so the check passed them. Found by audit-E1/labels_read.py.",
     "sure": True},
    {"where": "notes-C1.md lines 144 and 453",
     "what": "The instrument's: two small misquotes of the instrument's own text. Line 144 quotes the stage as \"apply the amended rule, yourself, never a reader\"; STAGE-C1 says \"applying the amended rule, yourself, never a reader\". Line 453 quotes T3-086 as \"a rivalry from the community's own life\"; scheme_final.jsonl says \"A dispute or rivalry from the community's own life\". Found by audit-E1/quote_sources_check.py.",
     "sure": True},
    {"where": "_adjudication-B4/boundaries.md line 59; confusions.md line 47; coordinating-rule-A1.md line 32",
     "what": "The instrument's: three examples of my own wording set in quotation marks with no attribution, where a reader could take them for members' words (\"help us at 200, 300\", \"those were not our people\", \"defending the script as fun\"). No concept holds them. Found by audit-E1/unresolved_hand.py, read at E1b-01.",
     "sure": True},
    {"where": "notes-B2.md line 5 (and the head's paragraph on reading)",
     "what": "Provenance: J's standing instruction on reading (11 October, 16:54 Berlin) is quoted, but no transcript holds its words before my own Write at B2a-r1; the message that carried it is not in the analyst's reach. The wording cannot be checked against J's. Found by audit-E1/quote_sources_check.py.",
     "sure": False},
    {"where": "rooms/armenia/model-D.md line 51; rooms/zootopia/model-D.md line 7; rooms/straya/model-D-recheck.md line 35; rooms/asexuality/model-D.md line 33; rooms/smite/model-D.md line 11",
     "what": "The instrument's (the D2 and D3 readers): five paraphrases inside quotation marks in the readers' room models, against the concepts they paraphrase (armenia/c0083, zootopia/c0190, straya/c0047, asexuality/c0090, smite/c0243). Seven more reader quotes are in no concept of the room (GuildWars2, armenia, croatia, monsterhunter, portugal, tf2, wildhockey) and may come from uncoded items, which the forest drops. Found by audit-E1/unresolved_read.py and labels_read.py.",
     "sure": True},
    {"where": "package/<sub>/case.md (the coders' case accounts): albania, greece, paladins and others in quote-check-E1.json's sample",
     "what": "The material's: the coders' case accounts set translations in quotation marks (albania five times, beside the Albanian originals; greece with no original), quote their own theme labels and their counter-readings' phrases in quotation marks (85 labels and 6 phrases among the 389 listed strings), and once give a label's wording as a post's words (paladins). Found by audit-E1/case_missing_read.py.",
     "sure": True},
    {"where": "package/store/pointers.jsonl (the pointer normalised as \"r/pokemongo and r/3ds\"), shown in _views/relations.tsv",
     "what": "The material's: one pointer's normalised name holds two rooms, so r/3ds is no room of the mention graph. Found by audit-E1/links_views.py.",
     "sure": True},
]
for x in L:
    print(json.dumps({"stage": "E1", "leg": "E1b-01", "where": x["where"], "what": x["what"], "sure": x["sure"]},
                     ensure_ascii=False))
