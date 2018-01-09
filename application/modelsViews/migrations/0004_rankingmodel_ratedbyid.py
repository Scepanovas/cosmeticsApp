# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-17 07:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelsViews', '0003_auto_20171119_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='rankingmodel',
            name='ratedById',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='ratedBy', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
