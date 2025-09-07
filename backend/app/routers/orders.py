
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.schemas import OrderOut
from app.services.order_engine import place_order
from urllib.parse import parse_qs

router = APIRouter(prefix="/api", tags=["orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/orders", response_model=OrderOut)
async def new_order(request: Request, db: Session = Depends(get_db)):
    # Accept both JSON body and form-urlencoded ("symbol=US%3ANVDA&side=buy&qty=1")
    payload = {}
    ctype = request.headers.get("content-type", "")
    if "application/json" in ctype:
        try:
            payload = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="invalid json body")
    else:
        raw = (await request.body()).decode("utf-8")
        kv = parse_qs(raw, keep_blank_values=True)
        payload = {k: (v[0] if isinstance(v, list) else v) for k, v in kv.items()}

    symbol = str(payload.get("symbol", "")).strip()
    side = str(payload.get("side", "")).strip().lower()
    qty_raw = payload.get("qty", "0")
    price_raw = payload.get("price", None)

    try:
        qty = float(qty_raw)
    except Exception:
        qty = 0.0
    try:
        price = float(price_raw) if price_raw not in (None, "", "null") else None
    except Exception:
        price = None

    if not symbol or side not in ("buy","sell") or qty <= 0:
        raise HTTPException(status_code=400, detail="symbol/side/qty required")

    result = place_order(db, symbol, side, qty, price)
    if result["status"] == "rejected":
        raise HTTPException(status_code=400, detail=result.get("reason", "rejected"))
    return OrderOut(client_id=result["client_id"], status=result["status"], filled_qty=result["filled_qty"], price=result.get("price"))
