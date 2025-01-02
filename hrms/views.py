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

from .models import Department, AttendanceRecord

def dep_attendance(request, id):  
    department = Department.objects.get(id=id)  # Get the department
    attendance_records = AttendanceRecord.objects.filter(employee__department=department)  # Get attendance records for the department

    context = {
        'department': department,
        'attendance_records': attendance_records,  # Pass only the relevant data
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


from datetime import datetime
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from weasyprint import HTML  # Ensure weasyprint is installed for PDF generation
from .models import CustomUser, Department, AttendanceRecord, LeaveRequest, GeneratedReport

def report_builder(request):
    employees = CustomUser.objects.filter(is_active=True).exclude(first_name="", last_name="")
    departments = Department.objects.exclude(name="ADMIN")


    if request.method == "POST":
        # Gather form data
        employee_id = request.POST.get("employee")
        department_name = request.POST.get("department")
        metrics = request.POST.getlist("metrics")
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")

        # Validate employee and department selection
        if not employee_id:
            messages.error(request, "Please select an employee.")
            return redirect("reportbuilder")

        if not department_name:
            messages.error(request, "Please select a department.")
            return redirect("reportbuilder")

        # Parse the date range
        try:
            start_date = datetime.strptime(date_from, "%Y-%m-%d")
            end_date = datetime.strptime(date_to, "%Y-%m-%d")
        except ValueError:
            messages.error(request, "Invalid date range.")
            return redirect("reportbuilder")

        # Validate employee and department relationship
        try:
            selected_employee = CustomUser.objects.get(id=employee_id)
        except CustomUser.DoesNotExist:
            messages.error(request, "Selected employee does not exist.")
            return redirect("reportbuilder")

        selected_department = Department.objects.filter(name=department_name).first()
        if not selected_department:
            messages.error(request, "Selected department does not exist.")
            return redirect("reportbuilder")

        if selected_employee.department != selected_department:
            messages.error(
                request, f"{selected_employee.first_name} does not belong to the {selected_department.name} department."
            )
            return redirect("reportbuilder")

        # Prepare report data
        report_data = {"username": selected_employee.username}

        if "basic_info" in metrics:
            report_data["basic_info"] = {
                "name": f"{selected_employee.first_name} {selected_employee.last_name}",
                "gender": selected_employee.gender,
                "department": selected_employee.department.name if selected_employee.department else "N/A",
                "position": selected_employee.position or "N/A",
                "start_date": selected_employee.start_date or "N/A",
                "exit_date": selected_employee.exit_date or "N/A",
                "reason_for_leaving": selected_employee.reason_for_leaving or "N/A",
            }

        if "attendance_overview" in metrics:
            attendance = AttendanceRecord.objects.filter(
                employee=selected_employee, date__range=[start_date, end_date]
            )
            report_data["attendance_overview"] = {
                "total_days_worked": attendance.count(),
                "average_check_in_time": calculate_average_check_in(attendance),
                "average_check_out_time": calculate_average_check_out(attendance),
            }

        if "leave_request" in metrics:
            leave_requests = LeaveRequest.objects.filter(
                employee=selected_employee, start_date__range=[start_date, end_date]
            )
            report_data["leave_request"] = {
                "total_leave_requests": leave_requests.count(),
                "approved_leaves": leave_requests.filter(status="APPROVED").count(),
                "pending_leaves": leave_requests.filter(status="PENDING").count(),
                "declined_leaves": leave_requests.filter(status="DECLINED").count(),
                "leave_days_requested": sum([leave.days_requested for leave in leave_requests]),
                "leave_days_approved": sum([leave.days_approved for leave in leave_requests if leave.days_approved]),
            }

        # Generate PDF
        html_content = render_to_string("hrms/admin/reports/pdf_template.html", {
            "metrics": metrics,
            "report_data": report_data,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        })

        report_name = f"Report_{datetime.today().strftime('%Y-%m-%d')}"
        pdf_file_path = f"reports/{report_name}.pdf"
        HTML(string=html_content).write_pdf(pdf_file_path)

        # Save generated report
        GeneratedReport.objects.create(
            employee=selected_employee,
            report_name=report_name,
            metrics_selected=metrics,
            filters_used={"employee": employee_id, "date_from": date_from, "date_to": date_to},
            pdf_file=pdf_file_path,
        )

        return redirect("report_list")

    return render(request, 'hrms/admin/reports/report-builder.html', {
        'employees': employees,
        'departments': departments,
    })





# Helper functions for attendance calculations
def calculate_average_check_in(attendance_records):
    """Calculate average check-in time from AttendanceRecord."""
    total_check_in_time = sum([record.check_in_time.hour + record.check_in_time.minute / 60 for record in attendance_records if record.check_in_time])
    return total_check_in_time / len(attendance_records) if attendance_records else 0

def calculate_average_check_out(attendance_records):
    """Calculate average check-out time from AttendanceRecord."""
    total_check_out_time = sum([record.check_out_time.hour + record.check_out_time.minute / 60 for record in attendance_records if record.check_out_time])
    return total_check_out_time / len(attendance_records) if attendance_records else 0





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


from django.utils import timezone
from django.shortcuts import render, redirect
from datetime import timedelta
from .models import AttendanceRecord

def check_in_or_out(request, id):
    # Ensure the user is logged in and is checking in or out for themselves
    if request.user.id != id:
        return redirect('home')  # Redirect if the user tries to access another user's page

    now = timezone.now()

    # Fetch today's attendance record for the user
    today = now.date()
    attendance_record, created = AttendanceRecord.objects.get_or_create(employee=request.user, date=today)

    # Time interval restriction for testing (5 seconds)
    interval_limit = timedelta(hours=3)

    message = None
    show_check_in = False
    show_check_out = False

    # Reset logic: Check if 5 seconds have passed since the last check-out
    if attendance_record.check_out_time:
        time_since_last_action = now - attendance_record.check_out_time
        if time_since_last_action >= interval_limit:
            attendance_record.check_in_time = None
            attendance_record.check_out_time = None
            attendance_record.save()
            show_check_in = True  # Enable check-in button after reset
        else:
            show_check_in = False  # Prevent check-in before interval
            show_check_out = False  # Prevent check-out
    else:
        # Determine button visibility
        if not attendance_record.check_in_time and not attendance_record.check_out_time:
            show_check_in = True  # Show check-in button
        elif attendance_record.check_in_time and not attendance_record.check_out_time:
            show_check_out = True  # Show check-out button

    # Handle POST requests for check-in or check-out
    if request.method == 'POST':
        action = request.POST.get('action')

        # Handle check-in
        if action == 'check_in':
            if not attendance_record.check_in_time:
                attendance_record.check_in_time = now
                attendance_record.save()
                message = "Checked in successfully."
                show_check_out = True  # Show check-out button
                show_check_in = False  # Hide check-in button
            else:
                message = "Invalid action: You are already checked in."

        # Handle check-out
        elif action == 'check_out':
            if attendance_record.check_in_time and not attendance_record.check_out_time:
                attendance_record.check_out_time = now
                attendance_record.save()
                message = "Checked out successfully."
                show_check_out = False  # Hide check-out button
                show_check_in = False  # Prevent immediate check-in
           

    # Context for the template
    context = {
        'attendance_record': attendance_record,
        'employee_details': request.user,
        'message': message,
        'show_check_in': show_check_in,
        'show_check_out': show_check_out,
    }
    return render(request, 'hrms/employee/checkin&out/check_in_or_out.html', context)










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
