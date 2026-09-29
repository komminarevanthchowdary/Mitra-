import type { Metadata } from "next";
import { PortalWorkspace } from "@/components/PortalWorkspace";

export const metadata: Metadata = {
  title: "Team Portal",
  robots: { index: false, follow: false },
};

export default function PortalPage() {
  return <PortalWorkspace />;
}
