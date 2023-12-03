from exam.models import *
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
class FrontQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'

