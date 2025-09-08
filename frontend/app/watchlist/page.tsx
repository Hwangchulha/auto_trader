'use client';
import { useEffect, useMemo, useRef, useState } from 'react';
import { api } from '../../lib/api';

type Row = { code: string; name?: string };

const LS_KEY = 'watchlist_rows';

export default function WatchlistPage(){
  const [rows, setRows] = useState<Row[]>([]);
  const codeRef = useRef<HTMLInputElement>(null);
  const nameRef = useRef<HTMLInputElement>(null);

  useEffect(()=>{
    try{
      const saved = localStorage.getItem(LS_KEY);
      if(saved) setRows(JSON.parse(saved));
    }catch{}
  },[]);

  useEffect(()=>{
    try{
      localStorage.setItem(LS_KEY, JSON.stringify(rows));
    }catch{}
  },[rows]);

  const add = ()=>{
    const code = codeRef.current?.value?.trim()?.toUpperCase() || '';
    const name = nameRef.current?.value?.trim() || '';
    if(!code) return;
    setRows(prev=>{
      if(prev.some(r=>r.code===code)) return prev;
      return [...prev, {code, name}];
    });
    if(codeRef.current) codeRef.current.value='';
    if(nameRef.current) nameRef.current.value='';
  };

  const remove = (code: string)=> setRows(prev=>prev.filter(r=>r.code!==code));

  const order = async (code: string, side: 'buy'|'sell', qty: number, price: number)=>{
    const body = new URLSearchParams();
    body.set('symbol', code);
    body.set('side', side);
    body.set('qty', String(qty));
    body.set('price', String(price));
    const res = await fetch('/api/orders', {
      method: 'POST',
      headers: {'Content-Type':'application/x-www-form-urlencoded'},
      body
    });
    const json = await res.json();
    if(!res.ok) throw new Error(JSON.stringify(json));
    alert(`주문 요청: ${json.message?.text || json.status}`);
  };

  return (
    <div style={{padding:24}}>
      <h2>위시리스트</h2>
      <div style={{display:'flex', gap:8, marginBottom:16}}>
        <input ref={codeRef} placeholder="종목코드 (예: KRX:005930)" className="input" style={{minWidth:240}}/>
        <input ref={nameRef} placeholder="메모/별칭" className="input" style={{minWidth:180}}/>
        <button className="btn" onClick={add}>추가</button>
      </div>
      <table style={{width:'100%', borderCollapse:'collapse'}}>
        <thead>
          <tr>
            <th style={{textAlign:'left', borderBottom:'1px solid #ddd', padding:'8px 4px'}}>코드</th>
            <th style={{textAlign:'left', borderBottom:'1px solid #ddd', padding:'8px 4px'}}>이름</th>
            <th style={{textAlign:'left', borderBottom:'1px solid #ddd', padding:'8px 4px'}}>주문</th>
            <th style={{textAlign:'left', borderBottom:'1px solid #ddd', padding:'8px 4px'}}>관리</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(r=>{
            const qRef = useRef<HTMLInputElement>(null);
            const pRef = useRef<HTMLInputElement>(null);
            return (
              <tr key={r.code}>
                <td style={{padding:'8px 4px'}}>{r.code}</td>
                <td style={{padding:'8px 4px'}}>{r.name || '-'}</td>
                <td style={{padding:'8px 4px'}}>
                  <div style={{display:'flex', gap:6}}>
                    <input ref={qRef} className="input" placeholder="수량" defaultValue="1" style={{maxWidth:80}} />
                    <input ref={pRef} className="input" placeholder="가격(0=시장가)" defaultValue="0" style={{maxWidth:140}} />
                    <button className="btn" onClick={()=>order(r.code, 'buy', Number(qRef.current?.value||'1'), Number(pRef.current?.value||'0'))}>매수</button>
                    <button className="btn" onClick={()=>order(r.code, 'sell', Number(qRef.current?.value||'1'), Number(pRef.current?.value||'0'))}>매도</button>
                  </div>
                </td>
                <td style={{padding:'8px 4px'}}>
                  <button className="btn" onClick={()=>remove(r.code)}>삭제</button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      <style jsx>{`
        .btn{
          padding:6px 10px; border:1px solid #888; border-radius:6px; background:#fff;
        }
        .btn:hover{ background:#f5f5f5; }
        .input{
          padding:6px 8px; border:1px solid #ccc; border-radius:6px;
        }
      `}</style>
    </div>
  )
}
