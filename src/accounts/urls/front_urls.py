from django.urls import path
from accounts.views.front_views import *
urlpatterns=[
    path('register/',UserRegisterView.as_view(),name='user-register'),
    path('child-register/', ChildRegisterView.as_view(), name='child-register'),

]