# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-09 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20160602_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegionalForecast',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('icon_url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RegionalForecastEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('animation_url', models.CharField(max_length=100)),
                ('regional_forecast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.RegionalForecast')),
            ],
        ),
        migrations.CreateModel(
            name='Warning',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('level', models.IntegerField()),
                ('date', models.DateField()),
                ('text', models.TextField()),
            ],
        ),
    ]
