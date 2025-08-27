import Link from 'next/link';

export default function CartPage() {
  return (
    <div className="container py-6">
      <h1 className="text-2xl font-semibold mb-4">Your Cart</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-4">
          {Array.from({ length: 2 }).map((_, i) => (
            <div key={i} className="card p-4 flex items-center justify-between">
              <div>
                <div className="font-medium">Item {i + 1}</div>
                <div className="text-xs text-gray-500">Options and notes</div>
              </div>
              <div className="flex items-center gap-2">
                <button className="btn btn-outline">-</button>
                <span>1</span>
                <button className="btn btn-outline">+</button>
              </div>
            </div>
          ))}
        </div>

        <div className="space-y-4">
          <div className="card p-4">
            <div className="mb-2 text-sm text-gray-600">Deliver to</div>
            <select className="w-full rounded-lg border px-3 py-2">
              <option>Hostel</option>
              <option>Classroom</option>
              <option>Custom</option>
            </select>
          </div>

          <div className="card p-4">
            <div className="mb-2 text-sm text-gray-600">Payment</div>
            <div className="grid grid-cols-2 gap-2">
              <button className="btn btn-outline">UPI</button>
              <button className="btn btn-outline">QR</button>
              <button className="btn btn-outline">Wallet</button>
              <button className="btn btn-outline">COD</button>
            </div>
          </div>

          <div className="card p-4">
            <div className="flex items-center justify-between text-sm">
              <span>Subtotal</span><span>₹0</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span>Delivery</span><span>₹0</span>
            </div>
            <div className="mt-2 flex items-center justify-between font-semibold">
              <span>Total</span><span>₹0</span>
            </div>
            <Link className="btn btn-primary w-full mt-3" href="/tracking">Continue to payment</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
