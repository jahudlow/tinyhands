# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2021-06-15 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0005_auto_20210518_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherbudgetitemcost',
            name='form_section',
            field=models.IntegerField(blank=True, null=True, verbose_name=[(1, 'Travel'), (2, 'Miscellaneous'), (3, 'Awareness'), (5, 'Potential Victim Care'), (7, 'Communication'), (8, 'Staff & Benefits'), (10, 'Administration'), (11, 'Past Month Sent Money'), (12, 'Limbo Potential Victims')]),
        ),
        
        migrations.RunSQL("insert into budget_otherbudgetitemcost (name, cost, form_section, budget_item_parent_id) "\
                "select 'Limbo PVs (' || "\
                    "food_and_gas_limbo_girls_multiplier || '*' || "\
                    "food_and_gas_number_of_limbo_girls || '*' || "\
                    "food_and_gas_number_of_days || ')' as name, "\
                    "food_and_gas_limbo_girls_multiplier * food_and_gas_number_of_limbo_girls * food_and_gas_number_of_days as cost, "\
                    "5 as form_section, "\
                    "id as budget_item_parent_id "\
                "from budget_borderstationbudgetcalculation "\
                "where food_and_gas_limbo_girls_multiplier > 0 "\
                    "and food_and_gas_number_of_limbo_girls > 0"\
                    "and food_and_gas_number_of_days > 0"),
    ]
