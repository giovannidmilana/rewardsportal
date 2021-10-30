from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *




class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        
        
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('admin',)
        
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first', 'last', 'email', 'address', 'phone',)
        
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('total',)
        
class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('upc',)
