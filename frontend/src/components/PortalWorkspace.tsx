"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiRequest, type ApiError } from "@/lib/api/client";
import { useAuth, type PortalUser } from "@/lib/auth/AuthProvider";

const roleNames = { SUPER_ADMIN: "Super Admin", ADMIN: "Admin", STAFF: "Staff", BRANCH: "Branch" } as const;

export function PortalWorkspace() {
  const router = useRouter();
  const { tokens, user, setUser, signOut } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    if (!tokens?.access_token) {
      router.replace("/login/");
      return () => { active = false; };
    }
    apiRequest<PortalUser>("/auth/me", {}, tokens.access_token)
      .then((profile) => { if (active) setUser(profile); })
      .catch((caught: ApiError) => {
        if (!active) return;
        if (caught.status === 401) {
          setError("Your session has ended. Please sign in again.");
          void signOut();
          router.replace("/login/");
        } else setError(caught.message);
      })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [tokens, router, setUser, signOut]);

  if (loading) return <section className="portal-page"><div className="site-container"><div className="portal-card"><p role="status">Connecting to your account…</p></div></div></section>;
  if (!user) return <section className="portal-page"><div className="site-container"><div className="portal-card"><p role="alert">{error || "Redirecting to sign in…"}</p></div></div></section>;

  return <section className="portal-page"><div className="site-container"><div className="portal-card">
    <div className="portal-top"><div><span className="eyebrow"><i />Team portal</span><h1>Welcome, {user.full_name.split(" ")[0]}.</h1><p>You are signed in as {user.email}.</p></div><button className="button button-dark" type="button" onClick={() => { void signOut(); router.replace("/login/"); }}>Sign out</button></div>
    <span className="portal-role">{roleNames[user.role]}</span>
    <div className="portal-panel"><h2>Portal foundation is ready</h2><p>The account and role boundary are connected. The lead workspace and administrative screens will be added in the next build phase.</p>
      <div className="portal-list"><div><strong>Role-aware API</strong><span>Permissions are checked by FastAPI for every request.</span></div><div><strong>Branch isolation</strong><span>Branch access is scoped from your authenticated account.</span></div><div><strong>Lead privacy</strong><span>Staff API responses do not include internal status or notes.</span></div></div>
    </div>
  </div></div></section>;
}
