from rest_framework import serializers
from accounts.models import User , ChildUser , UserProfile
from accounts.serializers.front_serializer import ChildRegisterSerializer , UserProfileModelSerializer


class EntryDashboardSerializer(serializers.ModelSerializer):
    children=serializers.SerializerMethodField()
    user_profile=serializers.SerializerMethodField()
    class Meta:
        model=User
        exclude=['password','is_active','phone_active','is_admin']

    def get_user_profile(self,obj):
        user_national_code=obj.national_code
        user=User.objects.get(national_code=user_national_code)
        user_profile=UserProfile.objects.get(user=user)
        return UserProfileModelSerializer(instance=user_profile).data
    def get_children(self,obj):
        childes=obj.father_child.all()
        ser_data=ChildRegisterSerializer(childes,many=True)
        return ser_data.data

# class ChildDashboardSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model=ChildUser
#         fields='__all__'
