/* My Decks: decks you've played, Claude's read of how they win, your own points, and a record. */
(function(){
var FP=window.FRA_PRACTICE, LS=FP.LS;
var MD={decks:LS.get('fra-mydecks',[]),cur:null,sample:null,canImage:false,image:null,ctl:null,draft:[]};
function $(id){return document.getElementById(id);}
function save(){ LS.set('fra-mydecks',MD.decks); }
function FR(){ return window.FRA_RATE; }
function deckOf(id){ return MD.decks.find(function(d){return d.id===id;}); }
function spells(list){ return list.filter(function(c){ return BYNAME[c.name]&&!FP.isLand(BYNAME[c.name]); }); }
function colorsOf(d){ var p={W:0,U:0,B:0,R:0,G:0}; spells(d.list).forEach(function(c){ var q=FP.pipsOf(BYNAME[c.name]); Object.keys(q).forEach(function(k){p[k]+=q[k]*c.count;}); }); return Object.keys(p).filter(function(k){return p[k]>0;}).sort(function(a,b){return p[b]-p[a];}); }
function count(list){ return list.reduce(function(s,c){return s+c.count;},0); }
function ratingOf(d){ try{ return FR().rateDeck(d.list); }catch(e){ return null; } }
var COPY={not_granted:'This page wasn’t allowed to ask Claude in this view.',sampling_disabled:'Claude isn’t available for this account.',images_unavailable:'This view can’t send images — paste the list instead.',image_rejected:'That file was rejected — try a PNG or JPEG under 20 MB.',rate_limited:'Too many requests right now. Try again in a minute.',session_expired:'Please sign in again.',refused:'Claude declined this request.',invalid_json:'The reply wasn’t clean JSON. Try again.',cancelled:'Stopped.'};

/* ---------- list ---------- */
function renderHome(){
  var host=$('md-body'); if(!host) return;
  var h='<div class="grid g2" style="align-items:start">';
  h+='<div class="card"><h4>Add a deck you played</h4>'+
    '<label class="gmeta" for="md-name">Name</label><input id="md-name" class="gsearch" style="width:100%;margin:4px 0 10px" placeholder="e.g. WU Fatehold, 5–2 on Tuesday">'+
    '<div id="md-img" hidden><p style="font-size:13px;color:var(--ink-2)">Screenshot of the Arena deck. Reading it asks Claude on your account.</p>'+
      '<input type="file" id="md-file" class="gsearch" style="padding:6px" accept="image/*"><div id="md-preview" style="margin:8px 0"></div>'+
      '<div style="display:flex;gap:8px;flex-wrap:wrap"><button class="linkbtn" type="button" id="md-read" disabled style="border-color:var(--accent);color:var(--accent)">Read the cards</button><button class="linkbtn" type="button" id="md-stop" hidden>Stop</button></div></div>'+
    '<p style="font-size:13px;color:var(--ink-2);margin-top:10px">Or paste the Arena export (Decks → your deck → Export), one card per line.</p>'+
    '<textarea id="md-text" class="gsearch" rows="5" style="width:100%;font-family:IBM Plex Mono,monospace;font-size:12.5px" placeholder="1 Fatehold Chronologist (FRA) 133&#10;2 Last Gasp (FRA) 56&#10;8 Island"></textarea>'+
    '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px"><button class="linkbtn" type="button" id="md-parse">Add these cards</button>'+
      '<button class="linkbtn" type="button" id="md-from-rate">Use the Rate-a-Deck list</button>'+
      '<select id="md-from-run" class="gsearch" style="padding:6px"><option value="">Use a practice run…</option>'+LS.get('fra-runs',[]).filter(function(r){return r.deck&&r.deck.length;}).slice(0,15).map(function(r){return '<option value="'+r.id+'">'+esc((r.mode||'draft')+' · '+(r.pair||'')+' · '+String(r.date).slice(0,10))+'</option>';}).join('')+'</select></div>'+
    '<p class="gmeta" id="md-status" style="margin-top:8px"></p>'+
    '<div id="md-draft" style="margin-top:10px"></div>'+
    '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px"><button class="linkbtn" type="button" id="md-save" style="border-color:var(--accent);color:var(--accent)">Save deck</button><button class="linkbtn" type="button" id="md-clear">Clear</button></div></div>';
  h+='<div class="card"><h4>Your decks</h4>'+(MD.decks.length?'':'<p class="gmeta">Nothing saved yet.</p>')+
    MD.decks.map(function(d){ var cs=colorsOf(d).slice(0,2); return '<div style="display:flex;gap:10px;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--line)">'+
      '<div>'+pips(cs)+' <strong>'+esc(d.name)+'</strong><div class="gmeta">'+String(d.created).slice(0,10)+' · '+count(d.list)+' cards · '+(d.wins||0)+'–'+(d.losses||0)+(d.analysis?' · analysed':'')+(d.points&&d.points.length?' · '+d.points.length+' points':'')+'</div></div>'+
      '<div style="display:flex;gap:6px"><button class="linkbtn" type="button" data-md-open="'+d.id+'">Open</button><button class="linkbtn" type="button" data-md-del="'+d.id+'">Delete</button></div></div>'; }).join('')+'</div>';
  h+='</div>';
  host.innerHTML=h; renderDraft(); wireHome();
}
function renderDraft(){
  var host=$('md-draft'); if(!host) return;
  if(!MD.draft.length){ host.innerHTML=''; return; }
  var sp=spells(MD.draft), lands=MD.draft.filter(function(c){return !(BYNAME[c.name]&&!FP.isLand(BYNAME[c.name]));});
  host.innerHTML='<p class="gmeta">'+count(sp)+' spells · '+count(lands)+' lands</p><div class="cgrid dgrid">'+MD.draft.map(function(c,i){return '<div style="position:relative">'+tile(c.name,{label:c.count>1?'×'+c.count:''})+'<button class="linkbtn" type="button" data-md-rm="'+i+'" style="position:absolute;top:2px;right:2px;z-index:3;padding:0 6px;font-size:11px;background:var(--surface)" aria-label="Remove '+esc(c.name)+'">×</button></div>';}).join('')+'</div>';
}
function addCards(cards){ cards.forEach(function(c){ var e=MD.draft.find(function(x){return x.name===c.name;}); if(e) e.count+=c.count; else MD.draft.push({name:c.name,count:c.count}); }); renderDraft(); }
function status(t,busy){ var s=$('md-status'); if(s) s.innerHTML=t; if($('md-read')) $('md-read').disabled=!!busy||!MD.image; if($('md-stop')) $('md-stop').hidden=!busy; }
async function readImage(){
  if(!MD.sample||!MD.image) return;
  var ctl=new AbortController(); MD.ctl=ctl; status('Reading the screenshot… up to a minute.',true);
  var names=CARDS.map(function(r){return r[0];}).concat(Object.keys(BASICCOL));
  var prompt='This image is a screenshot of a Magic: The Gathering Limited deck (usually the MTG Arena deck builder) from the set Reality Fracture. List every card in the deck with its quantity. Read counts from the list if shown; if the deck is a grid of card images, count duplicates. Include basic lands. Use ONLY names from this vocabulary, choosing the closest match for anything partially visible:\n'+names.join(' | ')+'\n\nReply with only JSON of the form {"cards":[{"name":"Card Name","count":2}]}. No other text.';
  try{
    var data=await MD.sample.json(prompt,{images:MD.image,modelTier:'default',signal:ctl.signal,cache:false});
    var got=[], unk=[]; ((data&&data.cards)||[]).forEach(function(c){ var m=FR().match(c.name); var n=Math.max(1,parseInt(c.count,10)||1); if(m) got.push({name:m.name,count:n}); else unk.push(c.name); });
    addCards(got); status('Read '+count(got)+' cards.'+(unk.length?' Couldn’t place: '+unk.map(esc).join(', ')+'.':'')+' Check the grid, name the deck, then save.',false);
  }catch(e){ status(COPY[e&&e.code]||('Couldn’t read the image ('+esc((e&&e.code)||'error')+').'),false); }
}
function wireHome(){
  $('md-parse').addEventListener('click',function(){ var p=FR().parseList($('md-text').value); addCards(p.cards.map(function(c){return {name:c.name,count:c.count};})); status(p.cards.length+' lines placed'+(p.unknown&&p.unknown.length?', couldn’t place: '+p.unknown.map(esc).join(', '):'')+'.'); $('md-text').value=''; });
  $('md-from-rate').addEventListener('click',function(){ var l=(FR().state().list||[]); if(!l.length){ status('The Rate-a-Deck list is empty.'); return; } addCards(l.map(function(c){return {name:c.name,count:c.count};})); status('Copied '+count(l)+' cards from Rate a Deck.'); });
  $('md-from-run').addEventListener('change',function(e){ var id=parseInt(e.target.value,10); var r=LS.get('fra-runs',[]).find(function(x){return x.id===id;}); if(!r) return; var list={}; r.deck.forEach(function(n){list[n]=(list[n]||0)+1;}); var cards=Object.keys(list).map(function(n){return {name:n,count:list[n]};}); if(r.lands&&r.lands.basics){ Object.keys(r.lands.basics).forEach(function(k){ var nm={W:'Plains',U:'Island',B:'Swamp',R:'Mountain',G:'Forest'}[k]; if(nm&&r.lands.basics[k]) cards.push({name:nm,count:r.lands.basics[k]}); }); (r.lands.duals||[]).forEach(function(n){cards.push({name:n,count:1});}); } MD.draft=[]; addCards(cards); if(!$('md-name').value) $('md-name').value=(r.mode||'draft')+' '+(r.pair||'')+' '+String(r.date).slice(0,10); status('Loaded the run’s 40.'); });
  $('md-clear').addEventListener('click',function(){ MD.draft=[]; renderDraft(); status(''); });
  $('md-save').addEventListener('click',function(){ if(!MD.draft.length){ status('Add some cards first.'); return; } var d={id:Date.now(),name:$('md-name').value.trim()||('Deck '+(MD.decks.length+1)),created:new Date().toISOString(),list:MD.draft.slice(),wins:0,losses:0,points:[],analysis:null}; MD.decks.unshift(d); MD.decks=MD.decks.slice(0,40); save(); MD.draft=[]; MD.cur=d.id; renderDetail(); });
  $('md-draft').addEventListener('click',function(e){ var b=e.target.closest('[data-md-rm]'); if(b){ MD.draft.splice(parseInt(b.dataset.mdRm,10),1); renderDraft(); } });
  if($('md-file')){ $('md-file').addEventListener('change',function(e){ var f=e.target.files&&e.target.files[0]; MD.image=f||null; var pv=$('md-preview'); if(f){ pv.innerHTML='<img src="'+URL.createObjectURL(f)+'" alt="" style="max-height:160px;border-radius:8px">'; } else pv.innerHTML=''; $('md-read').disabled=!f; }); $('md-read').addEventListener('click',readImage); $('md-stop').addEventListener('click',function(){ if(MD.ctl) MD.ctl.abort(); }); }
  if(MD.canImage&&$('md-img')) $('md-img').hidden=false;
}

/* ---------- detail ---------- */
function cardTx(n){ var g=GAME[n]; var r=BYNAME[n]; return (r?r[6]+' · '+r[9]:'')+(g&&g.tx?' — '+g.tx.replace(/\n/g,' / '):''); }
function analysisHtml(a){
  if(!a) return '';
  function cardsRow(cs){ var ok=(cs||[]).filter(function(n){return BYNAME[n];}); return ok.length?'<div class="cgrid dgrid" style="margin:6px 0 4px">'+ok.map(function(n){return tile(n);}).join('')+'</div>':''; }
  var h='';
  if(a.summary) h+='<p style="margin:6px 0 12px">'+esc(a.summary)+'</p>';
  if(a.win_conditions&&a.win_conditions.length) h+='<h4 style="margin:14px 0 4px">How it wins</h4>'+a.win_conditions.map(function(w){return '<div style="margin:4px 0 10px"><strong>'+esc(w.title||'')+'</strong>'+cardsRow(w.cards)+'<div style="font-size:13.5px">'+esc(w.how||'')+'</div></div>';}).join('');
  if(a.combos&&a.combos.length) h+='<h4 style="margin:14px 0 4px">Combos and synergies</h4>'+a.combos.map(function(c){return '<div style="margin:4px 0 10px">'+cardsRow(c.cards)+'<div style="font-size:13.5px">'+esc(c.why||'')+'</div></div>';}).join('');
  if(a.plan) h+='<h4 style="margin:14px 0 4px">Game plan</h4><dl><div><dt>Early</dt><dd>'+esc(a.plan.early||'')+'</dd></div><div><dt>Mid</dt><dd>'+esc(a.plan.mid||'')+'</dd></div><div><dt>Late</dt><dd>'+esc(a.plan.late||'')+'</dd></div></dl>';
  if(a.mulligan) h+='<h4 style="margin:14px 0 4px">Keepable hands</h4><p style="font-size:13.5px">'+esc(a.mulligan)+'</p>';
  if(a.weaknesses&&a.weaknesses.length) h+='<h4 style="margin:14px 0 4px">What beats it</h4><ul style="font-size:13.5px;padding-left:18px">'+a.weaknesses.map(function(w){return '<li>'+esc(w)+'</li>';}).join('')+'</ul>';
  if(a.cuts&&a.cuts.length) h+='<h4 style="margin:14px 0 4px">Weakest slots</h4>'+a.cuts.map(function(c){return '<div style="margin:4px 0 8px">'+cardsRow([c.card])+'<div style="font-size:13.5px">'+esc(c.why||'')+'</div></div>';}).join('');
  if(a.on_your_points&&a.on_your_points.length) h+='<h4 style="margin:14px 0 4px">On your points</h4><ul style="font-size:13.5px;padding-left:18px">'+a.on_your_points.map(function(w){return '<li>'+esc(w)+'</li>';}).join('')+'</ul>';
  return h;
}
function revisionsHtml(d){
  var rv=d.revisions||[]; if(!rv.length) return '';
  var latest=rv[0];
  var h='<div style="margin:10px 0 4px;padding:10px 12px;border:1px solid var(--accent);border-radius:10px"><div class="gmeta">Your latest point · '+String(latest.at).slice(0,16).replace('T',' ')+'</div>'+
    '<p style="margin:4px 0;font-style:italic">“'+esc(latest.point)+'”</p>'+
    (latest.reading?'<p style="margin:4px 0;font-size:13.5px"><strong>What it tells us:</strong> '+esc(latest.reading)+(latest.pattern?' <span class="gmeta">('+esc(latest.pattern)+')</span>':'')+'</p>':'')+
    (latest.changes&&latest.changes.length?'<p style="margin:4px 0 0;font-size:13.5px"><strong>What changed below:</strong></p><ul style="margin:2px 0 0;padding-left:18px;font-size:13.5px">'+latest.changes.map(function(c){return '<li>'+esc(c)+'</li>';}).join('')+'</ul>':'<p class="gmeta" style="margin:4px 0 0">The analysis stood as it was.</p>')+'</div>';
  if(rv.length>1) h+='<details style="margin:4px 0 8px"><summary class="gmeta" style="cursor:pointer">Earlier revisions ('+(rv.length-1)+')</summary>'+rv.slice(1).map(function(r){return '<div style="margin:8px 0;font-size:13px"><span class="gmeta">'+String(r.at).slice(0,10)+'</span> “'+esc(r.point)+'” — '+esc(r.reading||'')+(r.changes&&r.changes.length?'<ul style="margin:2px 0;padding-left:18px">'+r.changes.map(function(c){return '<li>'+esc(c)+'</li>';}).join('')+'</ul>':'')+'</div>';}).join('')+'</details>';
  return h;
}
function renderDetail(){
  var d=deckOf(MD.cur); if(!d){ MD.cur=null; renderHome(); return; }
  var host=$('md-body'); var cs=colorsOf(d); var rt=ratingOf(d);
  var sorted=d.list.slice().sort(function(a,b){ var ra=BYNAME[a.name], rb=BYNAME[b.name]; var la=ra?(FP.isLand(ra)?1:0):1, lb=rb?(FP.isLand(rb)?1:0):1; return (la-lb)||((ra?ra[5]:99)-(rb?rb[5]:99))||a.name.localeCompare(b.name); });
  var h='<p><a href="#" id="md-back" class="gmeta">← all decks</a></p>'+
    '<div class="card"><div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;justify-content:space-between">'+
      '<div>'+pips(cs.slice(0,3))+' <h4 style="display:inline;margin:0">'+esc(d.name)+'</h4><div class="gmeta">'+String(d.created).slice(0,10)+' · '+count(spells(d.list))+' spells + '+(count(d.list)-count(spells(d.list)))+' lands'+(rt?' · this page rates it <strong>'+rt.score.toFixed(1)+'/10</strong> as '+esc(rt.pair):'')+'</div></div>'+
      '<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap"><span class="gmeta">Record</span><strong id="md-rec">'+(d.wins||0)+'–'+(d.losses||0)+'</strong><button class="linkbtn" type="button" data-md-win="1">+ win</button><button class="linkbtn" type="button" data-md-loss="1">+ loss</button><button class="linkbtn" type="button" data-md-undo="1" title="Undo the last result">undo</button></div></div>'+
    '<div class="cgrid dgrid" style="margin-top:12px">'+sorted.map(function(c){return tile(c.name,{label:(c.count>1?'×'+c.count:'')+(UNTAPPED.cards[c.name]&&UNTAPPED.cards[c.name][1]!=null?(c.count>1?' · ':'')+(Math.round(UNTAPPED.cards[c.name][1]*1000)/10).toFixed(1)+'%':'')});}).join('')+'</div></div>';
  h+='<div class="grid g2" style="align-items:start;margin-top:16px"><div class="card"><h4>Your points</h4><p style="font-size:13px;color:var(--ink-2)">What you noticed playing it — a line that won, a card that underperformed, a question. Claude reads these when it analyses the deck.</p>'+
    '<ul id="md-points" style="padding-left:18px;font-size:13.5px">'+(d.points||[]).map(function(p,i){return '<li style="margin:4px 0">'+esc(p.text)+' <span class="gmeta">'+String(p.at).slice(0,10)+'</span> <button class="linkbtn" type="button" data-md-pdel="'+i+'" style="padding:0 6px;font-size:11px" aria-label="Remove point">×</button></li>';}).join('')+'</ul>'+
    '<div style="display:flex;gap:8px"><input id="md-point" class="gsearch" style="flex:1" placeholder="Add a point…"><button class="linkbtn" type="button" id="md-addpoint">Add</button></div></div>';
  h+='<div class="card"><h4>Claude’s read</h4>'+(MD.sample?'<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center"><button class="linkbtn" type="button" id="md-analyse" style="border-color:var(--accent);color:var(--accent)">'+(d.analysis?'Analyse again':'Analyse this deck')+'</button><button class="linkbtn" type="button" id="md-astop" hidden>Stop</button><span class="gmeta" id="md-astatus"></span></div>':'<p class="gmeta">Analysis asks Claude on your account and only works inside the claude.ai viewer.</p>')+
    (d.pendingPoint?'<p class="gmeta" style="color:var(--bad)">A point was added since the last analysis. Open this page in the claude.ai viewer to have it re-read.</p>':'')+
    revisionsHtml(d)+
    '<div id="md-analysis">'+(d.analysis?analysisHtml(d.analysis)+'<p class="gmeta" style="margin-top:10px">Analysed '+String(d.analysedAt||'').slice(0,16).replace('T',' ')+'</p>':'')+'</div></div></div>';
  host.innerHTML=h; wireDetail(d);
}
async function analyse(d,newPoint){
  if(!MD.sample) return;
  if(MD.ctl) MD.ctl.abort();
  var ctl=new AbortController(); MD.ctl=ctl; var st=$('md-astatus'); if(st) st.textContent=newPoint?'Reading your point and re-approaching the deck…':'Asking Claude… this takes a minute.'; if($('md-analyse')) $('md-analyse').disabled=true; if($('md-astop')) $('md-astop').hidden=false;
  var list=d.list.map(function(c){ return c.count+'x '+c.name+(BYNAME[c.name]?' — '+cardTx(c.name):''); }).join('\n');
  var pts=(d.points||[]).map(function(p){return '- '+p.text;}).join('\n');
  var prompt='You are a Magic: The Gathering Limited coach for the set Reality Fracture. Below is a 40-card deck the player has been playing on Arena, with each card\'s type, cost and rules text. Read the actual card texts; do not assume cards from other sets.\n\nDECK:\n'+list+
    (pts?'\n\nTHE PLAYER\'S OWN POINTS FROM PLAYING IT (oldest first):\n'+pts:'')+
    (d.analysis?'\n\nYOUR PREVIOUS ANALYSIS OF THIS DECK (JSON):\n'+JSON.stringify({summary:d.analysis.summary,win_conditions:d.analysis.win_conditions,combos:d.analysis.combos,plan:d.analysis.plan,mulligan:d.analysis.mulligan,weaknesses:d.analysis.weaknesses,cuts:d.analysis.cuts}):'')+
    (newPoint?'\n\nTHE PLAYER JUST ADDED THIS POINT:\n"'+newPoint+'"\n\nFirst analyse that point: what does it reveal about how the deck is actually playing, and is it a real pattern or variance? Then re-approach the whole deck analysis in light of it: keep what still holds, change what the point contradicts (a win condition that is not happening, a combo that does not assemble, a card to cut, a different plan or mulligan rule), and list every change you made and why. Do not just append a reply — revise the analysis itself.':'')+
    '\n\nExplain how this deck wins and what its combos are. Be concrete and name cards. Reply with ONLY JSON in this exact shape:\n'+
    '{"summary":"two sentences on what the deck is","win_conditions":[{"title":"short name","cards":["Card A","Card B"],"how":"how these cards actually close the game"}],'+
    '"combos":[{"cards":["Card A","Card B"],"why":"why they are better together, with the rules interaction"}],'+
    '"plan":{"early":"turns 1-3","mid":"turns 4-6","late":"turn 7+"},"mulligan":"what a keepable seven needs","weaknesses":["what beats this deck"],'+
    '"cuts":[{"card":"weakest card","why":"and what to want instead"}],"on_your_points":["a reply to each of the player\'s points, if any"],'+
    '"point_analysis":{"reading":"what the newest point tells you about the deck (empty string if no new point)","pattern":"real pattern | probably variance | need more games","changes":["each change made to the analysis because of it, and why"]}}\n'+
    'Give 2-4 win conditions, 4-8 combos, 2-4 weaknesses, 2 cuts. Use only card names that appear in the deck.';
  try{
    var a=await MD.sample.json(prompt,{modelTier:'default',signal:ctl.signal,cache:false});
    if(newPoint){ var pa=a.point_analysis||{}; d.revisions=d.revisions||[]; d.revisions.unshift({at:new Date().toISOString(),point:newPoint,reading:pa.reading||'',pattern:pa.pattern||'',changes:pa.changes||[]}); d.revisions=d.revisions.slice(0,20); }
    d.analysis=a; d.analysedAt=new Date().toISOString(); save(); if(MD.cur===d.id) renderDetail();
  }catch(e){ if(e&&e.code==='cancelled'&&MD.ctl!==ctl) return; if(st) st.textContent=COPY[e&&e.code]||('Couldn’t analyse ('+((e&&e.code)||'error')+').'); if($('md-analyse')) $('md-analyse').disabled=false; if($('md-astop')) $('md-astop').hidden=true; }
}
function wireDetail(d){
  if(d.pendingPoint&&MD.sample){ var pp=d.pendingPoint; d.pendingPoint=null; save(); analyse(d,pp); }
  $('md-back').addEventListener('click',function(e){ e.preventDefault(); MD.cur=null; renderHome(); });
  $('md-addpoint').addEventListener('click',function(){ var t=$('md-point').value.trim(); if(!t) return; d.points=d.points||[]; d.points.push({text:t,at:new Date().toISOString()}); d.pendingPoint=MD.sample?null:t; save(); renderDetail(); if(MD.sample) analyse(d,t); });
  $('md-point').addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); $('md-addpoint').click(); } });
  if($('md-analyse')){ $('md-analyse').addEventListener('click',function(){ analyse(d); }); $('md-astop').addEventListener('click',function(){ if(MD.ctl) MD.ctl.abort(); }); }
}
document.addEventListener('click',function(e){
  var t;
  if((t=e.target.closest('[data-md-open]'))){ MD.cur=parseInt(t.dataset.mdOpen,10); renderDetail(); return; }
  if((t=e.target.closest('[data-md-del]'))){ var id=parseInt(t.dataset.mdDel,10); if(t.dataset.sure){ MD.decks=MD.decks.filter(function(x){return x.id!==id;}); save(); renderHome(); } else { t.dataset.sure='1'; t.textContent='Really delete?'; } return; }
  var d=deckOf(MD.cur); if(!d) return;
  if(e.target.closest('[data-md-win]')){ d.wins=(d.wins||0)+1; d.last='w'; save(); $('md-rec').textContent=d.wins+'–'+(d.losses||0); return; }
  if(e.target.closest('[data-md-loss]')){ d.losses=(d.losses||0)+1; d.last='l'; save(); $('md-rec').textContent=(d.wins||0)+'–'+d.losses; return; }
  if(e.target.closest('[data-md-undo]')){ if(d.last==='w'&&d.wins) d.wins--; else if(d.last==='l'&&d.losses) d.losses--; d.last=null; save(); $('md-rec').textContent=(d.wins||0)+'–'+(d.losses||0); return; }
  if((t=e.target.closest('[data-md-pdel]'))){ d.points.splice(parseInt(t.dataset.mdPdel,10),1); save(); renderDetail(); return; }
});
(async function(){
  try{
    if(window.claude&&window.claude.use){ var s=await window.claude.use('sample'); MD.sample=s; if(s){ var caps=await s.limits().catch(function(){return null;}); MD.canImage=!!(caps&&caps.images); if(MD.canImage&&$('md-file')) $('md-file').accept=caps.images.mediaTypes.join(','); } }
  }catch(e){}
  if(MD.cur) renderDetail(); else renderHome();
})();
window.FRA_MYDECKS={state:function(){return MD;},renderHome:renderHome,renderDetail:renderDetail,analysisHtml:analysisHtml};
renderHome();
})();
