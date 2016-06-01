# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LocalForecast',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('icon_url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LocalForecastEntry',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('wave_direction', models.FloatField()),
                ('wave_height_sig', models.FloatField()),
                ('wave_height_max', models.FloatField()),
                ('wave_period', models.FloatField()),
                ('wind_direction', models.FloatField()),
                ('wind_speed', models.FloatField()),
                ('wind_burst', models.FloatField()),
                ('local_forecast', models.ForeignKey(to='api.LocalForecast')),
            ],
        ),
    ]
