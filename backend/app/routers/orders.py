from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Order
from ..services.broker_sim import place as sim_place
from ..services.broker_kis import order_cash
from ..services.kis_env import sim_mode

router = APIRouter(prefix="/api", tags=["orders"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/orders")
async def post_order(req: Request, db: Session = Depends(get_db)):
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

    if sim_mode():
        res = sim_place(symbol, side, qty, price)
        status = "filled"
    else:
        res = await order_cash(symbol, side, qty, price)
        status = "submitted"

    o = Order(client_id=res.get("client_id",""), symbol=symbol, side=side, qty=qty, price=price, status=status, raw=res)
    if status=="filled": o.filled_qty = qty
    db.add(o); db.commit()
    return {"status": status, "client_id": o.client_id or f"{symbol}-local", "filled_qty": float(o.filled_qty), "price": res.get("price", price or 0), "kis_response": res}
