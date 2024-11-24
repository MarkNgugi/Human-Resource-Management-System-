# Generated by Django 5.1.3 on 2024-11-16 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0008_generatedreport'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generatedreport',
            old_name='metrics_data',
            new_name='filters_used',
        ),
        migrations.AddField(
            model_name='generatedreport',
            name='metrics_selected',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='generatedreport',
            name='pdf_file',
            field=models.FileField(upload_to='reports/'),
        ),
    ]