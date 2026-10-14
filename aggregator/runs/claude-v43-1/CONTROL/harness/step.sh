#!/usr/bin/env bash
# step.sh, for an analysis branch (legs.py branch): refuses a leg before the branch's setup is published, while its
# publication is blocked, and its first leg outside legs.py (which tells the analyst it is a branch); then runs
# the parent's step.sh, kept unchanged beside it as step-parent.sh. BRANCH.json records the change.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
RUN="$(cd "$HERE/../.." && pwd -P)"
PY="${RPLACE_BRANCHES_PY:-$HERE/../../../../handler/claude-adapter/branches.py}"
python3 "$PY" check-step "$(basename "$RUN")" "$@" || exit 1
exec bash "$HERE/step-parent.sh" "$@"
