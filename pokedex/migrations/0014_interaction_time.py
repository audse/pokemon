# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-17 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0013_interaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]