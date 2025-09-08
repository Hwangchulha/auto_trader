from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Dict, List, Union
import logging

try:
    # expected existing dependency that returns an authenticated KIS client
    from app.deps import get_kis_client
except Exception:
    # fallback name used in some versions
    from app.deps import get_kis as get_kis_client  # type: ignore

router = APIRouter(prefix="/api/account", tags=["account"])
log = logging.getLogger("app")

def _first_item(obj: Union[Dict[str, Any], List[Dict[str, Any]], None]) -> Dict[str, Any]:
    if obj is None:
        return {}
    if isinstance(obj, list):
        return obj[0] if obj else {}
    if isinstance(obj, dict):
        return obj
    return {}

@router.get("/overview")
async def overview(kis = Depends(get_kis_client)) -> Dict[str, Any]:
    """Return a normalized account overview.
    This handler has been hardened to accept both dict and list payloads from KIS.
    """
    try:
        res: Dict[str, Any] = await kis.account_overview() if callable(getattr(kis, "account_overview", None)) else kis.account_overview()  # type: ignore
    except Exception as e:
        log.exception("KIS account_overview call failed: %s", e)
        raise HTTPException(status_code=502, detail="KIS 계좌 조회 실패")

    # KIS sometimes returns the data under different keys / shapes (dict or list).
    # We unwrap safely and try multiple field names for cash/balance.
    output = res.get("output") or {}
    output1 = res.get("output1") or {}
    output2 = res.get("output2") or {}

    o = _first_item(output)
    o1 = _first_item(output1)
    o2 = _first_item(output2)

    # Try fields commonly seen across KIS examples (names can differ by API):
    # dnca_tot_amt / dcna_tot_amt / dnca_tot_amt_smtl etc.
    def pick_num(d: Dict[str, Any], *keys: str) -> int:
        for k in keys:
            if k in d and d[k] not in (None, ""):
                try:
                    return int(str(d[k]).replace(",", ""))
                except Exception:
                    pass
        return 0

    cash = 0
    cash = cash or pick_num(o2, "dnca_tot_amt", "dcna_tot_amt", "dnca_tot_amt_smtl")
    cash = cash or pick_num(o1, "dnca_tot_amt", "dcna_tot_amt", "dnca_tot_amt_smtl")
    cash = cash or pick_num(o,  "dnca_tot_amt", "dcna_tot_amt", "dnca_tot_amt_smtl")

    return {
        "raw": res,
        "summary": {
            "cash": cash
        }
    }
