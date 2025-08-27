import { useEffect, useState } from 'react';

const demoBanners = [
	{ id: 'b1', title: '60% OFF', subtitle: 'no cooking July' },
	{ id: 'b2', title: ' biiig discounts', subtitle: 'now on your favourites' },
];

export default function BannerCarousel() {
	const [index, setIndex] = useState(0);
	useEffect(() => {
		const id = setInterval(() => setIndex((i) => (i + 1) % demoBanners.length), 3000);
		return () => clearInterval(id);
	}, []);

	return (
		<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
			{demoBanners.map((b, i) => (
				<div key={b.id} className={`rounded-xl p-6 text-white ${i % 2 ? 'bg-indigo-600' : 'bg-rose-500'} ${i === index ? '' : 'opacity-90'}`}>
					<div className="text-2xl font-bold">{b.title}</div>
					<div className="text-sm opacity-90">{b.subtitle}</div>
				</div>
			))}
		</div>
	);
}


