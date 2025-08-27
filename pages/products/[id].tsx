import { useRouter } from 'next/router';

export default function ProductDetails() {
  const { query } = useRouter();
  const id = query.id;

  return (
    <div className="container py-6">
      <div className="mb-4">
        <div className="h-48 w-full rounded-xl bg-gray-100" />
      </div>
      <h1 className="text-2xl font-semibold mb-1">Sample Vendor #{id}</h1>
      <p className="text-sm text-gray-600 mb-4">Healthy food · South Indian · 40 mins</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="card p-4">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="font-medium">Plant Protein Bowl</div>
                  <div className="text-xs text-gray-500">Veg · Bestseller</div>
                  <div className="mt-2 text-sm">₹199</div>
                </div>
                <div className="h-20 w-28 rounded-lg bg-gray-100" />
              </div>
              <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
                {['Paneer','Extra Veggies','Mushroom','Corn','Chilli Paneer'].map((opt)=> (
                  <label key={opt} className="flex items-center gap-2"><input type="checkbox"/> {opt}</label>
                ))}
              </div>
              <div className="mt-3 flex items-center gap-2">
                <button className="btn btn-outline">-</button>
                <span>1</span>
                <button className="btn btn-outline">+</button>
                <button className="btn btn-primary ml-auto">Add ₹199</button>
              </div>
            </div>
          ))}
        </div>

        <aside className="space-y-4">
          <div className="card p-4">
            <div className="text-sm text-gray-600">Offers</div>
            <div className="mt-2 text-sm">Use code ZIPZY30 for 30% OFF up to ₹75</div>
          </div>
          <div className="card p-4">
            <div className="text-sm text-gray-600 mb-2">Cart</div>
            <div className="text-gray-500 text-sm">No items yet.</div>
          </div>
        </aside>
      </div>
    </div>
  );
}
