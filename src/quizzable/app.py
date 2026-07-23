from pathlib import Path

from nicegui import app, ui

from .config import COLORS, STORAGE_SECRET
from .utils import current_user, substitute
from .views import (
    home_page,
    index_page,
    load_quiz_page,
    login_page,
    new_quiz_page,
    review_quiz_page,
)
from .widgets import custom_sub_pages, scaffold

parent = Path(__file__).parent


@ui.page("/")
@ui.page("/{_:path}")
async def main_page():
    # ui.run_javascript(
    # "var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;"
    # "var height = (window.innerHeight > 0) ? window.innerHeight : screen.height;"
    # )

    # setting default values that elements in the header can bind to
    app.storage.user.setdefault("auth", False)
    app.storage.client.setdefault("username", "")

    user = await current_user()

    with scaffold():
        custom_sub_pages(
            {
                "/": index_page,
                "/home": home_page,
                "/login": login_page,
                "/quiz": new_quiz_page,
                "/quiz/{file}": load_quiz_page,
                "/quiz/{file}/{selection}": review_quiz_page,
            },
            data=dict(user=user),
        ).classes("container mx-auto h-full relative")


def main(**kwargs):
    context = COLORS.copy()
    for file in (parent / "templates").glob("*.html"):
        content = substitute(file, context)
        ui.add_head_html(content, shared=True)
    ui.run(title="Quizzable", language="en-US", storage_secret=STORAGE_SECRET, **kwargs)


if __name__ in {"__main__", "__mp_main__"}:
    main()
