import Link from "next/link";

export function Brand({ compact = false }: { compact?: boolean }) {
  return (
    <Link href="/" className="brand" aria-label="Mitra Solar Enterprises home">
      <span className="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 40 40" fill="none">
          <path d="M20 4.5v7M20 28.5v7M4.5 20h7M28.5 20h7M9 9l5 5M26 26l5 5M31 9l-5 5M14 26l-5 5" stroke="currentColor" strokeWidth="2.1" strokeLinecap="round" />
          <circle cx="20" cy="20" r="6.8" stroke="currentColor" strokeWidth="2.1" />
        </svg>
      </span>
      {!compact && (
        <span className="brand-copy">
          <strong>Mitra Solar</strong>
          <small>ENTERPRISES</small>
        </span>
      )}
    </Link>
  );
}
