from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from .models import *


# Create your views here.


def index(request):
    return render(request,'app/index.html')

def register(request):
    return render(request, 'app/Register.html')

def login(request):
    return render(request, 'app/Login.html')

def dashboard(request):
    return render(request, 'app/dashboard.html')

def purchase(request):
    return render(request, 'app/Purchase.html')





 