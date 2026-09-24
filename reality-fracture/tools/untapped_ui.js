/* Untapped data tab: tier list, pick order, colour pairs, trophy decks, and where my reads were off. */
var RANKNAME={2:'Bronze',3:'Silver',4:'Gold',5:'Platinum',6:'Diamond',7:'Mythic'};
var dataView='tier', dataMin=30, dataCol='all', dataRar='all';
function pct(x){ return x==null?'—':(Math.round(x*1000)/10).toFixed(1)+'%'; }
function ucard(n){ return UNTAPPED.cards[n]; }
function untappedRow(name){
  var u=ucard(name), r=BYNAME[name];
  if(!u) return '<div><dt>Untapped data</dt><dd>No Arena games recorded for this card yet.</dd></div>';
  var n=u[0], w=n/(n+60), dg=untappedGrade(u[1]);
  return '<div><dt>Untapped · early access</dt><dd>'+
    '<strong>GIH WR '+pct(u[1])+'</strong> over '+n+' games'+(n<30?' <span style="color:var(--bad)">— too few to trust</span>':'')+
    ' · opening-hand WR '+pct(u[3])+' ('+u[2]+')'+
    (u[5]?' · taken on average at pick <strong>'+u[5].toFixed(1)+'</strong>, last seen at '+u[6].toFixed(1)+' ('+u[7]+' offers)':'')+
    '<br><span style="color:var(--muted);font-size:12.5px">Pre-release read '+(r&&r[11]!=null?r[11].toFixed(1):'—')+
    ' · data grade '+dg.toFixed(1)+' · blended '+(r?r[7].toFixed(1):'—')+' ('+Math.round(w*100)+'% data weight)</span></dd></div>';
}
function tierOf(wr){ return wr>=0.62?'S':wr>=0.58?'A':wr>=0.54?'B':wr>=0.50?'C':wr>=0.45?'D':'F'; }
function dataFilter(r){
  if(dataRar!=='all'&&String(r[4])!==dataRar) return false;
  if(dataCol==='all') return true;
  if(dataCol==='multi') return r[3].length>1;
  if(dataCol==='C') return r[3].length===0;
  return r[3].length===1&&r[3]===dataCol;
}
function dataControls(){
  var cols=[['all','All'],['W','W'],['U','U'],['B','B'],['R','R'],['G','G'],['multi','Multi'],['C','Colourless']];
  var rars=[['all','All'],['0','C'],['1','U'],['2','R'],['3','M']];
  var mins=[[10,'10+'],[30,'30+'],[60,'60+'],[100,'100+']];
  function seg(id,opts,cur){ return '<div class="seg" role="group" data-seg="'+id+'">'+opts.map(function(o){return '<button type="button" data-v="'+o[0]+'" aria-pressed="'+(String(cur)===String(o[0])?'true':'false')+'">'+o[1]+'</button>';}).join('')+'</div>'; }
  return '<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:10px 0 14px">'+
    '<span class="gmeta">Colour</span>'+seg('col',cols,dataCol)+'<span class="gmeta">Rarity</span>'+seg('rar',rars,dataRar)+
    '<span class="gmeta">Min games in hand</span>'+seg('min',mins,dataMin)+'</div>';
}
function renderTier(){
  var rows=CARDS.filter(function(r){ var u=ucard(r[0]); return u&&u[1]!=null&&dataFilter(r); });
  var ok=rows.filter(function(r){return ucard(r[0])[0]>=dataMin;}).sort(function(a,b){return ucard(b[0])[1]-ucard(a[0])[1];});
  var few=rows.filter(function(r){return ucard(r[0])[0]<dataMin;}).sort(function(a,b){return ucard(b[0])[0]-ucard(a[0])[0];});
  var groups={}; ok.forEach(function(r){ var t=tierOf(ucard(r[0])[1]); (groups[t]=groups[t]||[]).push(r[0]); });
  var h=dataControls();
  ['S','A','B','C','D','F'].forEach(function(t){
    if(!groups[t]) return;
    var lo={S:'62%+',A:'58–62%',B:'54–58%',C:'50–54%',D:'45–50%',F:'under 45%'}[t];
    h+='<h4 style="margin:18px 0 6px"><span class="tier tier-'+t+'">'+t+'</span> &nbsp;GIH WR '+lo+' · '+groups[t].length+' cards</h4>'+
      '<div class="cgrid dgrid">'+groups[t].map(function(n){var u=ucard(n);return tile(n,{label:pct(u[1])+' · '+u[0]+'g'});}).join('')+'</div>';
  });
  if(few.length) h+='<details style="margin-top:18px"><summary class="gmeta" style="cursor:pointer">'+few.length+' cards under '+dataMin+' games in hand (number is noise)</summary><div class="cgrid dgrid" style="margin-top:8px">'+few.map(function(n){var u=ucard(n[0]);return tile(n[0],{label:pct(u[1])+' · '+u[0]+'g'});}).join('')+'</div></details>';
  if(!ok.length&&!few.length) h+='<p class="gmeta">Nothing matches those filters.</p>';
  return h;
}
function renderPick(){
  var rows=CARDS.filter(function(r){ var u=ucard(r[0]); return u&&u[5]&&u[7]>=10&&dataFilter(r); }).sort(function(a,b){return ucard(a[0])[5]-ucard(b[0])[5];});
  var h=dataControls().replace(/Min games in hand[\s\S]*?<\/div>/,'</div>')+
    '<p class="gmeta" style="margin:0 0 10px">Sorted by average pick taken (ATA) — where the early-access drafters actually took each card. The second number is where it was last seen (ALSA); a big gap between the two means the tables disagree about the card.</p>';
  h+='<div class="cgrid dgrid">'+rows.map(function(r,i){var u=ucard(r[0]);return tile(r[0],{label:'#'+(i+1)+' · ATA '+u[5].toFixed(1)+' · seen '+u[6].toFixed(1)});}).join('')+'</div>';
  return h;
}
function pairMatch(k){ var s=k.split('').sort().join(''); return ARCH.find(function(a){return a.pair.split('').sort().join('')===s;}); }
function renderPairs(){
  var keys=Object.keys(UNTAPPED.pairs).sort(function(a,b){return (UNTAPPED.pairs[b][2]||0)-(UNTAPPED.pairs[a][2]||0);});
  var two=keys.filter(function(k){return k.length===2;}), more=keys.filter(function(k){return k.length!==2;});
  function row(k){
    var p=UNTAPPED.pairs[k], a=pairMatch(k);
    var name=a?a.name+' <span style="color:var(--muted)">'+a.tag+'</span>':(k==='other'?'Everything else (4–5 colours, mono)':'Three colours');
    return '<tr><td>'+(k==='other'?'—':pips(k.split('')))+'</td><td>'+name+'</td><td class="num"><strong>'+pct(p[2])+'</strong></td><td class="num">'+p[0]+'</td><td class="num">'+p[3].toFixed(1)+'%</td>'+
      '<td class="num">'+(a?a.draft.toFixed(1)+' <span class="tier tier-'+a.tier+'">'+a.tier+'</span>':'—')+'</td>'+
      '<td><span class="mtr" style="display:inline-block;width:120px;height:8px;border-radius:4px;background:var(--surface-2);overflow:hidden;vertical-align:middle"><i style="display:block;height:100%;width:'+Math.round(Math.max(0,(p[2]-0.35)/0.35)*100)+'%;background:var(--accent)"></i></span></td></tr>';
  }
  return '<p class="gmeta" style="margin:0 0 10px">Match win rate of every colour combination in the early-access Premier Draft, all ranks pooled, next to the pre-release draft score this page gave it. Popularity is the share of decks.</p>'+
    '<div style="overflow:auto"><table class="picks"><thead><tr><th></th><th>Pair</th><th class="num">Match WR</th><th class="num">Matches</th><th class="num">Popularity</th><th class="num">My prior</th><th></th></tr></thead><tbody>'+
    two.map(row).join('')+'<tr><td colspan="7" class="gmeta" style="padding-top:12px">Three colours and the rest</td></tr>'+more.map(row).join('')+'</tbody></table></div>';
}
function deckPair(d){
  var pipsT={W:0,U:0,B:0,R:0,G:0};
  d.cards.forEach(function(c){ var r=BYNAME[c[0]]; if(!r) return; var p=window.FRA_PRACTICE.pipsOf(r); Object.keys(p).forEach(function(k){pipsT[k]+=p[k]*c[1];}); });
  var cs=Object.keys(pipsT).sort(function(a,b){return pipsT[b]-pipsT[a];}).filter(function(k){return pipsT[k]>0;});
  var main=cs.slice(0,2); var a=pairMatch(main.join(''));
  return {pair:a?a.pair:main.join(''), arch:a, splash:cs.slice(2)};
}
function renderDecks(){
  var h='<p class="gmeta" style="margin:0 0 12px">'+UNTAPPED.decks.length+' of the '+UNTAPPED.meta.decksTotal+' 7-win decks Untapped lists (the free page shows the rest only to subscribers). Basic lands aren\'t on Untapped\'s list; <em>Play this deck</em> builds them from the pips. Hover a card for the full picture, click it for who wants it.</p>';
  UNTAPPED.decks.forEach(function(d,i){
    var dp=deckPair(d);
    var cards=d.cards.slice().sort(function(a,b){ var ra=BYNAME[a[0]], rb=BYNAME[b[0]]; return ((ra?ra[5]:99)-(rb?rb[5]:99))||a[0].localeCompare(b[0]); });
    var n=cards.reduce(function(s,c){return s+c[1];},0);
    var list=[]; cards.forEach(function(c){ if(BYNAME[c[0]]&&!window.FRA_PRACTICE.isLand(BYNAME[c[0]])) list.push({name:c[0],count:c[1]}); });
    var rt=null; try{ rt=window.FRA_RATE.rateDeck(list); }catch(e){}
    h+='<div class="card" style="margin-top:14px" data-deck="'+i+'">'+
      '<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;justify-content:space-between">'+
        '<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">'+pips(d.c.split(''))+'<h4 style="margin:0">'+esc(d.guild||d.c)+(dp.arch?' · '+esc(dp.arch.name)+' <span style="color:var(--muted);font-weight:400">'+esc(dp.arch.tag)+'</span>':'')+'</h4>'+
          '<span class="gmeta">'+d.w+'–'+d.l+' · '+esc(RANKNAME[d.rk]||('rank '+d.rk))+' · '+esc(d.p)+' · '+esc(String(d.d).slice(0,10))+'</span></div>'+
        '<div style="display:flex;gap:8px;flex-wrap:wrap"><button class="linkbtn" type="button" data-play="'+i+'">Play this deck</button></div></div>'+
      '<p class="gmeta" style="margin:6px 0 8px">'+n+' spells + '+d.lands+' lands · '+(d.rares!=null?d.rares+' rare+':'')+(dp.splash.length?' · splashing '+dp.splash.join('/'):'')+
        (rt?' · this page rates it <strong>'+rt.score.toFixed(1)+'/10</strong> as '+esc(rt.pair):'')+
        (d.key.length?' · Untapped\'s key cards: '+d.key.map(esc).join(', '):'')+'</p>'+
      '<div class="cgrid dgrid">'+cards.map(function(c){return tile(c[0],{label:(c[1]>1?'×'+c[1]+' · ':'')+(ucard(c[0])?pct(ucard(c[0])[1]):'')});}).join('')+'</div>'+
      '<div id="deck-game-'+i+'" hidden style="margin-top:12px"></div></div>';
  });
  return h;
}
function renderMine(){
  var rows=CARDS.filter(function(r){ var u=ucard(r[0]); return u&&u[0]>=40&&r[11]!=null; });
  rows.forEach(function(r){ r._d=untappedGrade(ucard(r[0])[1])-r[11]; });
  var under=rows.slice().sort(function(a,b){return b._d-a._d;}).slice(0,14);
  var over=rows.slice().sort(function(a,b){return a._d-b._d;}).slice(0,14);
  var cols={W:[],U:[],B:[],R:[],G:[]};
  CARDS.forEach(function(r){ var u=ucard(r[0]); if(u&&u[0]>=30&&r[3].length===1&&r[4]<=1) cols[r[3]].push(u[1]); });
  var ct=Object.keys(cols).map(function(c){ var xs=cols[c]; var m=xs.length?xs.reduce(function(a,b){return a+b;},0)/xs.length:null; return {c:c,n:xs.length,wr:m,mine:COLBEST[c]?COLBEST[c].score:null}; }).sort(function(a,b){return (b.wr||0)-(a.wr||0);});
  function grid(list){ return '<div class="cgrid dgrid">'+list.map(function(r){var u=ucard(r[0]);return tile(r[0],{label:'read '+r[11].toFixed(1)+' → data '+untappedGrade(u[1]).toFixed(1)+' · '+pct(u[1])});}).join('')+'</div>'; }
  return '<p class="gmeta" style="margin:0 0 10px">Where the early-access numbers disagree most with the pre-release reads on this page (cards with 40+ games in hand). The page\'s grades are now a blend: the more games a card has, the more the data counts.</p>'+
    '<h4 style="margin:14px 0 6px">Colours — commons and uncommons, mean GIH WR</h4><div style="overflow:auto"><table class="picks"><thead><tr><th>Colour</th><th class="num">Mean GIH WR</th><th class="num">Cards</th><th class="num">My prior /10</th></tr></thead><tbody>'+
    ct.map(function(x){return '<tr><td>'+pips([x.c])+' '+esc(window.FRA_PRACTICE.COLNAME[x.c]||x.c)+'</td><td class="num"><strong>'+pct(x.wr)+'</strong></td><td class="num">'+x.n+'</td><td class="num">'+(x.mine!=null?x.mine.toFixed(1):'—')+'</td></tr>';}).join('')+'</tbody></table></div>'+
    '<h4 style="margin:18px 0 6px">I underrated these</h4>'+grid(under)+
    '<h4 style="margin:18px 0 6px">I overrated these</h4>'+grid(over);
}
function renderData(){
  var host=document.getElementById('data-body'); if(!host) return;
  var views={tier:renderTier,pick:renderPick,pairs:renderPairs,decks:renderDecks,mine:renderMine};
  host.innerHTML=(views[dataView]||renderTier)();
  document.querySelectorAll('#data-views button').forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.view===dataView?'true':'false'); });
}
function playTrophy(i){
  var d=UNTAPPED.decks[i], FP=window.FRA_PRACTICE, FG=window.FRA_GAME, FR=window.FRA_RATE;
  var list=[]; d.cards.forEach(function(c){ if(BYNAME[c[0]]&&!FP.isLand(BYNAME[c[0]])) list.push({name:c[0],count:c[1]}); });
  var r=FR.rateDeck(list); if(!r) return;
  var lands=r.plan;
  var seed=Date.now()%1000000, rr=FP.rngf(seed+3), pool=[]; for(var k=0;k<6;k++) pool=pool.concat(FP.booster(rr));
  var bd=FG.botDeck(pool);
  var run={id:Date.now(),date:new Date().toISOString(),mode:'trophy',seed:seed,pair:r.pair,deck:r.spells.slice(),pool:r.spells.slice(),suggested:r.pair,attention:[],lands:{lands:lands.lands,basics:lands.basics,duals:lands.duals,why:'built from the pips of '+d.p+'\'s 7-win '+(d.guild||d.c)+' deck'},log:[],nudges:[],hands:[],games:[],score:r.score};
  var runs=FP.LS.get('fra-runs',[]); runs.unshift(run); FP.LS.set('fra-runs',runs.slice(0,30));
  var gh=document.getElementById('deck-game-'+i); gh.hidden=false;
  FG.mount(gh,{hd:r.spells.slice(),hl:lands,hp:r.pair,bd:bd.deck.filter(function(n){return !FP.isLand(BYNAME[n]);}),bl:{basics:bd.lands.basics,duals:bd.lands.duals},bp:bd.pair,seed:seed,runId:run.id},function(){ gh.hidden=true; if(FP.renderProfile) FP.renderProfile(); showTab('t-profile'); });
  gh.scrollIntoView({behavior:'smooth',block:'start'});
}
document.addEventListener('click',function(e){
  var g=e.target.closest('[data-goto]'); if(g){ e.preventDefault(); showTab(g.dataset.goto); window.scrollTo({top:0}); return; }
  var v=e.target.closest('#data-views button'); if(v){ dataView=v.dataset.view; renderData(); return; }
  var s=e.target.closest('#data-body .seg button'); if(s){ var id=s.closest('.seg').dataset.seg, val=s.dataset.v; if(id==='col') dataCol=val; else if(id==='rar') dataRar=val; else if(id==='min') dataMin=parseInt(val,10); renderData(); return; }
  var p=e.target.closest('[data-play]'); if(p){ playTrophy(parseInt(p.dataset.play,10)); return; }
});
renderData();
