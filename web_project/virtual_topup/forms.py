from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import json, uuid


status =(
    ('processing','processing'),
    ('failed','Failed'),
    ('successful','Successful'),
)

Airtime_choice =(
    (100 , '#100'),
    (500,'#500'),
    (1000,'#1000'),
    (5000,'#5000'),
    (1000,'#1000'),
)
Bank = (
    ('Palmpay', 'Palmpay'),
    ('Opay', 'Opay'),
    ('Moniepoint', 'Moniepoint'),
    ('FCMBank','FCMBank'),
    ('GTBank','GTBank'),
    ('FIdelity Bank','FIdelity Bank'),
    ('ECO Bank','ECO Bank'),
    ('First Bank of Nigeria','First Bank of Nigeria'),
    ('UBA','UBA'),
    ('Access Bank','Access Bank'),
    ('Wema Bank','Wema Bank'),
    ('Diamond Bank','Diamond Bank'),
    ('Heritage Bank','Heritage Bank'),
    ('Skye Bank','Skye Bank'),
    ('Stanbic IBTC','Stanbic IBTC'),
    ('Sterling Bank','Sterling Bank'),
    ('Union Bank','Union Bank'),
    ('Zenith Bank','Zenith Bank'),
    ('Unity Bank','Unity Bank'),
    
)

class CustomUserCreationForm(UserCreationForm):
    username  = forms.CharField()
    password1 = forms.CharField(widget = forms.PasswordInput, label='Password',
    help_text='min_lenght-8 mix characters [i.e musa1234] ')
    password2 = forms.CharField(widget = forms.PasswordInput,help_text='Enter same password as before',label='Confirm Password')
    Phone = forms.CharField(max_length = 11, min_length = 11)
    referer_username = forms.CharField(required=False,help_text='Leave blank if no referral',label='Referral username [optional]')


    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("FullName",'username','email','Phone','Address','referer_username','password1','password2')


class Pinform(forms.ModelForm):
      pin = forms.IntegerField( max_value=9999,min_value=0000,help_text='max 4 lenght digit')

      class Meta:
            model = PinCode
            fields =  ('pin',)
            
class airtimeform(forms.ModelForm):
      pin = forms.CharField(max_length = 18, min_length = 10)


class Meta:
        model = Airtime
        fields = ('network','pin','amount')



class AirtimeTopupform(forms.ModelForm):

     mobile_number = forms.CharField(max_length = 11, min_length = 11)
     amount =forms.IntegerField(min_value = 100 )
     Ported_number = forms.BooleanField(required=False,initial=False,label='Bypass number validator ')

     
     
     class Meta:
        model = AirtimeTopup
        fields =  ('network','airtime_type','mobile_number','amount',"Ported_number")
        
        
class paymentgateway_form(forms.ModelForm):

    class Meta:
        model = paymentgateway
        fields =  ('amount',)


class Bankpaymentform(forms.ModelForm):

      Reference = forms.CharField(max_length = 15,label ='Reference or Narration',required =True, help_text = "Use your name as  Reference or Narration if it is bank Tranfer")
      amount = forms.IntegerField(min_value = 0)
      class Meta:
        model = Bankpayment
        fields =  ('Bank_paid_to','Reference', 'amount',)
        
        
class dataform(forms.ModelForm):
     mobile_number = forms.CharField(max_length = 11, min_length = 11)
     Ported_number = forms.BooleanField(required=False,initial=False,label='Bypass number validator ')
     Amount = forms.CharField(required=False,max_length = 11, min_length = 11)

     class Meta:
        model = Data
        fields =  ('network','data_type','mobile_number','plan',"Amount","Ported_number")

     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].queryset = Plan.objects.none()

        if 'network' in self.data:
            try:
                network_id = int(self.data.get('network'))
                self.fields['plan'].queryset = Plan.objects.filter(network_id = network_id).order_by('plan_amount')

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['plan'].queryset = self.instance.network.plan_set.order_by('plan_amount')
            
            

class cableform(forms.ModelForm):

     smart_card_number = forms.CharField(max_length = 15, min_length = 5,label = 'Smart Card number / IUC number')

     class Meta:
        model = Cablesub
        fields =  ('cablename','smart_card_number','cableplan', 'customer_name',)

     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cableplan'].queryset = CablePlan.objects.none()

        if 'cablename' in self.data:
            try:
                cablename_id = int(self.data.get('cablename'))
                self.fields['cableplan'].queryset = CablePlan.objects.filter(cablename_id = cablename_id).order_by('plan_amount')

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['cableplan'].queryset = self.instance.cablename.cableplan_set.order_by('plan_amount')
            
            
class Billpaymentform(forms.ModelForm):
    Customer_Phone = forms.CharField(max_length = 11, min_length = 11,help_text="customer phone number")
    class Meta:
        model = Billpayment
        fields =  ('cable_name','meter_number','MeterType', 'customer_name', 'customer_address','amount','Customer_Phone')


class  monnify_payment_form(forms.Form):
    amount = forms.FloatField(label='Amount' ,min_value = 0.0 ,max_value = 5000.0)


gender =(
    ('MALE','MALE'),
    ('FEMALE','FEMALE'),

)


class KYCForm(forms.ModelForm):
     Gender = forms.ChoiceField(choices= gender)
     
     class Meta:
            model = KYC
            fields =  ('First_Name','Middle_Name',"Last_Name","DOB","Gender","State_of_origin","Local_gov_of_origin","BVN","passport_photogragh")


