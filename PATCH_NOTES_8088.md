# Patch: API port 8088 + Watchlist (FE) + Account overview fix + Orders form support

## 적용 방법 (요약)
1) 아래 zip을 프로젝트 루트( api/ 와 frontend/ 가 있는 곳 )에 풀어쓰기(덮어쓰기) 합니다.
2) `docker compose down -v` 로 중지/볼륨정리 후, `docker compose up -d --build` 로 다시 빌드/기동합니다.
3) 외부 접속 시 프론트엔드: `http://<서버IP>:3000`, 프론트에서 백엔드로는 `http://118.37.64.84:8088` 로 호출합니다.
   (override 파일에 이미 설정되어 있습니다.)
4) 헬스체크: `http://<서버IP>:8088/api/diag/health` 가 `{ "ok": true, ... }` 면 정상입니다.

## 포함 내용
- **백엔드** `app/routers/account.py`
  - KIS 응답이 `dict` 또는 `list` 인 모든 경우를 안전하게 처리하도록 수정
  - 로그의 `'list' object has no attribute 'get'` 예외 해결 (계좌 조회 시 발생) 
- **백엔드** `app/routers/orders.py`
  - JSON *또는* `application/x-www-form-urlencoded` 모두 수용
  - `price <= 0` 이면 **시장가(01)**, 그 외는 **지정가(00)** 로 자동 매핑
  - 응답에 KIS `msg_cd`, `msg1`(오류 메시지) 포함
- **프론트엔드**
  - `lib/api.ts`: 런타임에 `NEXT_PUBLIC_API_BASE` 없으면 `http://<호스트>:8088` 자동 사용
  - `app/page.tsx`: 메인에 **위시리스트**, **설정/키**, **계좌 현황** 버튼 추가
  - `app/watchlist/page.tsx`: 로컬 저장소 기반 위시리스트 + 매수/매도 버튼, **ref 타입 오류(Typescript) 수정**
  - `app/account/page.tsx`: 백엔드 계좌 현황 표시
  - `next.config.js`: `output: 'standalone'` 유지
  - `Dockerfile`: 스탠드얼론 런타임에서 `node server.js` 로 기동, `public/.keep` 포함 복사 오류 방지
- **docker-compose.override.yml**
  - API 포트 8088 오픈/바인딩, 프론트의 `NEXT_PUBLIC_API_BASE` 를 `http://118.37.64.84:8088` 로 지정
- **.env.example.patch**
  - 필수 환경값 샘플

## 왜 매수/매도가 안되었나? (로그 근거)
- UI 오류의 1차 원인은 계좌 조회 API에서 `list` 에 `.get()` 을 호출해 터지는 예외입니다. 이 패치로 해결합니다. (로그 참조)
- 또한 KIS에서 **장 시작 전** 등 사유로 주문이 거부될 때 `msg_cd=40570000` 과 함께 한글 메시지를 돌려줍니다.
  이제 주문 API가 그 메시지를 그대로 반환하므로, 프론트 알림에서 원인을 바로 확인할 수 있습니다.

## 외부 접속 확인 체크리스트
- 방화벽에서 **8088/TCP**(백엔드), **3000/TCP**(프론트) 허용
- `docker compose ps` 로 두 컨테이너가 Up 상태인지 확인
- 브라우저에서 `http://118.37.64.84:3000` 접속 → 메인 화면의 헬스 섹션 OK 확인
- `curl http://118.37.64.84:8088/api/diag/health` → `{ "ok": true, ... }` 확인

## 참고
- 만약 기존 `docker-compose.yml` 에 포트/명령이 이미 정의되어 있다면, 이 패치의
  **docker-compose.override.yml** 이 자동 머지되어 8088 포트가 적용됩니다.
- 실거래(`KIS_ENV=real`)로 전환 시 `.env` 에서 값을 바꾼 후 재기동하세요.
