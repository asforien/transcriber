# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0004_auto_20150928_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcription',
            name='timeTaken',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
