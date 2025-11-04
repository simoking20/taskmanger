# Accounts/urls.py
from django.urls import path
from . import views
from django.shortcuts import redirect
app_name = 'accounts'

urlpatterns = [
    path('', lambda request: redirect('accounts:login')), 
    path('dashboard/', views.member_dashboard, name='member_dashboard'),
    path('login/', views.member_login, name='login'),
    path('logout/', views.member_logout, name='logout'),
    path('signup/', views.member_signup, name='signup'),
]
