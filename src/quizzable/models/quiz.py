from enum import Enum

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

    def __str__(self):
        return self.file
