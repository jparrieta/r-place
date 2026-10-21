# RETURN-D2v. What a verdict reader returns.

You read one community's second-order themes against a global model of how communities organized
during the event. Return one line of JSON, then the end marker on its own line, and nothing else.

`verdict` is one of `composes`, `composes-with-residue`, `does-not-compose`, `cannot-tell`, by the
criterion in your packet. `themes` lists the room's theme ids your verdict rests on, and
`concepts` the unused concept ids it rests on (an empty list when none). `residue` lists the
themes or concepts carrying organizing the model lacks, and is null unless the verdict is
`composes-with-residue`. `cannot_tell_under` is `coded-share`, `off-platform`, `both`,
`missing-decisive-evidence`, `conflicting-evidence` or `other-evidence-limit` when the
verdict is `cannot-tell`, and null otherwise. Thresholds are prompts for evidence review, not sufficient
conditions for cannot-tell. Explain the decisive missing or conflicting evidence in `sentence`. `sentence` is one sentence in the criterion's
terms. `served` is the digest printed at the end of your packet, copied exactly.

```
{"sub": "<room>", "reader": "<your reader id, or r1>", "verdict": "composes", "themes": ["t03", "t07"], "concepts": ["c0041"], "residue": null, "cannot_tell_under": null, "sentence": "The room restates in the model's terms and its unused concepts show nothing the model lacks.", "served": "<the digest>"}
END-OF-VERDICT
```
