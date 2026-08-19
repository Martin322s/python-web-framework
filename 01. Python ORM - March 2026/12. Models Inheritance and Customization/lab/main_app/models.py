from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from .fields import BooleanChoiceField

# Create your models here.
class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    @property
    def age(self):
        today = date.today()
        age = today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

        return age

class Mammal(Animal):
    fur_color = models.CharField(max_length=50)

class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)

class Reptile(Animal):
    scale_type = models.CharField(max_length=50)

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True

class ZooKeeper(Employee):
    class SpecialtyChoices(models.TextChoices):
        MAMMALS = 'Mammals'
        BIRDS = 'Birds'
        REPTILES = 'Reptiles'
        OTHERS = 'Others'

    specialty = models.CharField(max_length=50, choices=SpecialtyChoices.choices)
    managed_animals = models.ManyToManyField('Animal')

    def clean(self):
        if self.specialty not in ZooKeeper.SpecialtyChoices:
            raise ValidationError('Specialty must be a valid choice.')

class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()



class ZooDisplayAnimal(Animal):
    def display_info(self):
        return f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. It makes a noise like '{self.sound}'."

    def is_endangered(self):
        if self.species in ['Cross River Gorilla', 'Orangutan', 'Green Turtle']:
            return f"{self.species} is at risk."
        else:
            return f"{self.species} is not at risk."

    class Meta:
        proxy = True