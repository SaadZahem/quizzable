from nicegui import app, ui
from nicegui.page_arguments import RouteMatch

from ..utils import is_authenticated, is_protected
from .error_card import error_card


class CustomSubPages(ui.sub_pages):
    """Custom ui.sub_pages with built-in authentication and custom 404 handling."""

    def _render_page(self, match: RouteMatch) -> bool:
        protected = is_protected(match.builder)
        app.storage.client.update(
            path=self._router.current_path,
            protected=protected,
        )
        if protected and not is_authenticated():
            ui.navigate.to(f"/login?redirect_url={match.full_url}")
            return True

        return super()._render_page(match)

    def _render_404(self) -> None:
        error_card(
            [
                "404 - Page Not Found",
                f'The page "{self._router.current_path}" does not exist.',
            ]
        )

    def _render_error(self, error: Exception) -> None:
        error_card(
            [
                "500 - Internal Server Error",
                f'The page "{self._router.current_path}" produced an error.',
                # we do not recommend to show exception messages in production (security risk)
                str(error),
            ]
        )


# Function-like access following NiceGUI convention where classes are callable to feel like functions
custom_sub_pages = CustomSubPages
