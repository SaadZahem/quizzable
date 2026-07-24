from __future__ import annotations

from enum import Enum
from typing import Self

from tortoise import fields, models


class ChoiceEnum(Enum):
    a = "a"
    b = "b"
    c = "c"
    d = "d"
    e = "e"


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
            k=self.correct.value,
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


class MCQuiz(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, unique=True)
    maintainer = fields.ForeignKeyField("quizzable.User", related_name="quizzes")
    tags = fields.TextField(default="")
    created = fields.DatetimeField(auto_now_add=True)
    last_edited = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "quizzes"

    @property
    def file(self):
        return self.title.lower().replace(*" -")

    def __repr__(self) -> str:
        return f"MCQuiz#{self.id}(title={self.title!r}, maintainer=#{self.maintainer_id}, created={self.created.strftime('%Y%m%d_%a')})"
