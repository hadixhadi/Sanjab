from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import  UserProfile , ChildUser
from accounts.serializers.front_serializer import ChildRegisterSerializer , UserProfileModelSerializer


class UserSerializer(serializers.ModelSerializer):
    children=serializers.SerializerMethodField()
    user_profile=serializers.SerializerMethodField()
    class Meta:
        model=get_user_model()
        exclude=['password','is_active','phone_active','is_admin']

    def get_user_profile(self,obj):
        user_national_code=obj.national_code
        user=get_user_model().objects.get(national_code=user_national_code)
        user_profile=UserProfile.objects.get(user=user)
        return UserProfileModelSerializer(instance=user_profile).data
    def get_children(self,obj):
        childes=obj.father_child.all()
        ser_data=ChildRegisterSerializer(childes,many=True)
        return ser_data.data


class ModifyChildSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChildUser
        exclude=("national_code","type","parent")