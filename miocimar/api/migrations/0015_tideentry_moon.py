# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-09 02:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='tideentry',
            name='moon',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
