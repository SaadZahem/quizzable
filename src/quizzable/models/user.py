from pydantic import BaseModel
from tortoise import fields, models


class Token(BaseModel):
    access_token: str
    token_type: str


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=32, unique=True)
    hashed_password = fields.TextField()
    created = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"

    def __str__(self):
        return f"@{self.username}"

    def __repr__(self):
        username = self.username
        return f"User(id={self.id}, {username=}, password=...)"
