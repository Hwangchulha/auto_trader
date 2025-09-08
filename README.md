# KIS Auto Trader — KIS-only (port 8088) v13.3

- 백엔드 포트: **8088**
- 시뮬 모드 없음. KIS(VTS/PROD) 전용.
- 기능: 워치리스트(+행 단위 주문), 대시보드, 계좌, 설정(키 저장)
- 프론트 포트: 3000

## 실행
```bash
copy .env.example .env
# 필요시 .env의 NEXT_PUBLIC_API_BASE를 서버IP로 변경 (예: http://192.168.0.10:8088)

docker compose up -d --build
# Frontend: http://localhost:3000
# Backend : http://localhost:8088/health
```

## 주요 API
- `GET /api/symbols` / `POST /api/symbols?code=...&name=...` / `DELETE /api/symbols?code=...`
- `POST /api/orders` (JSON 또는 x-www-form-urlencoded)
- `GET /api/account/overview`
- `GET /api/keys` / `POST /api/keys`
- `GET /api/settings/runtime`
- `GET /api/diag/env|health|logs|bundle`

## 주의
- 키 저장 전에는 대시보드에서 `needs_keys:true`로 안내합니다.
- 주문은 항상 KIS로 전송됩니다. `rt_cd!="0"`이면 `status=rejected`로 기록됩니다.
