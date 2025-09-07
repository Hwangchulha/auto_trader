
from sqlalchemy.orm import Session
from app.models import Symbol, Bar
from datetime import datetime, timedelta, timezone
import random

def ensure_symbol(db: Session, code: str, name: str = ""):
    market = code.split(":")[0] if ":" in code else ("KRX" if code.isdigit() else "US")
    full = code if ":" in code else (f"{market}:{code}")
    row = db.query(Symbol).filter(Symbol.code==full).first()
    if not row:
        row = Symbol(code=full, market=market, name=name or full)
        db.add(row); db.commit(); db.refresh(row)
    return row

def seed_random_walk(db: Session, symbol_code: str, tf: str = "1m", n: int = 200):
    sym = ensure_symbol(db, symbol_code)
    last = db.query(Bar).filter(Bar.symbol_id==sym.id, Bar.tf==tf).order_by(Bar.ts.desc()).first()
    if last:
        price = last.c; ts = last.ts + timedelta(minutes=1)
    else:
        price = 50000.0 if sym.market=="KRX" else 180.0
        ts = datetime.now(timezone.utc) - timedelta(minutes=n)
    for _ in range(n):
        drift = random.uniform(-0.003, 0.003)
        new_c = max(1.0, price * (1 + drift))
        o = price
        h = max(o, new_c) * (1 + random.uniform(0, 0.002))
        l = min(o, new_c) * (1 - random.uniform(0, 0.002))
        v = random.uniform(1000, 20000)
        db.add(Bar(symbol_id=sym.id, ts=ts, tf=tf, o=o, h=h, l=l, c=new_c, v=v))
        ts += timedelta(minutes=1); price = new_c
    db.commit()

def append_random_bar(db: Session, symbol_code: str, tf: str = "1m"):
    sym = ensure_symbol(db, symbol_code)
    last = db.query(Bar).filter(Bar.symbol_id==sym.id, Bar.tf==tf).order_by(Bar.ts.desc()).first()
    if not last:
        seed_random_walk(db, symbol_code, tf=tf, n=200); return
    ts = last.ts + timedelta(minutes=1)
    price = last.c
    drift = random.uniform(-0.003, 0.003)
    new_c = max(1.0, price * (1 + drift))
    o = price
    h = max(o, new_c) * (1 + random.uniform(0, 0.002))
    l = min(o, new_c) * (1 - random.uniform(0, 0.002))
    v = random.uniform(1000, 20000)
    db.add(Bar(symbol_id=sym.id, ts=ts, tf=tf, o=o, h=h, l=l, c=new_c, v=v))
    db.commit()
