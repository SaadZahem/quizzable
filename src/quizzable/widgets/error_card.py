from nicegui import ui

from ..utils import navigator


def error_card(code: int, messages: list[str]) -> ui.card:
    with ui.card().classes("container max-w-md absolute-center items-center") as card:
        ui.icon("error_outline", size="4rem").classes("text-negative")
        for not_first, message in enumerate(messages):
            if not not_first:
                ui.label(f"{code} - {message}").classes("text-2xl text-negative")
            else:
                ui.label(message).classes("text-gray-600")

        with ui.row().classes("mt-4"):
            ui.button("Go Home", icon="home", on_click=navigator("/")).props("outline")
            ui.button("Go Back", icon="arrow_back", on_click=ui.navigate.back).props(
                "outline"
            )

    ui.status_code(code)
    return card
