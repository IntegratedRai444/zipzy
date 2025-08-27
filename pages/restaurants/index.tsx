import Link from 'next/link';

interface RestaurantCardProps {
	id: string;
	name: string;
	cuisine: string;
	eta: string;
	rating: number;
}

function RestaurantCard({ id, name, cuisine, eta, rating }: RestaurantCardProps) {
	return (
		<Link href={`/restaurants/${id}`} className="block rounded-xl border p-4 hover:shadow">
			<div className="flex items-center justify-between">
				<div>
					<div className="font-semibold">{name}</div>
					<div className="text-xs text-gray-600">{cuisine}</div>
				</div>
				<div className="text-xs text-gray-700">{eta}</div>
			</div>
			<div className="mt-2 text-sm">⭐ {rating.toFixed(1)}</div>
		</Link>
	);
}

export default function RestaurantsListPage() {
	const list: RestaurantCardProps[] = [
		{ id: 'eat-healthy', name: 'Eat Healthy', cuisine: 'South Indian', eta: '40 mins', rating: 4.2 },
		{ id: 'pizza-place', name: 'Campus Pizza', cuisine: 'Italian, Fast Food', eta: '30 mins', rating: 4.4 },
		{ id: 'biryani-house', name: 'Biryani House', cuisine: 'Hyderabadi', eta: '45 mins', rating: 4.1 },
	];

	return (
		<div className="container py-6">
			<header className="mb-4 flex items-center justify-between">
				<div className="text-xl font-semibold">Restaurants</div>
				<Link href="/" className="text-sm">Home</Link>
			</header>

			<div className="mb-4 flex gap-2">
				<select className="h-10 rounded-md border px-3 text-sm">
					<option>All Cuisines</option>
					<option>South Indian</option>
					<option>Italian</option>
					<option>Hyderabadi</option>
				</select>
				<select className="h-10 rounded-md border px-3 text-sm">
					<option>Sort by: Popular</option>
					<option>Rating</option>
					<option>ETA</option>
				</select>
			</div>

			<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
				{list.map((r) => (
					<RestaurantCard key={r.id} {...r} />
				))}
			</div>
		</div>
	);
}
