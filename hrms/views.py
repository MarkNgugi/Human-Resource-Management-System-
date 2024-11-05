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

@login_required
def admin_dashboard(request):
    return render(request, 'hrms/admin/admin_dashboard.html')

@login_required
def hr_manager_dashboard(request):
    return render(request, 'hrms/hr/hr_manager_dashboard.html')

@login_required
def employee_dashboard(request):
    return render(request, 'hrms/employee/employee_dashboard.html')
