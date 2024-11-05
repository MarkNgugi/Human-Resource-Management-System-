from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user_role = request.user.role

    if user_role == 'admin':
        return redirect('admin_dashboard')
    elif user_role == 'hr_manager':
        return redirect('hr_manager_dashboard')
    elif user_role == 'employee':
        return redirect('employee_dashboard')
    else:
        return redirect('login')

# ================================================================================================
                                        # ADMIN START
# ================================================================================================

@login_required
def admin_dashboard(request):
    return render(request, 'hrms/admin/admin_dashboard.html')
 
# ============================EMPLOYEE MANAGEMENT START============================
def employee_profile(request):
    context = {}
    return render(request,'hrms/admin/employee-management/employee_profile.html',context)

def new_employee(request):
    context={}
    return render(request,'hrms/admin/employee-management/new_employee.html',context)

def document_management(request):
    context={}
    return render(request,'hrms/admin/employee-management/document_management.html',context)

def offboarding(request):
    context={}
    return render(request,'hrms/admin/employee-management/offboarding.html',context)

# ============================EMPLOYEE MANAGEMENT END==============================

# ============================HIRING AND ONBOARDING START============================

def job_posting(request):
    context={}
    return render(request,'hrms/admin/hiring-and-onboarding/jobposting.html',context)

def application_tracking(request):
    context={}
    return render(request,'hrms/admin/hiring-and-onboarding/applications-tracking.html',context)

def interview_scheduling(request):
    context={}
    return render(request,'hrms/admin/hiring-and-onboarding/interview-scheduling.html',context)

def onboarding_workflow(request):
    context={}
    return render(request,'hrms/admin/hiring-and-onboarding/onboarding.html',context)

# ============================HIRING AND ONBOARDING END==============================

# ============================ATTENDANCE AND LEAVE START============================

def time_tracking(request):
    context={}
    return render(request,'hrms/admin/attendance-and-leave/timetracking.html',context)

def attendance_reports_generation(request):
    context={}
    return render(request,'hrms/admin/attendance-and-leave/report-generation.html',context)

def leave_approval(request):
    context={}
    return render(request,'hrms/admin/attendance-and-leave/leave-approval.html',context)    

def leave_balance(request):
    context={}
    return render(request,'hrms/admin/attendance-and-leave/leave-balance.html',context)    


# ============================ATTENDANCE AND LEAVE END==============================

# ============================REPORTS START=========================================

def report_builder(request):
    context={}
    return render(request,'hrms/admin/reports/report-builder.html',context)  

def hr_dash(request):
    context={}
    return render(request,'hrms/admin/reports/hr-dashboard.html',context)      


# ============================REPORTS END===========================================

# ============================SETTINGS START=========================================

def system_config(request):
    context = {}
    return render(request,'hrms/admin/settings/system-config.html',context)

def roles_and_permissions(request):
    context={}
    return render(request,'hrms/admin/settings/roles-and-permissions.html',context)

def notification_settings(request):
    context = {}
    return render(request,'hrms/admin/settings/notification-settings.html',context)

# ============================SETTINGS END===========================================


# ================================================================================================
                                        # ADMIN END
# ================================================================================================




@login_required
def hr_manager_dashboard(request):
    return render(request, 'hrms/hr/hr_manager_dashboard.html')

@login_required
def employee_dashboard(request):
    return render(request, 'hrms/employee/employee_dashboard.html')

