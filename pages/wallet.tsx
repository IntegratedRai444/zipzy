export default function WalletPage() {
  return (
    <div className="container py-6">
      <h1 className="text-2xl font-semibold mb-4">Zipzy Wallet</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6">
          <div className="text-sm text-gray-600">Balance</div>
          <div className="text-3xl font-semibold mt-1">₹0</div>
        </div>
        <div className="md:col-span-2 card p-6">
          <div className="text-sm text-gray-600 mb-2">Transactions</div>
          <div className="text-sm text-gray-500">No transactions yet.</div>
        </div>
      </div>
    </div>
  );
}
