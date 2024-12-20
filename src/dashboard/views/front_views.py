from rest_framework import views, status
from dashboard.serializers.front_serializer import *
from rest_framework.response import Response
from courses.models import UserCourse, ModuleSchedule, Course, UserDoneContent, ContentPrerequisite
from courses.serializers.front_serializer import (UserCourseModelSerializer ,
    ModuleScheduleSerializer , ContentModelSerializer
                                                  )
from django.db.models import Q, OuterRef, Exists
from datetime import datetime
from accounts.models import ChildUser
from accounts.serializers.front_serializer import ChildRegisterSerializer
import pytz
from django.contrib.sessions.backends.db import SessionStore
from exam.models import Evaluation
from exam.serializers.front_serializer import EvaluationModelSerializer
# Create your views here.



class EntryDashboardView(views.APIView):
    """
     when user registered successfully redirects to this view
    """
    def get(self,request):
        session_id=request.GET.get('session')
        session=SessionStore(session_key=session_id)
        session['current_user']=request.user.national_code
        session['current_user_child']=None
        session.save()
        # print(f"current user : {session['current_user']}")
        # print(f"current child : {session['current_user_child']}")
        instance=get_user_model().objects.get(national_code=request.user.national_code)
        ser_data=UserSerializer(instance=instance)
        return Response(ser_data.data,status=status.HTTP_200_OK)



class UserCoursesView(views.APIView):
    """
    show courses that user already registered
    """
    def get(self,request):
        """
        this means user entered in dashboard as child user
        `request.session['current_user_child'] != None:`
        :param request: session_id
        :return: serialize data of UserCourse model
        """
        session_id=request.GET.get("session")
        session=SessionStore(session_key=session_id)
        if session['current_user_child'] != None:
            child=ChildUser.objects.get(national_code=session['current_user_child'])
            obj=UserCourse.objects.filter(Q(user=request.user)& Q(child=child)
                                          & Q(is_active=True) & Q(course__type=child.type)).exclude(
                Q(expire_at__lte=datetime.now(pytz.timezone("Asia/Tehran")))
            )

        else:
            obj = UserCourse.objects.filter(Q(user=request.user)& Q(child=None) & Q(is_active=True))
        ser_data=UserCourseModelSerializer(instance=obj,many=True)
        return Response(ser_data.data)



class UserCourseModules(views.APIView):
    def get(self,request,id):
        user=request.user
        course=Course.objects.get(pk=id)
        current_time= datetime.now()
        user_course_obj=UserCourse.objects.get(
            Q(user=user) &
            Q(course=course)
        )
        module_schedule_obj=ModuleSchedule.objects.filter(
            Q(active_at__lte=current_time) &
            Q(user_course=user_course_obj)
        )
        ser_data=ModuleScheduleSerializer(instance=module_schedule_obj,many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)



class ChangeChildUserView(views.APIView):
    """
    user can enter in dashboard as his/her child user
    """
    def get(self,request,national_code):
        """
        get child national_code and fetch child user form database
        then child object sets as current user in session
        :param request: session_id
        :param national_code: child national code
        :return: child user information
        """
        session_id=request.GET.get('session')
        session=SessionStore(session_key=session_id)
        child=ChildUser.objects.get(national_code=national_code)
        ser_data=ChildRegisterSerializer(instance=child)
        session['current_user_child']=national_code
        session['current_user']=national_code
        session.save()
        # print(f" current child user : {session['current_user_child']}")
        # print(f"current user : {session['current_user']}")
        return Response(ser_data.data,status=status.HTTP_200_OK)



class ShowCourseContentsView(views.APIView):
    """
    user can check contents of course that already registered
    """
    def get(self,request,course_id):
        """
        this means user entered in dashboard as parent user:
        `request.session['current_user_child'] == None:`
        :param request:
        :param course_id: id of course that user can check
        :return:
        """
        try:
            user_course_obj=UserCourse.get_user_course(request=request,course_id=course_id)
            course = user_course_obj.course
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        module=course.module_rel.first()
        age=datetime.now(tz=pytz.timezone("Asia/Tehran")) - user_course_obj.created_at

        all_contents = module.content_rel.filter(
            age__lte=age.days
        ).count()
        all_done_contents=UserDoneContent.objects.filter(user=request.user,
                                                         course=course).count()

        session_id = request.GET.get('session')
        session = SessionStore(session_key=session_id)

        if all_done_contents <= all_contents:
            #chatgpt
            # completed_contents = Content.objects.filter(
            #     content_user_watch_contents__user=request.user,  # Filter by the user
            #     content_user_watch_contents__content_id=OuterRef('prerequisite_content_id')
            #     # Join with prerequisite_content
            # )
            #
            # # Query the ContentPrerequisite table to get the main contents
            # main_contents = ContentPrerequisite.objects.filter(
            #     Exists(completed_contents)  # Filter by the completed_contents subquery
            # ).values('content')
            #
            # # Retrieve the actual Content objects
            # result = Content.objects.filter(id__in=main_contents)

            #end chat gpt
            contents=module.content_rel.filter(
                age__lte=age.days
            )
            ser_data = ContentModelSerializer(instance=contents, many=True,
                                              context={'request': request,
                                                       'course_id':course_id})
        else:
            all_user_childes=request.user.father_child.all()
            sum=0
            bs_child=None
            for child in all_user_childes:
                all_done_child_contents = UserDoneContent.objects.filter(user=request.user,
                                                                   course=course,child=child
                                                                   ).count()
                if all_done_child_contents > sum :
                    sum=all_done_contents
                    bs_child=child

            all_done_contents = UserDoneContent.objects.filter(user=request.user,
                                                               course=course,child=bs_child
                                                               )
            ser_data = UserDoneContentsModelSerializer(instance=all_done_contents, many=True)
        # result = {}
        # for i in ser_data.data:
        #     for key, value in i.items():
        #         if value not in result.values():
        #             result[key] = value

        return Response(ser_data.data,status=status.HTTP_200_OK)




class ModifyChildView(views.APIView):
    """
    modify child information except national code.
    """
    def put(self,request,national_code):
        user=get_user_model().objects.get(national_code=request.user.national_code)
        child=user.father_child.get(national_code=national_code)
        ser_data=ModifyChildSerializer(instance=child,data=request.data,partial=True)
        if ser_data.is_valid():
            ser_data.save()
            new_ser_data=ChildRegisterSerializer(instance=child)
            return Response(new_ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)




class CoursesByChild(views.APIView):
    """
    Status of registered courses by child
    """
    def get(self,request,national_code):
        user_courses=UserCourse.objects.filter(user=request.user,child__national_code=national_code)
        ser_data=UserCourseModelSerializer(instance=user_courses,many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)



class ChildValues(views.APIView):
    def get(self,request,national_code):
        child_values=Evaluation.objects.filter(user=request.user,
                                               child__national_code=national_code)
        ser_data=EvaluationModelSerializer(instance=child_values,many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)