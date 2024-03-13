from exam.serializers.front_serializer import *
from courses.models import *
from exam.models import Exam
from rest_framework import serializers

class UserDoneContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserDoneContent
        fields='__all__'

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
    # progress_process=serializers.SerializerMethodField()

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


    # def get_progress_process(self,obj):
    #     request=self.context.get("request")
    #     course_id=self.context.get("course_id")
    #
    #     registered_course_obj=UserCourse.objects.get(id=course_id)
    #     course_obj=registered_course_obj.course
    #     module_obj=course_obj.module_rel.first()
    #     all_course_contents=module_obj.content_rel.all().count()
    #     done_content=UserDoneContent.objects.filter(user=request.user,
    #                                                 course__id=course_obj.id).count()
    #
    #
    #     progress_process_percent=float((done_content/all_course_contents))*100
    #     return progress_process_percent
class ModuleModelSerializer(serializers.ModelSerializer):
    content=serializers.SerializerMethodField()
    class Meta:
        model=Module
        exclude=('course',)
    def get_content(self,obj):
        contents=obj.content_rel.all()
        return ContentModelSerializer(instance=contents,many=True).data
class CourseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'


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

