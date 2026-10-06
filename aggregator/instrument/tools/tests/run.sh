#!/usr/bin/env bash
# Runs the v38 tools over the synthetic fixture, then the verb tests (test_verbs.py, their own store).
# From INSTRUMENT/: bash tools/tests/run.sh [RUN]   (RUN: a real run folder to smoke-test the verbs on)
set -e
T="$(cd "$(dirname "$0")/.." && pwd)"; W="$(mktemp -d "${TMPDIR:-/tmp}/fixture.XXXXXX")"; cp -r "$T/tests/fixture/." "$W/"; cp "$T/../CONTRACT-aggregator.md" "$W/"
cd "$W"; echo C2 > .stage; echo C2a-01 > .leg
python3 "$T/ingest.py" D --check denmark
python3 "$T/ingest.py" D || true                       # asoiaf is meant to fail
# Sweden is present in the synthetic store but intentionally supplies no return.
printf 'sweden\tfixture supplies no return\n' >> DROPS/D/UNRETURNED.tsv
python3 "$T/mem.py" log "test" --kind note --ids denmark >/dev/null
python3 "$T/mem.py" diary --last 1
python3 "$T/cite.py" --room denmark --code c0117 | head -1
python3 "$T/cite.py" --resolve "calling for hands" && exit 1 || true   # a label must be rejected
python3 "$T/mem.py" adaptations --element P07 | head -3
python3 "$T/distance.py" --out out --quartets 500 | cut -c1-60
python3 "$T/gen_views.py" D3 --root .
python3 "$T/rebuild.py" denmark --out out | head -3
python3 "$T/links.py" --out out
ROOT=. bash "$T/done.sh" C2 --cut merging || echo "(done.sh refused the close: the fixture is not a stage C2 output; expected once validate.py exists)"
python3 "$T/validate.py" --self-test --summary > "$W/selftest.log" || { cat "$W/selftest.log"; exit 1; }; tail -1 "$W/selftest.log"
python3 "$T/tests/test_verbs.py" ${1:+--run "$1"} > "$W/verbs.log" || { grep -A12 FAIL "$W/verbs.log"; exit 1; }; tail -1 "$W/verbs.log"
python3 "$T/tests/test_stage_d.py" > "$W/stage-d.log" || { grep -A6 FAIL "$W/stage-d.log"; exit 1; }; tail -1 "$W/stage-d.log"
for TEST in test_methods_v40.py test_statistics.py test_views_v40.py; do
  python3 -B -W ignore::ResourceWarning "$T/tests/$TEST" > "$W/$TEST.log" 2>&1 || { cat "$W/$TEST.log"; exit 1; }
  tail -5 "$W/$TEST.log"
done
echo "fixture run OK in $W"
