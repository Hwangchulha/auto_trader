(()=>{
  const API = (window.NEXT_PUBLIC_API_BASE || window.__API_BASE__ ||
               (location.origin.replace(':3000', ':8000')) || location.origin);

  function el(tag, attrs={}, children=[]) {
    const e = document.createElement(tag);
    Object.entries(attrs).forEach(([k,v])=>{
      if (k==='style' && typeof v==='object') Object.assign(e.style, v);
      else if (k==='className') e.className = v;
      else e.setAttribute(k,v);
    });
    (Array.isArray(children)?children:[children]).filter(Boolean).forEach(c=>{
      if (typeof c==='string') e.appendChild(document.createTextNode(c));
      else e.appendChild(c);
    });
    return e;
  }

  function css() {
    const s = el('style', {}, `
    #kis-key-fab{position:fixed;right:18px;bottom:18px;z-index:2147483647;background:#222;color:#fff;border:none;border-radius:24px;padding:12px 16px;box-shadow:0 4px 12px rgba(0,0,0,.3);cursor:pointer;font-size:14px}
    #kis-key-modal{position:fixed;inset:0;z-index:2147483646;display:none;background:rgba(0,0,0,.5);align-items:center;justify-content:center}
    #kis-key-modal .card{background:#111;color:#eee;min-width:360px;max-width:560px;border:1px solid #333;border-radius:12px;padding:16px;box-shadow:0 8px 32px rgba(0,0,0,.4)}
    #kis-key-modal label{display:block;margin:8px 0 4px 2px;font-size:12px;opacity:.85}
    #kis-key-modal input,#kis-key-modal select{width:100%;padding:10px;border:1px solid #333;background:#0b0b0b;color:#eee;border-radius:8px}
    #kis-key-modal .row{display:grid;grid-template-columns:120px 1fr;gap:8px;align-items:center}
    #kis-key-modal .row > label{margin:0}
    #kis-key-modal .actions{display:flex;gap:8px;justify-content:flex-end;margin-top:12px}
    #kis-key-modal .btn{background:#2b63ff;border:none;color:#fff;padding:10px 14px;border-radius:8px;cursor:pointer}
    #kis-key-modal .btn-alt{background:#333}
    #kis-key-banner{position:fixed;top:8px;left:50%;transform:translateX(-50%);z-index:2147483647;background:#6a4; color:#111;padding:8px 14px;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,.25);display:none;cursor:pointer}
    `);
    document.head.appendChild(s);
  }

  function fab() {
    const b = el('button', {id:'kis-key-fab'}, '🔑 키 설정');
    b.onclick = ()=> openModal();
    document.body.appendChild(b);
  }

  function modal() {
    const wrap = el('div', {id:'kis-key-modal'});
    const card = el('div', {className:'card'});
    const title = el('div', {style:{fontSize:'16px', fontWeight:'700', marginBottom:'8px'}}, 'KIS 키 설정');
    const status = el('div', {id:'kis-key-status', style:{fontSize:'12px', opacity:'.8', marginBottom:'8px'}}, '상태: 확인 중...');

    const row = (label, input)=> el('div', {className:'row'}, [el('label',{},label), input]);
    const envSel = el('select', {}, [el('option',{value:'vts'},'모의(VTS)'), el('option',{value:'prod'},'실전(PROD)')]);
    const appKey = el('input', {placeholder:'App Key'});
    const appSec = el('input', {placeholder:'App Secret'});
    const cano   = el('input', {placeholder:'계좌(앞 8자리)'});
    const acnt   = el('input', {placeholder:'상품코드(예: 01)'});

    const actions = el('div', {className:'actions'}, [
      el('button', {className:'btn-alt', onclick: ()=> closeModal()}, '닫기'),
      el('button', {className:'btn', id:'kis-key-save'}, '저장'),
    ]);

    card.appendChild(title);
    card.appendChild(status);
    card.appendChild(row('환경', envSel));
    card.appendChild(row('앱키', appKey));
    card.appendChild(row('시크릿', appSec));
    card.appendChild(row('계좌', cano));
    card.appendChild(row('상품코드', acnt));
    card.appendChild(actions);
    wrap.appendChild(card);
    wrap.addEventListener('click', e=>{ if(e.target===wrap) closeModal(); });
    document.body.appendChild(wrap);

    async function loadMasked(){
      try{
        const r = await fetch(`${API}/api/keys`, {cache:'no-store'});
        if(!r.ok) throw new Error(await r.text());
        const d = await r.json();
        if(d.exists){
          envSel.value = d.kis_env || 'vts';
          acnt.value = d.acnt_prdt_cd || '01';
          status.textContent = `상태: 저장됨 (${d.kis_env}) | 앱키:${d.app_key} | 시크릿:${d.app_secret} | 계좌:${d.cano}`;
        }else{
          status.textContent = '상태: 아직 저장되지 않음';
        }
      }catch(err){
        status.textContent = '상태 확인 실패';
      }
    }

    async function save(){
      const payload = {
        kis_env: envSel.value,
        app_key: appKey.value,
        app_secret: appSec.value,
        cano: cano.value,
        acnt_prdt_cd: acnt.value || '01'
      };
      try{
        const r = await fetch(`${API}/api/keys`, { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(payload) });
        if(!r.ok) throw new Error(await r.text());
        await loadMasked();
        alert('저장 완료. 다음 호출부터 적용됩니다.');
        appKey.value=''; appSec.value=''; cano.value='';
      }catch(e){
        alert('저장 실패: ' + (e?.message||e));
      }
    }

    document.getElementById('kis-key-save').onclick = save;

    return {wrap, loadMasked};
  }

  function banner(){
    const b = el('div', {id:'kis-key-banner'}, '🔑 키가 설정되지 않았습니다. 클릭하여 설정하세요.');
    b.onclick = ()=> openModal();
    document.body.appendChild(b);
    return b;
  }

  let _modal;
  function openModal(){ if(!_modal) _modal = modal(); _modal.wrap.style.display='flex'; _modal.loadMasked(); }
  function closeModal(){ if(_modal) _modal.wrap.style.display='none'; }

  async function runtime(){
    try{
      const r = await fetch(`${API}/api/settings/runtime`, {cache:'no-store'});
      if(!r.ok) return {needs_keys:false};
      return await r.json();
    }catch{ return {needs_keys:false}; }
  }

  async function init(){
    css();
    fab();
    const b = banner();
    const rt = await runtime();
    if(rt && rt.needs_keys){
      b.style.display='block';
      openModal();   // 자동 오픈
    }
  }

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
