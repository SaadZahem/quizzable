TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3",
    },
    "apps": {
        "quizzable": {
            "models": ["quizzable.models"],
            "default_connection": "default",
            "migrations": "quizzable.migrations",
        }
    },
}
