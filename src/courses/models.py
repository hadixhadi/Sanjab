import json
from datetime import datetime , timedelta
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models, transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.contrib.sessions.backends.db import SessionStore
from rest_framework.response import Response
from rest_framework import status
import pytz
from accounts.models import ChildUser

# Create your models here.

class Course(models.Model):
    TYPE=[
        (1,'4-7'),
        (2,'8-11'),
        (3,'12-15'),
        (4,'PARENT')
    ]
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.BigIntegerField()
    type=models.SmallIntegerField(choices=TYPE)
    def __str__(self):
        return self.name


class CourseSettings(models.Model):
    title=models.CharField(max_length=50,null=True)
    expire_day=models.SmallIntegerField()




class Module(models.Model):
    name=models.CharField(max_length=200)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="module_rel")

    def __str__(self):
        return self.name





class Content(models.Model):
    module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name="content_rel")
    name=models.CharField(max_length=200)

    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    is_active=models.BooleanField(default=False,null=True,blank=True)
    is_exam_writeable=models.BooleanField(default=False)
    age=models.SmallIntegerField()
    def __str__(self):
        return self.name





class UserCourse(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="user_courses")
    course=models.ForeignKey(Course,on_delete=models.PROTECT,related_name="user_course_rel")
    created_at=models.DateTimeField(auto_now_add=True)
    child = models.ForeignKey(ChildUser, on_delete=models.CASCADE,
                              related_name="child_user_course", null=True, blank=True)
    expire_at=models.DateTimeField()
    is_active=models.BooleanField(default=False)
    is_graduated=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user} - {self.course}"

    @classmethod
    def create_user_course(cls,request,ser_data):
        user = request.user
        with transaction.atomic():
            session = SessionStore(ser_data.validated_data['session_id'])
            course_id = ser_data.validated_data['course']
            course = Course.objects.get(pk=course_id)
            course_setting=CourseSettings.objects.get()
            expire_day=course_setting.expire_day
            expire_date = datetime.now() + timedelta(days=expire_day)

            # if user enter dashboard as child user
            if session['current_user_child'] != None:
                child_user = ChildUser.objects.get(national_code=session['current_user_child'])

                if course.type == child_user.type:

                    user_course_obj_bool = UserCourse.objects.filter(Q(user=request.user) & Q(child=child_user)&
                                                                     Q(course=course)).exist()
                    if user_course_obj_bool:
                        user_course_obj = UserCourse.objects.get(Q(user=request.user) & Q(child=child_user)&
                                                                 Q(course=course))
                        if user_course_obj.is_active:
                            return Response("you have already registered this course!",
                                            status=status.HTTP_403_FORBIDDEN)
                        else:
                            user_course_obj.expire_at = expire_date
                            user_course_obj.is_active = True
                            user_course_obj.save()
                            user_course = user_course_obj
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
            elif request.user.type in [1, 2]:
                user_course_obj_bool=UserCourse.objects.filter(Q(user=request.user) &
                                                          Q(course=course)).exists()

                if user_course_obj_bool:
                    user_course_obj= UserCourse.objects.get(Q(user=request.user) &
                                                             Q(course=course))
                    if user_course_obj.is_active:
                        return Response("you have already registered this course!",
                                        status=status.HTTP_403_FORBIDDEN)
                    else:
                        user_course_obj.expire_at = expire_date
                        user_course_obj.is_active = True
                        user_course_obj.save()
                        user_course = user_course_obj

                else:
                    user_course = UserCourse.objects.create(
                        user=user,
                        course=course,
                        expire_at=expire_date,
                        is_active=True
                    )
            else:
                return Response("your type is not equal with course type",
                                status=status.HTTP_403_FORBIDDEN)
            modules = course.module_rel.all()
            active_at = datetime.now()
            for module in modules:
                ModuleSchedule.objects.create(
                    user_course=user_course,
                    module=module,
                    active_at=active_at,

                )
                active_at = datetime.now() + timedelta(days=90)
            user_course.save()
            # course = user_course.course
            # module = course.module_rel.first()
            # first_done_content = module.content_rel.first()
            # user_done_content = UserDoneContent.objects.create(
            #     user=request.user,
            #     content=first_done_content
            # )
            # user_done_content.save()

            interval_instance = IntervalSchedule.objects.create(
                every=expire_date.day,
                period=IntervalSchedule.DAYS
            )
            try:
                PeriodicTask.objects.create(
                    name=f"expire course {user_course.id} ",
                    task="courses.tasks.expire_course",
                    interval=interval_instance,
                    one_off=True,
                    kwargs=json.dumps({
                        "course_id": user_course.id,
                        "user_national_code": request.user.national_code
                    }),
                )
            except:
                per_task=PeriodicTask.objects.get(name=f"expire course {user_course.id} ")
                per_task.interval=interval_instance
                per_task.enabled=True
                per_task.save()
            return Response("course created successfully ", status=status.HTTP_201_CREATED)

    @classmethod
    def get_user_course(cls,request,course_id):
        session_id = request.GET.get('session')
        session = SessionStore(session_key=session_id)
        try:
            if session['current_user_child'] == None:
                user_course_obj = UserCourse.objects.get(Q(user=request.user) &
                                                         Q(id=course_id) & Q(is_active=True))
            else:

                user = ChildUser.objects.get(national_code=session['current_user_child'])
                user_course_obj = UserCourse.objects.get(Q(child=user) &
                                                         Q(id=course_id) & Q(is_active=True))
        except Exception as e:
            raise e
            # return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return user_course_obj




class ModuleSchedule(models.Model):
    user_course=models.ForeignKey(UserCourse,on_delete=models.CASCADE,
                                  related_name="user_course_moduleschedule")
    module=models.ForeignKey(Module,on_delete=models.CASCADE,
                             related_name="module_schedule")
    child=models.ForeignKey(ChildUser,on_delete=models.CASCADE,
                            related_name="child_module_schedule",null=True,blank=True)
    active_at=models.DateTimeField()




class VideoContents(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    url=models.URLField(max_length=300)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name="video content"
        verbose_name_plural="video contents"



class CourseInformation(models.Model):
    title=models.CharField(max_length=200,null=True,blank=True)
    description=models.TextField(null=True,blank=True)



class UserDoneContent(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,
                           related_name="user_watch_contents")
    child=models.ForeignKey(ChildUser,on_delete=models.CASCADE,
                            related_name="child_user_done_content_rel",null=True)
    content=models.ForeignKey(Content,on_delete=models.CASCADE,
                              related_name="content_user_watch_contents"
                              ,null=True,blank=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    watch_at=models.DateTimeField(auto_now_add=True)


    @classmethod
    def create_user_done_content(cls, request, user_course_obj,
                                 content_id, object_id, course_id):
        course = user_course_obj.course
        module = course.module_rel.first()
        age = datetime.now(tz=pytz.timezone("Asia/Tehran")) - user_course_obj.created_at

        session_id=request.GET.get('session')
        session=SessionStore(session_key=session_id)

        contents = module.content_rel.get(
            Q(age__lte=age.days) &
            Q(pk=content_id) & Q(object_id=object_id)
        )

        user_done_content_obj=None
        print(contents.content_type.id)
        try:
            user_done_content_obj = get_object_or_404(UserDoneContent,
                                                      user=request.user,
                                                      content=contents)
            if user_done_content_obj is not None:
                return Response('this content set done already!',
                                status=status.HTTP_403_FORBIDDEN)
        except :
            if not user_done_content_obj and contents.content_type.id != 6:

                done_content_obj=UserDoneContent.objects.create(
                    user=request.user,
                    content=contents,
                    course=course
                )
                if session['current_user_child'] != None:
                    child_national_code = session['current_user_child']
                    child = ChildUser.objects.get(national_code=child_national_code)
                    done_content_obj.child=child
                done_content_obj.save()
                return Response("content set done successfully", status=status.HTTP_200_OK)
        return Response("error", status=status.HTTP_403_FORBIDDEN)



class ContentPrerequisite(models.Model):
    prerequisite_content = models.ForeignKey(Content,
                                                  on_delete=models.CASCADE,
                                             related_name="prerequisite_content")
    content = models.ForeignKey(Content,
                                     on_delete=models.CASCADE,related_name="main_content")

    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="prerequisite_course")
