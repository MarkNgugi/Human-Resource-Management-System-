from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user_role = request.user.role

    if user_role == 'admin':
        return render(request, 'hrms/admin_dashboard.html')
    elif user_role == 'hr_manager':
        return render(request, 'hrms/hr_manager_dashboard.html')
    elif user_role == 'employee':
        return render(request, 'hrms/employee_dashboard.html')
    else:
        return redirect('login')
