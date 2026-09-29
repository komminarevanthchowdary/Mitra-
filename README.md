# Mitra Solar Enterprises

Two separately deployable applications for the Mitra Solar Enterprises public website and lead portal:

- `frontend/` — Next.js, React, TypeScript and Tailwind CSS, exported as static files for Cloudflare Pages.
- `backend/` — FastAPI, SQLAlchemy, Alembic and PostgreSQL for the REST API.

The application follows the attached development guide. The portfolio starts empty until verified projects are supplied. No certifications, performance figures, customer counts or other unverified claims are included.

## Local development

Use Node.js 22 LTS or newer and Python 3.12. A PostgreSQL database is required; a Neon development database works, or use any local PostgreSQL instance.

### Backend

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Set DATABASE_URL and JWT_SECRET in .env before continuing.
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

The API health check is at `http://localhost:8000/health`. OpenAPI docs are enabled only outside production at `http://localhost:8000/docs`.

Create the first administrator interactively (the password is read without echo and is never stored in the shell history):

```powershell
python -m app.scripts.create_super_admin --email owner@example.com --name "Mitra Administrator"
```

### Frontend

```powershell
cd frontend
npm ci
Copy-Item .env.example .env.local
npm run dev
```

The public website runs at `http://localhost:3000`. Set `NEXT_PUBLIC_API_URL` in `frontend/.env.local` to the API base URL, for example `http://localhost:8000/api/v1`.

## Public pages

- `/` — Home
- `/services/` — Services
- `/our-work/` — Our Work (empty until verified project records are added)
- `/quality/` — Quality
- `/contact/` — Contact Us and enquiry form
- `/login/` — Portal sign-in
- `/portal/` — Authenticated portal entry point

The frontend uses Next.js static export and browser-side API requests; it does not rely on Next.js server actions, route handlers or a Node server at runtime.

## API foundation

The API is versioned under `/api/v1` and currently includes:

- `GET /health`
- `GET /api/v1/services`, `GET /api/v1/projects`
- `POST /api/v1/contact`
- `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout`, `GET /api/v1/auth/me`
- `GET /api/v1/leads`, `POST /api/v1/leads`, `GET /api/v1/leads/{id}`, `PATCH /api/v1/leads/{id}/status`

Lead reads are serialized with role-specific schemas. Staff responses omit status, status history and internal notes at the API boundary. Branch records are scoped from the authenticated user's branch ID; the API does not trust a branch ID supplied by a Branch user. Status changes create history and audit records in the same transaction.

The database schema includes users, branches, services, projects, contact enquiries, leads, status history, refresh tokens and audit logs. Manage future schema changes with Alembic migrations; do not edit a deployed database by hand.

## Deployment handoff

The guide's zero-cost MVP path is Cloudflare Pages + Render + Neon:

1. Deploy the repository's `frontend/` directory to Cloudflare Pages. Build command: `npm run build`; output directory: `out`. Set `NEXT_PUBLIC_API_URL` to the deployed API's `/api/v1` base URL.
2. Create a Neon PostgreSQL database and set its SQLAlchemy URL on the API service as `postgresql+psycopg://...` (use TLS/SSL as required by the provider).
3. Deploy `backend/` as a Render Python web service. Install command: `pip install -r requirements.txt`. Start command: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Set `ENVIRONMENT=production`, `DATABASE_URL`, a cryptographically random `JWT_SECRET` of at least 32 characters, and `FRONTEND_ORIGINS` to the exact deployed frontend origin(s), comma-separated.
4. Create the first administrator using the one-time script against the deployed database. Do not put the password in source control or a deployment command.
5. Add the production API origin to frontend build variables and the frontend origin to API CORS settings, then redeploy.

Free plans are suitable for MVPs and pilots, not an uptime guarantee. The guide notes that Render's free service sleeps after inactivity; allow for cold-start latency. Recheck provider pricing, quotas and terms before launch because they change. For a commercial go-live with reliable availability, budget for a paid API instance and use a company-owned domain.

### Authentication deployment note

This initial split-domain MVP keeps access and refresh tokens in JavaScript memory only: reloading the tab requires signing in again, and tokens are not written to local or session storage. This avoids persistent browser token storage. Before a business launch, place the site and API under one company-owned root domain and move refresh-token handling to a `Secure`, `HttpOnly`, `SameSite` cookie with CSRF protection. The free `pages.dev` and `onrender.com` hostnames are different sites, and browsers may block cross-site cookies.

## Operational follow-up before collecting real leads

- Add provider-side rate limits and bot controls to login and contact endpoints.
- Configure database backups and test a restore.
- Set a retention period and deletion workflow for enquiry/lead personal data.
- Add monitoring and alerting for API errors, migration failures and database quota usage.
- Add automated authorization and integration tests, then run the public-page responsive/accessibility review before release.

The code here is a production-minded foundation, not a completed commercial launch: account management, password recovery, content administration, reporting, and full operational controls still need implementation.

The current frontend lock pins Next.js 16.3.7, the published patch available from npm during setup. Upstream announced 16.3.8 for the September 30, 2026 security release, but npm still returned `ETARGET` for 16.3.8 when the lockfile was generated. Upgrade Next.js and regenerate the lockfile before public deployment once 16.3.8 is available.
