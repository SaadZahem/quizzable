from __future__ import annotations

from nicegui import ElementFilter, ui
from nicegui.elements.choice_element import ChoiceElement

from ..models import MCQuestion


class EditableQuestionCard(ChoiceElement):
    def __init__(self, question: MCQuestion | None = None):
        options = {prefix: "" for prefix in "abcde"}
        value = question.correct.value if question and question.correct else None
        super().__init__(options=options, value=value or None)

        self.question = question
        self._choices = {}
        self._build(question or MCQuestion())

    def _build(self, question: MCQuestion):
        with self, ui.card():
            with (
                ui.input()
                .props("outlined dense autogrow")
                .bind_value(question, "text")
                .classes("self-stretch") as self._text_input,
                self._text_input.add_slot("after"),
                ui.element(),
            ):
                (
                    ui.button(
                        icon="delete", color="accent", on_click=self.delete
                    ).props("flat"),
                )
                # ui.icon("drag_indicator").props("flat").classes(
                #     "handle cursor-grab active:cursor-grabbing"
                # )

            for prefix in "abcde":
                self._choices[prefix] = _inp = ui.input(prefix=f"{prefix})").bind_value(
                    question, prefix
                )
                with (
                    _inp.props("outlined dense autogrow").add_slot("before"),
                    ui.button().props("flat round") as button,
                    ui.icon(
                        "radio_button_checked"
                        if self.value == prefix
                        else "radio_button_unchecked"
                    ).mark("radio") as icon,
                ):
                    button.on(
                        "click",
                        lambda ico=icon, value=prefix: self._handle_change(ico, value),
                    )

    def _handle_change(self, ico: ui.icon, value: str):
        ElementFilter(kind=ui.icon, marker="radio").within(instance=self).props(
            "name=radio_button_unchecked"
        )
        ico.props("name=radio_button_checked")
        self.value = value

    def validate_values(self) -> dict:
        questiondict = dict(
            q=self._text_input.value,
            **{key: inp.value for key, inp in self._choices.items()},
            k=self.value,
        )

        assert questiondict["q"], "A question is missing"
        assert questiondict["a"], "Option A is missing"
        assert questiondict["b"], "Option B is missing"
        assert questiondict["c"], "Option C is missing"
        assert questiondict["d"], "Option D is missing"
        assert questiondict["k"], "There must be a correct choice"

        if not questiondict["e"]:
            del questiondict["e"]

        return questiondict
