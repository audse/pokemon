# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-12 00:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0057_remove_adopt_box_pos'),
    ]

    operations = [
        migrations.AddField(
            model_name='adopt',
            name='park_adopt',
            field=models.BooleanField(default=False),
        ),
    ]
