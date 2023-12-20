from django.db import transaction

from courses.models import *
from rest_framework import views, status
from rest_framework.permissions import AllowAny
from courses.serializers.front_serializer import *
from rest_framework.response import Response
from datetime import datetime , timedelta
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class CourseView(views.APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        courses=Course.objects.all()
        ser_data=CourseModelSerializer(instance=courses,many=True)
        return Response(ser_data.data)

class CreateUserCourseView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user=request.user
        ser_data=CreateUserCourseSerializer(data=request.data)
        if ser_data.is_valid():
            with transaction.atomic():
                course_id=ser_data.validated_data['course']
                course=Course.objects.get(pk=course_id)
                user_course=UserCourse.objects.create(
                    user=user,
                    course=course,
                    expire_at=datetime.now() + timedelta(days=90)
                )
                modules=course.module.all()
                for module in modules:
                    active_at=datetime.now()
                    ModuleSchedule.objects.create(
                        user=user,
                        module=module,
                        active_at=active_at,
                        course=course
                    )
                    active_at = datetime.now() + timedelta(days=20)
                    print(module)
                user_course.save()
                return Response("course created successfully " , status=status.HTTP_201_CREATED)
        else:
            return Response(ser_data.errors,status=status.HTTP_403_FORBIDDEN)