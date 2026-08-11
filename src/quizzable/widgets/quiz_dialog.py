from contextlib import asynccontextmanager

from nicegui import ui

from ..models import MCQuiz, User
from ..utils import navigator

DATETIME_FORMAT = "%Y-%m-%d %I:%M %p UTC"


@asynccontextmanager
async def create(user: User | None, quiz: MCQuiz) -> ui.dialog:
    """
    Create a dialog holding the quiz details.
    """

    # Info about the quiz
    tags = quiz.tags.splitlines()
    count = len(await quiz.questions)
    maintainer = (await quiz.maintainer).username
    owner = user and user.username == maintainer
    creation_date = quiz.created.strftime(DATETIME_FORMAT)
    editing_date = quiz.last_edited.strftime(DATETIME_FORMAT)

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

            # let caller inject the menu button
            yield dialog, owner

        # Middle part of the dialog
        with ui.element().classes("px-4 py-2 w-full"):
            ui.markdown(
                "<br>".join(
                    (
                        f"Number of questions: {count}",
                        maintainer_label,
                        f"Created on: {creation_date}",
                        f"Last edited: {editing_date}",
                        "Tags:",
                    )
                )
            )
            # Fill the dialog width so the scrollbar only appears when the
            # tags actually overflow. min-w-0 lets the flex row shrink below
            # its content width instead of pushing the dialog wider.
            edge_fade = (
                "linear-gradient(to right,"
                " transparent 0, black 1rem,"
                " black calc(100% - 1rem), transparent 100%)"
            )
            with (
                ui.row(wrap=False)
                .classes("w-full min-w-0 gap-0 overflow-x-auto")
                # hide the scrollbar and fade the left/right edges so the
                # horizontal cut looks soft instead of sharp
                .style(
                    "scrollbar-width: none;"
                    "-ms-overflow-style: none;"
                    f"-webkit-mask-image: {edge_fade};"
                    f"mask-image: {edge_fade};"
                )
            ):
                for tag in tags:
                    ui.chip(tag).props("outline")

        # Lower part of the dialog
        ui.separator()
        (
            ui.button("Attempt")
            .on("click", navigator(f"/quiz/{quiz.id}"))
            .props("flat icon-right=arrow_forward")
            .classes("ms-auto")
        )
