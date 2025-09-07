
import "./styles/globals.css";
export const metadata = { title: "KIS Auto Trader", description: "KR/US Auto Trading Dashboard" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko"><body>
      <div className="max-w-7xl mx-auto px-4 py-6">
        <nav className="flex items-center justify-between py-2">
          <div className="text-lg font-semibold"><a href="/">KIS Auto Trader</a></div>
          <div className="space-x-4 text-sm opacity-80">
            <a href="/watchlist" className="underline">워치리스트</a>
            <a href="/account" className="underline">계좌</a>
            <a href="/settings" className="underline">설정</a>
          </div>
        </nav>
        {children}
      </div>
    </body></html>
  );
}
