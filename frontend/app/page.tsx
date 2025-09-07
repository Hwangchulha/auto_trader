
"use client";
import { useEffect, useState } from "react";
import axios from "axios";
const API = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
export default function Page() {
  const [overview, setOverview] = useState<any>(null);
  const [symbols, setSymbols] = useState<any[]>([]);
  useEffect(() => {
    const f = async () => {
      setOverview((await axios.get(`${API}/api/account/overview`)).data);
      setSymbols((await axios.get(`${API}/api/symbols`)).data);
    };
    f(); const t = setInterval(f, 5000); return () => clearInterval(t);
  }, []);
  const krw = overview?.balances?.krw?.cash ?? 0;
  const usd = overview?.balances?.usd?.cash ?? 0;
  const tot_krw = overview?.equity?.total_krw ?? 0;
  const tot_usd = overview?.equity?.total_usd ?? 0;
  return (
    <div className="space-y-6">
      <section className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <div className="card"><div className="text-xs opacity-60">총자산 (KRW)</div>
          <div className="text-2xl font-bold">{Math.round(tot_krw).toLocaleString()}</div></div>
        <div className="card"><div className="text-xs opacity-60">총자산 (USD)</div>
          <div className="text-2xl font-bold">{Math.round(tot_usd).toLocaleString()}</div></div>
        <div className="card"><div className="text-xs opacity-60">현금 (KRW)</div>
          <div className="text-2xl font-bold">{Math.round(krw).toLocaleString()}</div></div>
        <div className="card"><div className="text-xs opacity-60">현금 (USD)</div>
          <div className="text-2xl font-bold">{Math.round(usd).toLocaleString()}</div></div>
        <div className="card text-xs">
          <div className="opacity-60 mb-1">Guard</div>
          <div>cooldown: <b>{overview?.guard?.cooldown_bars}</b> bars</div>
          <div>confirm: <b>{overview?.guard?.confirm_bars}</b> bars</div>
          <div>hysteresis: <b>{(overview?.guard?.hysteresis_pct*100).toFixed(2)}%</b></div>
          <div>daily limit: <b>{overview?.guard?.daily_trade_limit}</b></div>
          <div>no pyramiding: <b>{overview?.guard?.no_pyramiding ? "ON":"OFF"}</b></div>
          <div>auto trade: <b>{overview?.guard?.auto_trade ? "ON":"OFF"}</b></div>
        </div>
        <div className="card"><a className="underline" href="/settings">설정 변경</a></div>
      </section>
      <section className="card">
        <div className="flex items-center justify-between mb-2">
          <h2 className="font-semibold">워치리스트(활성)</h2>
          <a className="text-xs underline" href="/account">계좌 상세 보기</a>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {symbols.map((s) => (
            <a key={s.code} href={`/chart/${encodeURIComponent(s.code)}`} className="card hover:bg-neutral-800/40 transition">
              <div className="text-sm opacity-70">{s.market}</div>
              <div className="text-lg font-semibold">{s.code}</div>
              <div className="text-xs opacity-60">{s.name}</div>
            </a>
          ))}
        </div>
      </section>
    </div>
  );
}
