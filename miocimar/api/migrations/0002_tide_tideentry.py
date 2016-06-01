# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tide',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('icon_url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TideEntry',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('tide_height', models.FloatField()),
                ('is_high_tide', models.BooleanField()),
                ('tide_region', models.ForeignKey(to='api.Tide')),
            ],
        ),
    ]
