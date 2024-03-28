from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from django.forms import model_to_dict

from courses.models import Content, CourseInformation
from courses.serializers.front_serializer import CourseInformationSerializer
from exam.models import *
from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from exam.models import Evaluation
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
    is_writeable=serializers.SerializerMethodField()
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

    def get_is_writeable(self,obj):
        content_type_obj = obj.content_type
        model_class = content_type_obj.model_class()
        item_id = obj.object_id
        content_type=ContentType.objects.get(model="exam")
        content=Content.objects.filter(Q(content_type=content_type) & Q(object_id=item_id)).first()
        return content.is_exam_writeable


class AnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_value = serializers.IntegerField()




class UserAnswerSerializer(serializers.Serializer):
    answers = serializers.DictField()

    def create(self, validated_data):
        with transaction.atomic():
            answers_data = validated_data['answers']
            user_answers = []
            request=self.context.get("request")
            course_id=self.context.get("course_id")
            user=request.user
            exam=self.context.get('content_exam')
            child_national_code=self.context.get('child_national_code')
            child=ChildUser.objects.get(national_code=child_national_code)
            exam_obj=Exam.objects.get(pk=exam.object_id)
            for question_id,answer_id in answers_data.items():
                question_instance=Question.objects.get(pk=question_id)
                user_answers.append(AnswerQuestion(user=user,exam=exam_obj,
                                                  question=question_instance,answer=answer_id,child=child
                                                   ))
            if exam_obj.is_last:
               AnswerQuestion.objects.bulk_create(user_answers)
               evaluated_exam = Evaluation.evaluate_exam(request=request,
                                           exam_id=exam_obj.id,child_national_code=child_national_code)
               if evaluated_exam:
                   user_course=UserCourse.get_user_course(request=request,course_id=course_id)
                   user_course.is_graduated=True
                   user_course.save()
            else:
                AnswerQuestion.objects.bulk_create(user_answers)
        # return Response("done",status=status.HTTP_200_OK)


class EvaluationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Evaluation
        fields='__all__'





