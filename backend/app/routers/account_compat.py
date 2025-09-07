from fastapi import APIRouter, Request
from app.routers.kis_account import overview as kis_overview
from app.routers.kis_orders import post_order as kis_post_order

router = APIRouter(tags=["compat"])

@router.get("/api/account/overview")
async def account_overview():
    # 기존 프론트가 기대하는 엔드포인트를 KIS 개요로 매핑
    return await kis_overview()

@router.post("/api/orders")
async def account_orders(request: Request):
    # 기존 프론트가 /api/orders 로 주문을 때리는 경우 KIS 주문으로 위임
    return await kis_post_order(request)

@router.get("/api/watchlist")
def watchlist():
    # 기존 프론트에서 폴링하는 경우가 있어 빈 리스트라도 반환
    # 필요시 DB/파일 연동으로 교체 가능
    return {"symbols": []}
