# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2020-10-27 17:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0159_india_ghana_irf'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_allocated', models.PositiveIntegerField()),
                ('form_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataentry.FormType')),
            ],
        ),
        migrations.AddField(
            model_name='borderstation',
            name='auto_number',
            field=models.CharField(max_length=127, null=True),
        ),
        migrations.AddField(
            model_name='autonumber',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataentry.BorderStation'),
        ),
    ]