'use client';
import { useEffect, useState } from 'react';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8088';

type Sym = { code:string, name:string };

export default function Watchlist(){
  const [syms, setSyms] = useState<Sym[]>([]);
  const [code, setCode] = useState('KRX:005930');
  const [name, setName] = useState('');
  const [qty, setQty]   = useState(1);
  const [price, setPrice] = useState<number | ''>('');
  const [side, setSide] = useState<'buy'|'sell'>('buy');
  const [msg, setMsg] = useState<string|undefined>();

  async function load(){
    const r = await fetch(`${API}/api/symbols`, { cache:'no-store' });
    setSyms(await r.json());
  }
  useEffect(()=>{ load(); }, []);

  async function add(e:any){
    e.preventDefault();
    const u = new URL(`${API}/api/symbols`);
    u.searchParams.set('code', code);
    if(name) u.searchParams.set('name', name);
    const r = await fetch(u.toString(), { method:'POST' });
    if(!r.ok) setMsg(await r.text()); else { setMsg('추가됨'); await load(); }
  }

  async function del(c:string){
    const u = new URL(`${API}/api/symbols`);
    u.searchParams.set('code', c);
    await fetch(u.toString(), { method:'DELETE' });
    await load();
  }

  async function trade(c:string){
    setMsg(undefined);
    const body = new URLSearchParams();
    body.set('symbol', c);
    body.set('side', side);
    body.set('qty', String(qty));
    body.set('price', price === '' ? '0' : String(price));
    const r = await fetch(`${API}/api/orders`, { method:'POST', headers:{'content-type':'application/x-www-form-urlencoded'}, body });
    const j = await r.json();
    if(!r.ok || j.status === 'rejected'){
      setMsg(`주문 실패: ${JSON.stringify(j.kis_response || j)}`);
    } else {
      setMsg(`주문 전송: ${j.client_id}`);
    }
  }

  return (
    <div className="row" style={{gap:16}}>
      <div className="card" style={{flexBasis:'100%'}}>
        <h3>워치리스트</h3>
        <form onSubmit={add} style={{display:'grid', gridTemplateColumns:'1fr 1fr 120px', gap:8, marginBottom:12}}>
          <input className="input" value={code} onChange={e=>setCode(e.target.value)} placeholder="KRX:005930 / US:NVDA" />
          <input className="input" value={name} onChange={e=>setName(e.target.value)} placeholder="이름(선택)" />
          <button className="btn" type="submit">추가</button>
        </form>
        <table className="table">
          <thead><tr><th>코드</th><th>이름</th><th style={{width:260}}>주문</th><th style={{width:120}}></th></tr></thead>
          <tbody>
            {syms.map(s=>(
              <tr key={s.code}>
                <td>{s.code}</td>
                <td>{s.name}</td>
                <td>
                  <div style={{display:'flex', gap:8, alignItems:'center'}}>
                    <select value={side} onChange={e=>setSide(e.target.value as any)}>
                      <option value="buy">매수</option>
                      <option value="sell">매도</option>
                    </select>
                    <input className="input" type="number" value={qty} onChange={e=>setQty(parseInt(e.target.value||'0',10))} style={{width:80}} placeholder="수량" />
                    <input className="input" type="number" value={price} onChange={e=>setPrice(e.target.value===''? '' : Number(e.target.value))} style={{width:100}} placeholder="가격(0=시장가)" />
                    <button className="btn" onClick={()=>trade(s.code)}>전송</button>
                  </div>
                </td>
                <td><button className="btn-danger" onClick={()=>del(s.code)}>삭제</button></td>
              </tr>
            ))}
          </tbody>
        </table>
        {msg && <div style={{marginTop:8, opacity:.9}}>{msg}</div>}
      </div>
    </div>
  );
}
