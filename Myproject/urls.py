"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path,include
from vtuapp.views import *
from vtuapp.models import *
from vtuapp.admin import *
from . import settings
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls
from django.views.generic.base import TemplateView

from django_otp.admin import OTPAdminSite
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from django.contrib.sites.models import Site
from django.contrib.admin.models import LogEntry

class OTPAdmin(OTPAdminSite):
    pass


admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(TOTPDevice, TOTPDeviceAdmin)
admin_site.site_title = f"Alxproject"
admin_site.site_header = f"Welcome To Alxproject Admin Panel"

admin_site.register(CustomUser,CustomUserAdmin)
admin_site.register(Data,DataAdmin)
admin_site.register(AirtimeTopup,AirtimeTopupAdmin)
admin_site.register(Plan,PlanAdmin)
admin_site.register(Network,NetworkAdmin)
admin_site.register(Wallet_summary,WalletAdmin)
admin_site.register(TopupPercentage,Topup_Percentage_Admin)
admin_site.register(Site)
admin_site.register(LogEntry)


urlpatterns = [
    
    path('',WelcomeView.as_view(),name='home'),
    path('',include('vtuapp.urls')),
    path('',include('django.contrib.auth.urls')),

    path('myadmin/page/', admin.site.urls),

    path('api/data/<int:id>', DataAPIView.as_view()),

    path('api/data/', DataAPIListView.as_view()),
    path('api/topup/<int:id>', AirtimeTopupAPIView.as_view()),

    path('api/topup/', AirtimeTopupAPIListView.as_view()),
   
    path('rest-auth/', include('rest_auth.urls')),
    
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('session_security/', include('session_security.urls')),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)