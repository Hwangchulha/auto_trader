// frontend/lib/api.ts
export function getApiBase(): string {
  const env = process.env.NEXT_PUBLIC_API_BASE;
  if (env && env.trim().length > 0) return env;
  if (typeof window !== 'undefined') {
    return `http://${window.location.hostname}:8088`;
  }
  return 'http://localhost:8088';
}

export async function api(path: string, init?: RequestInit) {
  const base = getApiBase();
  const url = path.startsWith('http') ? path : `${base}${path}`;
  const res = await fetch(url, init);
  if (!res.ok) {
    const text = await res.text().catch(()=>'');
    throw new Error(`HTTP ${res.status} ${res.statusText}: ${text}`);
  }
  return res.json();
}
