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
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('fileName', models.CharField(max_length=255)),
                ('numSegments', models.IntegerField()),
                ('answer', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('dominant_language', models.CharField(max_length=25)),
                ('other_languages', models.CharField(max_length=255)),
                ('target_language', models.BooleanField(default=False)),
                ('gender', models.CharField(max_length=10)),
                ('age', models.IntegerField(default=0)),
                ('question_order', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Transcription',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('result', models.CharField(max_length=40)),
                ('timeTaken', models.IntegerField()),
                ('score', models.IntegerField()),
                ('audio', models.ForeignKey(to='tone.Audio')),
                ('subject', models.ForeignKey(to='tone.Subject')),
            ],
        ),
    ]
