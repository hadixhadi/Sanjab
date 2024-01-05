from django.urls import path
from exam.views.front_views import *
urlpatterns=[
    path('qs-list/<int:course_id>/<int:content_id>/', FrontShowQuestions.as_view()),
    path('qs-post/', FrontShowQuestions.as_view()),
]