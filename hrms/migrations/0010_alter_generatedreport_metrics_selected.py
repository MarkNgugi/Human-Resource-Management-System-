# Generated by Django 5.1.3 on 2024-11-16 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0009_rename_metrics_data_generatedreport_filters_used_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatedreport',
            name='metrics_selected',
            field=models.JSONField(),
        ),
    ]
