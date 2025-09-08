from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Symbol
router = APIRouter(prefix="/api/symbols", tags=["symbols"])
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
@router.get("")
def list_symbols(db: Session = Depends(get_db)):
    rows = db.query(Symbol).filter(Symbol.active==True).order_by(Symbol.id.asc()).all()
    return [{"code": r.code, "name": r.name} for r in rows]
@router.post("")
def add_symbol(code: str, name: str = "", db: Session = Depends(get_db)):
    s = db.query(Symbol).filter(Symbol.code==code).first()
    if not s:
        s = Symbol(code=code, name=name, active=True); db.add(s)
    else:
        s.name = name or s.name; s.active = True
    db.commit(); return {"ok": True}
@router.delete("")
def del_symbol(code: str, db: Session = Depends(get_db)):
    s = db.query(Symbol).filter(Symbol.code==code).first()
    if s: db.delete(s); db.commit()
    return {"ok": True}
