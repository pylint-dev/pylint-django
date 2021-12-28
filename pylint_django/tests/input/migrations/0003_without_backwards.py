# pylint: disable=missing-docstring, invalid-name, line-too-long
from django.db import migrations


def forwards_test(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(),  # [missing-backwards-migration-callable]
        migrations.RunPython(forwards_test),  # [missing-backwards-migration-callable]
        migrations.RunPython(code=forwards_test),  # [missing-backwards-migration-callable]
        migrations.RunPython(code=forwards_test, atomic=False),  # [missing-backwards-migration-callable]
    ]
