import Link from 'next/link';

export default function Products() {
  const vendors = ['Canteen A', 'Local Tiffin', 'Grocery Hub', 'Stationery Store'];
  return (
    <div className="container py-6">
      <h1 className="text-2xl font-semibold mb-4">Vendors</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {vendors.map((v, i) => (
          <Link key={v} href={`/products/${i + 1}`} className="card p-4 hover:shadow">
            <div className="mb-3 h-32 w-full rounded-lg bg-gray-100" />
            <div className="font-medium">{v}</div>
            <div className="text-xs text-gray-500">Open · 25-35 min</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
