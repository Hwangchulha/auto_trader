# KIS VTS + Diagnostics Patch v12.2 (Frontend 무변경)

이 버전은 **로그가 안 떨어질 때 즉시 확인**할 수 있도록 아래 기능을 추가합니다.
- `/api/diag/touch` : 모든 로그에 테스트 라인을 강제로 기록 → 파일 경로와 결과 즉시 반환
- `/api/diag/log-config` : 어떤 로거에 어떤 핸들러(파일)가 달렸는지 덤프
- `/api/diag/env` : 마스킹된 환경 + 실제 사용 중인 LOG_DIR 공개
- `/api/diag/raise` : 의도적 예외 발생 → error.log 기록 확인

## 통합 순서
1) `backend/app/...` 폴더를 기존 프로젝트의 같은 위치에 **그대로 복사**합니다. (기존 파일 미변경)
2) `backend/requirements.txt`에 없으면 추가: `httpx==0.27.0`, `python-multipart==0.0.9`
3) `backend/app/main.py` 초반에 다음 두 줄이 있는지 확인(없다면 추가):
   ```python
   from app.logging_setup import setup_logging
   setup_logging()
   ```
4) FastAPI app 생성 후, 라우터/미들웨어 추가:
   ```python
   from app.middleware_logging import RequestContextMiddleware
   app.add_middleware(RequestContextMiddleware)

   from app.routers import kis_account, kis_orders, diag
   app.include_router(kis_account.router)
   app.include_router(kis_orders.router)
   app.include_router(diag.router)
   ```
5) Docker 권장 볼륨 (호스트에서 파일 보이게):
   ```yaml
   services:
     backend:
       volumes:
         - ./logs:/app/logs
   ```
6) `.env` 예시
   ```env
   SIM_MODE=0
   KIS_ENV=vts
   KIS_APP_KEY=모의앱키
   KIS_APP_SECRET=모의시크릿
   KIS_CANO=계좌앞8자리
   KIS_ACNT_PRDT_CD=01

   LOG_DIR=/app/logs       # 기본값
   LOG_LEVEL=INFO
   LOG_MAX_BYTES=5242880
   LOG_BACKUP_COUNT=5
   LOG_TO_STDOUT=1
   ```

## "로그가 안 떨어질 때" 체크리스트
1) `GET /api/diag/env`  → `resolved_log_dir` 확인 (어디에 쓰려고 하는지)
2) `GET /api/diag/touch` → app/kis/error/access/client 로그 각각 **1줄 이상** 써지는지, 파일 경로/크기 확인
3) 파일이 보이지 않으면:
   - Docker: `docker compose exec backend ls -al /app/logs`
   - 볼륨 매핑 재확인: `./logs:/app/logs` (호스트 `./logs`에 `app.log` 생겨야 정상)
   - 권한 문제: Windows라면 `./logs` 폴더를 미리 만들고 실행 (쓰기권한)
4) `GET /api/diag/log-config` → 핸들러들이 파일로 달렸는지 확인
5) `GET /api/diag/raise` → `error.log`에 스택 트레이스 떨어지는지 확인
