from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('hr_manager_dashboard/', hr_manager_dashboard, name='hr_manager_dashboard'),
    path('employee_dashboard/', employee_dashboard, name='employee_dashboard'),

    path('employee-profile/',employee_profile,name = 'employeeprofile'),
    path('add_employee/', add_employee, name='addemployee'),
    path('document_management/',document_management,name='documentmanagement'),
    path('documents/<int:employee_id>/manage/', manage_documents, name='manage_documents'),
    path('documents/<int:employee_id>/add/', add_document, name='add_document'),

    path('offboarding/',offboarding,name='offboarding'),

    path('attendance/department',departments,name='departments'),
    path('departmant-attendance/<int:id>/',dep_attendance,name='depattendance'),
    path('attendance-reports',attendance_reports,name='attendancereports'),
    

    path('time-tracking/',time_tracking,name='timetracking'),
    path('report-generation/',attendance_reports_generation,name='attendancereportsgeneration'),
    path('review_leaves/',leave_requests,name='reviewleaves'),
    path('update_leave_status/<int:leave_id>/<str:status>/',update_leave_status, name='update_leave_status'),
    path('leave-balance/',leave_balance,name='leavebalance'),

    path('report-builder/',report_builder,name='reportbuilder'),
    path('report-list/', report_list, name='report_list'),
    path('export-report/<int:report_id>/', export_report_pdf, name='export_report_pdf'),
    path('hr-dash/',report_builder,name='hrdash'),


    path('system-config/',system_config,name='systemconfig'),    
    path('notification-settings/',notification_settings,name='notificationsettings'),


 
    # ====================================EMPLOYEE START======================================================

    path('checkinorout/<int:id>/', check_in_or_out, name='check_in_or_out'),
    path('profile/<int:id>/',my_profile,name='myprofile'), 
    path('documnets/',my_documents,name='mydocs'), 


    path('apply_leave/', apply_leave, name='applyleave'),
    path('leave_status/',employee_leave_status, name='employeeleavestatus'),

 


    # ====================================EMPLOYEE END======================================================



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
