# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-08 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20161108_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='stickied',
            field=models.BooleanField(default=False),
        ),
    ]
