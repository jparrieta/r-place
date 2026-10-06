#!/usr/bin/env python3
"""Rewrite the <!-- INDEX --> block at the top of a Markdown file with section line ranges.
Usage: python3 index_md.py FILE [FILE ...]. Idempotent; run at every edit of the file."""
import re, sys
for path in sys.argv[1:]:
    lines = open(path).read().split('\n')
    a = lines.index('<!-- INDEX -->'); b = lines.index('<!-- /INDEX -->')
    body = lines[:a+1] + lines[b:]          # file with an empty index block
    # compute headers on the file as it will be after the index is inserted
    def build(index_len):
        out = body[:a+1] + ['(index)'] * index_len + body[a+1:]
        heads = [(i+1, l) for i, l in enumerate(out) if re.match(r'^#{2,3} ', l)]
        rows = []
        for k, (ln, l) in enumerate(heads):
            end = heads[k+1][0]-1 if k+1 < len(heads) else len(out)
            words = sum(len(x.split()) for x in out[ln-1:end])
            title = re.sub(r'^#+ ', '', l)
            indent = '  ' if l.startswith('### ') else ''
            rows.append(f'{indent}{title}: lines {ln} to {end}, {words} words')
        return rows
    rows = build(0)
    for _ in range(3):
        rows = build(len(rows) + 2)
    index = ['| section | lines | words |', '|---|---|---|'] + [
        '| ' + r.rsplit(': lines ', 1)[0] + ' | ' + r.rsplit(': lines ', 1)[1].split(',')[0] + ' | ' + r.rsplit(', ', 1)[1].replace(' words','') + ' |' for r in rows]
    if len(index) != len(rows) + 2: raise SystemExit('index size drift')
    new = body[:a+1] + index + body[a+1:]
    open(path, 'w').write('\n'.join(new) + '\n')
    print(path, len(new), 'lines,', sum(len(x.split()) for x in new), 'words')
