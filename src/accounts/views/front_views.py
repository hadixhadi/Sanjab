﻿import json
import random
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers.front_serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from rest_framework.permissions import AllowAny
from accounts.tasks import send_otp_code , send_nationalcode_faild
from accounts.models import OtpCode
from django_celery_beat.models import PeriodicTask , IntervalSchedule
from rest_framework.permissions import IsAuthenticated
from django.contrib.sessions.backends.db import SessionStore
# Create your views here.


class UserSendOtpCode(APIView):
    """
    create OTP code instance and send to user phone number.
    create a celery task to expire created OTP code after 2 min.

    """
    permission_classes = [AllowAny]
    throttle_scope='enter_phone_number'

    def post(self,request):
        ser_data=RegisterOrLoginSrializer(data=request.data)
        if ser_data.is_valid():
            with transaction.atomic():
                try:
                    myusr = User.objects.get(phone_number=request.data['phone_number'])
                    isactiveuser = myusr.is_active
                except:
                    isactiveuser = True
                if isactiveuser:
                    request.session['user_phone_number']=request.data
                    otp_code=random.randint(1000,9999)
                    phone_number=ser_data.data['phone_number']

                    otp_code_instance=OtpCode.objects.create(
                        phone_number=phone_number,
                        code=otp_code
                    )
                    otp_code_instance.set_expire_time()
                    otp_code_instance.save()
                    interval_instance=IntervalSchedule.objects.create(
                                every=1,
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
                    request.session.save()
                    send_otp_code.delay(phone_number=phone_number, otp_code=otp_code)
                    return Response(request.session.session_key,status=status.HTTP_200_OK)
                else:
                   return Response(f"User is Block",status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)


class UserOtpCodeVerification(APIView):
    """
    verify otp code and create JWT token if already registered.
    """
    permission_classes = [AllowAny]
    throttle_scope='otp_verification_views'
    def post(self,request):
        try:
            session_id=request.GET.get('session')
            session=SessionStore(session_key=session_id)
            user_phone=session['user_phone_number']
            user_phone_number=user_phone['phone_number']
            instance=OtpCode.objects.get(phone_number=user_phone_number)
            ser_data=UserVerificationCodeSerializer(data=request.data)
            current_time=timezone.now().time()
            if ser_data.is_valid():
                if ser_data.data['code'] == instance.code and instance.expire_at > current_time :
                    try:
                        user=get_object_or_404(User,phone_number=user_phone_number)
                        instance.delete()
                        if user.phone_active ==True:
                            refresh = RefreshToken.for_user(user)
                            token_response = {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                                'is_admin':user.is_admin,
                                'is_super_admin':user.is_super_admin
                            }
                            return Response(token_response, status=status.HTTP_201_CREATED)
                        return Response('phone number is not active!',status=status.HTTP_403_FORBIDDEN)
                    except:
                        instance.delete()
                        return JsonResponse({
                            "is_registered": False
                        })
                elif instance.expire_at < current_time:
                    instance.delete()
                    return Response('code expired',status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response('code is wrong', status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)


class UserRegistrationView(APIView):
    """
    fill parent user form to register and create JWT token.
    """
    permission_classes = [AllowAny]
    throttle_scope='user_register_views'
    def post(self,request):
        ser_data=UserRegisterSerializer(data=request.data)
        try:
            if ser_data.is_valid():
                with transaction.atomic():
                    user=ser_data.save()
                    user.phone_active=True
                    user.is_active=True
                    session_id = request.GET.get('session')
                    session = SessionStore(session_key=session_id)
                    user_phone = session['user_phone_number']
                    user_phone_number=user_phone['phone_number']
                    user.phone_number=user_phone_number
                    user.save()
                    refresh = RefreshToken.for_user(user)
                    token_response={
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                    return Response(token_response,status=status.HTTP_201_CREATED)
                    # return Response('registered successfully',status=status.HTTP_201_CREATED)
            else:
                if (ser_data.errors['national_code'][0] == 'user with this national code already exists.'):
                    usercodeobj = User.objects.get(national_code=request.data["national_code"])
                    send_nationalcode_faild(usercodeobj.phone_number, request.data)
                    return Response(ser_data.errors,status=status.HTTP_403_FORBIDDEN)
                return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message=str(e)
            return JsonResponse({
                'error':error_message
            },status=status.HTTP_400_BAD_REQUEST)


class ChildRegisterView(APIView):
    """
    register child user with post method and retrieve user's children with get method.
    """
    permission_classes = [IsAuthenticated]
    throttle_scope='user_register_views'
    def get(self,request):
        children=ChildUser.objects.filter(parent=request.user)
        ser_data=ChildRegisterSerializer(instance=children,many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)
    def post(self,request):
        print("requested user for child register : ",request.user)
        ser_data=ChildRegisterSerializer(data=request.data)
        if ser_data.is_valid():

            child_obj=ChildUser.objects.create(**ser_data.validated_data)
            child_obj.parent=request.user
            child_obj.save()
            return Response(ser_data.data,status=status.HTTP_201_CREATED)
        else:
            return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        ser_data=LogoutSerializer(data=request.data)
        if ser_data.is_valid():
            token=ser_data.validated_data['token']
            print(token)
            try:
                refresh_token=RefreshToken(token)
                refresh_token.blacklist()
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)


class RegisterHusband(APIView):
    def post(self,request):
        try:
            husband=request.user.user_profile_husband.first().user
        except:
            husband =None
        if husband is None :
            ser_data=RegisterHusbandModelSerializer(data=request.data,context={'request':request})
            if ser_data.is_valid():
                with transaction.atomic():
                    user = ser_data.save()
                    user.phone_active = False
                    user.is_active = False
                    if request.user.type ==1:
                        user.type =2
                    else:
                        user.type=1
                    user.save()
                    return Response(ser_data.data,status=status.HTTP_201_CREATED)
            return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({
                "register_husband":False
            })