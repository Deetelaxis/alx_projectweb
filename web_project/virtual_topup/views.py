# views.py in your Dja

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
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.utils.timezone import datetime as datetimex
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
from .models import Couponcode, CustomUser
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
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token


def sendmail(subject, message, user_email, username):
    ctx = {
        'message': message,
        "subject": subject,
        "username": username
    }
    message = get_template('email.html').render(ctx)
    msg = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()



def create_id():
        num = random.randint(1,10)
        num_2 = random.randint(1,10)
        num_3 = random.randint(1,10)
        return str(num_2)+str(num_3)+str(uuid.uuid4())

ident = create_id()

class referralView(TemplateView):
    template_name = 'referral.html'

    def get_context_data(self, **kwargs):

        context = super(referralView, self).get_context_data(**kwargs)
        context['referral'] = Referral_list.objects.filter(
            user=self.request.user)
        context['referal_total'] = Referral_list.objects.filter(
            user=self.request.user).count()

        return context
    
def monnifypage(request):

    return render(request, "bankpage.html", context={"bankname": request.user.reservedbankName, "banknumber": request.user.reservedaccountNumber})


class Wallet_Summary(TemplateView):
    template_name = 'wallet.html'

    def get_context_data(self, **kwargs):
        context = super(Wallet_Summary, self).get_context_data(**kwargs)
        context['wallet'] = Wallet_summary.objects.filter(user=self.request.user).order_by('-create_date')[:2000]

        return context
    
    
    class UserHistory(TemplateView):
    template_name = 'user_history.html'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q')

        if CustomUser.objects.filter(username__iexact=query).exists():
            user_h = CustomUser.objects.get(username__iexact=query)
            context = super(UserHistory, self).get_context_data(**kwargs)
            context['user'] = user_h
            context['airtime'] = Airtime.objects.filter(
                user=user_h).order_by('-create_date')
            context['withdraw'] = Withdraw.objects.filter(
                user=user_h).order_by('-create_date')
            context['data'] = Data.objects.filter(
                user=user_h).order_by('-create_date')
            context['airtimeswap'] = Airtimeswap.objects.filter(
                user=user_h).order_by('-create_date')
            context['airtimeTopup'] = AirtimeTopup.objects.filter(
                user=user_h).order_by('-create_date')
            context['Cablesub'] = Cablesub.objects.filter(
                user=user_h).order_by('-create_date')
            context['bank'] = Bankpayment.objects.filter(
                user=user_h).order_by('-create_date')
            context['bill'] = Billpayment.objects.filter(
                user=user_h).order_by('-create_date')
            context['paystact'] = paymentgateway.objects.filter(
                user=user_h).order_by('-created_on')

            return context
        
def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
# def sendmessage(sender, message, to, route):
#     payload = {
#         'sender': sender,
#         'to': to,
#         'message': message,
#         'type': '0',
#                 'routing': route,
#                 'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
#                 'schedule': '',
#     }

#     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
#     response = requests.get(baseurl, verify=False)


class ApiDoc(TemplateView):
    template_name = 'swagger-ui.html'

    def get_context_data(self, **kwargs):
        context = super(ApiDoc, self).get_context_data(**kwargs)
        context['plans'] = Plan.objects.all()
        context['network'] = Network.objects.all()
        context['cableplans'] = CablePlan.objects.all()
        context['cable'] = Cable.objects.all()
        context['disco'] = Disco_provider_name.objects.all()

        if Token.objects.filter(user=self.request.user).exists():
            context['token'] = Token.objects.get(user=self.request.user)
        else:
            Token.objects.create(user=self.request.user)
            context['token'] = Token.objects.get(user=self.request.user)

        return context
    
    
class ApiDoc(TemplateView):
    template_name = 'swagger-ui.html'

    def get_context_data(self, **kwargs):
        context = super(ApiDoc, self).get_context_data(**kwargs)
        context['plans'] = Plan.objects.all()
        context['network'] = Network.objects.all()
        context['cableplans'] = CablePlan.objects.all()
        context['cable'] = Cable.objects.all()
        context['disco'] = Disco_provider_name.objects.all()

        if Token.objects.filter(user=self.request.user).exists():
            context['token'] = Token.objects.get(user=self.request.user)
        else:
            Token.objects.create(user=self.request.user)
            context['token'] = Token.objects.get(user=self.request.user)

        return context
    
    
class WelcomeView(TemplateView):
    template_name = 'index.html'

    def referal_user(self):
        if self.request.GET.get("referal"):
            self.request.session["referal"] = self.request.GET.get("referal")
            #print(self.request.session["referal"])
            #print("sessin set")

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
        context['book1'] = Book.objects.all().order_by('-created_at')[:10]
        context['book2'] = Book.objects.all().order_by('-created_at')[:6]
        context['post_list1'] = Post.objects.all().order_by('-created_on')[:10]
        context['ref'] = self.referal_user()

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
        total_bonus = CustomUser.objects.all().aggregate(
             Sum('Referer_Bonus'))['Referer_Bonus__sum']
        bill_obj = Billpayment.objects.filter(
            create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        cable_obj = Cablesub.objects.filter(create_date__month=current_month).aggregate(
            Sum('plan_amount'))['plan_amount__sum']
        Topup_obj1 = AirtimeTopup.objects.filter(
            network=net, create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        Topup_obj2 = AirtimeTopup.objects.filter(
            network=net_2, create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        Topup_obj3 = AirtimeTopup.objects.filter(
            network=net_3, create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        Topup_obj4 = AirtimeTopup.objects.filter(
            network=net_4, create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        bank_obj = Bankpayment.objects.filter(
            Status="successful", create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        atm_obj = paymentgateway.objects.filter(
            Status="successful", created_on__month=current_month).aggregate(Sum('amount'))['amount__sum']
        pin_obj = Airtime.objects.filter(
            Status="successful", create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        
        try:
            def create_id():
                num = random.randint(1, 10)
                num_2 = random.randint(1, 10)
                num_3 = random.randint(1, 10)
                return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]

            body = {
                "accountReference": create_id(),
                "accountName": self.request.user.username,
                "currencyCode": "NGN",
                "contractCode": f"{config.monnify_contract_code}",
                "customerEmail": self.request.user.email,
                "incomeSplitConfig": [],
                "restrictPaymentSource": False,
                "allowedPaymentSources": {},
                "customerName": self.request.user.username,
                "getAllAvailableBanks": True,
            }

            # if not self.request.user.reservedaccountNumber:
            if not self.request.user.accounts:

                data = json.dumps(body)
                ad = requests.post("https://api.monnify.com/api/v1/auth/login", auth=HTTPBasicAuth(f'{config.monnify_API_KEY}', f'{config.monnify_SECRET_KEY}'))
                mydata = json.loads(ad.text)

                headers = {'Content-Type': 'application/json',
                            "Authorization": "Bearer {}" .format(mydata['responseBody']["accessToken"])}
                ab = requests.post(
                    "https://api.monnify.com/api/v2/bank-transfer/reserved-accounts", headers=headers, data=data)

                mydata = json.loads(ab.text)


                user = self.request.user

                user.reservedaccountNumber = mydata["responseBody"]["accounts"][0]["accountNumber"]
                user.reservedbankName = mydata["responseBody"]["accounts"][0]["bankName"]
                user.reservedaccountReference = mydata["responseBody"]["accountReference"]
                user.accounts = json.dumps({"accounts":mydata["responseBody"]["accounts"]})
                user.save()


                # user = self.request.user

                # user.reservedaccountNumber = mydata["responseBody"]["accountNumber"]
                # user.reservedbankName = mydata["responseBody"]["bankName"]
                # user.reservedaccountReference = mydata["responseBody"]["accountReference"]
                # user.save()

            else:
                pass
        except:
            pass


        context = super(Profile, self).get_context_data(**kwargs)
        context['airtime'] = Airtime.objects.filter(
            Status='processing').count()
        context['withdraw'] = Withdraw.objects.filter(
            Status='processing').count()
        context['data'] = Data.objects.filter(Status='processing').count()
        context['airtimeswap'] = Airtimeswap.objects.filter(
            Status='processing').count()
        context['airtimeTopup'] = AirtimeTopup.objects.filter(
            Status='processing').count()
        context['transfer'] = Transfer.objects.filter(
            Status='processing').count()
        context['Airtime_funding'] = Airtime_funding.objects.filter(
            Status='processing').count()
        context['CouponPayment'] = CouponPayment.objects.filter(
            Status='processing').count()
        context['unusedcoupon'] = Couponcode.objects.filter(Used=False).count()
        context['usedcoupon'] = Couponcode.objects.filter(Used=True).count()
        context['bank'] = Bankpayment.objects.filter(
            Status='processing').count()
        context['cable'] = Cablesub.objects.filter(Status='processing').count()
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
        context['banktotal'] = bank_obj
        context['atmtotal'] = atm_obj
        context['coupontotal'] = coupon_obj
        context['airtimetotal'] = pin_obj
        context['Noti'] = self.request.user.notifications.all()[:1]
        context['twallet'] = round(total_wallet, 2)
        context['tbonus'] = round(total_bonus, 2)
        context['alert'] = Info_Alert.objects.all()[:1]
        context['transactions'] = Transactions.objects.all()[:1]
        context['wallet'] = Wallet_summary.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['users'] = CustomUser.objects.all().count()
        context['referral'] = Referal_list.objects.filter(
            user=self.request.user).all().count()
        context['Billpayment_obj'] = bill_obj
        context['cable'] = cable_obj
        context['AirtimeTopup_obj'] = Topup_obj1
        context['AirtimeTopup_obj2'] = Topup_obj2
        context['AirtimeTopup_obj3'] = Topup_obj3
        context['AirtimeTopup_obj4'] = Topup_obj4

        context["verify"] = KYC.objects.filter(user = self.request.user).last()

        return context
    
    
    
    def monnify_payment(request):
    if request.method == 'POST':
        form = monnify_payment_form(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            username = request.user.username
            email = request.user.email
            phone = request.user.Phone

            amount = ((amount) + (0.015 * amount))

            headers = {'Content-Type': 'application/json', }

            def create_id():
                num = random.randint(1, 10)
                num_2 = random.randint(1, 10)
                num_3 = random.randint(1, 10)
                return str(num_2)+str(num_3)+str(uuid.uuid4())

            ab = {
                "amount": amount,
                "customerName": username,
                "customerEmail": email,
                "paymentReference": create_id(),
                "paymentDescription": "Wallet Funding",
                "currencyCode": "NGN",
                "contractCode": f"{config.monnify_contract_code}",
                "paymentMethods": ["CARD"],
                 "redirectUrl": "https://www.virtualtopup.com/profile",
                "incomeSplitConfig": []
                
                }
            data = json.dumps(ab)

            response = requests.post('https://api.monnify.com/api/v1/merchant/transactions/init-transaction',
                                     headers=headers, data=data, auth=HTTPBasicAuth(f'{config.monnify_API_KEY}', f'{config.monnify_SECRET_KEY}'))

            loaddata = json.loads(response.text)
            url = loaddata["responseBody"]["checkoutUrl"]

            #print(username, email, phone)

            return HttpResponseRedirect(url)

    else:
        form = monnify_payment_form()

    return render(request, 'monnify.html', {'form': form})

@require_POST
@csrf_exempt
# @require_http_methods(["GET", "POST"])
def monnify_payment_done(request):

    #secret = b'sk_live_627a99148869d929fdad838a74996891f5b660b5'
    payload = request.body

    forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))

    dat = json.loads(payload)
    a = "{}|{}|{}|{}|{}".format(config.monnify_SECRET_KEY,
                                dat["paymentReference"], dat["amountPaid"], dat["paidOn"], dat["transactionReference"])
    #print(forwarded_for)
    c = bytes(a, 'utf-8')
    hashkey = hashlib.sha512(c).hexdigest()
    if hashkey == dat["transactionHash"] and forwarded_for == "35.242.133.146":
        #print("correct")
        #print("IP whilelisted")
        response = requests.get("https://api.monnify.com/api/v1/merchant/transactions/query?paymentReference={}".format(
            dat["paymentReference"]), auth=HTTPBasicAuth(f'{config.monnify_API_KEY}', f'{config.monnify_SECRET_KEY}'))
        #print(response.text)
        ab = json.loads(response.text)

        if (response.status_code == 200 and ab["requestSuccessful"] == True) and (ab["responseMessage"] == "success" and ab["responseBody"]["paymentStatus"] == "PAID"):
            user = dat["customer"]["email"]
            mb = CustomUser.objects.get(email__iexact=user)
            amount = (ab['responseBody']['amount'])
            fee = (ab['responseBody']['fee'])
            
        if ab['responseBody']["paymentMethod"] == "CARD":
                paynow = (round(amount - fee))

        else:
                paynow = (round(amount - 50))
        ref = dat["paymentReference"]
            #print("hoooooook paid")

        if not paymentgateway.objects.filter(reference=ref).exists():
                try:
                    previous_bal = mb.Account_Balance
                    mb.deposit(mb.id, paynow,False ,"Monnify Funding")
                    paymentgateway.objects.create(
                        user=mb, reference=ref, amount=paynow, Status="successful", gateway="monnify")
                    Wallet_summary.objects.create(user=mb, product=" N{} Monnify Funding ".format(
                        paynow), amount=paynow, previous_balance=previous_bal, after_balance=(previous_bal + paynow))
                    notify.send(
                        mb, recipient=mb, verb='Monnify Payment successful you account has been credited with sum of #{}'.format(paynow))
                except:
                    return HttpResponse(status=200)
                else:
                    pass
                
        else:
            messages.error(
                request, 'Our payment gateway return Payment tansaction failed status {}'.format(ab["message"]))
            
    else:
        return HttpResponseForbidden('Permission denied.')
        #print("after monnify hook")
        return HttpResponse(status=200)

class HomeView(generic.DetailView):
    model = CustomUser
    template_name = 'detail.html'
    slug_field = "username"


class AirlisView(generic.ListView):

    template_name = 'airtime_success.html'
    context_object_name = 'Airtime_funding_list'

    def get_queryset(self):
        return Airtime_funding.objects.all()
        
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        #print(uid)
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')

        return redirect('profile')

    else:
        return HttpResponse('Activation link is invalid!')
    
    class SignUp(SuccessMessageMixin, generic.CreateView):
       form_class = CustomUserCreationForm
       success_url = reverse_lazy('login')
       template_name = 'signup.html'
       success_messages = 'Please confirm your email address to complete the registration,activation link has been sent to your email, also check your email spam folder'

    def abc(self):
        ref = ""
        if "referral" in self.request.session:
            ref = (self.request.session["referral"])

        return ref
    
    def get_context_data(self, **kwargs):

        context = super(SignUp, self).get_context_data(**kwargs)
        context['referal_user'] = self.abc()

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        username = object.username
        email = object.email
        object.is_active = False
        user = object
        
        if CustomUser.objects.filter(username__iexact=object.username).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This username has been taken'])
            return self.form_invalid(form)

        elif CustomUser.objects.filter(email__iexact=object.email).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This email has been taken'])
            return self.form_invalid(form)
        elif CustomUser.objects.filter(Phone__iexact=object.Phone).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This Phone has been taken'])
            return self.form_invalid(form)

        elif not object.email.endswith(("@gmail.com",'@yahoo.com')):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList([u'We accept only valid gmail or yahoo mail account'])
            return self.form_invalid(form)

        elif object.referer_username:
            if CustomUser.objects.filter(username__iexact=object.referer_username).exists():
                referal_user = CustomUser.objects.get(
                    username__iexact=object.referer_username)
            else:
                object.referer_username = None
                
        form.save()
            
    try:
                    
                    current_site = get_current_site(self.request)
                    mail_subject = 'Activate your virtualtopup account.'
                    message =  {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':account_activation_token.make_token(user),
                }
                    message = get_template('acc_active_email.html').render(message)
                    to_email = email
                    email = EmailMessage(mail_subject, message, to=[to_email] )
                    email.content_subtype = "html"
                    email.send()
                
    except:
              pass
    try:
                   Referal_list.objects.create(user=referal_user, username=username)
    except:
              pass
    try:

                  messages.success( self.request, 'Please confirm your email address to complete the registration,activation link has been sent to your email,, also check your email spam folder')

                  sendmail("Welcome to virtualtopup.com", "Welcome to virtualtopup.com ,We offer instant recharge of Airtime, Databundle, CableTV (DStv, GOtv & Startimes), Electricity Bill Payment and Airtime to Cash.", email, username)
                 
    except:
            pass
    try:

            def create_id():
                num = random.randint(1, 10)
                num_2 = random.randint(1, 10)
                num_3 = random.randint(1, 10)
                return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]  
            
            body = {
                "accountReference": create_id(),
                "accountName": username,
                "currencyCode": "NGN",
                "contractCode": f"{config.monnify_contract_code}",
                "customerEmail": email,
                "incomeSplitConfig": [],
                "restrictPaymentSource": False,
                "allowedPaymentSources": {}
            }
            if not email:

                data = json.dumps(body)
                ad = requests.post("https://api.monnify.com/api/v1/auth/login", auth=HTTPBasicAuth(
                    f'{config.monnify_API_KEY}', f'{config.monnify_SECRET_KEY}'))
                mydata = json.loads(ad.text)

                headers = {'Content-Type': 'application/json',
                           "Authorization": "Bearer {}" .format(mydata['responseBody']["accessToken"])}
                ab = requests.post(
                    "https://api.monnify.com/api/v1/bank-transfer/reserved-accounts", headers=headers, data=data)

                mydata = json.loads(ab.text)

                user = CustomUser.objects.get(email__iexact=email)

                user.reservedaccountNumber = mydata["responseBody"]["accountNumber"]
                user.reservedbankName = mydata["responseBody"]["bankName"]
                user.reservedaccountReference = mydata["responseBody"]["accountReference"]
                user.save()

            else:
                pass
            
    except:
            pass
    return super(SignUp, self).form_valid(form)

class UserEdit(generic.UpdateView):
    form_class = CustomUserChangeForm
    models = CustomUser
    success_url = reverse_lazy('userdetails')
    template_name = 'Editprofile.html'
    context_object_name = 'Edit'

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.id)

    def get_queryset(self):
        return CustomUser.objects.all()
    
    class BankpaymentCreate(generic.CreateView):
      form_class = Bankpaymentform
    template_name = 'bank_form.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user

        if float(object.amount) < 1000:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Minimun deposit is #1000'])
            return self.form_invalid(form)
        sendmessage('Msorg', "{0} want to fund his/her account with  bank payment  amount:{1} https://www.Husmodata.com/page-not-found-error/page/vtuapp/bankpayment/".format(
            object.user.username, object.amount), '2348166171824', '2')

        form.save()

        return super(BankpaymentCreate, self).form_valid(form)


def create_id():
    num = random.randint(1, 10)
    num_2 = random.randint(1, 10)
    num_3 = random.randint(1, 10)
    return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]

class airtimeCreate(generic.CreateView):
    form_class = airtimeform
    template_name = 'airtime_form.html'

    def get_context_data(self, **kwargs):

        context = super(airtimeCreate, self).get_context_data(**kwargs)
        context['mtn'] = Percentage.objects.get(
            network=Network.objects.get(name="MTN")).percent
        context['glo'] = Percentage.objects.get(
            network=Network.objects.get(name="GLO")).percent
        context['mobie'] = Percentage.objects.get(
            network=Network.objects.get(name="9MOBILE")).percent
        context['airtel'] = Percentage.objects.get(
            network=Network.objects.get(name="AIRTEL")).percent

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        net = str(object.network)
        amt = float(object.amount)
        
        def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
        # def sendmessage(sender, message, to, route):
        #     payload = {
        #         'sender': sender,
        #         'to': to,
        #         'message': message,
        #         'type': '0',
        #         'routing': route,
        #         'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
        #         'schedule': '',
        #     }

        #     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
        #     response = requests.get(baseurl, verify=False)
        
        if net == 'MTN' and (len(object.pin) < 16 or len(object.pin) > 17):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Invalid MTN card pin '])
            return self.form_invalid(form)

        elif net == '9MOBILE' and (len(object.pin) < 16 or len(object.pin) > 17):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Invalid 9MOBILE card pin'])
            return self.form_invalid(form)

        elif net == 'GLO' and (len(object.pin) < 16 or len(object.pin) > 17):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Invalid GLO card pin'])
            return self.form_invalid(form)

        elif net != 'MTN' and (amt == 400.0):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'#400 airtime only available for MTN'])
            return self.form_invalid(form)

        elif net == 'AIRTEL' and (len(object.pin) < 16 or len(object.pin) > 17):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Invalid AIRTEL card pin'])
            return self.form_invalid(form)
        
        elif net == 'MTN':
            perc = Percentage.objects.get(id=1)
            object.Receivece_amount = float(
                object.amount) * int(perc.percent)/100

        elif net == 'GLO':
            perc = Percentage.objects.get(id=2)
            object.Receivece_amount = float(
                object.amount) * int(perc.percent)/100

        elif net == '9MOBILE':
            perc = Percentage.objects.get(id=3)
            object.Receivece_amount = float(
                object.amount) * int(perc.percent)/100

        elif net == 'AIRTEL':
            perc = Percentage.objects.get(id=4)
            object.Receivece_amount = float(
                object.amount) * int(perc.percent)/100

        sendmessage('deetel', "{0} want to fund his/her account with airtime pin:{1} network: {2} amount:{3} https://www.virtual.com/page-not-found-error/page/vtuapp/airtime/".format(
            object.user.username, object.pin, object.network, object.amount), '2348166171824', '2')

        form.save()
        
        return super(airtimeCreate, self).form_valid(form)
    
    class airtime_success(generic.DetailView):
    model = Airtime
    template_name = 'Airtime_suc.html'
    queryset = Airtime.objects.all()
    context_object_name = 'Airtime_success'

    def get_context_data(self, **kwargs):

        context = super(airtime_success, self).get_context_data(**kwargs)
        context['net'] = Network.objects.get(name='MTN')
        context['net_2'] = Network.objects.get(name='GLO')
        context['net_3'] = Network.objects.get(name='9MOBILE')
        context['net_4'] = Network.objects.get(name='AIRTEL')
        return context