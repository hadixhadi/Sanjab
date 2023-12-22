from rest_framework import serializers
from rest_framework.response import Response

from courses.models import *

class ContentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Content
        fields='__all__'
class ModuleModelSerializer(serializers.ModelSerializer):
    content=serializers.SerializerMethodField()
    class Meta:
        model=Module
        exclude=('course',)
    def get_content(self,obj):
        contents=obj.content_rel.all()
        return ContentModelSerializer(instance=contents,many=True).data
class CourseModelSerializer(serializers.ModelSerializer):
    module=serializers.SerializerMethodField()
    class Meta:
        model=Course
        fields='__all__'
    def get_module(self,obj):
        module=obj.module_rel.all()
        return ModuleModelSerializer(instance=module,many=True).data

class UserCourseModelSerializer(serializers.ModelSerializer):
    course=CourseModelSerializer()
    class Meta:
        model=UserCourse
        exclude=('user',)

class CreateUserCourseSerializer(serializers.Serializer):
    course=serializers.IntegerField()


class ModuleScheduleSerializer(serializers.ModelSerializer):
    module=ModuleModelSerializer()
    class Meta:
        model=ModuleSchedule
        fields='__all__'