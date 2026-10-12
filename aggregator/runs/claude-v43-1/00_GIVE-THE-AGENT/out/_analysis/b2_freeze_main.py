#!/usr/bin/env python3
"""B2c: apply J's QB2-014 ruling (15:06 Berlin): the frozen scheme's main tier is "main". The 'common' files written
at B2b-r3-p3 move, unchanged, to out/_analysis/scheme_final_common.jsonl and scheme_final_common.md; scheme_final.jsonl
is written again with tier "main" where it said "common" and nothing else changed (checked field by field), and
scheme_final.md gets the new tier sentence and sha256. Refuses if the superseded copies exist. Dry run unless --write."""
import hashlib, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")

OLD_T = ("In scheme_final.jsonl the rare tier is marked \"tier\": \"rare\" and the main tier \"tier\": \"common\" "
         "(QB2-014).")
NEW_T = ("In scheme_final.jsonl the rare tier is marked \"tier\": \"rare\" and the main tier \"tier\": \"main\" (J, "
         "QB2-014, 15:06 Berlin: the word of B1's scheme.jsonl and of C1). It supersedes the file of the freeze, which "
         "wrote \"common\" and is kept as out/_analysis/scheme_final_common.jsonl; nothing else changed.")


def main():
    jp, mp = os.path.join(OUT, "scheme_final.jsonl"), os.path.join(OUT, "scheme_final.md")
    cj, cm = os.path.join(AN, "scheme_final_common.jsonl"), os.path.join(AN, "scheme_final_common.md")
    if os.path.exists(cj) or os.path.exists(cm):
        sys.exit("the superseded copies exist; the ruling was applied already")
    old = [json.loads(x) for x in open(jp, encoding="utf-8") if x.strip()]
    new = [dict(r, tier="main" if r["tier"] == "common" else r["tier"]) for r in old]
    for a, b in zip(old, new):
        diff = [k for k in set(a) | set(b) if a.get(k) != b.get(k)]
        if diff not in ([], ["tier"]):
            sys.exit("%s would change %s" % (a["id"], diff))
    body = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in new)
    sha_old = hashlib.sha256(open(jp, "rb").read()).hexdigest()
    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    md = open(mp, encoding="utf-8").read()
    if md.count(OLD_T) != 1 or md.count(sha_old) != 1:
        sys.exit("scheme_final.md does not hold the tier sentence and the old sha256 once")
    md2 = md.replace(OLD_T, NEW_T).replace(sha_old, sha)
    tiers = {}
    for r in new:
        tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1
    print("tiers %s; sha256 %s (was %s)" % (tiers, sha, sha_old))
    if "--write" not in sys.argv:
        return
    shutil.move(jp, cj)
    shutil.move(mp, cm)
    open(jp, "w", encoding="utf-8").write(body)
    open(mp, "w", encoding="utf-8").write(md2)
    print("written; the common files kept in out/_analysis/")


if __name__ == "__main__":
    main()
