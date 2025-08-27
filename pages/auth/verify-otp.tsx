import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useEffect, useMemo, useRef, useState } from 'react';

function OtpInputs({ length = 6, onComplete }: { length?: number; onComplete: (code: string) => void }) {
	const refs = useRef<Array<HTMLInputElement | null>>([]);
	const [digits, setDigits] = useState<string[]>(Array.from({ length }, () => ''));

	useEffect(() => {
		if (digits.every((d) => d !== '')) {
			onComplete(digits.join(''));
		}
	}, [digits, onComplete]);

	return (
		<div className="flex items-center gap-2">
			{digits.map((d, i) => (
				<input
					key={i}
					ref={(el) => (refs.current[i] = el)}
					value={d}
					onChange={(e) => {
						const v = e.target.value.replace(/[^0-9]/g, '').slice(0, 1);
						setDigits((prev) => {
							const next = [...prev];
							next[i] = v;
							return next;
						});
						if (v && i < length - 1) refs.current[i + 1]?.focus();
					}}
					onKeyDown={(e) => {
						if (e.key === 'Backspace' && !digits[i] && i > 0) refs.current[i - 1]?.focus();
					}}
					className="w-10 h-12 text-center rounded-md border text-lg"
					inputMode="numeric"
					aria-label={`OTP digit ${i + 1}`}
					title={`OTP digit ${i + 1}`}
				/>
			))}
		</div>
	);
}

export default function VerifyOtpPage() {
	const router = useRouter();
	const phone = useMemo(() => (typeof router.query.phone === 'string' ? router.query.phone : ''), [router.query.phone]);
	const [timer, setTimer] = useState<number>(20);
	const [verifying, setVerifying] = useState(false);

	useEffect(() => {
		const id = setInterval(() => setTimer((t) => (t > 0 ? t - 1 : 0)), 1000);
		return () => clearInterval(id);
	}, []);

	async function verify(code: string) {
		setVerifying(true);
		await new Promise((r) => setTimeout(r, 600));
		setVerifying(false);
		router.replace('/');
	}

	return (
		<>
			<Head>
				<title>Verify OTP | Zipzy</title>
			</Head>
			<div className="min-h-screen bg-white">
				<header className="sticky top-0 bg-white border-b">
					<div className="max-w-2xl mx-auto px-4 h-12 flex items-center gap-3">
						<Link href="/auth/phone-login" className="text-sm">←</Link>
						<div className="text-sm">We have sent a verification code to</div>
					</div>
				</header>
				<main className="max-w-2xl mx-auto px-4 py-8">
					<p className="text-center text-sm text-gray-700">{phone}</p>
					<div className="mt-6 flex justify-center">
						<OtpInputs length={6} onComplete={verify} />
					</div>
					<div className="mt-6 text-center text-sm text-gray-600">0:{timer.toString().padStart(2, '0')}</div>
					<div className="mt-6 text-center text-sm">
						Didn’t receive the code?{' '}
						<button className="underline disabled:opacity-50" disabled={timer > 0} onClick={() => setTimer(20)}>
							Resend now
						</button>
					</div>
					<div className="mt-8 flex justify-center">
						<button
							disabled={verifying}
							className="h-11 px-6 rounded-md bg-black text-white text-sm"
							onClick={() => verify('')}
						>
							{verifying ? 'Verifying…' : 'Verify'}
						</button>
					</div>
				</main>
			</div>
		</>
	);
}


