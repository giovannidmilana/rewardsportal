from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import (
    LoginView,
)
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from .forms import *
from .models import *
from django.views.generic import ListView
from django.db.models import Q

from messaging.views import *


from django.views import View

#import time
#from datetime import datetime, timedelta
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        employee = get_object_or_404(Employee, user_id = request.user.id)
        customer_form = CustomerForm()
        context = {'user' : request.user, 'customer_form' : customer_form, 'employee' : employee}
        return render(request, 'rewards/index1.html', context)
    else:
        
        employee = get_object_or_404(Employee, user_id = request.user.id)
        customer_form = CustomerForm()
        context = {'user' : request.user, 'customer_form' : customer_form, 'employee' : employee}
        return render(request, 'rewards/index1.html', context)
        
        
        #return HttpResponseRedirect(reverse('rewards:login'))
        
class login_view(LoginView):
    template_name = 'rewards/login1.html'
    
    
def logout_view(request):
    """Log the user out."""
    logout(request)
    return HttpResponseRedirect(reverse('rewards:index'))
        
        
def register(request):
    """register new user"""
    '''
    if admin_check(request) == True:
        pass
    else:
        return HttpResponseRedirect(reverse('rewards:index'))
    '''
    if request.method != 'POST':
        user_form = UserForm()
        employee_form = EmployeeForm()
    else:
        user_form = UserForm(data=request.POST)
        employee_form = EmployeeForm(data=request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            new_employee = employee_form.save(commit=False)
            new_employee.user = new_user
            new_employee.save()
            authenticated_user = authenticate(username=new_user.username,password=request.POST['password1'])
            login(request, authenticated_user)            
            return HttpResponseRedirect(reverse('rewards:index'))
            
    context = {'user_form': user_form, 'employee_form': employee_form}
    return render(request, 'rewards/register.html', context)
    
    
    
def customer_create(request):
    """register new user"""
    employee = get_object_or_404(Employee, user_id = request.user.id)
    if request.method != 'POST':
        customer_form = CustomerForm()
    else:
        #print('success')
        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            new_customer = customer_form.save(commit=False)
            new_customer.balance = float(0.0)   
            new_customer.save()
            #print('success')
            opt_in(new_customer.id)
            messaging_customer_creation(new_customer.id)
            return HttpResponseRedirect(reverse('rewards:index'))
            
    context = {'customer_form': customer_form, 'employee' : employee}
    return render(request, 'rewards/customer_creation.html', context)
    

#    Customer search
class SearchResultsView(ListView):
    model = Customer
    template_name = 'rewards/search_results.html'
    
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Customer.objects.filter(Q(first__icontains=query) | Q(last__icontains=query) | Q(phone__icontains=query) | Q(email__icontains=query) | Q(address__icontains=query))
        if ' ' in query:
            object_list = Customer.objects.filter(Q(first__icontains=query) | Q(last__icontains=query) | Q(phone__icontains=query) | Q(address__icontains=query) | Q(email__icontains=query) | Q(first__icontains=query.split()[0]) | Q(last__icontains=query.split()[1]))
        print(len(object_list))
        
        return object_list
        
    def get_context_data(self, **kwargs):
        employee = get_object_or_404(Employee, user_id = self.request.user.id)
        context = super().get_context_data(**kwargs)
        context['employee'] = employee
        return context

    
    
def create_transaction(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    
    if request.method != 'POST':
        transaction_form = TransactionForm()
    else:
        transaction_form = TransactionForm(data=request.POST)
        if transaction_form.is_valid():
            new_transaction = transaction_form.save(commit=False)
            new_transaction.customer = customer   
            new_transaction.user = request.user
            new_transaction.save()
            messaging_customer_trans(new_transaction.total, customer.id)
            ### DEFINE Points ECONOMY HERE
            customer.balance += new_transaction.total
            customer.save()
            #messaging_customer_trans(new_transaction.id, customer.id)
            #return HttpResponseRedirect(reverse('rewards:index'))
            return HttpResponseRedirect(reverse('rewards:customer_edit', args=(customer_id,)))
            
    context = {'transaction_form': transaction_form}
    return render(request, 'rewards/transaction_creation.html', context)
    
    
    
#user profile
def employee_edit(request):
    """register new user"""
    employee = get_object_or_404(Employee, user_id = request.user.id)
    uobj = get_object_or_404(User, id = request.user.id)
    if request.method != 'POST':
        user_form = UserForm(instance = uobj)
        #employee_form = EmployeeForm(instance = eobj)
        #get_object_or_404(Employee, user_id = request.user)
        #employee_form = EmployeeForm(Employee.objects.get(id=request.user.id))
    else:
        user_form = UserForm(instance = uobj, data=request.POST)
        #employee_form = EmployeeForm(data=request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            #new_employee = employee_form.save(commit=False)
            #new_employee.user = new_user
            #new_employee.save()
            authenticated_user = authenticate(username=new_user.username,password=request.POST['password1'])
            login(request, authenticated_user)            
            return HttpResponseRedirect(reverse('rewards:index'))
            
    context = {'user_form': user_form, 'employee' : employee}
    return render(request, 'rewards/profile_edit.html', context)
    
    
def m_opt_in(request, customer_id):
    opt_in(customer_id)
    return HttpResponseRedirect(reverse('rewards:customer_edit', args=(customer_id,)))
    
    
    
def customer_edit(request, customer_id):
    """register new user"""
    employee = get_object_or_404(Employee, user_id = request.user.id)
    promos = Promo.objects.filter(customer = customer_id)
    #promos = Promo.objects.all()
    transactions = Transaction.objects.filter(customer = customer_id)
    card_form = CardForm()
    transaction_form = TransactionForm()
    obj = get_object_or_404(Customer, id = customer_id)
    
    if request.method != 'POST':
        customer_form = CustomerForm(instance = obj)
    else:
        customer_form = CustomerForm(instance = obj, data=request.POST)
        if customer_form.is_valid():
            new_customer = customer_form.save()   
            return HttpResponseRedirect(reverse('rewards:customer_edit', args=(customer_id,)))
            
    context = {'employee' : employee, 'customer_form': customer_form, 'transaction_form' : transaction_form, 'customer' : obj, 'transactions' : transactions, 'card_form' : card_form, 'promos' : promos}
    return render(request, 'rewards/customer_edit.html', context)
    
#   Employee search  
class SearchResultsViewE(ListView):
    model = User
    template_name = 'rewards/search_results_E.html'
    
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = []
        if query != None:
            object_list = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query) | Q(username__icontains=query))
            if ' ' in query:
                object_list = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query) | Q(username__icontains=query) | Q(first_name__icontains=query.split()[0]) | Q(last_name__icontains=query.split()[1]))
        return object_list

#card/upc search
class SearchResultsViewC(ListView):
    model = Card
    template_name = 'rewards/search_results.html'
    
    def get_queryset(self): # new
        c_list = []
        query = self.request.GET.get('q')
        if query != None:
            object_list = Card.objects.filter(Q(upc__icontains=query))
            eobj = get_object_or_404(Customer, id = object_list[0].customer.id)
            c_list.append(eobj)
        return c_list
        
    def get_context_data(self, **kwargs):
        employee = get_object_or_404(Employee, user_id = self.request.user.id)
        context = super().get_context_data(**kwargs)
        context['employee'] = employee
        return context
        
        
        
def employee_edit2(request, user_id):
    """register new user"""
    '''
    if admin_check(request) == True:
        pass
    else:
        return HttpResponseRedirect(reverse('rewards:index'))
    '''
    eobj = get_object_or_404(Employee, user_id = user_id)
    uobj = get_object_or_404(User, id = user_id)
    if request.method != 'POST':
        user_form = UserForm(instance = uobj)
        employee_form = EmployeeForm(instance = eobj)
        #get_object_or_404(Employee, user_id = request.user)
        #employee_form = EmployeeForm(Employee.objects.get(id=request.user.id))
    else:
        user_form = UserForm(instance = uobj, data=request.POST)
        employee_form = EmployeeForm(instance = eobj, data=request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            new_employee = employee_form.save(commit=False)
            new_employee.user = new_user
            new_employee.save()
            authenticated_user = authenticate(username=new_user.username,password=request.POST['password1'])
            login(request, authenticated_user)            
            return HttpResponseRedirect(reverse('rewards:index'))
            
    context = {'user_form': user_form, 'employee_form': employee_form}
    return render(request, 'rewards/employee_edit.html', context)
    
    
def upc_create(request, customer_id):
    """register new user"""
    customer = get_object_or_404(Customer, id = customer_id)
    if request.method != 'POST':
        card_form = CardForm()
    else:
        card_form = CardForm(data=request.POST)
        if card_form.is_valid():
            new_card = card_form.save(commit=False)
            new_card.customer = customer  
            new_card.save()
            #return HttpResponseRedirect(reverse('rewards:index'))
            return HttpResponseRedirect(reverse('rewards:customer_edit', args=(customer_id,)))
            
    context = {'card_form': card_form}
    return render(request, 'rewards/card_creation.html', context)
    

def customer_delete(request, customer_id):
    
    if admin_check(request) == True:
        pass
    else:
        return HttpResponseRedirect(reverse('rewards:index'))

    customer = get_object_or_404(Customer, id = customer_id)
    
    
    mcustomer = get_object_or_404(MCustomer, customer = customer_id)
    
    
    trans = Transaction.objects.filter(customer = customer.id)
    
    cards = Card.objects.filter(customer = customer.id)
    
    for tran in trans:
        trans.delete()
    for card in cards:
        card.delete()
    customer.delete()
    mcustomer.delete()
    
    return HttpResponseRedirect(reverse('rewards:index'))
    
def employee_delete(request, user_id):
    '''
    if admin_check(request) == True:
        pass
    else:
        return HttpResponseRedirect(reverse('rewards:index'))
    '''
    try:
        eobj = get_object_or_404(Employee, user_id = user_id)
        pass
        
    except Exception as e:
        pass

    try:
        uobj = get_object_or_404(User, id = user_id)
    except Exception as e:
        pass

    try:
        eobj.delete()
        pass
    except Exception as e:
        pass

    try:
        uobj.delete()
    except Exception as e:
        pass


    '''  
    eobj = get_object_or_404(Employee, user_id = user_id)
    uobj = get_object_or_404(User, id = user_id)
    eobj.delete()
    uobj.delete()
    '''
    return HttpResponseRedirect(reverse('rewards:index'))




def promo_redeem(request, promo_id, customer_id):
    """register new user"""
    #eobj = get_object_or_404(Employee, user_id = request.user.id)
    obj = get_object_or_404(Promo, id = promo_id)
    obj.delete()
    return HttpResponseRedirect(reverse('rewards:customer_edit', args=(customer_id,)))



        
def admin_check(request):
    eobj = get_object_or_404(Employee, user_id = request.user.id)
    if eobj.admin == True:
        return True
    else:
        #return HttpResponseRedirect(reverse('rewards:index'))
        return False
        

def create_c_test():
    for i in range(0,40):
        c = Customer.objects.create(first = 'test', last = 'tester', email = 'gtechmedia840@gmail.com', address = 'hhhhhhhhhhhhhhhh', phone = '4703570000', balance = 0)
        messaging_customer_creation(c.id)





#create_c_test()
