from django.db import models

# Create your models here.
class Lecturer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    lecturer = models.ForeignKey(
    'Lecturer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    subjects = models.ManyToManyField('Subject', related_name='students')

class StudentEnrollment(models.Model):
    class GradeChoices(models.TextChoices):
        A = 'A'
        B = 'B'
        C = 'C'
        D = 'D'
        E = 'E'
        F = 'F'

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    enrollment_date = models.DateField(auto_now_add=True)

    grade = models.CharField(
        max_length=1,
        choices=GradeChoices.choices
    )

class LecturerProfile(models.Model):
    lecturer = models.OneToOneField(to='Lecturer', on_delete=models.CASCADE, to_field='id')
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    office_location = models.CharField(max_length=100, null=True, blank=True)