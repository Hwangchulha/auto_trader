
from sqlalchemy.orm import Session
from app.models import Symbol, Order, Execution, Position, Bar
from app.config import settings
from datetime import datetime, timezone
import uuid

def _broker(db: Session):
    if settings.SIM_MODE:
        from app.services.broker_sim import SimBroker
        return SimBroker(db)
    else:
        from app.services.broker_kis import KISBroker
        return KISBroker(db)

def utcnow():
    return datetime.now(timezone.utc)

def place_order(db: Session, symbol_code: str, side: str, qty: float, price: float|None):
    sym = db.query(Symbol).filter(Symbol.code==symbol_code).first()
    if not sym:
        return {"status": "rejected", "reason": "symbol not found"}
    cl_id = f"{symbol_code}-{uuid.uuid4().hex[:10]}"
    now = utcnow()
    order = Order(client_id=cl_id, symbol_id=sym.id, side=side, qty=qty, price=price, status="requested", created_at=now, updated_at=now)
    db.add(order); db.commit(); db.refresh(order)

    br = _broker(db)
    ok, fill = br.place_order(sym, side, qty, price)
    if ok:
        order.status = "filled"
        order.filled_qty = qty
        db.add(Execution(order_id=order.id, ts=utcnow(), qty=qty, price=fill["price"]))
        pos = db.query(Position).filter(Position.symbol_id==sym.id).first()
        if not pos:
            pos = Position(symbol_id=sym.id, qty=0.0, avg_price=0.0, last_price=fill["price"])
        if side == "buy":
            new_qty = pos.qty + qty
            pos.avg_price = (pos.avg_price*pos.qty + qty*fill["price"]) / max(1e-9, new_qty)
            pos.qty = new_qty
        else:
            pos.qty = max(0.0, pos.qty - qty)
        pos.last_price = fill["price"]
        db.add(pos)
    else:
        order.status = "rejected"
    order.updated_at = utcnow()
    db.add(order); db.commit()
    return {"client_id": order.client_id, "status": order.status, "filled_qty": float(order.filled_qty), "price": price if price is not None else (fill.get("price") if ok else None)}
