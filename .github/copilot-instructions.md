# Copilot Instructions — TenderTruck

## Stack
Python 3.12 · FastAPI · SQLAlchemy 2 (SYNC, psycopg3) · Alembic · Pydantic v2 · PostgreSQL 17 (Docker :5433)
Frontend: React + TS + Vite · Tailwind · shadcn/ui · TanStack Query
FORBIDDEN: async SQLAlchemy, asyncpg, Redis, microservices, make, bash scripts.

## Structure — Modular Monolith
backend/src/app/         — config, db, lib (shared core)
backend/src/modules/     — по доменам: auth, tenders, bids, fleet, documents, chat, notifications, reviews, dictionaries
  каждый модуль: router.py, schemas.py, models.py, service.py, __init__.py

Layer rule: router -> service -> model. Роутеры БЕЗ логики и БЕЗ прямых запросов к БД.

## Already Exists — DO NOT recreate
- backend/Dockerfile, backend/pyproject.toml
- backend/alembic/{alembic.ini, env.py}
- backend/src/app/config/settings.py
- backend/src/app/db/engine.py
- backend/src/app/lib/logging.py
- backend/src/app/lib/security.py
- docker-compose.yml

## Must Create Now
1. backend/requirements.txt
2. backend/src/main.py — FastAPI app, CORS (http://localhost:5173), trace_id middleware, exception handlers, GET /health -> {"status":"ok","version":"0.1.0"}, mount /api/v1 router.
3. backend/src/app/core/__init__.py + backend/src/app/core/exceptions.py — AppError hierarchy (NotFound, Unauthorized, Forbidden, Validation), unified format {code, message, details}, handlers for AppError + RequestValidationError.
4. .env.example — DATABASE_URL, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, CORS_ORIGINS, LOG_LEVEL.
5. backend/src/api_v1.py — empty APIRouter(prefix="/api/v1"), placeholder to mount future modules.

## DB Rules
- ALL PKs = UUID (uuid4). ALL tables have created_at + updated_at (timezone-aware, server_default=now()).
- Money = INTEGER minor units (kopecks). NEVER float/Decimal.
- Migrations only via Alembic.
- Core models (create later in Step 2):
  - Tender: title, start_price int, current_price int, step int, deadline, status ENUM(DRAFT,ACTIVE,CLOSED), extension_count int, max_extensions int (default 10).
  - Bid: tender_id, carrier_id, price int, idempotency_key, is_winner.
  - Bid submission: SELECT...FOR UPDATE + X-Idempotency-Key + UNIQUE(tender_id, key) + anti-sniping (+2min, max 10).

## Errors
Format: {"code": "SNAKE_CASE", "message": "...", "details": {}}. Use app.add_exception_handler.

## Logging
JSON structured + trace_id (from X-Trace-Id header or uuid4). Middleware registered in main.py.

## Code Style
- Python 3.12, type hints everywhere (str | None), line length 100, ruff.
- Sync only for DB (FastAPI handles via threadpool).
- No async def on routes/services that touch DB.

## Security
- Deny by default. Public: /health, /auth/login, /auth/register.
- JWT HS256, Bearer. Roles: customer, carrier, admin. Dependency require_role(...).

## Commands
docker compose up -d --build
docker compose exec backend alembic upgrade head
docker compose exec backend pytest
docker compose exec backend ruff check .

## Git
NEVER git push. NEVER commit .env. Commits: feat:, fix:, chore:.