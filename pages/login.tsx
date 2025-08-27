import Link from 'next/link';
import { useState } from 'react';
import { useAuthStore } from '@/store/auth';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const loginWithCredentials = useAuthStore((s) => s.loginWithCredentials);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const ok = loginWithCredentials(email, password);
    if (!ok) setError('Invalid credentials or not authorized');
  };

  return (
    <div className="container py-10 max-w-md">
      <h1 className="text-2xl font-semibold mb-4">Sign in</h1>
      <form onSubmit={onSubmit} className="card p-6 space-y-4">
        <div>
          <label className="block text-sm mb-1">Email or Name</label>
          <input className="w-full rounded-lg border px-3 py-2" value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="Rishabh kapoor or admin@zipzy.com" />
        </div>
        <div>
          <label className="block text-sm mb-1">Password</label>
          <input type="password" className="w-full rounded-lg border px-3 py-2" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="••••••••" />
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button className="btn btn-primary w-full" type="submit">Continue</button>
        <p className="text-xs text-gray-500">Admin password: Rishabhkapoor@0444</p>
      </form>
      <div className="mt-4 text-sm">
        New here? <Link className="text-purple-700 underline" href="/signup">Create account</Link>
      </div>
    </div>
  );
}
