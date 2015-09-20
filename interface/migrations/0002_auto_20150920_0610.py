# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transcription',
            name='distinctive_feature',
        ),
        migrations.AlterField(
            model_name='transcription',
            name='audio',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='Audio',
        ),
    ]
