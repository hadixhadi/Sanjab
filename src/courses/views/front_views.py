import json
from urllib.parse import urlparse, urlunparse
import pytz
from django.db import transaction
from django.db.models import Q
from rest_framework import views, status
from courses.serializers.front_serializer import *
from rest_framework.response import Response
from datetime import datetime , timedelta
from rest_framework.permissions import IsAuthenticated
from accounts.models import ChildUser
from django.contrib.sessions.backends.db import SessionStore
from django_celery_beat.models import PeriodicTask , IntervalSchedule

# Create your views here.

class CourseView(views.APIView):
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
        user=request.user
        print("user type : ",user)
        ser_data=CreateUserCourseSerializer(data=request.data)
        if ser_data.is_valid():
            with transaction.atomic():
                session = SessionStore(ser_data.validated_data['session_id'])
                course_id=ser_data.validated_data['course']
                course=Course.objects.get(pk=course_id)
                expire_date=datetime.now() + timedelta(days=10)
                if session['current_user_child'] != None:
                    child_user=ChildUser.objects.get(national_code=session['current_user_child'])
                    if course.type == child_user.type :
                        if UserCourse.objects.filter(Q(user=request.user) & Q(course=course)
                                                     & Q(child=child_user)).exists():
                            return Response("you have already registerd this course!",
                                            status=status.HTTP_403_FORBIDDEN)
                        else:
                            user_course = UserCourse.objects.create(
                                user=user,
                                course=course,
                                child=child_user,
                                expire_at=expire_date,
                                is_active=True
                            )
                    else:
                        return Response("your type is not equal with course type",
                                        status=status.HTTP_403_FORBIDDEN)
                elif request.user.type in [1,2]:
                    if UserCourse.objects.filter(Q(user=request.user) & Q(course=course)).exists():
                        return Response("you have already registerd this course!",
                                        status=status.HTTP_403_FORBIDDEN)
                    else:
                        user_course=UserCourse.objects.create(
                            user=user,
                            course=course,
                            expire_at=expire_date,
                            is_active=True
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
                course = user_course.course
                module = course.module_rel.first()
                first_done_content=module.content_rel.filter(
                    is_done=True
                ).first()
                user_done_content=UserDoneContent.objects.create(
                    user=request.user,
                    content=first_done_content
                )
                user_done_content.save()

                # Content.make_exam_content_writeable(module)
                interval_instance=IntervalSchedule.objects.create(
                    every=expire_date.day,
                    period=IntervalSchedule.DAYS
                )
                PeriodicTask.objects.create(
                    name=f"expire course {user_course.id} ",
                    task="courses.tasks.expire_course",
                    interval=interval_instance,
                    one_off=True,
                    kwargs=json.dumps({
                        "course_id": user_course.id,
                        "user_national_code":request.user.national_code
                    }),
                )
                return Response("course created successfully " , status=status.HTTP_201_CREATED)
        else:
            return Response(ser_data.errors,status=status.HTTP_403_FORBIDDEN)


class SetContentDone(views.APIView):
    def get(self, request, course_id,content_id,object_id):

        session_id = request.GET.get('session')
        session = SessionStore(session_key=session_id)

        # print(session['current_user_child'])
        try:
            if session['current_user_child'] == None:

                user_course_obj = UserCourse.objects.get(Q(user=request.user) &
                                                         Q(id=course_id) & Q(is_active=True))
            else:

                    user = ChildUser.objects.get(national_code=session['current_user_child'])
                    user_course_obj = UserCourse.objects.get(Q(child=user) &
                                                             Q(id=course_id) & Q(is_active=True))
        except Exception as e:
            return Response({'error':str(e)})
        course = user_course_obj.course
        module = course.module_rel.first()
        age = datetime.now(tz=pytz.timezone("Asia/Tehran")) - user_course_obj.created_at
        previous_content = module.content_rel.filter(
            Q(age__lte=age.days) & Q(is_done=True)
        ).order_by("-id").first()
        if previous_content:
            contents = module.content_rel.get(
                Q(age__lte=age.days) &
                Q(pk=content_id) & Q(object_id=object_id)
            )
            UserDoneContent.objects.create(
                user=request.user,
                content=contents
            )
            return Response("content set done successfully",status=status.HTTP_200_OK)
        else:
            return Response("error", status=status.HTTP_403_FORBIDDEN)