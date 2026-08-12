# Running Quizzable

A complete guide to running Quizzable — a NiceGUI web app for making, sharing, and
taking quizzes, backed by Tortoise ORM (SQLite in development, PostgreSQL in
production) with JWT auth and password hashing.

This document covers local development, testing, the required environment, and both
Docker setups (SQLite and PostgreSQL).

---

## 1. Overview

| Concern            | Choice                                                        |
| ------------------ | ------------------------------------------------------------- |
| Language / runtime | Python **3.13** (see `.python-version`)                        |
| Package / venv     | [`uv`](https://docs.astral.sh/uv/) (source of truth: `uv.lock`) |
| Web framework      | NiceGUI 3.x (FastAPI + uvicorn under the hood)                |
| ORM                | Tortoise ORM                                                  |
| Database           | SQLite by default; PostgreSQL (asyncpg) in production         |
| Auth               | JWT tokens (PyJWT) + password hashing (pwdlib/argon2)         |
| Default port       | **8080**                                                      |

The app binds `0.0.0.0:8080`. The database connection is chosen at runtime from the
`DATABASE_URL` environment variable, defaulting to local SQLite when unset.

---

## 2. Prerequisites

- **Python 3.13** — `uv` can install it for you if missing.
- **uv** — install via <https://docs.astral.sh/uv/getting-started/installation/>.
- **Docker + Docker Compose** — only needed for the containerized workflows in §7.
- **OpenSSL** — used by `bin/init_env.sh` to generate secrets (present on most systems).

---

## 3. Environment variables (`.env`)

The app **requires a `.env` file** in the working directory — `config.py` raises on
startup if it is missing. `.env` is gitignored; never commit real secrets.

| Variable            | Required            | Purpose                                                                 |
| ------------------- | ------------------- | ----------------------------------------------------------------------- |
| `SECRET_KEY`        | yes                 | Signs/secures JWT auth tokens.                                          |
| `STORAGE_SECRET`    | yes                 | Encrypts NiceGUI's `app.storage.user` data.                            |
| `DATABASE_URL`      | no (defaults SQLite)| Tortoise connection string. Set to a Postgres URL for production.       |
| `POSTGRES_USER`     | prod (compose) only | Postgres role for the `db` service in `docker-compose.prod.yml`.       |
| `POSTGRES_PASSWORD` | prod (compose) only | Postgres password.                                                     |
| `POSTGRES_DB`       | prod (compose) only | Postgres database name.                                                 |

Notes:
- When `DATABASE_URL` is **unset**, the app uses `sqlite://db.sqlite3` (a file in the
  working directory).
- In `docker-compose.prod.yml`, `DATABASE_URL` is built automatically from the
  `POSTGRES_*` values and points at the `db` service — you do **not** set it by hand
  there.
- `docker compose` auto-loads `.env` from the project root for `${...}` substitution.

### Generate a `.env`

The helper script creates `SECRET_KEY` and `STORAGE_SECRET`:

```bash
bin/init_env.sh
```

For Postgres, also add (see `.env.example` for the full template):

```dotenv
POSTGRES_USER="quizzable"
POSTGRES_PASSWORD="<openssl rand -hex 24>"
POSTGRES_DB="quizzable"
```

Copy `.env.example` → `.env` and fill in values if you prefer doing it manually.

---

## 4. Local development (SQLite, no Docker)

The project is an installable package (hatchling build backend, `src/` layout) with a
separate dev dependency group for tests.

```bash
# 1. Create the .env file (once)
bin/init_env.sh

# 2. Install everything (runtime + dev deps) into .venv, from the lockfile
uv sync

# 3. Run the app (development, auto-reload on file changes)
uv run python -m quizzable.app
```

Open <http://localhost:8080>.

`uv sync` reads `uv.lock` and installs the `quizzable` package (editable) plus the
`dev` dependency group. You do **not** need `requirements.txt` or manual
`uv pip install -e .` — those instructions in the old README are superseded by
`uv sync`. (`requirements.txt` is kept only as a plain-pip fallback; `uv.lock` is
authoritative.)

### Entry points and reload behavior

| Command                          | Reload | Use            |
| -------------------------------- | ------ | -------------- |
| `uv run python -m quizzable.app` | on     | development    |
| `uv run python -m quizzable`     | off    | production-ish |
| `uv run python main.py`          | off    | production-ish |

`main.py` and `python -m quizzable` call `main(reload=False)`. Running `app.py` as a
module enables uvicorn reload for `*.py`/`*.html`.

### Command-line options

```bash
uv run python -m quizzable.app --port 9000   # -p / --port, default 8080
```

Unknown arguments are ignored (via `parse_known_args`) so external runners like
pytest don't clash with the app's parser.

---

## 5. Testing

Tests use an in-memory SQLite database and the NiceGUI test plugin. Config lives in
`pyproject.toml` under `[tool.pytest.ini_options]`.

```bash
uv run pytest -q
```

Key points:
- `main_file = main.py` tells the NiceGUI `user` fixture how to bootstrap the app
  (it runs `main.py` via `runpy`).
- `addopts = -p nicegui.testing.plugin` activates the plugin (NiceGUI does **not**
  auto-register it).
- `asyncio_mode = auto` lets async tests run without explicit markers.

---

## 6. Database

The app uses `generate_schemas=True`, so **missing tables are created automatically
on startup** — no manual migration step is required for a fresh database. Three tables
are created: `users`, `quizzes`, `questions`.

- **Development:** `sqlite://db.sqlite3` (default). The file is created on first run.
- **Production:** set `DATABASE_URL` to a Postgres URL, e.g.
  `postgres://user:password@host:5432/dbname` (the `postgres://` scheme uses asyncpg).

`settings.py` mirrors the same `DATABASE_URL` default for any Tortoise CLI tooling.

There is no versioned migration workflow wired up; schema changes rely on
`generate_schemas`. For evolving a production schema over time, consider adding
`aerich` (out of scope here).

---

## 7. Running with Docker

Two Compose files are provided:

| File                       | Database         | Intended use            |
| -------------------------- | ---------------- | ----------------------- |
| `docker-compose.yml`       | SQLite (file)    | Local self-contained    |
| `docker-compose.prod.yml`  | PostgreSQL       | Production              |

Both build the image from the `Dockerfile`, which:
- installs dependencies from `uv.lock` (**runtime only**, `--no-dev`),
- puts the source on `PYTHONPATH=/app/src` (no package build inside the image),
- runs as UID 1000 friendly (chowns `/app` so SQLite can write its journal),
- starts `main.py` (no reload) on port 8080.

A `.env` file must exist before starting either stack — it is mounted read-only into
the container so secrets stay out of the image.

### 7a. SQLite stack (development)

```bash
docker compose up -d --build      # build + start
docker compose logs -f            # follow logs
docker compose down               # stop
```

- Runs as `user: "1000:1000"` so files written to bind mounts stay owned by you.
- Bind mounts: `.env` (ro), `db.sqlite3` (persisted), `.nicegui/` (session storage).

### 7b. PostgreSQL stack (production)

```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml logs -f
docker compose -f docker-compose.prod.yml down        # stop (keeps data)
docker compose -f docker-compose.prod.yml down -v     # stop + WIPE the DB volume
```

What it does:
- Starts a `postgres:17-alpine` service (`db`) with a persistent named volume
  `pgdata` and a `pg_isready` healthcheck.
- The app `depends_on` the db being **healthy** before starting.
- `DATABASE_URL` is assembled from the `POSTGRES_*` vars and points at `db:5432`.
- NiceGUI session storage persists in the named volume `nicegui_storage`.

Requires `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` in `.env` (see §3).

Open <http://localhost:8080> once both containers are up.

### Inspecting the Postgres database

```bash
docker compose -f docker-compose.prod.yml exec db \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\dt"
```

---

## 8. Supplementary scripts (`bin/`)

- **`bin/init_env.sh`** — creates `.env` with random `SECRET_KEY` and
  `STORAGE_SECRET`. Run once before first launch.
- **`bin/init_db.py`** — seeds quizzes into the database from a directory of YAML
  files. Caveats:
  - It expects a `data/` directory of `*.yml` files (the repo ships sample quizzes in
    `static/yaml/` instead — point it at the right path or create `data/`).
  - It requires at least one existing `User` (it assigns quizzes to `User.first()`),
    so sign up in the app first.
  - The project must be installed as a package (`uv sync` handles this).

Users can also upload quizzes through the app's upload page; see the on-page
instructions for the YAML format.

---

## 9. Project structure

```
.
├── main.py                 # production entry point (main(reload=False))
├── settings.py             # Tortoise CLI config (mirrors DATABASE_URL)
├── pyproject.toml          # deps, dev group, build backend, pytest config
├── uv.lock                 # authoritative dependency lock
├── Dockerfile              # runtime image (uv sync --no-dev, PYTHONPATH=src)
├── docker-compose.yml      # SQLite stack
├── docker-compose.prod.yml # PostgreSQL stack
├── .env.example            # env template (copy to .env)
├── docs/                    # documentation (this manual lives here)
├── bin/                    # init_env.sh, init_db.py
├── static/yaml/            # sample quizzes
└── src/quizzable/          # application package
    ├── app.py              # register_tortoise + ui.run(root)
    ├── config.py           # env + theme config (DATABASE_URL lives here)
    ├── models/             # User, MCQuiz, MCQuestion
    ├── services/           # qy (YAML), auth
    ├── views/, widgets/    # pages and UI components
    └── templates/          # header.html
```

---

## 10. Troubleshooting

- **`.env file is missing`** on startup — run `bin/init_env.sh` (or create `.env`),
  and ensure it is present in the working directory / mounted into the container.
- **`attempt to write a readonly database`** (SQLite in Docker) — the container user
  must own `/app` to create SQLite journal files; the `Dockerfile` chowns it. If you
  customize the image, preserve that.
- **Postgres tables never appear after a Compose `--build` that failed partway** — a
  failed `--build` (e.g. a transient registry timeout while pulling Postgres) can leave
  a **stale app image**, and a later plain `docker compose up -d` will silently run old
  code. Always re-run with `--build` after a failed build so the image reflects your
  code.
- **Port 8080 already in use** — stop the other stack first (the SQLite and Postgres
  compose files both use port 8080 and the container name `quizzable`), or change the
  published port in the compose file.
- **App uses SQLite when you expected Postgres** — confirm `DATABASE_URL` is set inside
  the container (`docker compose ... exec quizzable printenv DATABASE_URL`). When unset,
  the app falls back to SQLite by design.
```
