import os
from celery import Celery
from celery.schedules import schedule, crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.envs.developSettings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
CELERY_TIMEZONE = "Asia/Tehran"
app.conf.broker_url = 'amqp://rabbitmq'
CELERY_RESULT_BACKEND = 'django-db'

app.conf.beat_schedule={
    'flush-expire-tokens-database': {
        'task': 'accounts.tasks.flush_expired_token',
        'schedule': crontab(hour=3,minute=0),  # Run every 12 hours
    },
    'count-all-site-views': {
        'task': 'dashboard.tasks.count_website_views',
        'schedule': crontab(hour=2,minute=30),  # Run every 12 hours
    },
    'count-all-registered-courses': {
        'task': 'dashboard.tasks.count_all_registered_courses',
        'schedule': crontab(hour=2,minute=40),  # Run every 12 hours
    },
    'count-all-registered-users': {
        'task': 'dashboard.tasks.count_users',
        'schedule': crontab(hour=2,minute=50),  # Run every 12 hours
    },
}


