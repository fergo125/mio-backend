# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-28 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_tideregion_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='tideregion',
            name='medium_level',
            field=models.FloatField(default=1.4),
            preserve_default=False,
        ),
    ]
