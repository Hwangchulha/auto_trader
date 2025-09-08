'use client';
import { useEffect, useState } from 'react';
import axios from 'axios';
const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8088';
type Row = { code: string; name?: string };
export default function Watchlist(){
  const [rows, setRows] = useState<Row[]>([]);
  const [code, setCode] = useState('');
  const [name, setName] = useState('');
  const [msg, setMsg] = useState<string|undefined>();
  async function load(){ const r = await axios.get(`${API}/api/symbols`); setRows(r.data || []); }
  useEffect(()=>{ load(); }, []);
  async function add(){
    setMsg(undefined);
    if(!code) { setMsg('종목코드를 입력하세요. 예: KRX:005930'); return; }
    await axios.post(`${API}/api/symbols`, null, { params: { code, name } });
    setCode(''); setName(''); await load();
  }
  async function del(c: string){ await axios.delete(`${API}/api/symbols`, { params: { code: c } }); await load(); }
  async function order(c: string, side: 'buy'|'sell', qty: number, price: number){
    try{
      const body = new URLSearchParams({ symbol: c, side, qty: String(qty), price: String(price) });
      const r = await fetch(`${API}/api/orders`, { method:'POST', headers:{'content-type':'application/x-www-form-urlencoded'}, body });
      const d = await r.json();
      if(r.ok){ alert(side.toUpperCase() + ' 응답: ' + (d?.status || '') + ' / ' + (d?.client_id || '')); }
      else { alert('오류: ' + JSON.stringify(d)); }
    }catch(e:any){ alert('요청 실패: ' + (e?.message || e)); }
  }
  return (
    <div className="row" style={{alignItems:'flex-start'}}>
      <div className="card" style={{flexBasis:'100%'}}>
        <h3>워치리스트</h3>
        <div className="small">형식 예시: <code>KRX:005930</code>, <code>US:NVDA</code></div>
        <div style={{display:'grid', gridTemplateColumns:'1fr 1fr 120px', gap:8, marginTop:8}}>
          <input className="input" placeholder="종목코드 (예: KRX:005930)" value={code} onChange={e=>setCode(e.target.value)} />
          <input className="input" placeholder="이름(선택)" value={name} onChange={e=>setName(e.target.value)} />
          <button className="btn" onClick={add}>추가</button>
        </div>
        {msg && <div className="small" style={{marginTop:6}}>{msg}</div>}
        <table style={{marginTop:12}}>
          <thead><tr><th>종목</th><th>이름</th><th>주문</th><th>삭제</th></tr></thead>
          <tbody>
            {rows.map(r=>{
              let qRef: HTMLInputElement|null = null;
              let pRef: HTMLInputElement|null = null;
              return (
                <tr key={r.code}>
                  <td>{r.code}</td>
                  <td>{r.name || ''}</td>
                  <td>
                    <div style={{display:'flex', gap:6}}>
                      <input ref={(el)=>{ qRef = el }} className="input" placeholder="수량" defaultValue="1" style={{maxWidth:80}} />
                      <input ref={(el)=>{ pRef = el }} className="input" placeholder="가격(0=시장가)" defaultValue="0" style={{maxWidth:140}} />
                      <button className="btn" onClick={()=>order(r.code, 'buy', Number(qRef?.value||'1'), Number(pRef?.value||'0'))}>매수</button>
                      <button className="btn" onClick={()=>order(r.code, 'sell', Number(qRef?.value||'1'), Number(pRef?.value||'0'))}>매도</button>
                    </div>
                  </td>
                  <td><button className="btn" onClick={()=>del(r.code)}>삭제</button></td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
