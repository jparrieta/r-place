#!/usr/bin/env bash
# publish.sh LABEL [KIND]   Handler only; close.sh and interview.sh call it. Regenerates the Manual,
#   then, if the run sits in a git repository, commits everything and pushes. KIND is close,
#   interview, pause or finished; a close at an interview point or a finished stage is also tagged.
#   A push that fails (no network, no remote) is reported and never fails the close: the commit is
#   local and goes up with the next push.
#   The repository's .gitignore decides what is committed; the run's login (CONTROL/.cc) never is.
set -u
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
RUN="$(harness_run_dir)"; C="$RUN/CONTROL"
LABEL="${1:?label}"; KIND="${2:-close}"
python3 "$C/harness/gen_manual.py" "$RUN" || echo "  manual: not regenerated (see above)" >&2
TOP="$(cd "$RUN" && git rev-parse --show-toplevel 2>/dev/null || true)"
[ -n "$TOP" ] || { echo "  git: the run is not in a repository; nothing committed"; exit 0; }
cd "$TOP" || { echo "  git: cannot enter $TOP; nothing committed" >&2; exit 0; }
if ! ADDOUT="$(git add -A 2>&1)"; then   # v43.2: a failed add (a stale index.lock, say) is reported, never hidden
  echo "  git: add failed, nothing committed: $(printf '%s\n' "$ADDOUT" | tail -1)" >&2
  echo "  git: the checkpoint stands; mend the repository, then: bash \"$C/harness/publish.sh\" $LABEL $KIND" >&2
  exit 0
fi
if git diff --cached --quiet; then echo "  git: nothing new to commit"; else
  git commit -q -m "$KIND $LABEL" -m "$(date -u +%Y-%m-%dT%H:%M:%SZ)" && echo "  git: committed \"$KIND $LABEL\""
fi
LEG="${LABEL#*.}"; ST="${LABEL%%.*}"
# tags carry the run's folder name, so two runs in one repository never share a tag (restructure
# 2026-10-02): claude-v43-1/A1 for a finished stage, claude-v43-1/B3a for an interview point
RN="$(basename "$RUN")"
case "$KIND" in
  interview-point) git tag -f "$RN/$LEG" >/dev/null 2>&1 && echo "  git: tagged $RN/$LEG";;
  finished) git tag -f "$RN/$ST" >/dev/null 2>&1 && echo "  git: tagged $RN/$ST";;
esac
if git remote | grep -q .; then
  if git push -q --follow-tags 2>/dev/null && git push -q --tags -f 2>/dev/null; then echo "  git: pushed"
  else echo "  git: push failed; the commit is local and goes up with the next push" >&2; fi
else
  echo "  git: no remote set; committed locally"
fi
exit 0
