from fastapi import APIRouter, Request, HTTPException
from ..services.broker_kis import order_cash

router = APIRouter(prefix="/api/kis", tags=["kis-orders"])

@router.post("/orders")
async def post_order(req: Request):
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
    return {"status":"submitted", "request":{"symbol":symbol,"side":side,"qty":qty,"price":price}, "kis_response": res}
