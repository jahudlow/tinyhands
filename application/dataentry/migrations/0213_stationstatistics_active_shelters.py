# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-01-04 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0212_auto_20220103_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='stationstatistics',
            name='active_shelters',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
