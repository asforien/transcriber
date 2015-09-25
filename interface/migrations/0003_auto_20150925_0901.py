# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0002_auto_20150920_0610'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(primary_key=True, max_length=255, serialize=False)),
                ('nativeLanguages', models.CharField(max_length=255)),
                ('otherLanguages', models.CharField(max_length=255)),
                ('targetLanguage', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='transcription',
            name='subject',
            field=models.ForeignKey(default=None, to='interface.Subject'),
            preserve_default=False,
        ),
    ]
