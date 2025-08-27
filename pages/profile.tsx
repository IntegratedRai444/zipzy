export default function ProfilePage() {
  return (
    <div className="container py-6">
      <h1 className="text-2xl font-semibold mb-4">Profile</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card p-6">
          <div className="text-sm text-gray-600 mb-2">Student Details</div>
          <div className="space-y-1 text-sm">
            <div>Name: Rishabh kapoor</div>
            <div>Email: admin@zipzy.com</div>
            <div>Phone: +918091273304</div>
            <div>Student ID: GF202455815</div>
          </div>
        </div>
        <div className="card p-6">
          <div className="text-sm text-gray-600 mb-2">Saved Addresses</div>
          <div className="text-sm">Hostel · Classroom · Home</div>
        </div>
        <div className="card p-6 md:col-span-2">
          <div className="text-sm text-gray-600 mb-2">Order History</div>
          <div className="text-sm text-gray-500">No orders yet.</div>
        </div>
      </div>
    </div>
  );
}
