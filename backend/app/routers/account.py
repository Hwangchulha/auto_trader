from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Order, Symbol
from ..services.kis_env import sim_mode
from ..services.kis_accounts import fetch_domestic_balance, fetch_psbl_order

router = APIRouter(prefix="/api/account", tags=["account"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/overview")
async def overview(db: Session = Depends(get_db)):
    balances = {"krw":{"deposit":0,"buying_power":0}}
    positions = []
    mode = "SIM" if sim_mode() else "KIS-VTS"

    if sim_mode():
        balances["krw"]["deposit"] = 100_000_000
        balances["krw"]["buying_power"] = 100_000_000
    else:
        bal = await fetch_domestic_balance()
        out1 = bal.get("output1") or []
        out2 = bal.get("output2") or {}
        dep = out2.get("dnca_tot_amt") or out2.get("dcna_tot_amt") or out2.get("dnca_tot_amt_smtl") or "0"
        def _num(s): 
            try: return float(str(s).replace(",",""))
            except: return 0.0
        for it in out1:
            positions.append({
                "symbol": f"KRX:{it.get('pdno','')}",
                "name": it.get("prdt_name",""),
                "qty": _num(it.get("hldg_qty","0")),
                "avg_price": _num(it.get("pchs_avg_pric","0")),
                "eval_price": _num(it.get("evlu_amt","0")),
            })
        po = await fetch_psbl_order("005930")
        bp = (po.get("output") or {}).get("ord_psbl_cash", "0")
        balances["krw"]["deposit"] = int(_num(dep))
        balances["krw"]["buying_power"] = int(_num(bp))

    # recent orders
    orders = db.query(Order).order_by(Order.created_at.desc()).limit(20).all()
    recent = [{
        "client_id": o.client_id, "symbol": o.symbol, "side": o.side, "qty": o.qty, "price": o.price,
        "status": o.status, "created_at": o.created_at.isoformat() if o.created_at else ""
    } for o in orders]

    return {"mode": mode, "balances": balances, "positions": positions, "recent_orders": recent}
