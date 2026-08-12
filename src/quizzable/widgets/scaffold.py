import operator as op
from contextlib import contextmanager

from nicegui import app, html, ui

from ..utils import logout, navigator


@contextmanager
def scaffold():
    ui.query("body").classes("bg-brand")
    ui.query("#app").classes("h-screen")
    ui.query("main").classes("flex flex-row items-stretch")
    ui.query(".nicegui-content").classes("p-0 gap-0 grow min-w-0")

    with ui.header().classes("bg-brand border-b-1 border-dashed border-myblack"):
        with ui.row().classes("container mx-auto items-center text-primary"):
            with html.a().props("href=/").classes("hover:underline text-primary"):
                ui.label("Quizzable").classes("text-bold text-2xl")

            ui.space()
            (
                ui.button("Log in", on_click=navigator("/login", redirect=True))
                .props("no-caps outline")
                .classes("hover:scale-110")
                .bind_visibility_from(app.storage.user, "auth", op.not_)
            )
            (
                ui.label()
                .classes("text-xl")
                .bind_text_from(app.storage.user, "username")
                .bind_visibility_from(app.storage.user, "auth")
            )
            (
                ui.button(icon="logout", on_click=logout)
                .props("flat rounded")
                .bind_visibility_from(app.storage.user, "auth")
            )

    with ui.element().classes("size-full py-8 text-primary"):
        yield
