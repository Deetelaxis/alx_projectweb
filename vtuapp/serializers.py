from rest_framework.serializers import ModelSerializer
from  .models import *
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueValidator
from django.utils.timezone import datetime  as datetimex
import uuid
import random,requests,json
from requests.auth import HTTPBasicAuth
import hashlib
        


class PlanSerializer(serializers.ModelSerializer):
    plan_amount= serializers.ReadOnlyField(source='plan_amt')
    plan_network = serializers.ReadOnlyField(source='plan_net')
    plan= serializers.ReadOnlyField(source='plan_name')
    dataplan_id= serializers.ReadOnlyField(source='plan_id')


    class Meta:
        model = Plan
        fields = ('id','dataplan_id','network','plan_type','network','plan_network','month_validate', 'plan','plan_amount' )



class DataSerializer(ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    plan_name= serializers.ReadOnlyField(source='plan.plan_name')
    plan_amount= serializers.ReadOnlyField(source='data_amount')
    plan_network= serializers.ReadOnlyField(source='plan.plan_net')
    Ported_number= serializers.BooleanField()



    class Meta:
        model = Data
        fields =  ('user','id','network','ident','balance_before','balance_after','mobile_number','plan','Status','api_response','plan_network','plan_name','plan_amount','create_date',"Ported_number")


    def validate(self, data):
        errors = {}
        Mtn = ['07025', '07026', '0703', '0704', '0706', '0803', '0806', '0810', '0813', '0814', '0816', '0903','0913', '0906','0916']
        ETISALATE = ['0809', '0817', '0818', '0909', '0908']
        GLO = ['0705', '0805', '0811', '0807', '0815', '0905','0915']
        AIRTEL = ['0708', '0802', '0808', '0812','0907', '0701', '0901', '0902','0917', '0901', '0904']

        num = data.get('mobile_number')
        amount =  data.get('plan')
        user = data.get('user')
        net = data.get('network')
        plan = data.get('plan')
        Ported_number  = data.get('Ported_number')

        amount = float(plan.plan_amount)


        if len(str(num)) != 11   :
            errors['error'] = u'invalid mobile number {}!'.format(num)
            raise serializers.ValidationError(errors)

        elif Ported_number !=  True and net.name == '9MOBILE' and not num.startswith(tuple(ETISALATE)):

                errors['error'] = u'Please check entered number is not 9MOBILE user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif Ported_number !=  True and net.name == 'MTN' and not num.startswith(tuple(Mtn)):
                errors['error'] = u'Please check entered number is not MTN user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif Ported_number !=  True and net.name == 'GLO' and not num.startswith(tuple(GLO)):
                errors['error'] = u'Please check entered number is not GLO user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif Ported_number !=  True and net.name == 'AIRTEL' and not num.startswith(tuple(AIRTEL)):
                errors['error'] = u'Please check entered number is not AIRTEL user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif not num.isdigit():
            errors['error'] = u'invalid mobile number {}!'.format(num)
            raise serializers.ValidationError(errors)


        elif Network.objects.get(name=net.name).data_disable == True:
              errors['error'] = u'Data not available on this network currently'
              raise serializers.ValidationError(errors)

        elif not  Plan.objects.filter (network =net).filter(id=plan.id).exists():
            errors['error'] = u'invalid plan id {} for {}, check here for available plan list '.format(plan.id,net)
            raise serializers.ValidationError(errors)

        elif float(amount) > user.Account_Balance:
            errors['error'] = u'You can\'t purchase this plan due to insufficient balance  ₦{} Kindly Fund your Wallet'.format(user.Account_Balance)
            raise serializers.ValidationError(errors)



        return data



class AirtimeTopupSerializer(ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    plan_amount= serializers.ReadOnlyField(source='plan_amt')
    plan_network= serializers.ReadOnlyField(source='plan_net')
    Ported_number= serializers.BooleanField()


    class Meta:
        model = AirtimeTopup
        fields =  ('user','id','airtime_type','network','airtime_type','ident','paid_amount','mobile_number','amount','plan_amount','plan_network','balance_before','balance_after','Status','create_date',"Ported_number")


    def validate(self, data):
        errors = {}
        Mtn = ['07025', '07026', '0703', '0704', '0706', '0803', '0806', '0810', '0813', '0814', '0816', '0903','0913', '0906','0916']
        ETISALATE = ['0809', '0817', '0818', '0909', '0908']
        GLO = ['0705', '0805', '0811', '0807', '0815', '0905','0915']
        AIRTEL = ['0708', '0802', '0808', '0812','0907', '0701', '0901', '0902','0917', '0901', '0904']


        num = data.get('mobile_number')
        amount =  data.get('amount')
        amt =  data.get('amount')
        user = data.get('user')
        net = data.get('network')
        Ported_number  = data.get('Ported_number')
        airtime_type = data.get("airtime_type")
        print(Ported_number)
        print(Ported_number)

        if user.user_type == "Affilliate":
               perc = TopupPercentage.objects.get(network = Network.objects.get(name=net)).Affilliate_percent
               perc2 = TopupPercentage.objects.get(network = Network.objects.get(name=net)).share_n_sell_affilliate_percent

        elif user.user_type == "API":
              perc = TopupPercentage.objects.get(network = Network.objects.get(name=net)).api_percent
              perc2 = TopupPercentage.objects.get(network = Network.objects.get(name=net)).share_n_sell_api_percent

        elif user.user_type == "TopUser":

              perc = TopupPercentage.objects.get(network = Network.objects.get(name=net)).topuser_percent
              perc2 = TopupPercentage.objects.get(network = Network.objects.get(name=net)).share_n_sell_topuser_percent

        else:
              perc = TopupPercentage.objects.get(network = Network.objects.get(name=net)).percent
              perc2 = TopupPercentage.objects.get(network = Network.objects.get(name=net)).share_n_sell_percent


        if airtime_type == "VTU":
             amount = float(amount) * int(perc)/100

        else:
             amount = float(amount) * int(perc2)/100


        if float(amount) >user.Account_Balance:
            errors['error'] = u'You can\'t topup due to insufficient balance  ₦{} '.format(user.Account_Balance)
            raise serializers.ValidationError(errors)

        elif float(data.get('amount')) < 100:
            errors['error'] = u'minimum airtime topup is ₦100'
            raise serializers.ValidationError(errors)
        

        elif airtime_type == "Share and Sell" and float(data.get('amount')) < 100:
            errors['error'] = u'minimum airtime share and sell topup is ₦100'
            raise serializers.ValidationError(errors)


        elif len(str(num)) != 11   :
            errors['error'] = u'invalid mobile number {}!'.format(num)

            raise serializers.ValidationError(errors)

        elif not num.isdigit():
            errors['error'] = u'invalid mobile number {}!'.format(num)

            raise serializers.ValidationError(errors)

        elif Ported_number !=  True and  net.name == '9MOBILE' and not num.startswith(tuple(ETISALATE)):

                errors['error'] = u'Please check entered number is not 9MOBILE user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif  Ported_number !=  True and net.name == 'MTN' and not num.startswith(tuple(Mtn)):
                errors['error'] = u'Please check entered number is not MTN user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif  Ported_number !=  True and net.name == 'GLO' and not num.startswith(tuple(GLO)):
                errors['error'] = u'Please check entered number is not GLO user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif  Ported_number !=  True  and net.name == 'AIRTEL' and not num.startswith(tuple(AIRTEL)):
                errors['error'] = u'Please check entered number is not AIRTEL user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif Network.objects.get(name=net.name).airtime_disable == True:
              errors['error'] = u'Airtime is  not available on this network currently'
              raise serializers.ValidationError(errors)


        return data
        
 
