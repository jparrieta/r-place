import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from emit import Emit

E = Emit("out", corpus_path="coder_corpus.jsonl")

for theme_id, codes in [
    ("t20", ["c0421", "c0422", "c0423", "c0424", "c0427", "c0428", "c0429", "c0441", "c0442", "c0446", "c0447"]),
    ("t17", ["c0430"]),
    ("t16", ["c0440"]),
    ("t21", ["c0443"]),
    ("t06", ["c0444"]),
    ("t10", ["c0450", "c0451", "c0468", "c0469", "c0470", "c0471"]),
]:
    E.theme_add(theme_id, codes)

E.theme(
    "arguing over selling the room's shared work",
    "These codes conduct and contest poster sales made from the canvas: the seller invites orders and explains costs, critics object to profit from collective work, the criticism becomes copypasta, and practical sales-page faults are repaired.",
    ["c0425", "c0426", "c0431", "c0432", "c0433", "c0434", "c0435", "c0439", "c0445", "c0448", "c0449"],
)
E.theme(
    "answering poster-sale criticism with a giveaway",
    "These codes turn criticism of a paid poster into a proposed and announced giveaway, then negotiate whether free entry through the seller's website answers the objection; they vary from proposing the remedy to disputing its mechanics.",
    ["c0436", "c0437", "c0438", "c0459", "c0460", "c0461", "c0462", "c0463", "c0464", "c0465", "c0466", "c0467"],
)
E.theme(
    "welcoming someone who found the room through Place",
    "These codes form one arrival exchange: a newcomer follows the Yeezus canvas picture to r/kanye, makes a first post, and is welcomed through favourite-song answers, 'wavy dude' language, and an explanation of current room business.",
    ["c0452", "c0453", "c0454", "c0455", "c0456", "c0457", "c0458"],
)
