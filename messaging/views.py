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
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse

import os
from azure.communication.sms import SmsClient

import random

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, FileContent, FileName, FileType, Disposition, ContentId)
from sendgrid.helpers.mail import Attachment as FAttachment
import base64

import csv, io

#update datetimefield with datetime.datetime.now()



# Create your views here.



def recieve_messaging():
    CONNECTION_STR = "Endpoint=sb://rewardssb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=fHMy3hEwmC+2qnfWXjmoWsFznmaUMWcVXLaEhHLXRXw="
    QUEUE_NAME = "portalrm"

    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

    with servicebus_client:
        receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME, max_wait_time=5)
        with receiver:
            for msg in receiver:
                print("Received: " + str(msg))
                #number
                number = str(msg).split('+')[2].split('"')[0]
                #message
                message = str(msg).split('message')[2].split('"')[2].lower()
                receiver.complete_message(msg)
                if message == 'y' or message == 'yes':
                    opt_log(number)
                    opt_record_s2(str(msg), number)
                    
                    
def opt_log(number):
    print('get bitch')
    obj = Customer.objects.filter(phone = number[1:])
    mc = MCustomer.objects.filter(customer = obj[0].id)
    mc[0].opted = True
    mc[0].save()

def send_sm(customer_id, message):
    obj = get_object_or_404(Customer, id = customer_id)
    print(obj.phone)
    sms_client = SmsClient.from_connection_string('endpoint=https://portalcommunication.communication.azure.com/;accesskey=yEo6SpHo5gaGTpLbH3dqFyHPCVJf1Ot3I4kvNWom2wWXOU0wBWa3lmWzR68wiSFMvefXzZFafecGKgZRn10HPg==')
    sms_responses = sms_client.send(
    from_="+18333491173",
    to="+14703578182",
    message=message.body + ' \t-' + message.subject,
    enable_delivery_report=True, # optional property
    tag="custom-tag") # optional property
    print(sms_responses.message)
    
def send_e(customer_id, message, file_attachment=None):
    print("ehehehehehheheh")
    obj = get_object_or_404(Customer, id = customer_id)
    message = Mail(
        from_email='gtechmedia840@gmail.com',
        to_emails=obj.email,
        subject=message.subject,
        #html_content='<strong>and easy to do anywhere, even with Python</strong>')
        html_content=message.body)
    if file_attachment != None:
        
        #file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_attachment.upload.url)
        file_path = file_attachment.upload.path
        print(file_path)

        with open(file_path, 'rb') as f:
            data = f.read()

        encoded = base64.b64encode(data).decode()

        attachment = FAttachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType("application/pdf")
        attachment.file_name = FileName("attachment.pdf")
        attachment.disposition = Disposition("attachment")
        attachment.content_id = ContentId("PDF Document file")
        message.attachment = attachment
        
    try:
        #sg = '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'
        sg = SendGridAPIClient('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')
        response = sg.send(message)

    except Exception as e:
        print(e)
    




def opt_in(customer_id, *args, **kwargs):
    obj = get_object_or_404(Customer, id = customer_id)
    print(obj.phone)
    message = "send 'Y', 'y' or 'yes' to opt into messaging"
    sms_client = SmsClient.from_connection_string('endpoint=https://portalcommunication.communication.azure.com/;accesskey=yEo6SpHo5gaGTpLbH3dqFyHPCVJf1Ot3I4kvNWom2wWXOU0wBWa3lmWzR68wiSFMvefXzZFafecGKgZRn10HPg==')
    sms_responses = sms_client.send(
    from_="+18333491173",
    to='+1' + obj.phone,
    message = message,
    enable_delivery_report=True, # optional property
    tag="custom-tag") # optional property
    consent = "to " + sms_responses[0].to + "message id" + sms_responses[0].message_id
    opt_record_s1(consent, obj)
    
    
def opt_record_s1(consentm, customer):
    print('s1')
    print(consentm)
    try:
        r = OptRecord(consent=consentm, customer=customer)
        r.save()
        
    except Exception as e:
        r = OptRecord.objects.get(customer = customer.id)
        r.consent = consentm
        r.save()
    #r = OptRecord(consent=consentm, customer=customer)
    #r.save()
    
    
def opt_record_s2(opt, number):
    print('s1')
    print(len(opt))
    customer = Customer.objects.filter(phone = number[1:])
    mc = MCustomer.objects.get(customer = customer[0].id)
    mc.opted = True
    mc.save()
    r = OptRecord.objects.get(customer = customer[0])
    r.opt=opt
    r.save()

    
    
         
def message_s1():
     recieve_messaging()
     b1 = Behavior.objects.filter(demo = '1')
     b1 = list(b1)
     if len(b1) > 0:
         message_s2(b1, '1')
     
     b2 = Behavior.objects.filter(demo = '2')
     b2 = list(b2)
     if len(b2) > 0:
         message_s2(b2, '2')
     
     b3 = Behavior.objects.filter(demo = '3')
     b3 = list(b3)
     if len(b3) > 0:
         message_s2(b3, '3')
     
     b4 = Behavior.objects.filter(demo = '4')
     b4 = list(b4)
     if len(b4) > 0:
         message_s3(b4)
     
     b5 = Behavior.objects.filter(demo = '5')
     b5 = list(b5)
     if len(b5) > 0:
         message_s4(b5)
     b6 = Behavior.objects.filter(demo = '6')
     b6 = list(b6)
     if len(b6) > 0:
         message_s5(b6)
         
     if datetime.now().day == 1:
         print("first")
         new_period()
     else:
         print("not")
     



#sorts customer list by balance and isolates upper lower, middle and percentile 
def message_s2(mylist, d):
    #c = MCustomer.objects.filter(opted = True)
    c = MCustomer.objects.all()
    c.order_by('total_balance')
    c = list(c)
    print(len(mylist))
    if len(mylist) != 0:
        k = mylist[0]
        
        while k != None:
            if behavior_check(k) == True:
                #print("banacheck")
                v = int(len(c) * k.reach_percent / 100)
                if d == '1':
                    print("lower")
                    c = c[0:v]
                    c = customer_check2(c)
                    print(len(c))
                    send_messages(c, k)
                if d == '2':
                    print("middle")
                    mid = int(len(c) / 2) 
                    m = int((v/2))
                    c = c[mid - m : mid + m]
                    c = customer_check2(c)
                    print(len(c))
                    send_messages(c, k)
                if d == '3':
                    print("Higher")
                    c = c[len(c)-v: -1]
                    c = customer_check2(c)           
                    print(len(c))
                    send_messages(c, k)
            del mylist[0]
            return message_s2(mylist, d)
            


'''
#sorts customer list by balance and isolates upper lower, middle and percentile 
def message_s2(behaviors, d):
    #sorts customers by total_balance lower starting at index [0]
    c = MCustomer.objects.order_by('total_balance')
    c = list(c)
    #v = int(len(c) * behavior.reach_percent / 100)
    for behavior in behaviors:
       if behavior_check(behavior) == True:
           v = int(len(c) * behavior.reach_percent / 100)
           if d == '1':
               print(len(c[0:v]))
               c = c[0:v]
               print("c")
               print(len(c))
               c = customer_check2(c)
               send_messages(c, behavior)
           if d == '2':
               mid = int(len(c) / 2) 
               m = int((v/2))
               print(len(c[mid - m : mid + m]))
               c = c[mid - m : mid + m]
               c = customer_check2(c)
               send_messages(c, behavior)
           if d == '3':
               print(len(c[len(c)-v: -1]))
               c = c[len(c)-v: -1]
               c = customer_check2(c)           
               send_messages(c, behavior)
'''




#isolates a random demo of customers
def message_s3(mylist, customers=0, v=0):
    '''
    vc = []
    customers = MCustomer.objects.order_by('total_balance')
    customers = list(customers)
    v = int(len(customers) * mylist[0].reach_percent / 100)
    '''
    print("Random")
    if len(mylist) != 0:
        if v== 0:
            #print('test')
            customers = MCustomer.objects.order_by('total_balance')
            customers = list(customers)
            v = int(len(customers) * mylist[0].reach_percent / 100)
        k = mylist[0]
        ri = random.randint(0,len(customers))-1
        c = customers[ri]
        del customers[ri]
        #del mylist[0]
    
        if behavior_check(k) == True:
            if customer_check(c) == True:
                send_messages([c], k)
        v = v - 1
        if v == 0:
            del mylist[0]
        return message_s3(mylist, customers, v)





'''

#markets to randomly selected customers 
def message_s3(behaviors):
    vc = []
    c = MCustomer.objects.order_by('total_balance')
    c = list(c)
    v = int(len(c) * behaviors[0].reach_percent / 100)
    for behavior in behaviors:
        if behavior_check(behavior) == True:
            for i in range(0, v):
                if customer_check(c[random.randint(0,len(c))-1]) == True:
                    vc.append(c[random.randint(0,len(c))-1])
                else:
                    i = i-1
            c = customer_check2(vc)
            send_messages(c, behavior)
    print(len(vc))
'''


#messages to customers who havnt been in in a while
def message_s4(mylist):
    c = Customer.objects.order_by('lastvisit')
    c = list(c)
    print("long time no see")
    #print(len(mylist))
    if len(mylist) != 0:
        k = mylist[0]
        del mylist[0]
        while k != None:
            #print('checkaroo boi 3')
            if behavior_check(k) == True:
                #c = Customer.objects.order_by('lastvisit')
                v = int(len(c) * k.reach_percent / 100)
                #print(len(c[0:v]))
                c = customer_check2(c[0:v])
                send_messages(c, k)
            return message_s5(mylist)
    else:
        return







'''
#messages to customers who havnt been in in a while
def message_s4(behaviors):
    c = Customer.objects.order_by('lastvisit')
    for behavior in behaviors:
        if behavior_check(behavior) == True:
            #c = Customer.objects.order_by('lastvisit')
            v = int(len(c) * behavior.reach_percent / 100)
            print(len(c[0:v]))
            c = customer_check2(c[0:v])
            send_messages(c, behavior)
'''



#messages to customers who have recently visited
def message_s5(mylist):
    c = Customer.objects.order_by('lastvisit')
    c = list(c)
    #print("length")
    print("recently visited")
    if len(mylist) != 0:
        k = mylist[0]
        del mylist[0]
        while k != None:
            #print('checkaroo boi')
            if behavior_check(k) == True:
                #c = Customer.objects.order_by('lastvisit')
                v = int(len(c) * k.reach_percent / 100)
                #print(len(c[len(c)-v: -1]))
                c = customer_check2(c[len(c)-v: -1])
                send_messages(c, k)
            return message_s5(mylist)
    else:
        return
    
            





'''
#messages to customers who have recently visited
def message_s5(behaviors):
    c = Customer.objects.order_by('lastvisit')
    c = list(c)
    for behavior in behaviors:
        if behavior_check(behavior) == True:
            #c = Customer.objects.order_by('lastvisit')
            v = int(len(c) * behavior.reach_percent / 100)
            print(len(c[len(c)-v: -1]))
            c = customer_check2(c[len(c)-v: -1])
            send_messages(c, behavior)
'''     






#checks customers are valid to recieve mrketing
def customer_check2(customers):
    #obj = get_object_or_404(Customer, id = customer.customer_id)
    c = []
    print(len(customers))
    for i in range(0, len(customers)-1):
        if customer_check(customers[i]) != False:
            c.append(customers[i])
    return c



#checks customers are valid to recieve mrketing
def customer_check(customer):
    # chech opted field in Mcustomer
    tc = 0
    mp = 8
    try:
        customer = get_object_or_404(MCustomer, customer_id = customer.id)
        pass
        
    except Exception as e:
        pass
    #customer = get_object_or_404(MCustomer, customer_id = customer.id)
    # and customer.opted == True
    if (customer.last_marketed < (timezone.now() - timedelta(days=tc))) and (customer.messages_period < mp) and (customer.customer.lastvisit < (timezone.now() - timedelta(days=tc))):
        #print(customer.messages_period)
        return True
    else:
        return False



def send_messages(customers, behavior):
    messages = Message.objects.filter(behavior_id = behavior.id)
    attachments = Attachment.objects.filter(behavior_id = behavior.id)
    #print(len(messages))
    for i in range(0, len(customers)):
        update_cb(behavior, customers[i])
        if behavior.platform == '1':
            #print(len(Attachment.objects.filter(behavior_id = behavior.id)))
            if len(Attachment.objects.filter(behavior_id = behavior.id)) > 0:
                attachment = Attachment.objects.filter(behavior_id = behavior.id)[random.randint(0,len(Attachment.objects.filter(behavior_id = behavior.id))-1)]
                update_a(attachment)
            message = messages[random.randint(0,len(Message.objects.filter(behavior_id = behavior.id))-1)]
            #send_e(customers[i].customer.id, message, attachment)
            update_m(message)
            create_promo(message, behavior, customers[i])
        else:
            #send_sm(customers[i].customer.id, messages[random.randint(0,len(messages)-1)])
            pass

def update_a(attachment):
    print('update records')
    attachment.count = attachment.count + 1
    attachment.save()
    
    
    
def update_m(message):
    print('update records')
    message.count = message.count + 1
    message.save()


def update_cb(behavior, customer):
    try:
        customer = get_object_or_404(MCustomer, customer_id = customer.id)
        print('switched')
    except Exception as e:
        print('e')
    behavior.reached = behavior.reached + 1
    behavior.save()
    
    customer.messages_period = customer.messages_period + 1
    customer.save()
    
    customer.last_marketed = timezone.now()
    customer.save()
    #behavior.save()
    #customer.save()


def behavior_check(behavior):
    t = behavior.reach_percent * len(MCustomer.objects.all()) / 100
    if behavior.reached < t and behavior.reached < behavior.reach_total and behavior.active == True:
        print("True")
        return True
    else: 
        print("False")
        return False 



#message_s1()

            
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
    
def create_promo(message, behavior, customer):
    
    try:
        customer = get_object_or_404(MCustomer, customer_id = customer.id)
        pass
        
    except Exception as e:
        pass
    
    if behavior.promotion == True:
        print("created promotion")
        promotion = Promo.objects.create(customer = customer.customer, message = message, behavior = behavior)
    else:
       return


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
    
    
    
def get_customers(ids, behavior):
    customers = []
    for i in ids:
        customers.append(get_object_or_404(Customer, id = i))
    return send_messages(customers, behavior)





            

    

