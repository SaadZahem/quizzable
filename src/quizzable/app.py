from pathlib import Path

from nicegui import app, ui

from . import auth
from . import pages as pages  # tells my linter to shut up
from .config import COLORS, STORAGE_SECRET
from .services.auth import get_current_user
from .utils import substitute
from .widgets import theme

parent = Path(__file__).parent


@ui.page("/test")
async def test():
    await ui.context.client.connected()
    token = app.storage.user.get("token")

    if token:
        user = await get_current_user(token.access_token)
    else:
        user = None

    with theme.frame(user), ui.card().tight().classes("size-64"):
        ui.element().classes("size-64 bg-myblack")
        with ui.card_section():
            ui.label("Lorem ipsum dolor sit amit")


def main(**kwargs):
    app.include_router(auth.router)
    context = COLORS.copy()
    for file in (parent / "templates").glob("*.html"):
        content = substitute(file, context)
        ui.add_head_html(content, shared=True)
    ui.run(title="Quizzable", language="en-US", storage_secret=STORAGE_SECRET, **kwargs)


if __name__ in {"__main__", "__mp_main__"}:
    main()
