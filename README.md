# KIS Auto Trader — KIS-only (Port 8088) v13.6 (Build fix)

- 백엔드 포트 8088
- 워치리스트(매수/매도) + **빌드 에러 수정(TypeScript ref 콜백 반환값 void)**

## 실행
```powershell
copy .env.example .env
docker compose down -v
docker compose up -d --build
# Frontend: http://localhost:3000
# Backend : http://localhost:8088/health
```
