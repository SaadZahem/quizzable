from contextlib import contextmanager

from nicegui import html, ui

from ..models import User
from ..utils import navigator


@contextmanager
def frame(user: User = None):
    ui.query("#app").classes("h-screen bg-brand")
    ui.query(".nicegui-content").classes("p-0 gap-0")

    with (
        ui.header().classes("bg-brand border-b-1 border-dashed border-black"),
        ui.row().classes("container mx-auto items-center text-primary"),
    ):
        with html.a().props("href=/").classes("hover:underline text-primary"):
            ui.label("Quizzable").classes("text-bold text-2xl")

        ui.space()
        if user is None:
            (
                ui.button(
                    "Log in",
                    on_click=navigator("/login", redirect=True),
                )
                .props("flat no-caps")
                .classes("hover:scale-110")
            )
        else:
            ui.label(str(user)).classes("text-xl")
            ui.button(icon="logout").props("flat rounded")

    with (
        ui.element().classes("size-full py-8 text-primary"),
        ui.row().classes("container mx-auto h-max"),
    ):
        yield
