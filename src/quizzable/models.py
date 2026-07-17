from enum import Enum

from tortoise import fields, models


class ChoiceEnum(Enum):
    a = "a"
    b = "b"
    c = "c"
    d = "d"
    e = "e"


class MCQuestion(models.Model):
    id = fields.IntField(primary_key=True)
    text = fields.TextField()
    a = fields.TextField()
    b = fields.TextField()
    c = fields.TextField()
    d = fields.TextField()
    e = fields.TextField(null=True)
    correct = fields.CharEnumField(ChoiceEnum)
    quiz = fields.ForeignKeyField("models.MCQuiz", related_name="questions")


class MCQuiz(models.Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=255)

    @property
    def file(self):
        return self.title.lower().replace(*" -")
