'use client';

import { useState } from 'react';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function OrderPage(){
  const [symbol, setSymbol] = useState('KRX:005930');
  const [side, setSide] = useState<'buy'|'sell'>('buy');
  const [qty, setQty] = useState(1);
  const [price, setPrice] = useState<number | ''>(''); // 빈값=시장가
  const [res, setRes] = useState<any>(null);

  const submit = async (e:any)=>{
    e.preventDefault();
    const form = new URLSearchParams();
    form.append('symbol', symbol);
    form.append('side', side);
    form.append('qty', String(qty));
    form.append('price', price === '' ? '' : String(price));
    const r = await fetch(`${API}/api/orders`, { method:"POST", headers:{'Content-Type': 'application/x-www-form-urlencoded'}, body: form.toString() });
    const j = await r.json();
    setRes(j);
  };

  return (
    <div>
      <h2>수동 주문 테스트</h2>
      <form onSubmit={submit} style={{display:"grid", gridTemplateColumns:"160px 1fr", gap:8, maxWidth:600}}>
        <label>종목</label>
        <input value={symbol} onChange={e=>setSymbol(e.target.value)} />
        <label>방향</label>
        <select value={side} onChange={e=>setSide(e.target.value as any)}>
          <option value="buy">매수</option>
          <option value="sell">매도</option>
        </select>
        <label>수량</label>
        <input type="number" value={qty} onChange={e=>setQty(Number(e.target.value))} />
        <label>가격</label>
        <input placeholder="비우면 시장가" value={price as any} onChange={e=>setPrice(e.target.value===''? '': Number(e.target.value))} />
        <div style={{gridColumn:"1 / span 2", marginTop:8}}>
          <button type="submit">전송</button>
        </div>
      </form>

      {res && <pre style={{whiteSpace:"pre-wrap", background:"#fafafa", padding:12, border:"1px solid #eee", marginTop:16}}>{JSON.stringify(res, null, 2)}</pre>}
    </div>
  );
}
