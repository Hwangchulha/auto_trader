// 예시: Next.js Pages Router에서 keygate 스크립트 포함하기
import Document, { Html, Head, Main, NextScript } from 'next/document'

export default class MyDocument extends Document {
  render() {
    return (
      <Html lang="ko">
        <Head />
        <body>
          <Main />
          <NextScript />
          {/* 전 페이지 공통으로 FAB/모달 활성화 */}
          <script src="/kis-keygate.js" defer></script>
        </body>
      </Html>
    )
  }
}
