# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0008_transcription_choicetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='id',
            field=models.AutoField(serialize=False, auto_created=True, default=1, primary_key=True, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subject',
            name='email',
            field=models.CharField(max_length=255),
        ),
    ]
