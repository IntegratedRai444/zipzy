import Link from 'next/link';
import BannerCarousel from '../components/home/BannerCarousel';
import CategoryScroller from '../components/home/CategoryScroller';

export default function Home() {
  const categories = [
    { key: 'food', label: 'Food' },
    { key: 'stationery', label: 'Stationery' },
    { key: 'essentials', label: 'Essentials' },
    { key: 'clothing', label: 'Clothing' },
    { key: 'books', label: 'Books' },
    { key: 'custom', label: 'Custom Orders' },
  ];

  return (
    <div className="container py-6">
      <header className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Zipzy</h1>
        <nav className="flex gap-3 text-sm">
          <Link className="btn btn-outline" href="/login">Login</Link>
          <Link className="btn btn-primary" href="/search">Browse</Link>
        </nav>
      </header>

      <div className="mb-6">
        <input className="w-full rounded-lg border px-4 py-2" placeholder="Search items, stores, or categories" />
      </div>

      <section className="mb-8">
        <h2 className="mb-3 text-lg font-medium">Categories</h2>
        <CategoryScroller categories={categories} />
      </section>

      <section>
        <h2 className="mb-3 text-lg font-medium">Offers</h2>
        <BannerCarousel />
      </section>
    </div>
  );
}
