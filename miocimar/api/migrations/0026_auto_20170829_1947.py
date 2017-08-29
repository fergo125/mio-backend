# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-29 19:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_tideregion_mean_highest_tides'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slideforecastimage',
            name='forecast_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slides', to='api.RegionalForecast'),
        ),
    ]
