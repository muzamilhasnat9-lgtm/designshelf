(()=>{const g=document.getElementById('grid');if(!g)return;
const $=i=>document.getElementById(i),q=$('q'),c=$('cat'),f=$('fmt'),s=$('sort'),n=$('count'),cards=[...g.children],p=new URLSearchParams(location.search);
q.value=p.get('q')||'';c.value=p.get('cat')||'';$('flt').hidden=false;
const run=()=>{const t=q.value.trim().toLowerCase();let v=0;
cards.sort((a,b)=>s.value==='az'?a.dataset.n.localeCompare(b.dataset.n):b.dataset.d.localeCompare(a.dataset.d));
cards.forEach(x=>{const d=x.dataset,ok=(!t||d.s.includes(t))&&(!c.value||d.c===c.value)&&(!f.value||d.f.split(' ').includes(f.value));x.hidden=!ok;v+=ok;g.append(x)});
n.textContent=v+(v===1?' resource':' resources')+' found';};
[q,c,f,s].forEach(x=>x.addEventListener('input',run));run();})();
