# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-11 20:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0006_auto_20170811_0316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pm',
            old_name='deleted_by_receiver',
            new_name='removed_by_receiver',
        ),
        migrations.RenameField(
            model_name='pm',
            old_name='deleted_by_sender',
            new_name='removed_by_sender',
        ),
    ]
