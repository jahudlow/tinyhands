# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2020-05-13 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0142_auto_20200506_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='irfcommon',
            name='logbook_champion_verification',
            field=models.BooleanField(default=False, verbose_name='Champion verification'),
        ),
        migrations.AddField(
            model_name='irfcommon',
            name='rescue',
            field=models.BooleanField(default=False, verbose_name='Rescue'),
        ),
        migrations.RunSQL("update dataentry_irfcommon set logbook_first_verification = 'Should not count as an Intercept' "\
                        "where logbook_first_verification like 'Should%'"),
        migrations.RunSQL("update dataentry_irfcommon set logbook_second_verification = 'Should not count as an Intercept' "\
                        "where logbook_second_verification like 'Should%'"),
    ]
