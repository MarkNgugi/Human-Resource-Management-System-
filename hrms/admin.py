from django.contrib import admin
from .models import *

admin.site.register(LeaveRequest)
admin.site.register(AttendanceRecord)
admin.site.register(GeneratedReport)
admin.site.register(Document)