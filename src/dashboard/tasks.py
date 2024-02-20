from celery import  shared_task
from django.contrib.auth import get_user_model
from django.db.models import Q
from courses.models import UserCourse
from config.envs import settings
import redis
from .models import SimpleStattic
@shared_task
def count_website_views():
    r=redis.Redis(host='redis',port='6379',db='0')
    keys=r.keys('*')
    unique_ips=set()
    for key in keys:
        value = r.get(key).decode('utf-8')
        unique_ips.add(value)
    simple_statics_obj=SimpleStattic.objects.create(
        views=len(unique_ips),
        type=1
    )
    simple_statics_obj.save()
    r.flushdb()
#
@shared_task
def count_users():
    normal_users=get_user_model().objects.exclude(Q(type=3) | Q(type=4)).count()
    simple_statics_obj = SimpleStattic.objects.create(
        views=normal_users,
        type=2
    )
    simple_statics_obj.save()

@shared_task
def count_all_registered_courses():
     all_registered_courses=UserCourse.objects.all().count()
     simple_statics_obj = SimpleStattic.objects.create(
         views=all_registered_courses,
         type=3
     )
     simple_statics_obj.save()
