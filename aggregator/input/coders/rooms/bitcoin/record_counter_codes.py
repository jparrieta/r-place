from emit import Emit

emit = Emit("out", corpus_path="coder_corpus.jsonl")
rows = [
    ({"item_id": "dfq5lse", "start": 54, "end": 115, "text": "The old script writes over the american flag so I stopped it."}, "stopping an old script after it overwrites the American flag"),
    ({"item_id": "dfqfu3o", "start": 313, "end": 384, "text": "keeps us others unaware of the fact that we may be fighting each other."}, "warning that hidden conflict may leave participants fighting each other"),
    ({"item_id": "dfqkc39", "start": 214, "end": 248, "text": "multiple proposals are infighting."}, "saying multiple proposals are infighting"),
    ({"item_id": "dfqv5kr", "start": 301, "end": 453, "text": "Currently we are probably fighting each other with different  designs and scripts. It is important to get consensus, or at least 51% of the pixel power."}, "asking for consensus because designs and scripts are probably fighting each other"),
]
code_ids = [emit.code(cited, label, thread_id="62sapp", note="counter-reading search") for cited, label in rows]
emit.theme_add("t10", code_ids)
print(code_ids)
