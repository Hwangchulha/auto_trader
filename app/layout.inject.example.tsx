// 예시: Next.js App Router에서 keygate 스크립트 포함하기
import './globals.css'
import Script from 'next/script'

export const metadata = { title: 'KIS Auto Trader', description: '...' }

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>
        {children}
        {/* 여기에 스크립트 한 줄만 추가하면 전 페이지에서 FAB/모달이 활성화됩니다. */}
        <Script src="/kis-keygate.js" strategy="afterInteractive" />
      </body>
    </html>
  )
}
