# KIS Auto Trader — KIS-only (Port 8088) v13.5

- 백엔드 포트: **8088**
- 워치리스트 페이지 복원(+ 행 단위 매수/매도 버튼)
- Next.js **standalone 런타임**로 안정 실행
- 키 입력은 **설정 페이지**에서 저장 (시뮬 모드 없음)

## 실행
```powershell
copy .env.example .env
docker compose down -v
docker compose up -d --build
# Frontend: http://localhost:3000
# Backend : http://localhost:8088/health
```

## 주요 경로
- 대시보드: `http://localhost:3000/`
- 워치리스트: `http://localhost:3000/watchlist`
- 계좌: `http://localhost:3000/account`
- 설정: `http://localhost:3000/settings`

## API
- `GET|POST|DELETE /api/symbols`  (워치리스트)
- `POST /api/orders`              (KIS 주문 전송; rt_cd!=0 ⇒ rejected)
- `GET /api/account/overview`     (예수금/주문가능/보유/최근주문)
- `GET /api/keys` / `POST /api/keys`
- `GET /api/settings/runtime`
- `GET /api/diag/env|logs|bundle|health`
