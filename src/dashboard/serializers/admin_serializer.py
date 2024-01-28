from django.contrib.auth import get_user_model
from rest_framework import serializers
from courses.models import UserCourse

class UserIdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=['first_name','last_name','national_code','phone_number']
class RegisteredCoursesSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    class Meta:
        model=UserCourse
        fields='__all__'

    def get_user(self,obj):
        return UserIdentifierSerializer(instance=obj.user).data


