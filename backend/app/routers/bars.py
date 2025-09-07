
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Symbol, Bar
from app.schemas import BarOut
from sqlalchemy import desc
from datetime import timezone

router = APIRouter(prefix="/api", tags=["bars"])

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

@router.get("/bars/{symbol}", response_model=list[BarOut])
def get_bars(symbol: str, tf: str = Query("1m"), limit: int = Query(300), db: Session = Depends(get_db)):
    sym = db.query(Symbol).filter(Symbol.code==symbol).first()
    if not sym:
        raise HTTPException(status_code=404, detail="symbol not found")
    rows = db.query(Bar).filter(Bar.symbol_id==sym.id, Bar.tf==tf).order_by(desc(Bar.ts)).limit(limit).all()
    rows.reverse()
    return [BarOut(ts=to_aware_utc(r.ts), o=r.o, h=r.h, l=r.l, c=r.c, v=r.v, tf=r.tf) for r in rows]
