
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # <-- Here
from twilio.twiml.messaging_response import Message, MessagingResponse
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from requests.auth import HTTPBasicAuth   
import random
import uuid
from django.core.validators import URLValidator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.utils.timezone import datetime as datetimex
from datetime import datetime as Mdate
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.db.models import F
from twilio.rest import Client
from django import forms
from django.core import serializers as seria2
from django.utils.translation import gettext_lazy as _
from django.forms.utils import ErrorList
from .models import CustomUser
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from notifications.signals import notify
from django.db.models.signals import post_save
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
import uuid
import random
import json
from django.views.generic.edit import FormMixin
from rest_framework import generics
from .serializers import *
from django.utils.timezone import  datetime
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Sum
# new import for webhook
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from time import time
import urllib.parse
import hashlib
import hmac
from django.http import HttpResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

import base64
import logging


logger = logging.getLogger(__file__)


def Data_History_new(request):
    

    search = request.GET.get("q", None)

    if search:

        transactionslist = (
            Data.objects.filter(user=request.user)
            .filter(
                Q(id__icontains=search)
                | Q(ident__icontains=search)
                | Q(mobile_number__icontains=search)
                | Q(Status__icontains=search)

            )
            .order_by("-create_date")
        )

    else:
        transactionslist = Data.objects.filter(user=request.user).order_by("-create_date")

    page = request.GET.get("page", 1)
    paginator = Paginator(transactionslist,  20)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    return render(
        request,
        "data_history_new.html",
        {
            "search": search,
            "transactions": transactions,
        },
    )
    
def Airtime_History_new(request):
    

    search = request.GET.get("q", None)

    if search:

        transactionslist = (
            Data.objects.filter(user=request.user)
            .filter(
                Q(id__icontains=search)
                | Q(ident__icontains=search)
                | Q(mobile_number__icontains=search)
                | Q(Status__icontains=search)

            )
            .order_by("-create_date")
        )

    else:
        transactionslist = AirtimeTopup.objects.filter(user=request.user).order_by("-create_date")

    page = request.GET.get("page", 1)
    paginator = Paginator(transactionslist,  20)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    return render(
        request,
        "airtime_history_new.html",
        {
            "search": search,
            "transactions": transactions,
        },
    )

def Wallet_Summary(request):
    

    search = request.GET.get("q", None)

    if search:

        transactionslist = (
            Wallet_summary.objects.filter(user=request.user)
            .filter(
                Q(id__icontains=search)
                | Q(ident__icontains=search)
                | Q(product__icontains=search)
                | Q(Status__icontains=search)

            )
            .order_by("-create_date")
        )

    else:
        transactionslist = Wallet_summary.objects.filter(user=request.user).order_by("-create_date")

    page = request.GET.get("page", 1)
    paginator = Paginator(transactionslist,  20)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    return render(
        request,
        "wallet.html",
        {
            "search": search,
            "transactions": transactions,
        },
    )


class WelcomeView(TemplateView):
    template_name = 'index.html'

    def referal_user(self):
        if self.request.GET.get("referal"):
            self.request.session["referal"] = self.request.GET.get("referal")
           

    def get_context_data(self, **kwargs):
        net = Network.objects.get(name='MTN')
        net_2 = Network.objects.get(name='GLO')
        net_3 = Network.objects.get(name='9MOBILE')
        net_4 = Network.objects.get(name='AIRTEL')

        context = super(WelcomeView, self).get_context_data(**kwargs)
        context['plan'] = Plan.objects.filter(
            network=net).order_by('plan_amount')
        context['plan_2'] = Plan.objects.filter(
            network=net_2).order_by('plan_amount')
        context['plan_3'] = Plan.objects.filter(
            network=net_3).order_by('plan_amount')
        context['plan_4'] = Plan.objects.filter(
            network=net_4).order_by('plan_amount')
        context['networks'] = Network.objects.all()
        
        return context



class Profile(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        current_month = datetime.now().month
        net = Network.objects.get(name='MTN')
        net_2 = Network.objects.get(name='GLO')
        net_3 = Network.objects.get(name='9MOBILE')
        net_4 = Network.objects.get(name='AIRTEL')
        # (network=net,plan__plan_size__lt=100,create_date__month= current_month)
        data_mtn_obj = Data.objects.filter(network=net, plan__plan_size__lt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_mtn_obj_2 = Data.objects.filter(network=net, plan__plan_size__gt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_glo_obj = Data.objects.filter(network=net_2, plan__plan_size__lt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_glo_obj_2 = Data.objects.filter(network=net_2, plan__plan_size__gt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_9mobile_obj = Data.objects.filter(network=net_3, plan__plan_size__lt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_9mobile_obj_2 = Data.objects.filter(network=net_3, plan__plan_size__gt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_airtel_obj = Data.objects.filter(network=net_4, plan__plan_size__lt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_airtel_obj_2 = Data.objects.filter(network=net_4, plan__plan_size__gt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        total_wallet = CustomUser.objects.all().aggregate(
            Sum('Account_Balance'))['Account_Balance__sum']
       
        
        Topup_obj1 = AirtimeTopup.objects.filter(
            network=net, create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        Topup_obj2 = AirtimeTopup.objects.filter(
            network=net_2, create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        Topup_obj3 = AirtimeTopup.objects.filter(
            network=net_3, create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        Topup_obj4 = AirtimeTopup.objects.filter(
            network=net_4, create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        

       
        context = super(Profile, self).get_context_data(**kwargs)
        
        
        context['data'] = Data.objects.filter(Status='processing').count()
        
        context['airtimeTopup'] = AirtimeTopup.objects.filter(
            Status='processing').count()
        
        try:
            if data_mtn_obj_2:
                context['totalmtnsale'] = data_mtn_obj + (data_mtn_obj_2/1000)
            else:
                context['totalmtnsale'] = data_mtn_obj
            if data_glo_obj_2:
                context['totalglosale'] = data_glo_obj + (data_glog_obj_2/1000)
            else:
                context['totalglosale'] = data_glo_obj

            if data_airtel_obj_2:

                context['totalairtelsale'] = data_airtel_obj + \
                    (data_airtel_obj_2/1000)

            else:
                context['totalairtelsale'] = data_airtel_obj
            if data_9mobile_obj_2:
                context['totalmobilesale'] = data_9mobile_obj + \
                    (data_9mobile_obj_2/1000)
            else:
                context['totalmobilesale'] = data_9mobile_obj
        except:
            pass
        context['twallet'] = round(total_wallet, 2)
        context['wallet'] = Wallet_summary.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['users'] = CustomUser.objects.all().count()
        
        context['AirtimeTopup_obj'] = Topup_obj1
        context['AirtimeTopup_obj2'] = Topup_obj2
        context['AirtimeTopup_obj3'] = Topup_obj3
        context['AirtimeTopup_obj4'] = Topup_obj4
       
        
        return context



class SignUp(SuccessMessageMixin, generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    success_messages = 'You have successfully Registered, Kindly login to continue'


    def get_context_data(self, **kwargs):

        context = super(SignUp, self).get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        username = object.username
        email = object.email
        user = object

        if CustomUser.objects.filter(username__iexact=object.username).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This username has been taken'])
            return self.form_invalid(form)

        elif CustomUser.objects.filter(email__iexact=object.email).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This email has been taken'])
            return self.form_invalid(form)
        
        elif not object.email.endswith(("@gmail.com",'@yahoo.com')):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList([u'We accept only valid gmail or yahoo mail account'])
            return self.form_invalid(form)
      

        form.save()

      
        try:
            messages.success( self.request, 'You have successfully Registered, Kindly login to continue')
        except:
            pass
       
        return super(SignUp, self).form_valid(form)
        
        

class dataCreate(generic.CreateView):
    form_class = dataform
    template_name = 'data_form.html'

    def get_context_data(self,**kwargs):

        context = super(dataCreate,self).get_context_data(**kwargs)
        context['network'] = Network.objects.get(name ='MTN')
        context['network2'] = Network.objects.get(name ='AIRTEL')
        context['networks'] = Network.objects.all()
        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
            [u'use updated browser and retry'])
        return self.form_invalid(form)

        return super(dataCreate, self).form_valid(form)

def loadplans(request):

    network_id = request.GET.get('network')
    datatype = request.GET.get('datatype',None)
    netid = Network.objects.get(id=network_id)
    if datatype:
         plans = Plan.objects.filter(network_id=network_id).filter(plan_type=datatype).order_by('plan_amount')
    else:
         plans = Plan.objects.filter(network_id=network_id).order_by('plan_amount')

    #print(plans)
    return render(request, 'planslist.html', {'plans': plans})



class Data_success(generic.DetailView):
    model = Data
    template_name = 'Data-detail.html'
    queryset = Data.objects.all()
    context_object_name = 'Data_list'


class AirtimeTopupCreate(generic.CreateView):
    form_class = AirtimeTopupform
    template_name = 'AirtimeTopup_form.html'

    def get_context_data(self, **kwargs):

        context = super(AirtimeTopupCreate, self).get_context_data(**kwargs)

        context['mtn'] = (TopupPercentage.objects.get(
            network=Network.objects.get(name="MTN")).percent)/100
        context['glo'] = (TopupPercentage.objects.get(
            network=Network.objects.get(name="GLO")).percent)/100
        context['airtel'] = (TopupPercentage.objects.get(
            network=Network.objects.get(name="AIRTEL")).percent)/100
        context['mobile'] = (TopupPercentage.objects.get(
            network=Network.objects.get(name="9MOBILE")).percent)/100

        context['mtn_s'] = (TopupPercentage.objects.get(
            network=Network.objects.get(name="MTN")).share_n_sell_percent)/100
        context['glo_s'] = (TopupPercentage.objects.get(
            network=Network.objects.get(name="GLO")).share_n_sell_percent)/100
        context['airtel_s'] = (TopupPercentage.objects.get(
            network=Network.objects.get(name="AIRTEL")).share_n_sell_percent)/100
        context['mobile_s'] = (TopupPercentage.objects.get(
            network=Network.objects.get(name="9MOBILE")).share_n_sell_percent)/100

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
            [u'use updated browser and retry'])
        return self.form_invalid(form)

        return super(AirtimeTopupCreate, self).form_valid(form)

class AirtimeTopup_success(generic.DetailView):
    model = AirtimeTopup
    template_name = 'AirtimeTopup.html'
    queryset = AirtimeTopup.objects.all()
    context_object_name = 'AirtimeTopup_list'

def create_id():
    num = random.randint(1, 10)
    num_2 = random.randint(1, 10)
    num_3 = random.randint(1, 10)
    return str(num_2)+str(num_3)+str(uuid.uuid4())





class AlertAPIView(APIView):

    def get(self, request, format=None):

        if Info_Alert.objects.all():
            y = [x.message for x in Info_Alert.objects.all()[:1]][0]

        else:
            y = ""

        return Response({

            "alert": y


        })

class NetworkAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:

            plan_item = Plan.objects.filter(
                network=Network.objects.get(name="MTN")).order_by('plan_amount')
            plan_item_2 = Plan.objects.filter(
                network=Network.objects.get(name="GLO")).order_by('plan_amount')
            plan_item_3 = Plan.objects.filter(
                network=Network.objects.get(name="AIRTEL")).order_by('plan_amount')
            plan_item_4 = Plan.objects.filter(
                network=Network.objects.get(name="9MOBILE")).order_by('plan_amount')

            plan_serializer = PlanSerializer(plan_item, many=True)
            plan_serializer_2 = PlanSerializer(plan_item_2, many=True)
            plan_serializer_3 = PlanSerializer(plan_item_3, many=True)
            plan_serializer_4 = PlanSerializer(plan_item_4, many=True)

            return Response({

                'MTN_PLAN': plan_serializer.data,
                'GLO_PLAN': plan_serializer_2.data,
                'AIRTEL_PLAN': plan_serializer_3.data,
                '9MOBILE_PLAN': plan_serializer_4.data,

            })

        except:
            return Response(status=404)



class DataAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        try:
            item = Data.objects.filter(user=request.user).get(pk=id)
            serializer = DataSerializer(item)
            return Response(serializer.data)
        except Data.DoesNotExist:
            return Response(status=404)


class DataAPIListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        search = request.GET.get("search",None)
        if search:
            items =  Data.objects.filter(user=request.user).filter(Q(id__icontains=search) | Q(ident__icontains=search) | Q(mobile_number__icontains=search)).order_by('-create_date')
            serializer = DataSerializer(items, many=True)
            return Response(serializer.data)

        
        else:
                    
            items = Data.objects.filter(user=request.user).order_by('-create_date')
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(items, request)
            serializer = DataSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        status = "processing"

        serializer = DataSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            order_username = (serializer.validated_data["user"]).username
            num = serializer.validated_data["mobile_number"]
            plan = serializer.validated_data["plan"]


            net = str(serializer.validated_data["network"])
            user = (serializer.validated_data["user"])
            errors = {}
            api_response = ""

            previous_bal = user.Account_Balance

            amount = float(plan.plan_amount)

            with transaction.atomic():
                check = user.withdraw(user.id, amount)
                if check == False:
                    errors['error'] = u'Y insufficient balance '
                    raise serializers.ValidationError(errors)
                Wallet_summary.objects.create(user=user, product="{} {}{}   N{}  DATA topup topup  with {} ".format(
                    net, plan.plan_size, plan.plan_Volume, amount, num), amount=amount, previous_balance=previous_bal, after_balance=(previous_bal - amount))

            def create_id():
                    num = random.randint(1,10)
                    num_2 = random.randint(1,10)
                    num_3 = random.randint(1,10)
                    return "Data"+str(num_3)+str(uuid.uuid4())[:12]

            ident = create_id()
            

            def msorg_senddata(netid,num,plan_id):

                        url = "https://www.deetelaxis.com/api/data/"

                        headers = {
                        'Content-Type':'application/json',
                        'Authorization': 'Token 956bc5309fbc59848db872ba14cd6c0a10224558'
                        }
                        param = {"network": netid,"mobile_number": num,"plan": plan_id,"Ported_number":True}
                        param_data = json.dumps(param)
                        try:
                            response = requests.post(url, headers=headers, data=param_data, verify=False, timeout=60)
                            try:
                                if response.status_code == 200 or response.status_code == 201:
                                    resp =  json.loads(response.text)
                                    if "error" in resp:
                                        return 'failed','Error Occurs'
                                        
                                    if "Please wait while your request is being verified" in resp:
                                        return 'failed','Hosting Disconnected from Source'
                                        
                                    if "api_response" in resp:
                                        if "Status" in resp and resp["Status"]  == "successful" :
                                            return 'successful',resp["api_response"]
                                        elif "Status" in resp and resp["Status"]  == "processing":
                                            return 'successful',resp["api_response"]
                                        else:
                                            return 'failed',resp["api_response"]
                                    
                                    else:
                                        
                                        if "Status" in resp and resp["Status"]  == "successful" :
                                            return 'successful',''
                                        elif "Status" in resp and resp["Status"]  == "processing":
                                            return 'successful',''
                                        else:
                                            return 'failed',''
                                        
                                elif response.status_code == 400 or response.status_code == 401:
                                    return 'failed','No Response'
                                    
                                else:
                                    return 'processing','Response Not Available'
                            except:
                                    return 'processing','Error Occurs !!'
                        
                        except requests.exceptions.HTTPError as errh:
                            return "failed","Transaction Failed, HTTPError"
                        except requests.exceptions.ConnectionError as errc:
                            return "failed","Transaction Failed, ConnectionError"
                        except requests.exceptions.Timeout as errt:
                            return "processing","Transaction Failed, Timeout in 40secs"
                        except requests.exceptions.RequestException as err:
                            return "failed","Transaction Failed, RequestException"
                        except requests.exceptions.TooManyRedirects:
                            return "failed","Transaction Failed, TooManyRedirects"
                        except json.decoder.JSONDecodeError as jerr:  
                            if (response.status_code == 502):
                                return "failed","Bad Gateway"
                            elif (response.status_code == 50):
                                return "failed","Bad Gateway Timeout"
                            elif (response.status_code == 504):
                                return "failed","Gateway Timeout"
                            elif (response.status_code == 500):
                                return "processing","Internal Server Error!"
                            else:
                                return "failed",'Response not in JSON format!'
                        

            if net == 'MTN':
                    resp = msorg_senddata(Network.objects.get(name=net).msorg_web_net_id,num,plan.plan_name_id)
                    status = resp[0]
                    api_response = resp[1]
             
            elif net == 'GLO':
                    resp = msorg_senddata(Network.objects.get(name=net).msorg_web_net_id,num,plan.plan_name_id)
                    status = resp[0]
                    api_response = resp[1]

            elif net == 'AIRTEL':
                resp = msorg_senddata(Network.objects.get(name=net).msorg_web_net_id,num,plan.plan_name_id)
                status = resp[0]
                api_response = resp[1]

            elif net == "9MOBILE":
                    resp = msorg_senddata(Network.objects.get(name=net).msorg_web_net_id,num,plan.plan_name_id)
                    status = resp[0]
                    api_response = resp[1]



            serializer.save(Status=status, api_response=api_response, plan_amount=amount, ident=ident, medium='API',balance_before=previous_bal, balance_after=(previous_bal - amount))

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# airtime topup api

class AirtimeTopupAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        try:
            item = AirtimeTopup.objects.filter(user=request.user).get(pk=id)
            serializer = AirtimeTopupSerializer(item)
            return Response(serializer.data)
        except AirtimeTopup.DoesNotExist:
            return Response(status=404)


class AirtimeTopupAPIListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        search = request.GET.get("search",None)
        if search:
            items =  AirtimeTopup.objects.filter(user=request.user).filter(Q(id__icontains=search) | Q(ident__icontains=search) | Q(mobile_number__icontains=search)).order_by('-create_date')
            serializer = DataSerializer(items, many=True)
            return Response(serializer.data)

        
        else:
            items = AirtimeTopup.objects.filter(
                user=request.user).order_by('-create_date')
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(items, request)
            serializer = AirtimeTopupSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        status = "processing"
        fund = 0
        serializer = AirtimeTopupSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            order_username = (serializer.validated_data["user"]).username
            num = serializer.validated_data["mobile_number"]
            amt = serializer.validated_data["amount"]
            net = str(serializer.validated_data["network"])
            order_user = (serializer.validated_data["user"])
            user = serializer.validated_data["user"]
            previous_bal = order_user.Account_Balance
            airtime_type = (serializer.validated_data["airtime_type"])
            errors = {}

            def create_id():
                num = random.randint(1000, 4999)
                num_2 = random.randint(5000, 8000) 
                num_3 = random.randint(111, 999) * 2
                return str(Mdate.now().strftime("%Y%m%d%H%M%S")) + str(num) + str(num_2) + str(num_3) + str(uuid.uuid4())

            ident = create_id()

            
            perc = TopupPercentage.objects.get(
                network=Network.objects.get(name=net)).percent
            perc2 = TopupPercentage.objects.get(
                network=Network.objects.get(name=net)).share_n_sell_percent



            def msorg_sendairtime(netid,num,amt):

                    url = "https://www.deetelaxis.com/api/topup/"

                    headers = {
                    'Content-Type':'application/json',
                    'Authorization': 'Token 956bc5309fbc59848db872ba14cd6c0a10224558'
                    }
                    param = {"network": netid,"mobile_number": num,"amount":amt,"Ported_number":True,"airtime_type":"VTU"}
                    param_data = json.dumps(param)
                    response = requests.post(url, headers=headers, data=param_data, verify=False)
                    #print(response.text)
                    return response
            
            
            if airtime_type == "VTU":
                amount = float(amt) * int(perc)/100
                check = user.withdraw(user.id, amount)
                if check == False:
                    errors['error'] = u' insufficient balance '
                    raise serializers.ValidationError(errors)
                fund = amount
                Wallet_summary.objects.create(user=order_user, product="{} {} Airtime VTU topup  with {} ".format(net, amt, num), amount=fund, previous_balance=previous_bal, after_balance=(previous_bal - amount))

                amt = int(amt)
                if net == 'MTN':
                        msorg_sendairtime(Network.objects.get(name=net).msorg_web_net_id,num,amt)
                        status = "successful"
                        

                elif net == 'GLO':
                        msorg_sendairtime(Network.objects.get(name=net).msorg_web_net_id,num,amt)
                        status = "successful"


                elif net == 'AIRTEL':
                        msorg_sendairtime(Network.objects.get(name=net).msorg_web_net_id,num,amt)
                        status = "successful"

                elif net == '9MOBILE':
                        msorg_sendairtime(Network.objects.get(name=net).msorg_web_net_id,num,amt)
                        status = "successful"

            else:
                errors['error'] = u'Share and sell not available on this network currently'
                raise serializers.ValidationError(errors)
                

            serializer.save(Status=status, ident=ident, paid_amount=fund, medium='API',balance_before=previous_bal, balance_after=(previous_bal - amount))

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

