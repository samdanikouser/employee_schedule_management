import csv
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.conf import settings
from django.core.mail import EmailMessage
from .forms import UserRegisterForm
from .models import Employee, Department, Location, Scheduler


# registration function
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'employee/register.html', {'form': form, 'title': 'register here'})


# Login function
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            form = auth.login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('/employee/employee_list/')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = auth.forms.AuthenticationForm()
    return render(request, 'employee/login.html', {'form': form, 'title': 'log in'})


# logout function
def logout_view(request):
    auth.logout(request)
    return redirect('login')


# employee list function
def emp_list(request):
    emps = Employee.objects.all()
    return render(request, "employee/employee_list.html", {'emps': emps})


# add employee function
def add_employee(request):
    department = Department.objects.all()
    if request.method == "POST":
        emp_name = request.POST.get("name")
        emp_department = request.POST.get("department")
        emp_dob = request.POST.get('date_of_birth')
        e = Employee()
        e.full_name = emp_name
        e.department = Department.objects.get(department=emp_department)
        e.date_of_birth = emp_dob
        e.save()
    return render(request, "employee/add_employee.html", {'department': department})


# employee delete function
def delete_emp(request, emp_id):
    emp = Employee.objects.get(pk=emp_id)
    emp.delete()
    return redirect("/employee/employee_list/")


# update employee
def update_emp(request, emp_id):
    emp = Employee.objects.get(pk=emp_id)
    department = Department.objects.all()
    if request.method == "POST":
        emp_name = request.POST.get("emp_name")
        emp_dob = request.POST.get("emp_dob")
        department = request.POST.get("department")
        e = Employee.objects.get(pk=emp_id)
        e.full_name = emp_name
        e.department = Department.objects.get(department=department)
        e.date_of_birth = emp_dob
        e.save()
        return redirect("/employee/employee_list/")
    return render(request, "employee/update_emp.html", {"emp": emp, "department": department})


# location list funcion
def location_list(request):
    locations = Location.objects.all()
    return render(request, "employee/location_list.html", {"locations": locations})


# add location function
def add_location(request):
    if request.method == "POST":
        location = request.POST.get("location")
        emp_location = Location()
        emp_location.location = location
        emp_location.save()
    return render(request, "employee/add_location.html", {})


# location delete function
def delete_location(request, location):
    emp = Location.objects.get(location=location)
    emp.delete()
    return redirect("/employee/location_list/")


# update location function
def update_location(request, location):
    loc = Location.objects.get(location=location)
    if request.method == "POST":
        print("hello")
        loca = request.POST.get("loc_name")
        location = Location.objects.get(location=location)
        location.location = loca
        location.save()
        return redirect("/employee/location_list/")
    return render(request, "employee/update_location.html", {
        'loc': loc
    })


# department list function
def department_list(request):
    departments = Department.objects.all()
    return render(request, "employee/department_list.html", {"departments": departments})


# department add function
def add_department(request):
    if request.method == "POST":
        print(request.POST)
        department = request.POST.get("department")
        emp_department = Department()
        emp_department.department = department
        emp_department.save()
    return render(request, "employee/add_department.html", {})


# delete department function
def delete_department(request, id):
    emp = Department.objects.get(pk=id)
    emp.delete()
    return redirect("/employee/department_list/")


# update department function
def update_department(request, id):
    dep = Department.objects.get(pk=id)
    if request.method == "POST":
        deprt = request.POST.get("department_name")
        department = Department.objects.get(pk=id)
        department.department = deprt
        department.save()
        return redirect("/employee/department_list/")
    return render(request, "employee/update_department.html", {
        'dep': dep
    })


# scheduled list function
def schedule_list(request):
    schedule = Scheduler.objects.all()
    return render(request, "employee/schedule_list.html", {"schedule": schedule})


# employee shift schedule function
def employee_schedule(request):
    employees_scheduler = Employee.objects.all()
    location = Location.objects.all()
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        location = request.POST.get("location")
        employee_list = request.POST.getlist("checks")
        for employee_id in employee_list:
            scheduler = Scheduler()
            scheduler.location = Location.objects.get(location=location)
            scheduler.from_date = from_date
            scheduler.to_Date = to_date
            scheduler.employee = Employee.objects.get(employee_id=employee_id)
            scheduler.save()
            return redirect("/employee/employee_schedule/")
    return render(request, "employee/employee_schedule.html",
                  {'employees_scheduler': employees_scheduler, 'location': location})


# schedule delete function
def delete_schedule(request, id):
    emp_schedule = Scheduler.objects.get(pk=id)
    emp_schedule.delete()
    return redirect("/employee/schedule_list/")


# schedule update function
def update_schedule(request, id):
    scheduler = Scheduler.objects.get(pk=id)
    location = Location.objects.all()
    if request.method == "POST":
        location = request.POST.get("location")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        scheduler = Scheduler.objects.get(pk=id)
        scheduler.location = Location.objects.get(location=location)
        scheduler.to_Date = to_date
        scheduler.from_date = from_date
        scheduler.save()
        return redirect("/employee/schedule_list/")
    return render(request, "employee/scheduler_update.html", {
        'scheduler': scheduler, "location": location
    })


# report view fuction
def view_report(request):
    show_table = False
    if request.method == "POST":
        show_table = True
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        schedule_date_list = Scheduler.objects.filter(from_date=from_date, to_Date=to_date)
        return render(request, "employee/report.html", {
            'scheduler': schedule_date_list, "show_table": show_table, "from_date": from_date, "to_date": to_date
        })
    return render(request, "employee/report.html", {"show_table": show_table})


# generate report by mail or csv
def generate_report(request):
    show_table = False
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        if "report_generate" in request.POST:
            schedule_date_list = Scheduler.objects.filter(from_date=from_date, to_Date=to_date)
            today = date.today()
            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="Employee_schedule"' + str(today) + '.csv'},
            )
            writer = csv.writer(response)
            writer.writerow(["Employee Id", "Name", "Department", "Location", "From Date", "To Date"])
            for schedule_id in schedule_date_list:
                report_schedule_list = Scheduler.objects.get(pk=schedule_id.id)
                writer.writerow([report_schedule_list.id, report_schedule_list.employee.full_name,
                                 report_schedule_list.employee.department.department,
                                 report_schedule_list.location.location, report_schedule_list.from_date,
                                 report_schedule_list.to_Date])
            return response
        if "email_popup" in request.POST:
            return render(request, "employee/add_email.html", {"from_date": from_date, "to_date": to_date})
        if "send_email" in request.POST:
            schedule_date_list = Scheduler.objects.filter(from_date=from_date, to_Date=to_date)
            recip_email = request.POST.get("email")
            today = date.today()
            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="Employee_schedule"' + str(today) + '.csv'},
            )
            writer = csv.writer(response)
            writer.writerow(["Employee Id", "Name", "Department", "Location", "From Date", "To Date"])
            for schedule_id in schedule_date_list:
                report_schedule_list = Scheduler.objects.get(pk=schedule_id.id)
                writer.writerow([report_schedule_list.id, report_schedule_list.employee.full_name,
                                 report_schedule_list.employee.department.department,
                                 report_schedule_list.location.location, report_schedule_list.from_date,
                                 report_schedule_list.to_Date])
            subject = 'Employees Schedule Report'
            message = 'Report for Employee Schedule for the mentioned date in Report.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [recip_email, ]
            mail = EmailMessage(subject, message, email_from, recipient_list)
            mail.attach('employee_schedule.csv', response.getvalue(), 'text/csv')
            mail.send()
    return render(request, "employee/report.html", {"show_table": show_table})


# send auto mail
def cron_job_function(request):
    if "send_email" in request.POST:
        today = date.today()
        schedule_date_list = Scheduler.objects.filter(from_date=today)
        recip_email = request.POST.get("email")
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="Employee_schedule"' + str(today) + '.csv'},
        )
        writer = csv.writer(response)
        writer.writerow(["Employee Id", "Name", "Department", "Location", "From Date", "To Date"])
        for schedule_id in schedule_date_list:
            report_schedule_list = Scheduler.objects.get(pk=schedule_id.id)
            writer.writerow([report_schedule_list.id, report_schedule_list.employee.full_name,
                             report_schedule_list.employee.department.department,
                             report_schedule_list.location.location, report_schedule_list.from_date,
                             report_schedule_list.to_Date])
        subject = 'Employees Schedule Report'
        message = 'Report for Employee Schedule for the mentioned date in Report.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [recip_email, ]
        mail = EmailMessage(subject, message, email_from, recipient_list)
        mail.attach('employee_schedule.csv', response.getvalue(), 'text/csv')
        mail.send()
