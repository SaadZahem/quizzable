from pathlib import Path

from nicegui import app, ui

from . import auth
from .config import COLORS, STORAGE_SECRET
from .utils import substitute
from .views import home_page, index_page, login_page, quiz_page, result_page
from .widgets import custom_sub_pages, protected, theme

parent = Path(__file__).parent


@protected
def secure():
    raise ValueError("errrrr")


@ui.page("/")
@ui.page("/{_:path}")
def main_page():
    with theme.frame(None):
        custom_sub_pages(
            {
                "/": index_page,
                "/home": home_page,
                "/login": login_page,
                "/quiz/{file}": quiz_page,
                "/quiz/{file}/{selection}": result_page,
                "/secret": secure,
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
