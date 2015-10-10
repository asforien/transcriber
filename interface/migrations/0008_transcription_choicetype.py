# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0007_auto_20151010_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcription',
            name='choiceType',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
