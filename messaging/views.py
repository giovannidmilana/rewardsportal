from django.shortcuts import render

import os
import sys

from azure.servicebus import ServiceBusClient, ServiceBusMessage

from rewards.forms import *
from rewards.models import *
from .forms import *
from .models import *
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect, Http404, HttpResponse, FileResponse
from django.urls import reverse

import os
from azure.communication.sms import SmsClient

import random

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, FileContent, FileName, FileType, Disposition, ContentId)
from sendgrid.helpers.mail import Attachment as FAttachment
import base64

import csv, io

#import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from pandas import DataFrame, Timestamp


#update datetimefield with datetime.datetime.now()



# Create your views here.            
def messaging_customer_creation(customer_id):
    obj = get_object_or_404(Customer, id = customer_id)
    message_customer = MCustomer.objects.create(customer = obj, total_balance = obj.balance, messages_period = 1, last_marketed = timezone.now())
    
def messaging_customer_trans(transaction_total, customer_id):
    #customer = get_object_or_404(Customer, id = customer_id)
    #transaction = get_object_or_404(Transaction, id = transaction_id)
    messaging_customer = get_object_or_404(MCustomer, customer_id = customer_id)
    if transaction_total > 0:
        messaging_customer.total_balance += transaction_total
        messaging_customer.save()
    
def new_period():
    customers = MCustomer.objects.all()
    for obj in customers:
        print(0)
        obj.messages_period = 0
        obj.save()
    

def index2(request):
    behaviors = Behavior.objects.all()
    context = {'behaviors' : behaviors}
    return render(request, 'messaging/messaging_index.html', context)
    




def create_csv(request):
    response = HttpResponse(content_type='text/csv')
    
    writer = csv.writer(response)
    writer.writerow(['First', 'Last', 'Address', 'Email', 'Phone', 'Created', 'Balance', 'Last Visit', 'messages_period', 'total_balance', 'last_marketed', 'opted', 'id'])
    mcustomers = MCustomer.objects.all().order_by('customer_id').values_list('messages_period', 'total_balance', 'last_marketed', 'opted', 'customer_id')
    customers = Customer.objects.all().order_by('id').values_list('first', 'last', 'address', 'email', 'phone', 'created', 'balance', 'lastvisit')
    for i in range(0, len(customers)):
        writer.writerow(customers[i] + mcustomers[i])  
    response['Content-Disposition'] = 'attachments; filename="customer.csv" '
    return response




def transaction_csv(request):
    response = HttpResponse(content_type='text/csv')
    
    writer = csv.writer(response)
    writer.writerow(['time', 'total', 'customer', 'customer_id', 'user_id'])
    transactions = Transaction.objects.all().order_by('customer_id').values_list('time', 'total', 'customer', 'customer_id', 'user_id')
    #customers = Customer.objects.all().order_by('id').values_list('first', 'last', 'address', 'email', 'phone', 'created', 'balance', 'lastvisit')
    for i in range(0, len(transactions)):
        writer.writerow(transactions[i])  
    response['Content-Disposition'] = 'attachments; filename="transactions.csv" '
    return response




def promo_csv(request):
    response = HttpResponse(content_type='text/csv')
    
    writer = csv.writer(response)
    writer.writerow(['message', 'behavior', 'attachment', 'customer_id'])
    promos = Promo.objects.all().order_by('customer_id').values_list('message', 'behavior', 'attachment', 'customer_id')
    #customers = Customer.objects.all().order_by('id').values_list('first', 'last', 'address', 'email', 'phone', 'created', 'balance', 'lastvisit')
    for i in range(0, len(promos)):
        writer.writerow(promos[i])  
    response['Content-Disposition'] = 'attachments; filename="promotions.csv" '
    return response
    
    
    
def message_csv(request):
    response = HttpResponse(content_type='text/csv')
    
    writer = csv.writer(response)
    writer.writerow(['message', 'behavior', 'attachment', 'customer_id', 'created'])
    messages = ShortMessage.objects.all().order_by('customer_id').values_list('message', 'behavior', 'attachment', 'customer_id', 'created')
    #customers = Customer.objects.all().order_by('id').values_list('first', 'last', 'address', 'email', 'phone', 'created', 'balance', 'lastvisit')
    for i in range(0, len(messages)):
        writer.writerow(messages[i])  
    response['Content-Disposition'] = 'attachments; filename="messages.csv" '
    return response
    
    
    
    
def opt_record_csv(request):
    response = HttpResponse(content_type='text/csv')
    
    writer = csv.writer(response)
    writer.writerow(['consent', 'opt', 'customer_id'])
    optrecords = OptRecord.objects.all().order_by('customer_id').values_list('consent', 'opt', 'customer_id')
    #customers = Customer.objects.all().order_by('id').values_list('first', 'last', 'address', 'email', 'phone', 'created', 'balance', 'lastvisit')
    for i in range(0, len(optrecords)):
        writer.writerow(optrecords[i])  
    response['Content-Disposition'] = 'attachments; filename="opt_records.csv" '
    return response
    
    
def behavior_csv(request):
    response = HttpResponse(content_type='text/csv')
    
    writer = csv.writer(response)
    writer.writerow(['start', 'end', 'reach_percent', 'reach_total', 'title', 'comments', 'demo', 'platform', 'reached', 'active', 'promotion', 'expiration', 'id'])
    behaviors = Behavior.objects.all().order_by('id').values_list('start', 'end', 'reach_percent', 'reach_total', 'title', 'comments', 'demo', 'platform', 'reached', 'active', 'promotion', 'expiration', 'id')
    #customers = Customer.objects.all().order_by('id').values_list('first', 'last', 'address', 'email', 'phone', 'created', 'balance', 'lastvisit')
    for i in range(0, len(behaviors)):
        writer.writerow(behaviors[i])  
    response['Content-Disposition'] = 'attachments; filename="behavior.csv" '
    return response

    
    
def behavior_create(request):
    """register new user"""
    if request.method != 'POST':
        behavior_form = BehaviorForm()
    else:
        behavior_form = BehaviorForm(data=request.POST)
        if behavior_form.is_valid():
            new_behavior = behavior_form.save(commit=False)
            new_behavior.reached = 0  
            new_behavior.save()
            #return HttpResponseRedirect(reverse('rewards:index'))
            return HttpResponseRedirect(reverse('messaging:index2'))
            
    context = {'behavior_form': behavior_form}
    return render(request, 'messaging/behavior_creation.html', context)
    


def message_create(request, behavior_id):
    """register new user"""
    behavior = get_object_or_404(Behavior, id = behavior_id)
    messages = Message.objects.filter(behavior = behavior_id)
    attachments = Attachment.objects.filter(behavior = behavior_id)
    behaviors = Behavior.objects.all()
    if request.method != 'POST':
        message_form = MessageForm()
        attachment_form = AttachmentForm()
    else:
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.behavior = behavior   
            new_message.save()
            return HttpResponseRedirect(reverse('messaging:message_create', args=(behavior.id,)))
            
    context = {'message_form': message_form, 'behavior' : behavior, 'messages' : messages, 'attachments' : attachments, 'attachment_form' : attachment_form, 'behaviors' : behaviors}
    return render(request, 'messaging/message_creation.html', context)
    
    
def behavior_edit(request, behavior_id):
    """register new user"""
    #eobj = get_object_or_404(Employee, user_id = request.user.id)
    obj = get_object_or_404(Behavior, id = behavior_id)
    if request.method != 'POST':
        behavior_form = BehaviorForm(instance = obj)
    else:
        behavior_form = BehaviorForm(instance = obj, data=request.POST)
        if behavior_form.is_valid():
            new_behavior = behavior_form.save()        
            return HttpResponseRedirect(reverse('messaging:message_create', args=(behavior_id,)))
            
    context = {'behavior_form': behavior_form}
    return render(request, 'messaging/behavior_creation.html', context)
    
    
    
def behavior_delete(request, behavior_id):
    """register new user"""
    #eobj = get_object_or_404(Employee, user_id = request.user.id)
    behavior = get_object_or_404(Behavior, id = behavior_id)
    messages = Message.objects.filter(behavior = behavior.id)
    for message in messages:
        message.delete()
    behavior.delete()
    return HttpResponseRedirect(reverse('messaging:index2'))
            
    
    
    
def message_edit(request, message_id):
    """register new user"""
    #eobj = get_object_or_404(Employee, user_id = request.user.id)
    obj = get_object_or_404(Message, id = message_id)
    bobj = get_object_or_404(Behavior, id = obj.behavior.id)
    
    if request.method != 'POST':
        message_form = MessageForm(instance = obj)
    else:
        message_form = MessageForm(instance = obj, data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.behavior = bobj        
            return HttpResponseRedirect(reverse('messaging:message_create', args=(bobj.id,)))
            
    context = {'message_form': message_form, 'message' : obj}
    return render(request, 'messaging/message_edit.html', context)
    
    
    
def message_delete(request, message_id):
    """register new user"""
    #eobj = get_object_or_404(Employee, user_id = request.user.id)
    obj = get_object_or_404(Message, id = message_id)
    obj.delete()
    return HttpResponseRedirect(reverse('messaging:message_create', args=(obj.behavior.id,)))



def analytics(request):
    behaviors = Behavior.objects.all()
    l = []
    for i in behaviors:
        l.append('/media/plots/' + str(i.title) + '.png')
    
    
    context = {'l': l, 'behaviors' : behaviors}
    return render(request, 'messaging/analytics1.php', context)
    




def attachment_delete(request, attachment_id):
    """register new user"""
    #eobj = get_object_or_404(Employee, user_id = request.user.id)
    
    obj = get_object_or_404(Attachment, id = attachment_id)
    os.remove(obj.upload.path)
    obj.delete()
    return HttpResponseRedirect(reverse('messaging:message_create', args=(obj.behavior.id,)))
    
    
    
def attach_file(request, behavior_id):
    behavior = get_object_or_404(Behavior, id = behavior_id)
    if request.method != 'POST':
        # show empty form
        attachment_form = AttachmentForm()
    else:
        attachment_form = AttachmentForm(request.POST, request.FILES)
        if attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.behavior = behavior
            attachment.save()  
            return HttpResponseRedirect(reverse('messaging:message_create', args=(behavior.id,)))
            
    context = {'attachment_form': attachment_form}
    return render(request, 'messaging/attachment_upload.html', context)
    
    
    



def get_csv(request, behavior_id):
    ids = []
    behavior = get_object_or_404(Behavior, id = behavior_id)
    if request.method != 'POST':
        document_form = DocumentForm()
    else:
        document_form = DocumentForm(request.POST, request.FILES)
        if document_form.is_valid():
            document = document_form.save(commit=True)
            filename = open(document.upload.path, 'r')
            file = csv.DictReader(filename)
            for col in file:
                ids.append(col['id'])
            get_customers(ids, behavior)
            os.remove(document.upload.path)
            document.delete()
            return HttpResponseRedirect(reverse('messaging:index2'))
        
        
    context = {'document_form': document_form}
    return render(request, 'messaging/profile_upload.html', context)
    
    
    
def get_plot2():
    for behavior in Behavior.objects.all():
        get_plot(behavior.id)


def get_plot(behavior_id):
    behavior = get_object_or_404(Behavior, id = behavior_id)
    
    messages = pd.DataFrame(list(ShortMessage.objects.filter(behavior = behavior_id).values()))
    rt = pd.DataFrame(list(Transaction.objects.all().values()))
    print("K")
    print(len(messages))
    print(len(rt))
    
    rt = rt[rt['customer_id'].isin(messages['customer_id'].unique())]
    
    messages['V'] = np.arange(0, len(messages))
    #messages['V'] = np.ones(len(messages))
    #rt['V'] = np.arange(0,len(rt))

    rt = rt.sort_values(by='time',  ascending=True)
    messages = messages.sort_values(by='created', ascending=True)
    '''
    plt.plot(rt['time'], rt['total'], '-ok',markersize=1, linewidth=1, label = "transactions")
    plt.plot(messages['created'], messages['V'], linewidth=2.5, label = "messages")
    '''
    #print(rt['total'].rolling(5).mean())
    #print(messages['V'].rolling(5).mean())
    
    plt.plot(rt['time'], rt['total'], '-ok',markersize=1, linewidth=1, label = "transactions")
    plt.plot(messages['created'], messages['V'], linewidth=2.5, label = "messages")
    plt.legend(loc="upper left")
    #plt.legend()
    #plt.show()
    plt.savefig('media/plots/' + str(behavior.title).replace(" ", "") + '.png')
    plt.close()
    
    
    

    
    
def get_customers(ids, behavior):
    customers = []
    for i in ids:
        customers.append(get_object_or_404(Customer, id = i))
    return send_messages(customers, behavior)



def pdf_view(request, attachment_id):
    try:
        obj = get_object_or_404(Attachment, id = attachment_id)
        return FileResponse(open(obj.upload.path, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


#get_plot2()
#get_plot(12)
print("P")     

    

