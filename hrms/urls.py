from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('hr_manager_dashboard/', hr_manager_dashboard, name='hr_manager_dashboard'),
    path('employee_dashboard/', employee_dashboard, name='employee_dashboard'),

    path('employee-profile/',employee_profile,name = 'employeeprofile'),
    path('new-employee',new_employee,name='newemployee'),
    path('document_management',document_management,name='documentmanagement'),
    path('offboarding',offboarding,name='offboarding')
]
