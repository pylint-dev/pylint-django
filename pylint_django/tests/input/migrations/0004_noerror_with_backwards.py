# pylint: disable=missing-docstring, invalid-name
from django.db import migrations


# pylint: disable=unused-argument
def forwards_test(apps, schema_editor):
    pass


# pylint: disable=unused-argument
def backwards_test(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(forwards_test, backwards_test),
        migrations.RunPython(forwards_test, reverse_code=backwards_test),
        migrations.RunPython(code=forwards_test, reverse_code=backwards_test)
    ]
