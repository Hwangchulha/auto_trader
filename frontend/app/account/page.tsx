'use client';
import { useEffect, useState } from 'react';
import axios from 'axios';
const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8088';

export default function Account(){
  const [data, setData] = useState<any|undefined>();

  useEffect(()=>{
    const f = async ()=>{
      const r = await axios.get(`${API}/api/account/overview`);
      setData(r.data);
    };
    f(); const t = setInterval(f, 5000); return ()=> clearInterval(t);
  },[]);

  if(!data) return <div className="card">로딩 중...</div>;
  return (
    <div className="row" style={{gap:16}}>
      <div className="card" style={{flex:1}}>
        <h3>보유 종목</h3>
        <table className="table">
          <thead><tr><th>심볼</th><th>수량</th><th>평단</th><th>평가</th></tr></thead>
          <tbody>
            {data.positions.map((p:any)=>(
              <tr key={p.symbol}><td>{p.symbol}</td><td>{p.qty}</td><td>{p.avg_price}</td><td>{p.eval_price}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="card" style={{flex:1}}>
        <h3>최근 주문</h3>
        <ul>{data.recent_orders.map((o:any)=>(
          <li key={o.client_id}>{o.created_at} {o.side?.toUpperCase?.() ?? ''} {o.symbol} x {o.qty} @ {o.price} [{o.status}]</li>
        ))}</ul>
      </div>
    </div>
  );
}
