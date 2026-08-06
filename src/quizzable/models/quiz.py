from tortoise import fields, models


class MCQuiz(models.Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=255, unique=True)
    maintainer = fields.ForeignKeyField("quizzable.User", related_name="quizzes")
    tags = fields.TextField(default="")
    created = fields.DatetimeField(auto_now_add=True)
    last_edited = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "quizzes"

    @property
    def file(self):
        return self.title.lower().replace(*" -") + ".yml"

    def __repr__(self) -> str:
        return f"MCQuiz#{self.id}(title={self.title!r}, maintainer=#{self.maintainer_id}, created={self.created.strftime('%Y%m%d_%a')})"
