// Browser acceptance uses fake controller responses only. No research or model calls.
// NODE_PATH must locate Playwright; RPLACE_BROWSER may select an installed Chromium.
const {chromium}=require('playwright');
const fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const html=fs.readFileSync(path.join(__dirname,'../panel.html'),'utf8');
const checks=[];
function fixture(){return {actors:[
 {id:'handler-one',role:'handler',status:'idle',model:'gpt-6-sol',effort:'medium',last_turn_id:'h1'},
 {id:'handler-two',role:'handler',status:'idle'},
 {id:'agg-current',role:'aggregator',run:'study',leg:'A1b-01',status:'idle',model:'gpt-6-astra',effort:'medium'},
 {id:'agg-old',role:'aggregator',run:'study',leg:'A1a',status:'idle',last_turn_id:'old',checkpoint:'cp-old'},
 {id:'reader-one',role:'reader',study_run:'study',status:'working'},
 {id:'probe-one',role:'probe',status:'idle'}],
 runs:[{id:'study',created_utc:'2026-10-03',active_actor:'agg-current',legs:{A1a:{status:'verified',checkpoint:'cp-old'},'A1b-01':{status:'prepared'}}}],
 checkpoints:[{checkpoint:'cp-old',actor:'agg-old',role:'aggregator',boundary:'completed',utc:'2026-10-03'}],jobs:{},errors:[],features:['analysis-branches-v1','leg-blocks-v1','control-guards-v1','live-questions-v1','persistent-asks-v1','external-handler-v1']}}
function events(actor){return [
 {method:'item/started',params:{item:{id:'user-1',type:'userMessage',content:[{text:'Question to '+actor}]}}},
 {method:'item/completed',params:{item:{id:'user-1',type:'userMessage',content:[{text:'Question to '+actor}]}}},
 {method:'item/agentMessage/delta',params:{itemId:'answer-1',delta:'Answer from '}},
 {method:'item/agentMessage/delta',params:{itemId:'answer-1',delta:actor}},
 {method:'item/completed',params:{item:{id:'answer-1',type:'agentMessage',text:'Answer from '+actor}}},
 {method:'item/started',params:{item:{id:'cmd-1',type:'commandExecution',command:'python check.py',status:'working'}}},
 {method:'item/commandExecution/outputDelta',params:{itemId:'cmd-1',delta:'Checks passed'}}
 ].map(native=>({native}))}
async function setup(browser,width=390){
 const context=await browser.newContext({viewport:{width,height:844},isMobile:width<700,hasTouch:width<700});
 const page=await context.newPage(),state=fixture(),requests=[],errors=[];
 const box={page,context,state,requests,errors,holdActor:null,held:null,holdSend:false,heldSend:null,failSend:false,failStatus:false,holdRestore:false};
 page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/*',async route=>{
  const req=route.request(),url=new URL(req.url());
  if(url.origin!=='https://rplace.test')return route.abort();
  if(url.pathname!=='/api')return route.fulfill({contentType:'text/html',body:html});
  const d=req.postDataJSON();requests.push(d);let result={};
  if(box.responseOverride?.action===d.action)return route.fulfill({status:200,contentType:'application/json',body:box.responseOverride.body});
  if(d.action==='status'){if(box.failStatus)return route.abort();result=state;}
  else if(d.action==='events'){
   if(box.holdActor===d.actor){box.holdActor=null;await new Promise(resolve=>box.held=resolve)}
   result={offset:1,events:d.offset===0?(box.eventOverrides?.[d.actor]||events(d.actor)):[]};
  }else if(d.action==='prepare'){
   const id='prepared-'+d.leg;state.actors.push({id,role:'aggregator',run:d.run,leg:d.leg,status:'prepared'});
   state.runs[0].active_actor=id;state.runs[0].legs[d.leg]={status:'prepared'};result={actor:id,prompt:'Instrument prompt'};if(box.stopAfterPrepare)state.runs[0].stop={reason:'Operator stopped during preparation'};
  }else if(d.action==='start'){
   state.actors.find(a=>a.id===d.actor).active_turn_id='new-turn';result={turn:{id:'new-turn'}};
  }else if(d.action==='answer'||d.action==='answer-ask'){
   state.actors.find(a=>a.id===d.actor).questions=[];result={answered:d.request,new_turn_started:false};
  }else if(['message','card'].includes(d.action)){
   if(box.holdSend){box.holdSend=false;await new Promise(resolve=>box.heldSend=resolve)}
   if(box.failSend)return route.fulfill({status:502,contentType:'application/json',body:JSON.stringify({error:'Check Jobs before repeating the command.'})});
   result={turn:{id:'message-turn'}};
  }else if(d.action==='restore'){
   result={job:'restore-job'};state.actors.push({id:'interview-new',role:'interview',origin_role:'aggregator',leg:'A1a',status:'restored',parent_checkpoint:d.checkpoint});
   state.jobs['restore-job']={status:box.holdRestore?'working':'completed',request:{action:'restore',checkpoint:d.checkpoint},result:{id:'interview-new'}};
  }else if(d.action==='branch'){
   const branch={status:'draft',source_run:d.source_run,checkpoint:d.checkpoint,after_leg:'A1a',target_leg:d.leg,changes:{}};state.runs.push({id:d.run,branch,legs:{A1a:{status:'verified',checkpoint:d.checkpoint}},active_actor:null});state.jobs['branch-job']={status:'completed',result:{run:d.run,branch,new_turn_started:false}};result={job:'branch-job'};
  }else if(d.action==='branch-upload'){
   const r=state.runs.find(r=>r.id===d.run);r.branch.changes[d.path]={sha256:d.digest,bytes:d.total};result={received:d.offset+Buffer.from(d.content,'base64').length,complete:true,new_turn_started:false};
  }else if(d.action==='prepare-branch'){
   const r=state.runs.find(r=>r.id===d.run),id='branch-leg';r.branch.status='sealed';r.active_actor=id;r.legs[r.branch.target_leg]={status:'prepared'};state.actors.push({id,role:'aggregator',run:r.id,leg:r.branch.target_leg,status:'restored',last_turn_id:'inherited-turn',leg_started:false});state.jobs['branch-prepare-job']={status:'completed',result:{run:r.id,actor:id,new_turn_started:false}};result={job:'branch-prepare-job'};
  }else if(d.action==='run-block'){
   const r=state.runs.find(r=>r.id===d.run);r.block={id:'block-one',legs:[d.first,d.last],cursor:0,status:'running',reason:'Approved range'};result=r.block;
  }else if(d.action==='stop-block'){
   const r=state.runs.find(r=>r.id===d.run);r.block.status='stopped';r.block.reason='Stopped';result=r.block;
  }else if(d.action==='resume-block'){
   const r=state.runs.find(r=>r.id===d.run);r.block.status='running';result=r.block;
  }else if(d.action==='job')result=state.jobs[d.job];
  else if(d.action==='stop-run'){result={job:'stop-job'};state.jobs['stop-job']={status:'completed',request:{action:'stop-run',run:d.run},result:{stop_requested:true,actors:[]}}}
  else if(d.action==='build'){result={job:'build-job'};state.jobs['build-job']={status:'working',request:{action:'build',run:d.run}}}
  else if(d.action==='handler'){state.actors.push({id:'handler-new',role:'handler',status:'prepared'});result={actor:'handler-new'}}
  else result={job:'fake-job'};
  await route.fulfill({contentType:'application/json',body:JSON.stringify({result})});
 });
 await page.goto('https://rplace.test/#token=fixture-token');
 await page.waitForFunction(()=>document.querySelector('#connection').textContent==='Connected');return box;
}
const mutations=box=>box.requests.filter(r=>!['status','events','job'].includes(r.action));
async function select(box,id){const p=box.page,e=await p.evaluate(id=>conversationEntries().find(x=>x.value==='actor:'+id),id);if(!e.global)await p.selectOption('#study-picker',e.study);await p.selectOption('#type-picker',e.type);await p.selectOption('#conversation-picker','actor:'+id);await p.waitForFunction(id=>document.querySelector('#session-details').textContent.includes(id),id)}
async function check(browser,name,fn,width=390){const box=await setup(browser,width);try{await fn(box);assert.deepEqual(box.errors,[]);checks.push(name);console.log('PASS '+name)}finally{box.held?.();box.heldSend?.();await box.context.close()}}
(async()=>{
 const executablePath=process.env.RPLACE_BROWSER||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
 const browser=await chromium.launch({headless:true,executablePath});
 try{
  await check(browser,'study then category scopes stages fleets and inherited interviews',async b=>{
   const p=b.page;b.state.runs.push({id:'other',legs:{},active_actor:null});b.state.actors.push({id:'other-leg',role:'aggregator',run:'other',leg:'A1a',status:'saved'},{id:'other-reader',role:'reader',study_run:'other'},{id:'study-interview',role:'interview',parent_checkpoint:'cp-old'},{id:'nested-interview',role:'interview',parent_checkpoint:'cp-interview'});b.state.checkpoints.push({checkpoint:'cp-interview',actor:'study-interview',role:'interview',parent:'cp-old'});await p.evaluate(()=>refresh(true));
   await p.selectOption('#study-picker','study');await p.selectOption('#type-picker','stage');assert.deepEqual(await p.locator('#conversation-picker option').evaluateAll(es=>es.map(e=>e.value)),['','actor:agg-old','actor:agg-current']);
   await p.selectOption('#type-picker','fleet');assert.deepEqual(await p.locator('#conversation-picker option').evaluateAll(es=>es.map(e=>e.value)),['','actor:reader-one']);
   await p.selectOption('#type-picker','interview');assert.deepEqual((await p.locator('#conversation-picker option').evaluateAll(es=>es.map(e=>e.value))).sort(),['','actor:nested-interview','actor:study-interview']);
   await p.selectOption('#study-picker','other');assert.equal(await p.locator('#conversation-picker').isDisabled(),true);await p.selectOption('#type-picker','fleet');assert.deepEqual(await p.locator('#conversation-picker option').evaluateAll(es=>es.map(e=>e.value)),['','actor:other-reader']);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'changing tree branch clears the old composer while retaining its draft',async b=>{
   const p=b.page;await select(b,'agg-current');await p.fill('#message','Draft for this leg');await p.selectOption('#type-picker','fleet');assert.equal(await p.locator('#conversation-picker').inputValue(),'');assert.equal(await p.locator('#send').isDisabled(),true);assert.equal(await p.locator('#message').inputValue(),'');
   await select(b,'agg-current');assert.equal(await p.locator('#message').inputValue(),'Draft for this leg');assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'saved snapshot category restores its tree selection on reload',async b=>{
   const p=b.page;await p.selectOption('#type-picker','saved');await p.selectOption('#conversation-picker','checkpoint:cp-old');await p.reload();await p.waitForFunction(()=>document.querySelector('#conversation-picker').value==='checkpoint:cp-old');assert.equal(await p.locator('#type-picker').inputValue(),'saved');assert.equal(await p.locator('#study-picker').inputValue(),'study');assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'Run next below a verified leg prepares and starts exactly once',async b=>{
   const p=b.page,r=b.state.runs[0];r.active_actor=null;delete r.legs['A1b-01'];await p.evaluate(()=>refresh(true));await select(b,'agg-old');assert.equal(await p.locator('#next-leg-box').isVisible(),true);assert.equal(await p.locator('#next-leg-choice').inputValue(),'A1b-01');assert.deepEqual(mutations(b),[]);
   await p.click('#next-run');await p.locator('#next-run').dispatchEvent('click');await p.waitForFunction(()=>document.querySelector('#conversation-picker').value==='actor:prepared-A1b-01'&&document.querySelector('#start').hidden);assert.deepEqual(mutations(b),[{action:'prepare',run:'study',leg:'A1b-01'},{action:'start',actor:'prepared-A1b-01'}]);assert.equal(await p.locator('#next-leg-box').isVisible(),false);assert.equal(await p.locator('#type-picker').inputValue(),'stage');
  });
  await check(browser,'next control cannot skip the current leg or bypass stop and fleet gates',async b=>{
   const p=b.page,r=b.state.runs[0];await select(b,'agg-old');assert.equal(await p.locator('#next-leg-box').isVisible(),false);r.active_actor=null;delete r.legs['A1b-01'];r.stop={reason:'Hold'};await p.evaluate(()=>refresh(true));assert.equal(await p.locator('#next-run').isDisabled(),true);delete r.stop;r.dispatch_active='fleet';await p.evaluate(()=>refresh(true));assert.equal(await p.locator('#next-run').isDisabled(),true);delete r.dispatch_active;b.state.features=[];await p.evaluate(()=>refresh(true));assert.equal(await p.locator('#next-run').isDisabled(),true);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'a stop during preparation leaves the next leg idle',async b=>{
   const p=b.page,r=b.state.runs[0];r.active_actor=null;delete r.legs['A1b-01'];await p.evaluate(()=>refresh(true));await select(b,'agg-old');b.stopAfterPrepare=true;await p.click('#next-run');await p.waitForFunction(()=>document.querySelector('#error').textContent.includes('Preparation needs review'));assert.deepEqual(mutations(b),[{action:'prepare',run:'study',leg:'A1b-01'}]);assert.equal(b.state.actors.find(a=>a.id==='prepared-A1b-01').active_turn_id,undefined);
  });
  await check(browser,'uncertain next preparation never sends a start or retries',async b=>{
   const p=b.page,r=b.state.runs[0];r.active_actor=null;delete r.legs['A1b-01'];await p.evaluate(()=>refresh(true));await select(b,'agg-old');b.responseOverride={action:'prepare',body:''};await p.click('#next-run');await p.waitForFunction(()=>document.querySelector('#error').textContent.includes('No valid reply'));assert.deepEqual(mutations(b),[{action:'prepare',run:'study',leg:'A1b-01'}]);assert.equal(await p.locator('#next-run').isDisabled(),true);
  });
  await check(browser,'uncertain next start keeps the prepared leg visible and is not replayed',async b=>{
   const p=b.page,r=b.state.runs[0];r.active_actor=null;delete r.legs['A1b-01'];await p.evaluate(()=>refresh(true));await select(b,'agg-old');b.responseOverride={action:'start',body:''};await p.click('#next-run');await p.waitForFunction(()=>document.querySelector('#error').textContent.includes('No valid reply'));assert.equal(await p.locator('#conversation-picker').inputValue(),'actor:prepared-A1b-01');assert.deepEqual(mutations(b),[{action:'prepare',run:'study',leg:'A1b-01'},{action:'start',actor:'prepared-A1b-01'}]);assert.equal(await p.locator('#start').isDisabled(),true);
  });
  await check(browser,'prior and next legs are named without typing or implicit starts',async b=>{
   const p=b.page,r=b.state.runs[0];r.active_actor=null;delete r.legs['A1b-01'];await p.evaluate(()=>refresh(true));await p.locator('#new-session > summary').click();
   assert.equal(await p.locator('#leg-choice').inputValue(),'A1b-01');assert.match(await p.locator('#leg-choice option:checked').innerText(),/A1b-01 \(new\)/);assert.equal(await p.locator('#manual-leg').isVisible(),false);
   await p.selectOption('#leg-choice','A1a');await p.click('#open-leg');assert.equal(await p.locator('#conversation-picker').inputValue(),'actor:agg-old');assert.deepEqual(mutations(b),[]);
   await p.selectOption('#leg-choice','A1b-01');await p.click('#step');await p.waitForFunction(()=>document.querySelector('#conversation-picker').value==='actor:prepared-A1b-01');assert.deepEqual(mutations(b),[{action:'prepare',run:'study',leg:'A1b-01'}]);
  });
  await check(browser,'next choices respect pauses rounds and stage completion without deciding research gates',async b=>{
   const p=b.page,r=b.state.runs[0];r.active_actor=null;r.legs={'A1b-03-p2':{status:'paused'}};await p.evaluate(()=>refresh(true));assert.match(await p.locator('#leg-choice').textContent(),/A1b-03-p3 \(new\)/);assert.doesNotMatch(await p.locator('#leg-choice').textContent(),/A1c \(new\)/);
   r.legs={'A1b-03':{status:'verified'}};await p.evaluate(()=>refresh(true));assert.match(await p.locator('#leg-choice').textContent(),/A1b-04 \(new\)/);assert.match(await p.locator('#leg-choice').textContent(),/A1c \(new\)/);
   r.finished_stages=['A1','B1'];r.legs={'B2a-r3':{status:'verified'}};await p.evaluate(()=>refresh(true));assert.match(await p.locator('#leg-choice').textContent(),/B2b-r3 \(new\)/);
   r.legs={'B2b-r3':{status:'verified'}};await p.evaluate(()=>refresh(true));assert.match(await p.locator('#leg-choice').textContent(),/B2a-r4 \(new\)/);assert.match(await p.locator('#leg-choice').textContent(),/B2c \(new\)/);
   r.finished_stages=['A1'];r.legs={'A1c':{status:'verified'}};await p.evaluate(()=>refresh(true));assert.match(await p.locator('#leg-choice').textContent(),/B1a \(new\)/);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'study switching and stop gates keep the leg target explicit',async b=>{
   const p=b.page;b.state.runs.push({id:'fresh-study',created_utc:'later',legs:{},active_actor:null});await p.evaluate(()=>refresh(true));await p.selectOption('#study-picker','fresh-study');assert.equal(await p.locator('#leg-choice').inputValue(),'A1a');
   b.state.runs[1].stop={reason:'Hold'};await p.evaluate(()=>refresh(true));assert.equal(await p.locator('#step').isDisabled(),true);
   await p.selectOption('#study-picker','');assert.equal(await p.locator('#step').isDisabled(),true);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'test actors and duplicate snapshots are hidden but remain accessible',async b=>{
   const p=b.page;b.state.actors.push({id:'test',role:'acceptance',status:'saved',checkpoint:'test-cp'},{id:'test-interview',role:'interview',origin_role:'acceptance',status:'saved'});b.state.checkpoints.push({checkpoint:'test-cp',actor:'test',role:'acceptance',boundary:'completed'});await p.evaluate(()=>refresh(true));
   assert.equal(await p.locator('#conversation-picker option[value="actor:test"]').count(),0);assert.equal(await p.locator('#conversation-picker option[value="actor:test-interview"]').count(),0);assert.equal(await p.locator('#conversation-picker option[value="checkpoint:cp-old"]').count(),0);
   await p.selectOption('#study-picker','');await p.selectOption('#type-picker','test');assert.equal(await p.locator('#conversation-picker option[value="actor:test"]').count(),1);assert.equal(await p.locator('#conversation-picker option[value="checkpoint:test-cp"]').count(),1);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'empty malformed and unrelated status replies lock controls with connection guidance',async b=>{
   const p=b.page;await select(b,'agg-current');
   for(const body of ['', '<html>Attachment preview</html>', JSON.stringify({unrelated:true})]){
    b.responseOverride={action:'status',body};await p.evaluate(()=>refresh(true));assert.equal(await p.locator('#connection').innerText(),'Disconnected');assert.equal(await p.locator('#send').isDisabled(),true);assert.match(await p.locator('#error').innerText(),/controller|Mac/);assert.doesNotMatch(await p.locator('#error').innerText(),/Unexpected end|Unexpected token|SyntaxError/);
   }
   assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'missing private link avoids API calls and explains phone setup',async b=>{
   const p=b.page;await p.evaluate(()=>sessionStorage.removeItem('rplace-token'));await p.goto('https://rplace.test/');await p.waitForFunction(()=>document.querySelector('#error').textContent.includes('Phone access must be set up first'));
   const count=b.requests.length;await p.click('#refresh');await p.waitForTimeout(100);assert.equal(b.requests.length,count);assert.equal(await p.locator('#connection').innerText(),'Disconnected');assert.equal(await p.locator('#send').isDisabled(),true);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'empty command reply never retries a possibly accepted message',async b=>{
   const p=b.page;await select(b,'agg-current');b.responseOverride={action:'message',body:''};await p.fill('#message','One message only');await p.click('#send');await p.waitForFunction(()=>document.querySelector('#error').textContent.includes('No valid reply'));
   assert.match(await p.locator('#error').innerText(),/check Jobs after reconnecting/);assert.equal(mutations(b).length,1);assert.equal(mutations(b)[0].action,'message');assert.equal(await p.locator('#send').isDisabled(),true);
  });
  await check(browser,'live question survives reload with no automatic answer',async b=>{
   const p=b.page,a=b.state.actors.find(x=>x.id==='agg-current');a.active_turn_id='question-turn';a.status='working';a.questions=[{requestKey:'q-live',requestId:7,turnId:'question-turn',isBlocking:true,questions:[{id:'choice',question:'Which interpretation fits?',options:[{label:'First',description:'Initial view'},{label:'Second',description:'Other view'}]}]}];
   await p.evaluate(()=>refresh(true));await select(b,a.id);assert.equal(await p.locator('#questions').isVisible(),true);assert.equal(await p.locator('#question-choice').inputValue(),'');assert.equal(await p.locator('#message').isDisabled(),true);
   await p.fill('#question-choice','Second, retaining the exception.');await p.reload();await p.waitForFunction(()=>document.querySelector('#question-choice')?.value==='Second, retaining the exception.');assert.deepEqual(mutations(b),[]);
   await p.click('#answer');await p.waitForFunction(()=>document.querySelector('#questions').hidden);assert.deepEqual(mutations(b),[{action:'answer',actor:a.id,request:'q-live',answers:{choice:'Second, retaining the exception.'}}]);
  });
  await check(browser,'persistent questions accept idle answers without a new turn',async b=>{
   const p=b.page,a=b.state.actors.find(x=>x.id==='agg-current');a.questions_live=false;a.questions=[{source:'file',requestKey:'QA1-001',run:'study',isBlocking:false,answerable:true,origin_leg:'A1a',assumption:'Read independent rooms meanwhile',questions:[{id:'QA1-001',question:'Use the event boundary?'}]}];
   await p.evaluate(()=>refresh(true));await select(b,a.id);assert.equal(await p.locator('#answer').isEnabled(),true);assert.equal(await p.locator('#message').isEnabled(),true);assert.match(await p.locator('#question-help').innerText(),/independent rooms/);
   await p.fill('#question-QA1-001','Use 73 hours');await p.reload();await p.waitForFunction(()=>document.querySelector('#question-QA1-001'));assert.equal(await p.locator('#question-QA1-001').inputValue(),'Use 73 hours');
   await p.click('#answer');await p.waitForFunction(()=>document.querySelector('#questions').hidden);assert.deepEqual(mutations(b),[{action:'answer-ask',actor:a.id,run:'study',request:'QA1-001',text:'Use 73 hours'}]);
  });
  await check(browser,'closed latest leg accepts a durable answer without opening an interview',async b=>{
   const p=b.page,r=b.state.runs[0],a=b.state.actors.find(x=>x.id==='agg-old');r.active_actor=null;delete r.legs['A1b-01'];a.questions=[{source:'file',requestKey:'QA1-001',run:'study',isBlocking:false,answerable:true,questions:[{id:'QA1-001',question:'Keep this case?'}]}];
   await p.evaluate(()=>refresh(true));await select(b,a.id);assert.equal(await p.locator('#send').isDisabled(),true);assert.equal(await p.locator('#answer').isEnabled(),true);await p.fill('#question-QA1-001','Yes');await p.click('#answer');await p.waitForFunction(()=>document.querySelector('#questions').hidden);assert.deepEqual(mutations(b),[{action:'answer-ask',actor:a.id,run:'study',request:'QA1-001',text:'Yes'}]);
  });
  await check(browser,'recorded answers render as text and no website handler is created',async b=>{
   const p=b.page,a=b.state.actors.find(x=>x.id==='agg-current');a.study_asks=[{id:'QA1-001',leg:'A1a',question:'<script>bad</script>',answer:'<img src=x onerror=alert(1)>',answered:true}];await p.evaluate(()=>refresh(true));await select(b,a.id);
   assert.equal(await p.locator('#answered-asks').isVisible(),true);await p.locator('#answered-asks summary').click();assert.match(await p.locator('#answer-history').innerText(),/<img/);assert.equal(await p.locator('#answer-history img').count(),0);assert.equal(await p.locator('#handler').count(),0);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'questions stay scoped across agents and alert another conversation',async b=>{
   const p=b.page;for(const id of ['handler-one','agg-current'])b.state.actors.find(a=>a.id===id).questions=[{requestKey:id+'-q',isBlocking:true,questions:[{id:'same-id',question:'Question for '+id}]}];await p.evaluate(()=>refresh(true));await select(b,'handler-one');await p.fill('#question-same-id','Handler answer');await select(b,'agg-current');assert.equal(await p.locator('#question-same-id').inputValue(),'');await select(b,'handler-one');assert.equal(await p.locator('#question-same-id').inputValue(),'Handler answer');assert.match(await p.locator('#question-alerts').innerText(),/Question from/);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'question controls reject stopped detached or stale turns and show option reasons',async b=>{
   const p=b.page,a=b.state.actors.find(x=>x.id==='agg-current');a.active_turn_id='current';a.questions_live=true;a.questions=[{requestKey:'q',turnId:'current',isBlocking:true,questions:[{id:'scope',question:'Which scope?',options:[{label:'Narrow',description:'Preserves the current frame.'}]}]}];await p.evaluate(()=>refresh(true));await select(b,a.id);assert.equal(await p.locator('#answer').isEnabled(),true);assert.match(await p.locator('#question-fields').innerText(),/Preserves the current frame/);
   b.state.runs[0].stop={reason:'Operator stop'};await p.evaluate(()=>refresh(true));assert.equal(await p.locator('#answer').isDisabled(),true);delete b.state.runs[0].stop;a.questions_live=false;await p.evaluate(()=>refresh(true));assert.equal(await p.locator('#answer').isDisabled(),true);assert.match(await p.locator('#question-help').innerText(),/unattached/);a.questions_live=true;a.active_turn_id='different';await p.evaluate(()=>refresh(true));assert.equal(await p.locator('#answer').isDisabled(),true);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'conversation includes live tool command and output',async b=>{
   await select(b,'agg-current');await b.page.waitForFunction(()=>document.querySelector('#conversation').textContent.includes('Checks passed'));assert.match(await b.page.locator('#conversation').innerText(),/python check.py/);assert.equal(await b.page.locator('#conversation details').count(),1);assert.deepEqual(mutations(b),[]);
   await b.page.click('#conversation details summary');await b.page.evaluate(()=>{consume({method:'item/commandExecution/outputDelta',params:{itemId:'cmd-1',delta:'x'.repeat(9000)}});renderStreams()});assert.equal(await b.page.locator('#conversation details').evaluate(e=>e.open),true);assert.equal((await b.page.locator('#conversation details pre').textContent()).length,9013);
  });
  await check(browser,'restore notice belongs in collapsed Activity while user words survive replay',async b=>{
   const p=b.page,a=b.state.actors.find(x=>x.id==='agg-current');a.original_workspace='/old runtime/actors/parent/workspace';
   const notice='[Restore notice: the saved workspace '+a.original_workspace+' is now /new runtime/actors/'+a.id+'/workspace. Use the restored files; the parent is immutable.]';
   const words='The canvas closed at 73 so anything after is aftermath.\n\nKeep <the evidence> exactly.';
   b.eventOverrides={[a.id]:['item/started','item/completed'].map(method=>({native:{method,params:{item:{id:'restored-message',type:'userMessage',content:[{text:notice+'\n'+words}]}}}}))};
   const raw=JSON.stringify(b.eventOverrides);await p.evaluate(()=>refresh(true));await select(b,a.id);await p.waitForFunction(()=>document.querySelector('#conversation .user .text')?.textContent.includes('aftermath'));
   assert.equal(await p.locator('#conversation .user').count(),1);assert.equal(await p.locator('#conversation .user .text').textContent(),words);assert.equal((await p.locator('#conversation').textContent()).includes(notice),false);
   await p.click('#tab-activity');assert.equal(await p.locator('#activity details').count(),1);assert.equal(await p.locator('#activity details').evaluate(e=>e.open),false);assert.equal((await p.locator('#activity').innerText()).includes('/old runtime/'),false);
   await p.click('#activity summary');assert.equal(await p.locator('#activity pre').textContent(),notice);await p.evaluate(()=>renderStreams());assert.equal(await p.locator('#activity details').evaluate(e=>e.open),true);
   await p.reload();await p.waitForFunction(()=>document.querySelector('#conversation .user .text')?.textContent.includes('aftermath'));assert.equal(await p.locator('#conversation .user .text').textContent(),words);assert.equal(await p.locator('#activity details').evaluate(e=>e.open),false);assert.equal(JSON.stringify(b.eventOverrides),raw);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'unrecognized notices quotes paths and agent text stay visible',async b=>{
   const p=b.page,a=b.state.actors.find(x=>x.id==='agg-current');a.original_workspace='/old/actors/parent/workspace';
   const notice='[Restore notice: the saved workspace '+a.original_workspace+' is now /new/actors/'+a.id+'/workspace. Use the restored files; the parent is immutable.]';
   const texts=['Please explain:\n'+notice,notice.replace('/parent/','/different/')+'\nUser message',notice.replace('/agg-current/','/other/')+'\nUser message','[Restore notice: my own incomplete note]\nKeep this','Use /old/actors/parent/workspace in this example.'];
   b.eventOverrides={[a.id]:texts.map((text,i)=>({native:{method:'item/completed',params:{item:{id:'user-'+i,type:'userMessage',content:[{text}]}}}})).concat([{native:{method:'item/completed',params:{item:{id:'agent-notice',type:'agentMessage',text:notice}}}}])};
   await p.evaluate(()=>refresh(true));await select(b,a.id);await p.waitForFunction(()=>document.querySelectorAll('#conversation .user').length===5);assert.deepEqual(await p.locator('#conversation .user .text').allTextContents(),texts);assert.equal(await p.locator('#conversation .message:not(.user) .text').textContent(),notice);assert.equal(await p.locator('#activity details').count(),0);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'dropdown reconnects without creating or starting agents',async b=>{
   const p=b.page;await select(b,'handler-one');await select(b,'agg-current');
   assert.equal(await p.locator('#message').isEnabled(),true);assert.equal(await p.locator('#start').isVisible(),true);
   await select(b,'agg-old');assert.equal(await p.locator('#message').isDisabled(),true);
   assert.equal(await p.locator('#saved-interview').isVisible(),true);assert.deepEqual(mutations(b),[]);
   assert.equal(await p.locator('#conversation-picker option[value="actor:reader-one"]').count(),0);
  });
  await check(browser,'conversation replay deduplicates messages and embeds expandable tool activity',async b=>{
   const p=b.page;await select(b,'handler-one');await p.waitForFunction(()=>document.querySelector('#conversation').textContent.includes('Answer from handler-one'));
   assert.equal(await p.locator('#conversation .message:not(.tool)').count(),2);
   assert.equal((await p.locator('#conversation').innerText()).includes('Checks passed'),false);
   await p.click('#tab-activity');assert.match(await p.locator('#activity').innerText(),/Checks passed/);
   await select(b,'reader-one');assert.equal(await p.locator('#message').isDisabled(),true);
  });
  await check(browser,'late event response cannot cross conversation boundaries',async b=>{
   b.holdActor='agg-current';await select(b,'agg-current');await b.page.waitForTimeout(100);assert.equal(typeof b.held,'function');
   await select(b,'handler-one');b.held();await b.page.waitForFunction(()=>document.querySelector('#conversation').textContent.includes('Answer from handler-one'));
   assert.equal((await b.page.locator('#conversation').innerText()).includes('Answer from agg-current'),false);
  });
  await check(browser,'dropdown leg preparation and start are separate actions',async b=>{
   const p=b.page;b.state.runs[0].active_actor=null;await p.evaluate(()=>refresh(true));await p.locator('#new-session > summary').click();await p.selectOption('#leg-choice','__manual__');await p.selectOption('#stage-picker','B1');await p.selectOption('#step-picker','b');await p.fill('#leg-number','3');await p.click('#step');
   await p.waitForFunction(()=>document.querySelector('#conversation-picker').value==='actor:prepared-B1b-03');
   assert.deepEqual(mutations(b),[{action:'prepare',run:'study',leg:'B1b-03'}]);
   await p.click('#start');await p.waitForFunction(()=>document.querySelector('#start').hidden);
   assert.equal(mutations(b).filter(x=>x.action==='start').length,1);assert.equal(mutations(b).at(-1).actor,'prepared-B1b-03');
  });
  await check(browser,'round and paused-leg choices do not depend on hidden block input',async b=>{
   const p=b.page;b.state.runs[0].active_actor=null;await p.evaluate(()=>refresh(true));await p.locator('#new-session > summary').click();await p.selectOption('#leg-choice','__manual__');await p.selectOption('#stage-picker','B2');await p.fill('#leg-number','2');assert.equal(await p.locator('#leg-preview').innerText(),'B2a-r2');
   await p.fill('#leg-number','0');await p.selectOption('#stage-picker','A1');assert.equal(await p.locator('#leg-preview').innerText(),'A1a');
   await p.fill('#exact-leg','A1b-02-p2');await p.click('#step');await p.waitForFunction(()=>document.querySelector('#conversation-picker').value==='actor:prepared-A1b-02-p2');
   assert.equal(mutations(b)[0].leg,'A1b-02-p2');
  });
  await check(browser,'saved selection is read-only until explicit interview restore',async b=>{
   const p=b.page;await select(b,'agg-old');await p.click('#saved-interview');assert.deepEqual(mutations(b),[]);
   assert.equal(await p.locator('#message').isDisabled(),true);await p.click('#restore');
   await p.waitForFunction(()=>document.querySelector('#conversation-picker').value==='actor:interview-new');
   assert.deepEqual(mutations(b),[{action:'restore',checkpoint:'cp-old'}]);assert.equal(b.state.runs[0].active_actor,'agg-current');
  });
  await check(browser,'cards reach selected leg once even with repeated clicks',async b=>{
   const p=b.page;await select(b,'agg-current');await p.selectOption('#message-kind','card');await p.fill('#message','A research card');b.holdSend=true;
   await p.click('#send');await p.waitForTimeout(100);await p.locator('#send').dispatchEvent('click');
   assert.equal(mutations(b).length,1);b.heldSend();await p.waitForFunction(()=>!document.querySelector('#send').disabled);
   assert.deepEqual(mutations(b)[0],{action:'card',actor:'agg-current',text:'A research card'});
  });
  await check(browser,'draft and response remain attached to their own conversation',async b=>{
   const p=b.page;await select(b,'handler-one');await p.fill('#message','Draft for first handler');await select(b,'handler-two');await p.fill('#message','Draft for second handler');await select(b,'handler-one');
   assert.equal(await p.locator('#message').inputValue(),'Draft for first handler');b.holdSend=true;await p.click('#send');await p.waitForTimeout(100);await select(b,'handler-two');b.heldSend();
   await p.waitForFunction(()=>!document.querySelector('#send').disabled);assert.equal(await p.locator('#message').inputValue(),'Draft for second handler');
   assert.equal(mutations(b)[0].actor,'handler-one');
  });
  await check(browser,'failed command is not retried and draft stays visible',async b=>{
   const p=b.page;b.failSend=true;await select(b,'handler-one');await p.fill('#message','Do this once');await p.click('#send');await p.waitForFunction(()=>!document.querySelector('#error').hidden);
   await p.waitForTimeout(1200);assert.equal(mutations(b).length,1);assert.equal(await p.locator('#message').inputValue(),'Do this once');
  });
  await check(browser,'browser reload reconnects to the same selected conversation',async b=>{
   const p=b.page;await select(b,'handler-two');await p.reload();await p.waitForFunction(()=>document.querySelector('#conversation-picker').value==='actor:handler-two');assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'analysis fork uploads future card and publishes before an explicit first turn',async b=>{
   const p=b.page;await p.selectOption('#type-picker','saved');await p.selectOption('#conversation-picker','checkpoint:cp-old');await p.locator('#branch-create-box summary').click();await p.fill('#branch-name','variant');await p.fill('#branch-leg','B1a');await p.click('#branch-create');
   await p.waitForFunction(()=>document.querySelector('#study-picker').value==='variant');assert.equal(mutations(b).some(x=>['message','start','open'].includes(x.action)),false);
   await p.setInputFiles('#branch-file',{name:'STAGE-C2-test.md',mimeType:'text/markdown',buffer:Buffer.from('Revised C2 card')});
   assert.equal(await p.locator('#branch-delivery').inputValue(),'C2');await p.click('#branch-upload');await p.waitForFunction(()=>document.querySelector('#branch-changes').textContent.includes('STAGE-C2-test.md'));
   const uploaded=mutations(b).find(x=>x.action==='branch-upload');assert.equal(uploaded.stage,'C2');assert.equal(uploaded.path,'stages/STAGE-C2-test.md');assert.equal(Buffer.from(uploaded.content,'base64').toString(),'Revised C2 card');
   assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
   if(process.env.RPLACE_BRANCHSHOT)await p.screenshot({path:process.env.RPLACE_BRANCHSHOT,fullPage:true});
   await p.click('#branch-prepare');await p.waitForFunction(()=>document.querySelector('#conversation-picker').value==='actor:branch-leg');
   assert.equal(mutations(b).some(x=>['message','start','open'].includes(x.action)),false);assert.equal(await p.locator('#start').isVisible(),true);
   await p.click('#start');assert.equal(mutations(b).at(-1).action,'start');assert.equal(b.state.runs[0].active_actor,'agg-current');
  });
  await check(browser,'old controllers disable new branch operations',async b=>{
   const p=b.page;b.state.features=[];await p.evaluate(()=>refresh(true));await p.selectOption('#type-picker','saved');await p.selectOption('#conversation-picker','checkpoint:cp-old');await p.locator('#branch-create-box summary').click();assert.equal(await p.locator('#branch-create').isDisabled(),true);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'finite block approval survives browser reload without another start',async b=>{
   const p=b.page;await p.locator('#leg-block summary').click();await p.fill('#block-first','A1b-01');await p.fill('#block-last','A1b-02');await p.click('#block-start');
   await p.waitForFunction(()=>document.querySelector('#block-state').textContent.includes('running'));
   assert.deepEqual(mutations(b),[{action:'run-block',run:'study',first:'A1b-01',last:'A1b-02'}]);
   await p.reload();await p.waitForFunction(()=>document.querySelector('#connection').textContent==='Connected');
   assert.equal(mutations(b).length,1);await p.locator('#leg-block summary').click();await p.click('#block-stop');
   await p.waitForFunction(()=>!document.querySelector('#block-resume').disabled);await p.click('#block-resume');
   assert.deepEqual(mutations(b).map(x=>x.action),['run-block','stop-block','resume-block']);
   assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  });
  await check(browser,'old controllers cannot approve blocks',async b=>{
   b.state.features=[];await b.page.evaluate(()=>refresh(true));await b.page.locator('#leg-block summary').click();
   assert.equal(await b.page.locator('#block-start').isDisabled(),true);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'idle pause and inherited close are disabled',async b=>{
   const p=b.page,a=b.state.actors.find(a=>a.id==='agg-current');a.last_turn_id='inherited';a.leg_started=false;a.boundary='completed';await p.evaluate(()=>refresh(true));await select(b,'agg-current');
   assert.equal(await p.locator('#pause').isDisabled(),true);assert.equal(await p.locator('#close').isDisabled(),true);assert.equal(await p.locator('#start').isEnabled(),true);assert.match(await p.locator('#actor-status').innerText(),/Ready to start/);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'disconnection locks mutations and reconnect preserves draft',async b=>{
   const p=b.page;await select(b,'agg-current');await p.fill('#message','Retain this draft');b.failStatus=true;await p.evaluate(()=>refresh(true));await p.waitForFunction(()=>document.querySelector('#connection').textContent==='Disconnected');
   assert.equal(await p.locator('#start').isDisabled(),true);assert.equal(await p.locator('#send').isDisabled(),true);assert.equal(await p.locator('#handler').count(),0);assert.match(await p.locator('#connection-help').innerText(),/Mac may still be working/);
   b.failStatus=false;await p.evaluate(()=>refresh(true));await p.waitForFunction(()=>document.querySelector('#connection').textContent==='Connected');assert.equal(await p.locator('#message').inputValue(),'Retain this draft');assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'stop gate and failure are visible without opening Jobs',async b=>{
   const p=b.page;b.state.runs[0].stop={reason:'User stop'};b.state.actors.find(a=>a.id==='agg-current').error={message:'Runtime cannot load encodings'};await p.evaluate(()=>refresh(true));await select(b,'agg-current');
   assert.match(await p.locator('#study-summary').innerText(),/Study stopped/);assert.match(await p.locator('#actor-attention').innerText(),/encodings/);assert.equal(await p.locator('#send').isDisabled(),true);assert.equal(await p.locator('#start').isDisabled(),true);assert.equal(await p.locator('#continue-run').isEnabled(),true);assert.equal(await p.locator('#step').isDisabled(),true);
  });
  await check(browser,'pending restore locks duplicate actions until completion and after reload',async b=>{
   const p=b.page;b.holdRestore=true;await p.selectOption('#type-picker','saved');await p.selectOption('#conversation-picker','checkpoint:cp-old');await p.click('#restore');await p.waitForFunction(()=>document.querySelector('#notice').textContent.includes('Restoring'));
   assert.equal(await p.locator('#restore').isDisabled(),true);await p.reload();await p.waitForFunction(()=>document.querySelector('#conversation-picker').value==='checkpoint:cp-old');assert.equal(await p.locator('#restore').isDisabled(),true);assert.equal(mutations(b).length,1);
   b.state.jobs['restore-job'].status='completed';await p.evaluate(()=>refresh(true));await p.waitForFunction(()=>!document.querySelector('#restore').disabled);assert.equal(mutations(b).length,1);
  });
  await check(browser,'draft survives reload and tabs support keyboard navigation',async b=>{
   const p=b.page;await select(b,'handler-one');await p.fill('#message','Unsent private draft');await p.reload();await p.waitForFunction(()=>document.querySelector('#conversation-picker').value==='actor:handler-one');assert.equal(await p.locator('#message').inputValue(),'Unsent private draft');await p.focus('#tab-chat');await p.keyboard.press('ArrowRight');assert.equal(await p.locator('#tab-activity').getAttribute('aria-selected'),'true');assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'block preview states target and rejects cross-stage approval',async b=>{
   const p=b.page;await p.locator('#leg-block summary').click();await p.fill('#block-first','A1b-01');await p.fill('#block-last','A1b-05');assert.match(await p.locator('#block-preview').innerText(),/study: 5 leg/);await p.fill('#block-last','B1b-05');await p.click('#block-start');assert.match(await p.locator('#error').innerText(),/one repeated step/);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'uncertain first start cannot advertise another Start',async b=>{
   const p=b.page,a=b.state.actors.find(a=>a.id==='agg-current');a.leg_started=true;a.status='starting';await p.evaluate(()=>refresh(true));await select(b,'agg-current');assert.equal(await p.locator('#start').isVisible(),false);assert.match(await p.locator('#actor-attention').innerText(),/no turn is confirmed/);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'pending actor stop locks clearing the study stop across reload',async b=>{
   const p=b.page;b.state.runs[0].stop={reason:'User stop'};b.state.jobs.stopping={status:'working',request:{action:'stop',actor:'agg-current',run:'study'}};await p.reload();await p.waitForFunction(()=>document.querySelector('#connection').textContent==='Connected');await select(b,'handler-one');assert.equal(await p.locator('#continue-run').isDisabled(),true);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'pending branch preparation locks uploads and publication after reload',async b=>{
   const p=b.page,r=b.state.runs[0];r.active_actor=null;r.branch={status:'draft',source_run:'parent',after_leg:'A1a',target_leg:'A1b-01',changes:{}};r.legs={};b.state.jobs.preparing={status:'working',request:{action:'prepare-branch',run:'study'}};await p.reload();await p.waitForFunction(()=>document.querySelector('#connection').textContent==='Connected');assert.equal(await p.locator('#branch-prepare').isDisabled(),true);assert.equal(await p.locator('#branch-upload').isDisabled(),true);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'Build stays locked through its job and reports failure',async b=>{
   const p=b.page;await p.locator('summary').filter({hasText:'Study controls'}).click();await p.locator('summary').filter({hasText:'Build a new study'}).click();await p.fill('#new-run','new-study');await p.fill('#source','/fixture/pristine');await p.click('#build');await p.waitForFunction(()=>document.querySelector('#notice').textContent.includes('Study build is running'));assert.equal(await p.locator('#build').isDisabled(),true);assert.equal(mutations(b).length,1);
   b.state.jobs['build-job']={...b.state.jobs['build-job'],status:'failed',error:'Synthetic build failed'};await p.waitForFunction(()=>document.querySelector('#error').textContent.includes('Synthetic build failed'));assert.equal(mutations(b).length,1);
  });
  await check(browser,'legacy reader interview has independent controls even if source is stopped',async b=>{
   const p=b.page;b.state.runs[0].stop={reason:'Source stopped'};b.state.actors.push({id:'legacy-interview',role:'interview',run:null,study_run:'study',dispatch_id:'source-fleet',origin_role:'reader',status:'idle',last_turn_id:'interview-turn'});await p.evaluate(()=>refresh(true));await select(b,'legacy-interview');assert.equal(await p.locator('#send').isEnabled(),true);assert.equal(await p.locator('#stop').innerText(),'Stop and save');assert.match(await p.locator('#actor-description').innerText(),/Independent interview/);
   b.state.features=[];await p.evaluate(()=>refresh(true));assert.equal(await p.locator('#stop').isDisabled(),true);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'global handler explains its authority and leg title names its study',async b=>{
   const p=b.page;await select(b,'handler-one');assert.match(await p.locator('#actor-description').innerText(),/all studies/);await select(b,'agg-current');assert.match(await p.locator('#chat-title').innerText(),/study \/ A1b-01/);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'partial stop archive failure is visible in Jobs',async b=>{
   const p=b.page;b.state.jobs.stop={status:'completed',request:{action:'stop-run',run:'study'},result:{actors:[{actor:'agg-current',error:'Archive failed'}]}};await p.evaluate(()=>refresh(true));await p.click('#tab-jobs');assert.match(await p.locator('#jobs').innerText(),/Archive failed.*Store preserved/);assert.deepEqual(mutations(b),[]);
  });
  await check(browser,'main study Stop bypasses an in-flight actor message',async b=>{
   const p=b.page;await select(b,'agg-current');b.holdSend=true;await p.fill('#message','Working request');await p.click('#send');await p.waitForTimeout(100);assert.equal(typeof b.heldSend,'function');assert.equal(await p.locator('#stop').isEnabled(),true);await p.click('#stop');await p.waitForFunction(()=>document.querySelector('#jobs').textContent.includes('stop-run'));assert.equal(mutations(b).some(r=>r.action==='stop-run'&&r.run==='study'),true);assert.equal(mutations(b).some(r=>r.action==='stop'),false);b.heldSend();
  });
  for(const width of [320,390,768,1280])await check(browser,'layout fits '+width+'px without horizontal page scroll',async b=>{
   const p=b.page;await select(b,'agg-current');await p.locator('#new-session > summary').click();
   assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
   assert.ok((await p.locator('#send').boundingBox()).height>=44);
   assert.equal(await p.locator('#actor-actions button').evaluateAll(bs=>bs.filter(b=>!b.hidden).every(b=>b.scrollWidth<=b.clientWidth)),true);
   if(width===390&&process.env.RPLACE_SCREENSHOT){await p.locator('#new-session > summary').click();await p.screenshot({path:process.env.RPLACE_SCREENSHOT,fullPage:true})}
  },width);
  console.log(JSON.stringify({passed:checks.length,browser:await browser.version(),live_calls:0}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
