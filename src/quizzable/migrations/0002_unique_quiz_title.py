from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0001_initial')]

    initial = False

    operations = [
        ops.AlterField(
            model_name='MCQuiz',
            name='title',
            field=fields.CharField(unique=True, max_length=255),
        ),
    ]
