from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import EmployeeCreationForm
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from accounts.models import *
from .forms import LeaveRequestForm
from .models import *
from datetime import date
from weasyprint import HTML
import json

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
    employees = CustomUser.objects.filter(role__in=['employee','hr_manager'])
    context = {'employees':employees}
    return render(request,'hrms/admin/employee-management/employee_profile.html',context)

@login_required
def add_employee(request):
    if request.user.role != 'admin':
        return redirect('dashboard')

    form = EmployeeCreationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():        
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        user.save()

        return redirect('employeeprofile')

    return render(request, '/home/smilex/Documents/PROJECTS/MIKE/HRMS/HRMS/hrms/templates/hrms/admin/employee-management/add_emloyee.html', {'form': form})


def document_management(request):
    context={}
    return render(request,'hrms/admin/employee-management/document_management.html',context)

def offboarding(request):
    context={}
    return render(request,'hrms/admin/employee-management/offboarding.html',context)

# ============================EMPLOYEE MANAGEMENT END==============================

# ============================ATTENDANCE MANAGEMENT START============================

def departments(request):
    departments = Department.objects.exclude(name="ADMIN")
    context = {'departments':departments}
    return render(request,'hrms/admin/attendance-management/departments.html',context)
 
def dep_attendance(requestdep,id):  
    department = Department.objects.get(id=id)  
    attendance_records = AttendanceRecord.objects.filter(employee__department=department)

    context = {
        'department':department,
        'attendance_records':attendance_records
        }
    return render(requestdep, '/home/smilex/Documents/PROJECTS/MIKE/HRMS/HRMS/hrms/templates/hrms/admin/attendance-management/department_attendance.html',context)

def attendance_reports(request):
    context={}
    return render(request,'/home/smilex/Documents/PROJECTS/MIKE/HRMS/HRMS/hrms/templates/hrms/admin/attendance-management/attendance-reports.html',context)

# ============================ATTENDANCE MANAGEMENT END==============================

# ============================ATTENDANCE AND LEAVE START============================

def time_tracking(request):
    context={}
    return render(request,'hrms/admin/attendance-and-leave/timetracking.html',context)

def attendance_reports_generation(request):
    context={}
    return render(request,'hrms/admin/attendance-and-leave/report-generation.html',context)

@login_required
def leave_requests(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'hrms/admin/leave-approvals/leave_requests.html', {'leave_requests': leave_requests})

@login_required
def update_leave_status(request, leave_id, status):
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    if status in ['APPROVED', 'DECLINED']:
        leave_request.status = status
        leave_request.save()
    return redirect('reviewleaves')

def leave_balance(request):
    context={}
    return render(request,'/home/smilex/Documents/PROJECTS/MIKE/HRMS/HRMS/hrms/templates/hrms/admin/leave-approvals/leave-balance.html',context)    
 

# ============================ATTENDANCE AND LEAVE END==============================

# ============================REPORTS START=========================================


def report_builder(request):
    employees = CustomUser.objects.all()

    if request.method == "POST":
        # Gather form data
        employee = request.POST.get("employee")
        department = request.POST.get("department")
        job_role = request.POST.get("jobRole")
        date_range = request.POST.get("date_range")
        metrics = request.POST.getlist("metrics")

        # Generate Report Data
        report_name = f"Report_{date.today().strftime('%Y-%m-%d')}"
        filters_used = {
            "employee": employee,
            "department": department,
            "job_role": job_role,
            "date_range": date_range,
        }
        report = GeneratedReport.objects.create(
            report_name=report_name,
            metrics_selected=metrics,
            filters_used=filters_used,
        )

        # Generate PDF
        html_template = "hrms/admin/reports/pdf_template.html"
        pdf_content = render(request, html_template, {
            "metrics": metrics,
            "filters": filters_used,
        }).content
        pdf_file_path = f"reports/{report_name}.pdf"
        HTML(string=pdf_content).write_pdf(pdf_file_path)
        report.pdf_file = pdf_file_path
        report.save()

        return redirect("report_list")  

    return render(request, 'hrms/admin/reports/report-builder.html', {'employees': employees})

def report_list(request):
    reports = GeneratedReport.objects.all()
    return render(request, 'hrms/admin/reports/report-list.html', {'reports': reports})


def export_report_pdf(request, report_id):
    try:
        report = GeneratedReport.objects.get(id=report_id)
        with open(report.pdf_file.path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{report.report_name}.pdf"'
            return response
    except GeneratedReport.DoesNotExist:
        return HttpResponse("Report not found", status=404)

 

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



# ================================================================================================
                                        # HR START
# ================================================================================================

@login_required
def hr_manager_dashboard(request):
    return render(request, 'hrms/hr/hr_manager_dashboard.html')


# ================================================================================================
                                        # HR END
# ================================================================================================


# ================================================================================================
                                        # EMPLOYEE START
# ================================================================================================

@login_required
def employee_dashboard(request):
    return render(request, 'hrms/employee/employee_dashboard.html')

# ============================MY PROFILE START===========================================
 
def my_profile(request, id):
    employee_details = get_object_or_404(CustomUser, id=id)
    context = {'employee_details': employee_details}
    return render(request, '/home/smilex/Documents/PROJECTS/MIKE/HRMS/HRMS/hrms/templates/hrms/employee/profile/profile.html', context)

# ============================MY PROFILE END===========================================



# ============================LEAVE MANAGEMENT START===========================================

@login_required
def employee_leave_status(request):
    leave_requests = LeaveRequest.objects.filter(employee=request.user)
    return render(request, '/home/smilex/Documents/PROJECTS/MIKE/HRMS/HRMS/hrms/templates/hrms/employee/leave-management/leave-status.html', {'leave_requests': leave_requests})


@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            return redirect('employeeleavestatus')  
    else:
        form = LeaveRequestForm()
    return render(request, '/home/smilex/Documents/PROJECTS/MIKE/HRMS/HRMS/hrms/templates/hrms/employee/leave-management/apply-leave.html', {'form': form})

# ============================LEAVE MANAGEMENT END===========================================


# ================================================================================================
                                        # EMPLOYEE END
# ================================================================================================