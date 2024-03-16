from datetime import datetime
import pytz
from django.http import JsonResponse
from rest_framework import viewsets, views, status

from accounts.models import ChildUser
from exam.serializers.front_serializer import *
from rest_framework.permissions import IsAuthenticated
from exam.permissions.permissions import *
from courses.models import UserDoneContent
from django.contrib.sessions.backends.db import SessionStore

class FrontShowQuestions(views.APIView):
    permission_classes = [IsAuthenticated,IsOwner]
    def get(self, request, course_id,content_id):
        """
        show questions of exam
        this means user entered in dashboard as parent user:
        `request.session['current_user_child'] == None:`
        :param request:
        :param course_id: user registered course ID
        :param content_id: main id of content (top id)
        :return:
        """
        try:
            user_course_obj=UserCourse.get_user_course(request=request,course_id=course_id)
            course = user_course_obj.course
        except Exception as e:
            return Response(user_course_obj.data,status=status.HTTP_400_BAD_REQUEST)
        module = course.module_rel.first()
        age = datetime.now(tz=pytz.timezone("Asia/Tehran")) - user_course_obj.created_at

        session_id = request.GET.get('session')
        session = SessionStore(session_key=session_id)

        user_done_content_obj = UserDoneContent.objects.filter(course=course, user=request.user,
                                                               content__id=content_id)
        if session['current_user_child']!=None:
            child_national_code = session['current_user_child']
            child = ChildUser.objects.get(national_code=child_national_code)
            user_done_content_obj=UserDoneContent.objects.filter(course=course,user=request.user,
                                                  content__id=content_id,child=child)
        if not user_done_content_obj.exists():
            contents = module.content_rel.filter(
                Q(age__lte=age.days) & Q(content_type__model='exam') &
                Q(pk=content_id)
            )
            ser_data = ShowExamSerializer(instance=contents, many=True)
            return Response(ser_data.data, status=status.HTTP_200_OK)

        else:
            return JsonResponse({
                "exam_is_done":True
            })


class CommitExam(views.APIView):
    def post(self, request, course_id,content_id,):
        """
        show questions of exam
        this means user entered in dashboard as parent user:
        `request.session['current_user_child'] == None:`
        :param request:
        :param course_id: id of course that user can check
        :return:
        """

        user_course_obj=UserCourse.get_user_course(request=request,course_id=course_id)
        course = user_course_obj.course
        module = course.module_rel.first()
        age = datetime.now(tz=pytz.timezone("Asia/Tehran")) - user_course_obj.created_at
        content_exam = module.content_rel.get(
                Q(age__lte=age.days) & Q(content_type__model='exam') &
                Q(pk=content_id)
            )

        ser_data=UserAnswerSerializer(data=request.data,context={'request':request,
                                                                 'content_exam':content_exam,
                                                                 'course_id':course_id})
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
        else:
            return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

        return Response(ser_data.data,status=status.HTTP_200_OK)

