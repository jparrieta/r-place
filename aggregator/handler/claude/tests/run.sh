#!/usr/bin/env bash
# The harness test, with a stand-in for the claude CLI (tests/fake_claude.py): builds a run from
# this instrument over a small store and walks the paths every run takes: a refused close, a normal
# close with its snap and its probe (in a fork, the leg's transcript untouched), a forced close,
# the stage order, a fleet stage through packets-out, dispatch and check (B3), stage B2's round
# check, the D2 verdict packets, and the settings (denies, hooks, auto memory). Every check that
# does not pass is a FAIL and the script exits 1. It certifies the harness's logic, not the
# installed CLI; acceptance.sh does that on the Mac.
#   bash harness/tests/run.sh STORE_ROOT     (a folder holding package/ and trees/)
set -uo pipefail
H="$(cd "$(dirname "$0")/.." && pwd -P)"; I="$(cd "$H/../../instrument" && pwd -P)"; S="${1:?a folder holding package/ and trees/}"
export PATH="$H/tests/bin:$PATH"; unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_API_KEY
mkdir -p "$H/tests/bin"; ln -sf "$H/tests/fake_claude.py" "$H/tests/bin/claude"
T="$(mktemp -d)"; R="$T/run"; AG="$R/00_GIVE-THE-AGENT"; mkdir -p "$AG"
cp -r "$S/package" "$S/trees" "$AG/"
bash "$H/build.sh" "$R" >/dev/null 2>&1 || { echo "FAIL: build.sh"; exit 1; }
git init -q "$T" && git -C "$T" config user.email t@t && git -C "$T" config user.name t && git -C "$T" config gc.auto 0   # no background gc while verify.sh removes the folder
printf 'run/CONTROL/.cc/\n' > "$T/.gitignore"
cd "$R" || exit 1; P=0; F=0
t(){ if (set +o pipefail; eval "$2") >/dev/null 2>&1; then echo "ok:   $1"; P=$((P+1)); else echo "FAIL: $1"; F=$((F+1)); fi; }
TR(){ ls -t CONTROL/.cc/projects/run/*.jsonl 2>/dev/null | head -1; }

# 1. a close the analyst did not make is refused
bash CONTROL/harness/step.sh A1a >/dev/null 2>&1
o="$(bash CONTROL/harness/close.sh A1a 2>&1 || true)"
t "close refuses a leg the analyst did not close" '[[ "$o" == *analyst-did-not-close* ]]'
t "every launch turns auto memory off" 'python3 -c "import json,sys;sys.exit(0 if json.load(open(\"CONTROL/.cc/last_call.json\"))[\"auto_memory_off\"]==\"1\" else 1)"'
t "every launch runs in dontAsk: nothing asks (v43)" 'python3 -c "import json,sys;a=json.load(open(\"CONTROL/.cc/last_call.json\"))[\"argv\"];sys.exit(0 if a[a.index(\"--permission-mode\")+1]==\"dontAsk\" else 1)"'
# 2. a normal close: preclose passes on the analyst's own last turn, then the snap and a forked probe
SID="$(python3 -c "import json;print(json.load(open('CONTROL/sessions.json'))['A1.A1a']['session_id'])")"
LT="CONTROL/.cc/projects/run/$SID.jsonl"; N0="$(wc -l < "$LT")"
echo "x close" > "$AG/out/_closes/A1-A1a.closed"
o="$(bash CONTROL/harness/close.sh A1a 2>&1)"; rc=$?
t "a normal close sees the analyst's own last turn and the launcher's exit" 'python3 -c "import json,sys;d=json.load(open(\"CONTROL/close-status-A1.A1a.json\"));sys.exit(0 if d[\"completed_turn\"] and d[\"launcher_exited\"] else 1)"'
t "a normal close whose validation fails publishes no checkpoint" '[ $rc -ne 0 ] && [ ! -f CONTROL/snapshots/A1.A1a/COMMITTED ]'
t "the probe leaves the leg's transcript untouched" '[ "$(wc -l < "$LT")" = "$N0" ]'
# 3. order
o="$(bash CONTROL/harness/step.sh B1a 2>&1 || true)"
t "stage B2 refuses while B1 is unfinished" '[[ "$(bash CONTROL/harness/step.sh B2a-r1 2>&1 || true)" == *"not finished"* ]]'
# 4. a fleet stage: packets-out, dispatch, check
bash CONTROL/harness/step.sh B3a --force-order >/dev/null 2>&1
echo "x packets-out" > "$AG/out/_closes/B3-B3a.closed"
o="$(bash CONTROL/harness/close.sh B3a --force 2>&1 || true)"
t "a packets-out close names the dispatch" '[[ "$o" == *dispatch.sh* ]]'
t "the harness takes the snap at close" 'ls "$AG"/out/_snap/B3-*.sha256'
t "the probe runs in a fork of its own" '[ -s "$AG/out/_probe/B3-B3a.answers.md.session" ] && [ -f "CONTROL/.cc/projects/run/$(cat "$AG/out/_probe/B3-B3a.answers.md.session").jsonl" ]'
t "the check leg waits for DONE" '[[ "$(bash CONTROL/harness/step.sh B3b 2>&1 || true)" == *"has not finished"* ]]'
mkdir -p "$AG/out/_fleet_raw/B3"; echo '{}' > "$AG/out/_fleet_raw/B3/DONE"
bash CONTROL/harness/step.sh B3b >/dev/null 2>&1
t "the check leg is told the readers left their files" 'grep -q "readers left their files" CONTROL/next_prompt.txt'
t "an ordinary leg continues the last close's conversation (v40)" 'python3 -c "import json,sys;s=json.load(open(\"CONTROL/sessions.json\"));b=s.get(\"B3.B3b\",{});sys.exit(0 if b.get(\"mode\")==\"fork\" and b.get(\"parent_session\")==s[\"B3.B3a\"][\"session_id\"] else 1)"'
t "the continued leg is told it continues" 'grep -q "continues the last close" CONTROL/next_prompt.txt'
# 5. stage B2: the check leg names its round and reads that round's DONE
t "B2's check leg without a round is refused" '[[ "$(bash CONTROL/harness/step.sh B2b --force-order 2>&1 || true)" == *"is a round"* ]]'
mkdir -p "$AG/out/_fleet_raw/B2/round-1"
t "B2's B2b-r1 waits for round-1/DONE" '[[ "$(bash CONTROL/harness/step.sh B2b-r1 --force-order 2>&1 || true)" == *"has not finished"* ]]'
echo '{}' > "$AG/out/_fleet_raw/B2/round-1/DONE"
bash CONTROL/harness/step.sh B2b-r1 --force-order >/dev/null 2>&1
t "B2's B2b-r1 opens once round-1/DONE exists" 'grep -q "round-1" CONTROL/next_prompt.txt'
# 6. D2: the return specification is never a packet
V="$T/v"; mkdir -p "$V"; printf 'x\n' > "$V/denmark.md"; printf 'x\n' > "$V/sweden.md"; printf 'spec\n```\n{"sub":"x"}\nEND-OF-VERDICT\n```\n' > "$V/RETURN-D2v.md"
echo '{"denmark":{"items":1},"sweden":{"items":1}}' > "$V/MANIFEST.json"
o="$(python3 "$I/tools/fleet.py" D2 --packets "$V" --return "$V/RETURN-D2v.md" --raw "$T/rawD2v" --readers 1 --model x --shared "" --dry-run 2>&1 || true)"
t "D2: RETURN-D2v.md is not sent as a packet" '! printf "%s" "$o" | grep -q "RETURN-D2v:"'
# 7. the settings
t "_probe and _transcripts denied before stage E1" 'python3 -c "import json,sys;s=json.load(open(\"$AG/.claude/settings.json\"));d=s[\"permissions\"][\"deny\"];sys.exit(0 if any(\"_probe\" in x for x in d) and any(\"_transcripts\" in x for x in d) else 1)"'
t "INPUT denied to Bash" 'python3 -c "import json,sys;s=json.load(open(\"$AG/.claude/settings.json\"));sys.exit(0 if any(x.endswith(\"/INPUT\") for x in s[\"sandbox\"][\"filesystem\"][\"denyRead\"]) else 1)"'
# restructure 2026-10-02: a run in rplace/aggregator/runs/<run> has the shared input two levels up and
# coder/, data/, orchestrator/ three levels up; every one of them is shut
TN="$(mktemp -d)"; N="$TN/nest/rplace/aggregator/runs/r1"; mkdir -p "$N/CONTROL" "$N/00_GIVE-THE-AGENT" "$TN/nest/rplace/aggregator/runs/r2" \
  "$TN/nest/rplace/aggregator/input" "$TN/nest/rplace/aggregator/instrument" "$TN/nest/rplace/coder" "$TN/nest/rplace/orchestrator"
cp "$R/CONTROL/settings.template.json" "$N/CONTROL/"
python3 -c "import sys;sys.path.insert(0,sys.argv[1]);import protocol_guard as g;g.settings(sys.argv[2],'A1')" "$R/CONTROL/harness" "$N" >/dev/null 2>&1
t "the input, the other runs and the repository's other layers denied" 'python3 -c "import json,sys;d=json.load(open(\"$N/00_GIVE-THE-AGENT/.claude/settings.json\"))[\"sandbox\"][\"filesystem\"][\"denyRead\"];sys.exit(0 if all(any(x.endswith(e) for x in d) for e in (\"/aggregator/input\",\"/runs/r2\",\"/aggregator/instrument\",\"/rplace/coder\",\"/rplace/orchestrator\")) else 1)"'
t "tools/ and the instrument folders denied to writes" 'python3 -c "import json,sys;s=json.load(open(\"$AG/.claude/settings.json\"));w=s[\"sandbox\"][\"filesystem\"][\"denyWrite\"];sys.exit(0 if any(x.endswith(\"/tools\") for x in w) else 1)"'
t "the compaction hook and the tool guard run from CONTROL" 'grep -q "CONTROL/harness/after_compact.sh" "$AG/.claude/settings.json" && grep -q "CONTROL/harness/pretool_guard.py" "$AG/.claude/settings.json" && [ ! -e "$AG/tools/after_compact.sh" ]'
t "the compaction hook prints under 9,000 characters" '[ "$(bash CONTROL/harness/after_compact.sh | wc -c)" -lt 9000 ]'
mv CONTROL/.compact-gate.json CONTROL/.compact-gate.test.json 2>/dev/null
t "the tool guard blocks rm" '! (cd "$AG" && echo "{\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"rm out/x\"},\"cwd\":\"$AG\"}" | python3 "$R/CONTROL/harness/pretool_guard.py")'
t "the tool guard skips quoted text: rm inside a quotation is not a delete (J, 2026-10-06)" '(cd "$AG" && echo "{\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"echo '"'"'{\\\"why\\\": \\\"the troops rm the flag\\\"}'"'"' >> out/leads-A1.jsonl\"},\"cwd\":\"$AG\"}" | python3 "$R/CONTROL/harness/pretool_guard.py")'
t "the tool guard still reads a quoted command run by a shell (sh -c, eval)" '! (cd "$AG" && echo "{\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"bash -c \\\"rm out/x\\\"\"},\"cwd\":\"$AG\"}" | python3 "$R/CONTROL/harness/pretool_guard.py")'
t "the tool guard lets a verb through" '(cd "$AG" && echo "{\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"python3 tools/mem.py help\"},\"cwd\":\"$AG\"}" | python3 "$R/CONTROL/harness/pretool_guard.py")'
t "the tool guard keeps saturation.py decide for the PI" '! (cd "$AG" && echo "{\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"python3 tools/saturation.py decide --stage B1 stop --why x\"},\"cwd\":\"$AG\"}" | python3 "$R/CONTROL/harness/pretool_guard.py" 2>/dev/null)'
t "the tool guard refuses a column cut after mem.py (J, 2026-10-11)" '! (cd "$AG" && echo "{\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"python3 tools/mem.py theme a/t01 | cut -c1-100\"},\"cwd\":\"$AG\"}" | python3 "$R/CONTROL/harness/pretool_guard.py" 2>/dev/null)'
t "the tool guard refuses placement files in a blind window (J, 2026-10-11)" '(cd "$AG" && echo "{\"on\": true}" > out/_blind.json && ! (echo "{\"tool_name\":\"Read\",\"tool_input\":{\"file_path\":\"out/author_items.jsonl\"},\"cwd\":\"$AG\"}" | python3 "$R/CONTROL/harness/pretool_guard.py" 2>/dev/null); rc=$?; echo "{\"on\": false}" > out/_blind.json; exit $rc)'
t "the tool guard keeps out/_closes for the harness" '! (cd "$AG" && echo "{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"out/_closes/model-C5.sha256\"},\"cwd\":\"$AG\"}" | python3 "$R/CONTROL/harness/pretool_guard.py" 2>/dev/null)'
t "a malformed compaction gate never switches the guard off" '(cd "$AG" && echo "[]" > "$R/CONTROL/.compact-gate.json"; echo "{\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"rm out/x\"},\"cwd\":\"$AG\"}" | python3 "$R/CONTROL/harness/pretool_guard.py" 2>/dev/null; rc=$?; mv "$R/CONTROL/.compact-gate.json" "$T/gate-test-aside.json"; [ "$rc" -eq 2 ])'
t "counts.py runs on the store" '(cd "$AG" && python3 tools/counts.py . out)'
# 8. a pause at a safe stop, and the interview list, and stage D6
bash CONTROL/harness/pause.sh >/dev/null 2>&1
t "pause.sh leaves a pause request the analyst can see" '[ -f "$AG/.pause" ]'
bash CONTROL/harness/step.sh A1b-01 --force-order >/dev/null 2>&1
t "a new leg clears the pause request" '[ ! -f "$AG/.pause" ]'
(cd "$AG" && bash tools/done.sh A1 --pause >/dev/null 2>&1)
t "done.sh --pause refuses a leg with no pause line" '[ ! -f "$AG/out/_closes/A1-A1b-01.closed" ] || ! tail -1 "$AG/out/_closes/A1-A1b-01.closed" | grep -q " pause$"'
(cd "$AG" && python3 tools/mem.py log "reading the flags; next: sweden" --kind pause --stage A1 >/dev/null 2>&1 && bash tools/done.sh A1 --pause >/dev/null 2>&1)
t "done.sh --pause closes the leg without the stage's close-check" 'tail -1 "$AG/out/_closes/A1-A1b-01.closed" | grep -q " pause$"'
mkdir -p CONTROL/.cc/skills/synced && echo '{"oauthAccount":{"emailAddress":"x@y"}}' > CONTROL/.cc/.claude.json && echo s > CONTROL/.cc/skills/synced/s.md
o="$(bash CONTROL/harness/close.sh A1b-01 2>&1 || true)"
t "close.sh publishes a paused leg and says how to resume" '[[ "$o" == *"paused at a safe stop"* ]] && [ -f CONTROL/snapshots/A1.A1b-01/COMMITTED ] && grep -q paused CONTROL/stage-state/A1/PAUSES'
t "step.sh refuses a leg the analyst has closed" '[[ "$(bash CONTROL/harness/step.sh A1b-01 --force-order 2>&1 || true)" == *"REFUSING: leg A1b-01 is already closed"* ]]'
t "a close commits the run and writes the Manual" 'git -C "$T" log --oneline | grep -q "pause A1.A1b-01" && [ -f "$T/Manual/README.md" ] && grep -q "A1b-01" "$T/Manual/stages/A1.md"'
t "the Manual gives a command to talk with the leg" 'grep -q "claude --resume" "$T/Manual/stages/A1.md" && grep -q -- "--fork-session" "$T/Manual/stages/A1.md"'
t "a checkpoint keeps only the run's sessions of the Claude folder" 'tar -tzf CONTROL/snapshots/A1.A1b-01/agent.tar.gz | grep -q "^.cc/projects/run/.*\.jsonl$" && ! tar -tzf CONTROL/snapshots/A1.A1b-01/agent.tar.gz | grep -v -E "^\.cc/?$|^\.cc/projects/?$|^\.cc/projects/run(/|$)"'
t "the Manual's command cannot run commands or write" 'grep -q -- "--disallowedTools Bash Write Edit MultiEdit NotebookEdit" "$T/Manual/stages/A1.md"'
t "the login folder is never committed" '! git -C "$T" ls-files | grep -q "CONTROL/.cc/"'
t "the repository history is shut to the analyst" 'python3 -c "import json,sys;s=json.load(open(\"$AG/.claude/settings.json\"));sys.exit(0 if any(x.endswith(\"/.git\") for x in s[\"sandbox\"][\"filesystem\"][\"denyRead\"]) else 1)"'
t "transcripts are kept past 30 days" 'python3 -c "import json,sys;sys.exit(0 if json.load(open(\"CONTROL/.cc/settings.json\"))[\"cleanupPeriodDays\"]>=36500 else 1)"'
echo "x interview" >> "$AG/out/_closes/B3-B3a.closed"
t "interview.sh lists an interview point" 'bash CONTROL/harness/interview.sh --list | grep -q "B3.B3a"'
bash CONTROL/harness/step.sh C4a --force-order >/dev/null 2>&1
mkdir -p "$AG/out/_answers"; echo "Keep it." > "$AG/out/_answers/QA1-009.md"; sleep 1   # an answer while C4a is open, before its done.sh
(cd "$AG" && bash tools/done.sh C4 --cut interview >/dev/null 2>&1); rc=$?
t "an interview cut without its brief is refused" '[ "$rc" -ne 0 ] && [ ! -f "$AG/out/_closes/C4-C4a.closed" ]'
t "an interview cut on a step without one is refused" '! (cd "$AG" && printf "A1b-02\n" > .leg && bash tools/done.sh A1 --cut interview >/dev/null 2>&1); printf "C4a\n" > "$AG/.leg"'
mkdir -p "$AG/out/interview" "$AG/out/model" "$AG/out/fourth"; echo "brief" > "$AG/out/interview/C4a.md"; echo "# handback" > "$AG/out/handback-C4.md"
(cd "$AG" && touch out/dropped.jsonl out/model/arrows.jsonl out/model/history.jsonl out/fourth/fourth.jsonl && echo "# head" >> out/_head.md && echo "# notes-C4" > out/notes-C4.md && echo "The field was not held in this test." > out/field-C4.md)
(cd "$AG" && python3 tools/mem.py log "the field read" --stage C4 >/dev/null 2>&1; bash tools/done.sh C4 --cut interview >/dev/null 2>&1)
t "an interview brief is filed under leg, stage, step and minute" 'ls "$AG"/out/interview/ | grep -qE "^C4a_[a-z-]+_[a-z-]+_[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}\.md$"'
B="$(ls "$AG"/out/interview/C4a_*.md | head -1)"; sleep 1; echo "go on" > "${B%.md}-reply.md"
bash CONTROL/harness/step.sh A1b-02 --force-order >/dev/null 2>&1
t "the next leg is told to read the interview reply" 'grep -q "reply.md" CONTROL/next_prompt.txt'
t "an answer written before the last close is still named in the next leg (v43.2)" 'grep -q "QA1-009" CONTROL/next_prompt.txt && grep -q "^QA1-009	A1.A1b-02$" CONTROL/answers-named.tsv'
t "a leg id that does not parse is refused" '! bash CONTROL/harness/step.sh B1f --force-order >/dev/null 2>&1'
t "stage D6 is a stage" '(. CONTROL/harness/lib.sh; [ "$(norm_stage D6)" = D6 ]) && grep -q "^D6" DROPS/ORDER.tsv'
o="$(bash CONTROL/harness/step.sh E2a --force-order 2>&1 || true)"
t "stage E2 refuses without the proposal" '[[ "$o" == *"proposal.md"* ]] && [ ! -d "$AG/handling" ]'
echo "the proposal" > DROPS/E2/handling/proposal.md; [ -f DROPS/E2/handling/design-note.md ] || echo "note" > DROPS/E2/handling/design-note.md
bash CONTROL/harness/step.sh E2a --force-order >/dev/null 2>&1
t "an answer is named once, not again in a later leg (v43.2)" '! grep -q "QA1-009" CONTROL/next_prompt.txt'
t "E2 brings the proposal, the design note and the harness log" '[ -f "$AG/handling/proposal.md" ] && [ -f "$AG/handling/design-note.md" ] && [ -f "$AG/handling/harness-log/handover-events.log" ] && ls "$AG/handling/harness-log/first-messages/" | grep -q txt && grep -q "handling/ holds" CONTROL/next_prompt.txt'
t "the stage cards are written from the steps" 'ls "STAGE CARDS" | grep -q "Stage B1. Coding - third-order scheme.md" && grep -q "step.sh B1b-01" "STAGE CARDS/Stage B1. Coding - third-order scheme.md"'
bash CONTROL/harness/after_compact.sh >/dev/null 2>&1
gc(){ printf '{"cwd": "%s", "tool_name": "%s", "tool_input": %s}' "$AG" "$1" "$2" | python3 CONTROL/harness/pretool_guard.py >/dev/null 2>&1; }
t "after a compaction the guard refuses work until the head is read" '! gc Bash "{\"command\": \"ls\"}" && gc Read "{\"file_path\": \"out/_head.md\"}"'
t "a part of the stage file does not count as reading it" 'gc Read "{\"file_path\": \"$(cat "$AG/.stagefile")\", \"limit\": 1}" && gc Bash "{\"command\": \"python3 tools/mem.py diary --last 5\"}" && ! gc Bash "{\"command\": \"python3 tools/mem.py log done\"}" && [ -f CONTROL/.compact-gate.json ]'
t "the compaction gate lifts after the head, the stage file, the diary and a log line" 'gc Read "{\"file_path\": \"$(cat "$AG/.stagefile")\"}" && gc Bash "{\"command\": \"python3 tools/mem.py diary --last 5\"}" && gc Bash "{\"command\": \"python3 tools/mem.py log done\"}" && [ ! -f CONTROL/.compact-gate.json ] && gc Bash "{\"command\": \"ls\"}"'
# 9. the stage file is the one DROPS/ORDER.tsv names, whatever else sits beside it (review 2026-09-29)
SF="$(cat "$AG/.stagefile")"; STALE="$AG/stages/$(basename "$SF" | sed -E 's/^(STAGE-[A-E][1-6]-).*/\1aaa-stale.md/')"
echo "stale" > "$STALE"
t "the compaction hook names the stage file step.sh chose, not a stale neighbour" 'bash CONTROL/harness/after_compact.sh | grep -qF "$SF"'
t "validate.py opens the stage file step.sh chose" '(cd "$AG" && python3 tools/validate.py --open "$(cat .stage)" 2>&1 | grep -v aaa-stale >/dev/null) && ! (cd "$AG" && python3 tools/validate.py --open "$(cat .stage)" 2>&1 | grep -q "aaa-stale")'
mv "$STALE" "$T/"; mv CONTROL/.compact-gate.json "$T/gate-test-aside-2.json" 2>/dev/null
# 10. an interview has a folder of its own: the checkpoint restored, the live folder shut (J, 2026-09-29)
if [ -f CONTROL/snapshots/B3.B3a/COMMITTED ] && [ -f CONTROL/snapshots/B3.B3a/agent.tar.gz ]; then
  W="$(python3 CONTROL/harness/protocol_guard.py interview "$R" B3.B3a testfork 2>&1)"
  t "an interview restores the leg's folder as the checkpoint stored it, not the live one" '[ -f "$W/out/_closes/B3-B3a.closed" ] && [ -f "$AG/out/_closes/C4-C4a.closed" ] && [ ! -f "$W/out/_closes/C4-C4a.closed" ]'
  t "an interview's settings shut the live folder and carry no hooks" 'python3 -c "import json,sys;s=json.load(open(\"$W/.claude/settings.json\"));d=s[\"sandbox\"][\"filesystem\"][\"denyRead\"];sys.exit(0 if any(x.endswith(\"/00_GIVE-THE-AGENT\") and \"interview-workspaces\" not in x for x in d) and \"hooks\" not in s else 1)"'
  t "an interview's session is the checkpoint's, in a project of its own" 'ls CONTROL/.cc/projects/iv-testfork/*.jsonl'
  t "a second interview with the same fork id is refused" '! python3 CONTROL/harness/protocol_guard.py interview "$R" B3.B3a testfork'
else
  t "an interview can be restored (B3.B3a checkpoint present)" 'false'
fi
# 11. the trusted validator holds every module its checks import (audit 2026-09-29c)
t "the trusted validator can import everything its checks import" 'python3 - "$R/CONTROL/harness/validation_tools" "$I/tools" <<"PYI"
import glob, os, re, sys
vt, src = sys.argv[1], sys.argv[2]
tools = {os.path.splitext(os.path.basename(p))[0] for p in glob.glob(src + "/*.py")}
have = {os.path.splitext(os.path.basename(p))[0] for p in glob.glob(vt + "/*.py")}
miss = set()
for f in glob.glob(vt + "/*.py") + glob.glob(vt + "/checks/*.py"):
    for m in re.finditer(r"^\s*(?:from\s+(\w+)[\w.]*\s+import|import\s+([\w., ]+))", open(f).read(), re.M):
        for nm in ([m.group(1)] if m.group(1) else [x.strip().split(" ")[0].split(".")[0] for x in m.group(2).split(",")]):
            if nm in tools and nm not in have:
                miss.add(nm)
print(sorted(miss)); sys.exit(1 if miss else 0)
PYI'
# v41: one instrument, two platforms
t "the build stamps the run v43 (v43)" 'python3 -c "import json,sys;sys.exit(0 if json.load(open(\"CONTROL/RUN.json\"))[\"instrument_version\"]==\"v43\" else 1)"'
# v43: nothing asks. The leg runs in dontAsk, its writes in out/ and its CLI scratchpad allowed by rule, and the
# run's login trusts the repository, the run and the folder
t "a leg's settings are dontAsk with writes allowed in out/ (v43)" 'python3 -c "import json,sys;s=json.load(open(\"$AG/.claude/settings.json\"))[\"permissions\"];sys.exit(0 if s[\"defaultMode\"]==\"dontAsk\" and any(x.startswith(\"Edit(/\") and x.endswith(\"/out/**)\") for x in s[\"allow\"]) and \"Agent\" in s[\"allow\"] else 1)"'
t "the CLI scratchpad of this folder is a working directory, writable by rule (v43)" 'python3 -c "import json,sys;s=json.load(open(\"$AG/.claude/settings.json\"))[\"permissions\"];d=[x for x in s[\"additionalDirectories\"] if \"/claude-\" in x];sys.exit(0 if len(d)==2 and all(any(r==\"Edit(/\"+x+\"/**)\" for r in s[\"allow\"]) for x in d) else 1)"'
printf '{"keep": 1, "projects": {"elsewhere": {"hasTrustDialogAccepted": false}}}' > CONTROL/.cc/.claude.json
python3 CONTROL/harness/protocol_guard.py trust "$R" >/dev/null 2>&1
t "the run's login trusts the repository, the run and the folder, and keeps its other keys (v43)" 'python3 -c "import json,sys,os;d=json.load(open(\"CONTROL/.cc/.claude.json\"));p=d[\"projects\"];r=os.path.realpath(\"$R\");sys.exit(0 if d[\"keep\"]==1 and p[\"elsewhere\"][\"hasTrustDialogAccepted\"] is False and all(p[k][\"hasTrustDialogAccepted\"] is True for k in (r, r+\"/00_GIVE-THE-AGENT\", os.path.dirname(r))) else 1)"'
# v41: acceptance.sh fails when a check fails, and keeps what it made instead of deleting it
mkdir -p "$T/deadcli"; printf '#!/usr/bin/env bash\nexit 0\n' > "$T/deadcli/claude"; chmod +x "$T/deadcli/claude"
printf x > "$AG/tools/_x.py"   # a planted write into tools/: acceptance must see it before it moves it
ACCO="$(PATH="$T/deadcli:$PATH" bash CONTROL/harness/acceptance.sh 2>&1)"; ACCRC=$?
t "acceptance sees a write into tools/ before it moves the file (v41)" '[[ "$ACCO" == *"python wrote into tools/"* ]] && [ ! -f "$AG/tools/_x.py" ]'
t "acceptance exits non-zero when a check fails (v41)" '[ "$ACCRC" -ne 0 ] && [[ "$ACCO" == *STOP* ]]'
t "acceptance keeps its files, transcripts and scratch under _to_delete with a README (v41)" 'K="$(ls -d "$R"/_to_delete/acceptance-* 2>/dev/null | tail -1)"; [ -n "$K" ] && grep -q "failed" "$K/README.txt" && [ -d "$K/scratch" ] && ls "$K/files" | grep -q _acc && [ ! -f "$AG/out/_probe/_acc.txt" ] && [ ! -f "$R/INPUT/_acc.txt" ]'
# 2026-10-06 (J: nothing set aside stays in a repository): a run in a repository sets its files aside beside it, in
# Jail/_to_delete/ under their path; acceptance takes the compaction gate it makes, and a guard log its own sessions
# wrote, into its kept folder, and leaves a guard log that was there before
t "a run in a repository sets its files aside in Jail/_to_delete/ under their path; a run elsewhere in its own _to_delete/" '. CONTROL/harness/lib.sh; [ "$(set_aside_dir /x/Jail/r-place/aggregator/runs/r1)" = /x/Jail/_to_delete/r-place/aggregator/runs/r1 ] && [ "$(set_aside_dir /x/run)" = /x/run/_to_delete ]'
t "acceptance takes the compaction gate it made into its kept folder, not into CONTROL/ (v43.2)" 'K="$(ls -d "$R"/_to_delete/acceptance-2* 2>/dev/null | tail -1)"; [ -f "$K/compact-gate.json" ] && [ ! -e CONTROL/.compact-gate.json ] && ! ls CONTROL/.compact-gate.*.acceptance.json >/dev/null 2>&1'
mv "$AG/out/_closes/guard.log" "$T/guard-aside.log" 2>/dev/null
mkdir -p "$T/guardcli"; printf '#!/usr/bin/env bash\nprintf "blocked\\n" >> "%s/out/_closes/guard.log"\nexit 0\n' "$AG" > "$T/guardcli/claude"; chmod +x "$T/guardcli/claude"
PATH="$T/guardcli:$PATH" bash CONTROL/harness/acceptance.sh >/dev/null 2>&1
t "acceptance takes the guard log its own sessions wrote out of out/_closes into its kept folder (v43.2)" 'K="$(ls -d "$R"/_to_delete/acceptance-2* | tail -1)"; [ ! -e "$AG/out/_closes/guard.log" ] && grep -q blocked "$K/guard.log"'
printf 'before\n' > "$AG/out/_closes/guard.log"
PATH="$T/guardcli:$PATH" bash CONTROL/harness/acceptance.sh >/dev/null 2>&1
t "acceptance leaves a guard log that was there before it (v43.2)" 'head -1 "$AG/out/_closes/guard.log" | grep -qx before'
[ -f "$T/guard-aside.log" ] && mv "$T/guard-aside.log" "$AG/out/_closes/guard.log"
mkdir -p "$T/goodcli"; ln -sf "$H/tests/fake_claude_v41.py" "$T/goodcli/claude"
V41O="$(PATH="$T/goodcli:$PATH" bash CONTROL/harness/acceptance_v41.sh 2>&1)"; V41RC=$?
t "acceptance_v41.sh passes a correct analyst and a working restore (v41)" '[ "$V41RC" -eq 0 ] && [[ "$V41O" == *"LIVE CHECKS CLEAR"* ]]'
V41F="$(PATH="$T/deadcli:$PATH" bash CONTROL/harness/acceptance_v41.sh 2>&1)"; V41FRC=$?
t "acceptance_v41.sh fails a silent CLI and keeps what it made (v41)" '[ "$V41FRC" -ne 0 ] && ls -d "$R"/_to_delete/acceptance-v41-* | wc -l | grep -q 2'
t "the Claude build marks its platform and hands the Claude platform file only (v41)" '[ "$(cat CONTROL/PLATFORM)" = claude ] && [ -f "$AG/PLATFORM-claude.md" ] && [ ! -f "$AG/PLATFORM-codex.md" ] && grep -q claude-opus "$AG/PLATFORM-claude.md"'
t "the platform files match the two schedules (v41)" 'python3 "$H/gen_platform.py" --check'
# v43.2: the cost of a fork's first leg counts its own rows and models, never its parent's copies, which the CLI
# writes with their ids and without the parent's other lines (claude 2.1.289, J's Mac, 2026-10-05)
FC="$T/forkcost"; mkdir -p "$FC"
python3 - "$FC" <<'PY'
import json, os, sys
d = sys.argv[1]
def a(uid, sid):
    return {"type": "assistant", "uuid": uid, "sessionId": sid,
            "message": {"model": "m-1", "usage": {"input_tokens": 10, "output_tokens": 5}}}
meta = [{"type": k, "sessionId": "P"} for k in ("custom-title", "agent-name", "mode", "last-prompt")]
par = meta + [{"type": "user", "uuid": "u1", "sessionId": "P"}, a("a1", "P"),
              {"type": "user", "uuid": "u2", "sessionId": "P"}, a("a2", "P")] + meta
kid = ([{"type": "custom-title", "sessionId": "K"}] + [dict(r, sessionId="K") for r in par if r.get("uuid")]
       + [{"type": "user", "uuid": "u3", "sessionId": "K"}, a("a3", "K"), a("a4", "K"), {"type": "last-prompt", "sessionId": "K"}])
for n, rows in (("P", par), ("K", kid)):
    with open(os.path.join(d, n + ".jsonl"), "w") as f:
        f.write("".join(json.dumps(r) + "\n" for r in rows))
PY
python3 CONTROL/harness/protocol_guard.py cost "$FC/K.jsonl" 0 "$FC" K "$FC/cost.json" P >/dev/null 2>&1
t "a fork's first close counts its own turns and models, not its parent's (v43.2)" 'python3 -c "import json,sys;m=json.load(open(\"$FC/cost.json\"))[\"main\"];sys.exit(0 if m[\"assistant_turns\"]==2 and m[\"rows_skipped_as_inherited\"]==4 and m[\"models\"]=={\"m-1\":2} and m[\"output_tokens\"]==10 else 1)"'
# 13. publication: a failed git add is reported, never hidden as "nothing new" (v43.2)
: > "$T/.git/index.lock"; o="$(bash CONTROL/harness/publish.sh A1.A1b-02 close 2>&1 || true)"; rm -f "$T/.git/index.lock"
t "publish.sh reports a failed git add (v43.2)" '[[ "$o" == *"git: add failed"* ]] && [[ "$o" != *"nothing new to commit"* ]]'
# 14. the next leg in the leg handler's form, and D1's packets go out with D2's dispatch (v43.2)
bash CONTROL/harness/step.sh D1a --force-order >/dev/null 2>&1
echo "x packets-out" > "$AG/out/_closes/D1-D1a.closed"
o="$(bash CONTROL/harness/close.sh D1a --force 2>&1 || true)"
t "D1's packets go out with D2's dispatch (v43.2)" '[[ "$o" == *"dispatch.sh\" D2"* ]]'
t "a close names the next leg in the leg handler's form (v43.2)" '[[ "$(grep -c "legs.py" CONTROL/harness/close.sh)" -ge 2 ]] && grep -q "legs.py run" CONTROL/harness/dispatch.sh'
echo; echo "harness test: $P passed, $F failed (run left in $T)"
[ "$F" -eq 0 ]
