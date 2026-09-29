"use client";

import {
  createContext,
  useEffect,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { apiRequest } from "@/lib/api/client";

export type Role = "SUPER_ADMIN" | "ADMIN" | "STAFF" | "BRANCH";

export type PortalUser = {
  id: string;
  email: string;
  full_name: string;
  role: Role;
  branch_id: string | null;
};

type TokenPair = {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
  expires_in: number;
};

type AuthContextValue = {
  tokens: TokenPair | null;
  user: PortalUser | null;
  setUser: (user: PortalUser | null) => void;
  signIn: (email: string, password: string) => Promise<PortalUser>;
  rotateTokens: () => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [tokens, setTokens] = useState<TokenPair | null>(null);
  const [user, setUser] = useState<PortalUser | null>(null);

  const signIn = useCallback(async (email: string, password: string) => {
    const pair = await apiRequest<TokenPair>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    setTokens(pair);
    try {
      const profile = await apiRequest<PortalUser>("/auth/me", {}, pair.access_token);
      setUser(profile);
      return profile;
    } catch (error) {
      setTokens(null);
      setUser(null);
      throw error;
    }
  }, []);

  const rotateTokens = useCallback(async () => {
    if (!tokens?.refresh_token) throw new Error("Your session has ended. Please sign in again.");
    const pair = await apiRequest<TokenPair>("/auth/refresh", {
      method: "POST",
      body: JSON.stringify({ refresh_token: tokens.refresh_token }),
    });
    setTokens(pair);
  }, [tokens]);

  const signOut = useCallback(async () => {
    const refreshToken = tokens?.refresh_token;
    setTokens(null);
    setUser(null);
    if (!refreshToken) return;
    try {
      await apiRequest<void>("/auth/logout", {
        method: "POST",
        body: JSON.stringify({ refresh_token: refreshToken }),
      });
    } catch {
      // The local session is cleared even if a sleeping API is unavailable.
    }
  }, [tokens]);

  useEffect(() => {
    if (!tokens) return;
    const refreshIn = Math.max((tokens.expires_in - 60) * 1000, 1000);
    const timer = window.setTimeout(() => {
      void rotateTokens().catch(() => { void signOut(); });
    }, refreshIn);
    return () => window.clearTimeout(timer);
  }, [tokens, rotateTokens, signOut]);

  const value = useMemo(
    () => ({ tokens, user, setUser, signIn, rotateTokens, signOut }),
    [tokens, user, signIn, rotateTokens, signOut],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider.");
  return context;
}
