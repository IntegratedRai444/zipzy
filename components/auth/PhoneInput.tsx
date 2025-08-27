import { useState } from 'react';

interface PhoneInputProps {
	value?: string;
	onChange?: (value: string) => void;
	placeholder?: string;
}

export default function PhoneInput({ value, onChange, placeholder }: PhoneInputProps) {
	const [countryCode] = useState<string>('+91');

	return (
		<div className="flex items-center gap-2">
			<div className="px-3 h-12 rounded-lg border bg-white flex items-center text-sm text-gray-700">
				{countryCode}
			</div>
			<input
				type="tel"
				inputMode="numeric"
				value={value}
				onChange={(e) => onChange?.(e.target.value.replace(/[^0-9]/g, ''))}
				className="flex-1 h-12 rounded-lg border px-3 text-base"
				placeholder={placeholder ?? 'Enter phone number'}
				maxLength={10}
			/>
		</div>
	);
}


