
from sqlalchemy.orm import Session
from app.models import ConfigKV
from app.config import settings as env
from datetime import datetime, timezone

ALLOWED = {
    "AUTO_TRADE": ("bool", env.AUTO_TRADE),
    "COOLDOWN_BARS": ("int", env.COOLDOWN_BARS),
    "CONFIRM_BARS": ("int", env.CONFIRM_BARS),
    "HYSTERESIS_PCT": ("float", env.HYSTERESIS_PCT),
    "DAILY_TRADE_LIMIT": ("int", env.DAILY_TRADE_LIMIT),
    "NO_PYRAMIDING": ("bool", env.NO_PYRAMIDING),
    "FX_USDKRW": ("float", env.FX_USDKRW),
}

def _parse(t, v: str):
    if t=="bool":
        return str(v).lower() in ("1","true","on","yes")
    if t=="int":
        try: return int(float(v))
        except: return 0
    if t=="float":
        try: return float(v)
        except: return 0.0
    return v

def get_runtime(db: Session):
    rows = db.query(ConfigKV).all()
    data = {}
    for k,(typ, default) in ALLOWED.items():
        found = next((r for r in rows if r.key==k), None)
        if found:
            data[k] = _parse(typ, found.value)
        else:
            data[k] = default
    return data

def set_many(db: Session, updates: dict):
    now = datetime.now(timezone.utc)
    for k,v in updates.items():
        if k not in ALLOWED: 
            continue
        row = db.query(ConfigKV).filter(ConfigKV.key==k).first()
        val = str(v)
        if row:
            row.value = val; row.updated_at = now; db.add(row)
        else:
            db.add(ConfigKV(key=k, value=val, updated_at=now))
    db.commit()
    return get_runtime(db)
