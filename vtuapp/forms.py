from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import json, uuid



class CustomUserCreationForm(UserCreationForm):
    username  = forms.CharField()
    password1 = forms.CharField(widget = forms.PasswordInput, label='Password',
    help_text='Minimum length of 8 characters with a mixture of character types. (example abc080) ')
    password2 = forms.CharField(widget = forms.PasswordInput,help_text='Enter same password as before',label='Confirm Password')


    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email','password1','password2')


class AirtimeTopupform(forms.ModelForm):
     mobile_number = forms.CharField(max_length = 11, min_length = 11)
     amount =forms.IntegerField(min_value = 100 )
     Ported_number = forms.BooleanField(required=False,initial=False,label='Bypass number validator ')

   
     class Meta:
        model = AirtimeTopup
        fields =  ('network','airtime_type','mobile_number','amount',"Ported_number")


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



            