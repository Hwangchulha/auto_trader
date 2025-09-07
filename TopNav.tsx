'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const Item = ({href, children}:{href:string, children:any}) => {
  const path = usePathname();
  const active = path===href || (href!=='/' && path?.startsWith(href));
  return (
    <Link href={href} style={{padding:'8px 12px', color: active ? '#fff' : '#cbd5e1', textDecoration:'none', fontWeight: active ? 700 : 500}}>
      {children}
    </Link>
  );
};

export default function TopNav(){
  return (
    <div style={{position:'sticky', top:0, zIndex:999, backdropFilter:'blur(6px)',
      background:'rgba(15,23,42,.5)', borderBottom:'1px solid #1f2937'}}>
      <div style={{display:'flex', alignItems:'center', gap:8, padding:'8px 12px', maxWidth:1200, margin:'0 auto'}}>
        <div style={{fontWeight:800, color:'#fff'}}>KIS Auto Trader</div>
        <div style={{flex:1}}/>
        <Item href="/">대시보드</Item>
        <Item href="/account">계좌</Item>
        <Item href="/settings">설정</Item>
        <Item href="/keys">키 설정</Item>
      </div>
    </div>
  );
}
