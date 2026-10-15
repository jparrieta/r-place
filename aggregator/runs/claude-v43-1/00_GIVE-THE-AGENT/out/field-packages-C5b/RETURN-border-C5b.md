# RETURN-border-C5b: the return format for the second coding of border talk

Target length: about 150 words. One JSON object per record, in any order, then the end marker on a line of its own.

- `record`: the citation, copied exactly (`sub/cNNNN`);
- `code`: exactly one of `T`, `D`, `O`;
- `why`: one clause, naming the words that decide the code;
- `doubtful`: `true` or `false`; where `true`, `why` says what the other code would rest on.

```json
{"record": "sub/c0001", "code": "T", "why": "...", "doubtful": false}
END-OF-BORDER-RETURN
```

Your codes decide nothing alone. After your 40 lines, write the end marker `END-OF-BORDER-RETURN` on a line of its own. Confirm that you reached the end of the records by writing that marker; a return without it is partial.
