# RETURN-field-C5: the return format for the second reading of the declarations

Target length: about 300 words. One JSON object per line, in any order, then the end marker on a line of its own.

- **One line per numbered sentence,** each with:
  - `sentence`: the id, such as `T4-007.prose.3`;
  - `kind`: one of `claim in question` (it holds a word from the rule's lists), `description` (it says what members did), or `about the literature or the study`;
  - `stands`: `true` or `false`;
  - `rests_on`: what it stands on or fails for want of: the quote citations (`sub/cNNNN`), finding ids, `setting fact` or `count`; an empty list if nothing;
  - `why`: one sentence. Where it does not stand, say which part of the rule it fails, or what the quotes show instead.
- **One line per record** in `11-stigmergy-records.md`: `record` (the citation, copied exactly) and `code` (exactly one of `M`, `MP`, `P`, `O`).
- **Any number of lines on a declaration as a whole:** `declaration` (its id) and `note`. Use these, for example, for a member theme whose drawn quotes the declaration does not describe.

```json
{"sentence": "T4-007.prose.3", "kind": "description", "stands": true, "rests_on": ["bindingofisaac/c0181"], "why": "..."}
{"record": "sub/c0001", "code": "M"}
{"declaration": "T4-007", "note": "..."}
END-OF-FIELD-RETURN
```

A disagreement is never a verdict: your reading decides nothing alone.

After your lines, write the end marker `END-OF-FIELD-RETURN` on a line of its own. Confirm that you reached the end of the packages by writing that marker; a return without it is partial.
