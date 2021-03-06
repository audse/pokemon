# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-06 06:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pokedex', '0034_adopt_hatch_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sending_message', models.CharField(blank=True, max_length=140, null=True)),
                ('recieving_adopt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recieving_adopt', to='pokedex.Adopt')),
                ('recieving_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiving_user', to=settings.AUTH_USER_MODEL)),
                ('sending_adopt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sending_adopt', to='pokedex.Adopt')),
                ('sending_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sending_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
