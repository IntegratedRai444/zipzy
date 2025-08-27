import { useState } from 'react';

export default function Signup() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [collegeId, setCollegeId] = useState('');
  const [password, setPassword] = useState('');

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Signup submitted for ${name} (${collegeId})`);
  };

  return (
    <div className="container py-10 max-w-md">
      <h1 className="text-2xl font-semibold mb-4">Create account</h1>
      <form onSubmit={onSubmit} className="card p-6 space-y-4">
        <div>
          <label className="block text-sm mb-1">Full name</label>
          <input className="w-full rounded-lg border px-3 py-2" value={name} onChange={(e)=>setName(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Email</label>
          <input className="w-full rounded-lg border px-3 py-2" value={email} onChange={(e)=>setEmail(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">College ID</label>
          <input className="w-full rounded-lg border px-3 py-2" value={collegeId} onChange={(e)=>setCollegeId(e.target.value)} placeholder="GF202455815" />
        </div>
        <div>
          <label className="block text-sm mb-1">Password</label>
          <input type="password" className="w-full rounded-lg border px-3 py-2" value={password} onChange={(e)=>setPassword(e.target.value)} />
        </div>
        <button className="btn btn-primary w-full" type="submit">Create account</button>
      </form>
    </div>
  );
}
