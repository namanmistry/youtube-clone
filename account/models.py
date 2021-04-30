from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Account(models.Model):
    firstName = models.CharField(max_length=20, null=False)
    lastName = models.CharField(max_length=30, null=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    mobileNumber = PhoneNumberField(blank=False, unique=True)
    password = models.CharField(max_length=20, null=False)


