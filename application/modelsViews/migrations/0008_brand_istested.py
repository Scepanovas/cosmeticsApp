# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-06 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelsViews', '0007_auto_20180103_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='isTested',
            field=models.BooleanField(default=True),
        ),
    ]
