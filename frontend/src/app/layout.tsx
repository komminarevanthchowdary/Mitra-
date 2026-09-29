import type { Metadata } from "next";
import type { ReactNode } from "react";
import { AuthProvider } from "@/lib/auth/AuthProvider";
import { PublicFooter } from "@/components/PublicFooter";
import { PublicHeader } from "@/components/PublicHeader";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Mitra Solar Enterprises | Solar, Storage & Backup Power",
    template: "%s | Mitra Solar Enterprises",
  },
  description:
    "Explore solar, battery, inverter and UPS options with Mitra Solar Enterprises in Tanuku, Andhra Pradesh.",
  robots: { index: true, follow: true },
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <PublicHeader />
          <main>{children}</main>
          <PublicFooter />
        </AuthProvider>
      </body>
    </html>
  );
}
