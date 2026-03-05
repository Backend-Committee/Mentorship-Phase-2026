from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, unique=True)
    national_id = models.CharField(max_length=14, unique=True) # it is a string contrary to int in ERD
    full_name = models.CharField()
    mobile_number = models.CharField(unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Person \"{self.full_name}\""

class Staff(models.Model):
    person = models.OneToOneField(Person, on_delete=models.SET_NULL, null=True, unique=True)
    
    def __str__(self):
        return f"Staff \"{self.person.full_name}\""
    
    @property
    def user(self):
        return self.person.user
        

class Customer(models.Model):
    person = models.OneToOneField(Person, on_delete=models.SET_NULL, null=True, unique=True)
    
    def __str__(self):
        return f"Customer \"{self.person.full_name}\""
    
    @property
    def user(self):
        return self.person.user


class AccountType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    interest_frequency = models.PositiveIntegerField(null=True, blank=True)
    interest_rate = models.PositiveIntegerField()
    maximum_daily_withdrawal = models.PositiveIntegerField(null=True, blank=True)
    maximum_monthly_withdrawal = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class Account(models.Model):
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    balance = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Account {self.id}"