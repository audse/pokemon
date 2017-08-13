# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-11 08:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0004_remove_pm_parent_pm'),
    ]

    operations = [
        migrations.AddField(
            model_name='pm',
            name='parent_pm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pm.PM'),
        ),
    ]
