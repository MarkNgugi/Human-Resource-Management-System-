from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LeaveRequest, AttendanceRecord
from datetime import timedelta

@receiver(post_save, sender=LeaveRequest)
def update_attendance_on_leave_approval(sender, instance, created, **kwargs):
    # Check if the leave request was approved
    if instance.status == 'APPROVED':
        employee = instance.employee
        leave_date = instance.start_date
        # Check if an attendance record exists for the leave date
        attendance_record = AttendanceRecord.objects.filter(
            employee=employee,
            date=leave_date
        ).first()
        
        # If an attendance record doesn't exist, create one for that day
        if not attendance_record:
            attendance_record = AttendanceRecord.objects.create(
                employee=employee,
                date=leave_date,
                attendance_status='on_leave',
                remarks='On leave'
            )
        else:
            # Update the existing record if needed
            attendance_record.attendance_status = 'on_leave'
            attendance_record.remarks = 'On leave'
            attendance_record.save()
