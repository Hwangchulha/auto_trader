# Frontend KeyGate Overlay (v12.7)

**목표:** 메인 화면 포함 "모든 화면"에 버튼/모달로 **키 설정 UI를 즉시 제공** (라우팅/디자인 건드리지 않음)

## 적용 (2단계)
1) 이 폴더의 `public/kis-keygate.js` 를 **여러분 프론트 프로젝트의 `public/` 폴더에 복사**
2) **한 줄 추가**로 스크립트 포함
   - App Router: `app/layout.tsx`에
     ```tsx
     import Script from 'next/script'
     ...
     <Script src="/kis-keygate.js" strategy="afterInteractive" />
     ```
   - Pages Router: `pages/_document.tsx`에
     ```tsx
     <script src="/kis-keygate.js" defer></script>
     ```

이제 모든 페이지 오른쪽 아래에 **🔑 키 설정 버튼(FAB)** 이 나타나며,
키가 없으면 **상단 배너 + 자동 모달 오픈**으로 즉시 안내됩니다.
