from nicegui import html, ui

from ..utils import navigator


def header_element():
    with (
        html.header().classes("w-full py-4 shadow-inner-lg") as header,
        ui.row().classes("container mx-auto items-center"),
    ):
        with html.a().props('href="/"') as anchor, ui.element("h5"):
            anchor.classes("hover:underline")
            html.strong("Quizzable")

        ui.space()
        ui.button("Log in", on_click=navigator("/login")).props("flat no-caps")

    return header.classes("border-b-1 border-dashed border-slate")
