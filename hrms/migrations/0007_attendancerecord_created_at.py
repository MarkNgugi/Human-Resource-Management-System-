# Generated by Django 4.2.11 on 2024-11-11 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0006_delete_jobpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancerecord',
            name='created_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
