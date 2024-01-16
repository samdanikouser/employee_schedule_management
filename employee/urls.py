from django.urls import path
from django.contrib.auth import views as auth
from employee_scheduler import settings
from . import views

urlpatterns = [
    path('login/', views.Login, name='login'),
    path('logout/', auth.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('register/', views.register, name='register'),
    path("employee_list/", views.emp_list, name="employee_list"),
    path("schedule_list/", views.schedule_list, name="schedule_list"),
    path("location_list/", views.location_list, name="location_list"),
    path("department_list/", views.department_list, name="department_list"),
    path("employee_schedule/", views.employee_schedule, name="employee_schedule"),
    path("add_employee/", views.add_employee, name="add_employee"),
    path("add_location/", views.add_location, name="add_location"),
    path("add_department/", views.add_department, name="add_department"),
    path("delete_emp/<int:emp_id>", views.delete_emp, name="del_emp"),
    path("update_emp/<int:emp_id>", views.update_emp, name="upd_emp"),
    path("delete_location/<str:location>", views.delete_location, name="del_loc"),
    path("update_location/<str:location>", views.update_location, name="upd_loc"),
    path("delete_department/<int:id>", views.delete_department, name="del_dep"),
    path("update_department/<int:id>", views.update_department, name="upd_Dep"),
    path("delete_schedule/<int:id>", views.delete_schedule, name="del_sche"),
    path("update_schedule/<int:id>", views.update_schedule, name="upd_sche"),
    path("report/", views.view_report, name="view_report"),
    path("generate_report/", views.generate_report, name="generate_report")
]
