
"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import CandleChart from "../../components/Chart";
const API = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
export default function SymbolChart({ params }: { params: { symbol: string }}) {
  const symbol = decodeURIComponent(params.symbol);
  const [bars, setBars] = useState<any[]>([]);
  const [signals, setSignals] = useState<any[]>([]);
  const [side, setSide] = useState<string>("buy");
  const [qty, setQty] = useState<number>(1);
  const [submitting, setSubmitting] = useState(false);
  const [toast, setToast] = useState<string|null>(null);

  useEffect(() => {
    const f = async () => {
      const b = await axios.get(`${API}/api/bars/${encodeURIComponent(symbol)}?tf=1m&limit=500`);
      setBars(b.data.map((x:any)=>({ time: new Date(x.ts).getTime()/1000, open:x.o, high:x.h, low:x.l, close:x.c })));
      setSignals((await axios.get(`${API}/api/signals/${encodeURIComponent(symbol)}`)).data);
    };
    f(); const t = setInterval(f, 4000); return () => clearInterval(t);
  }, [symbol]);

  async function submit(e: any) {
    e.preventDefault();
    if (!qty || qty <= 0) { setToast("수량을 확인하세요."); setTimeout(()=>setToast(null), 2000); return; }
    setSubmitting(true);
    try {
      const { data } = await axios.post(`${API}/api/orders`, { symbol, side, qty: Number(qty) });
      setToast(`주문 완료: ${data.status} @ ${data.price ?? "-"}`);
    } catch (err:any) {
      const msg = err?.response?.data?.detail || err.message;
      setToast(`주문 실패: ${msg}`);
    } finally {
      setSubmitting(false);
      setTimeout(()=>setToast(null), 2500);
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">{symbol}</h1>
        <div className="space-x-2">
          {signals[0]?.signal === "BUY" && <span className="badge badge-green">BUY</span>}
          {signals[0]?.signal === "SELL" && <span className="badge badge-red">SELL</span>}
          {!signals[0] && <span className="badge badge-amber">NO SIGNAL</span>}
        </div>
      </div>
      <div className="card"><CandleChart data={bars} /></div>
      <div className="card">
        <form onSubmit={submit} className="flex flex-wrap items-end gap-2">
          <div><label className="label">Side</label>
            <select value={side} onChange={e=>setSide(e.target.value)} className="ml-2 bg-neutral-800 p-2 rounded">
              <option value="buy">매수</option><option value="sell">매도</option>
            </select></div>
          <div><label className="label">수량</label>
            <input value={qty} onChange={e=>setQty(parseFloat(e.target.value))} className="ml-2 bg-neutral-800 p-2 rounded w-20" /></div>
          <button disabled={submitting} className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded">
            {submitting ? "전송 중..." : "주문 전송"}
          </button>
          <a href="/account" className="ml-2 underline text-sm opacity-80">계좌 보기</a>
        </form>
      </div>
      {toast && <div className="fixed bottom-4 right-4 card">{toast}</div>}
    </div>
  );
}
