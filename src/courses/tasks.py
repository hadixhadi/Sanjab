from celery import shared_task
from django.db.models import Q
from requests import Response
from accounts.models import User
from .models import UserCourse

@shared_task
def expire_course(user_national_code,course_id):
    try:
        user=User.objects.get(national_code=user_national_code)
        user_course=UserCourse.objects.get(Q(user=user)&Q(id=course_id))
        user_course.is_active=False
        user_course.save()
    except Exception as e:
        return e
