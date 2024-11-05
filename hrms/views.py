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
    pass

def application_tracking(request):
    pass

def interview_scheduling(request):
    pass

def onboarding_workflow(request):
    pass
# ============================HIRING AND ONBOARDING END==============================

# ============================ATTENDANCE AND LEAVE START============================

def time_tracking(request):
    pass

# ============================ATTENDANCE AND LEAVE END==============================

# ============================REPORTS START=========================================

def report_builder(request):
    pass

# ============================REPORTS END===========================================

# ============================SETTINGS START=========================================

def system_config(request):
    pass

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

