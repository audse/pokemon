# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-10 23:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pokedex', '0052_remove_box_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='adopt',
            name='hatched_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hatched_by', to=settings.AUTH_USER_MODEL),
        ),
    ]