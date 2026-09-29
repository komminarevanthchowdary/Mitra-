"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { Brand } from "@/components/Brand";
import { ArrowRight } from "@/components/Icons";
import { useAuth } from "@/lib/auth/AuthProvider";

export function LoginForm() {
  const router = useRouter();
  const { signIn } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setBusy(true);
    try {
      await signIn(email.trim(), password);
      router.push("/portal/");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Sign-in could not be completed.");
    } finally {
      setBusy(false);
    }
  }

  return <section className="auth-page"><div className="site-container">
    <div className="auth-wrap">
      <aside className="auth-aside"><div><Brand /><h1>Good to have you here.</h1><p>Sign in to the Mitra Solar Enterprises team portal to continue.</p></div><span className="auth-aside-note">For authorized team members</span></aside>
      <div className="auth-form-wrap"><span className="eyebrow"><i />Team portal</span><h2>Sign in to your account</h2><p>Use the email address and password provided by your administrator.</p>
        <form className="auth-form" onSubmit={submit}>
          <div className="form-field"><label htmlFor="email">Email address</label><input id="email" type="email" autoComplete="username" required value={email} onChange={(event) => setEmail(event.target.value)} /></div>
          <div className="form-field"><label htmlFor="password">Password</label><input id="password" type="password" autoComplete="current-password" required minLength={12} value={password} onChange={(event) => setPassword(event.target.value)} /></div>
          {error && <p className="form-error" role="alert">{error}</p>}
          <button type="submit" className="button button-dark form-submit" disabled={busy}>{busy ? "Signing in…" : "Sign in"}<ArrowRight /></button>
        </form>
        <p className="auth-help">Need access? <Link href="/contact/">Contact the administrator</Link>. Password recovery will be available after email delivery is configured.</p>
      </div>
    </div>
  </div></section>;
}
