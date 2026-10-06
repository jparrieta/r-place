#!/usr/bin/env bash
# gitscope.sh REPO: what the first commit would hold under the repository's own .gitignore,
# without creating .git in REPO (a bare probe repository in TMPDIR). Prints the file count, the size
# by top folder, files over 50 MB, and any name that looks like residue or a credential store.
set -euo pipefail
R="$(cd "${1:?repository root}" && pwd -P)"; P="${TMPDIR:-/tmp}/gitscope.$$.git"
git init -q --bare "$P"
git --git-dir="$P" --work-tree="$R" ls-files -o --exclude-standard -z > "$P.list"
python3 - "$R" "$P.list" <<'PY'
import os, sys, collections, re
R, L = sys.argv[1], sys.argv[2]
fs = [f for f in open(L, "rb").read().decode().split("\0") if f]
by, n, big = collections.Counter(), collections.Counter(), []
for f in fs:
    s = os.path.getsize(os.path.join(R, f)); k = "/".join(f.split("/")[:2]); by[k] += s; n[k] += 1
    if s > 50e6: big.append((s, f))
print("files %d, %.2f GB" % (len(fs), sum(by.values()) / 1e9))
for k, v in sorted(by.items()): print("%9.1f MB %6d  %s" % (v / 1e6, n[k], k))
print("over 50 MB:", len(big))
pat = re.compile(r"to_delete|_versions|superseded|aborted|backup|\.bak$|/\.cc/|auth\.json|\.env$|settings\.json$|guard\.log|\.compact-gate|__pycache__")
sus = [f for f in fs if pat.search(f)]
print("names to look at:", len(sus)); [print("  " + f) for f in sus[:40]]
PY
