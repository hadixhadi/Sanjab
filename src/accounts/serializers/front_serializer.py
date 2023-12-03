from accounts.models import *
from rest_framework import serializers

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=['is_active','is_admin','phone_active','password']

class ChildRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChildUser
        fields='__all__'