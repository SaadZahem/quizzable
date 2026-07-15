TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3",
    },
    "apps": {
        "models": {
            "models": ["src.quizzable.models"],
            "default_connection": "default",
        }
    }
}
