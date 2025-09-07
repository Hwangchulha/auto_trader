
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Symbol, Signal
from app.schemas import SignalOut
from sqlalchemy import desc
from datetime import timezone

router = APIRouter(prefix="/api", tags=["signals"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def to_aware_utc(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

@router.get("/signals/{symbol}", response_model=list[SignalOut])
def recent_signals(symbol: str, db: Session = Depends(get_db)):
    sym = db.query(Symbol).filter(Symbol.code==symbol).first()
    if not sym:
        return []
    rows = db.query(Signal).filter(Signal.symbol_id==sym.id).order_by(desc(Signal.ts)).limit(50).all()
    return [SignalOut(ts=to_aware_utc(r.ts), strategy=r.strategy, signal=r.signal, score=r.score) for r in rows]
