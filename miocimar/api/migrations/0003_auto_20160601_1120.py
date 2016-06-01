# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_tide_tideentry'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tide',
            new_name='TideRegion',
        ),
    ]
