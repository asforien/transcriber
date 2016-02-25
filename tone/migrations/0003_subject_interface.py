# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tone', '0002_auto_20160119_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='interface',
            field=models.IntegerField(default=0),
        ),
    ]
