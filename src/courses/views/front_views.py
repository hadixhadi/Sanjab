from rest_framework import views
from courses.serializers.front_serializer import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import ChildUser
from django.contrib.sessions.backends.db import SessionStore
# Create your views here.

class CourseView(views.APIView):
    """

    Showing courses that can be registered according to the type and age range of the user.

    """
    def get(self,request):
        session_id=request.GET.get('session')
        session=SessionStore(session_key=session_id)
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
        ser_data=CreateUserCourseSerializer(data=request.data)
        if ser_data.is_valid():
            user_create_course=UserCourse.create_user_course(request=request, ser_data=ser_data)
            return user_create_course
        else:
            return Response(ser_data.errors,status=status.HTTP_403_FORBIDDEN)



class SetContentDone(views.APIView):

    def get(self, request, course_id,content_id,object_id):
        user_course_obj=UserCourse.get_user_course(request=request,course_id=course_id)
        session_id=request.GET.get('session')
        session=SessionStore(session_key=session_id)
        user_done_content=UserDoneContent.create_user_done_content(
            request=request,user_course_obj=user_course_obj,
            course_id=course_id,content_id=content_id,object_id=object_id
        )
        return Response(user_done_content.data)


