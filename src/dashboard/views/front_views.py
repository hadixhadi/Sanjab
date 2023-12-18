from django.shortcuts import render
from rest_framework import views, status
from accounts.models import User
from dashboard.serializers.front_serializer import *
from rest_framework.response import Response
from courses.models import UserCourse
from courses.serializers.front_serializer import UserCourseModelSerializer
# Create your views here.

class EntryDashboardView(views.APIView):
    def get(self,request):
        instance=User.objects.get(national_code=request.user.national_code)
        ser_data=EntryDashboardSerializer(instance=instance)
        return Response(ser_data.data,status=status.HTTP_200_OK)

class UserCoursesView(views.APIView):
    def get(self,request):
        obj=UserCourse.objects.filter(user=request.user)
        ser_data=UserCourseModelSerializer(instance=obj,many=True)
        return Response(ser_data.data)