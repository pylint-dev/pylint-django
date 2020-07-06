# pylint: disable=missing-docstring, invalid-name
from django.db import migrations


# pylint: disable=unused-argument
def forwards_test(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(),  # [missing-backwards-migration-callable]
        migrations.RunPython(  # [missing-backwards-migration-callable]
            forwards_test),
        migrations.RunPython(  # [missing-backwards-migration-callable]
            code=forwards_test),
        migrations.RunPython(  # [missing-backwards-migration-callable]
            code=forwards_test, atomic=False)
    ]
