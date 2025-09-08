'use client';
import { useEffect, useState } from 'react';
import axios from 'axios';
import Link from 'next/link';
const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8088';
type Overview = {
  mode: string;
  needs_keys: boolean;
  balances: { krw:{ deposit:number, buying_power:number } };
  positions: { symbol:string, name:string, qty:number, avg_price:number, eval_price:number }[];
  recent_orders: any[];
};
export default function Home() {
  const [ov, setOv] = useState<Overview|undefined>();
  useEffect(()=>{
    const f = async()=>{ const r = await axios.get(`${API}/api/account/overview`); setOv(r.data); };
    f(); const t = setInterval(f, 5000); return ()=> clearInterval(t);
  },[]);
  if(!ov) return <div className="card">로딩 중...</div>;
  return (
    <div className="row" style={{alignItems:'flex-start'}}>
      {ov.needs_keys && <div className="warn">🔑 KIS 키가 설정되지 않았습니다. [설정]에서 저장해 주세요.</div>}
      <div className="card stat"><div>총자산 (KRW)</div><h2>{ov?.balances.krw.deposit?.toLocaleString() ?? 0}</h2></div>
      <div className="card stat"><div>매수가능 (KRW)</div><h2>{ov?.balances.krw.buying_power?.toLocaleString() ?? 0}</h2></div>
      <div className="card stat"><div>모드</div><h2>{ov?.mode}</h2></div>
      <div className="card" style={{flexBasis:'100%'}}>
        <h3>바로가기</h3>
        <Link className="btn" href="/watchlist">워치리스트 열기</Link>
        <span style={{marginLeft:10}} />
        <Link className="btn" href="/account">계좌 상세</Link>
        <span style={{marginLeft:10}} />
        <Link className="btn" href="/settings">설정</Link>
      </div>
    </div>
  );
}
