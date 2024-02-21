from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *
import json



class CustomUserAdmin(UserAdmin):
    list_display =['username','email','user_type','Account_Balance','id','last_login','date_joined']
    search_fields = ('username','email','id','user_type')

    fieldsets = UserAdmin.fieldsets 
    # + (
    #          ("Profile", {'fields': ('email',"Account_Balance")}),
    # )

class DataAdmin(admin.ModelAdmin):
   
    add_form=dataform
    list_display =['user','network','mobile_number','plan','id','ident','api_response','Status','medium','create_date']
    search_fields = ('user__username','id','ident','mobile_number','Status',)

class NetworkAdmin(admin.ModelAdmin):
    list_display =['name','msorg_web_net_id']

class PlanAdmin(admin.ModelAdmin):
    list_display =['network','plansize','plan_type','planamount']
    ordering = ['network','plan_size']

    def plansize(self, obj):
        
        return  str(obj.plan_size) + str(obj.plan_Volume)

    def planamount(self, obj):
        
        return  "₦" + str(obj.plan_amount)


class AirtimeTopupAdmin(admin.ModelAdmin):
    add_form=AirtimeTopupform
    list_display =['user','network','mobile_number','amount','id','ident','Status','medium','create_date']
    search_fields = ('user__username','id','mobile_number','ident')

class Topup_Percentage_Admin(admin.ModelAdmin):
    list_display =['network','percent','id']

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount','previous_balance',"after_balance",'create_date')
    search_fields = ['user__username','product',]



admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Data,DataAdmin)
admin.site.register(AirtimeTopup,AirtimeTopupAdmin)
admin.site.register(Plan,PlanAdmin)
admin.site.register(Network,NetworkAdmin)
admin.site.register(Wallet_summary,WalletAdmin)
admin.site.register(TopupPercentage,Topup_Percentage_Admin)


