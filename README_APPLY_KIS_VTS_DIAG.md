# KIS 모의(VTS) + 스마트 디버깅 패치 (v12.1, **Frontend 무변경**)

이 패치는 기존 레포의 디자인/프론트는 그대로 두고, **백엔드(FastAPI)** 에
1) **KIS 모의 서버(VTS)** 연동 API  
2) **로테이팅 파일 로그 + 진단 번들(zip) 생성**  
을 추가합니다.

> 기준 레포: https://github.com/Hwangchulha/auto_trader/tree/main/ (프론트 무변경)

---

## 적용 순서 (복붙)

1. 이 패키지의 `backend/app/...` 폴더 내용을 **여러분 레포의 `backend/app/` 아래에 그대로 복사**하세요.  
   - 새 파일만 추가합니다. 기존 파일은 손대지 않습니다.
2. `backend/requirements.txt`에 다음이 없으면 추가하세요:
   ```
   httpx==0.27.0
   python-multipart==0.0.9
   ```
3. **로그 디렉터리**를 볼륨으로 잡아두면 편합니다. `docker-compose.yml`의 backend 서비스에:
   ```yaml
   services:
     backend:
       volumes:
         - ./logs:/app/logs
   ```
4. **.env**(또는 compose env)에 KIS 모의 설정:
   ```env
   SIM_MODE=0
   KIS_ENV=vts
   KIS_APP_KEY=모의앱키
   KIS_APP_SECRET=모의시크릿
   KIS_CANO=계좌앞8자리
   KIS_ACNT_PRDT_CD=01

   LOG_LEVEL=INFO
   LOG_MAX_BYTES=5242880          # 5MB
   LOG_BACKUP_COUNT=5
   LOG_TO_STDOUT=1                # 1이면 파일과 콘솔 둘 다
   ```
5. **`backend/app/main.py`에 3줄 추가**  
   맨 위 어딘가, FastAPI 앱 만들기 전에:
   ```python
   from app.logging_setup import setup_logging
   setup_logging()
   ```
   앱 생성 후 라우터 등록 쪽에:
   ```python
   from app.middleware_logging import RequestContextMiddleware
   app.add_middleware(RequestContextMiddleware)

   from app.routers import kis_account, kis_orders, diag
   app.include_router(kis_account.router)
   app.include_router(kis_orders.router)
   app.include_router(diag.router)
   ```
6. **재빌드/재기동**
   ```bash
   docker compose up --build -d
   ```

---

## 새로 생기는 API

- **KIS (모의)**
  - `GET /api/kis/overview` → 잔고/보유 + 주문가능현금
  - `POST /api/kis/orders`   → 국내 현금주문(시장가/지정가, JSON/폼 둘 다)

- **Diagnostics**
  - `GET  /api/diag/ping`        → 헬스 핑
  - `GET  /api/diag/health`      → DB 연결/KIS 토큰 체크
  - `GET  /api/diag/logs?file=app|kis|error|access|client&tail=200`
  - `POST /api/diag/clientlog`   → 브라우저/앱에서 클라이언트 오류 업로드
  - `GET  /api/diag/bundle`      → **버그 리포트 ZIP** 생성 및 다운로드
  - `GET  /api/diag/env`         → 민감정보 마스킹된 환경 정보

> 생성되는 로그 파일(회전): `logs/app.log`, `logs/error.log`, `logs/access.log`, `logs/kis.log`, `logs/client.log`

---

## 버그 리포트 ZIP (스마트 디버깅)

- 포함 항목
  - 최근 로그(각 파일 tail 5,000라인)
  - 마스킹된 env 요약(`env_summary.json`)
  - pip freeze(`pip_freeze.txt`, 실패 시 빈 파일)
  - Uvicorn/FastAPI 버전 등 런타임 요약
- 다운로드: `GET /api/diag/bundle`  
  - 파일명: `bug_report_YYYYmmdd_HHMMSS.zip`

이 ZIP 하나만 보내주시면 재현 없이도 상태 파악이 가능합니다.

---

## 로딩중 멈춤 현상 빠른 진단 포인트

- 프론트에서 `NEXT_PUBLIC_API_BASE` 환경값이 백엔드 주소와 다른지 확인
- CORS: 프론트→백엔드 도메인/포트 불일치 시 차단 여부
- KIS 401/403: `.env`의 APP_KEY/SECRET/계좌값 오탈자, vts/prod 혼동
- Docker 네트워크: `localhost` vs 컨테이너 내부 주소 차이 (프론트가 컨테이너면 `http://backend:8000` 사용)

이제 `/api/diag/health`와 `/api/diag/logs`로 바로 확인 가능합니다.
