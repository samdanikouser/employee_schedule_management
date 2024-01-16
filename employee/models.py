from django.db import models


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=200,unique=True,null=True)

    def __str__(self):
        return f"{self.department}"


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,null=True)
    date_of_birth = models.DateField("date of birth")

    def __str__(self):
        return f"{self.full_name}"


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=200,unique=True,null=True)

    def __str__(self):
        return f"{self.location}"


class Scheduler(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,null=True)
    from_date = models.DateField("shift from date")
    to_Date = models.DateField("shift to date")

    def __str__(self):
        return f"{self.employee}"
