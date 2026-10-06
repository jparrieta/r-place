"""Local HTML manual publishing. No network or provider dependency."""
import html,re
from .common import *

def render(text):
    lines=[]; code=False
    for line in text.splitlines():
        if line.startswith('```'):
            lines.append('</code></pre>' if code else '<pre><code>'); code=not code; continue
        if code: lines.append(html.escape(line)+'\n'); continue
        if not line.strip(): continue
        content=html.escape(line)
        content=re.sub(r'`([^`]+)`',r'<code>\1</code>',content)
        content=re.sub(r'\[([^]]+)\]\(([^)]+)\)',lambda m:'<a href="'+m[2]+'">'+m[1]+'</a>',content)
        n=len(line)-len(line.lstrip('#'))
        lines.append(f'<h{n}>{content[n:].strip()}</h{n}>' if 0<n<5 else '<p>'+content+'</p>')
    return '\n'.join(lines)

def publish():
    out=REPO/'Manual-html'; out.mkdir(exist_ok=True)
    from . import study
    rows=study.load_module(study.INSTRUMENT/'tools/steps.py','manual_steps').table()
    arm=read(study.HARNESS/'arm.codex.json')
    cards=REPO/'Manual/openai-stages'; cards.mkdir(parents=True,exist_ok=True)
    model_lines=['# OpenAI models and effort','', 'Pilot allocation, not a measured optimum. Aggregator: GPT-6 Astra. Routine packet readers and new case coders: GPT-6 Sol medium. D2 and D3 restore original case leads on their recorded model and effort. C2 and C5 reviewers: GPT-6 Astra high. Counts and scientific roles stay as specified by the instrument.','', '| Stage | Effort by step | Reader model and effort |','|---|---|---|']
    for stage in dict.fromkeys(r['stage'] for r in rows):
        selected=[r for r in rows if r['stage']==stage]; config=arm[stage]; reader=config.get('readers')
        efforts=', '.join(r['step']+': '+config.get('legs',{}).get(r['step'],{}).get('effort',config['effort']) for r in selected)
        fleet=(reader['model']+' '+reader['effort']) if reader else 'none'
        model_lines.append('| '+stage+' | '+efforts+' | '+fleet+' |')
        body='# '+stage+': '+selected[0]['stage_name']+'\n\nModel: '+config['analyst']+'. Effort: '+efforts+'.\n\n'
        body+='Use one leg at a time in a study. Each leg continues the previous native checkpoint. Reader jobs and separate studies can run in parallel. Closure automatically validates, archives and dispatches. Repeat counts and pilot rounds below are starting examples.\n\n```bash\n'
        for row in selected:
            leg=stage+row['step']+('-01' if row['repeat']=='yes' else '-r1' if row['repeat']=='round' else '')
            body+='python3 r-place/aggregator/handler/codex/run.py step STUDY '+leg+' --start\n'
        body+='```\n\nTalk through the live panel or `run.py chat ACTOR`. Open a checkpoint as an interview without changing the study. See [OpenAI operation](../../OPENAI.md).\n'
        atomic(cards/(stage+'.md'),body)
    atomic(REPO/'Manual/OPENAI-MODELS.md','\n'.join(model_lines)+'\n')
    text=(REPO/'OPENAI.md').read_text().replace('(Manual/OPENAI-MODELS.md)','(OPENAI-MODELS.html)').replace('(Manual/openai-stages/A1.md)','(OPENAI-A1.html)').replace('(FLEET-ARMS.md)','(FLEET-ARMS.html)').replace('(Manual-html/INSTRUMENT-v43.html)','(INSTRUMENT-v43.html)').replace('(aggregator/', '(../aggregator/')
    page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>OpenAI operation</title><style>body{font:17px system-ui;max-width:940px;margin:40px auto;padding:20px;line-height:1.6;color:#252822;background:#faf9f6}pre{padding:18px;background:#eceee9;overflow:auto}code{font:14px ui-monospace,monospace}a{color:#145740}</style><p><a href="OPENAI-LIVE.html">Open the live control panel</a> | <a href="index.html">Research manual</a></p>'+render(text)+'</html>'
    atomic(out/'OPENAI.html',page)
    models='<table><tr><th>Stage</th><th>Effort by step</th><th>Readers</th></tr>'
    for line in model_lines[5:]:
        if line.startswith('|') and not line.startswith('|---'):
            models+='<tr>'+''.join('<td>'+html.escape(v.strip())+'</td>' for v in line.strip('|').split('|'))+'</tr>'
    models+='</table>'
    shell=page[:page.index('<h1>')]
    # Publish the authoritative revised scientific cards, not only new launch commands.
    sources=[study.INSTRUMENT/n for n in ('CONTRACT-aggregator.md','METHOD.md','STANDING-INSTRUCTIONS.md','SCHEMA-adaptations.md','PRIOR-template.md','OPENAI-RUNTIME.md','HOW-TO-RUN.md')]+sorted((study.INSTRUMENT/'stages').glob('STAGE-*.md'))
    index=['# Instrument v43','', 'Current scientific rules and stage cards. Earlier manual narratives describe previous editions. The source instrument below governs new builds.','']
    for src in sources:
        dest='V43-'+src.stem+'.html'
        atomic(out/dest,shell+render(src.read_text())+'</html>')
        index.append('- ['+src.stem+']('+dest+')')
    index+=['','D4 exports the adaptation dendrogram as SVG, HTML and JSON. The root is the global model reference, leaves are cases, and declared cross-links remain explicit.','', '[Codex operation](OPENAI.html)']
    atomic(REPO/'Manual/INSTRUMENT-v43.md','\n'.join(index).replace('](V43-','](../Manual-html/V43-')+'\n')
    atomic(out/'INSTRUMENT-v43.html',shell+render('\n'.join(index))+'</html>')
    atomic(out/'FLEET-ARMS.html',shell+render((REPO/'FLEET-ARMS.md').read_text())+'</html>')
    atomic(out/'OPENAI-MODELS.html',shell+'<h1>Model and effort allocation</h1><p>Codex arm defaults. <a href="FLEET-ARMS.html">OpenRouter reader arm and configuration</a>. Pilot allocation, not a measured optimum.</p>'+models+'</html>')
    for card in cards.glob('*.md'):
        siblings='<p>'+ ' | '.join('<a href="OPENAI-'+st+'.html">'+st+'</a>' for st in dict.fromkeys(r['stage'] for r in rows))+'</p>'
        atomic(out/('OPENAI-'+card.stem+'.html'),shell+siblings+render(card.read_text().replace('(../../OPENAI.md)','(OPENAI.html)'))+'</html>')
    atomic(out/'OPENAI-LIVE.html','<!doctype html><meta charset="utf-8"><title>Start the controller</title><p>In Terminal, from this repository root, run:</p><pre>python3 "aggregator/handler/codex/run.py" serve</pre><p>Then open the private launcher path printed by the command. Its location relative to this repository is ../.rplace-runtime-v43/OPENAI-LIVE.html. This repository page contains no token.</p>')
    # Historical and Claude manual pages are owned separately. Do not rewrite them.
    return {'manual':str(out/'OPENAI.html'),'live':str(DATA/'OPENAI-LIVE.html')}
