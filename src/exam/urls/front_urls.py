from django.urls import path
from exam.views.front_views import *
urlpatterns=[
    path('qs-list', FrontShowQuestions.as_view({'get': 'list'})),
    path('qs-post/', FrontShowQuestions.as_view({'post': 'create'})),
]