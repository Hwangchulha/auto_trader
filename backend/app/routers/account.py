from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Order
from ..services.kis_accounts import fetch_domestic_balance, fetch_psbl_order
from ..services.keys_store import exists as keys_exists
router = APIRouter(prefix="/api/account", tags=["account"])
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
def _num(s):
    try: return float(str(s).replace(",",""))
    except Exception: return 0.0
def _first_dict(x):
    if isinstance(x, dict): return x
    if isinstance(x, list) and x: return x[0] if isinstance(x[0], dict) else {}
    return {}
@router.get("/overview")
async def overview(db: Session = Depends(get_db)):
    if not keys_exists():
        return {"mode":"KIS","needs_keys":True,"balances":{"krw":{"deposit":0,"buying_power":0}},
                "positions":[],"recent_orders":[]}
    bal = await fetch_domestic_balance()
    out1 = bal.get("output1") or []
    out2 = _first_dict(bal.get("output2"))
    dep = out2.get("dnca_tot_amt") or out2.get("dcna_tot_amt") or out2.get("dnca_tot_amt_smtl") or "0"
    positions = []
    for it in out1 or []:
        positions.append({
            "symbol": f"KRX:{it.get('pdno','')}",
            "name": it.get("prdt_name",""),
            "qty": _num(it.get("hldg_qty","0")),
            "avg_price": _num(it.get("pchs_avg_pric","0")),
            "eval_price": _num(it.get("evlu_amt","0")),
        })
    po = await fetch_psbl_order("005930")
    outp = po.get("output")
    if isinstance(outp, list): outp = outp[0] if outp else {}
    bp = (outp or {}).get("ord_psbl_cash", "0")
    orders = db.query(Order).order_by(Order.created_at.desc()).limit(20).all()
    recent = [{
        "client_id": o.client_id, "symbol": o.symbol, "side": o.side, "qty": o.qty, "price": o.price,
        "status": o.status, "created_at": o.created_at.isoformat() if o.created_at else ""
    } for o in orders]
    return {"mode":"KIS", "needs_keys":False,
            "balances":{"krw":{"deposit": int(_num(dep)), "buying_power": int(_num(bp))}},
            "positions": positions, "recent_orders": recent}
