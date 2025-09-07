# KIS 모의(VTS) 연동 패치 키트 (v12, Frontend 무변경)

**목표**: https://github.com/Hwangchulha/auto_trader/tree/main/ 레포의 **디자인/프론트는 그대로** 유지하고,
백엔드(FastAPI)에 **KIS 모의서버(VTS)** 연동을 추가합니다.

이 패치는 **새 라우터(`/api/kis/*`)와 서비스만** 추가합니다. 기존 API/화면을 전혀 건드리지 않습니다.

## 적용 방법 (복사-붙여넣기)

1) 이 폴더의 `backend/app/...` 을 **여러분 레포의 `backend/app/` 아래에 그대로 복사**합니다.
   - 새로 생기는 파일만 있고, 기존 파일은 덮어쓰지 않습니다.

2) `backend/requirements.txt`에 아래 행이 없다면 추가하세요:
   ```
   httpx==0.27.0
   ```
   > Docker를 쓰고 있다면 `docker compose build --no-cache` 로 재빌드 권장.

3) `.env`(또는 docker compose의 env)에 아래 값을 채우세요(모의 AppKey/Secret/계좌 필요):
   ```env
   SIM_MODE=0           # KIS 사용 모드
   KIS_ENV=vts          # 모의 서버
   KIS_APP_KEY=발급키
   KIS_APP_SECRET=발급시크릿
   KIS_CANO=계좌앞8자리
   KIS_ACNT_PRDT_CD=01
   ```

4) **재기동**
   ```bash
   docker compose up --build -d
   ```

5) 확인
   - `GET http://localhost:8000/api/kis/overview`  → 잔고/보유/주문가능 현금 표시
   - `POST http://localhost:8000/api/kis/orders`   → KIS **모의 주문** 요청 (시장가/지정가)
   - 프론트는 그대로 두고, 원한다면 UI에서 이 새 API를 호출해 **디자인 변경 없이** 기능 추가 가능

## 새 API 요약

- `GET /api/kis/overview`
  - 국내 잔고 `/uapi/domestic-stock/v1/trading/inquire-balance` (TR: VTTC8434R)
  - 주문가능 현금 `/uapi/domestic-stock/v1/trading/inquire-psbl-order` (TR: VTTC8908R, 기본 PDNO=005930)

- `POST /api/kis/orders` (JSON 또는 x-www-form-urlencoded)
  - 바디: `{ "symbol":"KRX:005930", "side":"buy"|"sell", "qty":1, "price":0 }`
    - `price` 비우거나 0 → **시장가(ORD_DVSN=01)**, 값 넣으면 **지정가(ORD_DVSN=00)**

> 토큰 `/oauth2/tokenP`, 해시키 `/uapi/hashkey`를 내부에서 자동 처리합니다.
