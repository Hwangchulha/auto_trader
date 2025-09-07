
"use client";
import { useEffect, useState } from "react";
import axios from "axios";
const API = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
export default function WatchlistPage() {
  const [items, setItems] = useState<any[]>([]);
  const [code, setCode] = useState(""); const [name, setName] = useState("");
  const load = async () => setItems((await axios.get(`${API}/api/watchlist`)).data);
  useEffect(()=>{ load(); const t=setInterval(load,4000); return ()=>clearInterval(t); },[]);
  const add = async (e:any) => { e.preventDefault(); if(!code.trim()) return;
    await axios.post(`${API}/api/watchlist`, { code, name }); setCode(""); setName(""); load(); };
  const toggle = async (c:string, active:boolean) => { await axios.patch(`${API}/api/watchlist/${encodeURIComponent(c)}`, { active: !active }); load(); };
  const remove = async (c:string) => { await axios.delete(`${API}/api/watchlist/${encodeURIComponent(c)}`); load(); };
  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold">워치리스트 관리</h1>
      <form onSubmit={add} className="card flex flex-wrap gap-2 items-end">
        <div><div className="label">코드 (예: KRX:005930 또는 AAPL)</div>
          <input value={code} onChange={e=>setCode(e.target.value)} className="input min-w-64" placeholder="KRX:005930 or AAPL"/></div>
        <div><div className="label">이름(선택)</div>
          <input value={name} onChange={e=>setName(e.target.value)} className="input min-w-64" placeholder="Samsung Electronics"/></div>
        <button className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded">추가</button>
      </form>
      <div className="card overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="opacity-70"><tr>
            <th className="text-left p-2">코드</th><th className="text-left p-2">이름</th>
            <th className="text-left p-2">시장</th><th className="text-center p-2">활성</th><th className="text-right p-2">액션</th>
          </tr></thead>
          <tbody>{items.map((it:any)=>(
            <tr key={it.code} className="border-t border-neutral-800">
              <td className="p-2"><a className="underline" href={`/chart/${encodeURIComponent(it.code)}`}>{it.code}</a></td>
              <td className="p-2">{it.name}</td><td className="p-2">{it.market}</td>
              <td className="p-2 text-center"><button onClick={()=>toggle(it.code, it.active)} className={`px-2 py-1 rounded ${it.active?"bg-green-700":"bg-neutral-700"}`}>{it.active?"ON":"OFF"}</button></td>
              <td className="p-2 text-right"><button onClick={()=>remove(it.code)} className="px-2 py-1 rounded bg-red-700 hover:bg-red-600">삭제</button></td>
            </tr>))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
