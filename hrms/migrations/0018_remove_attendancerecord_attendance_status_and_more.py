# Generated by Django 5.1.4 on 2024-12-27 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0017_remove_attendancerecord_source_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancerecord',
            name='attendance_status',
        ),
        migrations.RemoveField(
            model_name='attendancerecord',
            name='is_late',
        ),
        migrations.RemoveField(
            model_name='attendancerecord',
            name='is_on_time',
        ),
        migrations.RemoveField(
            model_name='attendancerecord',
            name='late_duration',
        ),
    ]
