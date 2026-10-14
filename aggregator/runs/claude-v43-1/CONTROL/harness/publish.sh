#!/usr/bin/env bash
# publish.sh LABEL [KIND], for an analysis branch (legs.py branch). The branch is committed to its own Git branch,
# analysis/<run>, through Git plumbing: main, the shared checkout and the Manual are left alone. It replaces the
# run's publish.sh; BRANCH.json records the change (harness_changed).
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
RUN="$(cd "$HERE/../.." && pwd -P)"
PY="${RPLACE_BRANCHES_PY:-$HERE/../../../../handler/claude-adapter/branches.py}"
python3 "$PY" publish "$(basename "$RUN")" "$1" "${2:-close}" || true
exit 0
