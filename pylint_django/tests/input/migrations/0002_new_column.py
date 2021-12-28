"""
Migration file which adds a new column with a default value.
This should trigger a warning because adding new columns with
default value on a large table leads to DB performance issues.

See:
https://github.com/PyCQA/pylint-django/issues/118 and
https://docs.djangoproject.com/en/2.0/topics/migrations/#postgresql

> ... adding columns with default values will cause a full rewrite of
> the table, for a time proportional to its size.
> For this reason, it’s recommended you always create new columns with
> null=True, as this way they will be added immediately.
"""
# pylint: disable=missing-docstring, invalid-name
from datetime import timedelta

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("input", "0001_noerror_initial"),
    ]

    operations = [
        # add a timedelta field
        migrations.AddField(  # [new-db-field-with-default]
            model_name="testrun",
            name="estimated_time",
            field=models.DurationField(default=timedelta(0)),
        ),
    ]
