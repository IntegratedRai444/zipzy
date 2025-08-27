export default function PartnerDashboard() {
  return (
    <div className="container py-6">
      <h1 className="text-2xl font-semibold mb-4">Partner Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card p-4">
          <div className="text-sm text-gray-600">Earnings (today)</div>
          <div className="text-2xl font-semibold">₹0</div>
        </div>
        <div className="card p-4">
          <div className="text-sm text-gray-600">Active Orders</div>
          <div className="text-2xl font-semibold">0</div>
        </div>
        <div className="card p-4">
          <div className="text-sm text-gray-600">Rating</div>
          <div className="text-2xl font-semibold">—</div>
        </div>
      </div>
      <div className="mt-6 card p-6">
        <div className="text-sm text-gray-600 mb-2">Incoming Requests</div>
        <div className="text-gray-500">No requests yet.</div>
      </div>
    </div>
  );
}
