# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-06 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0041_trade_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='adopt',
            name='ready_to_evo_by_trade',
            field=models.BooleanField(default=False),
        ),
    ]