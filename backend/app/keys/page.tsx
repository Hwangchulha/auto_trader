'use client';
import { useEffect, useState } from 'react';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

type Masked = {
  exists: boolean;
  kis_env?: string;
  app_key?: string;
  app_secret?: string;
  cano?: string;
  acnt_prdt_cd?: string;
}

export default function KeysPage(){
  const [m, setM] = useState<Masked>({exists:false});
  const [kis_env, setEnv] = useState<'vts'|'prod'>('vts');
  const [app_key, setAppKey] = useState('');
  const [app_secret, setAppSecret] = useState('');
  const [cano, setCano] = useState('');
  const [acnt, setAcnt] = useState('01');
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<string|undefined>();

  async function fetchMasked(){
    try{
      const r = await fetch(`${API}/api/keys`, { cache: 'no-store' });
      if(!r.ok) throw new Error(await r.text());
      const d = await r.json();
      setM(d);
      if(d.exists){ setEnv(d.kis_env || 'vts'); setAcnt(d.acnt_prdt_cd || '01'); }
    }catch(e:any){ setMsg(e?.message || '불러오기 실패'); }
  }

  useEffect(()=>{ fetchMasked(); },[]);

  async function save(e:any){
    e.preventDefault(); setSaving(true); setMsg(undefined);
    try{
      const r = await fetch(`${API}/api/keys`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ kis_env, app_key, app_secret, cano, acnt_prdt_cd: acnt }),
      });
      if(!r.ok) throw new Error(await r.text());
      setMsg('저장 완료. 다음 호출부터 적용됩니다.');
      setAppKey(''); setAppSecret(''); setCano('');
      await fetchMasked();
    }catch(err:any){ setMsg(err?.message || '저장 실패'); }
    finally{ setSaving(false); }
  }

  const card = { border:'1px solid #333', borderRadius:8, padding:16, marginTop:12 };

  return (
    <div style={{maxWidth:720, margin:'24px auto'}}>
      <h2>🔑 KIS 키 설정</h2>
      <p style={{opacity:.8}}>모의(VTS) / 실전(PROD) 앱키·시크릿·계좌를 저장합니다. 저장된 값은 서버 DB에 보관되며, 화면에는 마스킹되어 표시됩니다.</p>

      <div style={card}>
        <div style={{display:'grid', gridTemplateColumns:'160px 1fr', gap:8}}>
          <label>저장 상태</label><div>{m.exists ? '저장됨' : '없음'}</div>
          {m.exists && <>
            <label>환경</label><div>{m.kis_env}</div>
            <label>앱키</label><div>{m.app_key}</div>
            <label>시크릿</label><div>{m.app_secret}</div>
            <label>계좌</label><div>{m.cano}</div>
            <label>상품코드</label><div>{m.acnt_prdt_cd}</div>
          </>}
        </div>
      </div>

      <form onSubmit={save} style={{...card, display:'grid', gridTemplateColumns:'160px 1fr', gap:8}}>
        <label>환경</label>
        <select value={kis_env} onChange={e=>setEnv(e.target.value as 'vts'|'prod')}>
          <option value="vts">모의(VTS)</option>
          <option value="prod">실전(PROD)</option>
        </select>
        <label>앱키</label><input value={app_key} onChange={e=>setAppKey(e.target.value)} placeholder="발급받은 App Key" />
        <label>시크릿</label><input value={app_secret} onChange={e=>setAppSecret(e.target.value)} placeholder="발급받은 App Secret" />
        <label>계좌(앞 8자리)</label><input value={cano} onChange={e=>setCano(e.target.value)} placeholder="12345678" />
        <label>상품코드</label><input value={acnt} onChange={e=>setAcnt(e.target.value)} placeholder="01" />
        <div style={{gridColumn:'1 / span 2', marginTop:8}}>
          <button type="submit" disabled={saving}>{saving ? '저장 중...' : '저장'}</button>
          {msg && <span style={{marginLeft:12, opacity:.8}}>{msg}</span>}
        </div>
      </form>
    </div>
  );
}
