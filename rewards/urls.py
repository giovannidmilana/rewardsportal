from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

#app_name = 'rewards'

urlpatterns = [
    path('', views.index, name='index'),
    path('employee_edit/', views.employee_edit, name='employee_edit'),
    path('register/', views.register, name='register'),
    path('m_opt_in/<int:customer_id>/', views.m_opt_in, name='m_opt_in'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('searche/', SearchResultsViewE.as_view(), name='search_resultse'),
    path('searchc/', SearchResultsViewC.as_view(), name='search_resultsc'),
    path('customer_creation/', views.customer_create, name='customer_creation'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='rewards/login.html'), name='login'),
    path('transaction/<int:customer_id>/', views.create_transaction, name='create_transaction'),
    path('customer_edit/<int:customer_id>/', views.customer_edit, name='customer_edit'),
    path('employee_edit2/<int:user_id>/', views.employee_edit2, name='employee_edit2'),
    path('customer_delete/<int:customer_id>/', views.customer_delete, name='customer_delete'),
    path('employee_delete/<int:user_id>/', views.employee_delete, name='employee_delete'),
    path('add_card/<int:customer_id>/', views.upc_create, name='upc_create'),
    path('promo_redeem/<int:promo_id>/<int:customer_id>/', views.promo_redeem, name='promo_redeem'),


]

