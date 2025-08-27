export default function SearchPage() {
  return (
    <div className="container py-6">
      <h1 className="text-2xl font-semibold mb-4">Search</h1>
      <div className="mb-4 grid grid-cols-2 sm:grid-cols-4 gap-2">
        <input className="rounded-lg border px-3 py-2" placeholder="Keyword" />
        <select className="rounded-lg border px-3 py-2"><option>All</option><option>Food</option><option>Stationery</option></select>
        <select className="rounded-lg border px-3 py-2"><option>Popularity</option><option>Price</option></select>
        <button className="btn btn-outline">Apply</button>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="card p-4">
            <div className="mb-3 h-28 w-full rounded-lg bg-gray-100" />
            <div className="text-sm font-medium">Sample Item {i + 1}</div>
            <div className="text-xs text-gray-500">Vendor · 25-35 min</div>
            <button className="btn btn-primary w-full mt-3">Add</button>
          </div>
        ))}
      </div>
    </div>
  );
}
