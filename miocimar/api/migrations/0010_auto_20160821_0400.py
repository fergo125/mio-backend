# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-21 04:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20160726_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='localforecast',
            old_name='icon_url',
            new_name='large_icon_url',
        ),
        migrations.RenameField(
            model_name='localforecast',
            old_name='map_url',
            new_name='large_map_url',
        ),
        migrations.RenameField(
            model_name='regionalforecast',
            old_name='icon_url',
            new_name='large_icon_url',
        ),
        migrations.RenameField(
            model_name='tideregion',
            old_name='icon_url',
            new_name='large_icon_url',
        ),
        migrations.AddField(
            model_name='localforecast',
            name='comment',
            field=models.CharField(default='', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localforecast',
            name='english_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localforecast',
            name='medium_icon_url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localforecast',
            name='medium_map_url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localforecast',
            name='small_icon_url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localforecast',
            name='small_map_url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='regionalforecast',
            name='english_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='regionalforecast',
            name='medium_icon_url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='regionalforecast',
            name='small_icon_url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tideregion',
            name='english_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tideregion',
            name='medium_icon_url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tideregion',
            name='small_icon_url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
