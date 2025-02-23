from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import apps


class Department(models.Model):
    name = models.CharField(max_length=100, default='ADMIN')
    work_start_time = models.TimeField(null=True, blank=True) 
    work_end_time = models.TimeField(null=True, blank=True) 
    late_checkin_buffer = models.IntegerField(default=10)  # Buffer in minutes

    def __str__(self):
        return self.name  


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hr_manager', 'HR Manager'),
        ('employee', 'Employee'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female')], default='male')
    phone = models.CharField(max_length=15, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, default=None, null=True)
    start_date = models.DateField(blank=True, null=True)
    exit_date = models.DateField(null=True, blank=True)
    reason_for_leaving = models.CharField(max_length=255, null=True, blank=True)
    otp_secret = models.CharField(max_length=32, default='', blank=True)

    def save(self, *args, **kwargs):
        if not self.department:
            department_model = apps.get_model('hrms', 'Department')
            department, created = department_model.objects.get_or_create(name='ADMIN')
            self.department = department
        super().save(*args, **kwargs)


    