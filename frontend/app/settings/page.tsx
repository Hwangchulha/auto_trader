'use client';
import { useEffect, useState } from 'react';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function Settings(){
  const [rt, setRt] = useState<any|undefined>();
  const [keys, setKeys] = useState<any|undefined>();
  const [kis_env, setEnv] = useState<'vts'|'prod'>('vts');
  const [app_key, setAppKey] = useState('');
  const [app_secret, setAppSecret] = useState('');
  const [cano, setCano] = useState('');
  const [acnt, setAcnt] = useState('01');
  const [msg, setMsg] = useState<string|undefined>();

  async function loadAll(){
    const r1 = await fetch(`${API}/api/settings/runtime`, { cache:'no-store' });
    const r2 = await fetch(`${API}/api/keys`, { cache:'no-store' });
    const a = await r1.json(); const b = await r2.json();
    setRt(a); setKeys(b);
    if(b.exists){ setEnv(b.kis_env || 'vts'); setAcnt(b.acnt_prdt_cd || '01'); }
  }

  useEffect(()=>{ loadAll(); }, []);

  async function saveKeys(e:any){
    e.preventDefault(); setMsg(undefined);
    const r = await fetch(`${API}/api/keys`, {
      method:'POST', headers:{'content-type':'application/json'},
      body: JSON.stringify({ kis_env, app_key, app_secret, cano, acnt_prdt_cd: acnt })
    });
    if(!r.ok){ setMsg(await r.text()); return; }
    setMsg('저장 완료'); setAppKey(''); setAppSecret(''); setCano(''); await loadAll();
  }

  return (
    <div className="row">
      <div className="card" style={{flex:1}}>
        <h3>런타임</h3>
        <div>API: {rt?.NEXT_PUBLIC_API_BASE}</div>
        <div>SIM_MODE: {rt?.SIM_MODE}</div>
        <div>KIS_ENV(기본): {rt?.KIS_ENV}</div>
        <div>DEFAULT_TZ: {rt?.DEFAULT_TZ}</div>
      </div>

      <div className="card" style={{flex:1}}>
        <h3>🔑 KIS 키 설정</h3>
        {keys?.exists ? (
          <div style={{opacity:.9, marginBottom:8}}>
            <div>저장됨</div>
            <div>환경: {keys.kis_env}</div>
            <div>앱키: {keys.app_key}</div>
            <div>시크릿: {keys.app_secret}</div>
            <div>계좌: {keys.cano}</div>
            <div>상품코드: {keys.acnt_prdt_cd}</div>
          </div>
        ) : <div style={{opacity:.8, marginBottom:8}}>아직 저장되지 않았습니다.</div>}
        <form onSubmit={saveKeys} style={{display:'grid', gridTemplateColumns:'160px 1fr', gap:8}}>
          <label>환경</label>
          <select value={kis_env} onChange={e=>setEnv(e.target.value as any)}>
            <option value="vts">모의(VTS)</option>
            <option value="prod">실전(PROD)</option>
          </select>
          <label>앱키</label><input className="input" value={app_key} onChange={e=>setAppKey(e.target.value)} placeholder="App Key" />
          <label>시크릿</label><input className="input" value={app_secret} onChange={e=>setAppSecret(e.target.value)} placeholder="App Secret" />
          <label>계좌(앞 8자리)</label><input className="input" value={cano} onChange={e=>setCano(e.target.value)} placeholder="12345678" />
          <label>상품코드</label><input className="input" value={acnt} onChange={e=>setAcnt(e.target.value)} placeholder="01" />
          <div style={{gridColumn:'1 / span 2', display:'flex', gap:8}}>
            <button className="btn" type="submit">저장</button>
            {msg && <span style={{opacity:.8}}>{msg}</span>}
          </div>
        </form>
      </div>
    </div>
  );
}
