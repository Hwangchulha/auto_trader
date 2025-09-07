'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import axios from 'axios';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function KeyFab(){
  const [needs, setNeeds] = useState(false);
  useEffect(()=>{
    (async()=>{
      try{
        const r = await axios.get(`${API}/api/settings/runtime`);
        setNeeds(!!r.data?.needs_keys);
      }catch{ /* ignore */ }
    })();
  },[]);

  return (
    <Link href="/keys"
      style={{
        position:'fixed', right:20, bottom:20, zIndex:1000,
        background: needs ? '#d97706' : '#334155', color:'#fff',
        padding:'12px 16px', borderRadius:999, textDecoration:'none',
        boxShadow:'0 6px 18px rgba(0,0,0,.25)', fontWeight:600
      }}>
      🔑 키 설정
    </Link>
  );
}
