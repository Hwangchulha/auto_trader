
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SymbolOut(BaseModel):
    code: str
    market: str
    name: str
    active: bool

class BarOut(BaseModel):
    ts: datetime
    o: float; h: float; l: float; c: float; v: float
    tf: str

class OrderIn(BaseModel):
    symbol: str
    side: str
    qty: float
    price: Optional[float] = None

class OrderOut(BaseModel):
    client_id: str
    status: str
    filled_qty: float
    price: Optional[float] = None

class PortfolioOut(BaseModel):
    cash: float
    equity: float
    positions: list

class SignalOut(BaseModel):
    ts: datetime
    strategy: str
    signal: str
    score: float

class RuntimeSettingsIn(BaseModel):
    AUTO_TRADE: Optional[bool] = None
    COOLDOWN_BARS: Optional[int] = Field(None, ge=0, le=10000)
    CONFIRM_BARS: Optional[int] = Field(None, ge=1, le=1000)
    HYSTERESIS_PCT: Optional[float] = Field(None, ge=0.0, le=1.0)
    DAILY_TRADE_LIMIT: Optional[int] = Field(None, ge=0, le=10000)
    NO_PYRAMIDING: Optional[bool] = None
    FX_USDKRW: Optional[float] = Field(None, ge=0.0, le=1000000.0)
