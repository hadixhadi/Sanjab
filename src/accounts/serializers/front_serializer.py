from accounts.models import *
from rest_framework import serializers

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

class UserDashboardSerializer(serializers.ModelSerializer):
    children=serializers.SerializerMethodField()

    def get_children(self,obj):
        childs=obj.father_child.all()
        ser_data=ChildRegisterSerializer(childs,many=True)
        return ser_data.data
    class Meta:
        model=User
        exclude=['password','is_active','phone_active','is_admin']

