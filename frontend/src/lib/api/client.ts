export type ApiError = Error & { status?: number };

export function getApiBaseUrl(): string {
  const configured = process.env.NEXT_PUBLIC_API_URL?.trim();
  if (configured) {
    if (process.env.NODE_ENV === "production" && /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?(?:\/|$)/i.test(configured)) {
      throw new Error("The production site is pointing at a local API URL. Update NEXT_PUBLIC_API_URL and rebuild.");
    }
    return configured.replace(/\/+$/, "");
  }
  if (process.env.NODE_ENV === "development") return "http://localhost:8000/api/v1";
  throw new Error("The API URL has not been configured for this deployment.");
}

export async function apiRequest<T>(
  path: string,
  init: RequestInit = {},
  accessToken?: string,
): Promise<T> {
  const headers = new Headers(init.headers);
  if (init.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  headers.set("Accept", "application/json");
  if (accessToken) headers.set("Authorization", `Bearer ${accessToken}`);

  const url = `${getApiBaseUrl()}${path}`;
  let response: Response;
  try {
    response = await fetch(url, {
      ...init,
      headers,
      cache: "no-store",
    });
  } catch {
    throw new Error("The server is taking a moment to connect. Please try again shortly.");
  }

  if (!response.ok) {
    let message = "Something went wrong. Please try again.";
    try {
      const payload = (await response.json()) as { detail?: string };
      if (payload.detail) message = payload.detail;
    } catch {
      // Keep the plain-language fallback for non-JSON gateway errors.
    }
    const error = new Error(message) as ApiError;
    error.status = response.status;
    throw error;
  }

  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}
