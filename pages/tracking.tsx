export default function TrackingPage() {
  const steps = ['Order Placed', 'Preparing', 'Picked Up', 'In Transit', 'Delivered'];

  return (
    <div className="container py-6">
      <h1 className="text-2xl font-semibold mb-4">Live Order Tracking</h1>
      <div className="card p-6">
        <div className="mb-4 h-56 w-full rounded-lg bg-gray-100" />
        <ol className="space-y-2">
          {steps.map((s, i) => (
            <li key={s} className="flex items-center gap-3">
              <span className={`h-3 w-3 rounded-full ${i <= 2 ? 'bg-purple-600' : 'bg-gray-300'}`} />
              <span className={i <= 2 ? 'font-medium' : 'text-gray-500'}>{s}</span>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
