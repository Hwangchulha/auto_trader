from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Order
from ..services.broker_kis import order_cash
from ..services.keys_store import exists as keys_exists
router = APIRouter(prefix="/api", tags=["orders"])
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
def _extract_odno(res: dict) -> str:
    if not isinstance(res, dict): return ""
    out = res.get("output")
    if isinstance(out, list): out = out[0] if out else {}
    if isinstance(out, dict): return out.get("ODNO") or out.get("KRX_ODNO") or ""
    return res.get("ODNO","") or res.get("KRX_ODNO","")
@router.post("/orders")
async def post_order(req: Request, db: Session = Depends(get_db)):
    if not keys_exists():
        raise HTTPException(status_code=400, detail="KIS keys not set. Save keys in /settings.")
    ctype = (req.headers.get("content-type") or "").lower()
    if "application/json" in ctype:
        data = await req.json()
    else:
        body = (await req.body()).decode()
        from urllib.parse import parse_qs
        d = parse_qs(body)
        data = {k: (v[0] if isinstance(v, list) else v) for k, v in d.items()}
        if "qty" in data:
            try: data["qty"] = float(data["qty"])
            except: data["qty"] = 0.0
        if "price" in data:
            try: data["price"] = None if data["price"] in ("", "0", "0.0", None) else float(data["price"])
            except: data["price"] = None
    symbol = (data.get("symbol") or "").strip()
    side = (str(data.get("side") or "")).lower().strip()
    qty = float(data.get("qty", 0) or 0)
    price = data.get("price", None)
    if not symbol or side not in ("buy","sell") or qty <= 0:
        raise HTTPException(status_code=400, detail="symbol/side/qty required")
    res = await order_cash(symbol, side, qty, price)
    rt = str(res.get("rt_cd","")); status = "submitted" if rt == "0" else "rejected"
    client_id = _extract_odno(res)
    o = Order(client_id=client_id or f"{symbol}-pending", symbol=symbol, side=side, qty=qty, price=price, status=status, raw=res)
    db.add(o); db.commit()
    return {"status": status, "client_id": o.client_id, "kis_response": res}
