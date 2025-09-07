from fastapi import APIRouter, HTTPException
from ..services.kis_accounts import fetch_domestic_balance, fetch_psbl_order

router = APIRouter(prefix="/api/kis", tags=["kis-account"])

@router.get("/overview")
async def overview():
    try:
        bal = await fetch_domestic_balance()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"KIS balance error: {e}")
    out1 = bal.get("output1") or []
    out2 = bal.get("output2") or {}
    dep = out2.get("dnca_tot_amt") or out2.get("dcna_tot_amt") or out2.get("dnca_tot_amt_smtl") or "0"

    try:
        po = await fetch_psbl_order("005930")
        bp = (po.get("output") or {}).get("ord_psbl_cash", "0")
    except Exception as e:
        po = {"error": str(e)}; bp = "0"

    def _num(s): 
        try: return float(str(s).replace(",",""))
        except: return 0.0
    positions = [{
        "symbol": f"KRX:{it.get('pdno','')}",
        "name": it.get("prdt_name",""),
        "qty": _num(it.get("hldg_qty","0")),
        "avg_price": _num(it.get("pchs_avg_pric","0")),
        "eval_price": _num(it.get("evlu_amt","0")),
    } for it in out1]

    return {"balances":{"krw":{"deposit": int(_num(dep)), "buying_power": int(_num(bp))}},
            "positions": positions,
            "raw": {"balance": bal, "psbl_order": po}}
