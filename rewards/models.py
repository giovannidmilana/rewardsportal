from django.db import models
from rewards.models import *
from django.contrib.auth.models import User
# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    admin = models.BooleanField(default=False, null=False)
    creations = models.IntegerField(blank=True, null=True)
    
    
    
class Customer(models.Model):
     first = models.CharField(max_length=15)
     last = models.CharField(max_length=15)
     address = models.CharField(max_length=100)
     email = models.EmailField()
     phone = models.CharField(max_length=10)
     created = models.DateField(auto_now_add=True)
     balance = models.DecimalField(max_digits=6, decimal_places=2)
     #total_balance = models.DecimalField(max_digits=12, decimal_places=2)
     lastvisit = models.DateTimeField(auto_now=True)
     
     def get_model_fields(model):
         return model._meta.fields
     
     
class Transaction(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
class Card(models.Model):
    upc = models.CharField(max_length=30)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    
     
     


