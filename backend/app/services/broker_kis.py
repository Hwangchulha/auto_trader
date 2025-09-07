from typing import Dict, Any, Optional
from .kis_env import kis_cano, kis_acnt
from .kis_http import kis_post
ORDER_CASH_PATH = "/uapi/domestic-stock/v1/trading/order-cash"

def _pdno(symbol: str)->str: return symbol.split(":",1)[1] if ":" in symbol else symbol
def _ord_dvsn(price: Optional[float])->str: return "01" if (price is None or float(price)==0.0) else "00"
def _ord_unpr(price: Optional[float])->str: return "0" if (price is None or float(price)==0.0) else str(price)

async def order_cash(symbol: str, side: str, qty: float, price: Optional[float])->Dict[str,Any]:
    body = {"CANO": kis_cano(),"ACNT_PRDT_CD": kis_acnt(),"PDNO": _pdno(symbol),
            "ORD_DVSN": _ord_dvsn(price),"ORD_QTY": str(int(qty)),"ORD_UNPR": _ord_unpr(price)}
    tr_key = "order_cash_buy" if side.lower()=="buy" else "order_cash_sell"
    return await kis_post(ORDER_CASH_PATH, tr_key, body)
