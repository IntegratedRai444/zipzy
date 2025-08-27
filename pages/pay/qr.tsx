import { useMemo, useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';

// Simple UPI QR generator page (placeholder). This does not process payments; it
// just constructs a UPI URI and renders a scannable QR using a public QR API.
// Replace this with your production-grade integration (Razorpay / PhonePe / Stripe) later.

const encode = (value: string) => encodeURIComponent(value ?? '');

export default function QrPaymentPage() {
	const [upiId, setUpiId] = useState<string>('zipzy@upi');
	const [name, setName] = useState<string>('Zipzy Payments');
	const [amount, setAmount] = useState<string>('199');
	const [note, setNote] = useState<string>('Zipzy Order');

	const upiUri = useMemo(() => {
		// UPI URI format: upi://pay?pa=<vpa>&pn=<name>&am=<amount>&tn=<note>&cu=INR
		const params = [
			`pa=${encode(upiId)}`,
			`pn=${encode(name)}`,
			amount ? `am=${encode(amount)}` : undefined,
			note ? `tn=${encode(note)}` : undefined,
			`cu=INR`,
		].filter(Boolean);
		return `upi://pay?${params.join('&')}`;
	}, [upiId, name, amount, note]);

	const qrImageUrl = useMemo(() => {
		// Using goqr.me (api.qrserver.com) for quick demo QR rendering
		return `https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=${encodeURIComponent(
			upiUri
		)}`;
	}, [upiUri]);

	return (
		<>
			<Head>
				<title>Pay via UPI QR | Zipzy</title>
			</Head>
			<div className="min-h-screen bg-gray-50">
				<header className="sticky top-0 z-10 bg-white border-b">
					<div className="mx-auto max-w-2xl px-4 py-3 flex items-center justify-between">
						<Link href="/" className="text-sm text-gray-600 hover:text-gray-900">Home</Link>
						<h1 className="text-base font-semibold">UPI QR Payment</h1>
						<div />
					</div>
				</header>

				<main className="mx-auto max-w-2xl px-4 py-6">
					<section className="bg-white rounded-xl border p-4 sm:p-6 shadow-sm">
						<h2 className="text-lg font-semibold mb-4">Payment Details</h2>
						<div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
							<label className="flex flex-col gap-1">
								<span className="text-sm text-gray-600">Pay to UPI ID</span>
								<input
									value={upiId}
									onChange={(e) => setUpiId(e.target.value)}
									className="h-10 rounded-md border px-3 text-sm"
									placeholder="merchant@upi"
								/>
							</label>
							<label className="flex flex-col gap-1">
								<span className="text-sm text-gray-600">Payee Name</span>
								<input
									value={name}
									onChange={(e) => setName(e.target.value)}
									className="h-10 rounded-md border px-3 text-sm"
									placeholder="Zipzy Payments"
								/>
							</label>
							<label className="flex flex-col gap-1">
								<span className="text-sm text-gray-600">Amount (INR)</span>
								<input
									value={amount}
									onChange={(e) => setAmount(e.target.value.replace(/[^0-9.]/g, ''))}
									className="h-10 rounded-md border px-3 text-sm"
									placeholder="199"
								/>
							</label>
							<label className="flex flex-col gap-1 sm:col-span-2">
								<span className="text-sm text-gray-600">Note</span>
								<input
									value={note}
									onChange={(e) => setNote(e.target.value)}
									className="h-10 rounded-md border px-3 text-sm"
									placeholder="Zipzy Order"
								/>
							</label>
						</div>
					</section>

					<section className="mt-6 bg-white rounded-xl border p-4 sm:p-6 shadow-sm">
						<h2 className="text-lg font-semibold mb-4">Scan to Pay</h2>
						<div className="flex flex-col items-center justify-center gap-4">
							<img
								src={qrImageUrl}
								alt="UPI QR Code"
								className="border rounded-lg p-2 bg-white"
								width={240}
								height={240}
							/>
							<a
								href={upiUri}
								target="_blank"
								rel="noreferrer"
								className="inline-flex items-center justify-center h-10 px-4 rounded-md bg-black text-white text-sm font-medium hover:opacity-90"
							>
								Open in UPI app
							</a>
							<p className="text-xs text-gray-500 text-center">
								After paying, return to the app and tap Verify Payment below.
							</p>
							<button
								onClick={() => alert('This is a placeholder. Integrate server-side verification and webhooks.')}
								className="inline-flex items-center justify-center h-10 px-4 rounded-md border text-sm font-medium hover:bg-gray-50"
							>
								Verify Payment
							</button>
						</div>
					</section>

					<section className="mt-6 text-xs text-gray-500">
						<p>
							This screen is for demo only. Do not use in production without a proper payment gateway and server-side verification.
						</p>
					</section>
				</main>
			</div>
		</>
	);
}


