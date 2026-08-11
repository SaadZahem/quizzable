from functools import partial
from typing import Callable

from nicegui import ui

from ..models import MCQuiz
from ..utils import copy_relative_url, navigator


def create(quiz: MCQuiz, *, enabled: bool, remove: Callable):
    with (
        ui.button(icon="more_vert", color="mywhite")
        .classes("px-1")
        .props("flat round"),
        ui.menu().classes("text-primary"),
    ):
        (
            ui.menu_item("Edit")
            .set_enabled(enabled)
            .on("click", navigator(url := f"/quiz/{quiz.id}/edit"))
        )
        (
            ui.menu_item("Delete")
            .set_enabled(enabled)
            .classes("text-negative")
            .on("click", remove)
        )
        ui.separator()
        ui.menu_item("Copy link", partial(copy_relative_url, url))
        ui.menu_item(
            "Download yaml",
            lambda: ui.download.from_url(f"/yaml/{quiz.file}"),
        )
