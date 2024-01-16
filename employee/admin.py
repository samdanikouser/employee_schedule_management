from django.contrib import admin
from .models import Employee, Department, Location, Scheduler

# Register your models here.
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Scheduler)

