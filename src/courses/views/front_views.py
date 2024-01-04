from django.db import transaction
from rest_framework import views, status
from courses.serializers.front_serializer import *
from rest_framework.response import Response
from datetime import datetime , timedelta
from rest_framework.permissions import IsAuthenticated
from accounts.models import ChildUser
from django.contrib.sessions.backends.db import SessionStore
# Create your views here.

class CourseView(views.APIView):
    def get(self,request):
        session_id=request.GET.get('session')
        session=SessionStore(session_key=session_id)
        print(session['current_user_child'])
        if session['current_user_child'] == None:
            courses=Course.objects.filter(type=4)
        else:
            child_national_code=session['current_user_child']
            child=ChildUser.objects.get(national_code=child_national_code)
            courses=Course.objects.filter(type=child.type)
        ser_data=CourseModelSerializer(instance=courses,many=True)
        return Response(ser_data.data)

class CreateUserCourseView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user=request.user
        print("user type : ",user)
        ser_data=CreateUserCourseSerializer(data=request.data)
        if ser_data.is_valid():
            with transaction.atomic():
                course_id=ser_data.validated_data['course']
                course=Course.objects.get(pk=course_id)
                if request.session['current_user_child'] != None:
                    child_user=ChildUser.objects.get(national_code=request.session['current_user_child'])
                    if course.type == child_user.type :
                        user_course = UserCourse.objects.create(
                            user=user,
                            course=course,
                            child=child_user,
                            expire_at=datetime.now() + timedelta(days=15)
                        )
                    else:
                        return Response("your type is not equal with course type",
                                        status=status.HTTP_403_FORBIDDEN)
                elif request.user.type in [1,2]:
                    user_course=UserCourse.objects.create(
                        user=user,
                        course=course,
                        expire_at=datetime.now() + timedelta(days=15)
                    )
                else:
                    return Response("your type is not equal with course type",
                                    status=status.HTTP_403_FORBIDDEN)
                modules=course.module_rel.all()
                active_at = datetime.now()
                for module in modules:
                    ModuleSchedule.objects.create(
                        user_course=user_course,
                        module=module,
                        active_at=active_at,

                    )
                    active_at = datetime.now() + timedelta(days=90)
                user_course.save()
                return Response("course created successfully " , status=status.HTTP_201_CREATED)
        else:
            return Response(ser_data.errors,status=status.HTTP_403_FORBIDDEN)