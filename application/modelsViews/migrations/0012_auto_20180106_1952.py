# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-06 19:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelsViews', '0011_auto_20180106_1354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skintypemodel',
            name='user',
        ),
        migrations.AddField(
            model_name='brand',
            name='skinType',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='skinType', to='modelsViews.SkinTypeModel'),
        ),
    ]
