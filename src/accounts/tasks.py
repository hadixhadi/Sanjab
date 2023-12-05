from kavenegar import KavenegarAPI, APIException, HTTPException
from celery import shared_task
from accounts.models import OtpCode
@shared_task
def send_otp_code(phone_number,otp_code):
    try:
        api = KavenegarAPI('3747547076752F7864565A333241547A4F6A57644A71527A796F4654507975636B4F6A4D4B556A666776453D')
        params = {
            'sender': '100010008880',  # optional
            'receptor': f'{phone_number}',  # multiple mobile number, split by comma
            'message': f' کد تایید شما:{otp_code}',
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)

@shared_task
def remove_otp_code(id):
    try:
        instance=OtpCode.objects.get(id=id)
        instance.delete()
    except:
        pass