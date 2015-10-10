# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0005_transcription_timetaken'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('numSegments', models.IntegerField()),
                ('answer', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='transcription',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transcription',
            name='audio',
            field=models.ForeignKey(to='interface.Audio'),
        ),
    ]
