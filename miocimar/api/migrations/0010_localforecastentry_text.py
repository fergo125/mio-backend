# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20160726_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='localforecastentry',
            name='text',
            field=models.TextField(default='Blank text'),
            preserve_default=False,
        ),
    ]
