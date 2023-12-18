from accounts.models import *
from rest_framework import serializers
from courses.models import UserCourse

class RegisterOrLoginSrializer(serializers.Serializer):
    phone_number=serializers.CharField()
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=['is_active','is_admin','phone_active','password','phone_number']


class UserVerificationCodeSerializer(serializers.Serializer):
    code=serializers.IntegerField()
class ChildRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChildUser
        fields='__all__'



