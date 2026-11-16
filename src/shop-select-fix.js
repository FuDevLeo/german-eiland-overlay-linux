(()=>{
 const select=document.getElementById('skin-species-select');
 if(!select||select.dataset.geHtmlSelect)return;
 select.blur();select.dispatchEvent(new Event('blur'));select.size=1;
 select.dataset.geHtmlSelect='1';
 const original=select.getBoundingClientRect();
 const trigger=document.createElement('button');trigger.type='button';trigger.id='ge-species-trigger';trigger.setAttribute('aria-haspopup','listbox');trigger.setAttribute('aria-expanded','false');
 Object.assign(trigger.style,{minWidth:Math.max(180,original.width)+'px',height:Math.max(38,original.height)+'px',padding:'8px 14px',border:'1px solid #9f6bfd',borderRadius:'12px',background:'#191326',color:'#eee7ff',font:'inherit',textAlign:'left',cursor:'pointer'});
 select.after(trigger);select.style.setProperty('display','none','important');
 const list=document.createElement('div');list.id='ge-species-list';list.setAttribute('role','listbox');list.hidden=true;
 Object.assign(list.style,{position:'fixed',zIndex:'2147483647',overflowY:'auto',overscrollBehavior:'contain',touchAction:'pan-y',padding:'5px',background:'#191326',color:'#eee7ff',border:'1px solid #9f6bfd',borderRadius:'10px',boxShadow:'none'});
 document.body.appendChild(list);
 const label=()=>{trigger.textContent=(select.selectedOptions[0]?.text||'Alle Spezies')+'  ▾';};label();
 const close=()=>{list.hidden=true;trigger.setAttribute('aria-expanded','false');};
 const open=()=>{
  list.replaceChildren();
  for(const option of select.options){
   const item=document.createElement('button');item.type='button';item.textContent=option.text;item.setAttribute('role','option');item.setAttribute('aria-selected',String(option.selected));item.disabled=option.disabled;
   Object.assign(item.style,{display:'block',width:'100%',border:'0',borderRadius:'5px',padding:'8px 10px',textAlign:'left',background:option.selected?'#49306c':'transparent',color:'#eee7ff',font:'inherit',cursor:'pointer'});
   item.addEventListener('mouseenter',()=>item.style.background='#49306c');item.addEventListener('mouseleave',()=>item.style.background=option.selected?'#49306c':'transparent');
   item.addEventListener('click',()=>{select.value=option.value;select.dispatchEvent(new Event('input',{bubbles:true}));select.dispatchEvent(new Event('change',{bubbles:true}));label();close();trigger.focus();});list.appendChild(item);
  }
  const r=trigger.getBoundingClientRect(),below=innerHeight-r.bottom-12,above=r.top-12,height=Math.min(290,Math.max(below,above),select.options.length*34+12);
  Object.assign(list.style,{left:Math.min(r.left,innerWidth-240)+'px',width:Math.max(r.width,230)+'px',height:height+'px',top:(below>=height?r.bottom+4:Math.max(8,r.top-height-4))+'px'});
  list.hidden=false;trigger.setAttribute('aria-expanded','true');
 };
 trigger.addEventListener('click',()=>list.hidden?open():close());
 document.addEventListener('pointerdown',e=>{if(!list.contains(e.target)&&!trigger.contains(e.target))close();},true);
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!list.hidden){e.preventDefault();close();trigger.focus();}},true);
 list.addEventListener('wheel',e=>{if(list.hidden)return;e.preventDefault();e.stopPropagation();list.scrollTop+=e.deltaY*(e.deltaMode===1?20:e.deltaMode===2?list.clientHeight:1);},{passive:false});
 select.addEventListener('change',label);window.addEventListener('resize',close);window.addEventListener('scroll',e=>{if(e.target===list||list.contains(e.target))return;close();},true);
})();
