from django.db import models
from django.contrib.auth.models import AbstractUser

# User model (normal car renters)
class CustomUser(AbstractUser):
    driving_license_no = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username


# Admin model (car rental company admin)
class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 

    def __str__(self):
        return self.username


# Car model
class Car(models.Model):
    brand = models.CharField(max_length=100)
    number_plate = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.brand} - {self.number_plate}"


# Borrowing model
class Borrowing(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    date_of_issue = models.DateField()
    date_of_return = models.DateField(null=True, blank=True)
    state_on_issue = models.TextField()
    state_on_return = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.car.number_plate}"