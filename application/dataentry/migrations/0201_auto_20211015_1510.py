# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-10-15 15:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0200_auto_20211011_1338'),
    ]

    operations = [
        migrations.RunSQL("insert into dataentry_permission (permission_group, action, min_level, display_order)  values ('NOTIFICATIONS','COMMITTEE','STATION',-1)"),
    ]
