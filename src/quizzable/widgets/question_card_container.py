from __future__ import annotations

from nicegui import ElementFilter, background_tasks, ui

from ..models import ChoiceEnum, MCQuestion, MCQuiz, User
from ..utils import totitle
from .editable_question_card import EditableQuestionCard


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
