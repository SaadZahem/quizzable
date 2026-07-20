from nicegui import app, ui

from . import auth
from . import pages as pages  # tells my linter to shut up
from .config import STORAGE_SECRET


def main(**kwargs):
    app.include_router(auth.router)
    ui.run(title="Quizzable", language="en-US", storage_secret=STORAGE_SECRET, **kwargs)


if __name__ in {"__main__", "__mp_main__"}:
    main()
