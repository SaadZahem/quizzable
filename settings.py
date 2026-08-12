import os

# Mirror the runtime default in quizzable.config so CLI tooling and the app agree.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "quizzable": {
            "models": ["quizzable.models"],
            "default_connection": "default",
            "migrations": "quizzable.migrations",
        }
    },
}
