from datetime import datetime
import pytz
from django.contrib.sessions.backends.db import SessionStore
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, views, status
from accounts.models import ChildUser
from exam.serializers.front_serializer import *
from rest_framework.permissions import IsAuthenticated
from exam.permissions.permissions import *
# Create your views here.
class FrontShowQuestions(views.APIView):
    permission_classes = [IsAuthenticated,IsOwner]
    def get(self, request, course_id,content_id):
        """
        show questions of exam
        this means user entered in dashboard as parent user:
        `request.session['current_user_child'] == None:`
        :param request:
        :param course_id: id of course that user can check
        :return:
        """
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
        except:
            return Response("there is not registered course ", status=status.HTTP_200_OK)
        self.check_object_permissions(request,user_course_obj)
        course = user_course_obj.course
        module = course.module_rel.first()
        age = datetime.now(tz=pytz.timezone("Asia/Tehran")) - user_course_obj.created_at
        previous_content = module.content_rel.filter(
            Q(age__lte=age.days) & Q(is_done=True)
        ).order_by("-id").first()
        if previous_content:
            contents = module.content_rel.filter(
                Q(age__lte=age.days) & Q(content_type__model='exam') &
                Q(pk=content_id)
            )
            # print("contents : ",len(contents))
        else:
            contents = None
        ser_data = ShowExamSerializer(instance=contents, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


