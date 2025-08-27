import Link from 'next/link';

export default function AdminPage() {
  return (
    <div className="container py-6">
      <h1 className="text-2xl font-semibold mb-4">Admin Panel</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link className="card p-4" href="#">Users</Link>
        <Link className="card p-4" href="#">Orders</Link>
        <Link className="card p-4" href="#">Payments</Link>
        <Link className="card p-4" href="#">Partners</Link>
        <Link className="card p-4" href="#">Catalog</Link>
        <Link className="card p-4" href="#">Reports</Link>
      </div>
    </div>
  );
}
