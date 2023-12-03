from django.shortcuts import render
from rest_framework import viewsets ,views
from exam.serializers.front_serializer import *
# Create your views here.
class FrontShowQuestions(viewsets.ModelViewSet):
    def get_queryset(self):
        return Question.objects.all()
    def get_serializer_class(self):
        match self.action:
            case 'list':
                return FrontQuestionSerializer
            case 'create':
                return PostQuestionSerializer
            case _ :
                return FrontQuestionSerializer

