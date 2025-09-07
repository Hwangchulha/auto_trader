
import time
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.market_data import seed_random_walk, append_random_bar, ensure_symbol
from app.services.signal_engine import run_strategies
from app.services.order_engine import place_order
from app.services.trade_guard import TradeGuard
from app.services.runtime_settings import get_runtime
from app.models import Symbol, Position, Bar
from app.config import settings

def _active_symbols(db: Session) -> list[str]:
    rows = db.query(Symbol).filter(Symbol.active == True).all()
    return [r.code for r in rows]

def _bootstrap_symbols_from_env(db: Session):
    if db.query(Symbol).count() == 0:
        for code in [s.strip() for s in settings.SYMBOLS.split(",") if s.strip()]:
            ensure_symbol(db, code)

def _mark_positions(db: Session, symbol_code: str):
    sym = db.query(Symbol).filter(Symbol.code==symbol_code).first()
    if not sym: return
    last = db.query(Bar).filter(Bar.symbol_id==sym.id).order_by(Bar.ts.desc()).first()
    if not last: return
    pos = db.query(Position).filter(Position.symbol_id==sym.id).first()
    if pos:
        pos.last_price = last.c
        db.add(pos); db.commit()

def tick_once(db: Session, symbol_code: str):
    rt = get_runtime(db)
    if settings.SIM_MODE:
        append_random_bar(db, symbol_code, tf="1m")
    _mark_positions(db, symbol_code)
    outs = run_strategies(db, symbol_code, tf="1m")
    guard = TradeGuard(db, tf="1m", params=rt)
    for o in outs:
        side = "buy" if o["signal"]=="BUY" else ("sell" if o["signal"]=="SELL" else None)
        if side is None:
            continue
        allow, reason = guard.allow(symbol_code, side)
        if not allow:
            continue
        if not rt.get("AUTO_TRADE", True):
            continue
        place_order(db, symbol_code, side, qty=1, price=None)

def run_loop():
    db = SessionLocal()
    _bootstrap_symbols_from_env(db)
    for code in _active_symbols(db):
        seed_random_walk(db, code, tf="1m", n=300)
    while True:
        codes = _active_symbols(db)
        if not codes:
            time.sleep(2); continue
        for code in codes:
            tick_once(db, code)
        time.sleep(3)
