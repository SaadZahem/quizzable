from functools import partial

from nicegui import app, background_tasks, events, ui
from tortoise.expressions import Q

from ..models import MCQuiz, User
from ..utils import copy_relative_url, navigator
from ..widgets import quiz_dialog


async def home_page(q: str = ""):
    """View the home page."""

    # Accessing the current user
    user = app.storage.client.get("user")

    component = HomePageCard(user, page_size=20)

    await ui.context.client.connected()

    if q:
        component.search_input.bind_value(app.storage.tab, "q").set_value(q)
    else:
        component.search_input.bind_value(app.storage.tab, "search")


class HomePageCard(ui.card):
    def __init__(self, user: User | None, *, page_size: int = 20):
        super().__init__(align_items="center")

        self.user = user
        self.page_size = page_size
        self.search_input: ui.input
        self.results_list: ui.list

        with self.classes("grow self-stretch"):
            self._make()

    def _make(self) -> None:
        # Search input
        self.search_input = ui.input(
            "Search quizzes",
            on_change=self.handle_search_change,
        ).classes("self-stretch")

        # Add putton
        with self.search_input.add_slot("after"):
            (
                ui.button(icon="add", color="accent")
                .props("flat")
                .on("click", navigator("/quiz"))
                .tooltip("add a quiz")
            )

        # List - filtered with search bar
        self.results_list = ui.list().props("separator").classes("w-full")

        # Load quizzes initially
        ui.timer(0.1, self.load_quizzes, once=True)

    def handle_search_change(self, e: events.ValueChangeEventArguments):
        background_tasks.create_lazy(self.load_quizzes(e.value), name="load_quizzes")

    async def load_quizzes(self, query: str = "") -> None:
        query = (query or self.search_input.value).strip()

        orm_query = MCQuiz.all()
        if query:
            orm_query = orm_query.filter(
                Q(title__icontains=query) | Q(maintainer__username=query)
            )

        quizzes = await orm_query.order_by("-created").limit(self.page_size)

        with self.results_list.clear():
            if not quizzes:
                ui.label("No results found.").classes("text-gray-500 italic")
                return

            for index, quiz in enumerate(quizzes):
                with ui.item(on_click=partial(self.open_dialog, index, quiz)):
                    with ui.item_section().classes("grow-0 me-4"):
                        ui.icon("quiz").on("click")
                    with ui.item_section():
                        ui.label(quiz.title)

    async def open_dialog(self, index: int, quiz: MCQuiz):
        async def remove():
            await quiz.delete()
            list(self.results_list)[index].set_enabled(False)
            dialog.close()

        async with quiz_dialog.create(self.user, quiz, remove=remove) as (
            dialog,
            owner,
        ):
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
                    .on("click", remove)
                )
                ui.separator()
                ui.menu_item("Copy link", partial(copy_relative_url, url))
                ui.menu_item(
                    "Download yaml",
                    lambda: ui.download.from_url(f"/yaml/{quiz.file}"),
                )

        dialog.open()
