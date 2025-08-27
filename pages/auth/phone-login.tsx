import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useState } from 'react';
import PhoneInput from '../../components/auth/PhoneInput';

export default function PhoneLoginPage() {
	const router = useRouter();
	const [phone, setPhone] = useState('');
	const [loading, setLoading] = useState(false);

	async function handleSendOtp(e: React.FormEvent) {
		e.preventDefault();
		if (phone.length !== 10) return alert('Enter a valid 10-digit phone');
		setLoading(true);
		// Placeholder: integrate with your auth provider (Supabase OTP or custom API)
		await new Promise((r) => setTimeout(r, 600));
		setLoading(false);
		router.push(`/auth/verify-otp?phone=${encodeURIComponent('+91-' + phone)}`);
	}

	return (
		<>
			<Head>
				<title>Login with Phone | Zipzy</title>
			</Head>
			<div className="min-h-screen bg-gradient-to-b from-rose-500 to-fuchsia-600">
				<div className="mx-auto max-w-md px-4 pt-8 pb-16">
					<div className="flex justify-end">
						<Link href="/" className="text-xs text-white/80 rounded-full px-3 py-1 border border-white/30">Skip</Link>
					</div>
					<form onSubmit={handleSendOtp} className="mt-24 space-y-4">
						<PhoneInput value={phone} onChange={setPhone} placeholder="9010858965" />
						<button
							type="submit"
							disabled={loading}
							className="w-full h-12 rounded-lg bg-black text-white text-base font-medium hover:opacity-90 disabled:opacity-60"
						>
							{loading ? 'Sending...' : 'Send OTP'}
						</button>
						<div className="flex items-center gap-2 text-white/70 text-xs">
							<div className="flex-1 h-px bg-white/30" />
							<span>OR</span>
							<div className="flex-1 h-px bg-white/30" />
						</div>
						<div className="grid grid-cols-1 gap-3">
							<button type="button" className="h-12 rounded-lg bg-white text-gray-900 text-sm font-medium border flex items-center justify-center gap-2">
								<span>Continue with Email</span>
							</button>
							<div className="grid grid-cols-2 gap-3">
								<button type="button" className="h-12 rounded-lg bg-white text-gray-900 text-sm font-medium border">Facebook</button>
								<button type="button" className="h-12 rounded-lg bg-white text-gray-900 text-sm font-medium border">Google</button>
							</div>
						</div>
						<p className="text-[10px] text-white/70 text-center pt-2">
							By continuing, you agree to our Terms of Service, Privacy Policy and Content Policy.
						</p>
					</form>
				</div>
			</div>
		</>
	);
}


