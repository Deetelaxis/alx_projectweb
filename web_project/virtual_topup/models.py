from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import requests
import datetime
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.db.models import Sum
from django.db import transaction
from django.utils import dateparse
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
import json


# Create your models here.
import random


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


User = settings.AUTH_USER_MODEL

Network_choice = (
    ('MTN', 'MTN'),
    ('GLO', 'GLO'),
    ('AIRTEL', 'AIRTEL'),
    ('9MOBILE', '9MOBILE'),
)

Airtime_choice = (
    ('100', '#100'),
    ('200', '#200'),
    ('400', '#400'),
    ('500', '#500'),
    ('1000', '#1000'),
)

services = (
    ('Data', 'Data'),
    ('Airtime', 'Airtime'),
    ('Cablesub', 'Cablesub'),
    ('Bill', 'Bill'),
    ('Bankpayment', 'Bankpayment'),
    ('Monnify ATM', 'Monnify ATM'),
    ('Monnfy bank', 'Monnify bank'),
)

airtime_type = (
    ('VTU', 'VTU'),
)

dataplan_type = (
    ('CORPORATE GIFTING', 'CORPORATE GIFTING'),
    ('GIFTING', 'GIFTING'),
    ('SME', 'SME'),
)

Volume_choice = (
    ('MB', 'MB'),
    ('GB', 'GB'),
    ('TB', 'TB'),
)

cable_choice = (
    ('GOTV', 'GOTV'),
    ('DSTV', 'DSTV'),
    ('STARTIME', 'STARTIME'),
)

ctype = (
    ('Prepaid', 'Prepaid'),
    ('Postpaid', 'Postpaid'),
)

api_medium = (
    ('SIMSERVER', 'SIMSERVER'),
    ('SMEPLUG', 'SMEPLUG'),
    ('SMS', 'SMS'),
    ('VTPASS', 'VTPASS'),
)

coperate_api_medium = (
    ('SMEPLUG', 'SMEPLUG'),
    ('CG_KONNECT', 'CG_KONNECT'),
    ('SMS', 'SMS'),
    ('UWS', 'UWS'),
    ('USSD', 'USSD'),
    )

users = (
    ("Smart Earner", "Smart Earner"),
)

status = (
    ('Pending', 'Pending'),
    ('Processing', 'processing'),
    ('Delivered', 'Delivered'),
)

def create_id():
    num = random.randint(100, 2000)
    num_2 = random.randint(1, 1000)
    num_3 = random.randint(60, 1000)
    return str(num) + str(num_2)+str(num_3)+str(uuid.uuid4())[:8]

    # +str(num_2)+str(num_3)+str(uuid.uuid4())[:7]
    
    class CustomUserManager(UserManager):
     def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})
    
    class CustomUser(AbstractUser):
    objects = CustomUserManager()
    email = models.EmailField()
    birth_date = models.DateField(blank=True,null=True)
    FullName = models.CharField(max_length=200,  null=True)
    Address = models.CharField(max_length=500,  null=True)
    BankName = models.CharField(max_length=100, choices=Bank, blank=True)
    AccountNumber = models.CharField(max_length=40, blank=True)
    Phone = models.CharField(max_length=30, blank=True)
    AccountName = models.CharField(max_length=200, blank=True)
    Account_Balance = models.FloatField(
        default=0.00, null=True, validators=[MinValueValidator(0.0)],)
    pin = models.CharField(null=True, blank=True, max_length=5)
    referer_username = models.CharField(max_length=50, blank=True, null=True)
    first_payment = models.BooleanField(default=False)
    Referer_Bonus = models.FloatField(
        default=0.00, null=True, validators=[MinValueValidator(0.0)],)
    user_type = models.CharField(
        max_length=30, choices=users, default="Smart Earner", null=True)
    reservedaccountNumber = models.CharField(
        max_length=100, blank=True, null=True)
    reservedbankName = models.CharField(max_length=100, blank=True, null=True)
    reservedaccountReference = models.CharField(max_length=100, blank=True, null=True)
    Bonus = models.FloatField(default=0.00, null=True, validators=[ MinValueValidator(0.0)],)
    verify = models.BooleanField(default=False)
    DOB = models.DateField(null=True,blank=True,)
    Gender = models.CharField(max_length=6, null=True,)
    State_of_origin = models.CharField(max_length=100, null=True,)
    Local_gov_of_origin = models.CharField(max_length=100, null=True,)
    BVN = models.CharField(max_length=50, null=True,)
    passport_photogragh = models.ImageField(upload_to="passport_images", null=True, help_text="Maximum of 50kb in size")
    accounts = models.TextField(blank=True,null=True)


def f_account(self):
        try:
            return json.loads(self.accounts)
        except:
            return {}


def _str_(self):
        return self.username


class Transactions(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    amount = models.FloatField()
    balance_before = models.FloatField(blank=True, null=True)
    balance_after = models.FloatField(blank=True, null=True)
    transaction_type = models.CharField(max_length=30, blank=True)
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'WALLET TRANSACTIONS'

    def __str__(self):
        return str(self.transaction_type)

    def today_credit_transaction(self):

        today = datetime.date.today()
        return Transactions.objects.filter(create_date__gt=today, transaction_type="CREDIT").aggregate(Sum('amount'))['amount__sum']

    def today_debit_transaction(self):
        today = datetime.date.today()
        return Transactions.objects.filter(create_date__gt=today, transaction_type="DEBIT").aggregate(Sum('amount'))['amount__sum']

    def this_month_credit_transaction(self):
        current_month = datetime.datetime.now().month
        return Transactions.objects.filter(create_date__month=current_month, transaction_type="CREDIT").aggregate(Sum('amount'))['amount__sum']

    def this_month_debit_transaction(self):
        current_month = datetime.datetime.now().month
        return Transactions.objects.filter(create_date__month=current_month, transaction_type="DEBIT").aggregate(Sum('amount'))['amount__sum']
    def total_credit_transaction(self):
        return Transactions.objects.filter(transaction_type="CREDIT").aggregate(Sum('amount'))['amount__sum']

    def total_debit_transaction(self):
        return Transactions.objects.filter(transaction_type="DEBIT").aggregate(Sum('amount'))['amount__sum']


class Wallet_summary(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE,
                             editable=False, blank=False, null=True, related_name='wallet')
    product = models.CharField(max_length=500, blank=True)
    amount = models.CharField(max_length=30, blank=True)
    previous_balance = models.CharField(max_length=30, blank=True)
    after_balance = models.CharField(max_length=30, blank=True, null=True)
    Status = models.CharField(
        max_length=30, choices=status, default='successful')
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        try:
            sendmail("Transaction Notification ",f"{product} \n Amount : {self.amount} \n Previous Balance : {self.previous_balance} \n New Balance: {self.after_balance} \n Date {self.create_date.strftime('%d, %b %Y') }", self.user.email, self.user.username)
        except:
            pass
        super(Wallet_summary, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'USERS WALLET SUMMARY'
        
        class Airtime(models.Model):

    user = models.ForeignKey(
        users, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    network = models.ForeignKey(Network_choice, on_delete=models.SET_NULL, null=True)
    pin = models.CharField(max_length=30, blank=True)
    amount = models.CharField(
        max_length=30, choices=Airtime_choice, default='#100')
    Receivece_amount = models.FloatField(null=True)
    Status = models.CharField(
        max_length=30, choices=status, default='processing')
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    fund = models.BooleanField(default=False, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('airtime_success', args=[str(self.id)])

    def __str__(self):
        return self.Status

    def save(self, *args, **kwargs):
        if self.Status == 'successful' and self.fund == False:
            previous_bal = self.user.Account_Balance
            self.user.deposit(self.user.id, self.user.id,
                              float(self.Receivece_amount),False,"AIRTIME WALLET FUNDING")
            self.fund = True
            Wallet_summary.objects.create(user=self.user, product="Airtime  pin Funding", amount=self.Receivece_amount,
                                          previous_balance=previous_bal, after_balance=(previous_bal - float(self.Receivece_amount)))

        super(Airtime, self).save(*args, **kwargs)


class Recharge(models.Model):
    network = models.ForeignKey(Network_choice, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    amount = models.FloatField(default=0)
    amount_to_pay = models.FloatField(default=0)
    Affilliate_price = models.FloatField(default=100)
    TopUser_price = models.FloatField(default=100)
    api_price = models.FloatField(default=100)

def __str__(self):
        return str(self.amount_to_pay)

def netname(self):
        return str(self.network.name)


class Data(models.Model):
    user = models.ForeignKey(
        users, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    network = models.ForeignKey(Network_choice, on_delete=models.SET_NULL, null=True)
    plan = models.ForeignKey(Volume_choice, on_delete=models.SET_NULL, null=True)
    data_type = models.CharField(max_length = 30, choices=dataplan_type,blank=True,null=True,help_text="Select Plan Type SME or GIFTING or CORPORATE GIFTING")
    mobile_number = models.CharField(max_length=30, blank=True)
    Status = models.CharField(max_length=30, choices=status, default='processing',
                              help_text="Select failed and save to refund user")
    medium = models.CharField(max_length=30, default='website')
    create_date = models.DateTimeField(default=timezone.now)
    balance_before = models.CharField(max_length=30, blank=True)
    balance_after = models.CharField(max_length=30, blank=True, null=True)
    plan_amount = models.CharField(max_length=30, blank=True)
    Ported_number = models.BooleanField(default=False, blank=True, null=True)
    ident = models.CharField(default=create_id, editable=False, max_length=300)
    refund = models.BooleanField(default=False, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'DATA TOP-UP TRANSACTIONS'

    def __str__(self):
        return str(self.plan)

    def data_amount(self):
        return str(self.plan_amount)

    def save(self, *args, **kwargs):

        # previous_bal = self.user.Account_Balance

        # if self.Status != 'successful' and self.refund == False:
        if self.Status == 'failed' and self.refund == False:
            previous_bal = float(self.user.Account_Balance) - float(self.plan_amount)
            after_bal = self.user.Account_Balance

            self.user.deposit(self.user.id, float(self.plan_amount),False ,"FAILED DATA TOPUP REFUND")
            self.refund = True

            Wallet_summary.objects.create(user=self.user, product="FAILED DATA TOPUP REFUND for {} {}{}   N{}  with {} ".format(self.network.name, self.plan.plan_size, self.plan.plan_Volume,  self.plan_amount, self.mobile_number), amount=self.plan_amount, previous_balance=previous_bal, after_balance=after_bal)

            # Wallet_summary.objects.create(user=self.user, product="{} {}{}   N{}  DATA topup Refund for {} ".format(self.network.name, self.plan.plan_size, self.plan.plan_Volume,  self.plan_amount, self.mobile_number), amount=self.plan_amount, previous_balance=previous_bal, after_balance=(previous_bal + float(self.plan_amount)))

        super(Data, self).save(*args, **kwargs)

def get_absolute_url(self):
        return reverse('Data_success', args=[str(self.id)])


class AirtimeTopup(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    network = models.ForeignKey(Network_choice, on_delete=models.SET_NULL, null=True)
    mobile_number = models.CharField(max_length=30, blank=True)
    airtime_type = models.CharField(
        max_length=30, choices=airtime_type, default='VTU', help_text="VTU or share and Sell")
    amount = models.CharField(max_length=30, blank=True)
    paid_amount = models.CharField(max_length=30, blank=True)
    Status = models.CharField(max_length=30, choices=status, default='processing',
                              help_text="Select failed and save to refund user")
    create_date = models.DateTimeField(default=timezone.now)
    balance_before = models.CharField(max_length=30, blank=True)
    balance_after = models.CharField(max_length=30, blank=True)
    Ported_number = models.BooleanField(default=False, blank=True, null=True)
    medium = models.CharField(max_length=30, default='website')
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    refund = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.mobile_number
    
    def get_absolute_url(self):
        return reverse('AirtimeTopup_success', args=[str(self.id)])

    def plan_net(self):
        return str(self.network)

    def plan_amt(self):
        return "N"+str(self.amount)

    def save(self, *args, **kwargs):

        if self.Status == 'failed' and self.refund == False:
            previous_bal = self.user.Account_Balance
            self.user.deposit(self.user.id, float(self.paid_amount),False ,"AIRTIME TOPUP Refund")
            self.refund = True
            Wallet_summary.objects.create(user=self.user, product="{} {} Airtime topup Refund for {} ".format(
                self.network.name, self.amount, self.mobile_number), amount=self.paid_amount, previous_balance=previous_bal, after_balance=(previous_bal + float(self.paid_amount)))

        super(AirtimeTopup, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'AIRTIME TOPUP TRANSACTIONS'

class PinCode(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    pin = models.IntegerField(unique=True)

    def get_absolute_url(self):
        return reverse('Transfer_detail', args=[str(self.id)])
    
    class Bankpayment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)

    Bank_paid_to = models.CharField(max_length=15, blank=True, null=True)
    Reference = models.CharField(max_length=15, blank=True, null=True)
    amount = models.CharField(max_length=30, blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    Status = models.CharField(
        max_length=30, choices=status, default='processing')
    fund = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('Banksuccess', args=[str(self.id)])

    def save(self, *args, **kwargs):
        amount = self.amount
        if self.Status == 'successful' and self.fund == False:
            previous_bal = self.user.Account_Balance

            self.user.deposit(self.user.id, float(amount),False ,"Manual Bank Funding")
            self.fund = True
            Wallet_summary.objects.create(user=self.user, product="Manual Bank Funding", amount=amount,
                                          previous_balance=previous_bal, after_balance=(previous_bal + float(amount)))
            
        super(Bankpayment, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'MANUAL BANK FUNDING'

class paymentgateway(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    reference = models.CharField(null=True, blank=True, max_length=50)
    amount = models.FloatField(blank=True, null=True)
    Status = models.CharField(
        max_length=30, choices=status, default='processing')
    gateway = models.CharField(max_length=30, default="Paystack")
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = 'PAYMENT GATEWAY TRANSACTIONS'


class Cable(models.Model):
    name = models.CharField(max_length=30, choices=cable_choice, unique=True)
    status = models.CharField(max_length=30, choices=status)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'CABLE COMPANY'
        
        class CablePlan(models.Model):
    cablename = models.ForeignKey(Cable, on_delete=models.CASCADE)
    plan_amount = models.PositiveIntegerField()
    product_code = models.CharField(max_length=200, blank=True, null=True)
    package = models.CharField(
        max_length=200, help_text="package(ie GOTV Plus)")
    hasAddon = models.BooleanField(default=False)
    Addon_name = models.CharField(
        max_length=200, help_text="package(ie Asian Add-on)", blank=True, null=True)
    addoncode = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.package) + str(self.Addon_name) + '----' + '#' + str(self.plan_amount)

    def plan_name(self):
        return str(self.package)

    def cableplanname(self):
        return str(self.cablename)

    def plan_amt(self):
        return str(self.plan_amount)

    def plan_id(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'CABLE SUBSCRIPTION PLAN'
        
        
        class Cablesub(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    cablename = models.ForeignKey(Cable, on_delete=models.SET_NULL, null=True)
    cableplan = models.ForeignKey(
        CablePlan, on_delete=models.SET_NULL, null=True)
    smart_card_number = models.CharField(max_length=30, blank=True)
    balance_before = models.CharField(max_length=30, blank=True)
    balance_after = models.CharField(max_length=30, blank=True)
    plan_amount = models.CharField(max_length=30, blank=True)
    Status = models.CharField(max_length=30, choices=status, default='processing',
                              help_text="Select failed and save to refund user")
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    refund = models.BooleanField(default=False, blank=True, null=True)
    customer_name = models.CharField(max_length=70, blank=True, null=True)

    def __str__(self):
        return str(self.cableplan)

    def get_absolute_url(self):
        return reverse('cablesub_success', args=[str(self.id)])

    def save(self, *args, **kwargs):
        
        if self.Status == 'failed' and self.refund == False:
            previous_bal = self.user.Account_Balance
            self.user.deposit(self.user.id, float(self.plan_amount),False ,"Cablesub Refund")
            self.refund = True
            Wallet_summary.objects.create(user=self.user, product="{} N{} Cablesub Refund for {} ".format(self.cableplan.package, self.plan_amount,
                                                                                                          self.smart_card_number), amount=self.plan_amount, previous_balance=previous_bal, after_balance=(previous_bal + float(self.plan_amount)))

        super(Cablesub, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'CABLE SUBSCRIPTION TRANSACTIONS'
        
        
        class Billpayment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    disco_name = models.ForeignKey(
        cable_provider_name, on_delete=models.SET_NULL, null=True)
    amount = models.CharField(max_length=30)
    paid_amount = models.CharField(max_length=30, blank=True)
    balance_before = models.CharField(max_length=30, blank=True)
    balance_after = models.CharField(max_length=30, blank=True)
    meter_number = models.CharField(max_length=30, blank=True)
    token = models.CharField(max_length=200, blank=True, null=True)
    Customer_Phone = models.CharField(max_length=15, null=True)
    MeterType = models.CharField(max_length=30, choices=ctype, null=True)
    Status = models.CharField(max_length=30, choices=status, default='processing',
                              help_text="Select failed and save to refund user")
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    refund = models.BooleanField(default=False, blank=True, null=True)
    customer_name = models.CharField(max_length=250, blank=True, null=True)
    customer_address = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.disco_name)

    def get_absolute_url(self):
        return reverse('bill_success', args=[str(self.id)])
    
    def save(self, *args, **kwargs):

        if self.Status == 'failed' and self.refund == False:
            previous_bal = self.user.Account_Balance
            self.user.deposit(self.user.id, float(self.amount),False ,"Bill Payment Refund")
            self.refund = True
            Wallet_summary.objects.create(user=self.user, product="{} {}Bill Payment Refund for {} ".format(
                self.disco_name.name, self.amount, self.meter_number), amount=self.amount, previous_balance=previous_bal, after_balance=(previous_bal + float(self.amount)))

        elif self.token:

                def sendmessage(sender,message,to,route):
                             payload={
                                'sender':sender,
                                'to': to,
                                'message': message,
                                'type': '0',
                                'routing':route,
                                'token':'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
                                'schedule':'',
                                    }

                             baseurl = 'https://sms.hollatags.com/api/send/?user=oluwole1&pass=Pstsegunsss@c1&to={0}&from={1}&msg={2}'.format(to,sender,message)
                             response = requests.get(baseurl,verify=False)
                             
                             sendmessage('BILLTOKEN', "From datavilla your Bill Token is {0} ".format(
                    self.token), self.Customer_Phone, "02")

        super(Billpayment, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'BILL PAYMENT TRANSACTIONS'














