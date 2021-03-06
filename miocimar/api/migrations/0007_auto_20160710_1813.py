# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-10 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20160629_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='localforecast',
            name='map_url',
            field=models.CharField(default='http://res.cloudinary.com/dh0xtya60/image/upload/v1468174124/mapa_escondido_norte_pacifico_norte_3x_rgpdll.png', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='localforecast',
            name='icon_url',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='regionalforecast',
            name='icon_url',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='regionalforecastentry',
            name='animation_url',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='tideregion',
            name='icon_url',
            field=models.CharField(max_length=200),
        ),
    ]
