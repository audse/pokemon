# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-06 21:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0043_trade_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='adopt',
            name='daycare',
            field=models.BooleanField(default=False),
        ),
    ]
