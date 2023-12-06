from django.urls import path
from accounts.views.front_views import *
urlpatterns=[
    path('parent-register/',UserRegisterView.as_view(),name='parent-register'),
    path('phone-verification/', UserPhoneVeryfication.as_view(), name='phone-verification'),
    path('child-register/', ChildRegisterView.as_view(), name='child-register'),
    path('dashboard/',UserAdminDashboard.as_view({"get":"list"}),name='dashboard'),

]