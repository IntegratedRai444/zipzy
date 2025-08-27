import { useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Splash() {
  const router = useRouter();
  useEffect(() => {
    const t = setTimeout(() => router.replace('/'), 1500);
    return () => clearTimeout(t);
  }, [router]);

  return (
    <div className="h-screen flex items-center justify-center" style={{ background: 'linear-gradient(135deg,#6d28d9,#ec4899)' }}>
      <div className="text-center text-white">
        <div className="mx-auto mb-4 h-24 w-24 rounded-full bg-white/20 animate-pulse" />
        <h1 className="text-3xl font-semibold tracking-wide">ZIPZY</h1>
        <p className="mt-1 text-sm text-white/80">Remote Delivery for Campus</p>
      </div>
    </div>
  );
}
