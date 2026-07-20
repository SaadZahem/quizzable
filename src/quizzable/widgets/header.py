from nicegui import app, html, ui

from ..utils import navigator


@ui.refreshable
def header_element():
    def logout():
        del app.storage.user["token"]
        header_element.refresh()

    with (
        html.header().classes("w-full py-4 shadow-inner-lg") as header,
        ui.row().classes("container mx-auto items-center"),
    ):
        with html.a().props('href="/"') as anchor, ui.element("h5"):
            anchor.classes("hover:underline")
            html.strong("Quizzable")

        ui.space()
        if "token" in app.storage.user:
            ui.button("log out", icon="logout", on_click=logout)
        else:
            ui.button("Log in", on_click=navigator("/login")).props("flat no-caps")

    return header.classes("border-b-1 border-dashed border-slate")
