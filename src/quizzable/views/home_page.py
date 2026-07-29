from nicegui import app, ui

from ..models import MCQuiz
from ..utils import copy_relative_url, navigator


async def home_page():
    """View the home page."""

    # Accessing all quizzes
    all_quizzes = await MCQuiz.all()

    # Accessing the current user
    user = app.storage.client.get("user")

    async def remove(quiz: MCQuiz):
        """Remove a quiz from the list and from the database."""
        all_quizzes.remove(quiz)
        await quiz.delete()
        quiz_list.refresh()

    @ui.refreshable
    async def quiz_list():
        with ui.list().props("separator").classes("w-full"):
            for quiz in reversed(all_quizzes):
                for term in search.value:
                    if term.lower() not in quiz.title.lower():
                        break
                else:
                    with ui.expansion(quiz.title, group="quiz").classes(
                        "w-full"
                    ) as expansion:
                        with expansion.add_slot("header"):
                            with ui.item_section().classes("grow-0 me-4"):
                                ui.icon("quiz").on("click")
                            with ui.item_section():
                                ui.label(quiz.title)
                        with expansion.add_slot("default"):
                            await quiz_details(quiz)

    async def quiz_details(quiz: MCQuiz):
        """Show more details about the selected quiz."""

        # Info about the quiz
        count = len(await quiz.questions)
        maintainer = (await quiz.maintainer).username
        owner = user and user.username == maintainer

        maintainer_label = f"Maintainer: {maintainer}"
        if owner:
            maintainer_label += " (You)"

        # Dialog to appear when the button "Open" is clicked
        with (
            ui.dialog() as dialog,
            ui.card().classes("container max-w-lg text-primary"),
        ):
            # Upper part of the dialog
            with ui.row(wrap=False).classes("w-full justify-between items-center"):
                ui.label(quiz.title).classes("text-2xl mx-auto text-center")

                # Menu button
                with (
                    ui.button(icon="more_vert").classes("px-1").props("flat round"),
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

            # Lower part of the dialog
            (
                ui.button("Attempt")
                .on("click", navigator(f"/quiz/{quiz.id}"))
                .props("outline icon-right=arrow_right")
                .classes("mx-auto")
            )

        # Details to be shown when the item is expanded
        ui.label(f"Number of questions: {count}")
        ui.label(maintainer_label)
        ui.button("Open", on_click=dialog.open).props("flat").classes("self-end")

    # Enables app.storage.tab
    await ui.context.client.connected()

    # Main card element with search bar, a button, and a refreshable list
    with ui.card().classes("grow self-stretch items-center"):
        with (
            ui.input_chips("Search quizzes", on_change=quiz_list.refresh)
            .classes("self-stretch")
            .bind_value(app.storage.tab, "search") as search,
            search.add_slot("after"),
        ):
            (
                ui.button(icon="add", color="accent")
                .props("flat")
                .on("click", navigator("/quiz"))
                .tooltip("add a quiz")
            )

        await quiz_list()
