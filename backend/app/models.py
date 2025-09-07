
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime, timezone

def utcnow():
    return datetime.now(timezone.utc)

class Symbol(Base):
    __tablename__ = "symbols"
    id = Column(Integer, primary_key=True)
    code = Column(String, index=True, unique=True)    # "KRX:005930" / "US:AAPL"
    market = Column(String, index=True)
    name = Column(String, default="")
    active = Column(Boolean, default=True)
    bars = relationship("Bar", back_populates="symbol")

class Bar(Base):
    __tablename__ = "bars"
    id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), index=True)
    ts = Column(DateTime(timezone=True), index=True, default=utcnow)
    tf = Column(String, default="1m")
    o = Column(Float); h = Column(Float); l = Column(Float); c = Column(Float); v = Column(Float)
    symbol = relationship("Symbol", back_populates="bars")
    __table_args__ = (UniqueConstraint('symbol_id', 'ts', 'tf', name='uq_bar'),)

class Signal(Base):
    __tablename__ = "signals"
    id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, index=True)
    ts = Column(DateTime(timezone=True), index=True, default=utcnow)
    strategy = Column(String, index=True)
    signal = Column(String, index=True)  # BUY/SELL/HOLD
    score = Column(Float, default=0.0)
    params = Column(String, default="")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    client_id = Column(String, index=True, unique=True)
    symbol_id = Column(Integer, index=True)
    side = Column(String)
    qty = Column(Float)
    price = Column(Float, nullable=True)
    status = Column(String, default="requested")
    filled_qty = Column(Float, default=0.0)
    reject_code = Column(String, default="")
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow)

class Execution(Base):
    __tablename__ = "executions"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, index=True)
    ts = Column(DateTime(timezone=True), default=utcnow)
    qty = Column(Float)
    price = Column(Float)

class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, index=True)
    qty = Column(Float, default=0.0)
    avg_price = Column(Float, default=0.0)
    last_price = Column(Float, default=0.0)

class ConfigKV(Base):
    __tablename__ = "config_kv"
    key = Column(String, primary_key=True)  # e.g. "COOLDOWN_BARS"
    value = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow)
