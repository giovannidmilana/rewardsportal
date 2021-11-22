from django.db import models
from rewards.models import *
from datetime import datetime, timedelta
#from django.utils.timezone import now

from django.utils import timezone
# Create your models here.



class MCustomer(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=False)
    messages_period = models.IntegerField(blank=False, null=False)
    total_balance = models.DecimalField(max_digits=12, decimal_places=2)
    last_marketed = models.DateTimeField(null=False)
    opted = models.BooleanField(default=False, null=False)
    

def end_time(): 
    return timezone.now() + timedelta(days=730)



class Behavior(models.Model):
    CHOICES1 = (('1', 'Lower Percentile Customers'),
               ('2', 'Middle Percentile Customers'),
               ('3', 'Higher Percentile Customers'),
               ('4', 'Random'),
               ('5', 'Long Time No See'),
               ('6', 'Recently Visited'))
    
    CHOICES2 = (('1', 'Email'),
               ('2', 'Phone'))
    start = models.DateTimeField(null=False, default=timezone.now)
    end = models.DateTimeField(null=False, default=end_time())
    reach_percent = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    reach_total = models.IntegerField(null=True)
    title = models.CharField(max_length=20, null=False)
    comments = models.CharField(max_length=100)
    demo = models.CharField(choices=CHOICES1, max_length=2,)
    platform = models.CharField(choices=CHOICES2, max_length=6, null=False)
    reached = models.IntegerField(null=False, default=0)
    active = models.BooleanField(default=True, null=False)
    promotion = models.BooleanField(default=False, null=False)
    expiration = models.DateTimeField(null=True, blank=True)
    #add group field (FK)
    
    def plot_path(self):
        return "/media/plots/" + str(self.title).replace(" ", "") + ".png"
        
    def getMvalue(self):
        return len(ShortMessage.objects.filter(behavior_id = self.id))
        
    def getTvalue(self):
        l = []
        for i in ShortMessage.objects.filter(behavior_id = self.id):
            l.append(Transaction.objects.filter(customer_id = i.customer.id))
        return len(l)
        
    

    
class Message(models.Model):
    behavior = models.ForeignKey(Behavior, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    subject = models.TextField(max_length=70, default='')
    count = models.IntegerField(null=False, default=0)
    
class OptRecord(models.Model):
    consent = models.CharField(max_length=100, null=False)
    opt = models.CharField(max_length=600, null=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=False)
    

class Attachment(models.Model):
    title = models.CharField(max_length=20, null=False)
    behavior = models.ForeignKey(Behavior, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='attachments/')
    count = models.IntegerField(null=False, default=0)
    
    
class Promo(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    behavior = models.ForeignKey(Behavior, on_delete=models.CASCADE)
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    
class Document(models.Model):
    upload = models.FileField(upload_to='attachments/')
    
class ShortMessage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    behavior = models.ForeignKey(Behavior, on_delete=models.CASCADE)
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    
    
    
    
    
    
    
    

    
    
    
    
    

    
    
