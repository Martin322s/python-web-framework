from django.db import models

class LaptopBrandChoices(models.TextChoices):
    ASUS = 'ASUS', 'Asus'
    ACER = 'ACER', 'Acer'
    APPLE = 'APPLE', 'Apple'
    LENOVO = 'LENOVO', 'Lenovo'
    DELL = 'DELL', 'Dell'

class OperatingSystemChoices(models.TextChoices):
    WINDOWS = 'WINDOWS', 'Windows'
    MAC_OS = 'MAC OS', 'Mac OS'
    LINUX = 'LINUX', 'Linux'
    CHROME_OS = 'CHROME OS', 'Chrome OS'