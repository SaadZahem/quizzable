import sys

from nicegui import app, ui

from . import widgets as my
from .argument_parser import CustomArgumentParser
from .config import STORAGE_SECRET
from .utils import current_user
from .views import (
    edit_quiz_page,
    home_page,
    index_page,
    load_quiz_page,
    login_page,
    new_quiz_page,
    review_quiz_page,
    upload_quiz_page,
)


@ui.page("/")
@ui.page("/{_:path}")
async def main_page():
    # Setting default values that elements in the header can bind to
    auth = app.storage.user.setdefault("auth", False)
    app.storage.user.setdefault("username", "")

    # Obtaining and storing the user object to achieve the following:
    # - allow protected pages to access the current user even
    # - the access is not interrupted by a page reload if the token not expired
    # - allow other pages to update this value
    # - only verify the access token on page reloads or navigation even if it was expired
    if auth:
        app.storage.client["user"] = await current_user()

    with my.scaffold():
        my.custom_sub_pages(
            {
                "/": index_page,
                "/home": home_page,
                "/login": login_page,
                "/quiz": new_quiz_page,
                "/quiz/upload": upload_quiz_page,
                "/quiz/{quiz_id}": load_quiz_page,
                "/quiz/{quiz_id}/edit": edit_quiz_page,
                "/quiz/{quiz_id}/review/{selection}": review_quiz_page,
            },
        ).classes("container mx-auto h-full relative")


def main(**kwargs):
    # Parsing arguments
    args = CustomArgumentParser().parse_args(sys.argv[1:])

    # Starting/Reloading the server
    ui.run(
        port=args.port,
        title="Quizzable",
        language="en-US",
        storage_secret=STORAGE_SECRET,
        **kwargs,
    )


if __name__ in {"__main__", "__mp_main__"}:
    main(uvicorn_reload_includes="*.py, *.html")
