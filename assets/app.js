(function(){
var key='hb:'+location.pathname,done={};try{done=JSON.parse(localStorage.getItem(key)||'{}')}catch(e){}
function save(){try{localStorage.setItem(key,JSON.stringify(done))}catch(e){}}
// wrap each h2 block in a section so it can be filtered and marked
var main=document.querySelector('main'),kids=[].slice.call(main.children),sec=null;
kids.forEach(function(el){if(el.tagName==='H2'){sec=document.createElement('section');main.insertBefore(sec,el)}if(sec&&el.tagName!=='FOOTER'&&el.className!=='pn')sec.appendChild(el)});
function paint(h){var on=!!done[h.id];h.classList.toggle('done',on);h.querySelector('.mark').textContent=on?'Done ✓':'Mark done';
var a=document.querySelector('.side a[href="#'+h.id+'"]');if(a)a.parentNode.classList.toggle('done',on)}
[].forEach.call(document.querySelectorAll('main h2'),function(h){var b=document.createElement('span');b.className='mark';b.setAttribute('role','button');b.tabIndex=0;h.appendChild(b);
function t(){done[h.id]=!done[h.id];save();paint(h)}b.onclick=t;b.onkeydown=function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();t()}};paint(h)});
document.getElementById('find').addEventListener('input',function(){var q=this.value.trim().toLowerCase();
[].forEach.call(document.querySelectorAll('main section'),function(s){s.classList.toggle('hide',!!q&&s.textContent.toLowerCase().indexOf(q)<0)})});
// quiz: options are shuffled on every load so the position of the answer cannot be learned
[].forEach.call(document.querySelectorAll('.quiz'),function(z){var n=0,ok=0,tot=z.querySelectorAll('.q').length;
[].forEach.call(z.querySelectorAll('.q'),function(q){var bs=[].slice.call(q.querySelectorAll('button')),why=q.querySelector('.why');
for(var i=bs.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=bs[i];bs[i]=bs[j];bs[j]=t}bs.forEach(function(b){q.insertBefore(b,why)})});
z.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var q=b.parentNode;if(q.dataset.done)return;q.dataset.done=1;n++;
if(b.hasAttribute('data-ok'))ok++;else b.classList.add('wrong');q.querySelector('button[data-ok]').classList.add('right');q.querySelector('.why').hidden=false;
z.querySelector('.score').textContent='Score: '+ok+' of '+n+' answered ('+tot+' questions)'})});
// cheat sheet: print only that section
var cheat=document.querySelector('.cheat');
if(cheat){var s=cheat.closest('section');if(s)s.classList.add('sheet');var pb=document.createElement('button');pb.type='button';pb.className='pbtn';pb.textContent='Print the cheat sheet only';
pb.onclick=function(){document.body.classList.add('sheet');window.print();setTimeout(function(){document.body.classList.remove('sheet')},500)};cheat.parentNode.insertBefore(pb,cheat)}
// mobile contents menu
var mb=document.getElementById('menu');if(mb){mb.onclick=function(){var on=document.body.classList.toggle('nav');mb.setAttribute('aria-expanded',on);mb.textContent=on?'Close':'Contents'};
document.getElementById('side').addEventListener('click',function(e){if(e.target.tagName==='A'){document.body.classList.remove('nav');mb.setAttribute('aria-expanded',false);mb.textContent='Contents'}})}
var links=[].slice.call(document.querySelectorAll('.side a'));
if('IntersectionObserver'in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(l){l.classList.toggle('on',l.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-60px 0px -75% 0px'});
[].forEach.call(document.querySelectorAll('main h2,main h3'),function(h){io.observe(h)})}
})();
