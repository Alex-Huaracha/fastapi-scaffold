# FastAPI Scaffold

[![CI](https://github.com/Alex-Huaracha/fastapi-scaffold/actions/workflows/ci.yml/badge.svg)](https://github.com/Alex-Huaracha/fastapi-scaffold/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Alex-Huaracha/fastapi-scaffold/branch/main/graph/badge.svg)](https://codecov.io/gh/Alex-Huaracha/fastapi-scaffold)

A production-shaped starting point for a FastAPI service: async SQLAlchemy 2.0 over
PostgreSQL, Alembic migrations, a paginated CRUD module, domain exceptions mapped to
HTTP responses, and an integration test suite that runs against a real database.

## Stack

- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL 18
- Pydantic v2
- Alembic
- uv

## Requirements

Docker. Nothing else.

## Run the tests

```bash
./up_test.sh
```

Builds the image, starts a throwaway PostgreSQL, runs the suite inside a container and
removes everything afterwards. The script exits with pytest's exit code.

## Run the API

```bash
./up_dev.sh
```

Applies migrations and starts the server.

- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Logs: `docker compose logs -f api`
- Stop: `docker compose down`


## Design decisions

- **No repository layer.** SQLAlchemy already is the abstraction.
- **Services raise domain errors, never `HTTPException`.** One handler in `main.py` maps them.
- **`IntegrityError` is caught even after the pre-check.** The check has a race window; the constraint does not.
- **Pagination orders by `(name, id)`.** Without a tiebreaker, pages repeat or skip rows.
- **Tests run against a real PostgreSQL**, isolated by a transaction rollback per test.
- **`create_all` in tests, Alembic at runtime.** `alembic check` catches the drift.
- **Naming convention on `MetaData`.** Alembic cannot drop an unnamed constraint.

## Local development

To iterate without rebuilding the image, start only the test database once:

```bash
docker compose -f compose.test.yml up -d db-test --wait
uv run pytest -v
```

The suite runs in about 0.2s. `conftest.py` falls back to that database when
`DATABASE_URL` is not set, and respects it when Docker or CI injects one.

| Purpose | Command |
|---|---|
| Run the suite | `uv run pytest -v` |
| Lint | `uv run ruff check .` |
| Create a migration | `uv run alembic revision --autogenerate -m "..."` |
| Fail if models drifted from migrations | `uv run alembic check` |
