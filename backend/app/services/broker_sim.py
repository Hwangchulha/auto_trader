
from sqlalchemy.orm import Session
from app.models import Bar

class SimBroker:
    def __init__(self, db: Session):
        self.db = db
    def place_order(self, sym, side: str, qty: float, price: float|None):
        last = self.db.query(Bar).filter(Bar.symbol_id==sym.id).order_by(Bar.ts.desc()).first()
        px = (price if price is not None else (last.c if last else 100.0))
        return True, {"price": float(px)}
