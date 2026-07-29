from __future__ import annotations

from nicegui import html, ui

from ..models import MCQuestion


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
