from typing import Callable

from nicegui import ui

from ..models import MCQuiz, User
from ..utils import copy_relative_url, navigator


async def create(
    user: User | None,
    quiz: MCQuiz,
    *,
    remove: Callable[[MCQuiz], None],
) -> ui.dialog:
    """
    Create a dialog holding the quiz details.
    """

    # Info about the quiz
    count = len(await quiz.questions)
    maintainer = (await quiz.maintainer).username
    owner = user and user.username == maintainer
    datetime_format = "%Y-%m-%d %I:%M %p UTC"
    creation_date = quiz.created.strftime(datetime_format)
    editing_date = quiz.last_edited.strftime(datetime_format)

    maintainer_label = f"Maintainer: {maintainer}"
    if owner:
        maintainer_label += " (You)"

    # Dialog to appear when the button "Open" is clicked
    with (
        ui.dialog() as dialog,
        ui.card().tight().classes("container max-w-lg text-primary"),
    ):
        # Upper part of the dialog
        with ui.row(wrap=False).classes(
            "w-full justify-between items-center bg-primary"
        ):
            ui.label(quiz.title).classes("text-xl mx-4 text-mywhite")

            # Menu button
            with (
                ui.button(icon="more_vert", color="mywhite")
                .classes("px-1")
                .props("flat round"),
                ui.menu().classes("text-primary"),
            ):
                (
                    ui.menu_item("Edit")
                    .set_enabled(owner)
                    .on("click", navigator(url := f"/quiz/{quiz.id}/edit"))
                )
                (
                    ui.menu_item("Delete")
                    .set_enabled(owner)
                    .classes("text-negative")
                    .on("click", lambda: remove(quiz))
                )
                ui.separator()
                ui.menu_item("Copy link", lambda: copy_relative_url(url))
                ui.menu_item(
                    "Download yaml",
                    lambda: ui.download.from_url(f"/yaml/{quiz.file}"),
                )

        # Middle part of the dialog
        with ui.element().classes("px-4 py-2"):
            ui.markdown(
                "<br>".join(
                    (
                        f"Number of questions: {count}",
                        maintainer_label,
                        f"Created on {creation_date}",
                        f"Last edited: {editing_date}",
                    )
                )
            )

        # Lower part of the dialog
        ui.separator()
        (
            ui.button("Attempt")
            .on("click", navigator(f"/quiz/{quiz.id}"))
            .props("flat icon-right=arrow_forward")
            .classes("ms-auto")
        )
        return dialog
