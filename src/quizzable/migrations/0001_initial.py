from tortoise import migrations
from tortoise.migrations import operations as ops
from src.quizzable.models import ChoiceEnum
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='MCQuiz',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('title', fields.CharField(max_length=255)),
            ],
            options={'table': 'mcquiz', 'app': 'models', 'pk_attr': 'id'},
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
                ('quiz', fields.ForeignKeyField('models.MCQuiz', source_field='quiz_id', db_constraint=True, to_field='id', related_name='questions', on_delete=OnDelete.CASCADE)),
            ],
            options={'table': 'mcquestion', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
