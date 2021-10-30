from django import forms
from django.contrib.auth.models import User
from .models import *
from django.db import models




class BehaviorForm(forms.ModelForm):
    class Meta:
        model = Behavior
        fields = ('title', 'comments', 'start', 'end', 'reach_percent', 'reach_total', 'demo', 'platform', 'reached', 'active', 'promotion', 'expiration', )
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('body', 'subject',)
        widgets = {'body': forms.Textarea(attrs={'cols': 30, 'rows': 5}), 'subject': forms.Textarea(attrs={'cols': 20, 'rows': 2})}
        
class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('title', 'upload',)
        
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('upload',)
