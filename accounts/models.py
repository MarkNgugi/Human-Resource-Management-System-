from django.contrib.auth.models import AbstractUser
from django.db import models



class Department(models.Model):
    name = models.CharField(max_length=100,default='ADMIN')

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hr_manager', 'HR Manager'),
        ('employee', 'Employee'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    gender = models.CharField(max_length=20,choices=[
        ('male','Male'),        
        ('female','Female')
    ],default='male')
    phone = models.CharField(max_length=15, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE, default=1)    
    start_date = models.DateField(blank=True, null=True)
    exit_date = models.DateField(null=True, blank=True)
    reason_for_leaving = models.CharField(max_length=255, null=True, blank=True)
    