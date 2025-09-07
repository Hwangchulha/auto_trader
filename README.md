# KIS Auto Trader — Clean Pack (v13.0)

- **핵심 정리**
  - 기능 통합: `/api/account/overview`, `/api/symbols`, `/api/orders`, `/api/settings/runtime`, `/api/keys`, `/api/diag/*`
  - **키 입력은 '설정' 페이지(app/settings/page.tsx) 내에 통합**. 별도 경로/오버레이 없음.
  - DB: SQLite(`data/app.db`) — symbols / orders / kis_keys
  - 로깅: `/logs` 매핑(app/error/access/kis/client)

## 실행
```bash
copy .env.example .env   # .env 편집 (기본 SIM_MODE=1)
docker compose up -d --build
# 프론트: http://localhost:3000
# 백엔드: http://localhost:8000/health
```
- KIS 모의 사용: `.env`에서 `SIM_MODE=0`, `KIS_ENV=vts` 그리고 **설정 페이지에서 키 저장**

## 엔드포인트
- `GET /api/account/overview`  잔고/보유/최근주문
- `GET|POST|DELETE /api/symbols`
- `POST /api/orders`           (JSON/폼 모두 OK)
- `GET /api/settings/runtime`
- `GET /api/keys` / `POST /api/keys`
- `GET /api/diag/env|logs|bundle`

## 주의
- 키는 DB에 **평문** 저장(마스킹은 응답 표시용). 운영환경에선 암호화 저장 권장.
