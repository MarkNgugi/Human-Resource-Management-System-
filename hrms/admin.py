from django.contrib import admin
from .models import *

admin.site.register(JobPost)
admin.site.register(LeaveRequest)
admin.site.register(AttendanceRecord)