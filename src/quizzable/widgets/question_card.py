from nicegui import ElementFilter, background_tasks, html, ui
from nicegui.elements.choice_element import ChoiceElement

from ..models import ChoiceEnum, MCQuestion, MCQuiz, User


class QuestionCardContainer(ui.column):
    def __init__(self, user: User, title_input: ui.input):
        super().__init__(align_items="stretch")
        sortable = self.make_sortable(handle=".handle", group=self.__class__.__name__)
        sortable.disable()  # bugs

        self.user = user
        self.title_input = title_input
        self.cards: list[EditableQuestionCard] = []

    def add_editable_question_card(self):
        with self:
            card = EditableQuestionCard()
            self.cards.append(card)

    async def _create_quiz(self, values: list[dict[str, str]]):
        new_quiz = await MCQuiz.create(
            title=self.title_input.value.strip().title(),
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

    def create_quiz(self):
        values = []
        try:
            if not self.cards:
                raise ValueError

            for card in self.cards:
                values.append(card.validate_values())

        except ValueError:
            ui.notify("The quiz cannot be empty", color="negative")
        except AssertionError:
            ui.notify("There must be a correct choice", color="negative")
            ui.navigate.to(card)
        else:
            background_tasks.create(self._create_quiz(values))
            ui.navigate.back()


class EditableQuestionCard(ChoiceElement):
    def __init__(self, value: str | None = None):
        options = {prefix: "" for prefix in "abcde"}
        super().__init__(options=options, value=value or None)
        self._choices = {}
        self._build()

    def _build(self):
        with self, ui.card():
            with (
                ui.input()
                .props("outlined dense autogrow")
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
                self._choices[prefix] = _inp = ui.input(prefix=f"{prefix})")
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

        assert questiondict["q"]
        assert questiondict["a"]
        assert questiondict["b"]
        assert questiondict["c"]
        assert questiondict["d"]
        assert questiondict["k"]

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
