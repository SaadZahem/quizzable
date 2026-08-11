from nicegui import ElementFilter, ui

from ..models import MCQuestion, MCQuiz, User
from .editable_question_card import EditableQuestionCard


class QuestionCardContainer(ui.column):
    card = EditableQuestionCard

    def __init__(self, user: User, quiz: MCQuiz, title_input: ui.input):
        super().__init__(align_items="stretch")

        self.user = user
        self.quiz = quiz
        self.title_input = title_input

        self.sortable = self.make_sortable(
            handle=".handle",
            group=self.__class__.__name__,
        )
        self.sortable.disable()  # bugs

    def add_editable_question_card(self, question: MCQuestion | None = None):
        with self:
            self.card(question or MCQuestion())

    async def save(self):
        cards = list(ElementFilter[self.card](kind=self.card).within(instance=self))
        try:
            if not self.quiz.title:
                raise ValueError("Quiz title is missing")

            if not cards:
                raise ValueError("Questions are missing")

            for card in cards:
                card.validate_values()  # raises AssertionError

        except ValueError as error:
            ui.notify(error.args[0], color="negative")

        except AssertionError as error:
            ui.notify(error.args[0], color="negative")
            ui.navigate.to(card)

        else:
            await self.quiz.save()
            for card in cards:
                card.question.quiz = self.quiz
                await card.question.save()

            ui.navigate.to("/home")
