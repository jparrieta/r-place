#!/usr/bin/env bash
# interview.sh [LEG | NN.LEG | --list]   Talk to the analyst at an interview point.
#   Opens a fork of the session of a closed leg (default: the last interview point closed) in a
#   folder of its own: the analyst's folder and sessions exactly as that leg's checkpoint stored
#   them, restored into interview-workspaces/<LABEL>__<fork>/ (J, 2026-09-29). The analyst may read,
#   and you may add files there and ask it to write; nothing reaches the live run, and no interview
#   reuses another's folder. The fork is recorded in CONTROL/interviews.tsv and is never a leg.
#   --list    the interview points closed so far, newest last.
#   To return to an interview later: the command it prints at the end (claude --resume <id>).
set -eu
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
RUN="$(harness_run_dir)"; C="$RUN/CONTROL"; AG="$RUN/00_GIVE-THE-AGENT"
POINTS="$(grep -h -E ' interview$' "$AG"/out/_closes/*.closed 2>/dev/null | wc -l | tr -d ' ')"
# closed interview points, one per line: NN.LEG <tab> LEG
list() { for f in "$AG"/out/_closes/*.closed; do
  [ -e "$f" ] || continue
  if [ "$(tail -1 "$f" | awk '{print $2}')" = interview ]; then b="$(basename "$f" .closed)"; printf '%s\t%s\n' "${b%%-*}.${b#*-}" "${b#*-}"; fi
done; }
if [ "${1:-}" = "--list" ]; then list; exit 0; fi
ARG="${1:-$(list | tail -1 | cut -f1)}"
[ -n "$ARG" ] || { echo "no interview point has closed yet (${POINTS} found)" >&2; exit 1; }
case "$ARG" in *.*) LABEL="$ARG";; *) LABEL="$(list | awk -F'\t' -v l="$ARG" '$2==l{print $1}' | tail -1)";; esac
[ -n "$LABEL" ] || { echo "$ARG is not a closed interview point (interview.sh --list shows them)" >&2; exit 1; }
[ -f "$C/snapshots/$LABEL/COMMITTED" ] || { echo "$LABEL has no committed checkpoint: run close.sh for it first" >&2; exit 1; }
SID="$(session_of "$RUN" "$LABEL")"; [ -n "$SID" ] || { echo "no session recorded for $LABEL" >&2; exit 1; }
MODEL="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))[sys.argv[2].split('.')[0]]['analyst'])" "$C/arm.json" "$LABEL")"
FORK="$(python3 -c 'import uuid;print(uuid.uuid4())')"
LEG="${LABEL#*.}"
BRIEF=""; for b in "$AG"/out/interview/"$LEG"_*.md; do case "$b" in *-reply.md) ;; *) [ -f "$b" ] && BRIEF="$b";; esac; done   # the last brief, by name
WS="$(python3 "$C/harness/protocol_guard.py" interview "$RUN" "$LABEL" "$FORK")" || exit 1
printf '%s\t%s\t%s\t%s\n' "$(NOW)" "$LABEL" "$SID" "$FORK" >> "$C/interviews.tsv"
echo "Interview at $LABEL (fork $FORK), in its own copy of the folder as the leg closed: $WS"
echo "Add anything for the analyst to that folder; the live run is not touched."
if [ -n "$BRIEF" ]; then echo "The analyst's brief: $BRIEF"; else echo "No brief found for $LABEL."; fi
[ -n "$BRIEF" ] && echo "To leave the analyst a reply it reads at its next leg: write ${BRIEF%.md}-reply.md"
python3 "$C/harness/protocol_guard.py" trust "$RUN" "$WS" || true   # v43: no trust dialog in the copy either
cd "$WS"
CLAUDE_CONFIG_DIR="$C/.cc" CLAUDE_CODE_PROJECT_DIR_NAME="iv-$FORK" CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 \
  claude --resume "$SID" --fork-session --session-id "$FORK" --model "$MODEL" --strict-mcp-config --permission-mode dontAsk \
  "This is an interview, not a leg. The principal investigator wants to talk with you about the work so far. You are in a copy of your folder exactly as it stood when this leg closed; the run goes on elsewhere, and nothing you do here reaches it. Answer from what you did and read; read files through the verbs; write only what the principal investigator asks for."
# archive the interview's transcript beside the run (.gitignore keeps it out of git unless the PI commits it), commit the record, refresh the Manual
IT="$(ls "$C"/.cc/projects/iv-"$FORK"/"$FORK".jsonl 2>/dev/null | head -1 || true)"
if [ -n "$IT" ]; then mkdir -p "$RUN/interviews"; cp "$IT" "$RUN/interviews/${LABEL}__${FORK}.jsonl"; fi
bash "$C/harness/publish.sh" "$LABEL" interview || true
echo "To return to this interview: cd \"$WS\" && CLAUDE_CONFIG_DIR=\"$C/.cc\" CLAUDE_CODE_PROJECT_DIR_NAME=iv-$FORK claude --resume $FORK"
