# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_regionalforecast_regionalforecastentry_warning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localforecastentry',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
