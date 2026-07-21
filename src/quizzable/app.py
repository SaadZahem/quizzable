from pathlib import Path

from fastapi import HTTPException
from nicegui import app, ui

from .config import COLORS, STORAGE_SECRET
from .services.auth import get_current_user
from .utils import substitute
from .views import home_page, index_page, login_page, quiz_page, result_page
from .widgets import custom_sub_pages, protected, theme

parent = Path(__file__).parent


@protected
def secure():
    raise ValueError("errrrr")


@ui.page("/")
@ui.page("/{_:path}")
async def main_page():
    auth = app.storage.user.get("auth", False)
    token = app.storage.user.get("token")
    user = None
    try:
        if auth:
            user = await get_current_user(token)
    except HTTPException:
        app.storage.user.update(auth=False)
        del app.storage.user["token"]

    with theme.frame():
        custom_sub_pages(
            {
                "/": index_page,
                "/home": home_page,
                "/login": login_page,
                "/quiz/{file}": quiz_page,
                "/quiz/{file}/{selection}": result_page,
                "/secret": secure,
            },
            data=dict(
                user=user,
            ),
        ).classes("container mx-auto h-full relative")


def main(**kwargs):
    context = COLORS.copy()
    for file in (parent / "templates").glob("*.html"):
        content = substitute(file, context)
        ui.add_head_html(content, shared=True)
    ui.run(title="Quizzable", language="en-US", storage_secret=STORAGE_SECRET, **kwargs)


if __name__ in {"__main__", "__mp_main__"}:
    main()
