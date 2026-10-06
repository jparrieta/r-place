#!/usr/bin/env bash
# harness_test_copy.sh REPO [STORE]: the Claude harness tests in the same copy as the runtime's, on a
# small store (the tools fixture's package plus an empty trees/, made at ~/tmp/smallstore when absent).
set -euo pipefail
R="${1:?repository root}"; S="${2:-$HOME/tmp/smallstore}"; W="$HOME/harness-test-copy/aggregator"
[ -d "$S/package" ] || { mkdir -p "$S/trees"; cp -a "$R/aggregator/instrument/tools/tests/fixture/package" "$S/"; }
mkdir -p "$W/instrument" "$W/handler/claude"; rsync -a --exclude _versions "$R/aggregator/instrument/" "$W/instrument/"; rsync -a "$R/aggregator/handler/claude/" "$W/handler/claude/"
cd "$W/handler/claude"; TMPDIR="$HOME/tmp" bash tests/run.sh "$S" 2>&1 | grep -v "^ok:" | tail -5
