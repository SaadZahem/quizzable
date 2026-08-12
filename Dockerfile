# Self-contained image built from the uv lockfile.
# The base already ships Python 3.13 and the `uv` binary.
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Container-friendly uv settings:
# - compile .pyc at build time for faster startup
# - copy (don't symlink) packages so nothing points outside the image
# - never try to fetch a managed Python; the base already has one
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# Install dependencies in their own cached layer, so editing app code doesn't
# re-run the (slow) dependency resolve/install. We intentionally do NOT install
# the project itself as a package (there's no build backend declared); instead
# PYTHONPATH below makes the `quizzable` package importable straight from src.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Application code. main.py is the entrypoint; static/ is served at runtime.
COPY main.py ./
COPY src ./src
COPY static ./static

# Make `import quizzable` resolve without installing the project.
ENV PYTHONPATH=/app/src

# The container runs as UID 1000 (see docker-compose.yml). Hand ownership of the
# working dir to that user so SQLite can create its journal/WAL sidecar files in
# /app at runtime, otherwise it fails with "attempt to write a readonly database".
RUN chown -R 1000:1000 /app

EXPOSE 8080

# main.py runs main(reload=False) -> ui.run(port=8080), which binds 0.0.0.0.
CMD [".venv/bin/python", "main.py"]
