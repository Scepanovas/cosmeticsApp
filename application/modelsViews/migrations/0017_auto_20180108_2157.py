# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-08 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelsViews', '0016_auto_20180108_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='isBrand',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ingredientfunctionsmodel',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='ingredientsmodel',
            name='functions',
            field=models.ManyToManyField(blank=True, related_name='function', to='modelsViews.ingredientFunctionsModel'),
        ),
        migrations.AlterField(
            model_name='productsmodel',
            name='name',
            field=models.CharField(db_index=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='productsmodel',
            name='tagLine',
            field=models.CharField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='warningsmodel',
            name='referenceNumber',
            field=models.IntegerField(unique=True),
        ),
    ]