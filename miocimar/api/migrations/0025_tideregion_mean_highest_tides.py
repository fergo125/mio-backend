# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-29 19:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20170818_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='tideregion',
            name='mean_highest_tides',
            field=models.FloatField(default=0),
        ),
    ]
