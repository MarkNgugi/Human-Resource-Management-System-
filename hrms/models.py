from django.db import models
from accounts.models import *
from django.db import models
from datetime import timedelta
from django.utils import timezone
  

class Document(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

 
class AttendanceRecord(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)        
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee.username} - {self.date}'



class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DECLINED', 'Declined'),
    ]

    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.CharField(max_length=20, choices=[
        ('vacation', 'Vacation'),
        ('sick', 'Sick Leave'),
        ('personal', 'Personal Leave'),
    ])
    start_date = models.DateField()
    end_date = models.DateField()
    days_requested = models.IntegerField(editable=False, default=0) 
    days_approved = models.IntegerField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate days_requested based on start_date and end_date
        if self.start_date and self.end_date:
            self.days_requested = (self.end_date - self.start_date).days + 1  # Inclusive of start_date
        else:
            self.days_requested = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.status})"

    
class GeneratedReport(models.Model):
    report_name = models.CharField(max_length=255)
    metrics_selected = models.JSONField() 
    filters_used = models.JSONField()
    pdf_file = models.FileField(upload_to='reports/')
    start_date = models.DateField(null=True, blank=True)  # Make it nullable
    end_date = models.DateField(null=True, blank=True)    # Make it nullable
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_name} ({self.start_date} to {self.end_date})"

