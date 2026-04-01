# PodGap AI

Podcast topic discovery: niche gap analysis, intersection finder, trend intelligence, title generator, and competitive map.

## Stack

- **Backend:** Python 3.11+, FastAPI, PostgreSQL (async), Redis, Celery, Ollama (local LLM + embeddings)
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS
- **Local dev:** DDEV + Docker (PostgreSQL, Redis, RabbitMQ; optional Ollama in Docker)

## Quick start

### 1. Start services (DDEV + Docker)

From project root:

```bash
# If using DDEV
ddev start

# Or without DDEV: start only DB, Redis, RabbitMQ
docker compose up -d db redis rabbitmq
# Optional: Ollama in Docker
docker compose --profile ollama up -d ollama
```

Ensure `.env` exists (copy from `.env.example`) and `DATABASE_URL` points to your DB (e.g. `postgresql://podgap:podgap@db:5432/podgap` when using DDEV’s `db` service).

### 2. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
# Set DATABASE_URL etc. in .env (or export)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local   # set NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
npm run dev
```

App: http://localhost:3000

## Project layout

```
podgap-ai/
├── backend/           # FastAPI app
│   ├── app/
│   │   ├── api/       # Routes: auth, niche-gap, trends, titles, etc.
│   │   ├── core/      # Config, security (JWT)
│   │   ├── db/        # SQLAlchemy, session
│   │   └── models/    # User, etc.
│   └── requirements.txt
├── frontend/          # Next.js 14 (App Router)
│   └── src/
│       ├── app/       # Pages: (tools)/dashboard, niche-gap, trends, titles, competitive-map
│       ├── components/
│       └── lib/       # API client
├── .ddev/             # DDEV config + extra services (db, redis, rabbitmq)
├── docker-compose.yaml
└── .env.example
```

## Features (MVP)

- **Auth:** Register / login (JWT); optional for demo (endpoints work without token).
- **Niche Gap:** POST `/api/v1/niche-gap` — stub; to be wired to Listen Notes + Ollama embeddings.
- **Niche Intersection:** POST `/api/v1/niche-intersection` — stub.
- **Trends:** GET `/api/v1/trends?period=3m` — stub; to be wired to Google Trends + Reddit.
- **Titles:** POST `/api/v1/titles` — stub; to be wired to Ollama for SEO titles.
- **Competitive Map:** GET `/api/v1/competitive-map?niche=...` — stub.

## Environment

- `DATABASE_URL` — PostgreSQL (use `postgresql+asyncpg://` for async or set `postgresql://` and the app will convert).
- `REDIS_URL`, `CELERY_BROKER_URL` — for cache and workers.
- `OLLAMA_HOST` — e.g. `http://localhost:11434` or `http://ollama:11434` (Docker).
- `LISTEN_NOTES_API_KEY` — for real gap/intersection data (optional for stubs).
- `JWT_SECRET` — min 32 chars for production.
