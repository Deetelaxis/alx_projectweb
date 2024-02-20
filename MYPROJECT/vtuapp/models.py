from django.db import models
from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone



# Create your models here.

import random


User = settings.AUTH_USER_MODEL

class User(AbstractUser):
    # Add your custom fields here
    pass


    # Add custom fields and methods if needed

