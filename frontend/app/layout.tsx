import './globals.css'
import Link from 'next/link'

export const metadata = { title: 'KIS Auto Trader', description: 'KIS-only dashboard' }

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>
        <div className="container">
          <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', margin:'12px 0'}}>
            <div style={{fontWeight:800}}>KIS Auto Trader</div>
            <div className="nav">
              <Link href="/">대시보드</Link>
              <Link href="/watchlist">워치리스트</Link>
              <Link href="/account">계좌</Link>
              <Link href="/settings">설정</Link>
            </div>
          </div>
          {children}
        </div>
      </body>
    </html>
  )
}
