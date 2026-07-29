from nicegui import ElementFilter, ui
from nicegui.elements.choice_element import ChoiceElement

from ..models import ChoiceEnum, MCQuestion


class EditableQuestionCard(ChoiceElement):
    def __init__(self, question: MCQuestion):
        super().__init__(
            options={prefix: "" for prefix in "abcde"},
            value=question.correct.value if question.correct else None,
        )

        self.question = question
        self.bind_value_to(question, "correct", forward=ChoiceEnum.forward)
        self._build()

    def _build(self):
        with self, ui.card():
            with (
                ui.input()
                .bind_value(self.question, "text")
                .props("outlined dense autogrow")
                .classes("self-stretch")
                .add_slot("after"),
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
                _inp = ui.input(prefix=f"{prefix})").bind_value(self.question, prefix)
                with _inp.props("outlined dense autogrow").add_slot("before"):
                    with ui.button().props("flat round") as button:
                        icon = ui.icon(
                            "radio_button_checked"
                            if self.value == prefix
                            else "radio_button_unchecked"
                        ).mark("radio")
                        button.on(
                            "click",
                            lambda ico=icon, value=prefix: self._handle_change(
                                ico, value
                            ),
                        )

    def _handle_change(self, ico: ui.icon, value: str):
        (
            ElementFilter(kind=ui.icon, marker="radio")
            .within(instance=self)
            .props("name=radio_button_unchecked")
        )
        ico.props("name=radio_button_checked")
        self.value = value

    def validate_values(self) -> dict[str, str]:
        questiondict = self.question.as_dict()

        assert questiondict["q"], "A question is missing"
        assert questiondict["a"], "Option A is missing"
        assert questiondict["b"], "Option B is missing"
        assert questiondict["c"], "Option C is missing"
        assert questiondict["d"], "Option D is missing"
        # Option 'e' is optional

        assert questiondict["k"], "There must be a correct choice"
        return questiondict
