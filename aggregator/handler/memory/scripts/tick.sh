#!/bin/bash
# one handler tick: wait, then report closes and problems since the last tick
cd $HOME/mnt/Jail/r-place; RUN=claude-v43-1; R=aggregator/runs/$RUN; P=aggregator/handler/claude-adapter/legs.py; S=$HOME/.chatwatch-$RUN
python3 $P wait $RUN --timeout ${1:-140} | head -3 | cut -c1-300
python3 $P status $RUN | sed -n '4,5p' | cut -c1-200
touch $S.ev; grep -vxFf $S.ev $R/CONTROL/legs/events.log > $S.evnew; cat $S.evnew >> $S.ev
grep -E "closed|NEEDS YOU|stopped|refus|fail" $S.evnew | cut -c1-300
for f in $(grep -o 'closed A1\.[A-Za-z0-9-]*' $S.evnew | sed 's/closed //'); do
  echo "## $f"; python3 -c "import json;d=json.load(open('$R/CONTROL/close-status-$f.json'));print({k:d.get(k) for k in ('complete','validator_exit_code')})"
  grep -h "git:" $R/CONTROL/legs/actors/leg-$RUN-${f#A1.}-*/closes/*.log 2>/dev/null
  python3 -c "import json,glob;r=sorted(glob.glob('$R/CONTROL/legs/actors/leg-$RUN-${f#A1.}-*/turns/*/result.json'));d=[json.load(open(x)) for x in r];u=d[-1]['usage'];print('cost now',round(d[-1]['total_cost_usd'],2),'out',u['output_tokens'],'read',u['cache_read_input_tokens'],'min',round(sum(x['duration_ms'] for x in d)/60000,1))"
done
G=$(find $R -path '*/.cc' -prune -o -path '*/snapshots' -prune -o -name guard.log -print); [ -n "$G" ] && { echo "GUARD:"; wc -l $G; tail -3 $G; }
echo "defects $(wc -l < $R/00_GIVE-THE-AGENT/out/defects.jsonl) asks $(wc -l < $R/00_GIVE-THE-AGENT/out/asks.jsonl)"
timeout 80 python3 $P watch $RUN -n 4000 --full > $S.now 2>&1
grep -vxFf $S.seen $S.now > $S.new; cat $S.new >> $S.seen
echo "new lines $(wc -l < $S.new), bash $(grep -c '^[0-9:]*   Bash: ' $S.new), refused $(grep -c 'Permission refused' $S.new)"
grep -B1 'Permission refused' $S.new | grep -E '^[0-9:]+   (Bash|Read|Write|Edit)' | cut -c1-160
grep -i "analyst:.*\(cannot\|can't\|unable to\|not allowed to\|no way to\) \(ask\|reach\|contact\|talk\)\|no one to ask\|nobody to ask" $S.new | cut -c1-300
