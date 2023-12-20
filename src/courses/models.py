from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
# Create your models here.

class Course(models.Model):
    TYPE=[
        (1,'4-7'),
        (2,'8-11'),
        (3,'12-15')
    ]
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.BigIntegerField()
    type=models.SmallIntegerField(choices=TYPE)

    def __str__(self):
        return self.name
class Module(models.Model):
    name=models.CharField(max_length=200)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="module")

    def __str__(self):
        return self.name

class Content(models.Model):
    module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name="content")
    name=models.CharField(max_length=200)

    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name
class UserCourse(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="user_courses")
    course=models.ForeignKey(Course,on_delete=models.PROTECT)
    created_at=models.DateTimeField(auto_now_add=True)
    expire_at=models.DateTimeField()
    def __str__(self):
        return f"{self.user} - {self.course}"

class ModuleSchedule(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="user_module")
    module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name="module_schedule")
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_module_schedule")
    active_at=models.DateTimeField()