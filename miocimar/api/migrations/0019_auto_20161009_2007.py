# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-09 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_localforecast_taxonomy_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localforecast',
            name='comment',
            field=models.CharField(max_length=4000),
        ),
    ]
