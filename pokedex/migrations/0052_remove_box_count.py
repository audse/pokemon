# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-10 20:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0051_auto_20170809_0255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='count',
        ),
    ]
