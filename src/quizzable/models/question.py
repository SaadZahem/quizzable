from enum import Enum
from typing import Self

from tortoise import fields, models

from .quiz import MCQuiz


class ChoiceEnum(Enum):
    a = "a"
    b = "b"
    c = "c"
    d = "d"
    e = "e"

    @classmethod
    def forward(cls, value: str | None) -> Self | None:
        """Safely convert a string character to a new instance or return None."""
        if value and value in "abcde":
            return cls(value)


class MCQuestion(models.Model):
    id = fields.IntField(pk=True)
    text = fields.TextField()
    a = fields.TextField()
    b = fields.TextField()
    c = fields.TextField()
    d = fields.TextField()
    e = fields.TextField(null=True)
    correct = fields.CharEnumField(ChoiceEnum)
    quiz = fields.ForeignKeyField("quizzable.MCQuiz", related_name="questions")

    @classmethod
    async def from_dict(cls, questiondict: dict, quiz: MCQuiz, **kwargs) -> Self:
        questiondict.update(**kwargs)
        return await cls.create(
            text=questiondict["q"],
            a=questiondict["a"],
            b=questiondict["b"],
            c=questiondict["c"],
            d=questiondict["d"],
            e=questiondict.get("e"),
            correct=ChoiceEnum(questiondict["k"]),
            quiz=quiz,
        )

    def as_dict(self) -> dict:
        questiondict = dict(
            q=self.text,
            a=self.a,
            b=self.b,
            c=self.c,
            d=self.d,
            k=self.correct and self.correct.value,
        )
        if self.e:
            questiondict.update(e=self.e)

        return questiondict

    def __repr__(self) -> str:
        return (
            f"MCQuestion#{self.id}.from_dict({self.as_dict()!r}, quiz=#{self.quiz_id})"
        )

    class Meta:
        table = "questions"
