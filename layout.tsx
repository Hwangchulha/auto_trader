import './globals.css';
import TopNav from '../components/TopNav';
import KeyFab from '../components/KeyFab';
import NeedKeysBanner from '../components/NeedKeysBanner';

export const metadata = { title: 'KIS Auto Trader' };

export default function RootLayout({ children }:{ children: React.ReactNode }){
  return (
    <html lang="ko">
      <body style={{background:'#0b0f17', color:'#e5e7eb'}}>
        <TopNav/>
        <NeedKeysBanner/>
        <div style={{maxWidth:1200, margin:'0 auto', padding:'12px'}}>
          {children}
        </div>
        <KeyFab/>
      </body>
    </html>
  );
}
