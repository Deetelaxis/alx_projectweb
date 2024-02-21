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
from django.core import serializers as seria2
from colorfield.fields import ColorField
import urllib.parse
import base64


# Create your models here.
import random


User = settings.AUTH_USER_MODEL

status = (
    ('processing', 'processing'),
    ('failed', 'Failed'),
    ('successful', 'Successful'),
)

Netstatus = (
    ('Fair', 'Fair'),
    ('Bad', 'Bad'),
    ('Strong', 'Strong'),

)


plan_type = (
    ('CORPORATE', 'CORPORATE'),
    ('GIFTING', 'GIFTING'),
    ('SME', 'SME'),

)


Netchoice = (
    ('MTN', 'MTN'),
    ('GLO', 'GLO'),
    ('AIRTEL', 'AIRTEL'),
    ('9MOBILE', '9MOBILE'),

)

airtype = (
    ('VTU', 'VTU'),
    ('Share and Sell', 'Share and Sell'),

)

Volchoice = (
    ('MB', 'MB'),
    ('GB', 'GB'),
)

user_t = (
    ("Beginner", "Beginner"),
)


def create_id():
    num = random.randint(100, 2000)
    num_2 = random.randint(1, 1000)
    num_3 = random.randint(60, 1000)
    return str(num) + str(num_2)+str(num_3)+str(uuid.uuid4())[:8]


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    email = models.EmailField()
    Account_Balance = models.FloatField(
        default=0.00, null=True, validators=[MinValueValidator(0.0)],)
    user_type = models.CharField(max_length=30, choices=user_t, default="Beginner", null=True)


    def __str__(self):
        return self.username

    def walletb(self):
         return  str(round(self.Account_Balance))

    @classmethod
    def withdraw(cls, id, amount):
        with transaction.atomic():
            account = (cls.objects.select_for_update().get(id=id))
            print(account)
            balance_before = account.Account_Balance
            if account.Account_Balance < amount or amount < 0:
                return False
            account.Account_Balance -= amount
            account.save()


    @classmethod
    def deposit(cls, id, amount, transfer=False,medium = "NONE" ):
        with transaction.atomic():
            account = (cls.objects.select_for_update().get(id=id))
           

            balance_before = account.Account_Balance
            if medium != "NONE" : 

                  account.Account_Balance += amount
                  account.save()
                    
            

        return account  

    class Meta:
        verbose_name_plural = 'USERS MANAGEMENT'


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        User,
        related_name="logged_in_user",
        on_delete=models.CASCADE,
    )
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Wallet_summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
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
      
        super(Wallet_summary, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'USERS WALLET SUMMARY'


class Network(models.Model):
    name = models.CharField(max_length=30, choices=Netchoice, unique=True)
    msorg_web_net_id = models.CharField(max_length=5, null=True)
    airtime_disable = models.BooleanField(default=False, blank=True, null=True)
    data_disable = models.BooleanField(default=False, blank=True, null=True)
    

    def __str__(self):
        return str(self.name)
    
    def net_id(self):
        return str(self.id)
    
    class Meta:
        verbose_name_plural = 'NETWORKS'


class Plan(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    plan_size = models.FloatField()
    plan_Volume = models.CharField(max_length=30, choices=Volchoice)
    plan_amount = models.PositiveIntegerField()
   
    plan_name_id = models.CharField(max_length=500, null=True, blank=True)
    plan_type = models.CharField(
        max_length=30, choices=plan_type, blank=True, help_text="Data plan  type only .")
    month_validate = models.CharField(max_length=30)


    def __str__(self):
        return str(self.plan_size) + str(self.plan_Volume) + '----' + 'N' + str(self.plan_amount)

    def plan_name(self):
        return str(self.plan_size) + str(self.plan_Volume)

    def plan_net(self):
        return str(self.network)

    def plan_amt(self):
        return str(self.plan_amount)

    def plan_id(self):
        return str(self.id)
    
    class Meta:
        verbose_name_plural = 'DATA PLANS'


class TopupPercentage(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    percent = models.IntegerField()
    share_n_sell_percent = models.IntegerField(default=100)

    class Meta:
        verbose_name_plural = 'AIRTIME TOPUP PERCENTAGE'

    def __str__(self):
        return str(self.network) + "-----" + str(self.percent)

class Data(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    network = models.ForeignKey(Network, on_delete=models.SET_NULL, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    data_type = models.CharField(max_length = 30, choices=plan_type,blank=True,null=True,help_text="Select Plan Type SME or GIFTING or CORPORATE GIFTING")
    mobile_number = models.CharField(max_length=30, blank=True)
    Status = models.CharField(max_length=30, choices=status, default='processing',
                              help_text="Select failed and save to refund user")
    medium = models.CharField(max_length=30, default='website')
    create_date = models.DateTimeField(default=timezone.now)
    balance_before = models.CharField(max_length=30, blank=True)
    balance_after = models.CharField(max_length=30, blank=True, null=True)
    plan_amount = models.CharField(max_length=30, blank=True)
    Ported_number = models.BooleanField(default=False, blank=True, null=True)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    refund = models.BooleanField(default=False, blank=True, null=True)
    api_response = models.TextField(default='',blank=True)

    class Meta:
        verbose_name_plural = 'DATA TOP-UP TRANSACTIONS'
        
    def __str__(self):
        return str(self.plan)
    

    def data_amount(self):
        return str(self.plan_amount)

    def save(self, *args, **kwargs):

        if self.Status == 'failed' and self.refund == False:
            if self.id :
                previous_bal = self.user.Account_Balance
            else:
                previous_bal = self.balance_after
            self.user.deposit(self.user.id, float(self.plan_amount),False ,"DATA TOPUP Refund")
            self.refund = True
            Wallet_summary.objects.create(user=self.user, product="{} {}{}   N{}  DATA topup Refund for {} ".format(self.network.name, self.plan.plan_size, self.plan.plan_Volume,
                                                                                                                    self.plan_amount, self.mobile_number), amount=self.plan_amount, previous_balance=previous_bal, after_balance=(previous_bal + float(self.plan_amount)))

        super(Data, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('Data_success', args=[str(self.id)])

class AirtimeTopup(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    network = models.ForeignKey(Network, on_delete=models.SET_NULL, null=True)
    mobile_number = models.CharField(max_length=30, blank=True)
    airtime_type = models.CharField(
        max_length=30, choices=airtype, default='VTU', help_text="VTU or share and Sell")
    amount = models.CharField(max_length=30, blank=True)
    paid_amount = models.CharField(max_length=30, blank=True)
    Status = models.CharField(max_length=30, choices=status, default='processing',
                              help_text="Select failed and save to refund user")
    create_date = models.DateTimeField(default=timezone.now)
    balance_before = models.CharField(max_length=30, blank=True)
    balance_after = models.CharField(max_length=30, blank=True)
    Ported_number = models.BooleanField(default=False, blank=True, null=True)
    medium = models.CharField(max_length=30, default='website')
    ident = models.CharField(default=create_id, editable=False, max_length=300)
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
            if self.id :
                previous_bal = self.user.Account_Balance
            else:
                previous_bal = self.balance_after
            self.user.deposit(self.user.id, float(self.paid_amount),False ,"AIRTIME TOPUP Refund")
            self.refund = True
            Wallet_summary.objects.create(user=self.user, product="{} {} Airtime topup Refund for {} ".format(
                self.network.name, self.amount, self.mobile_number), amount=self.paid_amount, previous_balance=previous_bal, after_balance=(previous_bal + float(self.paid_amount)))

        super(AirtimeTopup, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'AIRTIME TOPUP TRANSACTIONS'
