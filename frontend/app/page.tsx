// frontend/app/page.tsx
'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { api } from '../lib/api';

export default function Home() {
  const [health, setHealth] = useState<any>(null);
  const [error, setError] = useState<string>('');

  useEffect(()=>{
    api('/api/diag/health').then(setHealth).catch(e=>setError(String(e)));
  },[]);

  return (
    <div style={{padding:24}}>
      <h1 style={{marginBottom:16}}>KIS Auto Trader</h1>
      <div style={{display:'flex', gap:8, marginBottom:20}}>
        <Link className="btn" href="/watchlist">위시리스트</Link>
        <Link className="btn" href="/settings">설정/키 입력</Link>
        <Link className="btn" href="/account">계좌 현황</Link>
      </div>
      <div style={{padding:12, border:'1px solid #ddd', borderRadius:8}}>
        <h3>백엔드 상태</h3>
        {error ? <pre style={{color:'crimson'}}>{error}</pre> : <pre>{JSON.stringify(health, null, 2)}</pre>}
      </div>
      <style jsx>{`
        .btn{
          display:inline-block; padding:8px 12px; border:1px solid #888; border-radius:6px;
          text-decoration:none;
        }
        .btn:hover{ background:#f3f3f3; }
      `}</style>
    </div>
  );
}
