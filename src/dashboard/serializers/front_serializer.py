from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import  UserProfile , ChildUser
from accounts.serializers.front_serializer import ChildRegisterSerializer , UserProfileModelSerializer
from courses.models import UserCourse, UserDoneContent
from courses.models import Content
from courses.serializers.front_serializer import ContentModelSerializer


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
        exclude=("national_code","parent")




# class UserCourseModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=UserCourse
#         fields='__all__'


class UserDoneContentsModelSerializer(serializers.ModelSerializer):
    content=serializers.SerializerMethodField()
    class Meta:
        model=UserDoneContent
        fields='__all__'

    def get_content(self,obj):
        content_obj=Content.objects.get(id=obj.content.id)
        request=self.context.get('request')
        course_id=self.context.get('course_id')
        ser_data=ContentModelSerializer(instance=content_obj)
        return ser_data.data



