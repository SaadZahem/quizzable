from __future__ import annotations

from nicegui import ElementFilter, background_tasks, html, ui
from nicegui.elements.choice_element import ChoiceElement

from ..models import ChoiceEnum, MCQuestion, MCQuiz, User
from ..utils import totitle


class QuestionCardContainer(ui.column):
    def __init__(self, user: User, title_input: ui.input, quiz: MCQuiz | None = None):
        super().__init__(align_items="stretch")
        sortable = self.make_sortable(handle=".handle", group=self.__class__.__name__)
        sortable.disable()  # bugs

        self.user = user
        self.title_input = title_input
        self.quiz = quiz

    def add_editable_question_card(self, question: MCQuestion | None = None):
        with self:
            if self.quiz and not question:
                EditableQuestionCard(MCQuestion(quiz=self.quiz))
            else:
                EditableQuestionCard(question)

    async def _create_quiz(self, title: str, values: list[dict[str, str]]):
        new_quiz = await MCQuiz.create(
            title=title,
            maintainer=self.user,
            tags="\n".join([]),
        )

        for questiondict in values:
            await MCQuestion.create(
                text=questiondict["q"],
                a=questiondict["a"],
                b=questiondict["b"],
                c=questiondict["c"],
                d=questiondict["d"],
                e=questiondict.get("e"),
                correct=ChoiceEnum(questiondict["k"]),
                quiz=new_quiz,
            )

    async def _save_quiz(self, cards: list[EditableQuestionCard]):
        for card in cards:
            await card.question.save()
        await self.quiz.save()

    def create_quiz(self):
        title = totitle(self.title_input.value.strip())
        cards = ElementFilter(kind=EditableQuestionCard)
        values = []
        try:
            if not title:
                raise ValueError("A quiz title is missing")

            for card in cards:
                values.append(card.validate_values())

            if not values:
                raise ValueError("Questions are missing")

        except ValueError as error:
            ui.notify(error.args[0], color="negative")

        except AssertionError as error:
            ui.notify(error.args[0], color="negative")
            ui.navigate.to(card)

        else:
            background_tasks.create(self._create_quiz(title, values))
            ui.navigate.to("/home")

    def save_quiz(self):
        cards = ElementFilter(kind=EditableQuestionCard)
        values = []
        try:
            if not self.quiz.title:
                raise ValueError("A quiz title is missing")

            for card in cards:
                values.append(card.validate_values())

            if not values:
                raise ValueError("Questions are missing")

        except ValueError as error:
            ui.notify(error.args[0], color="negative")

        except AssertionError as error:
            ui.notify(error.args[0], color="negative")
            ui.navigate.to(card)

        else:
            background_tasks.create(self._save_quiz(cards))
            ui.navigate.to("/home")


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
