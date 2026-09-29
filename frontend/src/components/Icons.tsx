import type { SVGProps } from "react";

type IconProps = SVGProps<SVGSVGElement>;

export function ArrowUpRight(props: IconProps) {
  return <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}><path d="M7 17 17 7M8 7h9v9" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" /></svg>;
}

export function ArrowRight(props: IconProps) {
  return <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}><path d="M4.5 12h15m-6-6 6 6-6 6" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" /></svg>;
}

export function SunIcon(props: IconProps) {
  return <svg viewBox="0 0 48 48" fill="none" aria-hidden="true" {...props}><circle cx="24" cy="24" r="7" stroke="currentColor" strokeWidth="1.7"/><path d="M24 5v6m0 26v6M5 24h6m26 0h6M10.6 10.6l4.2 4.2m18.4 18.4 4.2 4.2m0-26.8-4.2 4.2m-18.4 18.4-4.2 4.2" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round"/></svg>;
}
