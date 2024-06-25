from kavenegar import APIException, HTTPException
from celery import shared_task
from accounts.models import OtpCode
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken , BlacklistedToken
import requests
import datetime
from django.contrib.admin.models import LogEntry
try:
    import json
except ImportError:
    import simplejson as json

@shared_task
def send_otp_code(phone_number,otp_code):
    """
    get user phone number and send otp code to it
    :param phone_number: user phone number that stored in session
    :param otp_code: a random code
    :return: error or a dictionary
    """
    apikey = "3747547076752F7864565A333241547A4F6A57644A71527A796F4654507975636B4F6A4D4B556A666776453D"
    url_api = f"http://api.kavenegar.com/v1/{apikey}/verify/lookup.json?receptor={phone_number}&token={otp_code}&template=login"
    try:
        #sanjab api:
        # api = KavenegarAPI('3747547076752F7864565A333241547A4F6A57644A71527A796F4654507975636B4F6A4D4B556A666776453D')
        # api=KavenegarAPI('3747547076752F7864565A333241547A4F6A57644A71527A796F4654507975636B4F6A4D4B556A666776453D')
        #params = {
        #    'receptor': f'{phone_number}',
        #    'template': 'login',
        #    'token': f'{otp_code}',
        #}

        content = requests.get(url_api).content
        try:
            response = json.loads(content.decode("utf-8"))
            if (response['return']['status']==200):
                response=response['entries']
                print(response)
            else:
                raise APIException((u'APIException[%s] %s' % (response['return']['status'],response['return']['message'])).encode('utf-8'))
        except ValueError as e:
            raise HTTPException(e)
        #response = api.verify_lookup(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
        
@shared_task
def send_nationalcode_faild(phone_number, info):
    """
    get user phone number and send otp code to it
    :param phone_number: user phone number that stored in session
    :param otp_code: a random code
    :return: error or a dictionary
    """
    apikey = "3747547076752F7864565A333241547A4F6A57644A71527A796F4654507975636B4F6A4D4B556A666776453D"
    url_api = f"http://api.kavenegar.com/v1/{apikey}/verify/lookup.json?receptor={phone_number}&token={otp_code}&template=ncodefaild"
    try:
        logc = LogEntry.objects.create(action_time=datetime.datetime.now() , object_id='0', object_repr="تلاش برای ورود با کد ملی ثبت شده", action_flag=0, change_message=str({phone_number,info}), user_id='0000')
        #sanjab api:
        # api = KavenegarAPI('3747547076752F7864565A333241547A4F6A57644A71527A796F4654507975636B4F6A4D4B556A666776453D')
        
        #api=KavenegarAPI('3747547076752F7864565A333241547A4F6A57644A71527A796F4654507975636B4F6A4D4B556A666776453D')
        #params = {
        #    'receptor': f'{phone_number}',
        #    'template': 'ncodefaild',
        #    'token': f'{logc.id}',
        #}
        #response = api.verify_lookup(params)
        content = requests.get(url_api).content
        try:
            response = json.loads(content.decode("utf-8"))
            if (response['return']['status']==200):
                response=response['entries']
                print(response)
            else:
                raise APIException((u'APIException[%s] %s' % (response['return']['status'],response['return']['message'])).encode('utf-8'))
        except ValueError as e:
            raise HTTPException(e)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)

@shared_task
def remove_otp_code(id):
    """
    get an instance primary key and remove it
    :param id: otpCode instance primary key
    :return: None
    """
    try:
        instance=OtpCode.objects.get(id=id)
        instance.delete()
    except:
        pass

@shared_task
def flush_expired_token():
    OutstandingToken.objects.all().delete()
    BlacklistedToken.objects.all().delete()
