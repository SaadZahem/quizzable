from nicegui import ElementFilter, ui
from nicegui.elements.choice_element import ChoiceElement

from ..models import ChoiceEnum, MCQuestion
from ..services import qy


class EditableQuestionCard(ChoiceElement):
    def __init__(self, question: MCQuestion):
        super().__init__(
            options=list("abcde"),
            value=question.correct.value if question.correct else None,
        )

        self.question = question
        self.bind_value_to(question, "correct", forward=ChoiceEnum.forward)
        self._make()

    def _make(self):
        with self, ui.card():
            # question text input
            with self._make_input(bind="text") as _inp:
                with _inp.add_slot("after"):
                    ui.button(
                        icon="delete",
                        color="accent",
                        on_click=self.delete,
                    ).props("flat")

            # 5 choices
            for prefix in "abcde":
                # choice text input
                with self._make_input(bind=prefix, prefix=prefix) as _next_inp:
                    # home-made radio button
                    with (
                        _next_inp.add_slot("before"),
                        ui.button().props("flat round") as button,
                    ):
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

                # pressing enter on last input moves focus to this input
                _inp.on(
                    "keydown.enter.prevent",
                    lambda w=_next_inp: w.run_method("focus"),
                )
                _inp = _next_inp

            # last input, prevent default
            _inp.on("keydown.enter.prevent")

    def _make_input(self, bind: str, prefix: str = "") -> ui.input:
        if not prefix:
            # input for question
            w = ui.input().classes("self-stretch")
        else:
            # input for choices
            w = ui.input(prefix="%c)" % prefix).classes("min-w-3/4")

        return w.props("outlined dense autogrow").bind_value(self.question, bind)

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
        return qy.validate(questiondict)
