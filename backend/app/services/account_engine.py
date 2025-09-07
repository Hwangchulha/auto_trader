
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import Symbol, Position, Order, Execution, Bar
from app.config import settings
from datetime import datetime, timezone
from typing import Dict, Any
from app.services.runtime_settings import get_runtime
from app.services.kis_accounts import fetch_domestic_balance, fetch_domestic_deposit, fetch_overseas_balance
import asyncio

def _mark_to_market(db: Session):
    poss = db.query(Position).all()
    for p in poss:
        last = db.query(Bar).filter(Bar.symbol_id==p.symbol_id).order_by(Bar.ts.desc()).first()
        if last:
            p.last_price = last.c
            db.add(p)
    db.commit()

def _compute_cash_sim(db: Session) -> Dict[str, float]:
    krw = float(settings.INIT_CASH_KRW)
    usd = float(settings.INIT_CASH_USD)
    orders = {o.id: o for o in db.query(Order).all()}
    exes = db.query(Execution).all()
    for e in exes:
        o = orders.get(e.order_id)
        if not o: 
            continue
        sym = db.query(Symbol).filter(Symbol.id==o.symbol_id).first()
        if not sym:
            continue
        amt = float(e.price) * float(e.qty)
        if sym.market == "KRX":
            krw = krw - amt if o.side == "buy" else krw + amt
        else:
            usd = usd - amt if o.side == "buy" else usd + amt
    return {"krw": krw, "usd": usd}

def list_positions(db: Session):
    _mark_to_market(db)
    out = []
    poss = db.query(Position).all()
    for p in poss:
        sym = db.query(Symbol).filter(Symbol.id==p.symbol_id).first()
        if not sym: 
            continue
        value = p.last_price * p.qty
        upl = (p.last_price - p.avg_price) * p.qty
        upl_pct = ((p.last_price / p.avg_price - 1.0) * 100.0) if p.avg_price > 0 else 0.0
        out.append({
            "code": sym.code, "market": sym.market, "qty": float(p.qty),
            "avg_price": float(p.avg_price), "last_price": float(p.last_price),
            "value": float(value), "unrealized_pl": float(upl), "unrealized_pl_pct": float(upl_pct)
        })
    return out

def list_orders(db: Session, limit: int = 50):
    rows = db.query(Order).order_by(desc(Order.created_at)).limit(limit).all()
    out = []
    for o in rows:
        sym = db.query(Symbol).filter(Symbol.id==o.symbol_id).first()
        ts = (o.created_at if o.created_at.tzinfo else o.created_at.replace(tzinfo=timezone.utc)).isoformat() if o.created_at else None
        out.append({
            "client_id": o.client_id, "code": sym.code if sym else None, "side": o.side,
            "qty": float(o.qty), "price": o.price, "status": o.status,
            "filled_qty": float(o.filled_qty), "created_at": ts
        })
    return out

def list_executions(db: Session, limit: int = 50):
    rows = db.query(Execution).order_by(desc(Execution.ts)).limit(limit).all()
    out = []
    for e in rows:
        o = db.query(Order).filter(Order.id==e.order_id).first()
        sym = db.query(Symbol).filter(Symbol.id==o.symbol_id).first() if o else None
        ts = (e.ts if e.ts.tzinfo else e.ts.replace(tzinfo=timezone.utc)).isoformat() if e.ts else None
        out.append({
            "order_client_id": o.client_id if o else None,
            "code": sym.code if sym else None,
            "qty": float(e.qty), "price": float(e.price), "side": o.side if o else None,
            "ts": ts
        })
    return out

def kis_raw_bundle(db: Session) -> Dict[str, Any]:
    if settings.SIM_MODE:
        return {"mode":"SIM","domestic_balance":None,"domestic_deposit":None,"overseas_balance":None}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    dom_bal, dom_dep, os_bal = loop.run_until_complete(asyncio.gather(
        fetch_domestic_balance(), fetch_domestic_deposit(), fetch_overseas_balance()
    ))
    loop.close()
    return {"mode":"KIS","domestic_balance":dom_bal,"domestic_deposit":dom_dep,"overseas_balance":os_bal}

def get_overview(db: Session) -> Dict[str, Any]:
    rt = get_runtime(db)
    fx = float(rt.get("FX_USDKRW", settings.FX_USDKRW))
    _mark_to_market(db)
    cash_sim = _compute_cash_sim(db)
    pos = list_positions(db)
    pos_val_krw = sum(p["value"] for p in pos if p["market"] == "KRX")
    pos_val_usd = sum(p["value"] for p in pos if p["market"] == "US")

    kis_raw = None
    balances = {
        "krw": {"cash": float(cash_sim["krw"]), "buying_power": float(cash_sim["krw"]), "deposit": None, "withdrawable": None},
        "usd": {"cash": float(cash_sim["usd"]), "buying_power": float(cash_sim["usd"])},
    }

    if not settings.SIM_MODE:
        kis_raw = kis_raw_bundle(db)
        try:
            dom_dep = kis_raw.get("domestic_deposit") if kis_raw else None
            if isinstance(dom_dep, dict):
                balances["krw"]["deposit"] = dom_dep.get("output", {}).get("dnca_tot_amt") or None
                balances["krw"]["withdrawable"] = dom_dep.get("output", {}).get("prvs_rcdl_excc_amt") or None
                balances["krw"]["buying_power"] = dom_dep.get("output", {}).get("ord_psbl_cash") or balances["krw"]["buying_power"]
        except Exception:
            pass

    total_krw = balances["krw"]["cash"] + pos_val_krw + pos_val_usd * fx
    total_usd = balances["usd"]["cash"] + pos_val_usd + (pos_val_krw / fx if fx else 0.0)

    return {
        "mode": "SIM" if settings.SIM_MODE else "KIS",
        "account": {"cano": settings.KIS_CANO, "product_code": settings.KIS_ACNT_PRDT_CD},
        "balances": balances,
        "fx": {"usdkrw": fx},
        "equity": {
            "positions_value_krw": float(pos_val_krw),
            "positions_value_usd": float(pos_val_usd),
            "total_krw": float(total_krw),
            "total_usd": float(total_usd)
        },
        "positions": pos,
        "orders_recent": list_orders(db, limit=20),
        "executions_recent": list_executions(db, limit=20),
        "kis_raw": kis_raw,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "guard": {
            "cooldown_bars": rt["COOLDOWN_BARS"],
            "confirm_bars": rt["CONFIRM_BARS"],
            "hysteresis_pct": rt["HYSTERESIS_PCT"],
            "daily_trade_limit": rt["DAILY_TRADE_LIMIT"],
            "no_pyramiding": rt["NO_PYRAMIDING"],
            "auto_trade": rt["AUTO_TRADE"],
        }
    }
