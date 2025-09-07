
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Symbol
from app.schemas import SymbolOut

router = APIRouter(prefix="/api", tags=["symbols"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/symbols", response_model=list[SymbolOut])
def list_symbols(db: Session = Depends(get_db)):
    rows = db.query(Symbol).filter(Symbol.active==True).all()
    return [SymbolOut(code=r.code, market=r.market, name=r.name, active=r.active) for r in rows]
