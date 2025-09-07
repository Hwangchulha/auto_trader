
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.routers import health, symbols, bars, orders, portfolio, signals, watchlist, account
from app.routers import settings as settings_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="KIS Auto Trader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(symbols.router)
app.include_router(bars.router)
app.include_router(orders.router)
app.include_router(portfolio.router)
app.include_router(signals.router)
app.include_router(watchlist.router)
app.include_router(account.router)
app.include_router(settings_router.router)
