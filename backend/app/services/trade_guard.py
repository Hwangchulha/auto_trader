
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import Symbol, Position, Order, Bar, Signal
from app.services.runtime_settings import get_runtime

def _aware(dt):
    if dt is None: return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)

def _bars_elapsed_minutes(last_bar_ts, ref_ts):
    lb = _aware(last_bar_ts); rf = _aware(ref_ts)
    if rf is None or lb is None: return 1e9
    return max(0.0, (lb - rf).total_seconds() / 60.0)

class TradeGuard:
    def __init__(self, db: Session, tf: str = "1m", params: dict|None=None):
        self.db = db; self.tf = tf
        self.params = params or get_runtime(db)

    def _last_bar_ts(self, sym_id: int):
        last = self.db.query(Bar).filter(Bar.symbol_id==sym_id, Bar.tf==self.tf).order_by(Bar.ts.desc()).first()
        return _aware(last.ts) if last else None

    def _confirm(self, sym_id: int, want_signal: str, need: int) -> bool:
        if need <= 1: return True
        rows = self.db.query(Signal).filter(
            Signal.symbol_id==sym_id,
            Signal.signal==("BUY" if want_signal=="buy" else "SELL")
        ).order_by(Signal.ts.desc()).limit(need*3).all()
        uniq = []
        seen = set()
        for r in rows:
            ts = _aware(r.ts)
            if ts not in seen:
                seen.add(ts); uniq.append(ts)
            if len(uniq) >= need: return True
        return False

    def _daily_count(self, sym_id: int) -> int:
        now = datetime.now(timezone.utc)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.db.query(Order).filter(Order.symbol_id==sym_id, Order.created_at >= start).count()

    def allow(self, symbol_code: str, side: str):
        p = self.params
        sym = self.db.query(Symbol).filter(Symbol.code==symbol_code).first()
        if not sym: return False, "symbol_missing"
        pos = self.db.query(Position).filter(Position.symbol_id==sym.id).first()
        last_order = self.db.query(Order).filter(Order.symbol_id==sym.id).order_by(Order.created_at.desc()).first()
        last_bar_ts = self._last_bar_ts(sym.id)

        if p.get("NO_PYRAMIDING", True) and side=="buy" and pos and pos.qty > 0:
            return False, "no_pyramiding"
        if side=="sell" and (not pos or pos.qty <= 0):
            return False, "flat_no_sell"

        if p.get("DAILY_TRADE_LIMIT", 0) and self._daily_count(sym.id) >= p["DAILY_TRADE_LIMIT"]:
            return False, "daily_limit"

        cd = int(p.get("COOLDOWN_BARS", 0) or 0)
        if last_order and cd > 0:
            elapsed = _bars_elapsed_minutes(last_bar_ts, _aware(last_order.created_at))
            if elapsed < cd:
                return False, f"cooldown({elapsed:.1f}m<{cd})"

        if not self._confirm(sym.id, side, int(p.get("CONFIRM_BARS", 1))):
            return False, "need_confirmation"

        hyst = float(p.get("HYSTERESIS_PCT", 0.0) or 0.0)
        if pos and pos.qty > 0 and side == "sell" and hyst > 0:
            last_close = self.db.query(Bar).filter(Bar.symbol_id==sym.id).order_by(Bar.ts.desc()).first()
            if last_close and pos.avg_price > 0:
                change = abs(last_close.c / pos.avg_price - 1.0)
                if change < hyst:
                    return False, "hysteresis_guard"

        return True, "ok"
