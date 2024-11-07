from django.db import models
from accounts.models import CustomUser

class JobPost(models.Model):
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    job_requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.job_title
    

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DECLINED', 'Declined'),
    ]

    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="leave_requests")
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=50)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.status})"

