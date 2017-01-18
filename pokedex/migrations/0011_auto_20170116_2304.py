# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-17 05:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0010_lab_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='adopt',
            name='party',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='adopt',
            name='nature',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
    ]
