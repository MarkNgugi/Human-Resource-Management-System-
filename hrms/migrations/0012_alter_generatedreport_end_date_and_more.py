# Generated by Django 5.1.3 on 2024-11-17 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0011_generatedreport_end_date_generatedreport_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatedreport',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='generatedreport',
            name='start_date',
            field=models.DateField(),
        ),
    ]
