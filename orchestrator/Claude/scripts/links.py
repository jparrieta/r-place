import re, os, sys, urllib.parse
pat = re.compile(r'\]\(([^)\s]+)\)')
bad = {}
for f in sys.argv[1:]:
    try: t = open(f, encoding="utf-8").read()
    except Exception: continue
    for m in pat.finditer(t):
        u = m.group(1).split("#")[0]
        if not u or re.match(r'^[a-z]+:', u): continue
        p = os.path.normpath(os.path.join(os.path.dirname(f), urllib.parse.unquote(u)))
        if not os.path.exists(p): bad.setdefault(f, []).append(u)
for f, us in sorted(bad.items()): print(f, len(us), us[:4])
print("files with broken links:", len(bad), "links:", sum(len(v) for v in bad.values()))
