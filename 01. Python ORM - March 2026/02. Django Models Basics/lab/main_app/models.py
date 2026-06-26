import datetime
from string import digits

from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)

class Department(models.Model):
    class Cities(models.TextChoices):
        SF = ('SF', 'Sofia')
        PD = ('PD', 'Plovdiv')
        V = ('V', 'Varna')
        BS = ('BS', 'Burgas')

    code = models.CharField(
        max_length=4,
        unique=True,
        primary_key=True
    )
    name = models.CharField(max_length=50, unique=True)
    employees_count = models.PositiveIntegerField(default=1, verbose_name="Employees Count")
    location = models.CharField(max_length=20, choices=Cities.choices)
    last_edited_on = models.DateTimeField(auto_now=True, editable=False)

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    duration_in_days = models.PositiveIntegerField(verbose_name="Duration in Days")
    estimated_hours = models.FloatField(verbose_name="Estimated Hours")
    start_date = models.DateField(verbose_name="Start Date", default=datetime.date.today)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_edited_on = models.DateTimeField(auto_now_add=True, editable=False)

