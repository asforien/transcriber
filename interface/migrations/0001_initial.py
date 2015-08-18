# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('file_path', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Transcription',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('distinctive_feature', models.CharField(max_length=30)),
                ('result', models.CharField(max_length=30)),
                ('audio', models.ForeignKey(to='interface.Audio')),
            ],
        ),
    ]
