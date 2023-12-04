import random
from django.db import transaction
from accounts.serializers.front_serializer import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from rest_framework.permissions import AllowAny
from accounts.utils import send_otp_code
from accounts.models import OtpCode
# Create your views here.

class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        ser_data=UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            with transaction.atomic():
                request.session['parent_register_info']=request.data
                otp_code=random.randint(1000,9999)
                phone_number=request.POST['phone_number']
                send_otp_code(phone_number=phone_number,otp_code=otp_code)
                otp_code_instance=OtpCode.objects.create(
                    phone_number=phone_number,
                    code=otp_code
                )
                otp_code_instance.set_expire_time()
                otp_code_instance.save()
                return Response(ser_data.data,status=status.HTTP_100_CONTINUE)
        else:
            return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

class UserVeryfication(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        user_phone_number=request.session['parent_register_info']['phone_number']
        instance=OtpCode.objects.get(phone_number=user_phone_number)
        ser_data=UserVerificationCodeSerializer(data=request.data)
        current_time=timezone.now().time()
        if ser_data.is_valid():
            if ser_data.data['code'] == instance.code and instance.expire_at > current_time :
                with transaction.atomic():
                    user=User.objects.create(**request.session['parent_register_info'])
                    user.phone_active=True
                    user.save()
                    instance.delete()
                    return Response('registered successfully',status=status.HTTP_201_CREATED)
            elif instance.expire_at < current_time:
                instance.delete()
                return Response('time expired',status=status.HTTP_403_FORBIDDEN)
            else:
                return Response('code is wrong', status=status.HTTP_403_FORBIDDEN)





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