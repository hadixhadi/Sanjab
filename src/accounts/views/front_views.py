import json
import random
import traceback

from django.db import transaction
from django.http import JsonResponse

from accounts.serializers.front_serializer import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from accounts.tasks import send_otp_code , remove_otp_code
from accounts.models import OtpCode
from django_celery_beat.models import PeriodicTask , IntervalSchedule
# Create your views here.
class UserSendOtpCode(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        print("req get : ",request.GET)
    def post(self,request):
        ser_data=RegisterOrLoginSrializer(data=request.data)
        if ser_data.is_valid():
            with transaction.atomic():
                request.session['user_phone_number']=request.data
                otp_code=random.randint(1000,9999)
                phone_number=ser_data.data['phone_number']
                send_otp_code.delay(phone_number=phone_number,otp_code=otp_code)
                otp_code_instance=OtpCode.objects.create(
                    phone_number=phone_number,
                    code=otp_code
                )
                otp_code_instance.set_expire_time()
                otp_code_instance.save()
                interval_instance=IntervalSchedule.objects.create(
                            every=2,
                            period=IntervalSchedule.MINUTES
                        )
                PeriodicTask.objects.create(
                    name=f"remove otp code{otp_code_instance.id}",
                    task="accounts.tasks.remove_otp_code",
                    interval=interval_instance,
                    one_off=True,
                    kwargs=json.dumps({
                        "id": otp_code_instance.id
                    }),
                    expire_seconds=120
                )

                return Response("otp code has sent to your phone",status=status.HTTP_200_OK)
        else:
            return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

class UserOtpCodeVerification(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            user_phone_number=request.session['user_phone_number']['phone_number']
            instance=OtpCode.objects.get(phone_number=user_phone_number)
            ser_data=UserVerificationCodeSerializer(data=request.data)
            current_time=timezone.now().time()
            if ser_data.is_valid():
                if ser_data.data['code'] == instance.code and instance.expire_at > current_time :
                    if User.objects.filter(phone_number=user_phone_number).exists():
                        return JsonResponse({
                            "is_registered":True
                        })
                    else:
                        return JsonResponse({
                            "is_registered": False
                        })
                    instance.delete()
                elif instance.expire_at < current_time:
                    instance.delete()
                    return Response('time expired',status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response('code is wrong', status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response(traceback.format_exc())


class UserRegisterationView(APIView):
    def post(self,request):
        ser_data=UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            with transaction.atomic():
                user=ser_data.save()
                user.phone_active=True
                user.phone_number=request.session['user_phone_number']['phone_number']
                user.save()
                return Response('registered successfully',status=status.HTTP_201_CREATED)

class ChildRegisterView(APIView):
    def post(self,request):
        ser_data=ChildRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data,status=status.HTTP_201_CREATED)
        else:
            return Response(ser_data.errors)




class UserAdminDashboard(viewsets.ModelViewSet):

    def get_queryset(self):
        return User.objects.filter(national_code=self.request.user.national_code)
    def get_serializer_class(self):
        if self.action == 'list':
            return UserDashboardSerializer