# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-29 21:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localforecastentry',
            name='text',
        ),
    ]
