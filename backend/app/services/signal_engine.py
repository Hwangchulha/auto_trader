
import pandas as pd
from sqlalchemy.orm import Session
from app.models import Symbol, Bar, Signal

def df_from_bars(db: Session, symbol_id: int, tf: str = "1m", limit: int = 500) -> pd.DataFrame:
    rows = db.query(Bar).filter(Bar.symbol_id==symbol_id, Bar.tf==tf).order_by(Bar.ts.desc()).limit(limit).all()
    rows = list(reversed(rows))
    if not rows:
        return pd.DataFrame(columns=["ts","o","h","l","c","v"])
    return pd.DataFrame([{"ts":r.ts, "o":r.o, "h":r.h, "l":r.l, "c":r.c, "v":r.v} for r in rows])

def ma_cross(df: pd.DataFrame, fast: int = 12, slow: int = 26):
    if len(df) < slow + 2: return None
    df = df.copy()
    df["ma_fast"] = df["c"].rolling(fast).mean()
    df["ma_slow"] = df["c"].rolling(slow).mean()
    if df["ma_fast"].iloc[-2] < df["ma_slow"].iloc[-2] and df["ma_fast"].iloc[-1] >= df["ma_slow"].iloc[-1]: return ("BUY", 1.0)
    if df["ma_fast"].iloc[-2] > df["ma_slow"].iloc[-2] and df["ma_fast"].iloc[-1] <= df["ma_slow"].iloc[-1]: return ("SELL", 1.0)
    return None

def rsi_signal(df: pd.DataFrame, period: int = 14, low: float = 30, high: float = 70):
    if len(df) < period + 2: return None
    delta = df["c"].diff()
    up = (delta.clip(lower=0)).rolling(period).mean()
    down = (-delta.clip(upper=0)).rolling(period).mean()
    rs = up / (down + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    if rsi.iloc[-1] < low: return ("BUY", (low - rsi.iloc[-1]) / 100.0)
    if rsi.iloc[-1] > high: return ("SELL", (rsi.iloc[-1] - high) / 100.0)
    return None

def macd_signal(df: pd.DataFrame, fast=12, slow=26, signal=9):
    if len(df) < slow + signal + 2: return None
    ema_fast = df["c"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["c"].ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    sig = macd.ewm(span=signal, adjust=False).mean()
    hist_prev = macd.iloc[-2] - sig.iloc[-2]
    hist_now = macd.iloc[-1] - sig.iloc[-1]
    if hist_prev < 0 and hist_now > 0: return ("BUY", 1.0)
    if hist_prev > 0 and hist_now < 0: return ("SELL", 1.0)
    return None

STRATEGIES = {"MA_CROSS": ma_cross, "RSI": rsi_signal, "MACD": macd_signal}

def run_strategies(db: Session, symbol_code: str, tf: str = "1m") -> list[dict]:
    sym = db.query(Symbol).filter(Symbol.code==symbol_code).first()
    if not sym: return []
    df = df_from_bars(db, sym.id, tf=tf, limit=600)
    outs = []
    for name, fn in STRATEGIES.items():
        s = fn(df)
        if s:
            sig, score = s
            outs.append({"strategy": name, "signal": sig, "score": float(score)})
    if len(df):
        ts = df["ts"].iloc[-1]
        for o in outs:
            db.add(Signal(symbol_id=sym.id, ts=ts, strategy=o["strategy"], signal=o["signal"], score=o["score"]))
        db.commit()
    return outs
