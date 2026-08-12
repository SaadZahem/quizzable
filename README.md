# Quizzable

A web app for making, sharing, and taking multiple-choice quizzes.

Built with [NiceGUI](https://nicegui.io/) and [Tortoise ORM](https://tortoise.github.io/),
with JWT-based authentication and password hashing. It runs on SQLite for local
development and PostgreSQL in production.

## Features

- Create, edit, and take multiple-choice quizzes
- User accounts with JWT auth and hashed passwords
- Quiz tagging and copy-to-clipboard tags
- Upload quizzes from YAML files (set title and tags inside the file)
- Sample quizzes included under `static/yaml/`

## Tech stack

| Layer     | Choice                                             |
| --------- | -------------------------------------------------- |
| Runtime   | Python 3.13, managed with [`uv`](https://docs.astral.sh/uv/) |
| Web       | NiceGUI (FastAPI + uvicorn)                        |
| Database  | Tortoise ORM — SQLite (dev) / PostgreSQL (prod)    |
| Auth      | PyJWT + pwdlib (argon2)                            |

## Quick start (development)

Requires [`uv`](https://docs.astral.sh/uv/getting-started/installation/) and Python
3.13 (uv can install it for you).

```bash
bin/init_env.sh                    # generate the required .env secrets
uv sync                            # install deps (runtime + dev) into .venv
uv run python -m quizzable.app     # start with auto-reload
```

Then open <http://localhost:8080>.

> A `.env` file is **required** — the app refuses to start without it. See the
> environment section of the running guide.

## Running with Docker

```bash
docker compose up -d --build                            # SQLite stack
docker compose -f docker-compose.prod.yml up -d --build # PostgreSQL stack
```

## Testing

```bash
uv run pytest -q
```

## Documentation

Full instructions — environment variables, all run modes, Docker (SQLite and
PostgreSQL), the database model, helper scripts, project layout, and troubleshooting —
live in **[docs/RUNNING.md](docs/RUNNING.md)**.

## License

[MIT](LICENSE.md) © Saad El-Sayed Zahem
