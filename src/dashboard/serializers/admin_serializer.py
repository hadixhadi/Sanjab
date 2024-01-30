from django.contrib.auth import get_user_model
from rest_framework import serializers, status

from accounts.models import UserProfile
from accounts.serializers.front_serializer import UserProfileModelSerializer, ChildRegisterSerializer
from courses.models import UserCourse, Course
from rest_framework.response import Response
from accounts.models import ChildUser
from courses.serializers.front_serializer import CourseModelSerializer


class UserIdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=['first_name','last_name','national_code','phone_number']
class RegisteredCoursesSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    child_user=serializers.SerializerMethodField()
    course=serializers.SerializerMethodField()
    class Meta:
        model=UserCourse
        fields='__all__'

    def get_user(self,obj):
        return UserIdentifierSerializer(instance=obj.user).data
    def get_child_user(self,obj):
        child_user=ChildUser.objects.get(national_code=obj.child)
        ser_data=ChildRegisterSerializer(instance=child_user)
        return ser_data.data
    def get_course(self,obj):
        course=Course.objects.get(pk=obj.course)
        ser_data=CourseModelSerializer(instance=course)
        return ser_data.data

class AdminUpdateUserSerializer(serializers.ModelSerializer):
    user_profile=serializers.SerializerMethodField()

    class Meta:
        model=get_user_model()
        exclude=('is_admin','password')
        Read_only_fields=('national_code','is_admin')

    def get_user_profile(self, obj):
        user_national_code = obj.national_code
        user = get_user_model().objects.get(national_code=user_national_code)
        user_profile = UserProfile.objects.get(user=user)
        request_data=self.context.get('request_data')
        ser_data=UserProfileModelSerializer(instance=user_profile,data=request_data,partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return UserProfileModelSerializer(instance=user_profile).data
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)