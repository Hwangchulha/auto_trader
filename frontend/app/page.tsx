'use client';
import { useEffect, useState } from 'react';
import axios from 'axios';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

type Overview = {
  mode: string;
  balances: { krw:{ deposit:number, buying_power:number } };
  positions: { symbol:string, name:string, qty:number, avg_price:number, eval_price:number }[];
  recent_orders: any[];
};

export default function Home() {
  const [ov, setOv] = useState<Overview|undefined>();
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string|undefined>();

  useEffect(()=>{
    const f = async()=>{
      try{
        const r = await axios.get(`${API}/api/account/overview`);
        setOv(r.data);
      }catch(e:any){ setErr(e?.message); }
      finally{ setLoading(false); }
    };
    f(); const t = setInterval(f, 5000); return ()=> clearInterval(t);
  },[]);

  return (
    <div className="row">
      <div className="card stat">
        <div>총자산 (KRW)</div>
        <h2>{ov?.balances.krw.deposit?.toLocaleString() ?? 0}</h2>
      </div>
      <div className="card stat">
        <div>매수가능 (KRW)</div>
        <h2>{ov?.balances.krw.buying_power?.toLocaleString() ?? 0}</h2>
      </div>
      <div className="card stat">
        <div>모드</div>
        <h2>{ov?.mode ?? '-'}</h2>
      </div>
    </div>
  );
}
