
"use client";
import { useEffect, useState } from "react";
import axios from "axios";

const API = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

type Runtime = {
  AUTO_TRADE: boolean;
  COOLDOWN_BARS: number;
  CONFIRM_BARS: number;
  HYSTERESIS_PCT: number;
  DAILY_TRADE_LIMIT: number;
  NO_PYRAMIDING: boolean;
  FX_USDKRW: number;
};

export default function SettingsPage() {
  const [cfg, setCfg] = useState<Runtime | null>(null);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<string>("");

  async function load() {
    const r = await axios.get(`${API}/api/settings/runtime`);
    setCfg(r.data);
  }

  useEffect(() => { load(); }, []);

  async function save() {
    if (!cfg) return;
    setSaving(true);
    try {
      await axios.put(`${API}/api/settings/runtime`, cfg);
      setMsg("저장되었습니다.");
      setTimeout(()=>setMsg(""), 2000);
    } catch (e:any) {
      setMsg("저장 실패: " + (e?.response?.data?.detail || e.message));
    } finally {
      setSaving(false);
    }
  }

  function upd<K extends keyof Runtime>(key: K, val: Runtime[K]) {
    setCfg((c) => (c ? { ...c, [key]: val } as Runtime : c));
  }

  if (!cfg) return <div className="card">로딩 중...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold">설정</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="card space-y-3">
          <div className="text-sm font-semibold">자동매매</div>
          <div className="flex items-center gap-3">
            <label className="label">AUTO_TRADE</label>
            <input type="checkbox" checked={cfg.AUTO_TRADE} onChange={e=>upd("AUTO_TRADE", e.target.checked)} />
          </div>
          <div className="text-xs opacity-60">끄면 신호만 기록하고 실제 주문은 내지 않습니다.</div>
        </div>

        <div className="card space-y-3">
          <div className="text-sm font-semibold">환율</div>
          <label className="label">FX_USDKRW</label>
          <input className="input" type="number" step="0.01" value={cfg.FX_USDKRW} onChange={e=>upd("FX_USDKRW", parseFloat(e.target.value))} />
          <div className="text-xs opacity-60">총자산(원화/달러) 환산에 사용.</div>
        </div>
      </div>

      <div className="card space-y-3">
        <div className="text-sm font-semibold">과매매 방지(Trade Guard)</div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="label">COOLDOWN_BARS</label>
            <input className="input" type="number" min={0} step={1} value={cfg.COOLDOWN_BARS} onChange={e=>upd("COOLDOWN_BARS", parseInt(e.target.value||"0"))} />
            <div className="text-xs opacity-60 mt-1">최근 체결 후 최소 대기 바 수</div>
          </div>
          <div>
            <label className="label">CONFIRM_BARS</label>
            <input className="input" type="number" min={1} step={1} value={cfg.CONFIRM_BARS} onChange={e=>upd("CONFIRM_BARS", parseInt(e.target.value||"1"))} />
            <div className="text-xs opacity-60 mt-1">같은 방향 신호가 연속 M바일 때만</div>
          </div>
          <div>
            <label className="label">HYSTERESIS_PCT</label>
            <input className="input" type="number" min={0} step="0.001" value={cfg.HYSTERESIS_PCT} onChange={e=>upd("HYSTERESIS_PCT", parseFloat(e.target.value||"0"))} />
            <div className="text-xs opacity-60 mt-1">반대매매 허용 최소 변동률(예: 0.003=0.3%)</div>
          </div>
          <div>
            <label className="label">DAILY_TRADE_LIMIT</label>
            <input className="input" type="number" min={0} step={1} value={cfg.DAILY_TRADE_LIMIT} onChange={e=>upd("DAILY_TRADE_LIMIT", parseInt(e.target.value||"0"))} />
            <div className="text-xs opacity-60 mt-1">심볼당 일일 거래 한도</div>
          </div>
          <div className="flex items-center gap-3">
            <label className="label">NO_PYRAMIDING</label>
            <input type="checkbox" checked={cfg.NO_PYRAMIDING} onChange={e=>upd("NO_PYRAMIDING", e.target.checked)} />
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <button onClick={save} disabled={saving} className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded">
          {saving ? "저장 중..." : "저장"}
        </button>
        <div className="text-sm">{msg}</div>
      </div>
    </div>
  );
}
