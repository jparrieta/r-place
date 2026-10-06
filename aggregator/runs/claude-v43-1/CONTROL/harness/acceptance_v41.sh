#!/usr/bin/env bash
# acceptance_v41.sh: the Claude platform's live checks added in v41. Run once, in a Terminal, after
# acceptance.sh, before stage A1. Throwaway conversations only; nothing is deleted: everything the test
# makes is kept, with a README, in Jail/_to_delete/<repository>/aggregator/runs/<run>/acceptance-v41-<stamp>/ (since
# 2026-10-06, J: nothing set aside stays in the repository; lib.sh, set_aside_dir), with the guard log its sessions
# write, if there was none before.
#   A. Platform reading: in the analyst's folder, the analyst reads CLAUDE.md, AGENT.md and
#      PLATFORM-claude.md and states the models, routes, pause and continuation rules and who the D2
#      labelers are; the answers are checked against arm.claude.json; PLATFORM-codex.md must be absent.
#   B. Interview restore: a conversation and a folder are archived, restored into a separate folder and a
#      Claude project of its own, and resumed there as a fork; it must recall the conversation and read the
#      restored file, and the parent's transcript, folder and archive must keep their hashes. This is the
#      mechanism interview.sh uses (protocol_guard.py interview), exercised on a throwaway session; it is
#      not interview.sh end to end, which needs a closed leg.
#   C. The compaction hook firing on a real compaction is not exercised here; it is reported untested.
set -uo pipefail
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
RUN="$D"; while [ ! -d "$RUN/00_GIVE-THE-AGENT" ] && [ "$RUN" != / ]; do RUN="$(dirname "$RUN")"; done
[ -d "$RUN/00_GIVE-THE-AGENT" ] || { echo "cannot locate the run root from $D" >&2; exit 1; }
AG="$RUN/00_GIVE-THE-AGENT"; CC="$RUN/CONTROL/.cc"; ARM="$RUN/CONTROL/arm.json"
. "$D/lib.sh"
KEEP="$(set_aside_dir "$RUN")/acceptance-v41-$(date -u +%Y%m%dT%H%M%SZ)-$$"; mkdir -p "$KEEP"
GUARDLOG="$AG/out/_closes/guard.log"; GUARDNEW=1; [ -e "$GUARDLOG" ] && GUARDNEW=0
pass=0; fail=0
ok(){ echo "  PASS  $*"; pass=$((pass+1)); }
no(){ echo "  FAIL  $*"; fail=$((fail+1)); }
j(){ python3 -c "import json,sys;a=json.load(open(sys.argv[1]));print(eval(sys.argv[2]))" "$ARM" "$1"; }
uu(){ python3 -c 'import uuid;print(uuid.uuid4())'; }
MODEL="$(j "a['A1']['analyst']")"
python3 "$RUN/CONTROL/harness/protocol_guard.py" settings "$RUN" A1
BEFORE="$(ls "$AG/out" 2>/dev/null)"

echo; echo "=== A. does the analyst read its own platform file correctly? ==="
[ "$(cat "$RUN/CONTROL/PLATFORM" 2>/dev/null)" = claude ] && ok "the run is marked claude" || no "CONTROL/PLATFORM does not say claude"
[ -f "$AG/PLATFORM-claude.md" ] && ok "PLATFORM-claude.md delivered" || no "PLATFORM-claude.md missing"
[ ! -e "$AG/PLATFORM-codex.md" ] && [ ! -e "$AG/AGENTS.md" ] && ok "no Codex platform file delivered" || no "a Codex file is in the analyst's folder"
A="$(cd "$AG" && CLAUDE_CONFIG_DIR="$CC" CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude --model "$MODEL" --strict-mcp-config \
  --permission-mode dontAsk --allowedTools Read Bash Glob -p \
'This is a test of your instructions, not a stage. Read CLAUDE.md, AGENT.md and the platform file CLAUDE.md names. Run: ls PLATFORM-codex.md. Do not read or write anything else. Then output one JSON object on one line, nothing else, with these keys:
"platform" (claude or codex), "a1_model", "a1_effort", "b1_effort", "b2_reader_model", "b2_reader_route", "b2_readers", "c2_reviewer_model", "c2_reviewer_route", "how_a_leg_continues" (one sentence), "how_to_pause" (one sentence), "d2_labelers" (one sentence), "codex_platform_file_present" (true or false).' 2>&1)"
printf '%s\n' "$A" > "$KEEP/A-answer.txt"
python3 - "$ARM" "$KEEP/A-answer.txt" > "$KEEP/A-check.txt" <<'PY'
import json, re, sys
arm = json.load(open(sys.argv[1])); txt = open(sys.argv[2]).read()
m = re.findall(r"\{.*\}", txt, re.S)
try: a = json.loads(m[-1])
except Exception: print("FAIL no JSON answer"); sys.exit(0)
def low(x): return str(x).lower()
c = [
 ("platform is claude", low(a.get("platform")) == "claude"),
 ("A1 model", low(a.get("a1_model")) == arm["A1"]["analyst"]),
 ("A1 effort", low(a.get("a1_effort")) == arm["A1"]["effort"]),
 ("B1 effort", low(a.get("b1_effort")) == arm["B1"]["effort"]),
 ("B2 reader model", low(a.get("b2_reader_model")) == arm["B2"]["readers"]["model"]),
 ("B2 reader route", arm["B2"]["readers"]["route"] in low(a.get("b2_reader_route")) or "openrouter" in low(a.get("b2_reader_route"))),
 ("B2 readers", str(a.get("b2_readers")) == str(arm["B2"]["readers"]["n"])),
 ("C2 reviewer model", low(a.get("c2_reviewer_model")) == arm["C2"]["readers"]["model"]),
 ("C2 reviewer route", "cli" in low(a.get("c2_reviewer_route")) or "subscription" in low(a.get("c2_reviewer_route"))),
 ("continuation", any(w in low(a.get("how_a_leg_continues")) for w in ("fork", "continu")) and "close" in low(a.get("how_a_leg_continues"))),
 ("pause", "pause" in low(a.get("how_to_pause"))),
 ("D2 labelers resume Codex case leads", "codex" in low(a.get("d2_labelers")) and any(w in low(a.get("d2_labelers")) for w in ("case lead", "case-lead", "lead"))),
 ("no Codex file seen", a.get("codex_platform_file_present") in (False, "false")),
]
for name, good in c: print(("PASS " if good else "FAIL ") + name)
PY
while read -r st name; do [ "$st" = PASS ] && ok "reads: ${name}" || no "reads: ${name}"; done < <(sed 's/^\(PASS\|FAIL\) /\1 /' "$KEEP/A-check.txt")
for p in "$AG/out"/*; do [ -e "$p" ] || continue; f="$(basename "$p")"; printf '%s\n' "$BEFORE" | grep -qx "$f" || mv "$p" "$KEEP/out-$f"; done

echo; echo "=== B. does an archive restored into its own folder resume the conversation? ==="
W="$KEEP/parent"; mkdir -p "$W"; CW="CW$(uu | cut -c1-8)"; FS="FS$(uu | cut -c1-8)"
printf '%s\n' "$FS" > "$W/note.txt"
P="$(uu)"; K="$(uu)"; PP="v41parent-$(basename "$KEEP")"; IP="v41iv-$(basename "$KEEP")"
(cd "$W" && CLAUDE_CONFIG_DIR="$CC" CLAUDE_CODE_PROJECT_DIR_NAME="$PP" claude --session-id "$P" --model "$MODEL" --strict-mcp-config \
   -p "Remember this codeword: $CW. Do not use any tool. Reply with just OK." >/dev/null 2>&1)
PT="$CC/projects/$PP/$P.jsonl"
if [ -f "$PT" ]; then ok "the parent's transcript is where the project name puts it"; else no "no parent transcript at projects/$PP (CLAUDE_CODE_PROJECT_DIR_NAME not honoured?)"; PT="$(find "$CC/projects" -name "$P.jsonl" | head -1)"; fi
mkdir -p "$KEEP/checkpoint"; tar -czf "$KEEP/checkpoint/fs.tar.gz" -C "$W" . ; cp "$PT" "$KEEP/checkpoint/$P.jsonl" 2>/dev/null
h(){ shasum -a 256 "$@" 2>/dev/null | cut -d' ' -f1; }
H_PT="$(h "$PT")"; H_ARC="$(h "$KEEP/checkpoint/fs.tar.gz")"; H_W="$(cd "$W" && find . -type f | sort | xargs shasum -a 256 | shasum -a 256)"
IV="$KEEP/interview/workspace"; mkdir -p "$IV" "$CC/projects/$IP"
tar -xzf "$KEEP/checkpoint/fs.tar.gz" -C "$IV"; cp "$KEEP/checkpoint/$P.jsonl" "$CC/projects/$IP/$P.jsonl"
R="$(cd "$IV" && CLAUDE_CONFIG_DIR="$CC" CLAUDE_CODE_PROJECT_DIR_NAME="$IP" claude --resume "$P" --fork-session --session-id "$K" \
   --model "$MODEL" --strict-mcp-config --permission-mode dontAsk --allowedTools Bash Read \
   -p "Two things. First, what codeword did I ask you to remember? Second, read the file note.txt in your current folder. Reply on one line: CODEWORD=<word> FILE=<content of note.txt>" 2>&1)"
printf '%s\n' "$R" > "$KEEP/B-answer.txt"
printf '%s' "$R" | grep -q "$CW" && ok "the restored fork recalls the conversation" || no "the restored fork did not recall the codeword"
printf '%s' "$R" | grep -q "$FS" && ok "the restored fork reads the restored folder" || no "the restored fork did not read note.txt"
[ -f "$CC/projects/$IP/$K.jsonl" ] && grep -q "$CW" "$CC/projects/$IP/$K.jsonl" && ok "the fork's transcript sits in the interview's own project" || no "no fork transcript in projects/$IP"
[ "$H_PT" = "$(h "$PT")" ] && ok "the parent transcript is byte-identical" || no "the parent transcript changed"
[ "$H_ARC" = "$(h "$KEEP/checkpoint/fs.tar.gz")" ] && ok "the archive is byte-identical" || no "the archive changed"
[ "$H_W" = "$(cd "$W" && find . -type f | sort | xargs shasum -a 256 | shasum -a 256)" ] && ok "the parent folder is unchanged" || no "the parent folder changed"
for p in "$PP" "$IP"; do [ -d "$CC/projects/$p" ] && mv "$CC/projects/$p" "$KEEP/project-$p"; done
[ "$GUARDNEW" -eq 1 ] && [ -e "$GUARDLOG" ] && mv "$GUARDLOG" "$KEEP/guard.log"

echo; echo "=== C. not exercised ==="
echo "    The compaction hook firing on a real compaction: untested (acceptance.sh checks its output size only)."

printf 'acceptance_v41.sh on %s, %s: %s passed, %s failed.\nA-*: the platform-reading answer and its check. parent/, checkpoint/, interview/, project-*: the restore test and its transcripts. Kept for checking; the principal investigator may purge this folder.\n' "$RUN" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$pass" "$fail" > "$KEEP/README.txt"
echo; echo "================ RESULT:  $pass passed, $fail failed ================"
echo "    kept: $KEEP"
[ "$fail" -eq 0 ] && echo "v41 CLAUDE LIVE CHECKS CLEAR" || { echo "STOP -- see the FAIL lines"; exit 1; }
