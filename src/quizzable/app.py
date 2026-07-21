from pathlib import Path

from nicegui import app, ui

from . import auth
from . import pages as pages  # tells my linter to shut up
from .config import COLORS, STORAGE_SECRET
from .pages import (
    custom_sub_pages,
    home_page,
    index_page,
    login_page,
    quiz_page,
    result_page,
)
from .utils import substitute
from .widgets import theme

parent = Path(__file__).parent


@ui.page("/")
@ui.page("/{_:path}")
async def main_page():
    await ui.context.client.connected()
    with theme.frame(None):
        custom_sub_pages(
            {
                "/": index_page,
                "/home": home_page,
                "/login": login_page,
                "/quiz/{file}": quiz_page,
                "/quiz/{file}/{selection}": result_page,
            }
        ).classes("container mx-auto h-full relative")


def main(**kwargs):
    app.include_router(auth.router)
    context = COLORS.copy()
    for file in (parent / "templates").glob("*.html"):
        content = substitute(file, context)
        ui.add_head_html(content, shared=True)
    ui.run(title="Quizzable", language="en-US", storage_secret=STORAGE_SECRET, **kwargs)


if __name__ in {"__main__", "__mp_main__"}:
    main()
