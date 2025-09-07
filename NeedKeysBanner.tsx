'use client';
import { useEffect, useState } from 'react';
import axios from 'axios';
import Link from 'next/link';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function NeedKeysBanner(){
  const [needs, setNeeds] = useState(false);
  useEffect(()=>{
    (async()=>{
      try{
        const r = await axios.get(`${API}/api/settings/runtime`);
        setNeeds(!!r.data?.needs_keys);
      }catch{}
    })();
  },[]);
  if(!needs) return null;
  return (
    <div style={{background:'#78350f', color:'#fff', padding:'8px 12px', textAlign:'center'}}>
      KIS 키가 설정되지 않았습니다. <Link href="/keys" style={{textDecoration:'underline', color:'#fff'}}>여기를 눌러 키 설정</Link>
    </div>
  );
}
