from exam.models import *
from rest_framework import serializers
class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model=Exam
        fields='__all__'
class QuestionsSerializer(serializers.ModelSerializer):
    exam=serializers.SerializerMethodField()
    class Meta:
        model=Question
        exclude=['user_answer']
    def get_exam(self,obj):
        return obj.exam.subject