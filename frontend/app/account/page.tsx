
"use client";
import { useEffect, useState } from "react";
import axios from "axios";
const API = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

function fmtKST(s?: string) {
  if (!s) return "-";
  const d = new Date(s);
  return d.toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });
}

export default function AccountPage() {
  const [ov, setOv] = useState<any>(null);
  const [showRaw, setShowRaw] = useState(false);
  useEffect(() => {
    const f = async () => { setOv((await axios.get(`${API}/api/account/overview`)).data); };
    f(); const t = setInterval(f, 5000); return () => clearInterval(t);
  }, []);
  if (!ov) return <div className="card">로딩 중...</div>;

  const cashK = Math.round(ov?.balances?.krw?.cash || 0).toLocaleString();
  const cashU = Math.round(ov?.balances?.usd?.cash || 0).toLocaleString();
  const totK  = Math.round(ov?.equity?.total_krw || 0).toLocaleString();
  const totU  = Math.round(ov?.equity?.total_usd || 0).toLocaleString();
  const fx    = ov?.fx?.usdkrw || 0;
  const bpK   = Math.round(ov?.balances?.krw?.buying_power || 0).toLocaleString();
  const depK  = ov?.balances?.krw?.deposit!=null ? Math.round(ov.balances.krw.deposit).toLocaleString() : "-";
  const wdrK  = ov?.balances?.krw?.withdrawable!=null ? Math.round(ov.balances.krw.withdrawable).toLocaleString() : "-";

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold">계좌 정보</h1>

      <section className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <div className="card"><div className="text-xs opacity-60">모드</div><div className="text-2xl font-bold">{ov.mode}</div></div>
        <div className="card"><div className="text-xs opacity-60">총자산 (KRW)</div><div className="text-2xl font-bold">{totK}</div></div>
        <div className="card"><div className="text-xs opacity-60">총자산 (USD)</div><div className="text-2xl font-bold">{totU}</div></div>
        <div className="card"><div className="text-xs opacity-60">USD/KRW</div><div className="text-2xl font-bold">{fx}</div></div>
        <div className="card text-xs">
          <div className="opacity-60 mb-1">Guard</div>
          <div>cooldown: <b>{ov?.guard?.cooldown_bars}</b> bars</div>
          <div>confirm: <b>{ov?.guard?.confirm_bars}</b> bars</div>
          <div>hysteresis: <b>{(ov?.guard?.hysteresis_pct*100).toFixed(2)}%</b></div>
          <div>daily limit: <b>{ov?.guard?.daily_trade_limit}</b></div>
          <div>no pyramiding: <b>{ov?.guard?.no_pyramiding ? "ON":"OFF"}</b></div>
          <div>auto trade: <b>{ov?.guard?.auto_trade ? "ON":"OFF"}</b></div>
        </div>
        <div className="card"><a className="underline" href="/settings">설정 변경</a></div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="card">
          <div className="text-sm font-semibold mb-2">현금 (Cash)</div>
          <div className="flex gap-6 text-sm">
            <div><div className="opacity-60">KRW</div><div className="text-xl font-bold">{cashK}</div></div>
            <div><div className="opacity-60">USD</div><div className="text-xl font-bold">{cashU}</div></div>
          </div>
          <div className="text-xs opacity-60 mt-2">초기 현금은 .env 기본값이며, 환율은 설정에서 조정 가능.</div>
        </div>
        <div className="card">
          <div className="text-sm font-semibold mb-2">KIS (국내) — 예수금/주문가능</div>
          <div className="text-sm">주문가능(KRW): <b>{bpK}</b></div>
          <div className="text-sm">예수금(KRW): <b>{depK}</b></div>
          <div className="text-sm">출금가능(KRW): <b>{wdrK}</b></div>
        </div>
      </section>

      <section className="card overflow-x-auto">
        <div className="flex items-center justify-between mb-2">
          <div className="text-sm font-semibold">포지션</div>
          <a className="underline text-xs" href="/settings">Guard 조정</a>
        </div>
        <table className="table">
          <thead><tr>
            <th className="th">심볼</th><th className="th">수량</th><th className="th">평단</th><th className="th">현재가</th><th className="th">평가</th><th className="th">평가손익</th><th className="th">수익률</th>
          </tr></thead>
          <tbody>
          {ov.positions.map((p:any)=>(
            <tr key={p.code} className="border-t border-neutral-800">
              <td className="td">{p.code}</td>
              <td className="td">{p.qty}</td>
              <td className="td">{p.avg_price.toLocaleString()}</td>
              <td className="td">{p.last_price.toLocaleString()}</td>
              <td className="td">{Math.round(p.value).toLocaleString()}</td>
              <td className="td">{Math.round(p.unrealized_pl).toLocaleString()}</td>
              <td className="td">{p.unrealized_pl_pct.toFixed(2)}%</td>
            </tr>
          ))}
          {ov.positions.length===0 && <tr><td className="td" colSpan={7}>포지션 없음</td></tr>}
          </tbody>
        </table>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="card overflow-x-auto">
          <div className="text-sm font-semibold mb-2">최근 주문</div>
          <table className="table">
            <thead><tr><th className="th">시간(KST)</th><th className="th">심볼</th><th className="th">Side</th><th className="th">수량</th><th className="th">가격</th><th className="th">상태</th></tr></thead>
            <tbody>
              {ov.orders_recent.map((o:any)=>(
                <tr key={o.client_id} className="border-t border-neutral-800">
                  <td className="td">{fmtKST(o.created_at)}</td><td className="td">{o.code}</td><td className="td">{o.side}</td>
                  <td className="td">{o.qty}</td><td className="td">{o.price ?? "-"}</td><td className="td">{o.status}</td>
                </tr>
              ))}
              {ov.orders_recent.length===0 && <tr><td className="td" colSpan={6}>주문 없음</td></tr>}
            </tbody>
          </table>
        </div>
        <div className="card overflow-x-auto">
          <div className="text-sm font-semibold mb-2">최근 체결</div>
          <table className="table">
            <thead><tr><th className="th">시간(KST)</th><th className="th">심볼</th><th className="th">Side</th><th className="th">수량</th><th className="th">가격</th></tr></thead>
            <tbody>
              {ov.executions_recent.map((e:any, idx:number)=>(
                <tr key={idx} className="border-t border-neutral-800">
                  <td className="td">{fmtKST(e.ts)}</td><td className="td">{e.code}</td><td className="td">{e.side}</td>
                  <td className="td">{e.qty}</td><td className="td">{e.price}</td>
                </tr>
              ))}
              {ov.executions_recent.length===0 && <tr><td className="td" colSpan={5}>체결 없음</td></tr>}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
