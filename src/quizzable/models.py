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
    title = fields.CharField(max_length=255, unique=True)
    last_edited = fields.DatetimeField(auto_now=True)
    tags = fields.TextField(default="")
    maintainer = fields.ForeignKeyField("models.User", related_name="quizzes")

    @property
    def file(self):
        return self.title.lower().replace(*" -")

    def __str__(self):
        return self.file


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=32, unique=True)
    hashed_password = fields.TextField()

    def __str__(self):
        return f"@{self.username}"

    def __repr__(self):
        username = self.username
        hashed_password = self.hashed_password
        return f"User({username=}, {hashed_password=})"
