import json
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django_celery_beat.models import IntervalSchedule, PeriodicTask

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
    is_done=models.BooleanField(default=False)
    is_exam_writeable=models.BooleanField(default=False)
    age=models.SmallIntegerField()
    def __str__(self):
        return self.name

    # @classmethod
    # def make_exam_content_writeable(cls, user_module):
    #
    #     module = user_module
    #     exam_contents = module.content_rel.filter(
    #         content_type__model='exam'
    #     )
    #     interval_date = 1
    #     for exam_content in exam_contents.reverse():
    #         print(exam_content.subject)
    #         interval_instance = IntervalSchedule.objects.create(
    #             every=interval_date,
    #             period=IntervalSchedule.MINUTES
    #         )
    #         PeriodicTask.objects.create(
    #             name=f"make {exam_content} writeable ",
    #             task="courses.tasks.make_content_exam_writeable_task",
    #             interval=interval_instance,
    #             one_off=True,
    #             kwargs=json.dumps({
    #                 "exam_content_id": exam_content.id,
    #                 "module_id":module.id
    #             }),
    #         )
    #         interval_date += 1
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

    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="user_watch_contents")
    content=models.ForeignKey(Content,on_delete=models.CASCADE,
                              related_name="content_user_watch_contents"
                              ,null=True,blank=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    watch_at=models.DateTimeField(auto_now_add=True)