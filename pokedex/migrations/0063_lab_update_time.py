# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-12 22:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0062_adopt_daycare_adopt'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]