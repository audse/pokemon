# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-15 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='online',
            field=models.BooleanField(default=True),
        ),
    ]
