from app.logging_setup import setup_logging
setup_logging()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware_logging import RequestContextMiddleware
from app.routers import kis_account, kis_orders, diag, settings_runtime, account_compat

app = FastAPI(title="KIS Auto Trader API (with compat)")

# CORS wide-open for simplicity (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestContextMiddleware)

# Core routers
app.include_router(kis_account.router)
app.include_router(kis_orders.router)
app.include_router(diag.router)
app.include_router(settings_runtime.router)

# Compatibility routes expected by the existing frontend
app.include_router(account_compat.router)

@app.get("/health")
def health():
    return {"ok": True}
