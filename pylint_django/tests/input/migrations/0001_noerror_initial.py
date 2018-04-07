"""
Initial migration which should not raise any pylint warnings.
"""
# pylint: disable=missing-docstring, invalid-name
from django.db import migrations, models


class Migration(migrations.Migration):
    operations = [
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('summary', models.TextField()),
                ('environment_id', models.IntegerField(default=0)),
                ('auto_update_run_status', models.BooleanField(default=False)),
            ],
        ),
    ]
