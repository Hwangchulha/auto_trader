
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Position, Symbol
from app.schemas import PortfolioOut

router = APIRouter(prefix="/api", tags=["portfolio"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/portfolio/overview", response_model=PortfolioOut)
def overview(db: Session = Depends(get_db)):
    positions = db.query(Position).all()
    equity = 0.0
    items = []
    for p in positions:
        sym = db.query(Symbol).filter(Symbol.id==p.symbol_id).first()
        items.append({"code": sym.code if sym else "?", "qty": p.qty, "avg_price": p.avg_price, "last_price": p.last_price, "value": p.qty*p.last_price})
        equity += p.qty*p.last_price
    cash = 10000000.0  # demo
    return PortfolioOut(cash=cash, equity=equity, positions=items)
