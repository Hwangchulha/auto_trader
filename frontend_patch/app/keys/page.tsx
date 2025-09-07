'use client';
import { useEffect, useState } from 'react';
import axios from 'axios';

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

  useEffect(()=>{
    (async()=>{
      try{
        const r = await axios.get(`${API}/api/keys`);
        setM(r.data);
        if(r.data.exists){
          setEnv(r.data.kis_env || 'vts');
          setAcnt(r.data.acnt_prdt_cd || '01');
        }
      }catch(e:any){ setMsg(e?.message); }
    })();
  },[]);

  const save = async (e:any)=>{
    e.preventDefault();
    setSaving(true);
    setMsg(undefined);
    try{
      await axios.post(`${API}/api/keys`, { kis_env, app_key, app_secret, cano, acnt_prdt_cd: acnt });
      setMsg('저장 완료. (다음 호출부터 반영됩니다)');
      const r = await axios.get(`${API}/api/keys`);
      setM(r.data);
      setAppKey(''); setAppSecret(''); setCano('');
    }catch(err:any){
      setMsg(err?.message || '저장 실패');
    }finally{
      setSaving(false);
    }
  };

  return (
    <div style={{maxWidth:720, margin:"24px auto"}}>
      <h2>KIS 키 설정</h2>
      <p style={{opacity:.8}}>모의(VTS)/실전(PROD) 앱키/시크릿/계좌를 입력해 저장합니다. DB에 저장되며, 보안상 화면에는 마스킹된 값만 표시됩니다.</p>

      <div style={{border:"1px solid #222", padding:16, borderRadius:8, marginTop:12}}>
        <div style={{display:"grid", gridTemplateColumns:"160px 1fr", gap:8}}>
          <label>현재 저장 상태</label>
          <div>{m.exists ? "저장됨" : "없음"}</div>
          {m.exists && <>
            <label>환경</label><div>{m.kis_env}</div>
            <label>앱키</label><div>{m.app_key}</div>
            <label>시크릿</label><div>{m.app_secret}</div>
            <label>계좌</label><div>{m.cano}</div>
            <label>상품코드</label><div>{m.acnt_prdt_cd}</div>
          </>}
        </div>
      </div>

      <form onSubmit={save} style={{border:"1px solid #222", padding:16, borderRadius:8, marginTop:16, display:"grid", gridTemplateColumns:"160px 1fr", gap:8}}>
        <label>환경</label>
        <select value={kis_env} onChange={e=>setEnv(e.target.value as 'vts'|'prod')}>
          <option value="vts">모의(VTS)</option>
          <option value="prod">실전(PROD)</option>
        </select>
        <label>앱키</label>
        <input value={app_key} onChange={e=>setAppKey(e.target.value)} placeholder="발급받은 App Key" />
        <label>시크릿</label>
        <input value={app_secret} onChange={e=>setAppSecret(e.target.value)} placeholder="발급받은 App Secret" />
        <label>계좌(앞 8자리)</label>
        <input value={cano} onChange={e=>setCano(e.target.value)} placeholder="12345678" />
        <label>상품코드</label>
        <input value={acnt} onChange={e=>setAcnt(e.target.value)} placeholder="01" />
        <div style={{gridColumn:"1 / span 2", marginTop:8}}>
          <button type="submit" disabled={saving}>{saving ? "저장 중..." : "저장"}</button>
          {msg && <span style={{marginLeft:12, opacity:.8}}>{msg}</span>}
        </div>
      </form>

      <div style={{marginTop:16, opacity:.8}}>
        <b>TIP:</b> 저장 직후에는 토큰/해시키가 갱신되도록 자동 초기화됩니다. 이후 주문/조회 호출에서 새로운 키가 사용됩니다.
      </div>
    </div>
  );
}
