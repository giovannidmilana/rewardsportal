import os
import sys
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from rewards.models import *
from .models import *
from datetime import datetime, timedelta
from django.utils import timezone

from .views import *

import os
from azure.communication.sms import SmsClient
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, FileContent, FileName, FileType, Disposition, ContentId)
from sendgrid.helpers.mail import Attachment as FAttachment
import base64
import csv, io

from .views import *



def main():
    print('Main')
    behaviors = Behavior.objects.all()
    c = MCustomer.objects.all().order_by('total_balance')
    #c = list(c)
    t = len(list(c))
    print(t)
    for behavior in behaviors:
        v = int(t * behavior.reach_percent / 100)
        #lower percentage customers
        if behavior.demo == '1' and behavior_check(behavior) == True:
            c = MCustomer.objects.all().order_by('total_balance')
            c = c[0:v]
            c = customer_check2(c)
            send_messages(c, behavior)
        #median percentage customers
        if behavior.demo == '2' and behavior_check(behavior) == True:
            c = MCustomer.objects.all().order_by('total_balance')
            #middle of customer list
            mid = int(len(c) / 2) 
            #half the number of customer to be reached by behavior 
            m = int((v/2))
            #customer objects to reach 
            c = c[mid - m : mid + m]
            c = customer_check2(c)
            send_messages(c, behavior)
        #lower percentile customers
        if behavior.demo == '3' and behavior_check(behavior) == True:
            c = MCustomer.objects.all().order_by('total_balance')
            c = c[len(c)-v-1:]
            c = customer_check2(c)
            send_messages(c, behavior)
        #randomly selected customers
        if behavior.demo == '4' and behavior_check(behavior) == True:
            customers = MCustomer.objects.all()
            #customers = list(customers)
            #number of customers to reach
            for i in range(0,v):
                ri = random.randint(0,len(customers)-1)
                c = customers[ri]
                if customer_check(c) == True:
                    send_messages([c], behavior)
        #recently vistited
        if behavior.demo == '5' and behavior_check(behavior) == True:
            customers = Customer.objects.order_by('lastvisit')
            #c = list(c)
            #v = int(len(c) * k.reach_percent / 100)
            customers = customer_trans(customers)
            customers = customer_check2(customers[:v])
            send_messages(customers, behavior)
        #long time no see
        if behavior.demo == '6' and behavior_check(behavior) == True:
            customers = Customer.objects.order_by('lastvisit')
            #c = list(c)
            #v = int(len(c) * k.reach_percent / 100)
            customers = customer_trans(customers)
            customers = customer_check2(customers[t-v:])
            send_messages(customers, behavior)
        
        get_plot2()
        
        
        
        
        
#checks customers are valid to recieve mrketing
def customer_check2(customers):
    #obj = get_object_or_404(Customer, id = customer.customer_id)
    c = []
    print(len(customers))
    for i in range(0, len(customers)-1):
        if customer_check(customers[i]) != False:
            c.append(customers[i])
    return c


def customer_trans(customers):
    l = []
    for customer in customers:
        try:
            l.append(MCustomer.objects.get(customer_id = customer.id))
        except Exception as e:
            pass
    return l
        





#checks customers are valid to recieve mrketing
def customer_check(customer):
    # chech opted field in Mcustomer
    tc = 0
    mp = 14
    # and customer.opted == True
    if (customer.last_marketed < (timezone.now() - timedelta(days=tc))) and (customer.messages_period < mp) and (customer.customer.lastvisit < (timezone.now() - timedelta(days=tc))):
        #print(customer.messages_period)
        return True
    else:
        return False

########## make work better    
def send_messages(customers, behavior):
    messages = Message.objects.filter(behavior_id = behavior.id)
    attachments = Attachment.objects.filter(behavior_id = behavior.id)
    attachment = 0
    #print(len(messages))
    for i in range(0, len(customers)):
        #print(customers[i].total_balance)
        #update_cb(behavior, customers[i])
        if behavior.platform == '1':
            #print(len(Attachment.objects.filter(behavior_id = behavior.id)))
            if len(Attachment.objects.filter(behavior_id = behavior.id)) > 0:
                attachment = Attachment.objects.filter(behavior_id = behavior.id)[random.randint(0,len(Attachment.objects.filter(behavior_id = behavior.id))-1)]
                update_a(attachment)
            if len(Message.objects.filter(behavior_id = behavior.id)) > 0:
                print("M")
                print(len(messages) - 1)
                message = messages[random.randint(0,len(messages) - 1)]
                update_m(message)
                create_promo(message, behavior, customers[i])
                create_sm(message, behavior, customers[i], attachment)
                update_cb(behavior, customers[i])
            #send_e(customers[i].customer.id, message, attachment)
            #update_cb(behavior, customers[i])
        else:
            create_sm(message, behavior, customers[i], attachment)
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
        
        
def create_sm(message, behavior, customer, attachment):
    '''
    try:
        customer = get_object_or_404(MCustomer, customer_id = customer.id)
        pass
        
    except Exception as e:
        pass
    '''
    if attachment != 0:
        print("created message object with attachment")
        sm = ShortMessage.objects.create(customer = customer.customer, message = message, behavior = behavior, attachment = attachment)
    else:
       print("created message object without attachment")
       sm = ShortMessage.objects.create(customer = customer.customer, message = message, behavior = behavior)
    return
    
    
    
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

       
       
