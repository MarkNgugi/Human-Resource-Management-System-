# Generated by Django 4.2.11 on 2024-11-10 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_customuser_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.department'),
        ),
    ]
