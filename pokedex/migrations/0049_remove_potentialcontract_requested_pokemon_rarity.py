# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-09 01:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0048_auto_20170808_1917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='potentialcontract',
            name='requested_pokemon_rarity',
        ),
    ]
