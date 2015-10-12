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
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('numSegments', models.IntegerField()),
                ('answer', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('nativeLanguages', models.CharField(max_length=255)),
                ('otherLanguages', models.CharField(max_length=255)),
                ('targetLanguage', models.BooleanField()),
                ('gender', models.CharField(max_length=10)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transcription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('choiceType', models.IntegerField()),
                ('result', models.CharField(max_length=30)),
                ('timeTaken', models.IntegerField()),
                ('score', models.IntegerField()),
                ('audio', models.ForeignKey(to='interface.Audio')),
                ('subject', models.ForeignKey(to='interface.Subject')),
            ],
        ),
    ]
