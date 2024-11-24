# Generated by Django 4.2.11 on 2024-11-16 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0007_attendancerecord_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('metrics_data', models.JSONField()),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='reports/')),
            ],
        ),
    ]