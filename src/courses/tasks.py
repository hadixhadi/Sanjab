from celery import shared_task
from django.db.models import Q
from requests import Response
from accounts.models import User
from .models import UserCourse, Module, Content


@shared_task
def expire_course(user_national_code,course_id):
    try:
        user=User.objects.get(national_code=user_national_code)
        user_course=UserCourse.objects.get(Q(user=user)&Q(id=course_id))
        user_course.is_active=False
        user_course.save()
    except Exception as e:
        return e


@shared_task
def make_content_exam_writeable_task(module_id,exam_content_id):
    module=Module.objects.get(pk=module_id)
    content=Content.objects.get(Q(pk=exam_content_id) & Q(module=module))
    content.is_exam_writeable=True
    content.save()

