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