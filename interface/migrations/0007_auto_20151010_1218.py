# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0006_auto_20151010_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
