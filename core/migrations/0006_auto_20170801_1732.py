# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-01 22:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_currency'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='owner',
            new_name='user',
        ),
    ]
