from nicegui import ElementFilter, html, ui
from nicegui.elements.choice_element import ChoiceElement

from ..models import MCQuestion


class EditableQuestionCard(ChoiceElement):
    def __init__(self, value: str | None = None):
        options = {prefix: "" for prefix in "abcde"}
        super().__init__(options=options, value=value or None)
        self._build()

    def _build(self):
        with self, ui.card():
            with (
                ui.input()
                .props("outlined dense autogrow")
                .classes("self-stretch") as inp,
                inp.add_slot("after"),
                ui.button(icon="delete", color="accent", on_click=self.delete).props(
                    "flat"
                ),
            ):
                pass

            for index, prefix in enumerate("abcde", start=1):
                with (
                    ui.input(prefix=f"{prefix})").props(
                        "outlined dense autogrow"
                    ) as inp,
                    inp.add_slot("before"),
                    ui.button().props("flat round") as button,
                    ui.icon(
                        "radio_button_checked"
                        if self.value == prefix
                        else "radio_button_unchecked"
                    ) as icon,
                ):
                    button.on(
                        "click",
                        lambda ico=icon, btn=button: (
                            ElementFilter(kind=ui.icon)
                            .within(instance=self)
                            .props("name=radio_button_unchecked")
                            and ico.props("name=radio_button_checked")
                        ),
                    )


def question_card(number, question: MCQuestion, value: str = "-", *, review=False):
    q = question
    choices = [q.a, q.b, q.c, q.d]
    if q.e:
        choices.append(q.e)

    with ui.card().classes("self-stretch xl:w-xl xl:self-center") as card:
        if not review:
            html.strong(f"{number}. " + question.text)
            ui.radio(
                {
                    index: f"{prefix}) {choice}"
                    for index, prefix, choice in zip(range(5), "abcde", choices)
                },
            )
            return card

        # Question card for reviewing
        with ui.row().classes("w-full justify-end"):
            with ui.column():
                question_text = "{}. {}".format(number, question.text)
                html.strong(question_text)
                for prefix, choice in zip("abcde", choices):
                    choice_text = "{}) {}".format(prefix, choice)
                    label = ui.label(choice_text).classes("py-1 px-2 rounded-lg")

                    if prefix == question.correct.value:
                        label.classes("bg-green-300 text-[blue]")
                    elif prefix == value:
                        label.classes("bg-red-300 text-[blue]")

            ui.space().classes("grow")
            with ui.row().classes("self-stretch"):
                ui.separator().props("vertical")
                grade_text = "%i/1" % (value == question.correct.value)
                ui.label(grade_text).classes("my-auto text-end")

    return card
