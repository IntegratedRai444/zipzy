import Link from 'next/link';

interface CategoryScrollerProps {
	categories: Array<{ key: string; label: string; icon?: string }>;
}

export default function CategoryScroller({ categories }: CategoryScrollerProps) {
	return (
		<div className="flex gap-4 overflow-x-auto no-scrollbar py-1">
			{categories.map((c) => (
				<Link key={c.key} href={`/search?category=${c.key}`} className="flex-shrink-0 w-20 text-center">
					<div className="mx-auto w-16 h-16 rounded-full border flex items-center justify-center bg-white">
						<span className="text-sm">{c.icon ?? '🍽️'}</span>
					</div>
					<div className="mt-1 text-xs text-gray-700 truncate">{c.label}</div>
				</Link>
			))}
		</div>
	);
}


