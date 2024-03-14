from accounts.models import *
from rest_framework import serializers

class UserProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields='__all__'
        read_only_fields = ['user']


class RegisterOrLoginSrializer(serializers.Serializer):
    phone_number=serializers.CharField()




class UserRegisterSerializer(serializers.ModelSerializer):
    user_profile=UserProfileModelSerializer()
    class Meta:
        model=User
        exclude=['is_active','is_admin','phone_active','password','phone_number',]
    def create(self, validated_data):
        user_profile_data = validated_data.pop('user_profile')
        user = User.objects.create(**validated_data)
        UserProfile.objects.create(user=user, **user_profile_data)
        return user
    def validate_type(self,value):
        if value == 3:
            raise serializers.ValidationError("Only type 1 and 3 are allowed!")
        return value


class UserVerificationCodeSerializer(serializers.Serializer):
    code=serializers.IntegerField()




class ChildRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChildUser
        fields='__all__'



class LogoutSerializer(serializers.Serializer):
    token=serializers.CharField(required=True)



class RegisterHusbandModelSerializer(serializers.ModelSerializer):
    user_profile=UserProfileModelSerializer()
    class Meta:
        model=User
        exclude=['is_active','is_admin','phone_active','password','type']
    def create(self, validated_data):
        user_profile_data = validated_data.pop('user_profile')
        user = User.objects.create(**validated_data)
        request=self.context.get('request')
        UserProfile.objects.create(user=user,husband=request.user, **user_profile_data)
        return user
    def validate_type(self,value):
        if value == 3:
            raise serializers.ValidationError("Only type 1 and 3 are allowed!")
        return value