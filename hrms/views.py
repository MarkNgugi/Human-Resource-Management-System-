from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import EmployeeCreationForm
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from accounts.models import *
from .forms import *
from .models import *
from datetime import date
from datetime import datetime, timedelta
from django.db.models import Count, F
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
    query = request.GET.get('q', '')  # Get the search query from the request
    employees = CustomUser.objects.filter(role__in=['employee', 'hr_manager'])
    
    if query:
        employees = employees.filter(
            models.Q(first_name__icontains=query) | models.Q(last_name__icontains=query)
        )
    
    context = {'employees': employees}
    return render(request, 'hrms/admin/employee-management/employee_profile.html', context)


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

    return render(request, 'hrms/admin/employee-management/add_emloyee.html', {'form': form})


def document_management(request):
    employees = CustomUser.objects.all()
    departments = Department.objects.exclude(name__iexact='admin')  # Exclude 'Admin' department
    selected_employee = None
    error_message = None

    # Handle search functionality
    if request.method == 'GET' and 'employee' in request.GET and 'department' in request.GET:
        employee_id = request.GET.get('employee', '')
        department_name = request.GET.get('department', '')

        # Filter the employee based on the selected employee and department
        try:
            if employee_id and department_name:
                selected_employee = CustomUser.objects.get(id=employee_id, department__name=department_name)
            else:
                error_message = "Please select both an employee and a department."
        except CustomUser.DoesNotExist:
            error_message = "User not found."

    context = {
        'employees': employees,
        'departments': departments,
        'selected_employee': selected_employee,
        'error_message': error_message,
    }
    return render(request, 'hrms/admin/employee-management/document_management.html', context)


def manage_documents(request, employee_id):    
    employee = get_object_or_404(CustomUser, id=employee_id)
    
    documents = Document.objects.filter(employee=employee)
    
    context = {
        'employee': employee,
        'documents': documents,
    }
    
    return render(request, 'hrms/admin/employee-management/manage_documents.html', context)




def add_document(request, employee_id):
    employee = get_object_or_404(CustomUser, id=employee_id)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.employee = employee  # Associate the document with the selected employee
            document.save()
            return redirect('manage_documents', employee_id=employee.id)  # Redirect to manage documents page
    else:
        form = DocumentForm()

    return render(request, 'hrms/admin/employee-management/add_document.html', {'form': form, 'employee': employee})


def offboarding(request):
    context={}
    return render(request,'hrms/admin/employee-management/offboarding.html',context)

# ============================EMPLOYEE MANAGEMENT END==============================

# ============================ATTENDANCE MANAGEMENT START============================



def departments(request):
    departments = Department.objects.exclude(name="ADMIN")
    if request.method == "POST":
        name = request.POST.get("name")
        work_start_time = request.POST.get("work_start_time")
        late_checkin_buffer = request.POST.get("late_checkin_buffer", 10)
        Department.objects.create(
            name=name,
            work_start_time=work_start_time,
            late_checkin_buffer=late_checkin_buffer,
        )
        return redirect("departments")
    context = {"departments": departments}
    return render(request, "hrms/admin/attendance-management/departments.html", context)

 
def dep_attendance(request, id):  
    department = Department.objects.get(id=id)  
    attendance_records = AttendanceRecord.objects.filter(employee__department=department)

    total_employees = department.customuser_set.count()
    present_today = attendance_records.filter(attendance_status='present').count()
    absent_today = attendance_records.filter(attendance_status='absent').count()
    late_entries = attendance_records.filter(is_late=True).count()
    on_leave_today = attendance_records.filter(attendance_status='on_leave').count()

    context = {
        'department': department,
        'attendance_records': attendance_records,
        'total_employees': total_employees,
        'present_today': present_today,
        'absent_today': absent_today,
        'late_entries': late_entries,
        'on_leave_today': on_leave_today,
    }
    return render(request, 'hrms/admin/attendance-management/department_attendance.html', context)


def attendance_reports(request):
    context={}
    return render(request,'hrms/admin/attendance-management/attendance-reports.html',context)

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
        employee_id = request.POST.get("employee")
        department = request.POST.get("department")
        job_role = request.POST.get("jobRole")        
        metrics = request.POST.getlist("metrics")
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")

        # Parse the date range
        try:
            start_date = datetime.strptime(date_from, "%Y-%m-%d")
            end_date = datetime.strptime(date_to, "%Y-%m-%d")
        except ValueError:
            # Handle invalid date format, possibly show an error
            start_date = end_date = None

        # Filter employees if selected
        selected_employee = None
        if employee_id:
            selected_employee = CustomUser.objects.get(id=employee_id)

        # Query data for the selected metrics
        report_data = {}

        # Employee Demographics
        if "demographics" in metrics and selected_employee:
            report_data["demographics"] = {
                "name": f"{selected_employee.first_name} {selected_employee.last_name}",
                "gender": selected_employee.gender,
                "department": selected_employee.department.name if selected_employee.department else "N/A",
                "position": selected_employee.position or "N/A",
                "start_date": selected_employee.start_date or "N/A",
            }

        # Attendance Data (filtered by date range)
        if "attendance" in metrics and selected_employee:
            attendance = AttendanceRecord.objects.filter(employee=selected_employee, date__range=[start_date, end_date])
            report_data["attendance"] = attendance

        # Leave Patterns (filtered by date range)
        if "leave" in metrics and selected_employee:
            leave_requests = LeaveRequest.objects.filter(employee=selected_employee, start_date__range=[start_date, end_date])
            report_data["leave"] = leave_requests

        # Turnover (filtered by department and exit date)
        if "turnover" in metrics and department:
            turnover = CustomUser.objects.filter(department__name=department, exit_date__range=[start_date, end_date]).count()
            report_data["turnover"] = turnover

        # Generate PDF
        html_template = "hrms/admin/reports/pdf_template.html"
        pdf_content = render(request, html_template, {
            "metrics": metrics,
            "report_data": report_data,
        }).content
        report_name = f"Report_{datetime.today().strftime('%Y-%m-%d')}"
        pdf_file_path = f"reports/{report_name}.pdf"
        HTML(string=pdf_content).write_pdf(pdf_file_path)

        # Save the generated report to the database
        report = GeneratedReport.objects.create(
            report_name=report_name,
            metrics_selected=metrics,
            filters_used={"employee": employee_id, "department": department, "job_role": job_role, "date_from": date_from, "date_to": date_to},
            pdf_file=pdf_file_path,
        )

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
    return render(request, 'hrms/employee/profile/profile.html', context)


# ============================MY PROFILE END===========================================

 

# ============================LEAVE MANAGEMENT START===========================================

@login_required
def employee_leave_status(request):
    leave_requests = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'hrms/employee/leave-management/leave-status.html', {'leave_requests': leave_requests})


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
    return render(request, 'hrms/employee/leave-management/apply-leave.html', {'form': form})

# ============================LEAVE MANAGEMENT END===========================================


# ================================================================================================
                                        # EMPLOYEE END
# ================================================================================================
