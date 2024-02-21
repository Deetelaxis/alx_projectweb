from django.urls import path,include
from .import views
from .models import *
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib import admin
import notifications.urls

urlpatterns = [
    
    path('Airtime_History_new/',login_required(views.Airtime_History_new),name='airtime_history_new'),
    path('Data_History_new/',login_required(views.Data_History_new),name='data_history_new'),
    path('succesmessage/',TemplateView.as_view(template_name='succesmessage.html'),name='succesmessage.'),
    path('user-detail/', login_required(TemplateView.as_view(template_name='userdetails.html')),name='userdetails'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('Wallet_Summary/',login_required(views.Wallet_Summary),name='wallet'),
    path('data_Create/',login_required(views.dataCreate.as_view()),name='data'),
    path('AirtimeTopupCreate/',login_required(views.AirtimeTopupCreate.as_view()),name='topup'),
    path('ajax/load_plans/', login_required(views.loadplans), name='ajax_load_plans'),
    path('profile/',login_required(views.Profile.as_view()),name='profile'),
    path('AirtimeTopup_success/<int:pk>/',login_required(views.AirtimeTopup_success.as_view()),name='AirtimeTopup_success'),
    path('Data_success/<int:pk>/',login_required(views.Data_success.as_view()),name='Data_success'),
    
]

admin.site.site_title = f"Alxproject"
admin.site.site_header = f"Welcome To Alxproject Admin Panel"

