# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0003_auto_20150925_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='age',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subject',
            name='gender',
            field=models.CharField(default='Male', max_length=10),
            preserve_default=False,
        ),
    ]
