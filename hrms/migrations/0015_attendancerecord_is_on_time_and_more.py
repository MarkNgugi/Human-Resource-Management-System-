# Generated by Django 5.1.3 on 2024-11-24 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0014_alter_generatedreport_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancerecord',
            name='is_on_time',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
