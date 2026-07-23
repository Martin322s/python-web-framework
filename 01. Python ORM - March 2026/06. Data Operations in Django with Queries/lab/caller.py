import os
import django
from datetime import datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student
# Run and print your queries

def add_students():
    student1 = Student(
        student_id="FC5204",
        first_name="John",
        last_name="Doe",
        birth_date=datetime.strptime("15/05/1995", "%d/%m/%Y").date(),
        email="john.doe@university.com"
    )
    student1.save()

    student2 = Student(
        student_id="FE0054",
        first_name="Jane",
        last_name="Smith",
        birth_date=None,
        email="jane.smith@university.com"
    )
    student2.save()

    Student.objects.create(
        student_id="FH2014",
        first_name="Alice",
        last_name="Johnson",
        birth_date=datetime.strptime("10/02/1998", "%d/%m/%Y").date(),
        email="alice.johnson@university.com"
    )

    Student.objects.create(
        student_id="FH2015",
        first_name="Bob",
        last_name="Wilson",
        birth_date=datetime.strptime("25/11/1996", "%d/%m/%Y").date(),
        email="bob.wilson@university.com"
    )

def get_students_info():
    students = Student.objects.all()
    result = [f"Student №{student.student_id}: {student.first_name} {student.last_name}; Email: {student.email}" for student in students]

    return "\n".join(result)

def update_students_emails():
    students = Student.objects.all()

    for student in students:
        student.email = student.email.replace("@university.com", "@uni-students.com")
        student.save()

def truncate_students():
    students = Student.objects.all()
    for student in students:
        student.delete()
