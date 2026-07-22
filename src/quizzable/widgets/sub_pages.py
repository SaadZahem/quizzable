from nicegui import app, ui
from nicegui.page_arguments import RouteMatch

from ..utils import is_protected


class CustomSubPages(ui.sub_pages):
    """Custom ui.sub_pages with built-in authentication and custom 404 handling."""

    def _render_page(self, match: RouteMatch) -> bool:
        protected = is_protected(match.builder)
        app.storage.client.update(
            path=self._router.current_path,
            protected=protected,
        )
        if protected and not self._is_authenticated():
            ui.navigate.to(f"/login?redirect_url={match.full_url}")
            return True
        return super()._render_page(match)

    def _render_404(self) -> None:
        with ui.card().classes("absolute-center items-center"):
            ui.icon("error_outline", size="4rem").classes("text-negative")
            ui.label("404 - Page Not Found").classes("text-2xl text-negative")
            ui.label(f'The page "{self._router.current_path}" does not exist.').classes(
                "text-gray-600"
            )
            with ui.row().classes("mt-4"):
                ui.button(
                    "Go Home", icon="home", on_click=lambda: ui.navigate.to("/")
                ).props("outline")
                ui.button(
                    "Go Back", icon="arrow_back", on_click=ui.navigate.back
                ).props("outline")

    def _render_error(self, error: Exception) -> None:
        with ui.card().classes("absolute-center items-center"):
            ui.icon("error_outline", size="4rem").classes("text-red")
            ui.label("500 - Internal Server Error").classes("text-2xl text-red")
            ui.label(
                f'The page "{self._router.current_path}" produced an error.'
            ).classes("text-gray-600")
            # we do not recommend to show exception messages in production (security risk)
            ui.label(str(error)).classes("text-gray-600")
            with ui.row().classes("mt-4"):
                ui.button(
                    "Go Home", icon="home", on_click=lambda: ui.navigate.to("/")
                ).props("outline")
                ui.button(
                    "Go Back", icon="arrow_back", on_click=ui.navigate.back
                ).props("outline")

    def _is_authenticated(self) -> bool:
        return app.storage.user.get("auth", False)


# Function-like access following NiceGUI convention where classes are callable to feel like functions
custom_sub_pages = CustomSubPages
