from fastapi import APIRouter, Depends, HTTPException, Body, Request
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging

try:
    from app.deps import get_kis_client
except Exception:
    from app.deps import get_kis as get_kis_client  # type: ignore

router = APIRouter(prefix="/api", tags=["orders"])
log = logging.getLogger("app")

class OrderIn(BaseModel):
    symbol: str = Field(..., description="예: KRX:005930")
    side: str = Field(..., description="'buy' 또는 'sell'")
    qty: float = Field(..., description="수량")
    price: float = Field(0, description="0 이면 시장가")
    account: Optional[str] = None

def _normalize_symbol(symbol: str) -> Dict[str, str]:
    # Accept "KRX:005930" or raw "005930"
    s = (symbol or "").strip().upper()
    if ":" in s:
        market, code = s.split(":", 1)
    else:
        market, code = "KRX", s
    return {"market": market, "code": code}

@router.post("/orders")
async def create_order(
    request: Request,
    payload: Optional[OrderIn] = None,
    kis = Depends(get_kis_client)
) -> Dict[str, Any]:
    """Create an order (KIS). Accepts JSON *or* form-urlencoded.
    If price <= 0 -> market order, else limit order.
    """
    try:
        data: Dict[str, Any]
        if payload is not None:
            data = payload.model_dump()
        else:
            # Try to parse form data
            form = await request.body()
            if form:
                # application/x-www-form-urlencoded
                try:
                    from urllib.parse import parse_qs
                    qs = {k: v[0] for k, v in parse_qs(form.decode("utf-8")).items()}
                    data = {
                        "symbol": qs.get("symbol"),
                        "side": qs.get("side"),
                        "qty": float(qs.get("qty", "0") or "0"),
                        "price": float(qs.get("price", "0") or "0"),
                        "account": qs.get("account")
                    }
                except Exception:
                    raise HTTPException(status_code=422, detail="잘못된 폼 데이터입니다.")
            else:
                raise HTTPException(status_code=422, detail="주문 입력이 비어 있습니다.")
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Order payload parse error: %s", e)
        raise HTTPException(status_code=400, detail="주문 입력 파싱 실패")

    if not data.get("symbol") or not data.get("side"):
        raise HTTPException(status_code=422, detail="symbol/side는 필수입니다.")

    sym = _normalize_symbol(data["symbol"])
    side = data["side"].lower()
    qty = data.get("qty") or 0
    price = data.get("price") or 0

    if qty <= 0:
        raise HTTPException(status_code=422, detail="수량(qty)는 0보다 커야 합니다.")

    # Map to KIS fields
    ord_dvsn = "01" if float(price) <= 0 else "00"  # 01: 시장가, 00: 지정가 (일반)
    ord_prc = None if ord_dvsn == "01" else str(int(float(price)))  # KIS는 문자열/정수형 가격 기대

    try:
        res = await kis.order_cash(
            market=sym["market"],
            code=sym["code"],
            side=side,
            qty=int(qty),
            ord_dvsn=ord_dvsn,
            price=ord_prc
        ) if callable(getattr(kis, "order_cash", None)) else kis.order_cash(
            market=sym["market"],
            code=sym["code"],
            side=side,
            qty=int(qty),
            ord_dvsn=ord_dvsn,
            price=ord_prc
        )
    except Exception as e:
        log.exception("KIS order call failed: %s", e)
        raise HTTPException(status_code=502, detail="KIS 주문 실패")

    # Unify response
    msg_cd = None
    msg = None
    try:
        msg_cd = res.get("msg_cd") or res.get("output", {}).get("msg_cd")
        msg = res.get("msg1") or res.get("output", {}).get("msg1")
    except Exception:
        pass

    return {
        "status": "submitted",
        "request": {
            "symbol": sym,
            "side": side,
            "qty": int(qty),
            "ord_dvsn": ord_dvsn,
            "price": ord_prc or 0,
        },
        "kis_response": res,
        "message": {"code": msg_cd, "text": msg}
    }
