from app.logging_setup import setup_logging
setup_logging()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware_logging import RequestContextMiddleware
from app.db import Base, engine
from app.models import *
from app.routers import diag, symbols, orders, account, settings_runtime, keys

Base.metadata.create_all(bind=engine)

app = FastAPI(title="KIS Auto Trader API (KIS-only, 8088)")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestContextMiddleware)

# routers
app.include_router(diag.router)
app.include_router(symbols.router)
app.include_router(orders.router)
app.include_router(account.router)
app.include_router(settings_runtime.router)
app.include_router(keys.router)

@app.get("/health")
def health():
    return {"ok": True}
