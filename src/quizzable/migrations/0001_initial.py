from tortoise import migrations
from tortoise.migrations import operations as ops
from quizzable.models.quiz import ChoiceEnum
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='User',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('username', fields.CharField(unique=True, max_length=32)),
                ('hashed_password', fields.TextField(unique=False)),
                ('created', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'users', 'app': 'quizzable', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='MCQuiz',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('title', fields.CharField(unique=True, max_length=255)),
                ('maintainer', fields.ForeignKeyField('quizzable.User', source_field='maintainer_id', db_constraint=True, to_field='id', related_name='quizzes', on_delete=OnDelete.CASCADE)),
                ('tags', fields.TextField(default='', unique=False)),
                ('created', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('last_edited', fields.DatetimeField(auto_now=True, auto_now_add=False)),
            ],
            options={'table': 'quizzes', 'app': 'quizzable', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='MCQuestion',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('text', fields.TextField(unique=False)),
                ('a', fields.TextField(unique=False)),
                ('b', fields.TextField(unique=False)),
                ('c', fields.TextField(unique=False)),
                ('d', fields.TextField(unique=False)),
                ('e', fields.TextField(null=True, unique=False)),
                ('correct', fields.CharEnumField(description='a: a\nb: b\nc: c\nd: d\ne: e', enum_type=ChoiceEnum, max_length=1)),
                ('quiz', fields.ForeignKeyField('quizzable.MCQuiz', source_field='quiz_id', db_constraint=True, to_field='id', related_name='questions', on_delete=OnDelete.CASCADE)),
            ],
            options={'table': 'questions', 'app': 'quizzable', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
