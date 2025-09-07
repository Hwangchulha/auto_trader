
from sqlalchemy.orm import Session
from app.models import Symbol, Bar
import pandas as pd
from sklearn.linear_model import LogisticRegression

def rsi(series, period=14):
    delta = series.diff()
    up = (delta.clip(lower=0)).rolling(period).mean()
    down = (-delta.clip(upper=0)).rolling(period).mean()
    rs = up / (down + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)

def get_features(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    out["ret1"] = df["c"].pct_change()
    out["vol"] = df["c"].pct_change().rolling(10).std().fillna(0)
    out["mom10"] = df["c"] / df["c"].rolling(10).mean() - 1
    out["rsi"] = rsi(df["c"], 14)
    return out.fillna(0)

def train_and_predict(df: pd.DataFrame, horizon=5):
    if len(df) < 100 + horizon: return None
    features = get_features(df)
    y = (df["c"].shift(-horizon) > df["c"]).astype(int)
    X = features.iloc[:-horizon]; y = y.iloc[:-horizon]
    model = LogisticRegression(max_iter=1000).fit(X, y)
    prob = float(model.predict_proba(features.iloc[[-1]])[0,1])
    return {"prob_up": prob, "horizon_bars": horizon}

def get_latest_ai(db: Session, symbol_code: str):
    sym = db.query(Symbol).filter(Symbol.code==symbol_code).first()
    if not sym: return {"ts": None, "prob_up": None, "horizon_bars": 0}
    rows = db.query(Bar).filter(Bar.symbol_id==sym.id).order_by(Bar.ts.asc()).all()
    if not rows: return {"ts": None, "prob_up": None, "horizon_bars": 0}
    df = pd.DataFrame([{"ts":r.ts, "o":r.o, "h":r.h, "l":r.l, "c":r.c, "v":r.v} for r in rows])
    out = train_and_predict(df)
    if not out: return {"ts": df["ts"].iloc[-1].isoformat(), "prob_up": None, "horizon_bars": 0}
    return {"ts": df["ts"].iloc[-1].isoformat(), **out}
