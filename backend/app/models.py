from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from .db import Base

class Symbol(Base):
    __tablename__ = "symbols"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)  # e.g., "KRX:005930" / "US:NVDA"
    name = Column(String, default="")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True)
    symbol = Column(String, index=True)
    side = Column(String)          # buy/sell
    qty = Column(Float)
    price = Column(Float, nullable=True)  # None=market
    status = Column(String, default="submitted")  # submitted/filled/rejected
    filled_qty = Column(Float, default=0.0)
    raw = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class KISKey(Base):
    __tablename__ = "kis_keys"
    id = Column(Integer, primary_key=True, index=True)
    app_key = Column(String)
    app_secret = Column(String)
    cano = Column(String)
    acnt_prdt_cd = Column(String, default="01")
    kis_env = Column(String, default="vts")  # vts/prod
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
