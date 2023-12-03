from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from exam.serializers.admin_serializer import *
from exam.models import *
class ExamsViewsets(viewsets.ModelViewSet):
    def get_queryset(self):
        return Exam.objects.all()
    def get_serializer_class(self):
        match self.action:
            case 'list':
                return ExamSerializer
            case _ :
                return ExamSerializer

class QuestionViewsets(viewsets.ModelViewSet):
    def get_queryset(self):
        return Question.objects.all()
    def get_serializer_class(self):
        match self.action:
            case 'list':
                return QuestionsSerializer
            case _:
                return QuestionsSerializer