# TenderTruck Agent Guidelines

## Stack
- Python 3.12, FastAPI, SQLAlchemy 2 sync, psycopg3, Alembic, Pydantic v2.
- PostgreSQL 17; React, TypeScript, Vite, Tailwind, shadcn/ui, TanStack Query.

## Structure
- Backend code lives under `backend/src`.
- Shared application code belongs in `app`; domain code belongs in `modules`.
- Follow `router -> service -> model`; routers must not execute database queries.

## Commands
- `docker compose up -d --build`
- `docker compose exec backend alembic upgrade head`
- `docker compose exec backend pytest`
- `docker compose exec backend ruff check .`

## Rules
- UUID primary keys; timezone-aware timestamps; integer minor-unit money.
- Use migrations for schema changes; never use async SQLAlchemy, asyncpg, Redis, or microservices.
- Public health, login, and register routes only; protect the rest by JWT and roles.
- Never commit `.env`, push with Git, or use shell scripts where a native tool exists.

## Design Reference
- Keep the interface restrained and operational: [docs/design.md](docs/design.md).
