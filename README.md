# crypto_wallet_checker

[![Coverage Status](https://coveralls.io/repos/github/saladuit/Crypto_Wallets/badge.svg?branch=main)](https://coveralls.io/github/saladuit/Crypto_Wallets?branch=main) [![CI](https://github.com/saladuit/Crypto_Wallets/actions/workflows/ci.yml/badge.svg)](https://github.com/saladuit/Crypto_Wallets/actions/workflows/ci.yml)

A compact FastAPI backend for checking on-chain wallet balances against expected values stored locally.

**Project Structure**
- `backend/` — FastAPI app, DB layer, CRUD, models, routes, and tests.
- `frontend/` — React app.

Inside `backend/`:
- `crud/` — high-level DB operations used by routes/services.
- `db/` — SQLAlchemy DB definitions and helpers.
- `models/` — Pydantic/ORM models
- `routes/` — FastAPI route handlers.
- `services/` — business logic and external API wrapper(s).
- `app.py` — FastAPI application and route registration.

**Setup**
1. Create and activate a Python venv and install backend deps:

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
```

2. (Optional) Seed a local SQLite DB:

```bash
python backend/seed_db.py
```

3. Start the backend:

```bash
uvicorn backend.app:app --reload --port 8000
```

4. Start the frontend:

```bash
cd frontend
npm install
npm run dev
```

**Usage**
- Visit `http://localhost:8000/wallets` to get to show stored wallets.
- Visit `http://localhost:8000/docs` for interactive API docs.

**Tests**
- Run tests from the project root:

```bash
pytest -q --cov --cov-branch
```

***Test setup notes***
  - `backend/tests/conftest.py` configures an in-memory SQLite database for tests using:
  - `SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"` with `connect_args={"check_same_thread": False}` and `poolclass=StaticPool` so the same in-memory DB is accessible across threads/connections.
  - The fixture creates the schema once for the test session (`Base.metadata.create_all(bind=engine)`), yields, then drops it at teardown.
  - The `client` fixture overrides the app's `get_db` dependency so route handlers in tests use the test session.

This makes tests fast, isolated, and deterministic; external calls are mocked by tests (see `backend/services` mocks in test files).
