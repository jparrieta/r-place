#!/bin/bash
Y="$1"; F="$2"; shift 2
for s in "$@"; do
  T=$(mktemp -d)
  if python3 "$Y/$s/run/tools/tree_builder.py" --sub "$s" --codes-file "$F/rooms/$s/codes.jsonl" --record "$Y/$s/run/coder_corpus.jsonl" --out-dir "$T" > "$T/counts.json" 2> "$T/err.txt"; then
    cp "$T/package/forest.jsonl" "$F/rooms/$s/forest/forest.jsonl"
    cp "$T/package/tree_index.json" "$F/rooms/$s/forest/tree_index.json"
    cp "$T/trees/$s.md" "$F/rooms/$s/forest/$s.md"
    echo "$s ok"
  else
    echo "$s FAIL $(tail -1 "$T/err.txt")"
  fi
  rm -rf "$T"
done
