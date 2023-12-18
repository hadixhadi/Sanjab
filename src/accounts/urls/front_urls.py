from django.urls import path
from accounts.views.front_views import *

urlpatterns=[
    path('login-register/',UserSendOtpCode.as_view(),name='login-register'),
    path('phone-verification/',UserOtpCodeVerification.as_view(), name='phone-verification'),
    path('user-register/',UserRegisterationView.as_view(),name='user-register'),
    path('child-register/', ChildRegisterView.as_view(), name='child-register'),

]