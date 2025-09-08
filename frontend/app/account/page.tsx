'use client';
import { useEffect, useState } from 'react';
import { api } from '../../lib/api';

export default function AccountPage() {
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState<string>('');

  useEffect(()=>{
    api('/api/account/overview').then(setData).catch(e=>setErr(String(e)));
  },[]);

  return (
    <div style={{padding:24}}>
      <h2>계좌 현황</h2>
      {err && <pre style={{color:'crimson'}}>{err}</pre>}
      {data && (
        <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:16}}>
          <div className="card">
            <h4>요약</h4>
            <div>현금잔고: {data.summary?.cash?.toLocaleString?.() ?? data.summary?.cash ?? '-'}</div>
          </div>
          <div className="card">
            <h4>원본 응답</h4>
            <pre style={{maxHeight:400, overflow:'auto'}}>{JSON.stringify(data.raw, null, 2)}</pre>
          </div>
        </div>
      )}
      <style jsx>{`
        .card{ border:1px solid #ddd; border-radius:8px; padding:12px; }
      `}</style>
    </div>
  );
}
