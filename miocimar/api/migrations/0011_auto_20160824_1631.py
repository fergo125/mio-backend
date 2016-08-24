# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-24 16:31
from __future__ import unicode_literals

from django.db import migrations, models

from datetime import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20160821_0400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regionalforecastentry',
            name='regional_forecast',
        ),
        migrations.AddField(
            model_name='regionalforecast',
            name='animation_url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='regionalforecast',
            name='date',
            field=models.DateField(default=datetime.now()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='regionalforecast',
            name='text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='RegionalForecastEntry',
        ),
    ]
