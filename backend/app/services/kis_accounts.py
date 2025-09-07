from typing import Dict, Any
from .kis_env import kis_cano, kis_acnt
from .kis_http import kis_get

BALANCE_PATH = "/uapi/domestic-stock/v1/trading/inquire-balance"
PSBL_ORDER_PATH = "/uapi/domestic-stock/v1/trading/inquire-psbl-order"

def _common():
    return {"CANO": kis_cano(), "ACNT_PRDT_CD": kis_acnt()}

def _balance_params():
    p = _common()
    p.update({
        "AFHR_FLPR_YN":"N","OFL_YN":"N","INQR_DVSN":"02","UNPR_DVSN":"01",
        "FUND_STTL_ICLD_YN":"N","FNCG_AMT_AUTO_RDPT_YN":"N",
        "PRCS_DVSN":"01","CTX_AREA_FK100":"","CTX_AREA_NK100":""
    })
    return p

async def fetch_domestic_balance()->Dict[str,Any]:
    return await kis_get(BALANCE_PATH,"balance",_balance_params())

async def fetch_psbl_order(pdno: str)->Dict[str,Any]:
    p = _common()
    p.update({"PDNO":pdno,"ORD_UNPR":"0","ORD_DVSN":"01","CMA_EVLU_AMT_ICLD_YN":"N","OVRS_ICLD_YN":"N"})
    return await kis_get(PSBL_ORDER_PATH,"psbl_order",p)
