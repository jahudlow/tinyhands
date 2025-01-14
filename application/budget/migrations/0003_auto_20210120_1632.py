# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2021-01-20 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_borderstationbudgetcalculation_notes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borderstationbudgetcalculation',
            old_name='shelter_electricity',
            new_name='shelter_electricity_amount',
        ),
        migrations.RenameField(
            model_name='borderstationbudgetcalculation',
            old_name='shelter_rent',
            new_name='shelter_rent_amount',
        ),
        migrations.RenameField(
            model_name='borderstationbudgetcalculation',
            old_name='shelter_water',
            new_name='shelter_water_amount',
        ),
        
        migrations.CreateModel(
            name='StaffBudgetItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('cost', models.IntegerField(blank=True, default=0, null=True)),
                ('budget_calc_sheet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budget.BorderStationBudgetCalculation')),
                ('staff_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='static_border_stations.Staff')),
            ],
        ),
        
        migrations.RunSQL("insert into budget_staffbudgetitem (type_name, description, cost, budget_calc_sheet_id, staff_person_id) "\
            "select 'Salary', '', salary, budget_calc_sheet_id, staff_person_id from budget_staffsalary "),
        
        # Create other items entries for bikes for staff
        migrations.RunSQL("insert into budget_otherbudgetitemcost (name, cost, form_section, budget_item_parent_id) "\
            "select 'Staff bikes', travel_number_of_staff_using_bikes * travel_number_of_staff_using_bikes_multiplier, 1, id "\
            "from budget_borderstationbudgetcalculation "\
            "where travel_number_of_staff_using_bikes > 0 and travel_number_of_staff_using_bikes_multiplier > 0"),
        migrations.RunSQL("insert into budget_otherbudgetitemcost (name, cost, form_section, budget_item_parent_id) "\
            "select 'Shelter startup', shelter_shelter_startup_amount, 5, id "\
            "from budget_borderstationbudgetcalculation "\
            "where shelter_shelter_startup = true"),
        migrations.RunSQL("insert into budget_otherbudgetitemcost (name, cost, form_section, budget_item_parent_id) "\
            "select 'Last month''s medical expense', medical_last_months_expense, 8, id "\
            "from budget_borderstationbudgetcalculation "\
            "where medical_last_months_expense != 0"),
         migrations.RunSQL("insert into budget_otherbudgetitemcost (name, cost, form_section, budget_item_parent_id) "\
            "select 'Staff communication (' || communication_each_staff || ' * ' || communication_each_staff_multiplier ||')', communication_each_staff * communication_each_staff_multiplier, 7, id "\
            "from budget_borderstationbudgetcalculation "\
            "where communication_each_staff > 0 and communication_each_staff_multiplier > 0"),
         
         migrations.RunSQL("insert into budget_otherbudgetitemcost (name, cost, form_section, budget_item_parent_id) "\
            "select 'Manager communication', communication_manager_amount, 7, id "\
            "from budget_borderstationbudgetcalculation "\
            "where communication_manager = true"),
         migrations.RunSQL("insert into budget_otherbudgetitemcost (name, cost, form_section, budget_item_parent_id) "\
            "select 'Manager travel', travel_manager_with_bike_amount, 1, id "\
            "from budget_borderstationbudgetcalculation "\
            "where travel_manager_with_bike = true"),
        
        migrations.RunSQL("update budget_otherbudgetitemcost set form_section=5 where form_section=6"),
        migrations.RunSQL("update budget_otherbudgetitemcost set form_section=2 where form_section=4"),
        migrations.RunSQL("update budget_otherbudgetitemcost set form_section=8 where form_section=9"),
    ]
