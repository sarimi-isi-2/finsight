# FinSight — Local Development Setup

This guide gets the FinSight monorepo running on your machine: **Next.js web app**, **NestJS GraphQL API**, **Flask AI service**, **PostgreSQL**, and **Redis**.

Owner: FH (initial setup, Week 1). If something in this guide is out of date, please fix it directly rather than asking around Slack — that's the point of this doc.

---

## 1. Prerequisites

Install these before anything else:

| Tool | Version | Check with |
|---|---|---|
| Node.js | 20.x LTS | `node -v` |
| pnpm | latest | `pnpm -v` (install: `npm i -g pnpm`) |
| Docker Desktop (or Docker Engine + Compose) | latest | `docker -v` |
| Python | 3.11+ | `python3 -v` |
| Git | any recent | `git -v` |

You'll also need:

- A GitHub account added to the `finsight` repo
- The shared `.env` values from [wherever the team stores secrets — 1Password/Bitwarden vault, ask SL]

---

## 2. Clone the repo

```bash
git clone git@github.com:<org>/finsight.git
cd finsight
git checkout develop
```

We work off `develop` day-to-day and open PRs into it. `main` is production-only — see [Branching & Workflow](#6-branching--workflow) below.

---

## 3. Install dependencies

From the repo root (this installs all workspaces at once via pnpm):

```bash
pnpm install
```

For the AI service (Python, not part of the pnpm workspace):

```bash
cd apps/ai-service
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ../..
```

---

## 4. Start local infrastructure (Postgres + Redis)

```bash
docker compose up -d
```

This starts:

- **PostgreSQL** on `localhost:5432` (user: `finsight`, password: `finsight`, db: `finsight`)
- **Redis** on `localhost:6379`

Check they're running:

```bash
docker compose ps
```

To stop everything: `docker compose down`. To wipe the database volume and start fresh: `docker compose down -v`.

---

## 5. Environment variables

Each app has its own `.env.example` — copy it and fill in real values.

```bash
cp apps/web/.env.example apps/web/.env.local
cp apps/api/.env.example apps/api/.env
cp apps/ai-service/.env.example apps/ai-service/.env
```

**`apps/web/.env.local`**

```
NEXT_PUBLIC_API_URL=http://localhost:4000/graphql
NEXT_PUBLIC_WS_URL=ws://localhost:4000/graphql
```

**`apps/api/.env`**

```
DATABASE_URL=postgresql://finsight:finsight@localhost:5432/finsight
REDIS_URL=redis://localhost:6379
JWT_SECRET=<ask SL for the shared dev secret>
JWT_REFRESH_SECRET=<ask SL>
AI_SERVICE_URL=http://localhost:5000
PORT=4000
```

**`apps/ai-service/.env`**

```
REDIS_URL=redis://localhost:6379
LLM_API_KEY=<your own API key or shared dev key from IJ/DA>
FLASK_ENV=development
PORT=5000
```

Never commit a real `.env` file — only `.env.example` files with placeholder values belong in Git.

---

## 6. Database migrations (Prisma)

```bash
cd apps/api
npx prisma migrate dev
npx prisma generate
```

If you want to inspect the database visually:

```bash
npx prisma studio
```

Opens at `http://localhost:5555`.

---

## 7. Run everything

From the repo root:

```bash
pnpm dev
```

This runs `web` and `api` in parallel via TurboRepo. In a **separate terminal**, start the AI service (it's Python, so it's outside the Turbo pipeline for now):

```bash
cd apps/ai-service
source venv/bin/activate
flask run --port 5000
```

You should now have:

| Service | URL |
|---|---|
| Web (Next.js) | <http://localhost:3000> |
| API (GraphQL) | <http://localhost:4000/graphql> |
| AI Service | <http://localhost:5000/api/v1/health> |

Hit the AI health check to confirm it's up:

```bash
curl http://localhost:5000/api/v1/health
```

---

## 8. Running tests

```bash
pnpm turbo run lint test        # lint + unit tests across web and api
```

For the AI service:

```bash
cd apps/ai-service
source venv/bin/activate
pytest
```

E2E (Cypress) — once configured in `apps/web`:

```bash
cd apps/web
pnpm cypress open
```

---

## 9. Branching & Workflow

We follow Git Flow (per the PRD, Appendix C):

- `main` — production, protected, deploys automatically
- `develop` — integration branch, protected, this is your PR target
- `feature/<short-description>` — your working branches, cut from `develop`

```bash
git checkout develop
git pull
git checkout -b feature/wallet-transaction-api
# ...work, commit using Conventional Commits...
git push -u origin feature/wallet-transaction-api
# open a PR into develop, request 1 review
```

**Commit convention** (Conventional Commits):

```
feat: add transaction categorization endpoint
fix: correct budget progress calculation
chore: update prisma schema
docs: update SETUP.md
```

---

## 10. Module ownership (who to ask)

Per the PRD team assignments — if something in a module is broken or unclear, go to the owner first:

| Module | Owner |
|---|---|
| Auth, Wallet/Transaction | FH |
| Budget, Dashboard | SH |
| Subscription/Payment, Notification, deployment/infra | SL |
| AI categorization (`/api/v1/categorize`) | DA |
| AI chat (`/api/v1/chat`) | IJ |
| Design system, mockups | NS |

---

## 11. Common issues

| Problem | Fix |
|---|---|
| `docker compose up` fails on port 5432/6379 already in use | Stop any local Postgres/Redis you already have running, or change the port mapping in `docker-compose.yml` |
| Prisma migration fails with connection error | Confirm `docker compose ps` shows Postgres as healthy before running `prisma migrate dev` |
| `pnpm install` errors on the Python app | That's expected — `ai-service` isn't a pnpm workspace, it's installed separately via `pip` (Step 3) |
| GraphQL playground shows no schema | Make sure `apps/api` started without errors — check the terminal for a stack trace |
| AI service can't reach Redis | Confirm `REDIS_URL` in `apps/ai-service/.env` matches the Docker Compose service, and that Docker is running |

If you hit something not listed here, add it to this table in your PR — future-you (and everyone else) will thank you.

---

*Questions not answered here → ask in the team channel before pinging someone 1:1, so the answer helps everyone.*
