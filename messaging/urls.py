#urls
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

#app_name = 'messaging'

urlpatterns = [
    #path('opt_in/<int:customer_id>/', views.opt_in, name='opt_in'),
    path('behavior_creation/', views.behavior_create, name='behavior_creation'),
    path('messaging/', views.index2, name='index2'),
    path('message_creation/<int:behavior_id>/', views.message_create, name='message_create'),
    path('attach_file/<int:behavior_id>/', views.attach_file, name='attach_file'),
    path('behavior_edit/<int:behavior_id>/', views.behavior_edit, name='behavior_edit'),
    path('behavior_delete/<int:behavior_id>/', views.behavior_delete, name='behavior_delete'),
    path('message_edit/<int:message_id>/', views.message_edit, name='message_edit'),
    path('message_delete/<int:message_id>/', views.message_delete, name='message_delete'),
    path('attachment_delete/<int:attachment_id>/', views.attachment_delete, name='attachment_delete'),
    
    path('analytics/', views.analytics, name='analytics'),
    
    path('create_csv/', views.create_csv, name='create_csv'),
    
    path('transaction_csv/', views.transaction_csv, name='transaction_csv'),
    
    path('promo_csv/', views.promo_csv, name='promo_csv'),
    
    path('opt_record_csv/', views.opt_record_csv, name='opt_record_csv'),
    
    path('behavior_csv/', views.behavior_csv, name='behavior_csv'),
    
    path('message_csv/', views.message_csv, name='message_csv'),
    
    
    path('get_csv/<int:behavior_id>/', views.get_csv, name="get_csv"),
    
    path('pdf_view/<int:attachment_id>/', views.pdf_view, name="pdf_view"),
    
    
    
    #path('create_csv/', views.create_csv, name='create_csv')

]
