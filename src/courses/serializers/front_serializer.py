from rest_framework import serializers
from rest_framework.response import Response
from exam.serializers.front_serializer import *
from courses.models import *
from exam.models import Exam


class CourseInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseInformation
        fields='__all__'
class VideoContentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=VideoContents
        fields='__all__'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model=Exam
        fields='__all__'
class ContentModelSerializer(serializers.ModelSerializer):
    content=serializers.SerializerMethodField()
    class Meta:
        model=Content
        fields='__all__'
    def get_content(self,obj):
        content_type = obj.content_type
        model_class = content_type.model_class()
        item_id = obj.object_id


         # Retrieve the related object using the appropriate model class
        item = model_class.objects.get(id=item_id)
        # Serialize the related object using the appropriate serializer
        serializer = None
        if model_class == VideoContents:
            serializer = VideoContentModelSerializer(item)
        if model_class == Exam:
            serializer = ExamSerializer(item)
        if model_class == CourseInformation:
            serializer = CourseInformationSerializer(item)
        if serializer:
            return serializer.data
class ModuleModelSerializer(serializers.ModelSerializer):
    content=serializers.SerializerMethodField()
    class Meta:
        model=Module
        exclude=('course',)
    def get_content(self,obj):
        contents=obj.content_rel.all()
        return ContentModelSerializer(instance=contents,many=True).data
class CourseModelSerializer(serializers.ModelSerializer):
    # module=serializers.SerializerMethodField()
    class Meta:
        model=Course
        fields='__all__'
    # def get_module(self,obj):
    #     module=obj.module_rel.all()
    #     return ModuleModelSerializer(instance=module,many=True).data

class UserCourseModelSerializer(serializers.ModelSerializer):
    course=CourseModelSerializer()
    class Meta:
        model=UserCourse
        exclude=('user',)

class CreateUserCourseSerializer(serializers.Serializer):
    course=serializers.IntegerField()
    session_id=serializers.CharField(max_length=400)

class ModuleScheduleSerializer(serializers.ModelSerializer):
    module=ModuleModelSerializer()
    class Meta:
        model=ModuleSchedule
        fields='__all__'

