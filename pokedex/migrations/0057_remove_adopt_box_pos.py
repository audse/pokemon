# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-11 07:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0056_box_create_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adopt',
            name='box_pos',
        ),
    ]
