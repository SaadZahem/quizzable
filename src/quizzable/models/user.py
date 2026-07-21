from pydantic import BaseModel
from tortoise import fields, models


class Token(BaseModel):
    access_token: str
    token_type: str


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=32, unique=True)
    hashed_password = fields.TextField()

    def todict(self) -> dict:
        return dict(username=self.username)

    def __str__(self):
        return f"@{self.username}"

    def __repr__(self):
        username = self.username
        hashed_password = self.hashed_password
        return f"User({username=}, {hashed_password=})"
