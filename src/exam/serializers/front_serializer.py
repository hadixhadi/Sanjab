from courses.models import Content, CourseInformation
from courses.serializers.front_serializer import CourseInformationSerializer
from exam.models import *
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
class FrontQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'

class FullExamSerializer(serializers.ModelSerializer):
    questions=serializers.SerializerMethodField()

    def get_questions(self,obj):
        exam=Exam.objects.get(id=obj.id)
        questions=Question.objects.filter(exam=exam)
        return FrontQuestionSerializer(instance=questions,many=True).data
    class Meta:
        model=Exam
        fields='__all__'


class ShowExamSerializer(serializers.Serializer):
    content=serializers.SerializerMethodField()
    def get_content(self,obj):
        content_type = obj.content_type
        model_class = content_type.model_class()
        item_id = obj.object_id


         # Retrieve the related object using the appropriate model class
        item = model_class.objects.get(id=item_id)
        # Serialize the related object using the appropriate serializer
        serializer = None
        if model_class == Exam:
            serializer = FullExamSerializer(item)
        if serializer:
            return serializer.data