# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-06 13:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelsViews', '0010_brand_istested'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkinTypeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='SuggestedReasonsConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=400)),
                ('function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggestedFunction', to='modelsViews.ingredientFunctionsModel')),
            ],
        ),
        migrations.DeleteModel(
            name='UploadedImage',
        ),
        migrations.AddField(
            model_name='skintypemodel',
            name='notSuggested',
            field=models.ManyToManyField(related_name='notSuggested', to='modelsViews.SuggestedReasonsConfig'),
        ),
        migrations.AddField(
            model_name='skintypemodel',
            name='suggested',
            field=models.ManyToManyField(related_name='suggested', to='modelsViews.SuggestedReasonsConfig'),
        ),
        migrations.AddField(
            model_name='skintypemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testedUser', to=settings.AUTH_USER_MODEL),
        ),
    ]